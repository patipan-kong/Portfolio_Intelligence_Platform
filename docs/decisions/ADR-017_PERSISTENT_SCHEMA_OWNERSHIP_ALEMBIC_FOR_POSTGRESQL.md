# ADR-017: Persistent Schema Ownership — Alembic for PostgreSQL

**Status:** Accepted
**Date:** 2026-09-08
**Decision authority:** Human-approved Wealth OS operational-architecture
hardening decision
**Scope:** Which mechanism owns PostgreSQL schema creation and evolution at
application startup, and what role `Base.metadata.create_all()` retains
across this codebase's supported database backends. Does not define
migration orchestration, deployment automation, or any product/business
logic.

---

## Context

A 2026-09-08 reconnaissance ("Migration Ownership / `init_db()` Boundary")
traced a recurring class of development-database incident to a single root
cause: `backend/models/database.py`'s `init_db()` calls
`Base.metadata.create_all(bind=engine)` unconditionally, regardless of
database backend. `init_db()` runs on every application startup via
`main.py`'s FastAPI `lifespan()`, and again from the standalone
`scripts/seed_regime_scenarios.py` CLI.

Against PostgreSQL, this means any ORM model added to `database.py` before
its corresponding Alembic migration has been run gets silently created by
`create_all()` — with no `alembic_version` bookkeeping update, and often with
schema differences from what the migration itself would have produced (most
visibly, ORM `Column(..., index=True)` produces an extra index the
hand-written migration never defines). The next real `alembic upgrade head`
then fails with `DuplicateTable` on the first affected revision, blocking
every migration behind it.

This is not a first occurrence. `docs/engineering/DECISION_LOG.md`'s
"Alembic Migration Graph Corruption — Duplicate Revision ID + Unmerged
Branch" entry (2026-07-06) documents the identical root cause and fingerprint
against the same development database, and its own reasoning refers to *"a
third out-of-band `create_all()`"* — implying at least two prior
undocumented occurrences before that date. The incident repaired immediately
prior to this record (2026-09-08, dev DB restamped to `g4h5i6j7k8l9` then
upgraded to head `h5i6j7k8l9m0`) is at minimum the fourth occurrence of this
exact failure class.

`docs/architecture/ARCHITECTURE.md` already states, in one line, that
"PostgreSQL uses Alembic" — but no ADR has ever ratified this as a binding
boundary, and `init_db()` itself has never been brought into conformance with
it. The reconnaissance also confirmed production topology materially raises
the stakes: `backend/ecosystem.config.js` runs the backend under PM2 in
`cluster` mode with `instances: 4`, meaning every deploy/restart runs
`lifespan()` → `init_db()` → `create_all()` concurrently across four
processes against the same live PostgreSQL database — a confirmed, not
hypothetical, multi-process race on `CREATE TABLE` for any newly-added,
not-yet-migrated model.

At the same time, the reconnaissance confirmed two backend-startup patterns
that must **not** be disturbed:

1. SQLite is a legitimate, currently-supported persistent deployment mode
   (the default `DATABASE_URL` when unset), whose schema evolution has never
   used Alembic — it relies on `create_all()` for new tables and
   `migrate_legacy_data()`'s `_is_sqlite`-gated `ALTER TABLE` patches for new
   columns, entirely by design (`ARCHITECTURE.md`'s adjacent statement:
   "`migrate_legacy_data()` runs at startup for SQLite ALTER TABLE
   patches").
2. All ~106 backend test modules construct their own ephemeral
   `sqlite:///:memory:` engine and call `Base.metadata.create_all()`
   directly, independent of `DATABASE_URL` and of `init_db()` entirely. This
   pattern is correct and is not implicated in the incident.

## Decision

### 1. PostgreSQL: Alembic is the sole schema owner

For any engine bound to a non-SQLite `DATABASE_URL` (in practice, PostgreSQL),
Alembic is the sole owner of schema creation and evolution. Application
startup — via `init_db()`, and therefore via every caller of `init_db()`,
including `main.py`'s `lifespan()` and `scripts/seed_regime_scenarios.py` —
must not:

- call `Base.metadata.create_all()` against PostgreSQL;
- create a missing PostgreSQL table;
- alter PostgreSQL schema in any way;
- stamp an Alembic revision;
- automatically invoke `alembic upgrade` or any other migration command.

### 2. PostgreSQL startup invariant

Application code may complete startup against PostgreSQL only when the
database's current Alembic revision head-set exactly equals the repository's
migration-graph head-set. `init_db()` enforces this by comparing
`MigrationContext.get_current_heads()` (read from the live connection)
against `ScriptDirectory.get_heads()` (read from the repository's migration
scripts) using Alembic's own Python API — no shelling out, no new dependency
(`alembic` is already a production requirement), and no mutation.

A mismatch — including an empty/unversioned database, a database behind
head, a database on an unrecognized revision, or any other head-set
inequality — raises `DatabaseSchemaNotCurrentError` and aborts startup. There
is no environment-specific exception: local, VPS, and any other runtime
environment enforce the identical invariant. Partial availability against an
incompatible schema is not an accepted state — a process is not reliably
healthy merely because some endpoints might still work against a stale
schema.

The raised error states the database's current revision(s), the
repository's expected head(s), and the remediation (`alembic upgrade head`).
It never includes a database URL, credentials, or other connection secrets.

### 3. SQLite is unchanged

`create_all()` is not forbidden as a mechanism — the boundary is
backend-specific, not `create_all()`-specific. For the SQLite path (detected
via the existing `_is_sqlite` flag in `database.py`):

- `init_db()` continues to call `Base.metadata.create_all(bind=engine)`
  exactly as before;
- `migrate_legacy_data()`'s existing `_is_sqlite`-gated `ALTER TABLE` patches
  continue unchanged;
- test fixtures constructing their own ephemeral SQLite engine and calling
  `Base.metadata.create_all()` directly continue unchanged and are not
  targeted by this decision.

### 4. Deployment responsibility is unchanged

Running `alembic upgrade head` against PostgreSQL remains an explicit
operational/deployment responsibility performed by a human or a future,
separately-decided deployment automation step. This decision does not
introduce automatic migration execution, distributed locking, a migration
orchestration platform, or any startup retry/self-healing behavior. It makes
the *absence* of deploy-time migration automation loudly visible (via a hard
startup failure) rather than closing that operational gap itself.

### 5. Seed scripts inherit the boundary

`scripts/seed_regime_scenarios.py` and any future script calling the shared
`init_db()` inherit this boundary automatically and require no separate
schema-ownership logic of their own.

## Rationale

- The boundary this record ratifies is not new — `ARCHITECTURE.md` already
  states it in prose. What was missing was (a) a citable ADR binding future
  contributors to it, matching this repository's established pattern for
  every other durable architectural boundary (ADR-001 through ADR-016), and
  (b) code that actually enforces it, since the prose statement alone did not
  prevent at least three prior recurrences of the same incident.
- A hard, environment-uniform failure was chosen over a warn-only or
  environment-specific policy (e.g., "warn on VPS, fail locally") because a
  process serving requests against a structurally incompatible schema is not
  a safely degraded state — it is silently wrong in a way that is strictly
  worse than an explicit, immediate startup failure a human can act on.
- Confirming the boundary at the database-backend level (`_is_sqlite`)
  rather than the human-environment level (`APP_ENV=local`/`vps`) is
  necessary because a `local`-role process can still point at the same
  PostgreSQL instance a `vps`-role process serves; gating by human
  environment would have left that configuration unprotected.

## Consequences

Positive:

- Closes a failure class that has recurred at least four times against the
  same database, with a fix scoped to a single function.
- Converts silent, delayed-discovery schema drift into an immediate,
  actionable startup failure naming the exact remediation.
- Eliminates the confirmed four-way PM2 cluster race on `CREATE TABLE` for
  any newly-added, not-yet-migrated PostgreSQL table.
- Introduces no new dependency, no new infrastructure, and no change to the
  SQLite or test-fixture paths.

Tradeoffs:

- A developer who forgets to run `alembic upgrade head` after pulling new
  migrations now cannot start the application against PostgreSQL at all
  (previously, `create_all()` silently and temporarily masked the omission).
  This is accepted as the correct trade — the previous behavior is the
  incident this record exists to stop.
- No deploy-time migration automation is introduced, so a VPS deploy that
  ships new migrations without a preceding manual `alembic upgrade head`
  will now fail to start rather than partially serving stale-schema
  responses. This is accepted per §2's core judgment that partial
  availability against an incompatible schema is not an accepted state.

## Alternatives Considered

1. **Warn-only on VPS, hard-fail only locally (the initial reconnaissance
   recommendation).** Rejected on further review — a process that starts
   against a structurally-behind database is not reliably healthy merely
   because some endpoints may still work; environment-specific leniency
   reintroduces exactly the "looks fine, is actually wrong" state this
   record exists to eliminate.
2. **Auto-run `alembic upgrade head` at startup.** Rejected. Under the
   confirmed 4-instance PM2 cluster, four processes would race to run
   migrations concurrently; Alembic provides no built-in cross-process
   locking for this, and solving it would require exactly the distributed-
   lock machinery this decision's scope explicitly excludes. It also
   reintroduces "the application mutates its own schema," the same shape of
   problem as `create_all()`, merely relocated.
3. **Gate the boundary on `APP_ENV` (local/vps) instead of `_is_sqlite`.**
   Rejected — the risk is which database backend is targeted, not which
   human/process role is running; `APP_ENV=local` can point at the same
   PostgreSQL instance a `vps`-role process serves, so an `APP_ENV`-keyed
   gate would leave that configuration unprotected.
4. **Leave `create_all()` in place and rely on developer discipline plus the
   existing `ARCHITECTURE.md` prose statement.** Rejected — this is the
   status quo that has already failed at least three times before this
   record.

## Explicit Non-Goals

This decision does not introduce or authorize: automatic migration execution
on application startup; distributed locks or migration mutexes; a migration
orchestration platform; a schema diff engine; automatic Alembic stamping;
destructive or self-repairing schema behavior; any change to
`ecosystem.config.js`, PM2 configuration, deployment scripts, CI/CD, or
container/service-manager configuration; or any change to product,
optimizer, Decision Intelligence, Execution Intelligence, or Evaluation
behavior.

## Relationship to Prior Documentation

- **`docs/architecture/ARCHITECTURE.md`:** this record ratifies, as a binding
  ADR, the boundary that document already states in prose ("PostgreSQL uses
  Alembic"). The document is not restated in full here; this ADR is the
  citable authority a future contributor must consult before reintroducing
  `create_all()` against PostgreSQL.
- **`docs/engineering/DECISION_LOG.md` (2026-07-06 entry):** this record
  directly addresses the root cause that entry diagnosed but did not, at the
  time, convert into a binding architectural rule.

## Reopen Conditions

This decision is superseded only by a later ADR that explicitly names this
record and addresses one or more of: introducing deploy-time or startup-time
automatic migration execution (would need to resolve the multi-instance
locking concern in §3 of Alternatives Considered); changing the PostgreSQL
failure policy from hard-fail to any conditional or environment-specific
behavior; or extending schema ownership rules to a database backend other
than SQLite or PostgreSQL. Runtime behavior, new UI language, or persisted
data drift cannot amend this record by implication.
