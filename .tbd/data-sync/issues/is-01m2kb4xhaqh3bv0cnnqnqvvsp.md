---
type: is
id: is-01m2kb4xhaqh3bv0cnnqnqvvsp
title: "Lane 3: CI guardrail -- PR-wall budget, no empty PR-tier records, no record ratchet (G1-G3, G5 hook, bead hygiene)"
kind: task
status: in_progress
priority: 1
version: 7
labels:
  - validation
  - ci
dependencies: []
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
child_order_hints:
  - is-01m21mgmrpatjx0n66y23mmjc8
  - is-01m2m5a2v1gwa2he9nvev4csqb
  - is-01m2m5ad594cv9k37w6nm9e533
created_at: 2026-09-15T20:11:48.648Z
updated_at: 2026-09-16T03:49:32.238Z
---
Lane 3 of think-xfqk (2026-09-15). The register that was built to stop the first CI spiral (gate-budgets.yaml, check_gate_budgets.py, gate_budgets.judge) let the second through: seven of nine tiers had no record, suite's record was re-based three times (102.83 -> 162.62 -> 118.72 -> 183.44 s) while its ceiling followed (205 -> 260 -> 237 -> 275 s), and nothing budgets the PR wall OR-14 targets (154 s median on 09-06, 284-298 s on 09-15).

Deliverables, branch claude/ci-wall-budget, PR into main:
- G1: devtools/check_pr_wall.py reads a run's jobs from the GitHub API, computes run wall to the aggregator's start and per-job queue/setup/work, fails over a declared 180 s budget (OR-14's outer edge) or a >=20% regression against a recorded median for the workflow and PR kind, and says so when a run cannot be judged. One step in packing-required, one trailing pr-wall job in pages.yml. Fixture tests: pass, budget failure, regression failure, unmeasurable.
- G2: check_gate_budgets fails a tier a PR job runs with no recorded cost; checks and sweeps recorded from hosted runs, geometry refreshed.
- G3: record history kept in the register; a raise beyond the declared rise without an attribution entry (per-step or per-file costs and a named cause) fails.
- G5: consumer hook for lane 2's per-file report.
- Bead hygiene and BC-340's follow-up pointer.

## Notes

2026-09-16 review repair: PR #186's first hosted wall attempt never parsed under runner Python and its unmeasurable verdict exited zero. ba34637b pins uv 0.12.8/Python 3.14.7/PyYAML 6.0.3 in both jobs, uses the C safe loader, fails closed, removes fixture whitespace, and adds exit/workflow negative controls (62 focused tests; exact standalone command starts). The PR is still not merge-ready: it conflicts semantically with #183/#185 and the 180s budget has no observed variance margin (Pages 173/185s; validation 180s). Rebase after both land, refresh medians, and require a fully green integrated run; tracked as think-3919.
