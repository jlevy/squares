---
type: is
id: is-01m0tb40e0zj6d4p2ecbkb5wf9
title: Diagnose the retained n4 seed3 post-check rejection
kind: bug
status: closed
priority: 0
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0t4phe1905yy2jk7czp1391
created_at: 2026-08-24T16:54:36.223Z
updated_at: 2026-08-24T17:15:43.513Z
closed_at: 2026-08-24T17:15:43.503Z
close_reason: Closed by f15d036 + exp-024 in 7ec721d. Exact retained n=4 seed-3 cell proved rows 16 and 21 were simultaneously outside the unchanged 1e-10 screen; the argmax-only retry shifted the maximum. One bounded retry now tightens the complete initial offending set and replays every original row. Regression requires repair_rows [16,21]. Exp-024 independently replays 4/4 admissible side-2 events, 14,301/14,301 settled, 0 unsettled, 16.966654s. Full 30-step gate passed in 30s.
resolution: null
duplicate_of: null
---
D-171. BasinEvent/v3 n=4 seed 3 reaches one fixed-point evaluation whose successful HiGHS result still violates pair row 16 by 4.209e-10 after the single D-164 bounded repair. The producer correctly stops and retains one unsettled evaluation, leaving the four-seed positive-control cell only 3/4 admissible. Acceptance: retain the exact event and failing cell evidence; classify whether the second result reflects cell-boundary ambiguity, solver tolerance, or an incorrect row; preregister any bounded remedy; preserve the 1e-10 screen and independent validity; never promote the current stop.

## Notes

2026-08-24 diagnosis complete in committed engine f15d036. Initial n=4 seed-3 cell had rows 16 and 21 already outside the unchanged 1e-10 screen by ~4.209e-10; argmax-only repair shifted the maximum. One retry now freezes and tightens the complete initial offending set and replays all original rows. Uncommitted exp-024 replication: n=4 seeds 0-3 all side 2, 14,301/14,301 settled, 0 unsettled, 4/4 independent validity/admissibility, 16.966654s. Awaiting artifact/log/gate/commit.
