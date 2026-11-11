# Stage 4 Review Programs and Receipts: #943, #944, #945 and #947

The programs, frozen files and receipts of the stage 4 mathematical review
[review-2026-11-11-ozden-943-947.md](../../../../../../docs/project/reviews/review-2026-11-11-ozden-943-947.md)
(lane L83, bead `think-x8oc`), which decides Doğa Özden’s certificates at 156, 180, 268
and 269 with a clean-room exact checker.
Everything here was written for the review; none of it imports this repository’s code or
the author’s.

## Layout

| Path | What |
| --- | --- |
| `programs/` | the 18 Python programs and modules, the five run scripts, `controls-plan.json` and `issue-statements.json` |
| `frozen/checker-frozen-digests.txt` | the six checker files’ SHA-256, frozen at 2026-11-11T06:36:12Z before any producer code or this repository’s witness, verifier or promotion code was read |
| `frozen/controls-plan-digest.txt` | the plan, its two writers and its four facts receipts, frozen at 06:39:19Z before `l83_controls.py` existed |
| `frozen/review-2026-11-11-ozden-943-947.frozen.md` | the review text as frozen before the import lane’s work was read |
| `out/` | the receipts shared by all four counts (`selftest.json`, `sides.json`, `shares.json`, `custody.json`, `program-digests.json`) and the 156 receipts |

The 180, 268 and 269 receipts are in the `review/review-2026-11-11/out/` directories of
`ozden-s180-upper-bound-2026-11-10`, `ozden-s268-upper-bound-2026-11-10` and
`ozden-s269-upper-bound-2026-11-11`. Per count there are `check-nNNN.json`,
`plan-facts-nNNN.json`, `controls-nNNN.json`, `houses-nNNN.json`, `identity-nNNN.json`
and `construct-nNNN.json`.

## The Checker

- `l83_reader.py` composes the YAML with PyYAML, turns every scalar into an exact
  integer pair, fails closed on any layout it does not expect, and requires the JSON
  twin to hold the same tree.
- `l83_sat.py` is method A, separating axes in `fractions.Fraction`.
- `l83_clip.py` is method B, exact clipped areas in `gmpy2.mpq`.
- `l83_check.py` decides every square, wall and pair by both, with no distance filter.
- `l83_geom.py` holds the exact constructions, including the centre-line closing.
- `l83_selftest.py` holds the methods and the reader to 92 cases.

## Rerunning

From a checkout of `main` at `f54ad1048`, with the four repositories cloned at their
pins into `SRC/s156`, `SRC/s180`, `SRC/s268` and `SRC/s269`, and the four
`plan-facts-nNNN.json` receipts in `OUT`:

```bash
bash programs/run_all.sh SRC REPO_ROOT OUT
packing/.venv/bin/python3 -I -B programs/l83_digests.py RUN_DIR OUT/program-digests.json
```

`run_all.sh` runs every program once with `python -I -B` under `nice -n 19`, at most two
processes, in about five minutes and eight CPU-minutes.
`l83_digests.py` expects `programs/`, `frozen/` and the receipts under `out*/` in one
directory, as the review’s run had them; the receipts here are byte-identical copies of
that run’s.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
