"""Offline canonical-context contract and real endpoint serialization checks."""
import asyncio
import hashlib
import json
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.database import Base, OptimizerHistory
import models.asset
import models.registry_finding
from services import registry_service, registry_lookup
from services.asset_domain import AssetClaim, AssetType, IdentifierRecord, IdentifierType, RelationshipType
from services.execution_instrument_facts import resolve_execution_instruments
from services.optimizer.execution_penalty import compute_portfolio_execution_context, build_execution_prompt_block
from services.optimizer.instrument_context import build_instrument_context, VERSION
from agents.optimizer import _layer1_prompt, _layer2_prompt, _layer3_prompt

PAIRS = [('AAPL01.BK', 'AAPL'), ('GOOGL01.BK', 'GOOGL'), ('MICRON01.BK', 'MU'), ('NVDA01.BK', 'NVDA')]


@pytest.fixture
def db():
    registry_lookup.invalidate_cache()
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    yield session
    session.close()
    registry_lookup.invalidate_cache()


def mint(db, symbol, local=True):
    return registry_service.mint_asset(db, AssetClaim(symbol, AssetType.EQUITY,
        'Thailand' if local else 'US', 'SET' if local else 'NASDAQ', 'THB' if local else 'USD'),
        identifiers=[IdentifierRecord(IdentifierType.PROVIDER_SYMBOL, symbol, 'official-fixture')])


def prepare(db):
    for local, foreign in PAIRS:
        a, u = mint(db, local), mint(db, foreign, False)
        registry_service.link_relationship(db, a.id, u.id, RelationshipType.DEPOSITARY_RECEIPT_OF)
    mint(db, 'PTT.BK')
    db.commit()
    symbols = [p[0] for p in PAIRS] + ['PTT.BK', 'UNKNOWN01.BK']
    facts = resolve_execution_instruments(db, symbols)
    execution = compute_portfolio_execution_context({s: {} for s in symbols}, facts)
    execution['canonical_instrument_context'] = build_instrument_context(db, symbols, facts, execution)
    return symbols, facts, execution


def test_verified_dr_equity_unknown_units_and_rules(db):
    symbols, facts, execution = prepare(db)
    c = execution['canonical_instrument_context']
    rows = {p['held_symbol']: p for p in c['positions']}
    for local, foreign in PAIRS:
        row = rows[local]
        assert row['classification_verified'] and row['instrument_form'] == 'DEPOSITARY_RECEIPT'
        assert row['underlying']['canonical_symbol'] == foreign
        assert row['underlying']['currency'] == 'USD' and row['local_quote_currency'] == 'THB'
        assert row['execution']['asset_type'] == 'DR' and row['execution']['position_cap_pct'] == 15
        assert any(p['source_value'] == 'DEPOSITARY_RECEIPT_OF' for p in row['classification_provenance'])
    assert rows['PTT.BK']['instrument_form'] == 'EQUITY'
    assert rows['PTT.BK']['underlying'] is None
    assert not rows['UNKNOWN01.BK']['classification_verified']
    assert rows['UNKNOWN01.BK']['instrument_form'] == 'UNKNOWN'
    assert rows['UNKNOWN01.BK']['unresolved_evidence']
    assert c['rules']['dr_basket_guidance'] == {'threshold_pct': 40, 'enforcement': 'PROMPT_ONLY_ADVISORY', 'deterministic_breach_evaluated': False}
    assert c['rules']['execution_position_caps']['actions'] == ['BUY', 'ACCUMULATE']
    assert c['prompt_sha256'] == hashlib.sha256(c['prompt_block'].encode()).hexdigest()


def test_same_serialization_in_all_three_layers(db):
    _, _, execution = prepare(db)
    block = execution['canonical_instrument_context']['prompt_block']
    prompts = [_layer1_prompt([], [], [], [], execution_context=execution),
               _layer2_prompt([], [], {}, execution_context=execution),
               _layer3_prompt({}, {}, execution_context=execution)]
    for prompt in prompts:
        assert prompt.count(block) == 1
        assert 'not an enforced deterministic policy rule' in prompt
        assert 'Instrument form alone is not a BUY/SELL signal' in prompt


def test_missing_underlying_does_not_invent_identity(db, monkeypatch):
    _, facts, execution = prepare(db)
    monkeypatch.setattr(registry_service, 'get_asset', lambda *args: None)
    context = build_instrument_context(db, ['GOOGL01.BK'], facts, execution)
    row = context['positions'][0]
    assert row['underlying'] is None
    assert row['unresolved_evidence'] == ['Canonical underlying identity unavailable']


@pytest.mark.parametrize('fail,expected_layers', [
    ((), ['layer1', 'layer2', 'layer3']),
    (('layer1',), ['layer1_retry', 'layer2', 'layer3']),
    (('layer1', 'layer1_retry', 'layer2'), ['fallback']),
])
def test_endpoint_freezes_exact_shared_context_and_history_never_reclassifies(monkeypatch, fail, expected_layers):
    import main
    from tests.test_advisory_intent_integration import session, seed, patch_pipeline, FakeAI, l2, alloc, run
    from services import execution_instrument_facts
    from services.optimizer import execution_penalty
    db = session()
    held = {s: (1000, True) for s, _ in PAIRS}
    proposal = l2(*(alloc(s, 5, 'HOLD') for s in held))
    ai = FakeAI(proposal, fallback=proposal, fail=fail)
    patch_pipeline(monkeypatch, ai)
    # Restore authoritative producers after the general harness's unrelated stubs.
    monkeypatch.setattr(execution_instrument_facts, 'resolve_execution_instruments', resolve_execution_instruments)
    monkeypatch.setattr(execution_penalty, 'compute_portfolio_execution_context', compute_portfolio_execution_context)
    registry_lookup.invalidate_cache()
    p = seed(db, held, 500000)
    for local, foreign in PAIRS:
        a, u = mint(db, local), mint(db, foreign, False)
        registry_service.link_relationship(db, a.id, u.id, RelationshipType.DEPOSITARY_RECEIPT_OF)
    db.commit()
    result = run(db, p)
    row = db.query(OptimizerHistory).one()
    frozen_json = row.result_json
    captured = json.loads(frozen_json)['execution_context']['canonical_instrument_context']
    assert captured['version'] == VERSION
    assert captured == result['execution_context']['canonical_instrument_context']
    for layer in expected_layers:
        assert captured['prompt_block'] in ai.prompts[layer][0]
    # No canonical context in an old record means no retroactive reconstruction.
    old = OptimizerHistory(workspace_id=p.workspace_id, portfolio_id=p.id,
        portfolio_name=p.name, analyzed_at=datetime(2026, 1, 1),
        result_json=json.dumps({'status': 'NO_ACTION', 'target_allocations': []}))
    db.add(old)
    db.commit()
    old_json = old.result_json
    monkeypatch.setattr(execution_instrument_facts, 'resolve_execution_instruments', lambda *a: pytest.fail('historical Registry read'))
    monkeypatch.setattr(registry_service, 'get_asset', lambda *a: pytest.fail('historical underlying read'))
    read = asyncio.run(main.get_optimizer_history_detail(row.id, db))
    assert read['execution_context']['canonical_instrument_context'] == captured
    historic = asyncio.run(main.get_optimizer_history_detail(old.id, db))
    assert 'execution_context' not in historic
    assert row.result_json == frozen_json and old.result_json == old_json
    db.close()
    registry_lookup.invalidate_cache()
