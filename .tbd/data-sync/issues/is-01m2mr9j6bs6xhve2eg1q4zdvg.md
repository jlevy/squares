---
type: is
id: is-01m2mr9j6bs6xhve2eg1q4zdvg
title: "PR #186 review R5: non-finite wall values disable the gate"
kind: bug
status: open
priority: 1
version: 2
labels:
  - ci
  - validation
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T09:20:46.794Z
updated_at: 2026-09-17T02:06:22.351Z
---
At exact PR #186 head 46b0d368, packing/devtools/check_pr_wall.py _number accepts PyYAML .nan because it checks type and value <= 0 but not math.isfinite. Reproduction: load a valid minimal wall register with budget_seconds: .nan and median_seconds: .nan, then judge a 500-second Measurement. The tool returns status passed, no failures, and notes 500s is inside the nans budget and 500s is nanx the median. packing/devtools/check_gate_budgets.py wall_problems also accepts the budget because nan > 180 is false. This is a fail-open soundness defect. During PR #186 reconciliation, reject non-finite values in every wall numeric field, require integer-valued run IDs and min_samples, and add .nan/.inf negative tests proving both load_walls and the static wall check fail closed. Do not merge the PR until the repaired exact head has green integrated wall checks.

## Notes

2026-09-16 evidence audit at da2259fb: implementation SATISFIED (check_pr_wall.py:235-250 refuses bool, NaN/inf, <=0 and fractional integer fields; check_gate_budgets.py:188-196 fails on WallError; commits 5ca38b03, 5b5133c4). Tests covered only .nan in budget_seconds through load_walls; .inf and wall_problems cases are being added on #188. Close after green exact-head hosted CI.
