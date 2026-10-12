---
type: is
id: is-01m4m58ech2c366x1cpzzrgm17
title: "CI: replace expired measure-verifier measurement waiver for website integration"
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex-verifier-budget-fix
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-11T00:19:30.832Z
updated_at: 2026-10-11T01:13:23.089Z
started_at: 2026-10-11T00:19:38.347Z
closed_at: 2026-10-11T01:13:23.089Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Website integration at 13b4f557e fails tests/test_gate_budgets.py::test_every_tier_the_workflow_runs_on_a_pull_request_is_recorded in suite-d job 114347133704, run 38097761292. The measure_verifier tier remains pending under think-th8p through 2026-10-10, and the hosted runner has moved past that date. Fulfill the original measurement using devtools.read_tier_walls on completed hosted jobs at the current three-step reference shape, remove the pending fields, preserve the absolute ceiling and test the live register. Existing owner think-th8p is in_progress on claude-code@vm; this child tracks applying its missing receipt to the website integration branch.

## Notes

Staged budget-only receipt at branch head 13b4f557e; no commit or push by this worker. Maintained read_tier_walls --tier measure_verifier --job-id over eleven completed jobs separated ten 3-of-107 readings (59.12, 73.08, 59.92, 87.66, 71.80, 74.36, 72.40, 73.55, 90.06, 72.30 s; geometric mean 72.83 s, spread 1.52x) from one 3-of-110 reading (57.89 s, run 38093246298). Canonical measured_where records all run/job IDs. Pending fields removed; 90 s ceiling, reference and policy retained. Exact failing test reproduced before editing: 1 failed in 1.99 s. After editing, project Python 3.14 pytest tests/test_gate_budgets.py -q -p no:cacheprovider: 92 passed, 1 expected skip in 2.91 s. devtools.check_gate_budgets passed: 15 tiers, 10 recorded, every PR tier recorded and all ceilings within 2x headroom. git diff --cached --check passed. Parent owns senior review, commit/push and final hosted CI; leave this bead open until those complete. Original think-th8p remains claimed by claude-code@vm.
