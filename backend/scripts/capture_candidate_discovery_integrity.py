"""Optional Slice 1C local supplement. SELECT only; never refreshes caches."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))
from services.symbol_resolver import resolve_yfinance_symbol
from scripts.shadow_candidate_discovery import _json_default


def capture_integrity(baseline: dict, env_file: Path) -> dict:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from dotenv import dotenv_values

    symbols = sorted({resolve_yfinance_symbol(w['symbol']) for w in baseline['watchlist']})
    connection = psycopg2.connect(dotenv_values(env_file)['DATABASE_URL'], connect_timeout=5)
    connection.set_session(isolation_level='REPEATABLE READ', readonly=True, autocommit=False)
    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            def read(sql, params=()):
                cursor.execute(sql, params or None)
                return [dict(r) for r in cursor.fetchall()]

            result = {
                'supplement_version': 'wealth.shadow-integrity-local.v1',
                'captured_at': read('SELECT transaction_timestamp() AS t')[0]['t'],
                'purpose': 'Provider identity/period diagnostics and local history catalogue; never ranking inputs',
                'profiles': read('SELECT symbol,cache_type,payload_json,fetched_at,expires_at '
                    'FROM market_data_cache WHERE cache_type=%s AND symbol=ANY(%s) ORDER BY symbol',
                    ('fundamental', symbols)),
                'market_history_catalogue': read('SELECT symbol,cache_type,fetched_at,expires_at '
                    'FROM market_data_cache WHERE cache_type LIKE %s ORDER BY symbol,cache_type', ('history:%',)),
                'analysis_history_metadata': read('SELECT symbol,analyzed_at,fa_score,ta_score,scores '
                    'FROM analysis_history WHERE workspace_id=%s AND symbol=ANY(%s) '
                    'ORDER BY symbol,analyzed_at,id',
                    (baseline['workspace_id'], [w['symbol'] for w in baseline['watchlist']])),
                'history_table_catalogue': read('SELECT table_name FROM information_schema.tables '
                    "WHERE table_schema='public' AND (table_name LIKE '%agent%cache%' "
                    "OR table_name LIKE '%market%cache%' OR table_name LIKE '%analysis%history%') ORDER BY table_name"),
                'limitations': ['Supplement is a later local transaction, not proven original provider response',
                    'No historical FA observation/publication date inferred from cache or analysis times'],
            }
            return json.loads(json.dumps(result, default=_json_default))
    finally:
        connection.rollback()
        connection.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', required=True, type=Path)
    parser.add_argument('--env-file', type=Path, default=BACKEND / '.env')
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError('supplement must have a distinct unused filename')
    result = capture_integrity(json.loads(args.capture.read_text()), args.env_file)
    result['baseline_sha256'] = hashlib.sha256(args.capture.read_bytes()).hexdigest()
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f"Captured {len(result['profiles'])} already-local provider profiles; no refresh or writes")


if __name__ == '__main__':
    main()
