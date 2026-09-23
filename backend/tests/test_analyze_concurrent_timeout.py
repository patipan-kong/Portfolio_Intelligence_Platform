"""Concurrent Analysis Timeout Alignment + Timing Observability — regression
tests (Wealth OS GPT-6 Luna concurrent timeout investigation/fix).

Root cause (see the read-only investigation): `_analyze_one_concurrent()`
wraps the AI call in a 10 s application-level `asyncio.wait_for`, but the
underlying OpenAI-compatible SDK request had no timeout of its own and
inherited the SDK's ~600 s default. Once a worker thread started that
request, the app-level timeout could not stop it — the thread kept blocking
the shared default ThreadPoolExecutor for its true (potentially minutes-long)
duration, long after the app had already declared failure and moved on. The
logged "AI timeout after N ms" also conflated semaphore queue wait + agent
fetch time + the AI call itself into one misleading number.

The fix, covered here:
  1. `call_ai()` accepts an optional per-request `timeout` (OpenAI-compatible
     branch only, via the SDK's own `.create(timeout=...)` override) — every
     other caller that omits it keeps the existing SDK default unchanged.
  2. `analyze_summary()` forwards an optional `timeout` and tags
     `provider_timeout: True` on its returned error dict specifically when
     the provider-level bound (not some other AI error) fired.
  3. `_analyze_one_concurrent()` passes a bounded provider timeout
     (`_ANALYZE_AI_PROVIDER_TIMEOUT_S`, below the unchanged 10 s app bound
     `_ANALYZE_AI_APP_TIMEOUT_S`) and treats a `provider_timeout`-tagged
     result exactly like the existing `asyncio.TimeoutError` branch — the
     same deterministic fallback, never a cached "AI error" summary — and
     logs queue_wait_ms / agent_fetch_ms / ai_wait_ms / total_ms separately.

All network/provider calls are mocked. No paid API tokens are used. Tests
run sequentially, no sub-agents.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import openai
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base, AnalysisCache, AnalysisHistory

import main
import agents.summary as summary_module
import services.ai_client as ai_client


# ─── Tier 1: call_ai() — bounded per-request timeout passthrough ───────────

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

        class _Msg:
            content = '{"ok": true}'
            model_extra = {}

        class _Choice:
            message = _Msg()

        class _Usage:
            prompt_tokens = 10
            completion_tokens = 5

        class _Resp:
            choices = [_Choice()]
            usage = _Usage()

        return _Resp()


@pytest.fixture(autouse=True)
def _no_db_writes(monkeypatch):
    monkeypatch.setattr(ai_client, "_record_usage", lambda *a, **k: None)


def test_call_ai_forwards_bounded_timeout_to_openai_request(monkeypatch):
    """F.1 — the concurrent-analysis path's bounded timeout reaches the SDK."""
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _RecordingOpenAIClient(**kw))
    ai_client.call_ai("prompt", "openai", "gpt-6-luna", max_tokens=2048, timeout=9.0)
    kwargs = _RecordingOpenAIClient.last_kwargs
    assert kwargs["timeout"] == 9.0


def test_call_ai_omits_timeout_when_caller_does_not_opt_in(monkeypatch):
    """F.2 — unrelated callers (no `timeout=`) keep the SDK's own default;
    no `timeout` kwarg is injected on their behalf."""
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _RecordingOpenAIClient(**kw))
    ai_client.call_ai("prompt", "openai", "gpt-4o", max_tokens=2048)
    kwargs = _RecordingOpenAIClient.last_kwargs
    assert "timeout" not in kwargs


def test_gpt6_max_completion_tokens_intact_alongside_bounded_timeout(monkeypatch):
    """F.6 — the earlier GPT-6 max_completion_tokens compatibility fix is
    unaffected by adding a bounded timeout on the same call."""
    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _RecordingOpenAIClient(**kw))
    ai_client.call_ai("prompt", "openai", "gpt-6-luna", max_tokens=2048, timeout=9.0)
    kwargs = _RecordingOpenAIClient.last_kwargs
    assert kwargs["max_completion_tokens"] == 2048
    assert "max_tokens" not in kwargs
    assert kwargs["timeout"] == 9.0


class _FakeAnthropicContentBlock:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class _FakeAnthropicMessage:
    def __init__(self, text):
        self.content = [_FakeAnthropicContentBlock(text)]
        self.stop_reason = "end_turn"
        self.model = "claude-sonnet-4-6"

        class _Usage:
            input_tokens = 20
            output_tokens = 8

        self.usage = _Usage()


class _FakeAnthropicMessages:
    def create(self, model, max_tokens, thinking, messages):
        return _FakeAnthropicMessage('{"layer": "anthropic-untouched"}')


class _FakeAnthropicClient:
    def __init__(self, api_key=None):
        self.messages = _FakeAnthropicMessages()


def test_anthropic_path_ignores_openai_only_timeout_param(monkeypatch):
    """The `timeout` kwarg is scoped to the OpenAI-compatible branch only —
    passing it through call_ai() for the anthropic provider has no effect on
    (and does not crash) the anthropic branch."""
    import anthropic
    monkeypatch.setattr(anthropic, "Anthropic", lambda api_key=None: _FakeAnthropicClient())
    result = ai_client.call_ai("prompt", "anthropic", "claude-sonnet-4-6", max_tokens=1024, timeout=9.0)
    assert result["text"] == '{"layer": "anthropic-untouched"}'


# ─── Tier 2: analyze_summary() — provider_timeout marker ───────────────────

# Minimal valid technical dict — analyze_summary() short-circuits to
# {"error": "no data available for analysis"} (never calling call_ai() at
# all) when technical/fundamental/news are all None, so these tests need at
# least one real data source to actually reach the call_ai() call.
_VALID_TECH = {"short_term": {"score": 1}, "long_term": {"score": 1}, "ta_score": 1}


def test_analyze_summary_forwards_timeout_to_call_ai(monkeypatch):
    captured = {}

    def _fake_call_ai(*args, **kwargs):
        captured.update(kwargs)
        return {"text": '{"signal":"HOLD","confidence":"low","reasoning":"","risks":""}', "latency_ms": 5}

    monkeypatch.setattr(summary_module, "call_ai", _fake_call_ai)
    summary_module.analyze_summary("AOT.BK", _VALID_TECH, None, None, "openai", "gpt-6-luna", {}, timeout=9.0)
    assert captured["timeout"] == 9.0


def test_analyze_summary_tags_provider_timeout_on_api_timeout_error(monkeypatch):
    """F.5 building block — a simulated provider call that exceeds the
    bounded timeout is distinguishable from a generic AI error."""
    def _boom(*args, **kwargs):
        raise openai.APITimeoutError(request=None)

    monkeypatch.setattr(summary_module, "call_ai", _boom)
    result = summary_module.analyze_summary("AOT.BK", _VALID_TECH, None, None, "openai", "gpt-6-luna", {}, timeout=9.0)
    assert "error" in result
    assert result["provider_timeout"] is True


def test_analyze_summary_generic_error_not_tagged_provider_timeout(monkeypatch):
    def _boom(*args, **kwargs):
        raise ValueError("some other AI failure")

    monkeypatch.setattr(summary_module, "call_ai", _boom)
    result = summary_module.analyze_summary("AOT.BK", _VALID_TECH, None, None, "openai", "gpt-6-luna", {})
    assert "error" in result
    assert "provider_timeout" not in result


# ─── Tier 3: _analyze_one_concurrent() — end-to-end fallback + timing ──────

def _make_sessionmaker():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine), engine


async def _run_analyze(sym, s, src):
    """Fresh semaphore per test run — asyncio.run() gives each test its own
    event loop, and a semaphore must be bound to the loop that awaits it."""
    main._ANALYZE_SEMAPHORE = asyncio.Semaphore(main._ANALYZE_CONCURRENCY)
    return await main._analyze_one_concurrent(1, sym, s, src)


_S = {"analyze_provider": "openai", "analyze_model": "gpt-6-luna"}
_SRC = {"use_ta": True, "use_fa": True, "use_news": True}


async def _fake_fetch_agents_fast(db, sym, src):
    return None, None, None


def test_app_level_timeout_still_returns_deterministic_fallback(monkeypatch):
    """F.3 — the pre-existing asyncio.wait_for(app-level) timeout path keeps
    producing the same deterministic fallback shape as before this change."""
    Session, _engine = _make_sessionmaker()
    monkeypatch.setattr(main, "SessionLocal", Session)
    monkeypatch.setattr(main, "_fetch_agents", _fake_fetch_agents_fast)
    monkeypatch.setattr(main, "_ANALYZE_AI_APP_TIMEOUT_S", 0.05)
    monkeypatch.setattr(main, "_ANALYZE_AI_PROVIDER_TIMEOUT_S", 0.2)  # never fires first here

    def _hangs_forever(*args, **kwargs):
        import time
        time.sleep(2.0)  # simulates a worker thread that never returns in time
        return {"signal": "HOLD"}

    monkeypatch.setattr(main, "analyze_summary", _hangs_forever)

    result = asyncio.run(_run_analyze("AOT.BK", _S, _SRC))

    assert result["ai_fallback_used"] is True
    assert result["summary"]["ai_fallback_used"] is True
    assert result["summary"]["reasoning"] == "Deterministic fallback — AI timeout"
    # total_latency_ms should be close to the app-level bound, not the 2s sleep.
    assert result["total_latency_ms"] < 500


def test_provider_level_timeout_returns_same_fallback_not_cached_error(monkeypatch):
    """F.3/F.5 — when the bounded provider timeout fires first (detected via
    the provider_timeout marker), the outcome must be the SAME deterministic
    fallback as an app-level timeout — not a cached "AI error" summary. This
    is the core fallback-semantics-preservation guarantee of the fix."""
    Session, engine = _make_sessionmaker()
    monkeypatch.setattr(main, "SessionLocal", Session)
    monkeypatch.setattr(main, "_fetch_agents", _fake_fetch_agents_fast)
    monkeypatch.setattr(main, "_ANALYZE_AI_APP_TIMEOUT_S", 5.0)
    monkeypatch.setattr(main, "_ANALYZE_AI_PROVIDER_TIMEOUT_S", 0.05)

    def _provider_timeout_result(*args, **kwargs):
        # Exactly what analyze_summary() returns once it catches
        # openai.APITimeoutError for a bounded-timeout call.
        return {"error": "AI error: Request timed out.", "provider_timeout": True}

    monkeypatch.setattr(main, "analyze_summary", _provider_timeout_result)

    result = asyncio.run(_run_analyze("AOT.BK", _S, _SRC))

    assert result["ai_fallback_used"] is True
    assert result["summary"]["ai_fallback_used"] is True
    assert result["summary"]["reasoning"] == "Deterministic fallback — AI timeout"
    assert "error" not in result["summary"]

    # Must NOT have been cached as an "AI error" AnalysisCache row.
    verify = Session()
    cached = verify.query(AnalysisCache).filter(AnalysisCache.symbol == "AOT.BK").first()
    assert cached is None
    history = verify.query(AnalysisHistory).filter(AnalysisHistory.symbol == "AOT.BK").all()
    assert history == []


def test_success_path_unaffected_by_timeout_alignment(monkeypatch):
    """F.3 — a normal, fast, successful AI response is cached and returned
    exactly as before; the new timing/timeout plumbing is a no-op here."""
    Session, engine = _make_sessionmaker()
    monkeypatch.setattr(main, "SessionLocal", Session)
    monkeypatch.setattr(main, "_fetch_agents", _fake_fetch_agents_fast)
    monkeypatch.setattr(main, "_ANALYZE_AI_APP_TIMEOUT_S", 5.0)
    monkeypatch.setattr(main, "_ANALYZE_AI_PROVIDER_TIMEOUT_S", 4.5)

    def _fast_success(*args, **kwargs):
        return {
            "symbol": "AOT.BK", "signal": "BUY", "confidence": "high",
            "reasoning": "ok", "risks": "none", "executive_summary": "",
            "ai_summary": "", "ai_provider": "openai", "ai_model": "gpt-6-luna",
            "latency_ms": 12,
        }

    monkeypatch.setattr(main, "analyze_summary", _fast_success)

    result = asyncio.run(_run_analyze("AOT.BK", _S, _SRC))

    assert "ai_fallback_used" not in result
    assert result["summary"]["signal"] == "BUY"
    assert result["summary"]["from_cache"] is False

    verify = Session()
    cached = verify.query(AnalysisCache).filter(AnalysisCache.symbol == "AOT.BK").first()
    assert cached is not None
    assert cached.signal == "BUY"


def test_timing_diagnostics_distinguish_queue_fetch_and_ai_wait(monkeypatch, caplog):
    """F.4 — the warning log line reports queue_wait_ms, agent_fetch_ms,
    ai_wait_ms and total_ms as distinct fields, not one conflated number."""
    Session, engine = _make_sessionmaker()
    monkeypatch.setattr(main, "SessionLocal", Session)

    async def _slow_fetch(db, sym, src):
        await asyncio.sleep(0.05)
        return None, None, None

    monkeypatch.setattr(main, "_fetch_agents", _slow_fetch)
    monkeypatch.setattr(main, "_ANALYZE_AI_APP_TIMEOUT_S", 0.03)
    monkeypatch.setattr(main, "_ANALYZE_AI_PROVIDER_TIMEOUT_S", 0.2)

    def _hangs(*args, **kwargs):
        import time
        time.sleep(2.0)
        return {"signal": "HOLD"}

    monkeypatch.setattr(main, "analyze_summary", _hangs)

    with caplog.at_level("WARNING", logger="main"):
        result = asyncio.run(_run_analyze("AOT.BK", _S, _SRC))

    assert result["ai_fallback_used"] is True
    warning_lines = [r.message for r in caplog.records if "AI timeout" in r.message]
    assert warning_lines, "expected an AI timeout warning to be logged"
    line = warning_lines[0]
    assert "queue_wait_ms=" in line
    assert "agent_fetch_ms=" in line
    assert "ai_wait_ms=" in line
    assert "total_ms=" in line
    # agent_fetch_ms should reflect the ~50ms artificial fetch delay, proving
    # the split is measuring real, distinct phases rather than being cosmetic.
    import re
    fetch_ms = int(re.search(r"agent_fetch_ms=(\d+)", line).group(1))
    assert fetch_ms >= 30  # generous lower bound vs. the 50ms sleep, avoids CI flakiness


def test_provider_timeout_does_not_rely_on_sdk_default_600s(monkeypatch):
    """F.5 — end-to-end: a simulated OpenAI-compatible call that exceeds the
    bounded provider timeout resolves via analyze_summary()'s own
    openai.APITimeoutError handling well within the app-level window, never
    depending on (or waiting anywhere near) the SDK's ~600s default."""
    class _HangingClient:
        def __init__(self, api_key=None, base_url=None):
            self.chat = self

        @property
        def completions(self):
            return self

        def create(self, **kwargs):
            assert kwargs.get("timeout") == main._ANALYZE_AI_PROVIDER_TIMEOUT_S
            # Simulate the SDK itself enforcing the bounded timeout it was given.
            raise openai.APITimeoutError(request=None)

    monkeypatch.setattr(openai, "OpenAI", lambda **kw: _HangingClient(**kw))

    async def _fetch_valid_tech(db, sym, src):
        # analyze_summary() short-circuits before ever calling call_ai() if
        # technical/fundamental/news are all None — give it real data so the
        # call actually reaches the (hanging) OpenAI client.
        return _VALID_TECH, None, None

    Session, engine = _make_sessionmaker()
    monkeypatch.setattr(main, "SessionLocal", Session)
    monkeypatch.setattr(main, "_fetch_agents", _fetch_valid_tech)
    monkeypatch.setattr(main, "_ANALYZE_AI_APP_TIMEOUT_S", 5.0)
    monkeypatch.setattr(main, "_ANALYZE_AI_PROVIDER_TIMEOUT_S", 0.05)

    import time
    start = time.perf_counter()
    result = asyncio.run(_run_analyze("AOT.BK", _S, _SRC))
    elapsed = time.perf_counter() - start

    assert result["ai_fallback_used"] is True
    assert elapsed < 1.0  # nowhere near the SDK's ~600s default
