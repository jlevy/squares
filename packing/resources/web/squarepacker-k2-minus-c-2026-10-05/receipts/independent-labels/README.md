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
wall time. Ten negative controls are refused, each with an exactly checked witness, in
the claim’s box, that its claim is false. After
[review A of #884](https://github.com/jlevy/squares/pull/884#pullrequestreview-5734935204),
a seeded sample of 1,000 boxes was decided again, and every row came out identical.

Version 1.2’s Lemma 4.10 states the same model and decides the same 13 lists. Its
`data/kw9_data.zip` has the same SHA-256, `32634874…`, in both packets’ acquisition
manifests. The text of the lemma differs in the side condition `k ≥ 4`, an argument for
the arc `(2π̃, 2π)`, longer descriptions of the source’s float count and of the coverage
checks, and a mention of this project’s replay; the model is the same. So this run
decides version 1.2’s labels too.

## What Its Authors Read

This list is the independence record of
[`V-ryu-k2-minus-c-independent-labels`](../../../../../frontier/verifiers.yaml).

| Read | What it gave |
| --- | --- |
| `paper/paper.tex` of version 1.1: Sections 3 and 4, from the elementary geometry through Lemma 4.10, Remark 4.11 and the slit lemma | The model and the proof the program implements |
| Version 1.2’s Lemma 4.10, compared with version 1.1’s | That the model is unchanged |
| The format of the 13 box lists in `data/kw9_data.zip`, and the names of the zip’s other files | The input: `kind`, `U`, `box` as `[r_lo, r_hi, θ_lo, θ_hi]` per centre, and `h` with a side |
| [The 5 October review](../../../../../../docs/project/reviews/review-2026-10-05-squarepacker-k2-minus-c.md), in full | The reduction to `U(I)`, re-derived there, and an account of the source’s checker at the level of its code: the routines `certified_violation`, `check_inf` and `check_nowall`; `max_points` (`bnb.py` lines 99–123), its greedy count and closing test; 1,440 cells closed against their neighbours; six radial pieces of up to 16 sub-pieces; the tolerances, the `2π` extension, and Arb at 96 bits |
| This packet’s [README](../../README.md), and one line of a control receipt, to see the receipt format | The replay’s totals, which no decision here uses |
| The docstring of `cases/asymptotic/ryu_k2_minus_c_float_gap.py` | A description of the source’s float count; nothing of it is used |
| The rows of `frontier/asymptotic-waste-bounds.yaml` for Ryu’s preprints, the bead, `epistemics.md` and the stage 4 rules of `campaign/result-import.md` | The task, and how to record it |
| The lines that name `think-k3tk` in the 2 November review of the quarter-power and cube-root preprints (its F3), in `campaign/result-requests.yaml` and in three later packets’ READMEs | What this run bears on |
| [Review A of #884](https://github.com/jlevy/squares/pull/884#pullrequestreview-5734935204) and its scripts `mutants.py` and `mycontrols.py`, after the run | Six mutants of this program, controls E and F, and the findings this README answers. The reviewer’s own checker, `indep.py`, was not read |

**Never read or run:** `code/verify_leaves.py`, `code/verify_leaves2.py`, `code/bnb.py`,
`code/bnb_wall.py`, `code/coverage_check.py`, `code/coverage_independent/`,
`code/SUPERSEDED.md`, `code/experiments/` and every other program of the source, the
author’s verification and coverage outputs, and the body of
`ryu_k2_minus_c_float_gap.py`. The program imports NumPy, mpmath’s interval context, the
standard library, and `devtools.retained_data` to write and read its receipts. It does
not use python-flint.

The record keeps `clean_room: true`, since no program of the source was read. Its `read`
list includes `specification`, because the 5 October review describes the source’s
checker at the level of its code, so this second reading was not made wholly without the
first. Whether to record `clean_room: false` instead is the owner’s call.

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
inadmissible piece needs no bound. A box may have at most 4,096 pieces examined or
waiting. A box not certified as labelled is tried with every label. It is **certified otherwise** if that
succeeds, and **not certified** if it does not.

## The Price

The brief capped the run at 40 CPU-hours and asked for a price first. A seeded random
sample of 500 boxes (seed 20261102) took 14.4 CPU seconds on one core, 12.7 of them in
the boxes themselves. Class by class, that extrapolates to 0.54 CPU-hours for all 78,673
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

The `controls` command runs ten, under the run’s rules and its budget of 4,096 pieces, at
commit `231af6b4e` ([`controls.json`](controls.json), [receipt](controls.log), 9.0 CPU
seconds). Each claim is false. A rational witness, checked in exact arithmetic, shows
it: a configuration in the claim’s box that is admissible, lies in the lemma’s domain
`1/2 < |cᵢ| ≤ ρ₁` and, where the claim is a bound, has `U(I)` above it. A witness bounds
`Dᵢ*` from below by outer centres `x = cᵢ + w` whose conditions and pairwise separations
are checked exactly. The unperturbed claim beside each is certified, in one piece.

Each claim is refused by decision, not by the budget. `certify` takes the witness, in
binary64, as a focus, and of each piece it cuts it decides first the half that holds the
witness. The claim is refused when the piece holding the witness cannot be cut further,
with its widest side at most `10⁻¹³`, and is still undecided. A labeller that is sound
cannot decide that piece, however long it runs. The focus only orders the bisection, and
the run used none.

| Control | Claim that should fail | Refused after | Witness | Unperturbed |
| --- | --- | ---: | --- | --- |
| A | The sharp box, `bnb_n2_T9_0of1` line 24, at threshold 8 | 122 pieces | The slit configuration `±(1/2 + 10⁻⁹, 0)`: `E_II ≥ 1` and `D₁*, D₂* ≥ 4`, so `U(I) ≥ 9` | Certified at 9 |
| B | `bnb_n2_T9_0of1` line 1, `inf`, with the lower end of `ϑ₂` lowered from `7π/4` to `3π/2` | 129 | `c₁ = (4/5, 0)` and `c₂ = (16/101, −396/505)`: admissible, in the widened box and not in the original | `inf` |
| C | `bnbw_n2_T9_0of1` line 290, `nowall`, with the lower end of `h` lowered from 0.3536 to 0 | 212 | `c₁ = (−53/100, 13/20)`, `c₂ = (47/100, 13/25)` and `h = 1/25`: admissible, and `c₂` may have a side edge | `nowall` |
| D | The sharp box with the separation of the count halved to `γ₀/2` | 122 | The slit configuration with six directions per centre, pairwise `γ₀/2` apart, so `U(I) ≥ 13` | Certified at 9 |
| E | The sharp box’s neighbour, `bnb_n2_T9_0of1` line 32, at threshold 8 (review A) | 122 | `c₁ = (1/2 + 10⁻⁹, 0)` and `c₂ = (−1/2 − 10⁻⁹, 10⁻¹²)`: `U(I) ≥ 9` | Certified at 9 |
| F | `bnbw_n2_T9_0of1` line 4, `inf` through the side, with the lower end of `ϑ₂` lowered from `3π/2` to 3.5 (review A) | 212 | `c₁ = (4/5, −1/100)`, `c₂ = (−1/2, −1/5)` and `h = 141/200`: admissible, in the widened box and not in the original | `inf` |
| G | `E_II`’s `Λ`: about `c₁,₂ = (∓1413/2000, 9/20)` and `h = 1/10`, at threshold 0 | 56 | The pair is `1.413 < Λ` apart, so `E_II ≥ 1` | Certified at 1 |
| H | `W_I`’s `d + √2/2`: about `c₁ = (−1/20, 3/5)` and `h = 21/200`, at threshold 0 | 34 | `c₁,y + h = 0.705 < d + √2/2`, so `W_I ≥ 1` | Certified at 1 |
| I | The outer centres’ side condition: about `c₁ = (297/500, 137/250)` and `h = 39/250`, at threshold 0 | 34 | `w = (−7/5, −11/100)` gives an outer centre with `x_y + h = 0.594 ≥ 1/2`, so `D₁* ≥ 1` | Certified at 1 |
| J | `ρ₁`, the distance from `p` an outer centre must exceed: about `c₁ = (72/125, 0)`, with no side, at threshold 2 | 12 | Three outer centres, pairwise at least `γ₀` apart, one of them at squared distance 0.790 from `p`, beyond `ρ₁² = 0.750`, so `D₁* ≥ 3` | Certified at 3 |

Control A is the one the replay ran with the source’s checker; the others are new. D tests
the point count, the step finding RF-2 is about: with the separation halved, the count
rises and the box is refused. E and F are review A’s. G to J are each a box of half-width
`10⁻¹⁰` about a configuration at which the program’s bound is exact, at a claim one
below it. Each sits on one threshold of the model, and a labeller that moved that
threshold the permissive way would certify the claim.

Review A made six permissive mutants of this program. Under M1 to M4, controls A to D
were still refused, and only a sampled test caught them; G to J were added for those
four. The review’s script, run at commit `61f959a0c`, gives this. A control catches a
mutant when the mutant certifies its claim; with no mutant, all ten are refused.

| Mutant | Change | Caught by |
| --- | --- | --- |
| M1 | The outer centres’ side condition `x_y ≥ −h + 1/2` made 0.2 too strict | I |
| M2 | `W_I`’s distance `d + √2/2` shortened by 0.1 | H |
| M3 | `E_II`’s threshold lowered to `Λ² − 0.3` | G |
| M4 | The distance `ρ₁` from `p` an outer centre must exceed: its squared value raised by 0.05 in the hole in `t` | J |
| M5 | A piece inadmissible when a pair may be closer than 1 | A to F |
| M6 | The rectangle’s half-width narrowed to 0.45 | A, D, E, I and J |

A test of `tests/test_ryu_k2_minus_c_labels.py` keeps the check for M1 to M4.

## After Review A

Review A’s fixes add guards and the focus, and change no decision of the run. The
program now refuses to start unless binary64 rounds to nearest with gradual underflow,
which the one-ulp enclosure needs. It refuses a radius that reaches 1, an mpmath special
value, a direction cell coarser than level 2 and a separation above half a turn. With
no focus, `certify` cuts in the run’s order.

The `recheck` command decided a seeded sample of 1,000 boxes again (seed 884), at commit
`231af6b4e`, and compared each decision with its row in `labels/`
([`recheck-1000.json`](recheck-1000.json), [receipt](recheck-1000.log), 46.5 CPU
seconds). All 1,000 are identical in label, `U`, outcome, pieces, leaves, bound and
level. The sample holds 915 `inf` boxes, 4 of them bisected; 18 `nowall`; and 67
`closed`, 48 of them bisected.

## Files

| File | What it holds |
| --- | --- |
| [`price-500.json`](price-500.json), [`price-500-rows.jsonl`](price-500-rows.jsonl), [`price-500.log`](price-500.log) | The price: the sample’s totals, one row per sampled box, and the receipt |
| [`run-worker0.log`](run-worker0.log), [`run-worker1.log`](run-worker1.log) | The two workers’ receipts, from `devtools.replay_receipt` |
| [`summary.json`](summary.json), [`summarize.log`](summarize.log) | The counts per class and outcome, every box not certified as labelled (none), the bounds, levels and pieces, and the CPU; and the receipt |
| `labels/<list>.jsonl` | One row per box, in line order: the source’s label and bound, the outcome, the pieces, the label of each leaf, the largest `closed` bound, the finest level and the CPU. The nine lists of more than 1,000 boxes are stored as `.jsonl.gz` |
| [`controls.json`](controls.json), [`controls.log`](controls.log) | The ten controls and their receipt |
| [`recheck-1000.json`](recheck-1000.json), [`recheck-1000.log`](recheck-1000.log) | The sample decided again after review A, and its receipt |

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
.venv/bin/python3 -m cases.asymptotic.ryu_k2_minus_c_labels recheck --sample 1000 --seed 884 --receipts $P
```

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
