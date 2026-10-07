---
type: is
id: is-01m3z64qhhagqsd1wkzxnr9fd7
title: "H-264 per-state exclusion pilot: 17-owner kernel on residue states (lane K2)"
kind: task
status: open
priority: 1
version: 4
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-02T20:50:54.641Z
updated_at: 2026-10-05T05:37:02.992Z
---
Session 168. Two residue states (F1 distance 6, N1 distance 4) ran as 17-cell patterns
through the kernel at 32 bins: both certified stalls at the 45-minute cap after rounds
3-4 (receipts h-F1.json, h-N1.json in the session scratchpad, not committed).
A 2-hour N1 run is in flight.
Falsifier: fewer than half of 10-20 sampled orbits close within 2 CPU-hours each.
Next: commit the receipts to X048-session-168-pilots, decide H-264, and feed the
cost-reduction lanes.

## Notes

2026-10-03 00:40 UTC. N1 --check-saved PASS_SAVED_CLOSED in a fresh process (receipt
committed d97187d52: certificates/N1-state-pending/check-saved.json; 82 steps, 2,624
rows, 8,470 regions, closure interior-W step 81). Full verification assigned to F2 with
the new verifier 5c550f7c (pending R6 review of that verifier).
K2 queue: W7 at 32 then 16 bins with octagon core, then the 539-orbit south-wall class,
then N1 at the smaller size.

2026-10-05 (PR 347 status survey).
Work has run though the status is open.
N1 (distance 4) closed in 3,723 s and was admitted in exp-250; F1 (distance 6) stalled
at the 45-minute cap.
The falsifier needs 10 to 20 sampled states, so H-264 has no verdict yet.
PR 347 adds a dated progress annotation to H-264’s record.
