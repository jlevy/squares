# Addendum on #997: Programs, Frozen Files and Receipts

This directory keeps the programs and receipts of lane L182’s addendum to lane L180’s
stage 4 review of issue [#996](https://github.com/jlevy/squares/issues/996): the
replacement certificate of issue [#997](https://github.com/jlevy/squares/issues/997),
Joost de Winter’s $s(90) \le 9.994038766610$. The addendum is the last section of
[`docs/project/reviews/review-2026-11-15-de-winter-996.md`](../../../../../docs/project/reviews/review-2026-11-15-de-winter-996.md).

The sources are files of
[JoostdeWinter/square-packing](https://github.com/JoostdeWinter/square-packing) at
`fa53fb0d734fbf438bcfb73c1434a15894bb2bc5`, not retained here.
The same two blobs are at the head `6c0ad56a1334`. This directory is review-only.

| File | SHA-256 |
| --- | --- |
| `n90/n90_exact.json` | `85840c5563e023790ae32af68c62d636e041a7d34f01c0f772979450dd188a2a` |
| `n90/n90_witness.yaml` | `c9aa917fa0abc9bfe4ddfdd73ec391b20e474fb0c5c97252a7819ad7152c1628` |

The author’s `SHA256SUMS` at the head states both, and six more files, and they hold.
#996’s certificate (`64d5ee7`, `3adcc363…` and `3a28f570…`) is read for the comparison
from the same clone.

## Layout

- `programs/`: the addendum’s programs, its controls plan, the issue as fetched.
- `frozen/`: the plan’s digest list, written before any control ran, and the addendum’s
  digest list, written last.
- `out/`: the receipts.

L180’s programs in `../programs/` are used unchanged: their digests are checked against
L180’s three frozen lists before each use and again by `l182_digests.py`.

## Programs

The L182 programs are the addendum’s own.
They import nothing from this repository or the source, and they reuse L180’s modules,
unchanged, by importing them from `../programs/`.

| Program | Decides | Reads | Writes |
| --- | --- | --- | --- |
| `l182_plan_facts.py` | nothing: runs `l180_plan_facts.py` unchanged, then replaces the six S1 fields that depend on #996’s claim and floor, constants in that program, with #997’s | the certificate, its twin, the check receipt | `out/plan-facts-n90-997.json`, and L180’s unchanged output in scratch |
| `l182_make_plan.py` | nothing: runs `l180_make_plan.py` unchanged, re-targets the three texts that print #996’s values and G5’s premise, checks the preconditions L180’s texts assert, and records how each control differs from L180’s plan | the check receipt, the plan facts, L180’s `controls-plan.json` | `programs/controls-plan-997.json` |
| `l182_compare.py` | nothing: #997 against #996 square by square (moves, turns), wall by wall, pair by pair | both JSON files, both check receipts | `out/compare-997-996.json` |
| `l182_sides.py` | nothing: the claim’s arithmetic, the step from #996, the gain on T-303, both against the contraction margins; closed forms, L steps, monotonicity | both JSON files, the description, `packing/frontier/n-*.md`, the house witness, three contraction receipts | `out/sides-997.json` |
| `l182_digests.py` | every frozen digest of L180’s and of this addendum, a rerun of the addendum’s chain against the kept receipts, the digest of every file here | L180’s packet, this directory, both certificates | `out/addendum-digests.json` |

`programs/issue-997.json` is the issue as fetched at 13:06:57Z, trimmed as L180 trimmed
#996.

From `packing/`, with `S7` the clone checked out at `fa53fb0`, `S6` a directory holding
#996’s two files from `64d5ee7`, `R` L180’s packet, `A` this directory and `X` a scratch
directory:

```bash
PY="nice -n 19 uv run --frozen --all-extras --group dev python -I -B"
PB="nice -n 19 uv run --frozen --all-extras --group dev python -B"
DT="$PB -m"
J=$S7/n90/n90_exact.json
T=$S7/n90/n90_witness.yaml
J6=$S6/n90_exact.json
JS=85840c5563e023790ae32af68c62d636e041a7d34f01c0f772979450dd188a2a
TS=c9aa917fa0abc9bfe4ddfdd73ec391b20e474fb0c5c97252a7819ad7152c1628
HOUSE="T-303=witness-center-basis:witnesses/known-best/n-090.yaml"
# before the plan
$PY $R/programs/l180_selftest.py $A/out/selftest.json
$PY $R/programs/l180_check.py $J $JS $T $TS $A/out/check-n90-997.json
$PY $A/programs/l182_plan_facts.py $J $T $A/out/check-n90-997.json $X/plan-facts-l180-rules.json \
  $A/out/plan-facts-n90-997.json
$PY $A/programs/l182_make_plan.py $A/out/check-n90-997.json $A/out/plan-facts-n90-997.json \
  $R/programs/controls-plan.json $X/controls-plan-l180-rules.json $A/programs/controls-plan-997.json
# the plan hashed into frozen/controls-plan-digest.txt and pushed; then
$PY $R/programs/l180_controls.py $J $T $A/programs/controls-plan-997.json $A/out/plan-facts-n90-997.json \
  $A/out/check-n90-997.json $A/out/controls-n90-997.json
$PY $R/programs/l180_describe.py $J $A/out/check-n90-997.json $A/out/describe-n90-997.json
$DT devtools.contraction_margin --n 90 "$HOUSE" --against "#997=center-direction-json:$J" \
  --out $A/out/contraction-t303-house-n90-997.json
$DT devtools.contraction_margin --n 90 "#997=center-direction-json:$J" --out $A/out/contraction-new-n90-997.json
$DT devtools.contraction_margin --n 90 "#996=center-direction-json:$J6" --against "#997=center-direction-json:$J" \
  --out $A/out/contraction-996-against-997.json
$DT devtools.measure_identity --n 90 "#997=center-direction-json:$J" "#996=center-direction-json:$J6" "$HOUSE" \
  "grid=binary64-xyd:$R/out/grid-n90.txt" --out $A/out/identity-n90-997.json
$PY $A/programs/l182_compare.py $J $J6 $A/out/check-n90-997.json $R/out/check-n90.json $A/out/compare-997-996.json
$PY $A/programs/l182_sides.py $J $J6 $A/out/describe-n90-997.json frontier witnesses/known-best/n-090.yaml \
  $A/out/contraction-t303-house-n90-997.json $A/out/contraction-new-n90-997.json \
  $A/out/contraction-996-against-997.json $A/out/sides-997.json
$PY $R/programs/l180_lineage.py $J witnesses/known-best/n-090.yaml $A/out/lineage-n90-997.json
$PB $R/programs/l180_witness_read.py $J $T $X/n90_witness-997-adapter-order.yaml $A/out/witness-read-997.json
$PY $R/programs/l180_custody.py $S7 fa53fb0d734fbf438bcfb73c1434a15894bb2bc5 \
  6c0ad56a13346abda6debd73afab7892072896c7 $A/programs/issue-997.json $A/out/custody-997.json
$PY $A/programs/l182_digests.py $A $S7/n90 $S6 frontier witnesses/known-best/n-090.yaml $X/rerun \
  $A/out/addendum-digests.json
```

The devtools and `l180_witness_read.py` run with `python -B`, not `-I`, so that
`devtools` and `sqpack` import from `packing/`; they are this repository’s own, run
read-only, writing only here.

## What They Printed

- `l180_selftest.py`: `PASSED 31771 cases 0 failed`; the three broken copies fail 640,
  1,408 and 1,472.
- `l180_check.py`: `ACCEPT`. The twin agrees, every square listed counterclockwise from
  $C + (u + v)/2$; 4,005 pairs apart by both methods, least margin
  $2.02641179076 \times 10^{-12}$ at (2, 40); 17 wall contacts, eight at the left and
  nine at the bottom; least right and top clearance $2.51389952000 \times 10^{-22}$.
- `l182_plan_facts.py`: the closed form’s exact lists equal method A’s; G5 at square 10
  (bottom); 54 pairs overlapping with every $(c, s)$ read as $(c, -s)$; S4 the pair (2,
  40), square 40 moving; the claim the side’s 12-place ceiling.
- `l182_make_plan.py`: 26 controls; re-targeted by hand G5a, G7b, S1e and S1f; every
  precondition holds.
- `l180_controls.py`: `EVERY_CONTROL_AS_STATED`, 26 of 26.
- `l180_describe.py`: 50 squares exactly upright, 40 turned clockwise by 22.90° to
  30.99°; 197 pairs from $2.026 \times 10^{-12}$ to $4.041 \times 10^{-12}$, the next at
  $9.47 \times 10^{-6}$; the width $S - 2.51389952000 \times 10^{-22}$.
- Contraction: T-303 $1.098813 \times 10^{-11}$ (unchanged), the gain `within_margin:
  false`; #997 $1.818734 \times 10^{-11}$, first contact (2, 40); #996
  $9.532970 \times 10^{-12}$, the step to #997 9,539 times it, `within_margin: false`.
- `devtools.measure_identity`: against #996, square $k$ to square $k$ under the
  identity, nearest centres one to one, largest move 0.0142, none beyond 0.1; against
  T-303 the identity, six beyond 0.1, largest 0.645.
- `l182_compare.py`, `l182_sides.py`, `l180_lineage.py`, `l180_witness_read.py`,
  `l180_custody.py`: as the addendum reports them.
- `l182_digests.py`: `ALL_FROZEN_DIGESTS_HOLD` (47 digests, L180’s 27) and
  `RERUN_REPRODUCES_EVERY_RECEIPT`.

## Frozen Files

| File | What it fixes | When |
| --- | --- | --- |
| `frozen/controls-plan-digest.txt` | the source files, L180’s programs used unchanged, L182’s plan programs, the self-test and check receipts, the plan facts and the plan, before `l180_controls.py` ran | 2026-11-15T13:03:56Z, pushed as `c670153b9` |
| `frozen/addendum-frozen-digests.txt` | the source files and every file under `programs/`, `out/` and `frozen/` here, this README and the list itself aside | 2026-11-15T13:18:44Z, before the addendum’s commit |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
