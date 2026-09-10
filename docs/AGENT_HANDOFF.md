# Wealth OS — Agent Handoff

This file is the lightweight source of truth for the current Wealth OS working state.
Keep it short. Update it whenever the active track, branch, agent/session, or next action changes.

## Current Work

- Project: Wealth OS / Portfolio Intelligence Platform
- Repository: `patipan-kong/Portfolio_Intelligence_Platform`
- Current track: Goal ↔ Portfolio Mandate Visibility
- Current branch: `feature/wealth-os-goal-portfolio-mandate-visibility`
- Current phase: Track complete — awaiting commit/PR
- Latest active coding agent/session: Claude Code — Goal Portfolio Mandate Visibility Slice 1
- Last completed step: Slice 1 final review passed; Goal ↔ Portfolio Mandate Visibility complete
- Next action: commit the reviewed track, push feature branch, and open PR

## Previous Track

- Track: Decision & Execution Lifecycle Completeness
- PR: #39
- Status: MERGED
- Delivered:
  - REJECTED recommendations can preserve optional human rationale
  - EXPIRED recommendations persist `expiry_reason` as `superseded` or `aged_out`
- Final track decision: `TRACK COMPLETE`

## Working Rules

1. Start new product work from an up-to-date `main`.
2. Use one feature branch per track.
3. Flow: recon → implement → review → commit → push feature branch → PR → merge on GitHub → pull `main`.
4. Never push a feature branch directly to `main` with `<feature>:main`.
5. Before resuming work, read this file and confirm branch + phase + next action.
6. When switching coding agents/sessions, update `Latest active coding agent/session` immediately.
7. When a PR merges, record it under Previous Track before starting the next track.
8. Keep detailed implementation reports in PRs/docs; this file is only the handoff snapshot.

## Update Template

When handing off, update only these lines unless more context is genuinely needed:

```text
Current track:
Current branch:
Current phase:
Latest active coding agent/session:
Last completed step:
Next action:
```
