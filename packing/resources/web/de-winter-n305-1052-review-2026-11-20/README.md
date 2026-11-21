# Stage 4 Review of #1052’s 305: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane r1052’s blind stage 4 review of
Joost de Winter’s exact certificate for $s(305) \le 17.945755838742$, issue
[#1052](https://github.com/jlevy/squares/issues/1052):
[`docs/project/reviews/review-2026-11-20-de-winter-1052-n305.md`](../../../../docs/project/reviews/review-2026-11-20-de-winter-1052-n305.md).

The source is `n305/` of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing/tree/db8efcb6bf05906e977bc62f1f6d8ccfcaa296ef/n305)
at `db8efcb6bf05906e977bc62f1f6d8ccfcaa296ef`; the two certificate files were fetched
alone, by their blob ids, after the checker’s freeze. They are not retained here: this
directory is review-only, and retaining the source is the import lane’s.

| File | Blob | SHA-256 |
| --- | --- | --- |
| `n305_exact.json` | `355cbe46ff685c00c1bb292443b974084dc0b9c4` | `e6c7d0280396a2fa61804a24a7c757365320869dbb89e8cf94316bb8b6a7831f` |
| `n305_witness.yaml` | `58ab84e20c2eb6d533f59d8f3141de3d4bfbf4f1` | `b11a6e65a275d3282e1400b89b4cdbd9ca01cf99d01a8e9f0a38a56c20081a46` |

Both digests equal the folder’s `SHA256SUMS` lines for them, as checked after the
findings’ freeze; the issue states no digest. The reading copy of the witness that the
check and the controls read (SHA-256 `ab67001d…`) is not retained:
`r1052_envelope_copy.py` remakes it from the witness, and `out/envelope-copy.json` gives
both digests.

## Layout

- `programs/`: the review’s programs and the controls plan.
- `frozen/`: the checker’s and plan’s digests at their freeze, the findings’ digests at
  their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane r1052’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review. The review of #1012 (lane r1012) was the model; its text,
its packet’s README and its frozen digest lists were read, and its programs were not
opened. Each was run with CPython 3.14.7 (the project interpreter) as `python -I -B`,
under `nice -n 19`; the entry points put their own directory on the module path, since
`-I` leaves it off.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `r1052_reader.py` | the reading of both forms: form J (JSON, no duplicate key, no float or non-finite number, exactly the keys `n`, `side`, `square_size`, `format`, `squares`, rows of four scalar strings) and form C (one YAML document without directives, anchors, aliases, tags or duplicate keys; the softschema envelope with `contract` and `envelope`; the Witness/v2 keys with `claim`; `corners`, `rational`, the origin; distinct ids; four corners of two scalars); every scalar `p`, `p/q` or a quoted finite decimal; canonical form recorded | a certificate file | nothing (a module) |
| `r1052_poses.py` | method A: unit squares by $\cos^2 + \sin^2 = 1$, wall clearances by half-extents, and pair margins by separating axes on poses, each pose over one integer denominator, in Python integers; from corners, its own pose | rationals from the reader | nothing (a module) |
| `r1052_clip.py` | method B: unit squares by sides and diagonals, pairs and walls by exact convex clipping, containment by area, squared Euclidean gaps of pairs apart, in `gmpy2.mpq`; from poses, its own corners | rationals from the reader | nothing (a module) |
| `r1052_decide.py` | one packing by both methods, every square, wall and pair, and their agreement | the side and the poses or corners | nothing (a module) |
| `r1052_geom.py` | nothing: margins and clearances from centres and half-widths, closing moves and wall moves, for the self-test, the controls and the twin test’s corners | fractions | nothing (a module) |
| `r1052_writer.py` | nothing: a packing as form J or form C text, every scalar canonical | fractions | nothing (a module) |
| `r1052_check.py` | the two files against the tree’s blob ids, the twin, both files by both methods, the files’ agreement, and the claim’s 12-place arithmetic with both files decided in the claim’s box | the two files, the blob ids, the count, the claim | `out/check-n305.json`, `out/check-n305-reading-copy.json` |
| `r1052_selftest.py` | the reader, both methods, the third formulation and the check against 608 checks with hand-derived answers, broken packings, and substituted wrong methods | nothing | `out/selftest.json` |
| `r1052_controls.py` | the 51 controls of the plan, by both methods or the reader | the two files, the plan, the claim | `out/controls-n305.json` |
| `r1052_envelope_copy.py` | nothing: a reading copy of the witness with `envelope: witness` and a `claim` block inserted, proved to differ from the original by those lines only (after the checker’s freeze) | the witness | a scratch copy, `out/envelope-copy.json` |
| `r1052_describe.py` | nothing: the tilts, the half-angles, the coordinates’ places, the near pairs with exact Euclidean gaps, the near-axis squares and the walls | the two files | `out/describe-n305.json` |
| `r1052_sides.py` | arithmetic only: the sides at 305 and their differences, exactly (after the findings’ freeze) | form J, and the other sides as their sources print them | `out/sides.json` |

`programs/controls-plan.json` is the plan, written and hashed before any program read the
certificate; its outcomes are rules over the certificate’s exact facts.

From `packing/` of this repository, with `J` and `C` the two files fetched by their blob
ids, `C2` the reading copy, `W` a scratch directory and `R` this directory:

```bash
PY="nice -n 19 .venv/bin/python3 -I -B"
$PY $R/programs/r1052_selftest.py $R/out/selftest.json $W
$PY $R/programs/r1052_check.py $J $C 355cbe46ff685c00c1bb292443b974084dc0b9c4 \
  58ab84e20c2eb6d533f59d8f3141de3d4bfbf4f1 305 17.945755838742 $R/out/check-n305.json
# after the checker's freeze, since the reader refuses the witness as published
$PY $R/programs/r1052_envelope_copy.py $C $C2 $R/out/envelope-copy.json
$PY $R/programs/r1052_check.py $J $C2 355cbe46ff685c00c1bb292443b974084dc0b9c4 - 305 \
  17.945755838742 $R/out/check-n305-reading-copy.json
$PY $R/programs/r1052_controls.py $J $C2 $R/programs/controls-plan.json 17.945755838742 \
  $R/out/controls-n305.json
$PY $R/programs/r1052_describe.py $J $C2 $R/out/describe-n305.json
# after the findings' freeze; T309, T309C and OWNC are the side and contracted_side of
# out/contraction-T309-vs-1052.json and the contracted_side of out/contraction-1052.json
$PY $R/programs/r1052_sides.py $J $R/out/sides.json \
  "T-309, exact (results.yaml; the contraction receipt)=$T309" \
  "T-309 as the case record displays it=17.9457623596589697" \
  "T-309 at 12 places, as #1001 prints it=17.945762359659" \
  "T-309 shrunk to first contact (contraction receipt)=$T309C" \
  "JoeGun's exact touching point near T-309, numerical (joegun-local-minimum packet)=17.945762359467513364" \
  "Shadoks, Kaggle leaderboard, as the issue prints it=17.94575583874176" \
  "Shadoks, as JoeGun's README table prints it=17.945755838742" \
  "the claim=17.945755838742" \
  "the certificate shrunk to first contact (contraction receipt)=$OWNC" \
  "the side less 1e-12, S1f's floor box=17.945755838741"
```

What they printed:

| Program | Printed | CPU |
| --- | --- | ---: |
| `r1052_selftest.py` | `PASSED 608 of 608` | 2.5 s |
| `r1052_check.py`, the files as published | `REFUSE 305 squares, side 17.945755838741588671058398336013, 1 problems` | 96 s |
| `r1052_envelope_copy.py` | `copy written; deleting the inserted lines restores the original: True` | under 1 s |
| `r1052_check.py`, form J and the reading copy | `ACCEPT 305 squares, side 17.945755838741588671058398336013, 0 problems` | 190 s |
| `r1052_controls.py` | each control `as stated`, then `EVERY_CONTROL_AS_STATED 51 of 51` | 665 s |
| `r1052_describe.py` | `described 877 near pairs, 176 axis-aligned squares, 93 visibly turned` | 5 s |
| `r1052_sides.py` | each side, and the certificate less it | under 1 s |

## Receipts Written by This Repository’s Tools

After the findings’ freeze, from `packing/`, with the project interpreter under
`nice -n 19`, `C` naming the certificate as `#1052=center-direction-json:$J` and `T`
naming T-309 as `T-309=packet:joegun-upper-bounds-2026-11-16`:

```bash
python -m devtools.measure_identity --n 305 "$C" "$T" \
  "T-309-regularized=witness-center-basis:atlas/known-best/regularized/n-305-regularized.yaml.gz" \
  --out $R/out/identity-n305.json
python -m devtools.contraction_margin --n 305 "$C" --out $R/out/contraction-1052.json
python -m devtools.contraction_margin --n 305 "$T" --against "$C" \
  --out $R/out/contraction-T309-vs-1052.json
```

They measure identity against T-309 and the record’s regularized drawing of it, and the
contraction margins of the certificate and of T-309 against it; the contraction runs
decide their inputs and the contracted packings by this repository’s two maintained
exact routes. The certificate is read from `n305_exact.json` by the
`center-direction-json` adapter.

## The Freezes

- `frozen/checker-frozen-digests.txt`, written at 19:42:44Z and pushed at 19:43Z
  (commit `1e5214e`), before the certificate’s blobs were fetched (19:43:38Z) and
  before any program of this lane read them: the two blob ids from the source tree, the
  nine programs’ and the plan’s digests and the self-test receipt’s.
- `frozen/findings-frozen-digests.txt`, written at 20:16:13Z and pushed at 20:16:36Z
  (commit `c686263`): the frozen review text, the checker list,
  `r1052_envelope_copy.py` and `r1052_describe.py`, the six receipts the text cites,
  and the SHA-256 of both certificate files and of the reading copy.
- `frozen/review-2026-11-20-de-winter-1052-n305.frozen.md`: the review as it stood at
  the second freeze.

To check them, from this directory: `sha256sum -c` on the lines of each list, with the
paths in the first list read under `programs/` and `out/`, and the certificate files by
their blob ids (`git hash-object`) and SHA-256.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
