"""Explicit offline command; never imported by production runtime.

Capture uses one repeatable-read, READ ONLY PostgreSQL transaction. Replay uses
saved JSON. Both avoid app/model imports, cache helpers and market/AI clients.
"""
from __future__ import annotations

import argparse
import json
import importlib.metadata
import sys
from datetime import datetime, timezone
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from services.candidate_discovery_evidence import (  # noqa: E402
    FA_SOURCE, LEGACY_SOURCE, TIMING_SOURCE, compare_capture, source_digest,
)


def _json_default(value):
    if isinstance(value, datetime):
        return value.replace(tzinfo=value.tzinfo or timezone.utc).astimezone(timezone.utc).isoformat()
    raise TypeError(type(value).__name__)


def capture_current(workspace_id: int, env_file: Path) -> dict:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from dotenv import dotenv_values
    from services.symbol_normalization import get_yfinance_symbol

    url = dotenv_values(env_file).get("DATABASE_URL")
    if not url or not url.startswith(("postgresql://", "postgres://")):
        raise ValueError("capture requires configured PostgreSQL; use --input for offline replay")
    connection = psycopg2.connect(url, connect_timeout=5)
    connection.set_session(isolation_level="REPEATABLE READ", readonly=True, autocommit=False)
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            def read(sql, params=()):
                cursor.execute(sql, params)
                return [dict(row) for row in cursor.fetchall()]

            as_of = read("SELECT transaction_timestamp() AS timestamp")[0]["timestamp"]
            watchlist = read("SELECT id,symbol,sector,asset_id FROM watchlist "
                             "WHERE workspace_id=%s ORDER BY id", (workspace_id,))
            for row in watchlist:
                row["timing_fetch_symbol"] = get_yfinance_symbol(row["symbol"])
                row["timing_symbol_source"] = "services.symbol_normalization.get_yfinance_symbol"
            capture = {"capture_version": "wealth.shadow-capture.v1",
                "universe_id": f"workspace:{workspace_id}:watchlist",
                "as_of": as_of, "captured_at": as_of, "workspace_id": workspace_id,
                "runtime_versions": {name: importlib.metadata.version(name)
                    for name in ("pandas", "numpy", "pandas-ta", "pydantic")},
                "source_digests": {"fundamental": source_digest(FA_SOURCE),
                    "timing": source_digest(TIMING_SOURCE), "legacy": source_digest(LEGACY_SOURCE)},
                "watchlist": watchlist,
                "agent_cache": read("SELECT symbol,agent,result_json,cached_at FROM agent_cache "
                                    "WHERE agent IN ('fundamental','technical') ORDER BY symbol,agent"),
                "market_cache": read("SELECT symbol,cache_type,payload_json,fetched_at,expires_at "
                    "FROM market_data_cache WHERE cache_type IN ('history:1y:1d','history:3mo:1d') "
                    "ORDER BY symbol,cache_type"),
                "analysis_cache": read("SELECT symbol,signal,analyzed_at FROM analysis_cache "
                                       "WHERE workspace_id=%s ORDER BY symbol", (workspace_id,)),
                "assets": read("SELECT id,canonical_symbol,display_symbol,asset_type,tradable,status "
                               "FROM assets ORDER BY id"),
                "relationships": read("SELECT from_asset_id,to_asset_id,relationship_type,effective_date "
                                      "FROM asset_relationships ORDER BY id"),
                "portfolios": read("SELECT id,name FROM portfolios WHERE workspace_id=%s ORDER BY id", (workspace_id,)),
                "holdings": read("SELECT portfolio_id,symbol,asset_id,shares,sector,allow_swap FROM portfolio_items "
                                 "WHERE workspace_id=%s ORDER BY portfolio_id,symbol", (workspace_id,)),
                "portfolio_snapshots": read("SELECT DISTINCT ON (portfolio_id) id,portfolio_id,snapshot_date,"
                    "holdings_json,sector_breakdown_json FROM portfolio_snapshots WHERE workspace_id=%s "
                    "ORDER BY portfolio_id,snapshot_date DESC,id DESC", (workspace_id,)),
                "policy_snapshots": read("SELECT DISTINCT ON (portfolio_id) id,portfolio_id,created_at,"
                    "constraint_envelope_json FROM recommendation_snapshots WHERE workspace_id=%s "
                    "ORDER BY portfolio_id,created_at DESC,id DESC", (workspace_id,))}
            # JSON conversion freezes values and makes the exact capture replayable.
            return json.loads(json.dumps(capture, default=_json_default))
    finally:
        connection.rollback()
        connection.close()


def render_report(report: dict) -> str:
    result, legacy, comparison = report["standalone"], report["legacy"], report["comparison"]
    coverage = result["coverage"]
    lines = ["# Shadow Candidate Discovery — offline diagnostic", "",
        "Experimental FA + Timing / Pareto. No production recommendation authority.", "",
        f"As of: {result['as_of']}; universe: {result['universe_id']}", "",
        "## Coverage", "", "```json", json.dumps(coverage, indent=2), "```", "",
        "## Legacy comparison", "", f"Signal distribution: {legacy['signal_distribution']}",
        f"L1 gate eligible: {legacy['l1_eligible_count']}",
        f"Captured-input top ten: {', '.join(legacy['captured_order_top_10'])}",
        f"Legacy cutoff score: {legacy['top_10_cutoff_score']}; tied symbols: {legacy['cutoff_ties']}; "
        f"omitted by the existing cap/order: {legacy['cutoff_ties_omitted']}.",
        "Exact current runtime top ten: **UNPROVEN** (freshness, settings and tie order).", "",
        "## Pareto experiment", "", f"Front sizes: {result['front_sizes']}",
        f"Uncapped first-front shortlist: {result['experimental_shortlist']['symbols']}",
        f"Pair relationships: {comparison['eligible_pair_relationships']}",
        f"Selected by both: {comparison['both']}", f"Legacy only: {comparison['legacy_only']}",
        f"Discovery only: {comparison['discovery_only']}",
        f"Shortlist sectors: {comparison['shortlist_sector_distribution']}", "",
        f"Universe sectors: {comparison['universe_sector_distribution']}",
        f"Ranking-eligible sectors: {comparison['ranking_eligible_sector_distribution']}", "",
        "## Candidate evidence", "",
        "| Symbol | Sector | FA | Timing | FA percentile | Timing percentile | Front | Ranking exclusion |",
        "|---|---|---:|---:|---:|---:|---:|---|"]
    for row in result["candidates"]:
        item, rel = row["instrument"], row["relative"]
        lines.append(f"| {item['symbol']} | {item['sector'] or 'UNKNOWN'} | {item['fundamental']['value']} "
            f"| {item['timing']['value']} | {rel['fundamental']['midrank_percentile'] if rel else '—'} "
            f"| {rel['timing']['midrank_percentile'] if rel else '—'} | {rel['pareto_front'] if rel else '—'} "
            f"| {', '.join(row['ranking_eligibility']['reasons'])} |")
    lines.extend(["", "## Portfolio overlays", ""])
    shortlist = set(result["experimental_shortlist"]["symbols"])
    for overlay in report["portfolio_overlays"]:
        rows = overlay["candidates"]
        held = sum(r["already_held"] for r in rows)
        shortlist_held = sum(r["already_held"] for r in rows if r["symbol"] in shortlist)
        blocked = [(r["symbol"], r["portfolio_add_consideration"]["reasons"]) for r in rows
                   if r["portfolio_add_consideration"]["reasons"]]
        lines.extend([f"Portfolio {overlay['portfolio_id']}: universe held {held}, new {len(rows)-held}; "
            f"shortlist held {shortlist_held}, new {len(shortlist)-shortlist_held}.",
            f"Explicit consideration restrictions: {blocked}",
            f"Exposure source: {overlay['exposure_source']}; policy source: {overlay['policy_source']}.",
            "Historical exposure/policy is annotation only; current feasibility is unproven.", ""])
    from collections import Counter
    limits = Counter(limit for row in result["candidates"] for name in ("fundamental", "timing")
                     for limit in row["instrument"][name]["limitations"])
    lines.extend(["## Provenance limitations", "", "```json", json.dumps(dict(sorted(limits.items())), indent=2),
        "```", "", *[f"- {limit}" for limit in result["limitations"]], "",
        "This experiment does not establish superiority, deployment readiness or expected outperformance."])
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--input", type=Path, help="replay an existing capture without DB access")
    mode.add_argument("--capture-current", action="store_true", help="SELECT-only capture; no refresh")
    parser.add_argument("--workspace-id", type=int, default=1)
    parser.add_argument("--env-file", type=Path, default=BACKEND / ".env")
    parser.add_argument("--output-prefix", type=Path, required=True)
    args = parser.parse_args()
    capture = (json.loads(args.input.read_text(encoding="utf-8")) if args.input
               else capture_current(args.workspace_id, args.env_file))
    report = compare_capture(capture)
    prefix = args.output_prefix
    prefix.parent.mkdir(parents=True, exist_ok=True)
    outputs = {"capture.json": capture, "result.json": report}
    for suffix, data in outputs.items():
        path = Path(f"{prefix}.{suffix}")
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    Path(f"{prefix}.md").write_text(render_report(report), encoding="utf-8")
    print(json.dumps({"coverage": report["standalone"]["coverage"],
                      "front_sizes": report["standalone"]["front_sizes"],
                      "comparison": report["comparison"]}, indent=2))


if __name__ == "__main__":
    main()
