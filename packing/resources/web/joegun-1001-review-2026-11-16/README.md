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

## What They Printed

- `l186_selftest.py`: `PASSED 73784 cases 0 failed`; method A with only square $i$’s
  normals fails 376, method A counting a zero margin as apart 2,486, and method B with
  open half-planes 7,703.
- `l186_check.py`: `ACCEPT` at all five, every pair apart by both methods (8,001,
  20,706, 26,796, 34,716 and 46,360 pairs), least margins $1.12027 \times 10^{-11}$,
  $1.12031 \times 10^{-11}$, $9.97 \times 10^{-13}$, $1.20000 \times 10^{-12}$ and
  $1.12509 \times 10^{-11}$; each claim the side’s 12-place ceiling.
- `l186_controls.py`: `EVERY_CONTROL_AS_STATED`, 32 of 32 at each count.
- `l186_describe.py`: the tilts, the near pairs and how each wall contact is made.

## After the Freeze

Written and run after the findings were frozen at 06:34:58Z, none of them a decider of
the certificates:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l186_custody.py` | read-only Git plumbing on the clone: commits and times, the pin’s tree, each candidate’s SHA-256 at every commit against the issue’s list; no names or addresses | the clone, `programs/issue-1001.json` | `out/custody.json` |
| `l186_author_outputs.py` | the author’s printed outputs (`packing-witness-verify.txt`, `check-output.txt`) against this lane’s check receipts | those two files, `out/check-nNNN.json` | `out/author-outputs.json` |
| `l186_sides.py` | the gains on the case records’ exact sides, the issue’s printed values, Kodaj’s sides as printed, $s(m) + j$ near each side, the L steps, monotonicity | `packing/frontier/n-*.md` front matter, `programs/issue-1001.json`, the check receipts | `out/sides.json` |

`programs/issue-1001.json` is the issue as fetched at 06:35:25Z, with the digests it
states.

Two of this repository’s devtools were run read-only, writing only here, with
`python -B` from `packing/`. With `SRC`, `R` and `PY` as above, for each count `N`:

```bash
DT="nice -n 19 uv run --frozen --all-extras --group dev python -B -m"
H="house=witness-center-basis:witnesses/known-best/n-$N.yaml"
C="#1001=witness-corners:$SRC/n-$N-candidate.yaml"
$DT devtools.contraction_margin --n $N "$H" --against "$C" --out $R/out/contraction-house-n$N.json
$DT devtools.contraction_margin --n $N "$C" --out $R/out/contraction-new-n$N.json
$DT devtools.measure_identity --n $N "$C" "$H" --out $R/out/identity-n$N.json
$PY $R/programs/l186_custody.py $SRC bc10ce471c9d7841b9a53b383dae87d23dbe5a99 \
  $R/programs/issue-1001.json $R/out/custody.json
$PY $R/programs/l186_author_outputs.py $SRC/packing-witness-verify.txt $SRC/check-output.txt \
  $R/out/author-outputs.json $R/out/check-n127.json $R/out/check-n204.json \
  $R/out/check-n232.json $R/out/check-n264.json $R/out/check-n305.json
$PY $R/programs/l186_sides.py frontier $R/programs/issue-1001.json $R/out/sides.json \
  $R/out/check-n127.json $R/out/check-n204.json $R/out/check-n232.json \
  $R/out/check-n264.json $R/out/check-n305.json
```

They printed:

- **Contraction.** The houses at 127 and 305 first touch at $1 - \lambda^* = 0$ (a pair
  at exact contact); those at 204, 232 and 264 at $10^{-20}$, $2.03 \times 10^{-13}$ and
  $10^{-100}$, side margins $1.48 \times 10^{-19}$, $3.00 \times 10^{-12}$ and
  $1.68 \times 10^{-99}$. Every gain is `within_margin: false`. The certificates first
  touch at $1.12 \times 10^{-11}$, $1.12 \times 10^{-11}$, $9.97 \times 10^{-13}$,
  $1.2 \times 10^{-12}$ and $1.13 \times 10^{-11}$, side margins $1.21 \times 10^{-10}$,
  $1.55 \times 10^{-10}$, $1.47 \times 10^{-11}$, $1.89 \times 10^{-11}$ and
  $1.91 \times 10^{-10}$; both maintained routes accept each as given, with wall
  clearance 0 and least gap equal to `l186_check.py`’s least margin.
- **Identity.** Against each house no symmetry pairs nearest centres one to one; the
  optimal assignment moves 70, 73, 35, 44 and 113 squares beyond $10^{-1}$.
- **Custody.** One commit, the pin, which is the remote head; the five blobs equal the
  issue’s digests and are unchanged at every commit.
- **Sides.** The gains $9.124897 \times 10^{-3}$, $1.714541 \times 10^{-3}$,
  $1.878017 \times 10^{-3}$, $9.275344 \times 10^{-4}$ and $4.704122 \times 10^{-3}$;
  Kodaj’s printed sides less the exact sides equal the issue’s “our part” to its
  figures; no closed form within $10^{-3}$ at four counts and two near coincidences at
  305; no L step or monotonicity moves another count.

After the freeze the eight frozen programs and the plan were checked against
`frozen/checker-frozen-digests.txt` (all `OK`), and the self-test and the five checks,
rerun into scratch space, reproduced every kept receipt in everything but its CPU
seconds.
