# Stage 4 Review of #1038: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane r1038’s blind stage 4 review of
issue [#1038](https://github.com/jlevy/squares/issues/1038), Doğa Özden’s exact
certificate of jazivxt’s public Kaggle packing for $s(228) \le 15.596043116632$:
[`docs/project/reviews/review-2026-11-20-ozden-1038.md`](../../../../docs/project/reviews/review-2026-11-20-ozden-1038.md).

The source is `n-228-candidate.yaml` of
[kenaznia-doga/s228-upper-bound-1559604311](https://github.com/kenaznia-doga/s228-upper-bound-1559604311)
at `46ab8bf425f5cad886a8bc4023bfff904f43af99`, the repository’s only commit when it was
cloned, not retained here; an import lane would retain it in its own packet.
This directory is review-only.

| File | Blob | SHA-256 |
| --- | --- | --- |
| `n-228-candidate.yaml` | `1319f5936d2ce605519a9ffb4e1b0160a7cf1fb9` | `1b816e2e9302ad58ca2d5bb5882f4f98b2c8fb4f9e5746a8ed3f823cfd4a3387` |

The SHA-256 equals the one the issue states.

## Layout

- `programs/`: the review’s programs, the controls plan, and the issue as the REST API
  returned it at 08:14Z (`issue-1038.json`).
- `frozen/`: the checker’s and plan’s digests at their freeze, the findings’ digests at
  their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane r1038’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review.
The review of #1001 (lane L186) was the model; its text, its packet’s README and its
frozen digest lists were read, and its programs were not opened.
Each was run with CPython 3.14.7 (the project interpreter) as `python -I -B`, under
`nice -n 19`; the entry points put their own directory on the module path, since `-I`
leaves it off.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `r1038_reader.py` | the reading: one YAML document without anchors, aliases, tags, directives or duplicate keys; the softschema envelope and the Witness/v2 keys; `center-basis`, `rational`, the lower-left origin; ids 1 to $n$ in order; every scalar `p` or `p/q`; canonical form recorded | a certificate | nothing (a module) |
| `r1038_sat.py` | method A: unit bases, wall clearances and pair margins by separating axes on the centres and bases, each square over one integer denominator, in Python integers | rationals from the reader | nothing (a module) |
| `r1038_clip.py` | method B: corners built from centre and basis, unit squares (sides and diagonals), pairs and walls by exact convex clipping, containment by area, in `gmpy2.mpq` | centres and bases only | nothing (a module) |
| `r1038_decide.py` | a packing by both methods, every square, wall and pair, and their agreement | centres and bases | nothing (a module) |
| `r1038_check.py` | a certificate against its stated digest, and the claim’s 12-place arithmetic | a certificate, its digest, the claim | `out/check-n228.json` |
| `r1038_geom.py` | nothing: margins and clearances from corner projections, closing moves and wall moves, for the self-test and the controls | fractions | nothing (a module) |
| `r1038_selftest.py` | the reader, both methods and the corner formulation against 36,910 checks with hand-derived answers, and three broken packings | nothing | `out/selftest.json` |
| `r1038_controls.py` | the 36 controls of the plan, by both methods or the reader | a certificate, the plan, the claim | `out/controls-n228.json` |
| `r1038_describe.py` | nothing: the tilts, the near pairs with their Euclidean gaps and multiples of the factor’s epsilon, how each wall contact is made, and the factor’s pre-images about the lower-left origin and about the box centre | a certificate | `out/describe-n228.json` |
| `r1038_sides.py` | arithmetic only: the sides at 228 and their differences, exactly (after the findings’ freeze) | the certificate, the case record, the contraction receipt, the regularization driver’s report at 228, the source’s decimal slice | `out/sides.json` |

`programs/controls-plan.json` is the plan, written and hashed before any program read the
certificate; its outcomes are rules over the certificate’s exact facts.

From `packing/` of this repository, with `SRC` the clone checked out at `46ab8bf` and `R`
this directory:

```bash
PY="nice -n 19 .venv/bin/python3 -I -B"
$PY $R/programs/r1038_selftest.py $R/out/selftest.json
$PY $R/programs/r1038_check.py $SRC/n-228-candidate.yaml \
  1b816e2e9302ad58ca2d5bb5882f4f98b2c8fb4f9e5746a8ed3f823cfd4a3387 15.596043116632 \
  $R/out/check-n228.json
$PY $R/programs/r1038_controls.py $SRC/n-228-candidate.yaml $R/programs/controls-plan.json \
  15.596043116632 $R/out/controls-n228.json
$PY $R/programs/r1038_describe.py $SRC/n-228-candidate.yaml $R/out/describe-n228.json
$PY $R/programs/r1038_sides.py $SRC/n-228-candidate.yaml frontier/n-228.md \
  $R/out/contraction-T301-vs-1038.json \
  cases/regularized_drawings/think-17ex-2026-11-15/adopt-2026-11-15-n147-228-evand/n-228/report.json.gz \
  $SRC/source/hit-228.txt $R/out/sides.json
```

What they printed:

| Program | Printed | CPU |
| --- | --- | ---: |
| `r1038_selftest.py` | `PASSED 36910 of 36910` | 2.9 s |
| `r1038_check.py` | `ACCEPT 228 squares, 25878 pairs, side 15.596043116631766506701146832188` | 3.3 s |
| `r1038_controls.py` | each control `as stated`, then `EVERY_CONTROL_AS_STATED 36 of 36` | 126 s |
| `r1038_describe.py` | `described 318 near pairs, 146 axis-aligned squares` | 4.2 s |
| `r1038_sides.py` | the differences in `out/sides.json` | under 1 s |

## Receipts Written by This Repository’s Tools

After the findings’ freeze, from `packing/`, with the project interpreter under
`nice -n 19`:

```bash
python -m devtools.measure_identity --n 228 "#1038=witness-center-basis:$SRC/n-228-candidate.yaml" \
  "T-301=packet:ono-issue984-2026-11-14" "house=witness-center-basis:witnesses/known-best/n-228.yaml" \
  "T-300=packet:ozden-s228-upper-bound-2026-11-14" --out $R/out/identity-n228.json
python -m devtools.contraction_margin --n 228 'T-301=packet:ono-issue984-2026-11-14' \
  --against "#1038=witness-center-basis:$SRC/n-228-candidate.yaml" \
  --out $R/out/contraction-T301-vs-1038.json
python -m devtools.contraction_margin --n 228 "#1038=witness-center-basis:$SRC/n-228-candidate.yaml" \
  --out $R/out/contraction-1038.json
```

They measure identity against T-301, the house witness and T-300, and the contraction
margins of T-301 (against the certificate) and of the certificate; both contraction runs
decide their inputs by this repository’s two maintained exact routes.

## The Freezes

- `frozen/checker-frozen-digests.txt`, written at 08:32:15Z and pushed at 08:33:03Z
  (commit `4d8bb9f`), before any program of this lane read the certificate: the
  certificate’s digest, the eight programs’, the plan’s, the issue snapshot’s and the
  self-test receipt’s.
- `frozen/findings-frozen-digest.txt`, written at 08:41:53Z and pushed at 08:42:10Z
  (commit `3cc5e67`): the frozen review text, the checker list, `r1038_describe.py` and
  the four receipts the text cites.
- `frozen/review-2026-11-20-ozden-1038.frozen.md`: the review as it stood at the second
  freeze.

To check them, from this directory: `sha256sum -c` on the lines of each list, with the
paths in the first list read under `programs/` (and the certificate under the clone).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
