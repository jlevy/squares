# Stage 4 Review of #984 and #985: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L163’s blind stage 4 review of
issues [#984](https://github.com/jlevy/squares/issues/984) and
[#985](https://github.com/jlevy/squares/issues/985), Roberto Ono’s
$s(228) \le 15.596043120921$ and $s(147) \le 12.651043556588$:
[`docs/project/reviews/review-2026-11-14-ono-984-985.md`](../../../../docs/project/reviews/review-2026-11-14-ono-984-985.md).

The sources are files of
[RobertoOno/squares-in-square](https://github.com/RobertoOno/squares-in-square) at
`fce076f2bf459a25be3645d899e8950b93ed977c`, under `runs/2026-11-11_fable-5.2/`, not
retained here; an import lane would retain them in its own packet.
This directory is review-only.

| File | SHA-256 |
| --- | --- |
| `certificates/n228_S59604312.json` | `98987101c5a14e84cc1bdcb7497cc139be6ef71a17f7e7ec9ce3f89c80274944` |
| `evidence/registration/n228.cert` | `be120af6c2fc1e7b6a56deb8a3cee31e2abc4606be98ecfcfebcc889ab51e3f4` |
| `evidence/registration/n228.strict.cert` | `e243de776d011ab24f6221df42bbf6fc55de33c9c7612b92a2008777cff48569` |
| `evidence/registration/n228.strict.json` | `f6f4457cb8d767b70e8b3599ab424033203d3d464f61b7f2a7176fc8fb14e7e7` |
| `certificates/n147_S65104355.json` | `fce8c8c20bf3812173c76c6a2c1295541a72b23a9c948bdf380cc905d2038135` |
| `evidence/registration/n147.cert` | `0e09260712370f6561df1e9c0c835adc04f7d9f49ad40ad0e603c6c6a8cc11af` |
| `evidence/registration/n147.strict.cert` | `cfe0079654a433e4cb2739405f9d523c5557f7182618bc8fb33b656999a7a6ce` |
| `evidence/registration/n147.strict.json` | `f054b39d539cceb6404211ab0c448df15beda2b2c6d6d4293080cc81055bbde1` |

The issues state the digests of the JSON certificates, the `.cert` twins and the
`.strict.cert` files; the `.strict.json` digests are this review’s.

## Layout

- `programs/`: the review’s programs, the controls plan, the issues as fetched.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts; `out/xyd/` and `out/lineage/` hold derived inputs of the
  devtools, compressed with `gzip -n -9` after the runs.

## Programs

Every program is lane L163’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review.
The reviews of #977 and #979 (lane L153) and of #983 (lane L159) were the models; their
texts were read, and their programs were not opened.
Each was run with CPython 3.14.7 as `python -I -B` from `packing/` of a worktree of
`main` at `fa980f8e7`, through `uv run --frozen --all-extras --group dev`, under
`nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l163_reader.py` | the reading: the JSON keys, count and canonical `p/q` scalars; the `.cert` text form | a certificate or its twin | nothing (a module) |
| `l163_sat.py` | method A: unit directions, wall clearances and pair margins by separating axes in Python integers, from centres and half-angles | integers from the reader | nothing (a module) |
| `l163_clip.py` | method B: unit squares (sides and diagonals of the corners), pairs and walls by exact convex clipping, containment by area, in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l163_decide.py` | a certificate by both methods, every square, wall and pair, and their agreement | a reading | nothing (a module) |
| `l163_check.py` | a certificate, its `.cert` twin, and its strict variant with its exact relation to the certificate | the four files of a count | `out/check-nNNN.json` |
| `l163_geom.py` | nothing: the closed form by corner projections in `fractions`, squares with known margins, and closing moves, for the self-test and the plan | fractions | nothing (a module) |
| `l163_selftest.py` | both methods and the reader against 13,326 cases with hand-derived answers, and two broken copies | nothing | `out/selftest.json` |
| `l163_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | a certificate, its check receipt | `out/plan-facts-nNNN.json` |
| `l163_make_plan.py` | nothing: states the controls and their outcomes | the check receipts, the plan facts | `programs/controls-plan.json` |
| `l163_controls.py` | the controls, by both methods or the reader | a certificate, its twin, the plan, its facts, its check receipt | `out/controls-nNNN.json` |
| `l163_describe.py` | nothing: the tilts, the near-pair margins, the near-wall clearances, the extents | a certificate, its check receipt | `out/describe-nNNN.json` |

`programs/issue-984-985.json` is the two issues as fetched at 21:20Z, after the freeze,
trimmed to their text, dates and labels.

From `packing/`, with `S` the clone checked out at `fce076f` and `R` this directory:

```bash
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
D=$S/runs/2026-11-11_fable-5.2
E=$D/evidence/registration
M228=$D/certificates/n228_S59604312.json
M147=$D/certificates/n147_S65104355.json
$PY $R/programs/l163_selftest.py $R/out/selftest.json
$PY $R/programs/l163_check.py n228 $M228 $E/n228.cert $E/n228.strict.cert $E/n228.strict.json $R/out/check-n228.json
$PY $R/programs/l163_check.py n147 $M147 $E/n147.cert $E/n147.strict.cert $E/n147.strict.json $R/out/check-n147.json
$PY $R/programs/l163_plan_facts.py n228 $M228 $R/out/check-n228.json $R/out/plan-facts-n228.json
$PY $R/programs/l163_plan_facts.py n147 $M147 $R/out/check-n147.json $R/out/plan-facts-n147.json
$PY $R/programs/l163_make_plan.py $R/programs/controls-plan.json \
  n228 $R/out/check-n228.json $R/out/plan-facts-n228.json \
  n147 $R/out/check-n147.json $R/out/plan-facts-n147.json
for n in 228 147; do
  eval M=\$M$n
  $PY $R/programs/l163_controls.py n$n $M $E/n$n.cert $R/programs/controls-plan.json \
    $R/out/plan-facts-n$n.json $R/out/check-n$n.json $R/out/controls-n$n.json
  $PY $R/programs/l163_describe.py n$n $M $R/out/check-n$n.json $R/out/describe-n$n.json
done
```

## What They Printed

- `l163_selftest.py`: `PASSED 13326 cases 0 failed`; broken method A fails 815, broken
  method B 1,770.
- `l163_check.py`: `ACCEPT` for each certificate and each strict variant.
  228: 25,878 pairs apart by both methods, least margin $2.38935 \times 10^{-10}$ at (8,
  21), wall contacts 22 left, 31 and 34 bottom, 144 right.
  147: 10,731 pairs, least $3.00262 \times 10^{-10}$ at (101, 108), contacts 3 left, 65
  bottom, 134 top.
- `l163_plan_facts.py`: S4 pairs (9, 21) and (101, 108); 515 and 326 near pairs; 68 and
  56 pairs overlapping with every $t$ negated.
- `l163_controls.py`: `EVERY_CONTROL_AS_STATED`, 20 of 20 for each count.
- `l163_describe.py`: 55 and 44 squares turned beyond 0.5°, 58 and 38 exactly upright;
  each side the packing’s extent in one direction only.

## After the Freeze

Written and run after the findings were frozen, none of them a decider of the
certificates:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l163_convert.py` | nothing: a decimal centre-angle witness as `binary64-xyd` text for `devtools.measure_identity` | the witness | `out/xyd/*.txt`, kept as `.gz` |
| `l163_lineage.py` | each issue’s seed rebuilt exactly from its source, with its overlaps by method A; the 147 house against the 148 house | Couzo’s `n404.cert`, the 229, 147 and 148 house witnesses | `out/lineage-n228-n147.json`, `out/lineage/*.cert`, kept as `.gz` |
| `l163_sides.py` | the claims’ arithmetic: ceilings, gains on T-174, T-300, $7 + 4\sqrt 2$ and T-155, the side-only entries, the issues’ prints | both certificates, `n-228.md`, `n-147.md`, T-300’s certificate, the issues | `out/sides.json` |
| `l163_closedform.py` | each side against $s(m) + k$ for every reported value below it and $k \le 16$, and the L steps from it | both certificates, `packing/frontier/n-NNN.md` | `out/closedform.json` |
| `l163_custody.py` | read-only Git plumbing on the clone, the run’s stated times, `VERIFIER.sha256`, the licence, the issues’ times; no e-mail addresses | the clone, `programs/issue-984-985.json` | `out/custody.json` |
| `l163_digests.py` | every frozen digest against the kept bytes, a rerun of the frozen chain against the kept receipts, and the digest of every file here | this directory, the source run, the rerun | `out/program-digests.json` |

Two of this repository’s devtools were run read-only, writing only here, with
`python -B` from `packing/`. With `S`, `E`, `R` as above, `T` a copy of
`packing/resources/web/ozden-s228-upper-bound-2026-11-14/source/n-228-candidate.yaml`
and `H` of `packing/witnesses/known-best/n-228.yaml`, both from `main` at `473577f42`
(after PR #986 merged), and `X` a scratch directory holding the frozen chain’s receipts
written again:

```bash
DT="nice -n 19 uv run --frozen --all-extras --group dev python -B -m"
N228="#984=evand-cert:$E/n228.cert"
N147="#985=evand-cert:$E/n147.cert"
EV=resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs
T155=cases/regularized_bounds/views/n-147.yaml.gz
$DT devtools.contraction_margin --n 228 "$N228" --out $R/out/contraction-new-n228.json
$DT devtools.contraction_margin --n 147 "$N147" --out $R/out/contraction-new-n147.json
$DT devtools.contraction_margin --n 228 "T-174=witness-center-basis:witnesses/known-best/n-228.yaml" \
  --against "$N228" --out $R/out/contraction-t174.json
$DT devtools.contraction_margin --n 228 "T-300=witness-corners:$T" --against "$N228" \
  --out $R/out/contraction-t300.json
$DT devtools.contraction_margin --n 228 "house-main=witness-center-basis:$H" --against "$N228" \
  --out $R/out/contraction-house-main-n228.json
$DT devtools.contraction_margin --n 147 "T-155=witness-center-basis:$T155" --against "$N147" \
  --out $R/out/contraction-t155.json
$DT devtools.contraction_margin --n 147 "T-101=evand-cert:$EV/n-147.cert" --against "$N147" \
  --out $R/out/contraction-t101.json
$PY $R/programs/l163_convert.py resources/web/franciscouzo-square-packing-2026-10-03/facts/n-228.yaml $R/out/xyd/t092-n228.txt
$PY $R/programs/l163_convert.py resources/web/franciscouzo-square-packing-2026-09-27/facts/n-228.yaml $R/out/xyd/t056-n228.txt
$PY $R/programs/l163_convert.py witnesses/known-best/n-147.yaml $R/out/xyd/house-n147.txt
$DT devtools.measure_identity --n 228 "$N228" "T-174=witness-center-basis:witnesses/known-best/n-228.yaml" \
  "T-300=witness-corners:$T" \
  "T-128=evand-cert:resources/web/couzo-exact-refinements-2026-10-08/source/certificates/n228.cert.gz" \
  "T-098=evand-cert:$EV/n-228.cert" "T-092=binary64-xyd:$R/out/xyd/t092-n228.txt" \
  "T-056=binary64-xyd:$R/out/xyd/t056-n228.txt" --out $R/out/identity-n228.json
$DT devtools.measure_identity --n 147 "$N147" "T-155=witness-center-basis:$T155" \
  "T-101=evand-cert:$EV/n-147.cert" "house-n147=binary64-xyd:$R/out/xyd/house-n147.txt" \
  --out $R/out/identity-n147.json
$DT devtools.measure_identity --n 228 "$N228" "house-main=witness-center-basis:$H" \
  --out $R/out/identity-house-main-n228.json
$PY $R/programs/l163_lineage.py resources/web/couzo-issue763-2026-10-23/source/certificates/best/n404.cert \
  witnesses/known-best/n-229.yaml witnesses/known-best/n-147.yaml witnesses/known-best/n-148.yaml \
  $R/out/lineage $R/out/lineage-n228-n147.json
$DT devtools.measure_identity --n 228 "$N228" \
  "seed-mirror-x=evand-cert:$R/out/lineage/seed-n228-mirror-x-dropped.cert" \
  "seed-mirror-y=evand-cert:$R/out/lineage/seed-n228-mirror-y-dropped.cert" \
  --out $R/out/identity-seed-n228.json
$DT devtools.measure_identity --n 147 "$N147" "seed=evand-cert:$R/out/lineage/seed-n147.cert" \
  --out $R/out/identity-seed-n147.json
$PY $R/programs/l163_sides.py $M228 $M147 frontier/n-228.md frontier/n-147.md $T \
  $R/programs/issue-984-985.json $R/out/sides.json
$PY $R/programs/l163_closedform.py frontier $R/out/closedform.json n228=$M228 n147=$M147
$PY $R/programs/l163_custody.py $S fce076f2bf459a25be3645d899e8950b93ed977c \
  $R/programs/issue-984-985.json $R/out/custody.json
$PY $R/programs/l163_digests.py $R $D $X $R/out/program-digests.json
```

They printed: T-174 and T-155 have contraction margin 0 (squares 201 and 227, and 1 and
2, touch); T-300 has $2.949 \times 10^{-12}$ at (118, 119), its certificate and `main`’s
house witness alike; T-101 has $1.27 \times 10^{-19}$; #984 and #985 contract by
$3.488 \times 10^{-9}$ and $2.934 \times 10^{-9}$; every gain `within_margin: false`. No
symmetry pairs either certificate one to one with any registered packing at its count by
nearest centres. The 147 seed has 147 squares, deepest overlap 0.00978, and pairs one to
one with the certificate; the 228 seed needs the mirror in $x$ and two squares dropped,
and lies 34 squares beyond a tenth from the certificate.
No $s(m) + k$ lies within $10^{-9}$ of either side.
Custody holds, and `l163_digests.py` printed `ALL_FROZEN_DIGESTS_HOLD` and
`RERUN_REPRODUCES_EVERY_RECEIPT`.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the eight source files, the seven checker files and the receipts they had written | 2026-11-14T21:07:22Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l163_controls.py` existed | 2026-11-14T21:10:47Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | 2026-11-14T21:17:04Z |
| `frozen/review-2026-11-14-ono-984-985.frozen.md` | the review as frozen, before the author’s reports, checkers or outputs, or this repository’s verifier, were read | 2026-11-14T21:17:04Z |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
