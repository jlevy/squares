# Stage 4 Review of #954: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L101’s blind stage 4 review of
issue [#954](https://github.com/jlevy/squares/issues/954), Doğa Özden’s
$s(179) \le 13.881367160110$:
[`docs/project/reviews/review-2026-11-11-ozden-954.md`](../../../../docs/project/reviews/review-2026-11-11-ozden-954.md).

The source is `n-179-candidate.yaml` of
[kenaznia-doga/s179-upper-bound@bd262d8](https://github.com/kenaznia-doga/s179-upper-bound/tree/bd262d8ba2966000e827547597fe6da24d0e118c),
SHA-256 `75813e7cc0ee167557678ce6dab287359711c58796afa3048cd10ff2f6a8041b`. It is not
retained here: the import lane retains it in its own packet.
This directory is review-only and sits beside that packet so that the two lanes write
disjoint paths.

## Layout

- `programs/`: the review’s programs, the controls plan, and the run scripts.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L101’s own, imports nothing from this repository or the source,
and was run with CPython 3.14.7 as `python -I -B` from `packing/` of a checkout of
`main`, through `uv run --frozen --all-extras --group dev`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l101_reader.py` | the reading: layout, count, ids, canonical scalars, the JSON twin | the certificate and its twin | nothing (a module) |
| `l101_sat.py` | method A: unit squares, wall clearances and pair margins by separating axes in `fractions.Fraction` | integers from the reader | nothing (a module) |
| `l101_clip.py` | method B: unit squares, walls and pairs by exact clipping in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l101_check.py` | the certificate, by both methods, every square, wall and pair | the certificate and its twin | `out/check-n179.json` |
| `l101_geom.py` | nothing: builds modified squares and closing times for the self-test and the controls | integers | nothing (a module) |
| `l101_selftest.py` | both methods and the reader against 987 cases | nothing | `out/selftest.json` |
| `l101_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | the certificate, the check receipt | `out/plan-facts-n179.json` |
| `l101_make_plan.py` | nothing: states the 17 controls and their outcomes | the check receipt, the plan facts | `programs/controls-plan.json` |
| `l101_controls.py` | the 17 controls, by both methods or the reader | the certificate, the plan, the plan facts | `out/controls-n179.json` |

`run_frozen.sh SOURCE_DIR OUT_DIR` reruns the self-test, the check and the controls.

Written and run after the findings were frozen, none of them a decider of the
certificate:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l101_sides.py` | the claim’s arithmetic: the side’s prints, the house side, the gain, the context values | the certificate, `programs/issue-954.json` (the issue as fetched), the case records at 179, 70 and 207, the house witness, the author’s two printed outputs | `out/sides.json` |
| `l101_house.py` | decides the house witness at 179 with the frozen `l101_check.decide` | `packing/witnesses/known-best/n-179.yaml` | `out/house-n179.json` |
| `l101_pose.py` | the certificate against its decimal pose at 60 digits | the pose, the certificate, the check receipt | `out/pose-n179.json` |
| `l101_identity.py` | the certificate against the house, pose by pose, under eight symmetries and five anchorings | the certificate, the house witness | `out/identity-n179.json` |
| `l101_band.py` | the tilted bands at 179, 70 and 207, and the stated seed against the new band | the certificate, the house, the 70 and 207 witnesses | `out/band-n179.json` |
| `l101_custody.py` | read-only Git plumbing on the clone and this repository | the clone, this repository | `out/custody.json` |
| `l101_digests.py` | every program and receipt against the kept bytes and the frozen digests | this directory | `out/program-digests.json` |

`run_after.sh SOURCE_DIR REPO_DIR OUT_DIR` reruns them.
`l101_digests.py` printed `ALL_RECEIPTS_MATCH`.

## What They Printed

- `l101_selftest.py`: `PASSED 987 cases, 0 failed`.
- `l101_check.py`: `ACCEPT`, 15,931 pairs clear by both methods, wall contacts square 39
  bottom, 117 right and 123 left.
- `l101_controls.py`: `EVERY_CONTROL_AS_STATED`.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the six checker files | 2026-11-11T19:12:23Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l101_controls.py` existed | 2026-11-11T19:14:36Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | 2026-11-11T19:19:43Z |
| `frozen/review-2026-11-11-ozden-954.frozen.md` | the review as frozen, before anything of the import lane or the author’s checkers was read | 2026-11-11T19:19:43Z |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
