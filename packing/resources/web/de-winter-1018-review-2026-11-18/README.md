# Blind Stage 4 Review of jlevy/squares#1018: Programs and Receipts

Lane r108-1118 of the intake pass of 17 and 18 November 2026 (bead `think-i5en`, under
the heading “R-108 (blind review)”). This packet holds the programs a blind stage 4
mathematical review wrote for Joost de Winter’s claim
$s(109) \ge s(108) \ge 1700799526134255846599/159999384348528500000$, their controls plan,
the frozen digest lists and the receipts.
The review itself is `docs/project/reviews/review-2026-11-18-de-winter-1018.md`.

The source is read as data at
[JoostdeWinter/square-packing `cc20a268`](https://github.com/JoostdeWinter/square-packing/tree/cc20a26845789c2502950041c26709eda8a71081/lower_n108),
folder `lower_n108/`. None of the source’s programs ran, and its `check_lower.py` and
`stretch_measure.py` were not opened before the findings were frozen. The comparison
measure is T-216’s retained candidate,
`packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/release/certificates/mixed_n108_L1062/candidate.json.gz`.

## Programs

Every program is this lane’s own, imports nothing from this repository or the source, and
runs under the project interpreter (CPython 3.14.7, numpy 2.5.2, gmpy2 2.3.1) as
`python -I`, at `nice -n 19` with `OPENBLAS_NUM_THREADS=1`. The C decider builds with the
host’s gcc (13.3.0) and the flags `rv1018_decide.py` states.

| Program | Reads | Decides |
| --- | --- | --- |
| `rv1018_common.py` | (a module) the strict reader, the D4 expansion, the net, two exact captures (clipping, chords) and a float search capture | nothing by itself |
| `rv1018_custody.py` | every file of `lower_n108/`, this repository’s crate and documents at stated commits (`git show`), T-216’s retained file | nothing: digests and byte identity |
| `rv1018_premises.py` | the rescaled measure; T-216’s file for informational values | the measure’s and the net’s exact premises, and the PDF’s enlargement in exact arithmetic |
| `rv1018_measure.py` | the rescaled measure, T-216’s retained file, the source’s copy of it | whether the measure is T-216’s with every coordinate times 1063/1062 and every mass kept |
| `rv1018_runs.py` | the twelve archived direction-run logs, the rescaled measure | whether the logs cover every direction the argument needs, with the premises recomputed here |
| `rv1018_axis.py` | the rescaled measure; `rv1018_runs.py`’s output | direction 0 completely, by exact events and a rigorous vertex bound |
| `rv1018_poses.py` | the rescaled measure; `rv1018_runs.py`’s output | nothing: exact captures at the source’s 401 logged poses |
| `rv1018_sample.py` | the rescaled measure; the runs and poses outputs | nothing: a seeded search at a fixed sample of directions |
| `rv1018_decide.py` with `rv1018_bnb.c` | the rescaled measure; the sample | each sampled rotated direction completely, by this lane’s own branch and bound |
| `rv1018_selftest.py` | synthetic data only | nothing: holds the evaluators and deciders to each other and to refusals |
| `rv1018_controls.py` | the measure, T-216’s file, the run logs and outputs above | nothing: runs `controls-plan.json` |

`programs/issue-1018.json` is the issue as the REST API returned it at 01:34:16Z on 18
November (body only was read). `programs/controls-plan.json` states every control and its
expected outcome, and the run plan with its pricing rules.

## Freeze Protocol

1. The programs and the controls plan were committed and pushed, with their SHA-256 in
   `frozen/checker-frozen-digests.txt`, before any program of this lane read the
   certificate, T-216’s file or the run logs. Before that freeze they ran only on
   synthetic data.
2. Then they ran, in the order of the plan.
3. The findings were frozen in `frozen/findings-frozen-digests.txt` before the doc-map
   entry, the synopsis map or the pull request.

Verify a freeze from this directory:

```bash
cd packing/resources/web/de-winter-1018-review-2026-11-18
sha256sum -c frozen/checker-frozen-digests.txt
```

## Reproduction

From the repository root, with the source cloned at the pin into `$SRC` (the folder
`lower_n108/`):

```bash
R=packing/resources/web/de-winter-1018-review-2026-11-18
P=$R/programs
PY="packing/.venv/bin/python3 -I"
export OPENBLAS_NUM_THREADS=1
BASE=packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/release/certificates/mixed_n108_L1062/candidate.json.gz
M=$SRC/evidence/n108_measure.json.gz
SHA=d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88
$PY $P/rv1018_selftest.py --scratch "${TMPDIR:-/tmp}" --out $R/out/selftest.json
$PY $P/rv1018_custody.py --source $SRC --repo . --commit 910b6b12c --commit f9ddfeeef \
  --retained-base $BASE --out $R/out/custody.json
$PY $P/rv1018_premises.py --measure $M --base $BASE --out $R/out/premises.json
$PY $P/rv1018_measure.py --base $BASE --new $M --source-copy $SRC/evidence/Hosono_n108.json.gz \
  --out $R/out/measure.json
$PY $P/rv1018_runs.py --runs $SRC/evidence/direction_runs --measure $M --reviewed-source $SHA \
  --out $R/out/runs.json
$PY $P/rv1018_axis.py --measure $M --runs $R/out/runs.json --out $R/out/axis.json
$PY $P/rv1018_axis.py --measure $M --factor 99/100 --out $R/out/axis-99_100.json
$PY $P/rv1018_poses.py --measure $M --runs $R/out/runs.json --out $R/out/poses.json
$PY $P/rv1018_sample.py --measure $M --runs $R/out/runs.json --poses $R/out/poses.json \
  --out $R/out/sample.json
$PY $P/rv1018_decide.py --measure $M --directions-from $R/out/sample.json \
  --scratch "${TMPDIR:-/tmp}" --out $R/out/decide-sample.json
$PY $P/rv1018_controls.py --measure $M --base $BASE --runs $SRC/evidence/direction_runs \
  --runs-out $R/out/runs.json --sample $R/out/sample.json --reviewed-source $SHA \
  --scratch "${TMPDIR:-/tmp}" --out $R/out/controls.json
```

What each printed, its CPU time, and what failed along the way are recorded below once the
runs are done.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
