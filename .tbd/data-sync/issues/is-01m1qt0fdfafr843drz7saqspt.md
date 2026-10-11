---
type: is
id: is-01m1qt0fdfafr843drz7saqspt
title: "Exhaustive tier: test_verify_claim's two full decisions add about 400 s against main's 892-930 s under an 1800 s budget"
kind: task
status: closed
priority: 3
version: 3
labels: []
dependencies: []
parent_id: is-01m1qgrj2q8kmrbqrgvkaksn87
created_at: 2026-09-05T03:32:47.663Z
updated_at: 2026-10-06T08:34:54.862Z
closed_at: 2026-10-06T08:34:54.862Z
close_reason: "Done: the option 'accept it and record the new measurement' was taken. The bead's 2026-09-05 note records the exhaustive tier at 649 s on PR 84 (merged 2026-09-05), inside the 1800 s budget; the tier has since been re-sharded."
resolution: null
duplicate_of: null
---
The merge of PR 82 into PR 79 puts two full standard-library decisions (verify_claim.py on 19/5 in about 36 s, and the ten-row falsification test, each Condition 5 row a full 19/5 sweep) into the exhaustive_exact tier, beside main's own minimal_verify and third-party full decisions. main measured that tier at 892 s on CI's two-core runner and 930 s on four cores under EXHAUSTIVE_SUITE_BUDGET_SECONDS = 1800; this branch adds roughly 400 s, so headroom drops from about 2x to about 1.4x. Either accept it and record the new measurement, or move the ten-row falsification test behind a narrower selection (only the Condition 5 rows need the sweep).

## Notes

Measured on the PR 84 branch: the exhaustive tier runs 13 verifier nodes in 649 s. The full push gate on the merged tree took 1426 s for 2012 fast tests, so the tier still sits inside the 1800 s budget.
