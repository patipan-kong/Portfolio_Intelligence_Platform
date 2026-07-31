# M44-WP4 — Positive Documentary Vectors

**Milestone:** M44

**Work package:** M44-WP4 only

**Artifact class:** Normative documentary fixture artifact

**Contract:** [M44-WP4 Portfolio Composition Canonical Byte Representation Contract](../../M44_WP4_PORTFOLIO_COMPOSITION_CANONICAL_BYTE_REPRESENTATION_CONTRACT.md)

**Status:** `RC4 — SERIALIZATION CORRECTED; NOT INDEPENDENTLY SERIALIZATION-APPROVED OR CONFIRMED`

**Constitutional contract review:** `APPROVED` at RC3

**Runtime authority:** `NONE`
**Source-code authority:** `NONE`
**Persistence/schema/migration authority:** `NONE`
**API/transport authority:** `NONE`
**UI/presentation authority:** `NONE`
**Implementation authority:** `NONE`
**Provider authority:** `NONE`
**Production-method authority:** `NONE`
**Executable-validation authority:** `NONE`
**Capability-completion authority:** `NONE`
**Frozen-artifact-amendment authority:** `NONE`
**Ownership-determination authority:** `NONE`
**Vocabulary-admission authority:** `NONE`
**Encoding-selection authority:** `NONE`

**Fixture encoding-selection note:** NONE — every grammar element shown derives from the contract’s bounded container-level encoding selection; the fixture selects no grammar or encoding.

---

## 1. Fixture boundary and mandatory labels

These are documentary vectors, not executable fixtures.

Every specimen containing synthetic nested bytes is labelled exactly:

- `ARTIFICIAL`
- `NON-EFFECTIVE`
- `NON-CONFORMANCE-ESTABLISHING`

In the tables, `ARTIFICIAL / NON-EFFECTIVE /
NON-CONFORMANCE-ESTABLISHING` applies all three labels to that specimen.
Artificial specimens prove container mechanics only. They do not prove a valid
production Composition, source-owner conformance, `G-3` closure, complete
Composition bytes, a concrete `PMS1` subject, or a concrete `PAIM1` manifest.

Intentionally unlabelled specimens contain no synthetic nested bytes. Their
bases are stated where they appear: container primitive, frozen exact literal,
container-owned association mechanics, or documentary reading expectation.

Hexadecimal is documentary notation. Spaces separate octets and emit no bytes.
`A × n` means exactly `n` repetitions of octet `41`; it is not an alternate
grammar.

Every byte-level reproducibility or round-trip proof below binds all input
octets exactly. No parameterized template is used as byte-vector evidence.

## 2. WP4-local primitive framing and boundaries

| Vector | Normative rows | Input | Expected bytes or boundary | Classification |
| --- | --- | --- | --- | --- |
| `WP4-PV-U32-00` | `WP4-NR-006`, `-024` | integer `0` | `00 00 00 00` | Container primitive |
| `WP4-PV-U32-01` | `WP4-NR-006`, `-024` | integer `1` | `00 00 00 01` | Container primitive |
| `WP4-PV-U32-02` | `WP4-NR-006`, `-024` | integer `255` | `00 00 00 ff` | Container primitive |
| `WP4-PV-U32-03` | `WP4-NR-006`, `-024` | integer `256` | `00 00 01 00` | Container primitive |
| `WP4-PV-U32-04` | `WP4-NR-006`, `-024` | integer `4,294,967,295` | `ff ff ff ff` | Container primitive |
| `WP4-PV-U32-05` | `WP4-NR-006`, `-024` | integer `65,535` | `00 00 ff ff` | Container primitive |
| `WP4-PV-U32-06` | `WP4-NR-006`, `-024` | integer `65,536` | `00 01 00 00` | Container primitive |
| `WP4-PV-LP-00` | `WP4-NR-007` | primitive `lp(empty)` | `00 00 00 00`; valid primitive mechanics but prohibited as a required coordinate by `WP4-NR-015` | Container primitive only |
| `WP4-PV-LP-01` | `WP4-NR-007` | `lp(41)` | `00 00 00 01 41` | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-LP-02` | `WP4-NR-007` | `lp(A × 255)` | prefix `00 00 00 ff`, then exactly 255 `41` octets | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-LP-03` | `WP4-NR-007` | `lp(A × 256)` | prefix `00 00 01 00`, then exactly 256 `41` octets | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-LP-04` | `WP4-NR-007` | conceptual payload of maximum admitted length | prefix `ff ff ff ff`; documentary boundary only, not materialized | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-LP-05` | `WP4-NR-007` | `lp(A × 65,535)` | prefix `00 00 ff ff`, then exactly 65,535 octets | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-LP-06` | `WP4-NR-007` | `lp(A × 65,536)` | prefix `00 01 00 00`, then exactly 65,536 octets | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |

## 3. Frozen tag and fixed order

| Vector | Normative rows | Documentary input | Expected result | Classification |
| --- | --- | --- | --- | --- |
| `WP4-PV-PR-01` | `WP4-NR-003`, `-004`, `-008` | Frozen M42-WP7 §5 tag and sequence | The first 31 octets are raw `ASCII("M42-WP7-PORTFOLIO-COMPOSITION-1")`; the next nine components are fields 2–10 in frozen order | Frozen literal and container mechanics |
| `WP4-PV-ORD-01` | `WP4-NR-004`, `-009`, checklist 10 | The exact 591-octet artificial mechanics stream in §5.1: `F2=02` through `F8=08`, the exact 440-octet `OA` in §4.1, and the exact 77-octet `PA` in §4.2 | The parser assigns `F2` through `F8` by position, then decodes exact `OA` and `PA`; re-encoding produces the identical 591-octet stream | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-PERM-01` | `WP4-NR-009`, `-020`, `-026` | Presentation A lists the exact §5.1 components in field order `1,2,3,4,5,6,7,8,9,10`; presentation B lists those same exact components in order `10,9,8,7,6,5,4,3,2,1` | Both documentary encodes disregard presentation order, apply the fixed grammar, and produce the identical exact 591-octet stream in §5.1 | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |

The exact frozen order checked by these vectors is:

1. `schema_version`;
2. `portfolio_identity`;
3. `accounting_scope`;
4. `portfolio_membership`;
5. `portfolio_base_currency`;
6. `investment_universe_declaration`;
7. `portfolio_benchmark_declaration`;
8. `portfolio_lifecycle_state`;
9. `coordinate_owner_attributions`; and
10. `coordinate_provenance_associations`.

## 4. Association framing specimens

### 4.1 Owner-attribution envelope

`WP4-PV-OA-01` covers `WP4-NR-003`, `-011`, and `-023`.

Basis for no artificial labels: container-owned association mechanics; the
specimen contains no synthetic nested coordinate bytes and selects no grammar
outside the contract.

```text
u32(10)
u32(1)  u32(1) lp(ASCII("Portfolio Intelligence"))
u32(2)  u32(1) lp(ASCII("Ledger & Accounting"))
u32(3)  u32(1) lp(ASCII("Ledger & Accounting"))
u32(4)  u32(1) lp(ASCII("Ledger & Accounting"))
u32(5)  u32(2) lp(ASCII("Ledger & Accounting")) lp(ASCII("Asset Foundation"))
u32(6)  u32(2) lp(ASCII("Portfolio Intelligence")) lp(ASCII("Asset Foundation"))
u32(7)  u32(3) lp(ASCII("Portfolio Intelligence")) lp(ASCII("Market Intelligence")) lp(ASCII("Asset Foundation"))
u32(8)  u32(1) lp(ASCII("Ledger & Accounting"))
u32(9)  u32(1) lp(ASCII("Portfolio Intelligence"))
u32(10) u32(2) lp(ASCII("Connectivity & Ingestion")) lp(ASCII("Portfolio Intelligence"))
```

The exact 440-octet `OA` payload is:

```text
00 00 00 0a 00 00 00 01 00 00 00 01 00 00 00 16 50 6f 72 74 66 6f 6c 69
6f 20 49 6e 74 65 6c 6c 69 67 65 6e 63 65 00 00 00 02 00 00 00 01 00 00
00 13 4c 65 64 67 65 72 20 26 20 41 63 63 6f 75 6e 74 69 6e 67 00 00 00
03 00 00 00 01 00 00 00 13 4c 65 64 67 65 72 20 26 20 41 63 63 6f 75 6e
74 69 6e 67 00 00 00 04 00 00 00 01 00 00 00 13 4c 65 64 67 65 72 20 26
20 41 63 63 6f 75 6e 74 69 6e 67 00 00 00 05 00 00 00 02 00 00 00 13 4c
65 64 67 65 72 20 26 20 41 63 63 6f 75 6e 74 69 6e 67 00 00 00 10 41 73
73 65 74 20 46 6f 75 6e 64 61 74 69 6f 6e 00 00 00 06 00 00 00 02 00 00
00 16 50 6f 72 74 66 6f 6c 69 6f 20 49 6e 74 65 6c 6c 69 67 65 6e 63 65
00 00 00 10 41 73 73 65 74 20 46 6f 75 6e 64 61 74 69 6f 6e 00 00 00 07
00 00 00 03 00 00 00 16 50 6f 72 74 66 6f 6c 69 6f 20 49 6e 74 65 6c 6c
69 67 65 6e 63 65 00 00 00 13 4d 61 72 6b 65 74 20 49 6e 74 65 6c 6c 69
67 65 6e 63 65 00 00 00 10 41 73 73 65 74 20 46 6f 75 6e 64 61 74 69 6f
6e 00 00 00 08 00 00 00 01 00 00 00 13 4c 65 64 67 65 72 20 26 20 41 63
63 6f 75 6e 74 69 6e 67 00 00 00 09 00 00 00 01 00 00 00 16 50 6f 72 74
66 6f 6c 69 6f 20 49 6e 74 65 6c 6c 69 67 65 6e 63 65 00 00 00 0a 00 00
00 02 00 00 00 18 43 6f 6e 6e 65 63 74 69 76 69 74 79 20 26 20 49 6e 67
65 73 74 69 6f 6e 00 00 00 16 50 6f 72 74 66 6f 6c 69 6f 20 49 6e 74 65
6c 6c 69 67 65 6e 63 65
```

Expected documentary decode: ten field-number associations in exact frozen
order with exact owner counts, domain names, and co-owner sequence. The
contract's role matrix remains controlling; these association bytes transfer no
meaning or ownership.

### 4.2 Provenance-association envelope

`WP4-PV-PA-01` covers `WP4-NR-012`, `-013`, and `-023`.

The explicit artificial payload assignments are:

- `a2 = a2`;
- `a4_1 = a4 01`; and
- `a4_2 = a4 02`.

```text
u32(7)
u32(2) u32(1) lp(a2)
u32(3) u32(0)
u32(4) u32(2) lp(a4 01) lp(a4 02)
u32(5) u32(0)
u32(6) u32(0)
u32(7) u32(0)
u32(8) u32(0)
```

The exact 77-octet `PA` payload is:

```text
00 00 00 07 00 00 00 02 00 00 00 01 00 00 00 01 a2 00 00 00 03 00 00 00
00 00 00 00 04 00 00 00 02 00 00 00 02 a4 01 00 00 00 02 a4 02 00 00 00
05 00 00 00 00 00 00 00 06 00 00 00 00 00 00 00 07 00 00 00 00 00 00 00
08 00 00 00 00
```

The payloads are exact opaque artificial non-empty byte strings. Their specimen
classification is `ARTIFICIAL / NON-EFFECTIVE /
NON-CONFORMANCE-ESTABLISHING`. Expected documentary decode: `a2` remains
attached to field 2; `a4 01` then `a4 02` remain attached to field 4 in that
exact order; and fields 3, 5, 6, 7, and 8 retain exact zero item counts. The
specimen does not establish that any authoritative Provenance representation,
boundary, order, or completeness basis exists.

## 5. Opaque bytes, affirmative absence, and round trip

| Vector | Normative rows | Input and operation | Expected result | Classification |
| --- | --- | --- | --- | --- |
| `WP4-PV-OPAQUE-01` | `WP4-NR-010`, `-014`, `-026`, `-028` | Opaque payload `c3 28 00 ff 41 61` is framed as one nested value | Exact octets survive; no Unicode decode, case-fold, normalization, number parsing, or text substitution occurs | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-ABS-01` | `WP4-NR-015`, `-016`, `-027` | Abstract owner-supplied affirmative-absence bytes `aa` are present as `lp(aa)` | Decode yields a present one-octet value, distinct from a missing slot and from `lp(empty)` | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-RT-01` | `WP4-NR-018`, `-019`, `-021`, `-025` | Decode and re-encode the exact 591-octet artificial mechanics stream in §5.1 | Exact decoded component sequence in §5.1, complete input consumption, and byte-for-byte equality with the same 591-octet stream | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |

`WP4-PV-ABS-01` proves only the container distinction. `aa` is not a Benchmark
form, `Explicitly None` representation, production value, or source-owner
conformance evidence.

### 5.1 Exact order and round-trip byte proof

This single exact specimen supplies the byte-level evidence for
`WP4-PV-ORD-01` and `WP4-PV-RT-01`. Its classification is
`ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING`.

The exact input component bytes are:

| Component | Exact octets |
| --- | --- |
| Raw schema tag | `4d 34 32 2d 57 50 37 2d 50 4f 52 54 46 4f 4c 49 4f 2d 43 4f 4d 50 4f 53 49 54 49 4f 4e 2d 31` |
| `F2` | `02` |
| `F3` | `03` |
| `F4` | `04` |
| `F5` | `05` |
| `F6` | `06` |
| `F7` | `07` |
| `F8` | `08` |
| `OA` | Exact 440-octet payload in §4.1; top-level prefix `00 00 01 b8` |
| `PA` | Exact 77-octet payload in §4.2; top-level prefix `00 00 00 4d` |

The complete expected 591-octet top-level stream is:

```text
4d 34 32 2d 57 50 37 2d 50 4f 52 54 46 4f 4c 49 4f 2d 43 4f 4d 50 4f 53
49 54 49 4f 4e 2d 31 00 00 00 01 02 00 00 00 01 03 00 00 00 01 04 00 00
00 01 05 00 00 00 01 06 00 00 00 01 07 00 00 00 01 08 00 00 01 b8 00 00
00 0a 00 00 00 01 00 00 00 01 00 00 00 16 50 6f 72 74 66 6f 6c 69 6f 20
49 6e 74 65 6c 6c 69 67 65 6e 63 65 00 00 00 02 00 00 00 01 00 00 00 13
4c 65 64 67 65 72 20 26 20 41 63 63 6f 75 6e 74 69 6e 67 00 00 00 03 00
00 00 01 00 00 00 13 4c 65 64 67 65 72 20 26 20 41 63 63 6f 75 6e 74 69
6e 67 00 00 00 04 00 00 00 01 00 00 00 13 4c 65 64 67 65 72 20 26 20 41
63 63 6f 75 6e 74 69 6e 67 00 00 00 05 00 00 00 02 00 00 00 13 4c 65 64
67 65 72 20 26 20 41 63 63 6f 75 6e 74 69 6e 67 00 00 00 10 41 73 73 65
74 20 46 6f 75 6e 64 61 74 69 6f 6e 00 00 00 06 00 00 00 02 00 00 00 16
50 6f 72 74 66 6f 6c 69 6f 20 49 6e 74 65 6c 6c 69 67 65 6e 63 65 00 00
00 10 41 73 73 65 74 20 46 6f 75 6e 64 61 74 69 6f 6e 00 00 00 07 00 00
00 03 00 00 00 16 50 6f 72 74 66 6f 6c 69 6f 20 49 6e 74 65 6c 6c 69 67
65 6e 63 65 00 00 00 13 4d 61 72 6b 65 74 20 49 6e 74 65 6c 6c 69 67 65
6e 63 65 00 00 00 10 41 73 73 65 74 20 46 6f 75 6e 64 61 74 69 6f 6e 00
00 00 08 00 00 00 01 00 00 00 13 4c 65 64 67 65 72 20 26 20 41 63 63 6f
75 6e 74 69 6e 67 00 00 00 09 00 00 00 01 00 00 00 16 50 6f 72 74 66 6f
6c 69 6f 20 49 6e 74 65 6c 6c 69 67 65 6e 63 65 00 00 00 0a 00 00 00 02
00 00 00 18 43 6f 6e 6e 65 63 74 69 76 69 74 79 20 26 20 49 6e 67 65 73
74 69 6f 6e 00 00 00 16 50 6f 72 74 66 6f 6c 69 6f 20 49 6e 74 65 6c 6c
69 67 65 6e 63 65 00 00 00 4d 00 00 00 07 00 00 00 02 00 00 00 01 00 00
00 01 a2 00 00 00 03 00 00 00 00 00 00 00 04 00 00 00 02 00 00 00 02 a4
01 00 00 00 02 a4 02 00 00 00 05 00 00 00 00 00 00 00 06 00 00 00 00 00
00 00 07 00 00 00 00 00 00 00 08 00 00 00 00
```

The exact decoded component sequence is the raw 31-octet tag; `F2=02`;
`F3=03`; `F4=04`; `F5=05`; `F6=06`; `F7=07`; `F8=08`; the exact 440-octet
`OA` payload from §4.1; and the exact 77-octet `PA` payload from §4.2. The
decoder consumes all 591 octets. Re-encoding that sequence produces exactly the
591-octet stream above:

`encode(decode(stream)) = stream`.

No `OA`, `PA`, `a2`, `a4_1`, or `a4_2` value remains undefined in this
byte-level proof. The explicit bytes do not establish source-owner conformance,
close `G-3`, form complete production Composition bytes, form a concrete
`PMS1`, or form a concrete `PAIM1`.

## 6. Per-field positive documentary coverage

| Vector | Frozen field | Normative rows | Documentary case and expectation | Classification |
| --- | --- | --- | --- | --- |
| `WP4-PV-F01` | `schema_version` | `WP4-NR-003`, `-004`, `-008` | Emit the exact 31 raw ASCII octets; this is the only constitutionally representable effective field-level byte specimen | Frozen exact literal |
| `WP4-PV-F02` | `portfolio_identity` | `WP4-NR-003`, `-010`, `-014` | Frame opaque artificial `02`; do not parse or claim an owner-supplied identity form | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-F03` | `accounting_scope` | `WP4-NR-003`, `-010`, `-014` | Frame opaque artificial `03`; preserve slot and bytes only | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-F04` | `portfolio_membership` | `WP4-NR-003`, `-010`, `-014` | Frame opaque artificial `04`; make no claim about set elements, cardinality, or order | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-F05` | `portfolio_base_currency` | `WP4-NR-003`, `-010`, `-014` | Frame opaque artificial `05`; preserve Ledger/Asset co-allocation | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-F06` | `investment_universe_declaration` | `WP4-NR-003`, `-010`, `-014` | Frame opaque artificial `06`; do not define its six-facet nested form or order | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-F07` | `portfolio_benchmark_declaration` | `WP4-NR-003`, `-010`, `-017` | Frame opaque artificial `07`; do not use a frozen form label or claim `Explicitly None` bytes | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-F08` | `portfolio_lifecycle_state` | `WP4-NR-003`, `-010`, `-014`, `-018` | The frozen lifecycle vocabulary is supplied semantically. Frame the artificial opaque byte sequence `08` only to test container mechanics. The artificial bytes do not represent `active`, `archived`, or `closed`, and WP4 selects no lifecycle byte encoding. | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |
| `WP4-PV-F09` | `coordinate_owner_attributions` | `WP4-NR-003`, `-011` | Use exact `WP4-PV-OA-01`; decode all ten associations without ownership transfer | Container-owned association mechanics; no synthetic nested bytes |
| `WP4-PV-F10` | `coordinate_provenance_associations` | `WP4-NR-003`, `-012`, `-013` | Use `WP4-PV-PA-01`; preserve opaque items and exact associations | `ARTIFICIAL / NON-EFFECTIVE / NON-CONFORMANCE-ESTABLISHING` |

Fields 2–7 and field 10 are not presently constitutionally representable as
effective complete nested canonical content under the binding WP1 inventory.
Their artificial cases satisfy per-field container-mechanics coverage only.
Field 8 differs on two independent constitutional points:

1. it is supplied on both frozen inventory axes and is not a routed missing
   element; and
2. WP4 still lacks authority to author its Ledger & Accounting-owned byte
   encoding, so any field-8 bytes consumed by the container remain opaque and
   owner-supplied.

## 7. Authority, inventory, and inherited-matter specimens

| Vector | Normative rows | Documentary expectation | Basis for no artificial labels |
| --- | --- | --- | --- |
| `WP4-PV-AUTH-01` | `WP4-NR-001`, `-002`, `-032` | A reader derives container-only authority from `E-1` and `E-2`, derives no authority from silence, observes no frozen-artifact amendment, and does not convert own-domain meaning ownership into nested-form authority. | Documentary reading expectation; no synthetic nested bytes |
| `WP4-PV-INV-01` | `WP4-NR-005`, `-030`, `-031`, `-032` | A reader applies the frozen WP1 field and facet tables unchanged and reaches only `G-3 OPEN — PARTIAL`, with every missing element routed, field 8 supplied and not routed, and no checkpoint outcome declared. | Documentary reading expectation; no synthetic nested bytes |
| `WP4-PV-M34-01` | `WP4-NR-029` | The record cites the exact title “Decompose the instrument-analysis product contract,” relies only on the exact consequence sentence, and records without correcting the frozen M44 characterization divergence. | Documentary reading expectation; no synthetic nested bytes |

## 8. Documentary conclusion

The vectors prove that two independent readers can agree on the WP4 container
mechanics for artificial inputs. That agreement is never evidence for `G-3`
closure. No vector in this artifact claims a valid complete production
Composition, concrete `PMS1`, or concrete `PAIM1`.
