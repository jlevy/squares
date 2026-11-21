# Blind Stage 4 Review R1 of jlevy/squares#1041 and #1042: Programs and Receipts

Lane rR1-lower of the intake pass of 20 November 2026 (bead `think-dhjz`). This packet
holds the programs a blind stage 4 mathematical review wrote for the method behind Joost
de Winter’s 77 standalone lower-bound certificates (after Hiroaki Hosono): the 34 of
issue #1041 (folders `proof/nNNN/`) and the 43 of issue #1042 (folders
`followup/lower/nNNN/`) of
[JoostdeWinter/square-packing `21d944c4`](https://github.com/JoostdeWinter/square-packing/tree/21d944c43098e2261ab7d713cd10f02a5eb13f3d/lower_bounds_2026_11_19),
folder `lower_bounds_2026_11_19/`; the review plan, the controls plan, the frozen
digest lists and the receipts. The review itself is
`docs/project/reviews/review-2026-11-20-de-winter-lower-r1-octagon.md`.

The source is read as data. None of the source’s programs ran, and none of them
(`proof/gram.cpp`, `proof/octagon.cpp`, `proof/check.py`, `proof/bm.py` and the rest) was
opened before the findings were frozen.

## Programs

Every program is this lane’s own, imports nothing from this repository or the source, and
runs under the project interpreter (CPython 3.14.7) as `python -I`. The C core builds with
the host’s gcc (13.3.0) as `gcc -O2 -std=gnu11 rr1_decide.c -lm`, which the drivers run
themselves.

| Program | Reads | Decides |
| --- | --- | --- |
| `rr1_common.py` | (a module) the strict reader, the eight-image expansion, the bins, the exact bin polygon, exact captures of true unit squares, the lattice data | nothing by itself |
| `rr1_decide.c` | the lattice data written by the drivers | each bin’s branch and bound in exact integer arithmetic (mode `decide`); float modes `fsearch` and `fcap` decide nothing |
| `rr1_decide.py` | one certificate | each requested bin completely, or a refusal with an exact witness |
| `rr1_premises.py` | all 77 certificates, `lower_bounds.csv`, `followup/best_by_count.csv` | the exact premises, and the premise controls P1 to P5 |
| `rr1_search.py` | all 77 certificates | nothing unless it finds a capture below 1: a float search with exact end points |
| `rr1_runs.py` | the certificates and the search’s output | the planned runs: `tier1`, `controls`, `sample` |
| `rr1_selftest.py` | synthetic data only | nothing: holds the clip, the polygon, the box bound, the domain and the decider to exact computations, and catches the broken variants T1 to T3 |

`programs/issue-1041.json` and `programs/issue-1042.json` are the issues as the REST API
returned them at 17:53:41Z on 20 November. `programs/controls-plan.json` states every
control, its expected outcome, and the run plan with its CPU rule.

## Freeze Protocol

1. The review plan (`frozen/review-plan.md`) was committed and pushed with its SHA-256 in
   `frozen/plan-frozen-digests.txt` before this lane wrote any checker.
2. The programs and the controls plan were committed and pushed, with their SHA-256 in
   `frozen/checker-frozen-digests.txt`, before any program of this lane read a
   certificate. Before that they ran only on synthetic data.
3. Then they ran, in the order of the plan; one amendment after the checker freeze is
   recorded in `frozen/checker-amendments.txt`.
4. The findings were frozen in `frozen/findings-frozen-digests.txt` before any program of
   the source was opened.

Verify a freeze from this directory:

```bash
cd packing/resources/web/de-winter-lower-r1-review-2026-11-20
sha256sum -c frozen/plan-frozen-digests.txt
sha256sum -c frozen/checker-frozen-digests.txt  # rr1_common.py differs by the amendment
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
