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

Written and run after the findings were frozen, none of them a decider of the
certificate:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l109_sides.py` | the claim’s arithmetic: the side’s prints, the record’s sides at 237 (T-190, the house, and T-189), the gain, the context values, the author’s printed outputs | the certificate, `programs/issue-960.json`, `n-237.md`, `results.yaml`, the house witness, the author’s two printed outputs | `out/sides.json` |
| `l109_pose.py` | the certificate against its decimal pose at 60 digits | the pose, the certificate, the check receipt | `out/pose-n237.json` |
| `l109_identity.py` | the certificate against the house, under eight symmetries, five anchorings and two assignment costs | the certificate, the house witness | `out/identity-n237.json` |
| `l109_band.py` | the tilted bands at 237 and 70, and the stated seed against the new band | the certificate, the house, the 70 witness | `out/band-n237.json` |
| `l109_custody.py` | read-only Git plumbing on the clone and this repository | the clone, this repository, the issue as fetched | `out/custody.json` |
| `l109_digests.py` | every program and receipt against the kept bytes and the frozen digests | this directory | `out/program-digests.json` |

Two repository tools at `c8448724e` were run read-only, without `--out`, their printed
output redirected to a receipt:

| Tool | Receipt |
| --- | --- |
| `python -m devtools.contraction_margin --n 237 'T-190=witness-center-basis:witnesses/known-best/n-237.yaml' --against 'issue-960=witness-corners:SOURCE/n-237-candidate.yaml'` | `out/contraction-margin-t190.json` |
| the same with `'T-189=evand-cert:resources/web/couzo-certificates-2026-10-14/source/submissions/2026-10-14/certificates/n237.cert'` | `out/contraction-margin-t189.json` |
| `python -m devtools.measure_identity --n 237` of the certificate against T-190 and T-189 | `out/measure-identity-n237.json` |

`run_after.sh SOURCE_DIR OUT_DIR` reruns all of them.

## What They Printed

- `l109_selftest.py`: `PASSED 2838 cases, 0 failed`, with 55 and 109 failures from the
  two broken copies.
- `l109_check.py`: `ACCEPT`, 27,966 pairs apart by both methods, wall contacts square 67
  bottom, 152 left and 236 top.
- `l109_controls.py`: `EVERY_CONTROL_AS_STATED`.
- `devtools.contraction_margin`: T-190’s margin $1.59 \times 10^{-19}$ and T-189’s
  $2.39 \times 10^{-11}$, each with `within_margin: false` against the new side.
- `l109_digests.py`: `ALL_RECEIPTS_MATCH`.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the six checker files | 2026-11-11T22:05:18Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts, the check and self-test receipts, and the plan’s programs, before `l109_controls.py` existed | 2026-11-11T22:07:16Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and every program and receipt at the freeze | 2026-11-11T22:12:51Z |
| `frozen/review-2026-11-11-ozden-960.frozen.md` | the review as frozen, before anything of an import lane, the author’s checker or its outputs was read | 2026-11-11T22:12:51Z, pushed as `61e6c3aa9` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
