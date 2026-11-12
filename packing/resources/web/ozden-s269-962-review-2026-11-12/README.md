# Stage 4 Review of #962: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L117’s blind stage 4 review of
issue [#962](https://github.com/jlevy/squares/issues/962), Doğa Özden’s
$s(269) \le 16.899469075856$:
[`docs/project/reviews/review-2026-11-12-ozden-962.md`](../../../../docs/project/reviews/review-2026-11-12-ozden-962.md).

The source is `n-269-candidate.yaml` of
[kenaznia-doga/s269-upper-bound-16899469076@fdab2c0](https://github.com/kenaznia-doga/s269-upper-bound-16899469076/tree/fdab2c0073ea91701d0d8429663faa6e5c7f831f),
SHA-256 `54b408b2f1b45fc3d0a1330767c8740f0889eecb73f5fcf7888710526dbcc26b`. It is not
retained here; an import lane would retain it in its own packet. This directory is
review-only.

## Layout

- `programs/`: the review’s programs, the controls plan, the issue as fetched, and the
  run script.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L117’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review. The review of #959 (lane L108) was the model; its text,
README and frozen digest lists were read, and its programs were not opened. Each was run
with CPython 3.14.7 as `python -I -B` from `packing/` of a checkout of `main` at
`2fe557598`, through `uv run --frozen --all-extras --group dev`, under `nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l117_reader.py` | the reading: layout, count, ids, canonical scalars, the JSON twin | the certificate and its twin | nothing (a module) |
| `l117_sat.py` | method A: unit squares, wall clearances and pair margins by separating axes in Python integers over per-square denominators | integers from the reader | nothing (a module) |
| `l117_hull.py` | method B: unit squares (sides and right angles), pairs as the convex hull of vertices and edge crossings, walls by centre and slabs, in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l117_check.py` | the certificate, by both methods, every square, wall and pair | the certificate and its twin | `out/check-n269.json` |
| `l117_geom.py` | nothing: builds squares, the closed-form margin from centres and half-widths, and closing times, for the self-test and the controls | fractions | nothing (a module) |
| `l117_selftest.py` | both methods and the reader against 12,445 cases, and two broken copies | nothing | `out/selftest.json` |
| `l117_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | the certificate, the check receipt | `out/plan-facts-n269.json` |
| `l117_make_plan.py` | nothing: states the 20 controls and their outcomes | the check receipt, the plan facts | `programs/controls-plan.json` |
| `l117_controls.py` | the 20 controls, by both methods or the reader | the certificate, the plan, the plan facts, the check receipt | `out/controls-n269.json` |

`programs/issue-962.json` is the issue and the author’s announcing comment on #947 as
fetched, trimmed to their text and dates.
`run_frozen.sh SOURCE_DIR OUT_DIR` reruns the self-test, the check, the plan facts, the
plan and the controls.

## What They Printed

- `l117_selftest.py`: `PASSED 12445 cases, 0 failed`; broken method A fails 814, broken
  method B 2,078.
- `l117_check.py`: `ACCEPT`, 36,046 pairs apart by both methods, eleven wall contacts
  (square 103 bottom, 155 top, 158 and 160 to 167 left), least gap
  $2.03406594369835 \times 10^{-13}$ at (10, 13).
- `l117_controls.py`: `NOT_EVERY_CONTROL_AS_STATED`, 19 of 20; G2 refused the file as
  stated, and method B read the right wall of a square beyond its slab as apart (F2 of
  the review).

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the six checker files and the receipts they had written | 2026-11-12T00:12:46Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l117_controls.py` existed | 2026-11-12T00:15:04Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | 2026-11-12T00:23:36Z |
| `frozen/review-2026-11-12-ozden-962.frozen.md` | the review as frozen, before the author’s checkers, outputs or README, or this repository’s verifier, were read | 2026-11-12T00:23:36Z |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
