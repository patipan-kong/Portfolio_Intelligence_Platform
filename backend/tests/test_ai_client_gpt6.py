"""
Regression tests for GPT-6 Sol/Luna OpenAI-compatibility (max_completion_tokens
vs. max_tokens) and the optimizer's failure semantics around it.

Root cause (services/ai_client.py `call_ai`, OpenAI-compatible branch):
`_REASONING_PATTERNS` gates which model IDs receive `max_completion_tokens`
instead of the legacy `max_tokens` parameter. GPT-6 model IDs ("gpt-6-sol",
"gpt-6-luna") were missing from that tuple, so calls used `max_tokens`, which
the real OpenAI API rejects for reasoning-family models with:

    "Unsupported parameter: 'max_tokens' is not supported with this model.
     Use 'max_completion_tokens' instead."

That exception propagated out of optimizer.py's per-layer try/except, left
Layer 2's target_allocations empty, and triggered the "L2 allocation plan
empty after all layers attempted" RuntimeError -> global single-shot
fallback. All provider calls are mocked; no network calls or paid tokens
are used.
"""

import os
import sys

import openai
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import services.ai_client as ai_client
import agents.optimizer as optimizer_module


# ─── Fakes for the OpenAI-compatible SDK surface ───────────────────────────

class _FakeMessage:
    def __init__(self, content):
        self.content = content
        self.model_extra = {}


class _FakeChoice:
    def __init__(self, content):
        self.message = _FakeMessage(content)


class _FakeUsage:
    def __init__(self, prompt_tokens=10, completion_tokens=5):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens


class _FakeChatResponse:
    def __init__(self, content='{"ok": true}'):
        self.choices = [_FakeChoice(content)]
        self.usage = _FakeUsage()


class _RecordingOpenAIClient:
    """Captures the kwargs passed to chat.completions.create(). Never raises."""

    last_kwargs: dict | None = None

    def __init__(self, api_key=None, base_url=None):
        self.chat = self

    @property
    def completions(self):
        return self

    def create(self, **kwargs):
        _RecordingOpenAIClient.last_kwargs = kwargs
        return _FakeChatResponse()


class _StrictOpenAIClient:
    """Simulates the real OpenAI API's parameter validation: rejects
    `max_tokens` for reasoning-family models and `max_completion_tokens` for
    everything else, exactly like the live "Unsupported parameter" error.
    Returns a per-model canned JSON body (from `responses`) on success.
    """

    # independently duplicated from OpenAI's own documented reasoning-model
    # list, NOT imported from ai_client — this must reflect real API
    # behavior, not mirror whatever the implementation currently does.
    _REASONING_MODELS = ("gpt-5", "gpt-6", "o1", "o3", "o4")

    def __init__(self, responses: dict, api_key=None, base_url=None):
        self._responses = responses
        self.chat = self

    @property
    def completions(self):
        return self

    def create(self, **kwargs):
        model = kwargs.get("model", "")
        is_reasoning = any(pat in model for pat in self._REASONING_MODELS)
        if is_reasoning and "max_tokens" in kwargs:
            raise openai.BadRequestError(
                "Unsupported parameter: 'max_tokens' is not supported with "
                "this model. Use 'max_completion_tokens' instead.",
                response=_fake_httpx_response(),
                body=None,
            )
        if not is_reasoning and "max_completion_tokens" in kwargs:
            raise openai.BadRequestError(
                "Unsupported parameter: 'max_completion_tokens' is not "
                "supported with this model. Use 'max_tokens' instead.",
                response=_fake_httpx_response(),
                body=None,
            )
        if model not in self._responses:
            raise AssertionError(f"unexpected model in test double: {model!r}")
        return _FakeChatResponse(self._responses[model])


def _fake_httpx_response():
    import httpx
    return httpx.Response(
        400, request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
    )


@pytest.fixture(autouse=True)
def _no_db_writes(monkeypatch):
    """These tests exercise the real call_ai() parameter-selection logic;
    stub out DB usage recording so no test touches the database."""
    monkeypatch.setattr(ai_client, "_record_usage", lambda *a, **k: None)


# ─── 1-2. GPT-6 Sol / Luna use max_completion_tokens ───────────────────────

@pytest.mark.parametrize("model", ["gpt-6-sol", "gpt-6-luna"])
def test_gpt6_models_use_max_completion_tokens(monkeypatch, model):
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _RecordingOpenAIClient(**kw))
    ai_client.call_ai("prompt", "openai", model, max_tokens=2048)
    kwargs = _RecordingOpenAIClient.last_kwargs
    assert "max_completion_tokens" in kwargs
    assert kwargs["max_completion_tokens"] == 2048
    assert "max_tokens" not in kwargs


# ─── 3. Legacy OpenAI models remain on max_tokens ──────────────────────────

@pytest.mark.parametrize("model", ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"])
def test_legacy_openai_models_still_use_max_tokens(monkeypatch, model):
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _RecordingOpenAIClient(**kw))
    ai_client.call_ai("prompt", "openai", model, max_tokens=2048)
    kwargs = _RecordingOpenAIClient.last_kwargs
    assert "max_tokens" in kwargs
    assert kwargs["max_tokens"] == 2048
    assert "max_completion_tokens" not in kwargs


# ─── 4. Pre-existing gpt-5/o-series behavior is preserved ─────────────────

@pytest.mark.parametrize("model", ["gpt-5.6-terra", "o1-preview", "o3-mini", "o4-mini"])
def test_preexisting_reasoning_models_unaffected_by_gpt6_fix(monkeypatch, model):
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _RecordingOpenAIClient(**kw))
    ai_client.call_ai("prompt", "openai", model, max_tokens=2048)
    kwargs = _RecordingOpenAIClient.last_kwargs
    assert "max_completion_tokens" in kwargs
    assert "max_tokens" not in kwargs


# ─── 5. Non-OpenAI providers on the OpenAI-compatible branch (deepseek) ───

def test_deepseek_non_reasoning_model_still_uses_max_tokens(monkeypatch):
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _RecordingOpenAIClient(**kw))
    ai_client.call_ai("prompt", "deepseek", "deepseek-chat", max_tokens=2048)
    kwargs = _RecordingOpenAIClient.last_kwargs
    assert "max_tokens" in kwargs
    assert "max_completion_tokens" not in kwargs


# ─── 6. Simulated real API: GPT-6 no longer raises "Unsupported parameter" ─

@pytest.mark.parametrize("model", ["gpt-6-sol", "gpt-6-luna"])
def test_gpt6_call_does_not_raise_against_simulated_api(monkeypatch, model):
    responses = {model: '{"status": "REBALANCE"}'}
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _StrictOpenAIClient(responses, **kw))
    result = ai_client.call_ai("prompt", "openai", model, max_tokens=2048)
    assert result["text"] == '{"status": "REBALANCE"}'


# ─── 7. Anthropic / Gemini paths are structurally unaffected ──────────────

class _FakeAnthropicContentBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class _FakeAnthropicMessage:
    def __init__(self, text):
        self.content = [_FakeAnthropicContentBlock(text)]
        self.stop_reason = "end_turn"
        self.model = "claude-sonnet-4-6"
        self.usage = _FakeUsage(prompt_tokens=20, completion_tokens=8)


class _FakeAnthropicMessages:
    def create(self, model, max_tokens, thinking, messages):
        return _FakeAnthropicMessage('{"layer": "anthropic-untouched"}')


class _FakeAnthropicClient:
    def __init__(self, api_key=None):
        self.messages = _FakeAnthropicMessages()


def test_anthropic_path_unaffected_by_reasoning_pattern_change(monkeypatch):
    import anthropic
    monkeypatch.setattr(anthropic, "Anthropic", lambda api_key=None: _FakeAnthropicClient())
    result = ai_client.call_ai("prompt", "anthropic", "claude-sonnet-4-6", max_tokens=1024)
    assert result["text"] == '{"layer": "anthropic-untouched"}'
    assert result["provider"] == "anthropic"


class _FakeGeminiUsageMeta:
    def __init__(self):
        self.prompt_token_count = 12
        self.candidates_token_count = 6


class _FakeGeminiResponse:
    def __init__(self, text):
        self.text = text
        self.usage_metadata = _FakeGeminiUsageMeta()


class _FakeGeminiModels:
    def generate_content(self, model, contents, config):
        return _FakeGeminiResponse('{"layer": "gemini-untouched"}')


class _FakeGeminiClient:
    def __init__(self, api_key=None):
        self.models = _FakeGeminiModels()


def test_gemini_path_unaffected_by_reasoning_pattern_change(monkeypatch):
    from google import genai as google_genai
    monkeypatch.setattr(google_genai, "Client", lambda api_key=None: _FakeGeminiClient())
    result = ai_client.call_ai("prompt", "gemini", "gemini-3.8-flash", max_tokens=1024)
    assert result["text"] == '{"layer": "gemini-untouched"}'
    assert result["provider"] == "gemini"


# ─── 8. Optimizer integration: GPT-6 in L2/L3 does not trigger fallback ───

def test_optimizer_layer2_layer3_gpt6_do_not_trigger_global_fallback(monkeypatch):
    """End-to-end through the real call_ai() + real OpenAI-compatible branch:
    before the fix, this exact layer setup (L2/L3 on GPT-6) raised
    "Unsupported parameter: 'max_tokens'" out of Layer 2, which optimizer.py
    treats as "L2 allocation plan empty" and routes to the emergency
    single-shot fallback. After the fix, the 3-layer pipeline must complete
    normally and never call the fallback.
    """
    responses = {
        "gpt-4o": '{"swaps": [], "top_buys": [], "sector_flags": [], "priority": ""}',
        "gpt-6-sol": '{"allocations": [{"s": "A", "tw": 25, "sig": "BUY", "r": "buy"}], "status": "REBALANCE"}',
        "gpt-6-luna": '{"risk_flags": [], "safer_choice": "layer2", "final_risk_level": "low"}',
    }
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _StrictOpenAIClient(responses, **kw))
    monkeypatch.setattr(
        optimizer_module, "_run_single_shot_fallback",
        lambda *a, **k: pytest.fail("GPT-6 layers must not trigger the global fallback"),
    )

    layers = {
        "layer1": {"name": "Strategist", "role": "Strategist", "provider": "openai", "model": "gpt-4o"},
        "layer2": {"name": "Challenger", "role": "Challenger", "provider": "openai", "model": "gpt-6-sol"},
        "layer3": {"name": "Risk Auditor", "role": "Risk Auditor", "provider": "openai", "model": "gpt-6-luna"},
    }

    result = optimizer_module.run_layered_optimizer(
        [{"symbol": "A", "shares": 1, "current_price": 100, "signal": "BUY", "sector": "Technology"}],
        [], "P", layers=layers,
    )

    assert "error" not in result["layer2_result"]
    assert "error" not in result["layer3_result"]
    assert result["target_allocations"]
    assert "fallback_mode" not in result
