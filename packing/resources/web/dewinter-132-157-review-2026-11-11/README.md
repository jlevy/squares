# Stage 4 Review of de Winter’s 132 and 157: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L105’s blind stage 4 review of
Joost de Winter’s packings at 132 and 157, folders `n132/` and `n157/` of
[JoostdeWinter/square-packing@6617869](https://github.com/JoostdeWinter/square-packing/tree/6617869a3491b5872c6ecdff55db05cbee57d516),
reported in issue [#958](https://github.com/jlevy/squares/issues/958):
[`docs/project/reviews/review-2026-11-11-dewinter-132-157.md`](../../../../docs/project/reviews/review-2026-11-11-dewinter-132-157.md).

The source files are not retained here: the import lane retains them in its own packet.
This directory is review-only and sits beside that packet so that the two lanes write
disjoint paths.

## Layout

- `programs/`: the review’s programs, the controls plan, the issue as fetched, and the
  run scripts.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digests at their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L105’s own, imports nothing from this repository or the source,
and was run with CPython 3.14.7 as `python -I -B` from `packing/` of a checkout of
`main`, through `uv run --frozen --all-extras --group dev`, under `nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l105_reader.py` | the reading: layouts, count, ids, canonical scalars, and whether the JSON and the YAML hold the same packing | `nNNN_exact.json`, `nNNN_witness.yaml` | nothing (a module) |
| `l105_sat.py` | method A: unit squares, wall clearances and pair margins by separating axes in `fractions.Fraction` | integers from the reader | nothing (a module) |
| `l105_clip.py` | method B: unit squares, walls and pairs by exact clipping in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l105_check.py` | both files of one folder, by both methods, every square, wall and pair | the folder | `out/check-nNNN.json` |
| `l105_geom.py` | nothing: builds modified squares, closing moves and wall moves | integers | nothing (a module) |
| `l105_selftest.py` | both methods and the reader against 2,213 cases; with `--mutant A0` or `--mutant Bopen`, a broken method that must fail | nothing | `out/selftest.json`, `out/selftest-mutant-*.json` |
| `l105_plan.py` | nothing: the exact facts of the unmodified files and the 16 controls per count with their stated outcomes | both folders’ JSON | `out/plan-facts-nNNN.json`, `programs/controls-plan.json` |
| `l105_controls.py` | the 16 controls of one count, by both methods or the reader, held to the plan | the folder, the plan, the plan facts | `out/controls-nNNN.json` |

`programs/issue-958.json` is issue #958 as fetched through the GitHub API at 21:15Z.
`run_frozen.sh SOURCE_DIR OUT_DIR` reruns the self-test, the checks and the controls;
SOURCE_DIR is a checkout of the source at `6617869`, holding `n132/` and `n157/`.

Written and run after the findings were frozen, none of them a decider of either
packing:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l105_sides.py` | the claims’ arithmetic: the 12-place ceilings, the issue’s and READMEs’ prints, the record values, the gains, the seed’s comparison at 109 | the source, `programs/issue-958.json`, the case records at 109, 132 and 157 | `out/sides.json` |
| `l105_construct.py` | tilt counts and angles, the near pairs’ opening, the wall squares, corner incidences | the source | `out/construct.json` |
| `l105_lineage.py` | the two growth steps from the seed at 109, in binary64 with SciPy’s assignment | the seed’s `best_fit_101_500.csv`, the source | `out/lineage.json` |
| `l105_identity.py` | the 132 packing against the house witness, eight symmetries and five anchorings | the source, `packing/witnesses/known-best/n-132.yaml` | `out/identity-n132.json` |
| `l105_custody.py` | read-only Git plumbing on both clones; the licence against this repository’s retained copies; no e-mail addresses | both clones, this repository | `out/custody.json` |
| `l105_digests.py` | every program and receipt against the kept bytes and the three frozen lists | this directory | `out/program-digests.json` |

`run_after.sh SOURCE_DIR SEED_DIR REPO_DIR OUT_DIR` reruns them; SEED_DIR is a clone of
`Samanyu-dev/squares_in_squares` at `53551d77513a`. `l105_digests.py` printed
`ALL_RECEIPTS_MATCH`.

## What They Printed

- `l105_selftest.py`: `PASSED 2213 cases, 0 failed, 0 errors`; the two mutants
  `FAILED`.
- `l105_check.py`: `ACCEPT` at 132 (8,646 pairs, 20 wall contacts) and at 157 (12,246
  pairs, one wall contact), the JSON and the YAML the same packing.
- `l105_controls.py`: `EVERY_CONTROL_AS_STATED` at both counts.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the six checker files and `run_frozen.sh` | 2026-11-11T21:07:25Z |
| `frozen/controls-plan-digest.txt` | the plan, its facts, its program and the check receipts, before `l105_controls.py` existed | 2026-11-11T21:10:39Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text, every program and every receipt at the freeze | 2026-11-11T21:19:41Z |
| `frozen/review-2026-11-11-dewinter-132-157.frozen.md` | the review as frozen, before anything of the import lane, the author’s checker or the record at 132 and 157 was read | 2026-11-11T21:19:41Z |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
