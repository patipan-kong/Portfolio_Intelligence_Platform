# Shadow Candidate Discovery — Artifact Checksum Manifest

Raw artifacts under `artifacts/shadow-discovery/` stay out of version control:
they are ~13 MB and contain captured portfolio holdings/snapshots and raw
provider payloads. This manifest freezes them by SHA-256 (computed 2026-10-07).
The first six match `2026-10-07-slice1c.preservation.json`.

| SHA-256 | File |
|---|---|
| `acc4cc219f3ca954eb56b5f765e58031c957e5f3d5c93020c47889b1c08c02da` | 2026-10-07-watchlist.capture.json |
| `2c044fb4d08292e755e4284e97a64e92dccb2d1099093765b1694c1926c0924a` | 2026-10-07-watchlist.result.json |
| `0780d363223572786d420b0f6954e992e9c30c1f5fc173d8ebfcc353c793bc50` | 2026-10-07-watchlist.md |
| `75ce11cc0e5c8ea2add06437c8eb6b10411d71689489313ae2f1477d6c73bd4a` | 2026-10-07-slice1b.fa-supplement.json |
| `d2a24b20a253d5f8f6fe5a363b022754f6851137305246ef830a3a32b0f5aa59` | 2026-10-07-slice1b.result.json |
| `8ac7573f2468aec51168f056633d2b7330e831f4e7b31264b822e17a80151c37` | 2026-10-07-slice1b.md |
| `24b5574d6d342cba5d8a38d18c34264988e11a3bb0b18fc60decc1081ea4ac90` | 2026-10-07-slice1c.local-supplement.json |
| `d525562766e10877889510150942cc9a5c7e462c1c854c597605e01ed231ba51` | 2026-10-07-slice1c.banpu-history-supplement.json |
| `752b5d8960f60a6e71dd171ecec5166ca3d03de775038e90968df5b5939a77c0` | 2026-10-07-slice1c.result.json |
| `421b2a8d27ea85eb24b0bb78b35bbad7f4c466f06edb0c90406ddf5fd1ce95f2` | 2026-10-07-slice1c.md |
| `dac5790dcb4f1953d250784dbc7e9b23dd8cc408e283b438180b44d6e65d7ee6` | 2026-10-07-slice1c.preservation.json |

Replay is also bound to the production source digests recorded in each
capture (`fundamental.py`, `timing_intelligence.py`, `optimizer.py`); a change to
any of those files makes `adapt_capture` refuse to replay. Record the commit
SHA of those sources alongside this manifest when freezing.

## Source provenance (recorded at freeze)

Verified 2026-10-07 against base commit `653a3ed` (the parent of the Discovery
commit; sources last changed in `1f92aff`). The digests in
`2026-10-07-watchlist.capture.json` → `source_digests` match these files:

| Key | Source | SHA-256 |
|---|---|---|
| `fundamental` | `backend/agents/fundamental.py` | `64e90655b1c11e2e92c5de819d4f6b39e491447bc7a66991836a85d963913eea` |
| `timing` | `backend/services/timing_intelligence.py` | `ce20fe57782bd7b30b1e0ab05bec781f00f6b044292d9cbe7594503a5b0a4e4a` |
| `legacy` | `backend/agents/optimizer.py` | `9585515022851870a3071ea91179c4ad2f984b83456e73bb1ffeddabd81d9da0` |

To verify, recompute SHA-256 of each file under `artifacts/shadow-discovery/`
and compare with the first table. The artifacts are reference
copies for this shadow record only; they carry no production authority.
