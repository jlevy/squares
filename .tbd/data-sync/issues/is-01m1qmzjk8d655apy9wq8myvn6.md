---
type: is
id: is-01m1qmzjk8d655apy9wq8myvn6
title: "Directional rounding: 38 case bodies state a lower bound rounded up past what is proved"
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T02:04:55.272Z
updated_at: 2026-09-05T02:06:59.989Z
---
Found by the residual audit of PR 80. check_case_prose renders bound decimals with ROUND_HALF_UP, so 38 open-case bodies state a lower bound strictly above the proved value (n-028: 5.358899 against sqrt(19)+1 = 5.3588989...) and 16 state an upper bound below it. PR 80 fixes it with a directional rule (lower bounds rounded down, upper bounds rounded up: its safe_decimal_at / _field_matches_claim with ROUND_FLOOR / ROUND_CEILING) plus tests test_decimal_bound_rendering_is_directionally_safe and test_fix_rewrites_nearest_decimals_without_strengthening_bounds, and re-renders the affected case bodies (git diff HEAD 04127189 -- packing/devtools/check_case_prose.py packing/tests/test_case_prose.py 'packing/frontier/n-0*.md'). Port the rule and the tests onto this branch's check_case_prose (which has its own D-445/D-451 shapes), then regenerate or hand-fix every affected body with each figure re-derived from the front matter; record as a defect entry (class soundness, direction flattering: a stated lower bound above the proved one). Do not port PR 80's novelty rescoping of those bodies in the same commit.
