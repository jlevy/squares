---
type: is
id: is-01m2hdrejydj446zd13cpxkstz
title: sqpack.verify.verify_packing at float_sign accepts a NaN pose
kind: bug
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-09-15T02:18:56.989Z
updated_at: 2026-09-15T02:18:56.989Z
---
Found while addressing PR #125 review D25 (think-fshc, fixed in 471781af).

`sqpack.verify.verify_packing(squares, side, sign=float_sign(tol))` accepts a pose with a NaN coordinate: every sign test on a NaN returns "touching", so the report is valid. The new test `test_the_ratchet_verifier_admits_a_record_and_refuses_non_finite_poses` in packing/tests/test_divide_and_concur.py pins this as a control (NaN in record(5) pose 2, x) and run_projection_ratchet now guards finiteness before calling the oracle. Other float-oracle callers (sqpack.campaign.runner verify-archive, used by run_arm_sweep and exp-204's guard) have no such guard.

Decide whether verify_packing itself must refuse non-finite corners and side (the soundness fix at the source), then drop the per-caller guards or keep them as belt and braces. A float oracle that certifies NaN is a soundness defect under epistemics.md even if no recorded run has produced one.
