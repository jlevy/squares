---
type: is
id: is-01m4m58ech2c366x1cpzzrgm17
title: "CI: replace expired measure-verifier measurement waiver for website integration"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex-verifier-budget-fix
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-11T00:19:30.832Z
updated_at: 2026-10-11T00:19:38.348Z
started_at: 2026-10-11T00:19:38.347Z
---
Website integration at 13b4f557e fails tests/test_gate_budgets.py::test_every_tier_the_workflow_runs_on_a_pull_request_is_recorded in suite-d job 114347133704, run 38097761292. The measure_verifier tier remains pending under think-th8p through 2026-10-10, and the hosted runner has moved past that date. Fulfill the original measurement using devtools.read_tier_walls on completed hosted jobs at the current three-step reference shape, remove the pending fields, preserve the absolute ceiling and test the live register. Existing owner think-th8p is in_progress on claude-code@vm; this child tracks applying its missing receipt to the website integration branch.
