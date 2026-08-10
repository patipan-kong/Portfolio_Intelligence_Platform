# M46-WP1 — Authority and Frozen-Baseline Register

**Artifact class:** Authorized WP1 documentary implementation deliverable 1 of 6

**Authoring role:** M46-WP1 Implementation Author

**Authorization:** [M46-WP1 Authorization Record](M46_WP1_AUTHORIZATION_RECORD.md)

**Disposition:** `AUTHORED — FAIL-CLOSED BLOCKED`

**Code, schema, runtime, migration, and successor-package authority:** `NONE`

---

## 1. Purpose and boundary

This register fixes the exact authority and evidence baseline against which the
six M46-WP1 documentary deliverables were authored. It performs no allocation,
authorization, review, confirmation, content-identity validation, freeze, or
closeout. It modifies no frozen artifact.

The implementation author is confined to the six paths in authorization §4.
`M46-WP2` through `M46-WP8` remain outside scope.

## 2. Authority chain

| Act | Repository evidence | State consumed by WP1 |
| --- | --- | --- |
| M46 planning mandate | [Planning Allocation / Commissioning Record](../governance/M46_CORPORATE_ACTION_PORTFOLIO_ACCOUNTING_PLANNING_ALLOCATION_RECORD.md) | Planning mandate only |
| M46 planning freeze | [Planning Freeze Record](M46_PLANNING_FREEZE_RECORD.md) | `COMPLETE — FROZEN` |
| WP1 allocation | [M46-WP1 Allocation Record](M46_WP1_ALLOCATION_RECORD.md) | `ALLOCATED` |
| WP1 authorization | [M46-WP1 Authorization Record](M46_WP1_AUTHORIZATION_RECORD.md) | `AUTHORIZED` for six documentary outputs only |

No item in this chain supplies owner-domain, runtime, schema, migration,
production-correction, release, successor-package, review, confirmation, or
freeze authority.

## 3. Frozen M46 planning baseline

SHA-256 was recomputed from current binary working-tree bytes.

| Frozen artifact | Freeze-recorded SHA-256 | Recomputed SHA-256 | Bytes | Lines | Result |
| --- | --- | --- | ---: | ---: | --- |
| [Architecture and Implementation Plan](M46_ARCHITECTURE_AND_IMPLEMENTATION_PLAN.md) | `1D3A6C58999A16DC4EA687049352DC4ACFAC7E9CFC439D1EC156291F53FD2337` | `1D3A6C58999A16DC4EA687049352DC4ACFAC7E9CFC439D1EC156291F53FD2337` | 95,689 | 1,702 | `EXACT` |
| [Work-Package Decomposition and Roadmap](M46_WORK_PACKAGE_DECOMPOSITION_AND_ROADMAP.md) | `51D3BFD77145107849FFABC3675F713AC9BBA3AF8E09CE8738870FDF425B8806` | `51D3BFD77145107849FFABC3675F713AC9BBA3AF8E09CE8738870FDF425B8806` | 54,833 | 901 | `EXACT` |

The M46 planning corpus remains complete, ratified, and frozen at these exact
identities. `M46-G0` remains satisfied.

## 4. Governing WP1 record identities

These records are additive governance evidence, not members of the frozen
planning pair.

| Record | Recomputed SHA-256 | Bytes | Lines |
| --- | --- | ---: | ---: |
| [M46 Planning Freeze Record](M46_PLANNING_FREEZE_RECORD.md) | `3005C159777A1995E7BCC7D403868BE941E152B18EE07A85FF675A83A67F462F` | 28,834 | 459 |
| [M46-WP1 Allocation Record](M46_WP1_ALLOCATION_RECORD.md) | `8404EF5A7A72BA40E0B19C61B20770E9D4303619124583CB4BA2F92CB8F2B5BB` | 8,686 | 173 |
| [M46-WP1 Authorization Record](M46_WP1_AUTHORIZATION_RECORD.md) | `7CA9A80AFE6B08176E6AA0FC0B95609B6A2424834DC522701BD8E04D8A4CD6E9` | 24,618 | 442 |

## 5. Frozen Asset Foundation predecessor identity audit

The AF freeze records identify six frozen implementation artifacts. For every
artifact, the current normalized Git blob matches the recorded blob, but the
raw working-tree blob, byte count, and binary SHA-256 do not match the frozen
working-tree identity. No file was changed to resolve this condition.

| Package and artifact | Recorded SHA-256 / bytes | Current raw SHA-256 / bytes | Recorded blob / current normalized blob | Current raw blob | Result |
| --- | --- | --- | --- | --- | --- |
| AF-WP1 [AF-1 canonical lexical form](ASSET_FOUNDATION_AF_WP1_AF_1_CANONICAL_LEXICAL_FORM.md) | `19D432D409C2BAD2A7D76CDF618545CBCEE4986FE221684B44572F2C2A22120E` / 19,784 | `32B37F3A9C4B6611102356D25D84C74E8CD968416833283D5CF7C1F324855F60` / 20,203 | `4d98bfe57dab18240bc1615d0cfe6d7b4c4c7597` / same | `14b985a6e03cdbb3df55e76c127101133038cf5f` | `MISMATCH` |
| AF-WP1 [vector annex](ASSET_FOUNDATION_AF_WP1_VECTOR_ANNEX.md) | `93595ED544E3DAA920F04785F0BA24F2AC35DB2A4B6F4403DF2E8614477B4605` / 13,523 | `27B4ECE787D35827085F6FA4EFE9D67037E77BD3742E20645118FB9FCE364B07` / 13,709 | `4e42eba5b083787b10c8fd37ac11f82a4d045f2d` / same | `ac85f996addb4d819ddd6d77765096b188aa8ca9` | `MISMATCH` |
| AF-WP2 [AF-2 canonical form](ASSET_FOUNDATION_AF_WP2_AF_2_DENOMINATION_IDENTIFIER_DIMENSION_CANONICAL_FORM.md) | `3910EB6445CF5F24CFE638AE63748353743FD779DF26A7A1C2763DFBCFC32B6F` / 26,283 | `A881AF4D2BC72E751C8DA63A43655E60359BD29BCEC2C9D1A2814ACBE7E0C0EB` / 26,797 | `da899612572dbfaff10792759a1f24e4cd2e6cd0` / same | `3b33c363b6a75f957868042dd1f8e192880422ec` | `MISMATCH` |
| AF-WP2 [vector annex](ASSET_FOUNDATION_AF_WP2_VECTOR_ANNEX.md) | `89011098F42C77A9049127126AE28BDB9693B20D7F66391C05992F11FF350939` / 15,912 | `700B299D53A75DFA6BCF479EAE4EE18EF695EEEA9116468F1BB4E7F83C8C57E0` / 16,121 | `f831fd24ae78ae85814dcf9fa598d926f31441de` / same | `3f50c50fa475427b5bec72e98f07ffa0f9668472` | `MISMATCH` |
| AF-WP3 [owner evidence manifest and annex index](ASSET_FOUNDATION_AF_WP3_OWNER_EVIDENCE_MANIFEST_AND_CONFORMANCE_ANNEX_INDEX.md) | `095C081746FCF00FCE27C8B9BCFD2E6E37482E28028B93943A3B3A9A938FE67F` / 25,735 | `59E5D7BB51285209FAC3B071351BBE34879DD210783CA0CA75FBB2193502178A` / 26,067 | `4f8cae8e17be4f8e743a6d0a43b5c43a6dec851a` / same | `935317687b676617510b86e6faecbb60d1334e73` | `MISMATCH` |
| AF-WP4 [release-attestation candidate](ASSET_FOUNDATION_AF_WP4_RELEASE_ATTESTATION.md) | `5A3B3CE7A4A8874CC78C2A98FD0A2D64B6B5624F1D04A16B2272B5BA02C825CB` / 30,145 | `0F37928D1461C33F156E43233F53D25973C8087141FAAFC3390262049CEE4A41` / 30,495 | `372ebf8680c3a4654ae65d769723c0bb6bd2a8de` / same | `89a9400c6b9f6e28ab90edbd7776cf834c215cd6` | `MISMATCH` |

For each row, the current byte surplus equals the recorded line count. This is
consistent with LF-to-CRLF working-tree conversion, but that diagnosis does not
make the binary identities equal. Authorization §9.2.1 requires a fail-closed
stop on any frozen-predecessor identity mismatch. WP1 has no authority to
normalize, repair, refreeze, or reinterpret these predecessors.

## 6. Six-deliverable corpus map

| # | Authorized deliverable | Repository path | Authorship state |
| --- | --- | --- | --- |
| 1 | Authority and frozen-baseline register | `docs/implementation/M46_WP1_BASELINE_REGISTER.md` | `AUTHORED` |
| 2 | Current-state and gap inventory | `docs/implementation/M46_WP1_CURRENT_STATE_AND_GAP_INVENTORY.md` | `AUTHORED` |
| 3 | Alignment-residual disposition | `docs/implementation/M46_WP1_ALIGNMENT_RESIDUAL_DISPOSITION.md` | `AUTHORED — BLOCKED` |
| 4 | Vocabulary ownership/disposition register | `docs/implementation/M46_WP1_VOCABULARY_REGISTER.md` | `AUTHORED — NO ADMISSIONS` |
| 5 | Acceptance-vector contract and coverage matrix | `docs/implementation/M46_WP1_ACCEPTANCE_VECTOR_CONTRACT.md` | `AUTHORED — FIXTURE EXECUTION BLOCKED` |
| 6 | Risk and open-dependency register | `docs/implementation/M46_WP1_RISK_AND_DEPENDENCY_REGISTER.md` | `AUTHORED — OPEN BLOCKERS RECORDED` |

## 7. Baseline disposition

The governing M46 planning pair is exact. The required AF-WP1–AF-WP4 source
set is present but fails the authorization's binary working-tree identity
check. The recorded ownership alignment also retains the separate residual
dispositioned in deliverable 3.

**Terminal disposition: `AUTHORED — FAIL-CLOSED BLOCKED`.**

This register does not authorize implementation, review, confirmation,
content-identity validation, freeze, WP2–WP8, schema or runtime change,
migration, cutover, production correction, release, or closeout.
