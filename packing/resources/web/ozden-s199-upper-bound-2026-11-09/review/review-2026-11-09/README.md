# Stage 4 Review of #938: Programs and Receipts

The programs, frozen files and receipts of the stage 4 mathematical review of issue
[#938](https://github.com/jlevy/squares/issues/938), Doğa Özden’s
$s(199) \le 14.614689853287$. The review is
[review-2026-11-09-ozden-938.md](../../../../../../docs/project/reviews/review-2026-11-09-ozden-938.md);
bead `think-ntcf`, lane L77.

The certificate reviewed is `n-199-candidate.yaml` of
[kenaznia-doga/s199-upper-bound@d03ee0b](https://github.com/kenaznia-doga/s199-upper-bound/tree/d03ee0bdb223e00fe124e818ed242f6cbd714fad),
SHA-256 `8a85b4c3536757a77fd51e2a0e361de1ecef36b38d59ed3111611672e6a78aca`. This
directory does not retain it; the import packet that holds this directory does.

## Programs

All run with CPython 3.14.7 as `python -I -B`, importing nothing from this repository or
from the source under review.
They read the source as data and run none of its code.

| Program | Does | Receipt |
| --- | --- | --- |
| `l77_checker.py` | the clean-room checker: strict reader, method A (separating axes in `Fraction`), method B (clipped areas in `gmpy2.mpq`) | (module) |
| `l77_selftest.py` | 138 stated cases for both methods and the reader | `out/selftest.json` |
| `l77_mutants.py` | the self-test against seven mutated checkers, each of which must fail | `out/mutants.json` |
| `l77_check.py` | decides a witness and its JSON twin by both methods | `out/check-n199.json` |
| `l77_construct.py` | squares 1–172 against T-282, the side, the L, every old–grid gap | `out/construct-n199.json` |
| `l77_plan_facts.py` | the exact facts the controls plan states outcomes from | `out/plan-facts-n199.json` |
| `l77_controls.py` | the 23 controls of `controls-plan.json` | `out/controls-n199.json` |
| `l77_sides.py` | the side, the claim, the gap and every print | `out/sides.json` |
| `l77_propagate.py` | the L step over every case record on `main`, and the closure | `out/propagate.json` |
| `l77_custody.py` | commits, trees, blobs, digests and licences | `out/custody.json` |
| `l77_pose.py` | the decimal pose against #935’s pose and the certificate | `out/pose.json` |
| `l77_identity.py` | the packing against the 199 house, pose by pose | `out/identity-n199.json` |
| `l77_digests.py` | holds every receipt to the kept programs and frozen digests | `out/program-digests.json` |
| `l77_compare_lane.py` | after the freeze: lane L76’s receipts against these, and its tilt-sign split | `out/compare-lane.json` |

`run_all.sh` reruns them all; its header names its four arguments.

## Frozen Files

- `frozen/checker-frozen-digests.txt`: the four checker files, frozen at
  2026-11-09T21:05:54Z, before any producer code or this repository’s witness, verifier
  or promotion code was read.
- `frozen/controls-plan-digest.txt`: `controls-plan.json`, stated at
  2026-11-09T21:20:11Z before `l77_controls.py` existed.
- `frozen/review-2026-11-09-ozden-938.frozen.md`: the review as frozen at
  2026-11-09T21:38:04Z, before the import lane’s work was read; its digest is in
  `frozen/findings-frozen-digest.txt` (`7c5decb8…`).

`run_all.sh` does not run `l77_compare_lane.py`, whose input was the import lane’s
uncommitted working tree; it ran once, after the freeze.

`issue-statements.json` transcribes every number the issue, its comment, the README and
the printed outputs state, for `l77_sides.py` to check.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
