---
type: is
id: is-01m4vczk3s9agjadp837m0479x
title: "Stack 498: #511/#530 must merge atomically with #580 (yield_to_bound, BOUND_FIRST)"
kind: task
status: closed
priority: 1
version: 2
labels:
  - stack-498
  - merge-constraint
dependencies: []
created_at: 2026-10-13T19:49:10.393Z
updated_at: 2026-10-14T02:58:06.572Z
closed_at: 2026-10-14T02:58:06.572Z
close_reason: "Merged atomically: #511, #530, #548, #549, #559 and #580 in one stack merge at aeef99e (14 Oct 2026)"
resolution: null
duplicate_of: null
---
Formal stack 498 has merged layers singly: #487 on 11 October, and #497 alone at
2026-10-13T18:14:15Z. Two layers carry correctness fixes that live in #580 only, so
neither may reach `main` without #580 in the same stack merge. The merge must be
targeted at #580 or above.

- **#511** (regularization tools, `claude/busy-pascal-vgiccb`): review B's B4 (Medium)
  is fixed only by #580's `051082536` (`yield_to_bound`). Without it,
  `regularize_evand.decide` takes `governing = dict(decisions["same"] or
  decisions["solved"])`. So wherever the solve reaches `U`, a same-side view above `U`
  still governs over the solved view at `U`. That contradicts the owner's answer to
  question 13 (13 October). Review B listed 14 counts where `U` is rational and below
  `s_W`. Review C on #511 (C2, Medium,
  https://github.com/jlevy/squares/pull/511#pullrequestreview-5508789148) found this
  unrecorded.
- **#530** (grid slack, `claude/busy-pascal-vgiccb-grid`): review B's B2 (Medium) is
  fixed only by #580: `attempts_for` and `BOUND_FIRST` in `regularize_grid_slack.py`
  try a rational `U` first. Review C on #530 confirmed that `051082536` is an ancestor
  of #580's head and that the fix reaches #530 only in the atomic merge.

Done when #511, #530 and #580 reach `main` in one stack merge targeted at #580 or
above, or when `yield_to_bound`, `attempts_for` and `BOUND_FIRST` are moved down into
#511 and #530 so that each layer stands alone. Until then, a merge gate for #511 or
#530 must treat this bead as blocking. The PR bodies of #511 and #530 state the
constraint and link this bead.
