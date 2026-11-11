# Stage 4 Review of #960: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L109’s blind stage 4 review of
issue [#960](https://github.com/jlevy/squares/issues/960), Doğa Özden’s
$s(237) \le 15.893805580573$:
[`docs/project/reviews/review-2026-11-11-ozden-960.md`](../../../../docs/project/reviews/review-2026-11-11-ozden-960.md).

The source is `n-237-candidate.yaml` of
[kenaznia-doga/s237-upper-bound@13c4b23](https://github.com/kenaznia-doga/s237-upper-bound/tree/13c4b231bb16437a6ee3751e75113ef95113b235),
SHA-256 `80687bdceef5780f907c7f47a181802fbfb76a026d077aa18f7bb3eaa3ec3833`. It is not
retained here: an import lane retains it in its own packet.
This directory is review-only, so that the review and the import write disjoint paths.

## Layout

- `programs/`: the review’s programs, the controls plan, the issue as fetched, and the
  run script.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L109’s own, written for this review, imports nothing from this
repository or the source, and shares no code with lane L101’s review of #954 or any
other review. Each was run with CPython 3.14.7 as `python -I -B` from `packing/` of a
worktree of `main`, through `uv run --frozen --all-extras --group dev`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l109_reader.py` | the reading: layout, count, ids, canonical scalars, the JSON twin | the certificate and its twin | nothing (a module) |
| `l109_axes.py` | method A: unit squares, wall clearances and pair margins by separating axes in `fractions.Fraction` | integers from the reader | nothing (a module) |
| `l109_clip.py` | method B: unit squares, walls and pairs by exact clipping in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l109_check.py` | the certificate, by both methods, every square, wall and pair | the certificate and its twin | `out/check-n237.json` |
| `l109_geom.py` | nothing: builds squares, moves and exact closing times for the self-test and the controls | rationals | nothing (a module) |
| `l109_selftest.py` | both methods and the reader against 2,838 cases, and two broken copies that must fail | nothing | `out/selftest.json` |
| `l109_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | the certificate | `out/plan-facts-n237.json` |
| `l109_make_plan.py` | nothing: states the 17 controls and their outcomes | the check receipt, the plan facts | `programs/controls-plan.json` |
| `l109_controls.py` | the 17 controls, by both methods or the reader | the certificate, the plan, the plan facts | `out/controls-n237.json` |
| `l109_census.py` | nothing: margins and wall clearances by decade | the certificate | `out/census-n237.json` |

`programs/issue-960.json` is the issue as fetched through the GitHub API at
2026-11-11T21:56:43Z.
`run_frozen.sh SOURCE_DIR OUT_DIR` reruns the self-test, the check, the census and the
controls.

## What They Printed

- `l109_selftest.py`: `PASSED 2838 cases, 0 failed`, with 55 and 109 failures from the
  two broken copies.
- `l109_check.py`: `ACCEPT`, 27,966 pairs apart by both methods, wall contacts square 67
  bottom, 152 left and 236 top.
- `l109_controls.py`: `EVERY_CONTROL_AS_STATED`.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the six checker files | 2026-11-11T22:05:18Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts, the check and self-test receipts, and the plan’s programs, before `l109_controls.py` existed | 2026-11-11T22:07:16Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and every program and receipt at the freeze | as it records |
| `frozen/review-2026-11-11-ozden-960.frozen.md` | the review as frozen, before anything of an import lane, the author’s checker or its outputs was read | as above |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
