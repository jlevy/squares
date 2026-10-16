---
type: is
id: is-01m51j2bqzex9th23e720jv38w
title: "Review: retained replays of T-185 to T-190 (stage 4 review lane, upper bounds registered 15 October)"
kind: task
status: in_progress
priority: 1
version: 7
delegate: user-eb-review-185-190
labels:
  - validation
dependencies: []
parent_id: is-01m51hyxstsa9ptekd2ss26ksn
hold: null
hold_until: null
created_at: 2026-10-16T05:13:30.623Z
updated_at: 2026-10-16T05:32:01.238Z
started_at: 2026-10-16T05:13:42.512Z
---
Stage 4 review lane (W2) for the upper-bound entries registered on 15 October at V0/C0 whose next rung is "independently review the retained replay": T-185 (#506, 175), T-186 (#593, twelve counts), T-187 (#606, 146), T-188 (211), T-189 (#607, 237) and T-190 (237). Model: docs/project/reviews/review-2026-10-14-upper-bound-imports-561-593.md (the review of T-161 to T-183). Deliverable: docs/project/reviews/review-2026-10-16-upper-bound-imports-<issues>.md on its own branch and draft PR, which reproduces each packet's retained replay (devtools.upper_bound_reports PACKET check --replay), runs the third exact route, re-fetches each pinned scope and checks digests, measures credit, grades findings, and says per entry whether V3/C3 is supported and what each count's adoption should be. It moves no rung; the records lane that follows (a separate bead) writes the rungs and adoptions.

## Validation
- Claim: the finite upper bounds T-185 to T-190 state, their retained rational certificates and replays in their packets, the maintained exact routes and the third route.
- Run: upper_bound_reports check --replay per packet, the third route's citations check, pinned-scope fetch and digest checks.
- Cost: the 14 October review of 28 certificates replayed in minutes per packet on this host; estimate under 1 CPU-h here.
- Budget status: runnable (under the 40 CPU-h cap; small).
- Depends on: nothing; all on main e2e018f32.
- Done when: the review document is on a pushed branch with its PR, findings graded, and per-entry verdicts stated.
- Machine note: serial, one process; shares the 4-core host with the regularization lane (2 workers).

## Notes

2026-10-16 05:29Z user-eb-review-185-190: replay evand-n146-2026-10-14 check --replay (T-187, n=146): 3 jobs decided again, every one equal to its retained row, exit 0, 20 s wall (05:27:50Z-05:28:10Z), worktree review-185 at e2e018f32.

2026-10-16 05:29Z user-eb-review-185-190: replay couzo-verified-bounds-2026-10-14 check --replay (T-188, n=211): 3 jobs equal to retained rows, exit 0, 45 s wall (05:28:10Z-05:28:55Z).

2026-10-16 05:32Z user-eb-review-185-190: replay couzo-n237-2026-10-15 check --replay (T-190, n=237): 3 jobs equal to retained rows, exit 0, 43 s (05:28:55Z-05:29:37Z).

2026-10-16 05:32Z user-eb-review-185-190: replay couzo-certificates-2026-10-14 check --n 237 --replay (T-189's in-scope count): 3 jobs equal, exit 0, 36 s (05:29:37Z-05:30:13Z); the packet's other 22 counts (beyond-horizon, no entry here cites them) queued after the in-scope work.

2026-10-16 05:32Z user-eb-review-185-190: replay couzo-certificates-2026-10-11 check --n 175 --replay (T-185): 3 jobs equal, exit 0, 31 s (05:30:13Z-05:30:45Z); the packet's other 14 counts (T-152's and beyond-horizon rows) queued after.
