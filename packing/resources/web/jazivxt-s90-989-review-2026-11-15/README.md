# Stage 4 Review of #989: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L169’s blind stage 4 review of
issue [#989](https://github.com/jlevy/squares/issues/989), $s(90) \le 9.998277166926$,
credited to jazivxt and GPT-6 Astra Ultra and opened by dpre4ai:
[`docs/project/reviews/review-2026-11-15-jazivxt-989.md`](../../../../docs/project/reviews/review-2026-11-15-jazivxt-989.md).

The sources are files of
[dpre4ai/n90-square-packing](https://github.com/dpre4ai/n90-square-packing) at
`179fcba7f0e91e2c3d3e92525e0738b6da0f8dd5`, not retained here; an import lane would
retain them in its own packet.
This directory is review-only.

| File | SHA-256 |
| --- | --- |
| `n90.cert` | `88c93b2f1d1f3061d1e6815f790d13f3d8f174dd3431f50d8d4d9d4383b3d466` |
| `n90.csv` | `181a51b9c0c23b47bf8d203cedd98076d79f9714e42b6e991d6f1a10c87ca774` |
| `n90.png` | `81eaae7e8196587c0b3ea28ee8fec955630483344e3b3714a64e3922e7e3093e` |
| `README.md` | `bbf6660a0a96dbf9ed575f75be08f16f167daf4b29cf2b65116b7ea92f870153` |
| `DONOR-LICENSE.txt` | `324f918c18cdddf76fb5365f1ff8b3c126bf83ab47937c59d1d2443ba61b9c7a` |

The issue states the certificate’s digest; the author’s `SHA256SUMS` states all five,
and they hold.

## Layout

- `programs/`: the review’s programs, the controls plan, the issue as fetched.
- `frozen/`: the checker’s digests at its freeze, the plan’s digest when it was stated,
  the findings’ digest at their freeze, and the frozen review text.
- `out/`: the receipts; `out/lineage/` holds the seed rebuilt from de Winter’s 157, the
  input of one identity measurement.

## Programs

Every program is lane L169’s own, written for this review as a clean-room
implementation: it imports nothing from this repository or the source, and reuses no
code of any earlier review.
The reviews of #984 and #985 (lane L163) and of #983 (lane L159) were the models; their
texts were read, and their programs were not opened.
Each was run with CPython 3.14.7 as `python -I -B` from `packing/` of a worktree of
`main` at `a4f36ae70`, through `uv run --frozen --all-extras --group dev`, under
`nice -n 19`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l169_reader.py` | the reading: the `.cert` text, its count and canonical `p/q` scalars | a certificate | nothing (a module) |
| `l169_sat.py` | method A: unit directions, wall clearances and pair margins by separating axes in Python integers, from centres and half-angles | integers from the reader | nothing (a module) |
| `l169_clip.py` | method B: unit squares (sides and diagonals of the corners), pairs and walls by exact convex clipping, containment by area, in `gmpy2.mpq` | integers from the reader | nothing (a module) |
| `l169_decide.py` | a certificate by both methods, every square, wall and pair, and their agreement | a reading | nothing (a module) |
| `l169_check.py` | the certificate, against its stated digest | `n90.cert` | `out/check-n90.json` |
| `l169_geom.py` | nothing: the closed form by corner projections in `fractions`, and closing moves, for the self-test and the plan | fractions | nothing (a module) |
| `l169_selftest.py` | both methods and the reader against 6,166 cases with hand-derived answers, and three broken copies | nothing | `out/selftest.json` |
| `l169_plan_facts.py` | nothing: the exact facts the controls plan states its outcomes from | the certificate, its check receipt | `out/plan-facts-n90.json` |
| `l169_make_plan.py` | nothing: states the controls and their outcomes | the check receipt, the plan facts | `programs/controls-plan.json` |
| `l169_controls.py` | the 23 controls, by both methods or the reader | the certificate, the plan, its facts, the check receipt | `out/controls-n90.json` |
| `l169_describe.py` | nothing: the tilts, the near-pair margins, the near-wall clearances, the extents | the certificate, its check receipt | `out/describe-n90.json` |

From `packing/`, with `S` the clone checked out at `179fcba` and `R` this directory:

```bash
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
C=$S/n90.cert
$PY $R/programs/l169_selftest.py $R/out/selftest.json
$PY $R/programs/l169_check.py $C 88c93b2f1d1f3061d1e6815f790d13f3d8f174dd3431f50d8d4d9d4383b3d466 $R/out/check-n90.json
$PY $R/programs/l169_plan_facts.py $C $R/out/check-n90.json $R/out/plan-facts-n90.json
$PY $R/programs/l169_make_plan.py $R/out/check-n90.json $R/out/plan-facts-n90.json $R/programs/controls-plan.json
$PY $R/programs/l169_controls.py $C $R/programs/controls-plan.json $R/out/plan-facts-n90.json \
  $R/out/check-n90.json $R/out/controls-n90.json
$PY $R/programs/l169_describe.py $C $R/out/check-n90.json $R/out/describe-n90.json
```

## What They Printed

- `l169_selftest.py`: `PASSED 6166 cases 0 failed`; method A with only square $i$’s
  normals fails 288, method A counting a zero margin as apart 1,476, and method B with
  open half-planes 1,584.
- `l169_check.py`: `ACCEPT`. 4,005 pairs apart by both methods, least margin
  $1.19448 \times 10^{-12}$ at (79, 81); no pair touches and no square touches a wall;
  least clearances $2.1 \times 10^{-15}$ (left and bottom) and
  $2.3772283 \times 10^{-13}$ (right and top).
- `l169_plan_facts.py`: the closed form’s exact margin and clearance lists equal method
  A’s; G5 at square 60 (left wall); 66 pairs overlapping with every $t$ negated; the S4
  pair (79, 81) with square 79 moving.
- `l169_controls.py`: `EVERY_CONTROL_AS_STATED`, 23 of 23.
- `l169_describe.py`: 41 squares upright, 44 turned clockwise by 22.61° to 31.56°, five
  within 0.07°; 174 pairs between $1.19 \times 10^{-12}$ and $8.16 \times 10^{-12}$, the
  next at $2.05 \times 10^{-4}$; the packing’s width in each direction
  $S - 2.398228330832381 \times 10^{-13}$.

## After the Freeze

Written and run after the findings were frozen, none of them a decider of the
certificate:

| Program | What it measures | Reads | Writes |
| --- | --- | --- | --- |
| `l169_lineage.py` | the symmetry and translation that carry de Winter’s 157 onto the certificate, the README’s crop and its least pitch, the seed of two copies, its overlaps, and the certificate’s moves from it, in binary64 | de Winter’s `n157_exact.json` as the T-293 packet retains it, the certificate | `out/lineage-n90.json`, `out/lineage/seed-n90.cert` |
| `l169_record.py` | the claim’s arithmetic; every case’s reported bound around the grid, $s(k^2 - k)$ and $s(k^2 - 10)$; which families reach 90; $s(m) + j$ near the side; the L steps; monotonicity | `packing/frontier/n-*.md`, the certificate | `out/record-n90.json` |
| `l169_custody.py` | read-only Git plumbing on the clone, `SHA256SUMS`, the CSV against the certificate, the issue’s time; no e-mail addresses | the clone, `programs/issue-989.json` | `out/custody.json` |
| `l169_digests.py` | every frozen digest against the kept bytes, a rerun of the frozen chain against the kept receipts, and the digest of every file here | this directory, the certificate, the rerun | `out/program-digests.json` |

Two of this repository’s devtools were run read-only, writing only here, with
`python -B` from `packing/`. With `S`, `C`, `R` and `PY` as above, and `X` a scratch
directory:

```bash
DT="nice -n 19 uv run --frozen --all-extras --group dev python -B -m"
N157=resources/web/de-winter-s157-upper-bound-2026-11-11/source/n157/n157_exact.json
HOUSE="house=witness-corners:witnesses/known-best/n-090.yaml"
$PY $R/programs/l169_lineage.py $N157 $C $R/out/lineage-n90.json $R/out/lineage/seed-n90.cert
$DT devtools.contraction_margin --n 90 "#989=evand-cert:$C" --out $R/out/contraction-new-n90.json
$DT devtools.contraction_margin --n 90 "$HOUSE" --against "#989=evand-cert:$C" \
  --out $R/out/contraction-house-n90.json
$DT devtools.measure_identity --n 90 "#989=evand-cert:$C" "$HOUSE" \
  "seed=evand-cert:$R/out/lineage/seed-n90.cert" --out $R/out/identity-n90.json
$PY $R/programs/l169_record.py frontier $C $R/out/record-n90.json
$PY $R/programs/l169_custody.py $S 179fcba7f0e91e2c3d3e92525e0738b6da0f8dd5 \
  $R/programs/issue-989.json $R/out/custody.json
$PY $R/programs/l169_digests.py $R $C $X $R/out/program-digests.json
```

They printed:

- **Lineage.** De Winter’s 157 under the identity (it is a fourfold pinwheel, so the
  four rotations read alike, and no mirror matches), translated by
  $(-2.99624, 0.00183)$; the crop from his bottom wall to the top of his square 103,
  9.3533845, 107 squares; least pitch 9.353384 for a copy shifted by 0 or −1 and
  9.019403129 for one shifted by +1; 91 centres in the certificate’s box, of which a
  side-10 window with its left edge 0.113 to 0.503 to the right holds exactly 90 (81 and
  9 from the two copies); the certificate one to one with that seed, largest move
  0.1457, largest turn 4.02°.
- **Contraction.** The house at 90 (the grid) has margin 0, squares 1 and 2 touching;
  the gain $861416537/500000000000$ is `within_margin: false`. The certificate contracts
  by $1 - \lambda^* = 1.194485 \times 10^{-12}$ at (79, 81), a side margin of
  $1.0988 \times 10^{-11}$, and both maintained routes accept it as given.
- **Identity.** Against the house no symmetry pairs the squares one to one (52 move
  beyond a tenth, and 44 tilted squares pair with upright ones); against the seed the
  pairing is one to one under the identity.
- **Record.** The claim is exactly 9.998277166926 and gains 0.001722833074 on 10. The
  reported $s(k^2 - k)$ is $k$ for $k = 2$ to 10 and below $k$ for $k = 11$ to 18;
  $s(k^2 - 10)$ is below $k$ for $k \le 9$ and $k$ for $k = 10$ to 18. No family of
  $s(k^2 - c) = k$ with $c \le 5$ reaches 90; no $s(m) + j$ lies within $10^{-3}$ of the
  side; no L step from the new side improves a case; nothing moves by monotonicity.
- **Custody.** Three commits by one author name within 46 seconds; the pin changes only
  the README’s credit line and `SHA256SUMS` from its parent; every digest of
  `SHA256SUMS` holds; the CSV equals the certificate to $8.2 \times 10^{-16}$; the issue
  was opened 11 seconds after the pin’s commit; the repository’s only licence file is de
  Winter’s MIT licence.
- **Digests.** `ALL_FROZEN_DIGESTS_HOLD` and `RERUN_REPRODUCES_EVERY_RECEIPT`.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/checker-frozen-digests.txt` | the source certificate, the seven checker files and the receipts they had written | 2026-11-15T03:19:25Z |
| `frozen/controls-plan-digest.txt` | the controls plan, its facts and their programs, before `l169_controls.py` existed | 2026-11-15T03:21:48Z |
| `frozen/findings-frozen-digest.txt` | the frozen review text and the receipts at the freeze | 2026-11-15T03:28:11Z |
| `frozen/review-2026-11-15-jazivxt-989.frozen.md` | the review as frozen, before the author’s README, the record at 90 or Couzo’s checker were read | 2026-11-15T03:28:11Z |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
