# Stage 4 Review of #1001: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L186’s blind stage 4 review of
issue [#1001](https://github.com/jlevy/squares/issues/1001), JoeGun’s five upper bounds
$s(127)$, $s(204)$, $s(232)$, $s(264)$ and $s(305)$ on Tomáš Kodaj’s public Kaggle
packings:
[`docs/project/reviews/review-2026-11-16-joegun-1001.md`](../../../../docs/project/reviews/review-2026-11-16-joegun-1001.md).

The sources are files of
[JonathanGun/square-packing-upper-bounds](https://github.com/JonathanGun/square-packing-upper-bounds)
at `bc10ce471c9d7841b9a53b383dae87d23dbe5a99`, the repository’s only commit when it was
cloned, not retained here; an import lane would retain them in its own packet.
This directory is review-only.

| File | SHA-256 |
| --- | --- |
| `n-127-candidate.yaml` | `9bde48b76afce9ab7d20d6d180650d0a6bbe46b7f106573f8155dfe9ed9d06f0` |
| `n-204-candidate.yaml` | `1daa0e09b5b403e4e47048104c760f3d8a9b6997d77d26a30930bf1e257ea90c` |
| `n-232-candidate.yaml` | `93d856c25c9f75842ca5e36552ccb726e87884440689c9ce4100d2a58d5a279d` |
| `n-264-candidate.yaml` | `14fef8f163b2cdb9062f714cdd41d81dce2447691a2de55e3797810cdcd676ee` |
| `n-305-candidate.yaml` | `14d2e37e22218defb238e0b0e657f139bab0c2873cc3d05f781b0f3b13a75494` |

All five equal the digests the issue lists.

## Layout

- `programs/`: the review’s programs and the controls plan.
- `frozen/`: the checker’s and plan’s digests at their freeze, the findings’ digest at
  their freeze, and the frozen review text.
- `out/`: the receipts.

## Programs

Every program is lane L186’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review.
The review of #996 (lane L180) was the model; its text, its packet’s README and its
frozen checker list were read, and its programs were not opened.
Each was run with CPython 3.14.7 (the project interpreter) as `python -I -B`, under
`nice -n 19`; the entry points put their own directory on the module path, since `-I`
leaves it off.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l186_reader.py` | the reading: one YAML document without anchors, aliases, tags or duplicate keys; the softschema envelope and the Witness/v2 keys; `corners`, `rational`, the lower-left origin; ids 1 to $n$ in order; every scalar `p` or `p/q`; canonical form recorded | a certificate | nothing (a module) |
| `l186_sat.py` | method A: unit squares, wall clearances and pair margins by separating axes on the corners, each square over one integer denominator, in Python integers | rationals from the reader | nothing (a module) |
| `l186_clip.py` | method B: unit squares (sides and diagonals), pairs and walls by exact convex clipping, containment by area, in `gmpy2.mpq` | corners only | nothing (a module) |
| `l186_decide.py` | a packing by both methods, every square, wall and pair, and their agreement | corners | nothing (a module) |
| `l186_check.py` | a certificate against its stated digest, and the claim’s 12-place arithmetic | a certificate, its digest, the claim | `out/check-nNNN.json` |
| `l186_geom.py` | nothing: the closed form by centres and half-extents, closing moves and wall moves, for the self-test and the controls | fractions | nothing (a module) |
| `l186_selftest.py` | the reader, both methods and the closed form against 73,784 checks with hand-derived answers, and three broken copies | nothing | `out/selftest.json` |
| `l186_controls.py` | the 32 controls of the plan, by both methods or the reader | a certificate, the plan | `out/controls-nNNN.json` |
| `l186_describe.py` | nothing: the tilts, the near pairs, how each wall contact is made, the near clearances | a certificate, its check receipt | `out/describe-nNNN.json` |

`programs/controls-plan.json` is the plan, written and hashed before any program read a
certificate; its outcomes are rules over each certificate’s exact facts.

From `packing/` of this repository, with `SRC` the clone checked out at `bc10ce4` and
`R` this directory:

```bash
PY="nice -n 19 .venv/bin/python3 -I -B"
$PY $R/programs/l186_selftest.py $R/out/selftest.json
$PY $R/programs/l186_check.py $SRC/n-127-candidate.yaml \
  9bde48b76afce9ab7d20d6d180650d0a6bbe46b7f106573f8155dfe9ed9d06f0 11.801753890487 \
  $R/out/check-n127.json
# likewise 204 (14.802646843107), 232 (15.759531627557), 264 (16.773807598002)
# and 305 (17.945762359659), with the digests above
$PY $R/programs/l186_controls.py $SRC/n-127-candidate.yaml $R/programs/controls-plan.json \
  127 $R/out/controls-n127.json
$PY $R/programs/l186_describe.py $SRC/n-127-candidate.yaml $R/out/check-n127.json \
  $R/out/describe-n127.json
```
