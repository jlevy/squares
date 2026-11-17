# Review Programs and Receipts: Yim’s vitamoon Certificates, 9 November 2026

The programs, frozen digests and receipts of the stage 4 mathematical review
[review-2026-11-09-yim-vitamoon.md](../../../../../../docs/project/reviews/review-2026-11-09-yim-vitamoon.md)
(lane L70, bead `think-i5a5`). It reviews fifteen rational certificates by Kaelan Yim in
[vitamoon/vitamoon](https://github.com/vitamoon/vitamoon): `n130.cert`, `n299.cert` and
`n303.cert` at `ac14112`, the first `n303.cert` at `78eb9ea`, and the eleven
beyond-horizon certificates at 553 to 700 committed at `78eb9ea` and unchanged at
`ac14112`. The certificates themselves are the import packet’s; nothing of the source is
copied here.

## Layout

- `programs/`: every program this review ran, with the two frozen plans.
  - The checker, frozen at 2026-11-09T14:05:49Z: `l70_reader.py` (strict readers,
    integers out), `l70_sat.py` (method A, separating axes in `fractions.Fraction`),
    `l70_clip.py` (method B, exact clipped areas in `gmpy2.mpq`), `l70_check.py` (both
    methods over every square, wall and pair) and `l70_selftest.py`.
  - The controls: `controls-plan.json`, frozen at 2026-11-09T14:21:32Z before
    `l70_controls.py` existed, and `controls-plan-addendum.json`, frozen before
    `l70_controls_addendum.py` ran.
  - The measurements, which decide nothing: `l70_sides.py`, `l70_contract.py` (the
    contraction margins of RV-3), `l70_identity.py`, `l70_relative303.py`,
    `l70_construct.py`, `l70_custody.py`, and `l70_digests.py`, which holds every receipt
    to its programs.
  - After the findings were frozen: `l70_compare_lane.py`, which holds the import lane’s
    receipts (copied from `claude/bold-ritchie-xo28us-l65` at `66555e138a54` by
    `git show`, and not kept here, since the packet keeps them) to this review’s.
- `frozen/`: the checker’s and the plans’ digests with their times, and the findings as
  frozen at 2026-11-09T15:17:46Z, before the import lane’s work was read
  (`review-2026-11-09-yim-vitamoon.frozen.md`, SHA-256 `167e3bcc…` in
  `findings-frozen-digest.txt`).
- `out/`: the receipts. Each records the SHA-256 of the programs that wrote it.
- `plumbing/`: the read-only `git ls-tree` and `git log` outputs custody reads.

## Rerunning

From a checkout of `ef1af4933` (the predecessors’ retained files) with the project
interpreter (CPython 3.14.7), and the two trees of vitamoon/vitamoon extracted as data
under `SRC/ac14112/` and `SRC/78eb9ea/` (`git archive` of each commit):

```bash
PY="packing/.venv/bin/python3 -I -B"   # never the python3 on PATH
R=packing/resources/web/yim-certificates-2026-11-09/review/review-2026-11-09
$PY $R/programs/l70_selftest.py --out $R/out/selftest.json
$PY $R/programs/l70_run_checks.py --src SRC --repo . --out $R/out --workers 2
$PY $R/programs/l70_run_controls.py --src SRC --plan $R/programs/controls-plan.json --checks $R/out --out $R/out
$PY $R/programs/l70_contract.py --src SRC --repo . --out $R/out/contract.json
$PY $R/programs/l70_digests.py --root $R
```

The other measurements take the same `--src`, `--repo` and `--checks $R/out` arguments
their docstrings give; `programs/run_measures.sh` and `programs/run_addendum.sh` are the
exact invocations used.

The programs run nothing of the source’s, read the certificates as untrusted data, and
import nothing from this repository.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
