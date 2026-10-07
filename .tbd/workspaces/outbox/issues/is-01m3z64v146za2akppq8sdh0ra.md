---
type: is
id: is-01m3z64v146za2akppq8sdh0ra
title: "Cost reduction to hundreds of CPU-hours: pruning and route redesign review (lane F1, done)"
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:58.212Z
updated_at: 2026-10-02T22:46:28.608Z
closed_at: 2026-10-02T22:46:28.608Z
close_reason: Review committed in 83783ab29; ranked plan dispatched to K2 (rank 1) and S2 (rank 2)
resolution: null
duplicate_of: null
---
Owner request, Session 168: the residue is costed at 4e3-4e4 CPU-h; find layered sound
ways (covers, conditioned sub-patterns, counting packets, dominance, shared
certificates, coarse certificates exploiting >=1e-2 margins, LP per state) to reach
hundreds. Deliverable:
docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md (uncommitted until
reported).

## Notes

Review committed 83783ab29:
docs/project/reviews/review-2026-10-02-n17-cost-reduction-pruning.md.
Ranked plan: (1) octagon core and W7 at 32 and 16 rows (K2, running); (2) residue
arity-8-to-10 sweep (S2, after the finish stage); (3) certify in marginal-coverage
order; (4) Taylor relaxation for the branch and bound; (5) per-state tail; (6) Mode B
after a wall prefix.
Model: about 10^3 CPU-hours on count and size, hundreds only with a short tail or with
F2’s rate gain.
