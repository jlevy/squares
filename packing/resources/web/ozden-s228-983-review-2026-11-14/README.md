# Stage 4 Review of #983: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L159’s blind stage 4 review of
issue [#983](https://github.com/jlevy/squares/issues/983), Doğa Özden’s
$s(228) \le 15.600801734812$:
[`docs/project/reviews/review-2026-11-14-ozden-983.md`](../../../../docs/project/reviews/review-2026-11-14-ozden-983.md).

The source is `n-228-candidate.yaml` of
[kenaznia-doga/s228-upper-bound@8bebf3f](https://github.com/kenaznia-doga/s228-upper-bound/tree/8bebf3f78ef50baa0b47341a836b5e45717c49cc),
SHA-256 `4dc2075f5fb06bb7a1ca68aabd8eebd0d326c16c5f408151876a165d2246b747`. It is not
retained here; an import lane would retain it in its own packet.
This directory is review-only.

## Layout

- `programs/`: the review’s programs, the controls plan, the issue and its timeline as
  fetched.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L159’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review.
The review of #967 (lane L127) was the model; its text, README and frozen digest lists
were read, and its programs, plan and receipts were not opened.
Each was run with CPython 3.14.7 as `python -I -B` from `packing/` of a checkout of
`main` at `fa980f8e7`, through `uv run --frozen --all-extras --group dev`, under
`nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l159_reader.py` | the reading: layout, count, ids, canonical scalars, the JSON twin | the certificate and its twin | nothing (a module) |
| `l159_sat.py` | method A: unit squares, wall clearances and pair margins by separating axes in Python integers over per-square denominators | integers from the reader | nothing (a module) |
| `l159_clip.py` | method B: unit squares (sides and diagonals), pairs and walls by exact Sutherland–Hodgman clipping, containment by area, in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l159_check.py` | the certificate, by both methods, every square, wall and pair | the certificate and its twin | `out/check-n228.json` |
| `l159_geom.py` | nothing: builds squares, the closed-form margin from centres and half-widths, closing times, exact decimal prints | fractions | nothing (a module) |
| `l159_selftest.py` | both methods and the reader against 32,833 cases, and two broken copies | nothing | `out/selftest.json` |
| `l159_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | the certificate, the check receipt, the issue | `out/plan-facts-n228.json` |
| `l159_make_plan.py` | nothing: states the 20 controls and their outcomes | the check receipt, the plan facts | `programs/controls-plan.json` |
| `l159_controls.py` | the 20 controls, by both methods or the reader | the certificate, the plan, the plan facts, the check receipt | `out/controls-n228.json` |
| `l159_describe.py` | nothing: the side’s decimals, the margin and clearance distributions, the tilts | the certificate, the check receipt | `out/describe-n228.json` |

`programs/issue-983.json` is the issue as fetched at 19:04Z, trimmed to its text, dates
and labels.

From `packing/`, with `SRC` the clone at the pin and `R` this directory:

```bash
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
Y="$SRC/n-228-candidate.yaml $SRC/n228-witness.json"
$PY $R/programs/l159_selftest.py $R/out/selftest.json
$PY $R/programs/l159_check.py $Y $R/out/check-n228.json
$PY $R/programs/l159_plan_facts.py $Y $R/out/check-n228.json $R/programs/issue-983.json \
  $R/out/plan-facts-n228.json
$PY $R/programs/l159_make_plan.py $R/out/check-n228.json $R/out/plan-facts-n228.json \
  $R/programs/controls-plan.json
$PY $R/programs/l159_controls.py $Y $R/programs/controls-plan.json $R/out/plan-facts-n228.json \
  $R/out/check-n228.json $R/out/controls-n228.json
$PY $R/programs/l159_describe.py $Y $R/out/check-n228.json $R/out/describe-n228.json
```

Written and run after the findings were frozen, none of them a decider of the
certificate:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l159_sides.py` | the claim’s arithmetic: the side’s prints, the gain on T-174 and T-128, the side-only and Kaggle values, the decimal pose’s and the search sides, the promotion and interval reports, the contractions | the certificate, `n-228.md`, the house witness, T-128’s certificate, the decimal pose, the search record, two of the author’s `checks/` reports, the issue, both contraction receipts | `out/sides.json` |
| `l159_pose.py` | the certificate against its decimal pose at 60 digits, the pose’s own margins, every near pair’s relative gap, the search record against the pose | the certificate, the decimal pose, `hit-n228-114-0.txt`, the check receipt | `out/pose-n228.json` |
| `l159_lineage.py` | the issue’s lineage counts against T-174, and the same measures against T-128, T-098, T-092 and T-056, under eight symmetries, five anchorings and two assignments | the certificate, the five registered packings at 228 | `out/lineage-n228.json` |
| `l159_closedform.py` | the side against $s(m) + k$ for every registry value below 228 and $k \le 16$ | the certificate, `packing/frontier/n-NNN.md` | `out/closedform-n228.json` |
| `l159_custody.py` | read-only Git plumbing on the clone and this repository, and the issue’s times | the clone, this repository, `programs/issue-983.json`, `programs/issue-983-timeline.json`, `programs/issue-983-context.json` | `out/custody.json` |
| `l159_digests.py` | every frozen digest against the kept bytes, the digest of every file here, and a rerun of the frozen chain against the kept receipts | this directory, the rerun directory | `out/program-digests.json` |

`programs/issue-983-timeline.json` is the issue’s REST timeline as fetched at 19:27Z,
trimmed; its two `referenced` events are this review’s own pushed commits.
`programs/issue-983-context.json` holds the four issues the filing says it checked, as
fetched; the head of `evand/square-packing` was not fetched, because the GitHub API call
and a `git ls-remote` of it were both refused in this session.

Two of this repository’s devtools were run read-only, writing only here, with
`python -B` from `packing/`: `devtools.contraction_margin` (`out/contraction-t174.json`,
the house T-174 against the certificate; `out/contraction-new.json`, the certificate
itself) and `devtools.measure_identity` (`out/identity-n228.json`, against T-174, T-128
and T-098).

From `packing/` of a checkout of `main` at `fa980f8e7`:

```bash
DT="nice -n 19 uv run --frozen --all-extras --group dev python -B -m"
CERT="#983=witness-corners:$SRC/n-228-candidate.yaml"
COUZO=resources/web/couzo-exact-refinements-2026-10-08/source/certificates/n228.cert.gz
EVAND=resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-228.cert
$DT devtools.contraction_margin --n 228 "T-174=witness-center-basis:witnesses/known-best/n-228.yaml" \
  --against "$CERT" --out $R/out/contraction-t174.json
$DT devtools.contraction_margin --n 228 "$CERT" --out $R/out/contraction-new.json
$DT devtools.measure_identity --n 228 "$CERT" \
  "T-174=witness-center-basis:witnesses/known-best/n-228.yaml" \
  "T-128=evand-cert:$COUZO" "T-098=evand-cert:$EVAND" --out $R/out/identity-n228.json
$PY $R/programs/l159_sides.py $Y frontier/n-228.md witnesses/known-best/n-228.yaml $COUZO \
  $SRC/n-228-decimal-pose.yaml $SRC/hit-n228-114-0.json $SRC/checks/promote.json \
  $SRC/checks/interval.json $R/programs/issue-983.json $R/out/contraction-new.json \
  $R/out/contraction-t174.json $R/out/sides.json
$PY $R/programs/l159_pose.py $Y $SRC/n-228-decimal-pose.yaml $SRC/hit-n228-114-0.txt \
  $R/out/pose-n228.json
$PY $R/programs/l159_lineage.py $Y $R/out/lineage-n228.json \
  "T-174=witness-center-basis:witnesses/known-best/n-228.yaml" "T-128=evand-cert:$COUZO" \
  "T-098=evand-cert:$EVAND" \
  "T-092=witness-center-angle:resources/web/franciscouzo-square-packing-2026-10-03/facts/n-228.yaml" \
  "T-056=witness-center-angle:resources/web/franciscouzo-square-packing-2026-09-27/facts/n-228.yaml"
$PY $R/programs/l159_closedform.py $Y frontier $R/out/closedform-n228.json
$PY $R/programs/l159_custody.py $SRC .. 8bebf3f78ef50baa0b47341a836b5e45717c49cc \
  $R/programs/issue-983.json $R/programs/issue-983-timeline.json \
  $R/programs/issue-983-context.json $R/out/custody.json
$PY $R/programs/l159_digests.py $R $R/out/program-digests.json $RERUN
```

`$RERUN` is a scratch directory into which the frozen chain above was run again.

## What They Printed

- `l159_selftest.py`: `PASSED 32833 cases 0 failed`; broken method A fails 913, broken
  method B 2,135.
- `l159_check.py`: `ACCEPT`, 25,878 pairs apart by both methods, three wall contacts
  (square 63 left, 167 bottom, 213 top), least gap exactly $101/500000000000000$ at
  (118, 119) and six more pairs.
- `l159_controls.py`: `EVERY_CONTROL_AS_STATED`, 20 of 20.
- `devtools.contraction_margin`: T-174 has no contraction margin, $\lambda^* = 1$, since
  its squares 201 and 227 already touch; the gain, $3.7997 \times 10^{-3}$, is not
  within it. The certificate itself first touches at
  $1 - \lambda^* = 101/500000000000101$ (118, 119), a side margin of
  $2.949 \times 10^{-12}$, and both maintained routes accept it as given.
- `devtools.measure_identity`: no symmetry pairs the certificate one to one with T-174,
  T-128 or T-098 by nearest centres.
- `l159_lineage.py`: the issue’s counts (228, 93, 0.940, 59) under T-174 transposed in
  the new box, anchored at the lower-left corner, under either assignment.
- `l159_closedform.py`: no $s(m) + k$ within $10^{-9}$; the nearest, $s(37) + 9$, at
  $2.18 \times 10^{-3}$.
- `l159_digests.py`: `ALL_FROZEN_DIGESTS_HOLD`, and the rerun reproduces every receipt.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the six checker files and the receipts they had written; pushed as `e17f9fa9e` | 2026-11-14T19:12:07Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l159_controls.py` existed; pushed as `a9e3fa610` | 2026-11-14T19:15:44Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | 2026-11-14T19:22:58Z |
| `frozen/review-2026-11-14-ozden-983.frozen.md` | the review as frozen, before the author’s checkers, outputs or README, or this repository’s verifier, were read; pushed as `c2ed4e00c` | 2026-11-14T19:22:58Z |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
