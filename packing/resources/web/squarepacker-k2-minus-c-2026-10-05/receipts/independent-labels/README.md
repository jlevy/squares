# An Independent Labelling of Lemma 4.10

This directory holds a second route to the 78,673 box labels of Lemma 4.10 of Sungjoon
Ryu’s preprint, which this packet retains at version 1.1. The labels decide the constant
`0.033` and the formula for `k ≥ 10¹³`; without them the analytic Lemma 4.9 gives
`0.027`. Until this run, the labels had one implementation, the source’s
`verify_leaves2.py`, which shares the search’s cell grid, float prefilter, split rule and
float point count (findings RF-1 and RF-2 of
[the 5 October review](../../../../../../docs/project/reviews/review-2026-10-05-squarepacker-k2-minus-c.md)).

The program is
[`cases/asymptotic/ryu_k2_minus_c_labels.py`](../../../../../cases/asymptotic/ryu_k2_minus_c_labels.py).
It was written from the proof of Lemma 4.10 and the disc model of the TeX for bead
`think-k3tk`, by lane L26 of the 2 November 2026 intake (`think-3guf`). It decides every
box again without the source’s programs.

**Result.** All 78,673 boxes are certified as labelled: 72,174 `inf`, 1,094 `nowall`
and 5,405 `closed`, and the largest bound of a `closed` piece is 9. None needed another
label, and none failed. The run took 1,880.8 CPU seconds on two cores, 16 minutes of
wall time. Four negative controls are refused, each with an exactly checked witness that
its claim is false.

Version 1.2’s Lemma 4.10 states the same model and decides the same 13 lists. Its
`data/kw9_data.zip` has the same SHA-256, `32634874…`, in both packets’ acquisition
manifests. The text of the lemma differs only in the side condition `k ≥ 4`, an argument
for the arc `(2π̃, 2π)`, and a longer description of the source’s float count. So this
run decides version 1.2’s labels too.

## What Its Authors Read

This list is the independence record of
[`V-ryu-k2-minus-c-independent-labels`](../../../../../frontier/verifiers.yaml).

| Read | What it gave |
| --- | --- |
| `paper/paper.tex` of version 1.1: Sections 3 and 4, from the elementary geometry through Lemma 4.10, Remark 4.11 and the slit lemma | The model and the proof the program implements |
| Version 1.2’s Lemma 4.10, compared with version 1.1’s | That the model is unchanged |
| The format of the 13 box lists in `data/kw9_data.zip`, and the names of the zip’s other files | The input: `kind`, `U`, `box` as `[r_lo, r_hi, θ_lo, θ_hi]` per centre, and `h` with a side |
| [The 5 October review](../../../../../../docs/project/reviews/review-2026-10-05-squarepacker-k2-minus-c.md), in full | The reduction to `U(I)`, re-derived there, and a prose account of the source’s checker: 1,440 cells closed against their neighbours, the greedy count, the `2π` extension, Arb at 96 bits |
| This packet’s [README](../../README.md), and one line of a control receipt, to see the receipt format | The replay’s totals, which no decision here uses |
| The docstring of `cases/asymptotic/ryu_k2_minus_c_float_gap.py` | A description of the source’s float count; nothing of it is used |
| The rows of `frontier/asymptotic-waste-bounds.yaml` for Ryu’s preprints, and the bead | The task |

**Never read or run:** `code/verify_leaves.py`, `code/verify_leaves2.py`, `code/bnb.py`,
`code/bnb_wall.py`, `code/coverage_check.py`, `code/coverage_independent/`,
`code/SUPERSEDED.md`, `code/experiments/` and every other program of the source, the
author’s verification and coverage outputs, and the body of
`ryu_k2_minus_c_float_gap.py`. The program imports NumPy, mpmath’s interval context, the
standard library, and `devtools.retained_data` to write its receipts. It does not use
python-flint.

The authors are a Claude agent, of the system family the source says helped write its
programs. The prompt and the code are separate from the source’s, so the two readings of
the proof are separate readings by one family.

## The Model

The proof fixes `d = 10⁻⁴` and puts the uncovered point at `p = 0`. Then
`Λ = d + √2`, `ρ₁ = √((d + √2/2)² + 1/4)` and `γ₀ = arccos(1 − 1/(2Λ²))`. A box gives
each of `n ≤ 5` inner centres `cᵢ = rᵢ(cos ϑᵢ, sin ϑᵢ)` an interval of `rᵢ` and of `ϑᵢ`.
With a side, the side is the line `y = −h`, and `h` has an interval too.

- **Admissible.** `|cᵢ − cⱼ| ≥ 1` for every pair and, with a side, `cᵢ,y + h ≥ 1/2`.
- **`E_II`.** The pairs closer than `Λ`.
- **`W_I`.** The centres that may have a side edge: `|cᵢ,x| ≤ 1/2`, `cᵢ,y ≥ 0` and
  `cᵢ,y + h < d + √2/2`.
- **`Dᵢ*`.** The largest number of directions, pairwise at least `γ₀` apart, in which an
  outer centre `x = cᵢ + t·u` may lie. Here `1 ≤ t < Λ`, `|x| > ρ₁`, `p` lies in
  `R(cᵢ, x)` (`cᵢ·u ≤ 0` and `|cᵢ × u| ≤ 1/2`), `|x − cⱼ| ≥ 1` for every other inner
  centre, and, with a side, `x_y ≥ −h + 1/2`.

A box is `inf` when no configuration in it is admissible, `nowall` when no admissible
one has a possible side edge, and `closed` when `E_II + W_I + Σ Dᵢ* ≤ 9` throughout.
An upper angle end at the binary64 value of `2π` is extended to the next binary64
number, which lies above `2π`, as the proof extends it to `2π`.

## How It Decides

| Step | The source’s checker, as the TeX and the review describe it | This program |
| --- | --- | --- |
| Arithmetic | Arb balls at 96 bits, through python-flint | Binary64, every basic operation rounded outward by one ulp; transcendental values from mpmath intervals at 200 bits, rounded outward |
| Directions | 1,440 fixed arcs of 0.25°, each closed against the next | Dyadic cells of `2⁻ᴸ` turn, `L` from 5 to 13; a kept cell is split at the next level |
| Discarding a direction | For each of six radial intervals, up to 16 sub-pieces, one condition fails | Each condition is a quadratic or linear inequality in `t`. The `t` where it can hold is the complement of an open interval between two roots, rounded inward, and the cell is discarded when those intervals cover `[1, Λ]` |
| Point count | Double precision, `γ₀` lowered by `10⁻¹²` | Exact integers in units of `2⁻⁶⁴` turn, with a separation `g` below `γ₀/(2π)`. A cosine inequality on intervals certifies that bound |
| Bisection | The search’s split rule | The widest side, with an angle weighted by its largest radius |
| Prefilter | A float mask proposes the cells | None |

The count is exact because the kept cells have dyadic end points and `g` is rational.
It is the greedy count from the start of each maximal run of cells, with the closing
condition. The proof of Lemma 4.10 shows that this greedy count is the maximum. A full
circle gives `⌊1/g⌋ = 8`.

A box is **certified as labelled** when every piece of its bisection is decided by its
own label. An `inf` piece also counts inside a `closed` or `nowall` box, since an
inadmissible piece needs no bound. A box is cut into at most 4,096 pieces. A box not
certified as labelled is tried with every label. It is **certified otherwise** if that
succeeds, and **not certified** if it does not.

## The Price

The brief capped the run at 40 CPU-hours and asked for a price first. A seeded random
sample of 500 boxes (seed 20261102) took 14.4 CPU seconds on one core, 12.7 of them in
the boxes, and
extrapolates, class by class, to 0.54 CPU-hours for all 78,673
([`price-500.json`](price-500.json), [rows](price-500-rows.jsonl),
[receipt](price-500.log)). Every sampled box was certified as labelled.

## The Run

Two workers ran at once on a four-core host shared with other lanes, each under
`nice -n 10` and `devtools.replay_receipt`, at commit `0f3a027f5`, from 08:22:42Z to
08:38:57Z on 2 November 2026 ([worker 0](run-worker0.log), [worker 1](run-worker1.log)).
Worker `w` decided the boxes whose global index is `w` modulo 2: 39,337 boxes in 960.2
CPU seconds, and 39,336 in 920.6. `summarize` gathered their rows into
[`summary.json`](summary.json) and `labels/` ([receipt](summarize.log)). It refuses a
run that misses a box or decides one twice, and a row whose label or bound differs from
its list’s.

| Label | Boxes | Certified as labelled | Certified otherwise | Not certified |
| --- | ---: | ---: | ---: | ---: |
| `inf` | 72,174 | 72,174 | 0 | 0 |
| `nowall` | 1,094 | 1,094 | 0 | 0 |
| `closed` | 5,405 | 5,405 | 0 | 0 |

A row counts every piece examined, the box included, so a box bisected `k` times examines
`2k + 1` pieces.

- **`inf`.** 71,910 boxes are decided in one piece. The other 264 are bisected, and every
  piece is inadmissible.
- **`nowall`.** All 1,094 are decided in one piece: 613 with no possible side edge, and
  481 with no admissible configuration at all.
- **`closed`.** 1,655 boxes are decided in one piece and 3,750 are bisected. 604 are
  decided by `closed` pieces alone, 2,190 by `closed` and `inf` pieces, and 2,611 by
  pieces that are all inadmissible, so the label holds on them vacuously. Of the 2,794
  boxes with a `closed` piece, the largest bound is 9 for 2,576, 8 for 199, 7 for 15, 6
  for 3 and 5 for 1. That bound is the first one at most 9 that the grid reaches, not the
  least, so it is not compared with the source’s `U`.
- **Bisection.** The run made 42,939 bisections; the source’s checker reports 59,238 of
  its own. No box came near the budget: the most pieces examined were 491
  (`bnb_n4_T9_1of2` line 2304), and the slowest box took 11.9 CPU seconds (line 3186 of
  the same list).
- **The direction grid.** The boxes with a `closed` piece used levels 5 to 13, and 139 of
  them needed the finest, `2⁻¹³` turn.

## Soundness Checks

These are diagnostics. They test the program; they decide no label.

- **Sampled `U(I)`.** Before the run, a scratch probe drew random admissible points of
  `closed` boxes and estimated `U(I)` at each by float sampling of 7,200 directions and
  80 radii. At 1,131 points, from two seeds, the estimate never exceeded the program’s
  finest rigorous bound on the point box. The two were equal at many points, so the
  bound is tight there. The probe decides nothing. Its kept form is a test of
  `tests/test_ryu_k2_minus_c_labels.py`, with margins that let float sampling only
  undercount.
- **The slit configuration** `c₁,₂ = ±(1/2 + 10⁻⁹, 0)`. The sampled `U(I)` is 9, and the
  program’s bound on the point box is 9 at every level of the direction grid.
- **The bounds never increase** from one level of the grid to the next, at every point
  checked.

## Controls

The `controls` command runs four, under the run’s rules and its budget of 4,096 pieces,
at commit `4fd07e1b3` ([`controls.json`](controls.json), [receipt](controls.log), 45.9 CPU
seconds). Each perturbs one bound of a box or one weight of the count so that its claim is
false. A rational witness, checked in exact arithmetic, shows the claim is false: a
configuration in the perturbed box that is admissible and, where the claim is a bound,
whose `U(I)` exceeds it. A witness bounds `Dᵢ*` from below by outer centres whose
conditions and pairwise separations are checked exactly. Each unperturbed box is certified.

| Control | Perturbed claim | Refused | Witness | Unperturbed |
| --- | --- | --- | --- | --- |
| A | The sharp box, `bnb_n2_T9_0of1` line 24, at threshold 8 | Budget spent, 4,071 pieces | The slit configuration `±(1/2 + 10⁻⁹, 0)`: `E_II ≥ 1` and `D₁*, D₂* ≥ 4`, so `U(I) ≥ 9` | Certified at 9 in one piece |
| B | `bnb_n2_T9_0of1` line 1, `inf`, with the lower end of `ϑ₂` lowered from `7π/4` to `3π/2` | A piece too small to cut stays undecided | `c₁ = (4/5, 0)` and `c₂ = (16/101, −396/505)`: admissible, in the widened box and not in the original | `inf` in one piece |
| C | `bnbw_n2_T9_0of1` line 290, `nowall`, with the lower end of `h` lowered from 0.3536 to 0 | Budget spent, 4,011 pieces | `c₁ = (−53/100, 13/20)`, `c₂ = (47/100, 13/25)` and `h = 1/25`: admissible, and `c₂` may have a side edge | `nowall` in one piece |
| D | The sharp box with the separation of the count halved to `γ₀/2` | A piece too small to cut stays undecided | The slit configuration with six directions per centre, pairwise `γ₀/2` apart, so `U(I) ≥ 13` | Certified at 9 in one piece |

Control A is the one the replay ran with the source’s checker; B, C and D are new. Control
D tests the point count, the step finding RF-2 is about: with the separation halved, the
count rises and the box is refused.

## Files

| File | What it holds |
| --- | --- |
| [`price-500.json`](price-500.json), [`price-500-rows.jsonl`](price-500-rows.jsonl), [`price-500.log`](price-500.log) | The price: the sample’s totals, one row per sampled box, and the receipt |
| [`run-worker0.log`](run-worker0.log), [`run-worker1.log`](run-worker1.log) | The two workers’ receipts, from `devtools.replay_receipt` |
| [`summary.json`](summary.json), [`summarize.log`](summarize.log) | The counts per class and outcome, every box not certified as labelled (none), the bounds, levels and pieces, and the CPU; and the receipt |
| `labels/<list>.jsonl` | One row per box, in line order: the source’s label and bound, the outcome, the pieces, the label of each leaf, the largest `closed` bound, the finest level and the CPU. The nine lists of more than 1,000 boxes are stored as `.jsonl.gz` |
| [`controls.json`](controls.json), [`controls.log`](controls.log) | The four controls and their receipt |

## Reproduce

From `packing/`, with the project interpreter. Each worker decides the boxes whose
global index has its residue. A worker that stops resumes from the rows already written.

```bash
P=resources/web/squarepacker-k2-minus-c-2026-10-05/receipts/independent-labels
.venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels price --sample 500 --receipts $P
for w in 0 1; do
  .venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels run --out OUT --worker $w --workers 2 &
done; wait
.venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels summarize --out OUT --receipts $P
.venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels controls --receipts $P
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
