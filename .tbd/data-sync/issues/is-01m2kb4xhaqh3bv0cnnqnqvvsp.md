---
type: is
id: is-01m2kb4xhaqh3bv0cnnqnqvvsp
title: "Lane 3: CI guardrail -- PR-wall budget, no empty PR-tier records, no record ratchet (G1-G3, G5 hook, bead hygiene)"
kind: task
status: in_progress
priority: 1
version: 4
labels:
  - validation
  - ci
dependencies: []
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
child_order_hints:
  - is-01m21mgmrpatjx0n66y23mmjc8
created_at: 2026-09-15T20:11:48.648Z
updated_at: 2026-09-16T03:09:02.250Z
---
Lane 3 of think-xfqk (2026-09-15). The register that was built to stop the first CI spiral (gate-budgets.yaml, check_gate_budgets.py, gate_budgets.judge) let the second through: seven of nine tiers had no record, suite's record was re-based three times (102.83 -> 162.62 -> 118.72 -> 183.44 s) while its ceiling followed (205 -> 260 -> 237 -> 275 s), and nothing budgets the PR wall OR-14 targets (154 s median on 09-06, 284-298 s on 09-15).

Deliverables, branch claude/ci-wall-budget, PR into main:
- G1: devtools/check_pr_wall.py reads a run's jobs from the GitHub API, computes run wall to the aggregator's start and per-job queue/setup/work, fails over a declared 180 s budget (OR-14's outer edge) or a >=20% regression against a recorded median for the workflow and PR kind, and says so when a run cannot be judged. One step in packing-required, one trailing pr-wall job in pages.yml. Fixture tests: pass, budget failure, regression failure, unmeasurable.
- G2: check_gate_budgets fails a tier a PR job runs with no recorded cost; checks and sweeps recorded from hosted runs, geometry refreshed.
- G3: record history kept in the register; a raise beyond the declared rise without an attribution entry (per-step or per-file costs and a named cause) fails.
- G5: consumer hook for lane 2's per-file report.
- Bead hygiene and BC-340's follow-up pointer.

## Notes

**2026-09-16:** pushed as PR #186. `check_pr_wall.py` and `read_tier_walls.py` with tests over four recorded runs; the three register rules (no empty pull-request record, no unattributed rise, history kept); records written for `checks` (145.53 s, seven runs, with its 1.46x attribution), `frontend` and `sweeps`; and the rules written into `OR-14`, `development.md` and agenda 036's BC-352 correction. Not done: no hosted run has exercised the wall check yet, four commits are still labelled `wip`, the per-file test-cost feed comes from lane 2, and the rest of the bead hygiene in `attic/ci-review/prior-work.md` is outstanding. `think-uwow` was reopened and is now parented here.
