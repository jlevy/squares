---
type: is
id: is-01m4qhcw0287k3633q1rhz4jwn
title: "Workbench trajectory cost check: compare the best of three timings with the 400 ms ceiling (flaked on #512)"
kind: bug
status: closed
priority: 3
version: 10
delegate: claude-workbench-cost-fix-20261019
labels:
  - testing
dependencies: []
parent_id: is-01m4padgs7fh6ze3tbh57d5ar1
hold: null
hold_until: null
created_at: 2026-10-12T07:49:22.050Z
updated_at: 2026-10-19T23:01:42.589Z
started_at: 2026-10-19T17:01:19.072Z
closed_at: 2026-10-19T23:01:42.589Z
close_reason: "Timing fix landed in #685 (02b644c6f, 14fd9e27f); #538's record moved the play attribution to think-8vsk in #646 (028bc72ec, site v0.7.35, deploy verified 4708/4708); #538 follow-up posted: https://github.com/jlevy/squares/issues/538#issuecomment-6279239104"
resolution: null
duplicate_of: null
---
packages/workbench/tools/workbench_tools/animate_view_contract.py (about lines 1036-1043, run by workbench_tools.check_frontend as the "workbench browser behavior in Chromium" step) times six trajectory builds (n = 11, 100, 324; styles physics and bodies) once each and requires each under 400 ms and 4 MB. On PR #512, run 38182457550 attempt 1 (frontend job 114597711232, head 604699ee1) failed with "a trajectory costs over 400 ms or 4 MB: [(324, 'physics', 454, 1807280)]"; attempt 3 at the same commit passed. Proposed fix (not implemented): time each build three times and compare the fastest with 400 ms; keep the 4 MB limit on one measurement and both ceilings unchanged. Done when the check uses the best of three, the ceilings are unchanged, and check_frontend passes.

## Notes

2026-10-19 claude coordinator: fix 02b644c6f (measurePhysics cache-bypass API + best-of-three in animate_view_contract) on claude/workbench-trajectory-best-of-three; ported into PR #685 (f3495bc0e) under its site v0.7.32 successor. 217/217 node tests; workbench check passed locally (322 ms fastest). Close when #685 merges.


The parent of this bead is:
---
type: is
id: is-01m4padgs7fh6ze3tbh57d5ar1
title: "Intake pass 2026-10-11: six new upper-bound reports, two n17 issues, four unread comments, six watched repositories"
kind: epic
status: in_progress
priority: P1
version: 99
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
child_order_hints:
  - is-01m4padhpzys6zpwepcve5pwxm
  - is-01m4padjx7fep1w6y30v4pqz9n
  - is-01m4padkz7c8b0chp1f85vmfy8
  - is-01m4padmx9cdj5hsv7snr426rb
  - is-01m4padnyzybc7ms1bryby9ax2
  - is-01m4padq3szbdty8bmp3r2bxqh
  - is-01m4padr3md3xwace5s7695t9v
  - is-01m4pads1y316jmhb4rp0fpvpg
  - is-01m4padszrtqcj8b3qyff911cd
  - is-01m4padtzpm1sj8gg4ygyrjjck
  - is-01m4pan44x8vekhh54vsb2vhan
  - is-01m4pan85d4sartjf3m3h3p1b6
  - is-01m4pcbmdj7qjggrjemdjsct5v
  - is-01m4pcbp72f9p5qad5yy2jgfmf
  - is-01m4pcbr88e5we5fgkmf7qhfgv
  - is-01m3wx2hm1ezys1w50g5pk9eet
  - is-01m4pcccsnaq8tp3nvze2wfpcs
  - is-01m4pd6dbc6j1wyjg6n62dv8ag
  - is-01m4pe36zqv5wkdyp33hpb5ahh
  - is-01m4pfeqkmdtcze4v746vtn23v
  - is-01m4pff4kjeeg11941am6tb84v
  - is-01m4pn087wev95haqgv9rffnj9
  - is-01m4pgzs74gxzc2c2srp9hg2vw
  - is-01m4ptzjgr1nmf0264k67x4ypn
  - is-01m4pv16sta8jkhsfkk7sgc46n
  - is-01m4pvgyhtqs5v7fvt63f9653r
  - is-01m4qaftjqtfy02k7kdaya84an
  - is-01m4qafvvrkvvc884100g1ch9t
  - is-01m4qdj56xc8fnfdn0yz2ddvp9
  - is-01m4qdvm05t297yghevg6nm7gz
  - is-01m4qfk7nzmgrwxdj50b3h3k5w
  - is-01m4qhcw0287k3633q1rhz4jwn
  - is-01m4qhcybbrt2fnj26vxs9595n
  - is-01m4qjdc5dyqnrex0vceagw93z
  - is-01m4qjdm5hbj0m43ymvkcjr2jm
  - is-01m4qkwr49aszyn8q68yde48q9
  - is-01m4qkww5wn1cvm898ebvwfcyx
… [73 lines omitted]

2026-10-19 coordinator (session 013djgnY): reopened. Closing it broke check_bead_tree on every branch: main's result-requests.yaml #538 entry still has a queued ask, bead and answer_bead naming think-1bm2. Close only with a records change that marks #538's ask done (and attributes the Animate play message, which close_when also requires), posts the #538 reply, and closes the issue once the site agrees. The timing fix itself landed in #685 (14fd9e27f).

2026-10-19 lane-645 (review G2 on #646): close condition updated. #646 moves #538's answer_bead and the queued play ask to think-8vsk and marks the timing ask done; close this bead once #646 has merged and the #538 follow-up reply is posted. The play attribution belongs to think-8vsk.
