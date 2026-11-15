# Stage 4 Review of #996: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L180’s blind stage 4 review of
issue [#996](https://github.com/jlevy/squares/issues/996), Joost de Winter’s
$s(90) \le 9.994038857546$:
[`docs/project/reviews/review-2026-11-15-de-winter-996.md`](../../../../docs/project/reviews/review-2026-11-15-de-winter-996.md).

The sources are files of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing) at
`64d5ee762a1159248d375973fb33825d51da637d`, not retained here; an import lane would
retain them in its own packet.
The same two blobs are at the head `9cafa33d43f6`. This directory is review-only.

| File | SHA-256 |
| --- | --- |
| `n90/n90_exact.json` | `3adcc363dc2d2cd5e52c1d0196536d137c2039de532de52b5eab39ba7a98e2dc` |
| `n90/n90_witness.yaml` | `3a28f570aaabfa5cb443d1c270925733d714009850deee852abde5f63e809aa6` |

The author’s `SHA256SUMS` at the head states both, and six more files, and they hold.

## Layout

- `programs/`: the review’s programs, the controls plan, the issue as fetched.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts, and `out/grid-n90.txt`, the grid the identity measurement reads.

## Programs

Every program is lane L180’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review.
The reviews of #989 (lane L169) and of #977 and #979 (lane L153) were the models; their
texts were read, and their programs were not opened.
Each was run with CPython 3.14.7 as `python -I -B` from `packing/` of a worktree of
`main` at `91acf2022`, through `uv run --frozen --all-extras --group dev`, under
`nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l180_reader.py` | the reading: the JSON file’s keys, count and canonical scalars; the Witness/v2 twin’s envelope, keys and corners; that the twin holds exactly the JSON file’s packing | a certificate and its twin | nothing (a module) |
| `l180_axes.py` | method A: unit directions, wall clearances and pair margins by separating axes in Python integers, from the JSON file’s centres and edge directions | rationals from the reader | nothing (a module) |
| `l180_clip.py` | method B: unit squares (sides and diagonals of the corners), pairs and walls by exact convex clipping, containment by area, in `gmpy2.mpq` | corners only | nothing (a module) |
| `l180_decide.py` | a packing by both methods, every square, wall and pair, and their agreement | poses and corners | nothing (a module) |
| `l180_check.py` | the certificate and its twin, against their stated digests | `n90_exact.json`, `n90_witness.yaml` | `out/check-n90.json` |
| `l180_geom.py` | nothing: the closed form by corner projections in `fractions`, closing moves and rotations, for the self-test and the plan | fractions | nothing (a module) |
| `l180_selftest.py` | both methods, the closed form and the reader against 31,771 checks with hand-derived answers, and three broken copies | nothing | `out/selftest.json` |
| `l180_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | the certificate, its twin, the check receipt | `out/plan-facts-n90.json` |
| `l180_make_plan.py` | nothing: states the 26 controls and their outcomes | the check receipt, the plan facts | `programs/controls-plan.json` |
| `l180_controls.py` | the 26 controls, by both methods or the reader | the certificate, its twin, the plan, its facts, the check receipt | `out/controls-n90.json` |
| `l180_describe.py` | nothing: the tilts, the near pairs, the near walls, the extents | the certificate, its check receipt | `out/describe-n90.json` |

`programs/issue-996.json` is the issue as fetched at 12:12:19Z, trimmed to its text,
labels and dates.

From `packing/`, with `S` the clone checked out at `64d5ee7` and `R` this directory:

```bash
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
J=$S/n90/n90_exact.json
T=$S/n90/n90_witness.yaml
JS=3adcc363dc2d2cd5e52c1d0196536d137c2039de532de52b5eab39ba7a98e2dc
TS=3a28f570aaabfa5cb443d1c270925733d714009850deee852abde5f63e809aa6
$PY $R/programs/l180_selftest.py $R/out/selftest.json
$PY $R/programs/l180_check.py $J $JS $T $TS $R/out/check-n90.json
$PY $R/programs/l180_plan_facts.py $J $T $R/out/check-n90.json $R/out/plan-facts-n90.json
$PY $R/programs/l180_make_plan.py $R/out/check-n90.json $R/out/plan-facts-n90.json $R/programs/controls-plan.json
$PY $R/programs/l180_controls.py $J $T $R/programs/controls-plan.json $R/out/plan-facts-n90.json \
  $R/out/check-n90.json $R/out/controls-n90.json
$PY $R/programs/l180_describe.py $J $R/out/check-n90.json $R/out/describe-n90.json
```

## What They Printed

- `l180_selftest.py`: `PASSED 31771 cases 0 failed`; method A with only square $i$’s
  normals fails 640, method A counting a zero margin as apart 1,408, and method B with
  open half-planes 1,472.
- `l180_check.py`: `ACCEPT`. The twin agrees with the JSON file, every square listed
  counterclockwise from $C + (u + v)/2$; 4,005 pairs apart by both methods, least margin
  $1.06410355706 \times 10^{-12}$ at (2, 40); 18 wall contacts, nine at the left and
  nine at the bottom; least right and top clearance $5.07389735200 \times 10^{-21}$.
- `l180_plan_facts.py`: the closed form’s exact margin and clearance lists equal method
  A’s; G5 at square 10 (bottom wall); 52 pairs overlapping with every $(c, s)$ read as
  $(c, -s)$; the S4 pair (2, 40) with square 40 moving.
- `l180_controls.py`: `EVERY_CONTROL_AS_STATED`, 26 of 26.
- `l180_describe.py`: no square exactly upright; 50 at $-1.83 \times 10^{-10}$ degrees
  under one exact direction, 40 turned clockwise by 22.90° to 30.99°; 195 pairs from
  $1.064 \times 10^{-12}$ to $9.197 \times 10^{-12}$, the next at $5.85 \times 10^{-6}$;
  the packing’s width in each direction $S - 5.07389735200 \times 10^{-21}$.

## After the Freeze

Written and run after the findings were frozen, none of them a decider of the
certificate:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l180_grid.py` | nothing: writes the grid at 90, nine rows of ten in $[0, 10] \times [0, 9]$, as a binary64 text | nothing | `out/grid-n90.txt` |
| `l180_lineage.py` | the optimal assignment against T-303’s house witness, square by square: moves, turns, the leaning counts | the certificate, `witnesses/known-best/n-090.yaml` | `out/lineage-n90.json` |
| `l180_sides.py` | the claim’s arithmetic and the gain on T-303; the pairs with centres closer than $\sqrt 2$; $s(m) + j$ near the side; the L steps; monotonicity | the certificate, `packing/frontier/n-*.md`, the house witness | `out/sides.json` |
| `l180_witness_read.py` | the twin through `sqpack.witness.validate_witness_document` and the `witness-corners` adapter, as published and with three conventions changed | the certificate, its twin | `out/witness-read.json`, and a changed copy in scratch space |
| `l180_custody.py` | read-only Git plumbing on the clone, `SHA256SUMS`, the issue’s time, the licence, the README’s AI credit; no e-mail addresses | the clone, `programs/issue-996.json` | `out/custody.json` |
| `l180_digests.py` | every frozen digest against the kept bytes, a rerun of the frozen chain against the kept receipts, and the digest of every file here | this directory, the certificate, the rerun | `out/program-digests.json` |

Two of this repository’s devtools were run read-only, writing only here, with
`python -B` from `packing/`, as was `l180_witness_read.py`, which imports this
repository’s witness readers.
With `S`, `J`, `T`, `R` and `PY` as above, `C` the clone and `X` a scratch directory:

```bash
DT="nice -n 19 uv run --frozen --all-extras --group dev python -B -m"
PB="nice -n 19 uv run --frozen --all-extras --group dev python -B"
HOUSE="T-303=witness-center-basis:witnesses/known-best/n-090.yaml"
$DT devtools.contraction_margin --n 90 "$HOUSE" --against "#996=center-direction-json:$J" \
  --out $R/out/contraction-t303-house-n90.json
$DT devtools.contraction_margin --n 90 "#996=center-direction-json:$J" \
  --out $R/out/contraction-new-n90.json
$PY $R/programs/l180_grid.py $R/out/grid-n90.txt
$DT devtools.measure_identity --n 90 "#996=center-direction-json:$J" "$HOUSE" \
  "grid=binary64-xyd:$R/out/grid-n90.txt" --out $R/out/identity-n90.json
$PY $R/programs/l180_lineage.py $J witnesses/known-best/n-090.yaml $R/out/lineage-n90.json
$PY $R/programs/l180_sides.py $J frontier witnesses/known-best/n-090.yaml $R/out/sides.json
$PB $R/programs/l180_witness_read.py $J $T $X/n90_witness-adapter-order.yaml $R/out/witness-read.json
$PY $R/programs/l180_custody.py $C 64d5ee762a1159248d375973fb33825d51da637d \
  9cafa33d43f60423e51058f51dbdf042077c7cc2 $R/programs/issue-996.json $R/out/custody.json
$PY $R/programs/l180_digests.py $R $S/n90 $X/rerun $R/out/program-digests.json
```

They printed:

- **Contraction.** T-303’s house first touches at $1 - \lambda^* = 1.194485 \times
  10^{-12}$, squares 79 and 81, a side margin of $1.098813 \times 10^{-11}$; the gain
  $84766187606095817/20000000000000000000$ is `within_margin: false`, $3.857 \times
  10^8$ times the margin.
  The new certificate first touches at $1.059921 \times
  10^{-12}$, squares 2 and 40, a side margin of $9.532970 \times 10^{-12}$, and both
  maintained routes accept it as given, wall clearance 0 and least gap this review’s.
- **Identity.** Against T-303 no symmetry pairs nearest centres one to one; the optimal
  assignment under the identity moves 89 squares beyond $10^{-3}$, 34 beyond $10^{-2}$
  and 6 beyond $10^{-1}$ (largest 0.646), and pairs each square $k$ with T-303’s square
  $k$. Against the grid, 56 squares lie beyond a tenth and all 40 turned squares pair
  with upright ones.
- **Lineage.** T-303’s 43, 57, 58 and 60 are now upright; 63, 70, 86 and 89 take the
  common near-upright direction; 4, 5, 17, 19, 21, 24, 42, 54, 64, 65, 72 and 80 turn
  further clockwise by 1.03° to 4.89°. Leaning counts: T-303 49, 48, 44 and the new
  packing 90, 40, 40 for squares not exactly upright, beyond $10^{-9}$ degrees and
  beyond 1°.
- **Sides.** The claim is the side’s 12-place ceiling; the gain on T-303 is
  0.00423830938030479085; 202 pairs have centres closer than $\sqrt 2$; no $s(m) + j$
  lies within $10^{-3}$; no L step from the new side improves a case; nothing moves by
  monotonicity.
- **The twin.** `validate_witness_document` accepts it; the `witness-corners` adapter
  refuses it as published (the schema named by URL) and reads the changed copy back to
  the JSON poses exactly.
- **Custody.** Three commits on 15 November, all by Joost de Winter; the certificate
  blobs unchanged from the pin to the head; every digest of `SHA256SUMS` holds; the
  issue opened 167 seconds after the pin and 46 after the head; the MIT licence; the
  pin’s README credits “OpenAI Codex (GPT-6 Astra)”, the head’s GPT-6.1 Sol Max.
- **Digests.** `ALL_FROZEN_DIGESTS_HOLD` and `RERUN_REPRODUCES_EVERY_RECEIPT`.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the two source files, the seven checker files and the receipts they had written | 2026-11-15T12:12:15Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l180_controls.py` existed | 2026-11-15T12:15:57Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | 2026-11-15T12:23:58Z |
| `frozen/review-2026-11-15-de-winter-996.frozen.md` | the review as frozen, before the author’s README, checkers, the record at 90 or T-303’s certificate were read | 2026-11-15T12:23:58Z |

## Addendum on #997

Issue [#997](https://github.com/jlevy/squares/issues/997) replaces this certificate by a
smaller one, at `fa53fb0d734fbf438bcfb73c1434a15894bb2bc5`. Lane L182’s addendum decides
it with the programs here, unchanged, and keeps its own programs, plan, receipts and
frozen digest lists in [`addendum-997/`](addendum-997/README.md).
In this packet it changed nothing outside that directory but this section.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
