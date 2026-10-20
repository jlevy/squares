---
type: is
id: is-01m4pcp9t15wsdbwb9kdhw58eq
title: Register exact packings at the witnesses' printed sides where they fall below the 14-decimal verified bound, in one batch
kind: task
status: in_progress
priority: 2
version: 4
delegate: claude-code@vm
labels:
  - regularization
dependencies: []
parent_id: is-01m4mdb1j4atn6yvmtcf93eqmt
hold: null
hold_until: null
created_at: 2026-10-11T21:07:53.793Z
updated_at: 2026-10-12T11:32:19.400Z
started_at: 2026-10-12T11:32:11.970Z
---
The same-side re-solve produces exact rational packings at a decimal witness's printed side that lie about 1e-14 below a verified bound rounded up at fourteen decimals (pilots: 37, 87, 101, 200, 260; 17 waits on the n = 17 hold think-x4v4). Each is a new verified upper bound, so policy row 3 holds the drawing until it is registered. One W1/W2 import with a regularizations item per count closes the reported-verified gap and admits the drawings. Owner question 3 in its current, small form; needs the owner's yes first (see the pilot-decisions bead).

## Notes

2026-10-12, owner answer q6 "yes regularize and correct always": every exact view whose side is below the verified bound is registered (a new verified upper bound), in batches, then its drawing admitted; no longer waiting on a yes. Input: the full run's receipt `candidates` list (row 3 on either output). n = 17 still waits on think-x4v4.

2026-10-12: done as T-151 on jlevy/squares#549 — 60 counts, 5.4e-20 to 9.9e-15 below the ceilings, V3/C3, S1; printed values kept, exact_form moves. Bounds refreshed from the records admit 16 of the 23 held counts. Closes when #549 merges (after #516's T-147..T-150).
