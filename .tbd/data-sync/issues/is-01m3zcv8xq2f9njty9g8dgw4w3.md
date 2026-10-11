---
type: is
id: is-01m3zcv8xq2f9njty9g8dgw4w3
title: Taylor relaxation for the n17 branch and bound, with verifier support (lane P2, F1 rank 4)
kind: task
status: open
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T22:48:04.791Z
updated_at: 2026-10-03T00:08:55.378Z
---
Rank 4 of the cost-reduction plan (review section 4.2). Add a first-order Taylor relaxation of the trigonometric coefficients to devtools/pilot_n17_subpattern_bb.py as an option (off = byte-identical certificates), extend verify_n17_bb_certificate.py to re-prove it exactly with mutant tests, measure on A against 41,598 nodes, and Knuth-estimate two or three stalled interior classes. Falsifier: Taylor estimates above 10^6 nodes at arity 8. Lane P2 started 2026-10-02 22:55 UTC.

## Notes

2026-10-03 00:10 UTC. Taylor committed ff5471e89 (falsifier met). P2 diagnostic (uncommitted: diagnose_n17_bb_losses.py, prototype_n17_bb_coupled.py, test): on A, I8 and N8, 80-85% of closable open nodes are held by the range of the pair normals over the angle box (98% of pair terms have both squares' normals live; 91% give no LP cut), not by the gap (15-20%) or the chord. A coupled McCormick form applies to only 1.2-2.4% of pair terms and does not change the estimates; I8 and N8 stay above 1e6. Conclusion: no relaxation fixes this; the lever, if any, is narrowing centre boxes (one cheap test running). Otherwise the branch and bound stays at arity <= 7 and interior arity-8 crowds go to the kernel.
