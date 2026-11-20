# Blind Stage 4 Review of jlevy/squares#1031: Programs and Receipts

Lane r1031-1118 of the intake pass of 17 and 18 November 2026 (bead `think-r3tn`). This
packet holds the programs a blind stage 4 mathematical review wrote for Joost de Winter’s
claim $s(299) \le 17.793636991744$, their controls plan, the frozen digest lists and the
receipts. The review itself is `docs/project/reviews/review-2026-11-18-de-winter-1031.md`.

The source is read as data at
[JoostdeWinter/square-packing `497eb478`](https://github.com/JoostdeWinter/square-packing/tree/497eb478b790175ea8690671b66785b70c97f9f2/n299),
folder `n299/`: `n299_exact.json` (form J, a centre and a unit edge direction per square)
and `n299_witness.yaml` (form C, a Witness/v2 corners file). None of the source’s programs
ran, and its `verify_exact.py` and `check_area.py` were not opened before the findings
were frozen. T-325, the house at 299, is read from the import packet of #1009,
`packing/resources/web/mishapolk-issue1009-2026-11-16/source/`.

## Programs

Every program is this lane’s own, imports nothing from this repository or the source, and
runs under the project interpreter (CPython 3.14.7, gmpy2 2.3.1, PyYAML 6.0.3, numpy
2.5.2, scipy 1.17.1) as `python -I -B`, at `nice -n 19`. Each adds its own directory to
`sys.path`, since `-I` does not.

| Program | Reads | Decides |
| --- | --- | --- |
| `rv1031_reader.py` | (a module) forms J, C (corners or center-basis) and P, strictly, into exact rationals | nothing by itself |
| `rv1031_axes.py` | (a module) method A: separating axes on poses, `fractions.Fraction` | pair margins and wall clearances |
| `rv1031_clip.py` | (a module) method B: exact Sutherland–Hodgman clipping on corners, `gmpy2.mpq` | pair classes and areas, wall terms, area inside |
| `rv1031_decide.py` | (a module) whole-packing decisions by both methods and their comparison | nothing by itself |
| `rv1031_check.py` | forms J and C | the certificate, directly and crossed, and the claim |
| `rv1031_contract.py` | any one form, and optionally its twin | the contraction margin, exactly, and verifies it |
| `rv1031_controls.py` | forms J and C, `controls-plan.json` | nothing: runs the controls plan, optionally under a broken copy |
| `rv1031_selftest.py` | synthetic data only | nothing: holds the methods to hand-derived values and to seven broken copies |
| `rv1031_synth.py` | nothing | nothing: writes the synthetic certificates the controls were tried on |
| `rv1031_custody.py` | the two fetched copies, the API listings, the source’s `SHA256SUMS` | nothing: digests and blob ids |
| `rv1031_identity.py` | the certificate and every house at 299 | nothing: identity under the box’s symmetries, binary64 |
| `rv1031_describe.py` | the certificate | nothing: tilts, close and near pairs, clearances |
| `rv1031_lineage.py` | the certificate, the record’s packings at 299, 335 and 372 | nothing: the reflection across $x + y = S$ and a scan for copied bands |
| `rv1031_measures.py` | the certificate, the houses, `out/contraction-t325.json` | nothing: the gains, exactly |
| `rv1031_synthetic.sh` | the synthetic certificates | nothing: reruns the synthetic trials with the frozen programs |
| `rv1031_price.py` | a synthetic packing | nothing: the pricing trial, run in scratch before the freeze |

The first nine were frozen before any of them read a certificate. The next five, and
`rv1031_synthetic.sh`, were written after the checker’s freeze and before the findings’
freeze; they decide nothing. `rv1031_price.py` ran in scratch before the freeze and is
kept as it ran.

`programs/issue-1031.json` is the issue as the REST API returned it at 07:36:09Z on 18
November (the body only was read). `programs/controls-plan.json` states every control and
its outcome as a rule over the certificate’s exact facts, the priors, and the run plan
with its pricing. `out/custody-inputs/` holds the API’s tree listings of `n299/` at the
pin and at the head, the pin’s commit metadata (its file patches removed, unread), the
comparison of the pin with the head, and the source’s `SHA256SUMS` from commit
`3293038d`.

## Freeze Protocol

1. The programs and the controls plan were committed and pushed at 08:02:05Z (commit
   `212876836f`), with their SHA-256 in `frozen/checker-frozen-digests.txt`, before any
   program of this lane read the certificate or any packing of the record. Before that
   freeze they ran only on synthetic data.
2. Then they ran, in the order of the plan, and the five measuring programs were written
   and run.
3. The findings were frozen in `frozen/findings-frozen-digests.txt` with the review as
   frozen, `frozen/review-2026-11-18-de-winter-1031.frozen.md`, before the doc-map entry,
   the synopsis map, the review’s footer or the pull request.

Verify a freeze from this directory:

```bash
cd packing/resources/web/de-winter-1031-review-2026-11-18
sha256sum -c frozen/checker-frozen-digests.txt
sha256sum -c frozen/findings-frozen-digests.txt
```

## Reproduction

From the repository root, with the two certificate files fetched at the pin into `$SRC`
(and a second copy by the git-blob API into `$API`, for custody):

```bash
R=packing/resources/web/de-winter-1031-review-2026-11-18
P=$R/programs
PY="packing/.venv/bin/python3 -I -B"
W=packing/resources/web
T=$W/mishapolk-issue1009-2026-11-16/source
$PY $P/rv1031_selftest.py --out $R/out/selftest.json
$PY $P/rv1031_check.py --json $SRC/n299_exact.json --witness $SRC/n299_witness.yaml \
  --claim 17.793636991744 --out $R/out/check.json
$PY $P/rv1031_controls.py --json $SRC/n299_exact.json --witness $SRC/n299_witness.yaml \
  --claim 17.793636991744 --plan $P/controls-plan.json --out $R/out/controls.json
$PY $P/rv1031_contract.py --kind json --file $SRC/n299_exact.json \
  --twin-kind witness --twin $SRC/n299_witness.yaml --out $R/out/contraction-1031.json
$PY $P/rv1031_contract.py --kind witness --file $T/witnesses/2026-11-16/n-299.yaml \
  --twin-kind cert --twin $T/certificates/0000-0999/n299.cert --out $R/out/contraction-t325.json
$PY $P/rv1031_custody.py --route raw=$SRC --route api=$API --inputs $R/out/custody-inputs \
  --out $R/out/custody.json
$PY $P/rv1031_describe.py --kind json --file $SRC/n299_exact.json --out $R/out/describe-1031.json
```

The controls under a broken copy add `--mutant always-accept` or `--mutant always-refuse`
and write to `out/broken-copies/`. The identity, lineage and gain measures take the houses
as `LABEL=KIND:PATH`; `out/identity.json`, `out/lineage-houses.json` and
`out/measures.json` record every path and digest they read. They read T-101 from
`$W/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-299.cert`,
T-155 from `packing/cases/regularized_bounds/views/n-299.yaml.gz` (decompressed), T-248
and T-258 from the two `evand-n299-*` packets’ `.cert` files, T-263 and T-277 from the two
`ozden-s299-upper-bound-*` packets’ `n-299-candidate.yaml`, T-280 from
`$W/yim-certificates-2026-11-09/source/n299.cert` with its UTF-8 comment line removed (the
frozen reader is ASCII only), T-325 as above and the house witness
`packing/witnesses/known-best/n-299.yaml`; the lineage scan reads the record’s eight
packings at 335 and 372 under `$W/couzo-*` and `$W/mishapolk-issue732-*`. The synthetic
trials are rerun with `bash programs/rv1031_synthetic.sh PYTHON` from this directory.

## What Each Program Printed

| Program | Printed | CPU (s) |
| --- | --- | ---: |
| `rv1031_selftest.py` | `PASSED 14785 0`, and each broken copy’s failures: 831, 1,076, 1,013, 1,009, 1,084, 3 and 1 | 12.8 |
| `rv1031_check.py` | `ACCEPT []` | 25.1 |
| `rv1031_controls.py` | `CONTROLS_NOT_AS_STATED ['S1d', 'E1p']`: 34 of 36 as stated | 396.1 |
| `rv1031_controls.py --mutant always-accept` | `CONTROLS_NOT_AS_STATED ['G1', 'G2', 'S1d', 'E1p', 'P1p', 'W1p', 'W0p']` | 395.6 |
| `rv1031_controls.py --mutant always-refuse` | `CONTROLS_NOT_AS_STATED ['S1d', 'E1c', 'E1p', 'K1c', 'P1c', 'W1c']` | 394.3 |
| `rv1031_contract.py`, #1031 | `MEASURED 6.42436473987e-67 1.00072861528e-74` | 14.7 |
| `rv1031_contract.py`, T-325 | `MEASURED 3.56121490758e-27 2.00004386193e-28` | 10.4 |
| `rv1031_custody.py` | `CUSTODY_HOLDS`, one digest per file, `REGISTRATION.md` and `SHA256SUMS` added after the pin | 0.1 |
| `rv1031_identity.py` | no house one to one under any symmetry; best moves 121 to 131 beyond a tenth | 3 |
| `rv1031_describe.py` | 184 upright, 115 turned, 55 and 54 by at least 15°, 714 close pairs, 734 near pairs | 5 |
| `rv1031_lineage.py`, the donors | the reflection across $x + y = S$; at most 3 turned squares matched at 335 and 372 | 4 |
| `rv1031_lineage.py`, the houses | 52 or 53 turned squares matched at every house from T-248, 1 at T-101 | 4 |
| `rv1031_measures.py` | gain $7.36744250872624 \times 10^{-3}$ below T-325, $2.06880 \times 10^{24}$ times its contraction margin | 0.5 |
| `rv1031_synthetic.sh` | every control as stated on both synthetic packings; each broken copy but form P read clockwise fails 1 to 18 controls | 5 |
| `rv1031_price.py`, in scratch before the freeze | `A 1.1 B 2.1 cmp 0.0`, `contract 1.5`, 0.142 ms a pair for the corner projections | 7 |

## What Failed Along the Way

Before the checker’s freeze, on synthetic data only:

- Under `python -I` the programs could not import one another until each added its own
  directory to `sys.path`.
- The self-test expected an unquoted integer corner to be read; the reader refuses it, as
  the schema’s scalars are strings, and the synthetic writer now quotes integers as the
  source does. A synthetic side `8`, unquoted, was refused for the same reason.
- A broken copy that crashed the self-test was counted as one failure; the self-test now
  counts it check by check. The symmetry controls were made to hold method B’s classes
  and areas to the original’s directly, not only through method A.

After the freeze:

- `/usr/bin/time` is not installed, so the first launch of the self-test and the check
  ran nothing; they were relaunched without it.
- The frozen form P reader refuses T-280’s certificate, whose comment line is UTF-8; the
  measures read a copy without that line.
- The API’s commit record of the pin carries every file’s patch, the author’s programs
  among them. The copy in `out/custody-inputs/` keeps only the commit’s metadata and file
  list; the patches were not read.
- Two rules of the controls plan, S1d and E1p, were wrong for this certificate (the
  review’s F3); their outcomes are the side rule’s.

After the checker’s freeze nothing in the checker’s digest list changed (`sha256sum -c`
above).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
