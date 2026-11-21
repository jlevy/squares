# Stage 4 Review of #1012's 109: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane r1012's blind stage 4 review of
the exact Witness/v2 certificate that Joost de Winter attached to issue
[#1012](https://github.com/jlevy/squares/issues/1012#issuecomment-6972165182), his
transcription of Tomáš Kodaj's public Kaggle rows for $s(109) \le 10.949289580944$:
[`docs/project/reviews/review-2026-11-20-de-winter-1012-n109.md`](../../../../docs/project/reviews/review-2026-11-20-de-winter-1012-n109.md).

The source is `n109_kaggle/n109_tomkodaj.yaml` of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/aae089c37a2d3fb91b161a1b3a45f06a41277d18)
at `aae089c37a2d3fb91b161a1b3a45f06a41277d18`, which `7232328` removed again, fetched
alone by its blob id; it is not retained here, and the import lane retains it in its own
packet (`de-winter-kodaj-n109-2026-11-18`). This directory is review-only.

| File | Blob | SHA-256 |
| --- | --- | --- |
| `n109_tomkodaj.yaml` | `9f270d766597af325b3222003fb9b76aa06445ba` | `56b4655fada7dfd5d54c1483b021d5b700ecb5c41beba2865a6a8ef7e223b3fb` |

The SHA-256 equals the folder's `SHA256SUMS` line for it. The issue comment states no
digest of this file.

## Layout

- `programs/`: the review's programs and the controls plan.
- `frozen/`: the checker's and plan's digests at their freeze, the findings' digests at
  their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane r1012's own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review. The review of #1038 (lane r1038) was the model; its text,
its packet's README and its frozen digest lists were read, and its programs were not
opened. Each was run with CPython 3.14.7 (the project interpreter) as `python -I -B`,
under `nice -n 19`; the entry points put their own directory on the module path, since
`-I` leaves it off.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `r1012_reader.py` | the reading: one YAML document without anchors, aliases, tags, directives or duplicate keys; the softschema envelope and the Witness/v2 keys; `corners`, `rational`, the origin; distinct ids; four corners of two scalars per square; every scalar `p`, `p/q` or a finite decimal; canonical form recorded | a certificate | nothing (a module) |
| `r1012_sat.py` | method A: unit squares by their sides, wall clearances, and pair margins by separating axes on the corners, each square over one integer denominator, in Python integers | rationals from the reader | nothing (a module) |
| `r1012_clip.py` | method B: unit squares by sides and diagonals, pairs and walls by exact convex clipping, containment by area, in `gmpy2.mpq` | the side and the corners only | nothing (a module) |
| `r1012_decide.py` | a packing by both methods, every square, wall and pair, and their agreement | the side and the corners | nothing (a module) |
| `r1012_geom.py` | nothing: margins and clearances from centres and half-widths, closing moves, wall moves and Euclidean gaps, for the self-test, the controls and the check's description | fractions | nothing (a module) |
| `r1012_writer.py` | nothing: a packing as Witness/v2 corners text in canonical form | fractions | nothing (a module) |
| `r1012_check.py` | a certificate against the git blob id the source tree lists, every square, wall and pair, and the claim's 12-place arithmetic | a certificate, the blob id, the claim | `out/check-n109.json` |
| `r1012_selftest.py` | the reader, both methods and the third formulation against 4,593 checks with hand-derived answers, and three broken packings | nothing | `out/selftest.json` |
| `r1012_controls.py` | the 37 controls of the plan, by both methods or the reader | a certificate, the plan, the claim | `out/controls-n109.json` |
| `r1012_describe.py` | nothing: the tilts, the half-angles, the frame, the extent, the near pairs and the wall contacts | a certificate | `out/describe-n109.json` |
| `r1012_renumber.py` | nothing: the certificate with ids 1 to 109 for this repository's tools, every value read back unchanged (after the findings' freeze) | a certificate | a scratch copy |
| `r1012_binary64_rows.py` | nothing: Samanyu-dev's binary64 rows at 109 read exactly as a corners witness (after the findings' freeze) | `best_fit_101_500.csv` at Samanyu-dev/squares_in_squares `53551d7` | a scratch witness, `out/samanyu-n109-exact.json` |
| `r1012_sides.py` | arithmetic only: the sides at 109 and their differences, exactly (after the findings' freeze) | the certificate, Kodaj's CSV, the contraction receipts, the import lane's contraction receipt | `out/sides.json` |

`programs/controls-plan.json` is the plan, written and hashed before any program read the
certificate; its outcomes are rules over the certificate's exact facts.

From `packing/` of this repository, with `CERT` the certificate fetched by its blob id,
`SRC` the source folder `n109_kaggle/` at `aae089c`, `SAM` Samanyu-dev's
`best_fit_101_500.csv` at `53551d7` (SHA-256 `377b9177…6c04`), `W` a scratch directory,
`IMP` the import lane's `measure/contraction-n109-samanyu.json`, and `R` this directory:

```bash
PY="nice -n 19 .venv/bin/python3 -I -B"
$PY $R/programs/r1012_selftest.py $R/out/selftest.json
$PY $R/programs/r1012_check.py $CERT 9f270d766597af325b3222003fb9b76aa06445ba \
  10.949289580944 $R/out/check-n109.json
$PY $R/programs/r1012_controls.py $CERT $R/programs/controls-plan.json 10.949289580944 \
  $R/out/controls-n109.json
$PY $R/programs/r1012_describe.py $CERT $R/out/describe-n109.json
# after the findings' freeze
$PY $R/programs/r1012_renumber.py $CERT $W/n109_tomkodaj-ids-1-109.yaml
$PY $R/programs/r1012_binary64_rows.py $SAM \
  377b9177febf1b89f08d655531880fb683666e494a3b303f10645e7440996c04 109 \
  $W/samanyu-n109-exact.yaml $R/out/samanyu-n109-exact.json
$PY $R/programs/r1012_check.py $W/samanyu-n109-exact.yaml - 10.949289580946 \
  $R/out/check-samanyu-n109.json
$PY $R/programs/r1012_sides.py $CERT $SRC/n109_tomkodaj.csv $R/out/samanyu-n109-exact.json \
  $R/out/contraction-1012.json $R/out/contraction-samanyu-vs-1012.json \
  $R/out/contraction-T101-vs-1012.json $IMP $R/out/sides.json
```

What they printed:

| Program | Printed | CPU |
| --- | --- | ---: |
| `r1012_selftest.py` | `PASSED 4593 of 4593` | 0.9 s |
| `r1012_check.py` | `ACCEPT 109 squares, 5886 pairs, side 10.949289580943438996860000000000` | 10.6 s |
| `r1012_controls.py` | each control `as stated`, then `EVERY_CONTROL_AS_STATED 37 of 37` | 122 s |
| `r1012_describe.py` | `described 246 near pairs, 24 axis-aligned squares` | 2.2 s |
| `r1012_renumber.py` | `renumbered 109 squares 1..109`, the written copy's SHA-256 `b2236863…` | under 1 s |
| `r1012_binary64_rows.py` | `wrote 109 squares, side 10.94928958094538` | under 1 s |
| `r1012_check.py`, Samanyu-dev's 109 | `ACCEPT 109 squares, 5886 pairs, side 10.949289580945379363234535713286` (its claim argument is a placeholder) | 8.4 s |
| `r1012_sides.py` | the differences in `out/sides.json` | under 1 s |

## Receipts Written by This Repository's Tools

After the findings' freeze, from `packing/`, with the project interpreter under
`nice -n 19`, `C` naming the renumbered copy as `#1012=witness-corners:$W/n109_tomkodaj-ids-1-109.yaml`
and `T` naming T-101 as
`T-101=evand-cert:resources/web/evand-square-packing-2026-10-05/square-packing/s12/search/exact/batch/certs/n-109.cert`:

```bash
python -m devtools.measure_identity --n 109 "$C" "$T" \
  "Samanyu-dev=witness-corners:$W/samanyu-n109-exact.yaml" --out $R/out/identity-n109.json
python -m devtools.contraction_margin --n 109 "$C" --out $R/out/contraction-1012.json
python -m devtools.contraction_margin --n 109 "Samanyu-dev=witness-corners:$W/samanyu-n109-exact.yaml" \
  --against "$C" --out $R/out/contraction-samanyu-vs-1012.json
python -m devtools.contraction_margin --n 109 "$T" --against "$C" \
  --out $R/out/contraction-T101-vs-1012.json
```

They measure identity against T-101 and Samanyu-dev's 109, and the contraction margins of
the certificate, of Samanyu-dev's 109 against it and of T-101 against it; the contraction
runs decide their inputs and the contracted packings by this repository's two maintained
exact routes. The `witness-corners` adapter on `main` reads squares numbered 1 to n, so
the file as published was refused and the renumbered copy was given instead.

## The Freezes

- `frozen/checker-frozen-digests.txt`, written at 11:31:47Z and pushed at 11:32:06Z
  (commit `f7fba53`), before the certificate's blob was fetched and before any program
  of this lane read it: the certificate's git blob id from the source tree, the nine
  programs' digests, the plan's and the self-test receipt's.
- `frozen/findings-frozen-digest.txt`, written at 11:41:02Z and pushed at 11:41:11Z
  (commit `b65873d`): the frozen review text, the checker list, `r1012_describe.py`, the
  four receipts the text cites and the certificate's SHA-256.
- `frozen/review-2026-11-20-de-winter-1012-n109.frozen.md`: the review as it stood at
  the second freeze.

To check them, from this directory: `sha256sum -c` on the lines of each list, with the
paths in the first list read under `programs/` and `out/`, and the certificate by its
blob id (`git hash-object`) and SHA-256.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
