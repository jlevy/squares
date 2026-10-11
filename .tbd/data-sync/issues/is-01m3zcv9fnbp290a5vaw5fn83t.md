---
type: is
id: is-01m3zcv9fnbp290a5vaw5fn83t
title: Octagon (second-order) core in the hull kernel; W7 at 32 and 16 rows (lane K2, F1 rank 1)
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T22:48:05.365Z
updated_at: 2026-10-03T00:59:51.236Z
closed_at: 2026-10-03T00:59:51.236Z
close_reason: "Falsifier fired: W7 does not close at 32 bins with the octagon core (a9d261fce)"
resolution: null
duplicate_of: null
---
Rank 1 of the cost-reduction plan (review section 4.1): a 4- to 16-fold cut in every kernel certificate's size and verification if W7 closes at 32 or 16 rows with the octagon core. Falsifier: W7 fails to close at 32 rows with the octagon. Lane K2 started 2026-10-02 22:45 UTC, after N1's --check-saved and standing verification.

## Notes

SETTLED, falsifier fired (a9d261fce). W7 at 32 bins with the octagon core stalls at a producer fixed point after 11 rounds (77 steps, 2,464 rows, 1,052 s, PASS_CERTIFIED_STALL; receipt receipts/kernel-octagon-W7-bins32.json). side-N0, interior-SW and interior-W never lose a row; side-N0 residual freezes at 0.590 x 0.911. Reading: the octagon cuts the core loss but not the domain loss (the union over the row's angles). Kernel certificates stay at 64 bins. Untested alternative: adaptive rows (angle bisection only where residual or partner cover is wide); K2 to assess feasibility in the grammar and checker.
