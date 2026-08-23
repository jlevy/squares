# Synopsis: The `s(n)` Program

**Date:** 2026-08-23 (last updated 2026-08-23)

**Status:** Living document, revised whenever a result lands.

**Owns:** The single technical account of what this project knows, how it knows it, and
what it is doing next.
Everything below is either derived from a schema-validated artifact in this directory or
reproducible by a command given in the text.

> This document is the root.
> It states results and points at the artifact that carries the detail; it does not
> restate the detail. Where a number appears here it also appears in a validated
> artifact, and the artifact is authoritative.

## Overview

`s(n)` is the side of the smallest square that contains `n` non-overlapping unit
squares, which may be rotated freely.
The motivating case is `n = 11`: the smallest instance nobody has solved, and the
smallest open gap at `n ≤ 100`.

This project has three lanes, in the order they were built:

1. **Know the frontier.** A schema-validated record of the best known packing and the
   best proved lower bound for every `n ≤ 100`, with provenance, plus a local archive of
   the primary literature.
2. **Verify exactly.** A separating-axis verifier that decides validity over the
   packing’s own algebraic number field, so a configuration with contacts at *exactly*
   zero separation can be certified rather than guessed at.
3. **Search, under an experiment contract.** A hypothesis registry with kill criteria
   written before the run, a metric vector, an accept rule, and a ledger generated from
   the artifacts rather than typed.

The strategy that organises lane 3 is stated in
[A Search Philosophy for Square Packing](docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md):
**the map of the local optima is the deliverable, and records are corollaries.** The
argument for it, and the measurement registered to kill it if it is wrong, are in
[Theoretical Results](#theoretical-results) and
[The Hypothesis Registry](#the-hypothesis-registry) below.

### Document map

Each document owns one thing.
Nothing here duplicates what another owns.

| Document | Owns |
| --- | --- |
| **This synopsis** | The state of the program: results, their status, the roll-up of rounds |
| [`README.md`](README.md) | What is in the directory, and how to run the verifier |
| [`conventions.md`](conventions.md) | Every rule the directory runs on, and which are machine-checked |
| [`frontier/`](frontier/README.md) | What is known about `s(n)` for every `n ≤ 100`, one artifact per case |
| [`resources/`](resources/README.md) | The primary literature, local and greppable |
| [Packing 11 Unit Squares](docs/project/research/research-2026-08-22-packing-11-unit-squares.md) | The mathematics of `s(11)`: what is proved, what is conjectured, why the proof technique stalls |
| [Algorithms and Tooling](docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md) | How packings are found, refined to exact form, and verified |
| [FrankenSim as a Rust Toolkit](docs/project/research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md) | First-hand study of one Rust framework as a source of parts |
| [Infrastructure for Packing Exploration](docs/project/research/research-2026-08-22-infrastructure-for-packing-exploration.md) | The build order, the language boundary, what not to build |
| [Lean for Packing Proofs](docs/project/research/research-2026-08-22-lean-for-packing-proofs-and-validation.md) | Where a proof assistant fits, and what it would be pointed at first |
| [A Search Philosophy](docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md) | The strategy layer: why pointing should beat scaling |
| [Standing review](docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md) | The experimental method, and the register `H-001`–`H-015` in prose |
| [Plan spec](docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md) | The seven build phases and their bead tree |
| [Campaign runbook](campaign/README.md) | The contract every round runs under, frozen while rounds run |
| [Idea board](campaign/ideas.md) | The whole idea space on one page, including dead ends |
| [Ledger](campaign/ledger.md) | Generated roll-up of series, registry and rounds |

## The Problem

A **packing** of `n` unit squares in a container square of side `s` is a placement of
the `n` squares, each free to translate and rotate, whose interiors are pairwise
disjoint and which all lie inside the container.
`s(n)` is the infimum of the `s` for which one exists.
Touching is allowed, and in good packings it is pervasive.

For most `n` the answer is uninteresting: `s(m²) = m` by the grid.
It becomes interesting just above a perfect square, where the leftovers must be tilted
in.

At `n = 11` the two ends of the interval have barely moved in a generation:

|  | value | source |
| --- | --- | --- |
| Best known packing (upper bound) | `3.87708359002281417730789706010096…` | Walter Trump, 1979 |
| Best proved lower bound | `2 + 4/√5 = 3.788854382…` | Stromquist 2003, Theorem 2 |
| Gap | `0.088229208023` | the smallest open gap at `n ≤ 100` |

Trump’s packing is six axis-aligned squares plus a block of five tilted at
`a* ≈ 40.181937290329714°`. The container side is an algebraic number of degree 8, the
root of

```
s⁸ − 20s⁷ + 178s⁶ − 842s⁵ + 1923s⁴ − 496s³ − 6754s² + 12420s − 6865 = 0
```

lying in `[3.87, 3.88]`. The packing is **rigid**: it has no slack anywhere, which is
what makes it hard to find and, separately, what makes it hard to check.

### Why exactness is not optional

Disjoint *interiors* means touching is legal, and record packings touch a great deal.
In Trump’s packing 14 of the 55 pairs are separated by exactly zero, and 20 corner
coordinates lie exactly on the container boundary.

Floating point can certify a strict inequality.
It cannot certify an equality.
A float verifier therefore needs a tolerance to accept the true contacts, and that
tolerance is a blind spot that also accepts overlaps smaller than itself; setting it to
zero rejects the true packing instead.
Both failure modes are demonstrated by `negative_control.py`.

The fix is representational rather than numerical: express the configuration in the real
algebraic number field it actually lives in, where equality is decidable.
That is what `sqpack` does, and it is why the evidence tiers below make `exact` the only
tier permitted to say **record**.

## The Lay of the Land, by `n`

Where the program has actually spent effort, and what came of it.

| `n` | Status | Standing best | Role here | What has been done |
| --- | --- | --- | --- | --- |
| 5 | proved, `2 + ½√2` | `2.70710678…` | engine self-test | `sqsearch --selftest` recovers it on every run; the budget-binding defect was caught and measured here ([exp-001](campaign/series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md)). In the declared sweeps of H-001 and H-002 |
| 8 | proved, `3` | `3` | census kill line | The `n` at which [H-011](campaign/hypotheses/H-011-small-n-census.md)’s discovery curve must plateau, or enumeration is abandoned |
| **10** | **proved**, `3 + ½√2` | `3.70710678…` | **positive control** | Two rounds ([exp-001](campaign/series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md), [exp-002](campaign/series/series-000-smoke-and-calibration/experiments/exp-002-baseline-n10-positive-control.md)). Annealer finds the right basin and stops `4.19e-04` short: a **polish** failure. In the sweeps of H-001, H-002, H-011, H-012, and the δ- and archive-ladders |
| **11** | **open** | `3.87708359…` (Trump 1979) | **target** | Exact verification over `ℚ(u)` (**T-1**); the cell decomposition and its angle-space profile (**T-2**, **T-3**); two rounds ([exp-001](campaign/series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md), [exp-003](campaign/series/series-000-smoke-and-calibration/experiments/exp-003-baseline-n11-target.md)) landing `3.73e-02` short: an **exploration** failure |
| **12** | open; `4` believed optimal | `4` | **negative control** | Two rounds ([exp-001](campaign/series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md), [exp-004](campaign/series/series-000-smoke-and-calibration/experiments/exp-004-baseline-n12-negative-control.md)). Returns exactly `4.0` on all five seeds and never below. Also where the search and proof lanes are planned to meet |
| 17 | open | `4.67553009…` (Bidwell 1998) | mechanism-matched calibration | Registered in the standing sweep; **no rounds yet**. The nearest case whose record uses genuinely oblique structure — tilts of `0°` and `±40°` |
| 61, 78, 97 | open, `m² − 3` | `8`, `9`, `10` (grids) | opportunistic slot | The narrowest gaps in the table. An analytic Cleemann-style attempt at `arctan(3/4)` is registered and **not yet made** |
| 1–100 | 35 proved, 65 open | — | the corpus | One schema-validated artifact per case in [`frontier/`](frontier/README.md), with provenance; 63 of the 65 open cases are bounded below by Nagamochi’s general theorem |

Two facts about this table drive the whole strategy.

**Every proved case in the calibration ladder is a 45° mechanism.** `n = 5` and `n = 10`
are both symmetric arrangements that blind search reaches without help.
`n = 11` needs an oblique core locked at an irrational angle, which **no proved case
exercises**. An engine can pass the ladder and remain structurally blind to what the
target demands, so the ladder validates *machinery*, not *strategy*.

**`n = 17` is the only registered cell that tests record-finding.** It is cheap to carry
and has never been run.
That is currently the largest unforced gap in the coverage.

## Theoretical Results

Status is recorded on the same three tiers the campaign uses for measurements, so a
claim’s evidential standing is never ambiguous.

| Tier | Meaning |
| --- | --- |
| **proved** | A mathematical argument, checkable by reading |
| **exact** | Decided by exact arithmetic over the relevant number field; a proof, mechanised |
| **verified (f64)** | Computed in floating point; strong evidence, not a proof |

### Results relied on from the literature

Cited near the claims they support in the
[`n = 11` report](docs/project/research/research-2026-08-22-packing-11-unit-squares.md);
listed here so the dependencies of this program are explicit.

- **`s(10) = 3 + ½√2`**, Stromquist 2003, Theorem 1. Ten unavoidable points, then case
  analysis. Not pigeonhole alone.
- **`s(11) ≥ 2 + 4/√5`**, Stromquist 2003, Theorem 2, proved directly for `n = 11`.
- **`s(11) ≤ 3.877083590022814…`**, Trump 1979, by construction.
  Every upper bound in this subject is a construction; no non-constructive upper bound
  has ever been obtained.
- **The `0°`/`45°` class cannot achieve it.** Stromquist bounds that orientation class
  below at `2 + (4/3)√2 ≈ 3.885618`, which Trump’s oblique packing beats.
  This is what makes `n = 11` the first case where tilt matters, and it is the sharpest
  available statement of why the target is structurally different from the ladder.

### Results established here

Three, in dependency order.
`T-2` is the one with consequences for everything else.

| Id | Statement | Tier | Reproduce with |
| --- | --- | --- | --- |
| **T-1** | Trump’s 1979 packing is a valid packing of 11 unit squares in a square of side `s`, where `s` is the degree-8 algebraic number above; 14 of its 55 pairs touch at exactly zero separation and 20 corner coordinates lie exactly on the boundary | **exact** | `python3 verify_trump11.py` |
| **T-2** | Fixing every angle and every pair’s separating axis reduces the problem to a **linear program** in the centres and the side. All nonconvexity lives in the angles and in the combinatorial choice of cell | **proved**, and instantiated at **verified (f64)** | `python3 lp_cell.py` |
| **T-3** | On Trump’s cell, the LP optimum as a function of the tilt angle is minimised **at a kink**, not at a smooth stationary point: the one-sided slopes are stable under refinement and differ by a factor of ≈ 2.20 | **verified (f64)**, one cell, one instance | `python3 lp_cell.py` |

**T-1** is also an independent check of the published record: the 33 digits on the
*Squares in Squares* record page agree with the value computed here from the field.
No other public tool is known to check a record packing exactly, and the 14 zero-gap
pairs are precisely the ones no floating-point verifier can decide.

**T-2** and **T-3** are elaborated in full in the next section.
T-2 originated in the
[standing review](docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#r-2)
as observation R-2; T-3 is first reported here.

## The Cell Decomposition

The result the refiner rests on, stated so it can be checked.

### Setup

Fix `n` unit squares.
A configuration is

- a **centre** `(xᵢ, yᵢ) ∈ ℝ²` and an **angle** `θᵢ ∈ [0, π/2)` for each square `i`, and
- the container side `s`,

so `3n + 1` real coordinates in all, which is 34 at `n = 11`.

The four corners of square `i` are `(xᵢ, yᵢ) + Rᵢ·(±½, ±½)` where `Rᵢ` is rotation by
`θᵢ`. Write `oᵢₖ ∈ ℝ²` for the four corner offsets, `k = 1…4`. **Once `θᵢ` is fixed the
`oᵢₖ` are constants**, and every corner is an affine function of the centre alone.

Two squares have disjoint interiors exactly when some line separates them, and for
convex polygons it suffices to test lines parallel to their edges.
A square has two distinct edge normals (opposite edges are parallel), so a pair has four
candidate axes; these too are functions of the angles alone.

Define a **cell** of the configuration space to be a choice, for each of the `C(n,2)`
pairs, of one candidate axis together with an order (which square lies on the low side).
A configuration lies in a cell when that axis genuinely separates that pair in that
order.

### Statement

> **T-2.** Fix the angle vector `θ` and fix a cell `C`. Then
> 
> ```
> minimise   s
> subject to  the configuration lies in cell C and inside [0, s]²
> ```
> 
> is a linear program in the `2n + 1` variables `(x₁,…,xₙ, y₁,…,yₙ, s)`, with
> `16·(n + C(n,2))` inequality constraints.

At `n = 11`: **23 variables and 1,056 constraints.**

### Why

Four observations, each immediate once the angles are fixed.

1. **Corners are affine in the centres.** Corner `k` of square `i` is `(xᵢ, yᵢ) + oᵢₖ`
   with `oᵢₖ` constant.
2. **Containment is linear.** Each corner must satisfy `0 ≤ xᵢ + oᵢₖ,ₓ ≤ s` and
   `0 ≤ yᵢ + oᵢₖ,ᵧ ≤ s`. That is 4 inequalities per corner, 16 per square.
   Note that `s` appears here, and only here, as a variable.
3. **Separation along a *fixed* axis is linear.** For axis `ν` and order `(i before j)`,
   separation says every corner of `i` projects at or before every corner of `j`:
   `⟨ν, (xᵢ,yᵢ) + oᵢₖ⟩ ≤ ⟨ν, (xⱼ,yⱼ) + oⱼₗ⟩` for all `k, l`. Since `ν` is a constant
   vector, each is a linear inequality in four of the variables.
   That is 16 per pair.
   (The equivalent `max ≤ min` form is the same feasible set with fewer rows; the 16-row
   form is used because it needs no auxiliary variables.)
4. **The objective is linear**, being `s` itself.

The nonlinearity of the original problem is entirely in two places: the trigonometric
dependence of `oᵢₖ` and `ν` on the angles, and the *discrete* choice of cell.
Neither is present once both are fixed.

Note what the statement does **not** claim.
The LP optimises within one cell.
A different cell may have a lower optimum, and finding the best cell is the
combinatorial part of the problem, which is not made easy by any of this.

### The instance: Trump’s cell

`lp_cell.py` reads the cell off `sqpack`’s exact certificate — eleven angles and
fifty-five axis choices, and nothing else — rebuilds the LP from scratch, and solves it.
**The centres are never given to the solver.** They are what it must reconstruct.

```
The cell, read off the exact certificate
  distinct angles:  [0.0, 40.18193729] deg
  tilted squares:   [6, 7, 8, 9, 10]
  axis choices:     55 pairs
  LP shape:         23 variables, 1056 constraints  (= 16 x (11 + 55))

Solving it, without telling the solver where the squares go
  LP optimum        s = 3.8770835900228136
  exact value       s = 3.8770835900228140
  |difference|        = 4.441e-16
  worst centre error  = 1.332e-15
```

Both residuals are at `f64` round-off.
**The cell containing Trump’s packing, solved as a linear program, is Trump’s packing.**

This is what makes the middle evidence tier real.
“Where the annealer stopped” is a property of the cooling schedule; “the optimum of the
cell the annealer stopped in” is a property of the landscape, and it is computable
exactly.

### Thirty-four dimensions become one

Trump’s packing uses two distinct angles: `0°` on six squares and `a*` on five.
Holding the cell fixed and varying the single free angle gives a function

```
φ(a) = the LP optimum of Trump's cell with the five tilted squares at angle a
```

which is the entire problem, restricted to this cell, in **one** variable.

| `a` (deg) | `φ(a)` | `φ(a) − s*` |
| --- | --- | --- |
| 39.000000 | 3.880706142326 | `+3.623e-03` |
| 39.500000 | 3.879169268857 | `+2.086e-03` |
| 40.000000 | 3.877638844995 | `+5.553e-04` |
| 40.100000 | 3.877333546175 | `+2.500e-04` |
| **40.181937** | **3.877083590023** | `−4.441e-16` ← Trump |
| 40.300000 | 3.877877577363 | `+7.940e-04` |
| 40.500000 | 3.879235737993 | `+2.152e-03` |
| 41.000000 | 3.882703521786 | `+5.620e-03` |
| 42.000000 | 3.889950463054 | `+1.287e-02` |

A 2,001-point scan of `[38°, 42°]` puts the minimum at `40.182°`, one grid step
(`0.002°`) from `a*`.

So Trump’s angle is not an input to this computation; it is **the argument that
minimises a one-dimensional convex-looking function that anyone can plot.** The
34-dimensional search problem, once the cell is known, is a scalar minimisation.
This is the concrete content of the claim that the honest continuous dimension of the
problem is the number of *distinct angles*, empirically one or two at small `n`, rather
than `3n + 1`.

### The minimum is a kink

`φ` is not smooth at its minimum.
Measuring one-sided slopes and refining the step:

| `h` (deg) | left slope | right slope |
| --- | --- | --- |
| `1e-02` | `3.049623e-03` | `6.702833e-03` |
| `1e-03` | `3.049503e-03` | `6.700977e-03` |
| `1e-04` | `3.049491e-03` | `6.700791e-03` |
| `1e-05` | `3.049490e-03` | `6.700772e-03` |

Both converge, and they converge to **different** values, ratio ≈ 2.1973. The derivative
does not vanish at `a*`; it jumps.

The mechanism is visible in the LP. Where the optimal basis is locally constant, `φ` is
smooth, and its derivative is read off the active constraints.
A kink is a **change of optimal basis** — the set of contacts that bind switches as `a`
crosses `a*`. That the switch happens exactly at the minimum is what rigidity means,
expressed in the coordinates the refiner actually works in: at `a*` the packing is
maximally constrained, and moving the angle either way relaxes one contact set and
tightens another.

This has a direct consequence for the refiner that
[H-002](campaign/hypotheses/H-002-lp-in-cell-polish.md) is registered to build.
**A first-order angle move cannot terminate at the optimum by a vanishing-gradient test,
because the gradient does not vanish there.** The angle-space loop needs a non-smooth
method — bisection on the sign of the one-sided derivative, or an active-set switch —
and a smooth Newton or gradient step will either overshoot or stall short.
This is exactly the “behaviour at cell boundaries” that H-002 names as the untested half
of its claim, and it says the answer is not a detail.

### Consequences

In increasing order of ambition, and all of them downstream of a result that takes 13
seconds to check.

- **The refiner is an LP solve per cell**, exact to solver precision, with rational
  output. That is the campaign’s missing middle tier, and the reason
  [H-002](campaign/hypotheses/H-002-lp-in-cell-polish.md) is the registry’s top
  priority.
- **Basins become nameable.** A local minimum stops being tolerance-dependent and
  becomes a discrete object with an exact side length, which is what makes a census, an
  atlas, and basin statistics well defined at all.
- **The search space factorises** into a small continuous part (the angles) and a
  combinatorial part (the cell), which is the premise of the angle-class proposer
  ([H-001](campaign/hypotheses/H-001-angle-class-reduction.md)).
- **Rational-slope tilts need no number field.** At a Pythagorean angle such as
  `arctan(3/4)` every coordinate and the LP optimum are rational, so exact verification
  is `ℚ`-arithmetic at degree 1. The cost of the exact layer is a function of the
  *angle’s* algebraic complexity, and a search can choose to look where that cost is
  low.

### Reproducing all of it

```bash
cd explorations/packing
python3 verify_trump11.py    # T-1: exact verification over Q(u)
python3 lp_cell.py           # T-2 and T-3: the LP, the sweep, the slopes  (needs scipy)
./test.sh                    # both of the above, plus every other gate
```

`lp_cell.py` asserts every figure quoted above, so a change that breaks one fails the
gate rather than silently editing the record.
Only `lp_cell.py` and `derive_field.py` need third-party packages (scipy and SymPy
respectively); the verifier itself is standard library.

## The Program So Far

This section is deliberately historical: it records the order in which things were done
and why, because several of the decisions were made by measurement and the measurements
are the reason later work is shaped as it is.

**Establish the frontier, then the mathematics.** The `n ≤ 100` corpus was built first,
as one validated artifact per case, so that “the standing best” is a fact read from a
file rather than a number retyped into a paragraph.
Retrieving the primary sources then corrected the record in ways secondary summaries had
not: one widely-repeated explicit constant turned out to appear in no primary paper at
all.
That episode is why the grounding rule for every later lane is that nothing enters a
prompt or an artifact unverified.

**Build the exact verifier before building the search.** The rigidity of record packings
means a float check cannot decide them, and the tolerance blind spot is not a rounding
concern but a correctness one.
`sqpack` was written, validated against Trump’s packing (**T-1**), and given a negative
control that demonstrates both float failure modes.

**Study the tooling question, then decide by measurement.** Three reports — on
algorithms, on one Rust framework as a source of parts, and a synthesis — concluded a
build order in which compiled code arrives late and only where a profile names it.
The profile said the exact verifier, not the annealer, is the expensive stage.

**Write the search engine; two formulations failed first.** Fixing a container side and
asking whether the squares fit needs an outer loop that decides when an anneal has
failed, and it starts from the trivial grid, which is exactly jammed: shrinking it at
all is infeasible, and only a wholly different tilted configuration helps.
Two versions were built and measured.
The first crawled, reaching `2.875` on `n = 5` where the answer is `2.707`; the second
never left the grid basin at all.
Both are recorded as dead ends on the [idea board](campaign/ideas.md).
The replacement removes the container from the variables entirely, minimising
`required_side + λ·total_overlap` with `λ` ramped upward — a linear penalty, because a
squared penalty’s gradient dies as the overlap closes.

**Run the baseline, and discover the instrument was lying.** A restart cap was stopping
every chain before the declared move budget did, so `--budget-moves` was inert and two
strategies compared “at equal budget” would have had unequal work.
The tell was that results got *worse* when the declared budget was raised.
After the fix the `n = 5` control improved eighteenfold.

**Add the method, and find the missing stage.** A standing review audited the toolkit
documents and found that all of them presumed a refinement stage that none of them
built. In looking for it, the review found **T-2** — the stage is a linear program — and
supplied the experimental method the project lacked: a hypothesis register with kill
criteria written before the run, a run protocol, and a seven-series plan.

**Adopt a strategy, and register the premise so it can fail.** The search-philosophy
report argued that records are rigid, rigid optima live in rare basins, and therefore
scaling a volume-weighted sampler multiplies effort against a probability the problem
drives toward zero. The response is to make the set of local optima the object of study.
Because that argument is load-bearing, the measurement that would refute it
([H-012](campaign/hypotheses/H-012-record-basins-are-rare.md)) is registered in the
cheapest budget tier and scheduled early.

**Consolidate.** The campaign’s registry and the review’s register had been numbered
independently and collided; they were merged under one numbering, with the renumbering
recorded as annotations rather than silent edits.
The four baseline rounds were re-run one cell per round on a corrected archive after a
review found that the first round’s archive discarded the configurations and its
recorded commit had been orphaned by a rebase.

### How rounds are run

The full contract is the [runbook](campaign/README.md); the parts that matter for
reading the results below:

- **Three evidence tiers**, and a number’s tier decides what it may claim: `f64_screen`
  (a candidate was proposed), `polished` (this is the basin, named and exactly valued),
  `exact` (validity, and only here a record).
  **`beat_record: true` may only be written at `exact`.**
- **Four instance cells with different jobs**: `n = 10` positive control, `n = 11`
  target, `n = 12` negative control, `n = 17` mechanism-matched calibration.
  A guard breach rejects a round regardless of its outcome, because it means the
  instrument is wrong rather than the strategy good.
- **Five seeds minimum per cell**, with median and min–max range both reported.
  Overlapping ranges mean *no detectable effect*, never “a small win”.
- **Budgets in pair-tests**, tiers S/M/L = `1e9`/`1e11`/`1e13`, because wall clock is
  not comparable across machines and move counts are not comparable across proposers.
- **Negative results are kept.** A run that came out badly is not deleted, and a
  defective artifact is corrected by dated annotation rather than rewriting.

## The Hypothesis Registry

Seven claims are codified as artifacts; eleven more exist as prose in the standing
review’s register with their ids reserved.
The [ledger](campaign/ledger.md) is generated from the artifacts and is the current
view; this section is the reading of it.

### Refuted

**[H-016](campaign/hypotheses/H-016-stock-annealer-reaches-standing-best.md) — the stock
annealer reaches the standing best on every cell.** The null hypothesis: that a
general-purpose annealer, given a serious budget, finds the best known packing.
Claim was `1e-4` on every cell of `n = 10, 11, 12`; only `n = 12` met it.
Resolved by four rounds, `exp-001` through `exp-004`.

The refutation is not the interesting part.
**The two failures are different in kind, and one criterion could not tell them apart:**

- At `n = 10` the search finds the right basin and stops `4.19e-04` short of a proved
  optimum. That is a **polish** failure, and `T-2` is its fix.
- At `n = 11` the search never reaches the right region at all, landing `3.73e-02`
  short. That is an **exploration** failure, and no amount of polish addresses it.

This distinction is why H-002 became the registry’s top priority, and it is the single
most useful thing the baseline produced.

### Key open hypotheses

Ordered as the registry orders them.
All four are **blocked**: their instruments do not exist yet, and all four wait directly
or transitively on H-002.

**[H-002](campaign/hypotheses/H-002-lp-in-cell-polish.md) — LP-in-cell polish is exact
and sufficient.** *Priority 1, tier S.* Alternating per-cell LP solves with local angle
moves refines any annealer output to a genuine cell-optimum matching the analytic value.
The single-cell half is **already established** (T-2 above); what is under test is the
**loop** — angle moves between solves, and behaviour at cell boundaries.
T-3 says that behaviour is non-smooth and therefore not a detail.
Kill: cycling between cells, or systematic gaps to the analytic optima.
**Nearly everything in the registry waits on this**, and it needs only Python and scipy.

**[H-011](campaign/hypotheses/H-011-small-n-census.md) — the small-`n` landscape is
censusable.** *Priority 1, tier S.* LP-quenching multistarts at `n ≤ 10` yields a basin
count that saturates, giving a near-complete atlas with canonical identities and exact
side lengths. Kill: no plateau by `n = 8` within tier S.

**[H-012](campaign/hypotheses/H-012-record-basins-are-rare.md) — record basins are rare
in quench measure.** *Priority 1, tier S, a query over H-011’s data.* **The load-bearing
premise of the entire strategy layer**, registered so it can fail cheaply.
Kill: record-basin probability within ~10× of the modal basin’s — in which case blind
multistart plus polish is already adequate, the cartography program stands down, and the
campaign reverts to raw throughput.
Grounding is real but thin: Ellsworth’s 4-in-3,004 basins for `s(51)`, the 14 zero-gap
pairs in Trump’s packing, and the double-funnel precedent from energy-landscape science.
None of that is a measurement of *this* landscape.

**[H-001](campaign/hypotheses/H-001-angle-class-reduction.md) — angle-class reduction
beats free `3n`-dimensional annealing.** *Priority 2, tier M.* Optimal packings at
`n ≤ ~30` use at most 3 distinct tilt angles, so a two-level search — outer over class
count and angles, inner the cell LP — reaches known optima in less budget.
T-2 is the geometric statement of why this could work.
Recorded caution: a win shows that *given* the right angular structure the rest is easy,
which locates the difficulty; it is not evidence that an unguided method could find
`n = 11`.

### Registered and runnable today

**[H-018](campaign/hypotheses/H-018-basin-entry.md) — basin entry.** *Priority 1, under
a minute of compute.* Start at Trump’s exact configuration, perturb by uniform noise of
size `ε`, and measure what fraction of runs return.
This separates “search cannot find the region” from “the refiner cannot hold it”, two
failures with identical symptoms and different fixes, and the `ε` at which the return
rate collapses is the basin width in the units the search actually moves in.
It produces a number either way.
**This is the cheapest informative measurement available, and it has not been run.**

**[H-017](campaign/hypotheses/H-017-budget-scaling.md) — 100× the budget reaches Trump’s
basin.** *Priority 4, ~3 hours.* Demoted on merge, because H-012 answers the same
question far better and off data worth collecting anyway.
Kept because it is runnable today.
**The prediction, recorded before the run, is that it fails**, and a partial improvement
should be recorded `unresolved` rather than argued into either story.

### Reserved but not codified

`H-003`–`H-010` and `H-013`–`H-015` exist as prose in the
[standing review’s register](docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#the-hypothesis-register)
with their ids reserved and enforced.
They cover, among others: basin frequency versus contact count; neighbour-transfer
seeding; the `m² − 3` analytic attempt; LP duals as unavoidable-set generators for the
proof lane; saturation-curve fitting; the false-basin rate; symmetry dedup ratios;
δ-continuation; superdisk continuation; and MAP-Elites illumination.
The [idea board](campaign/ideas.md) carries all of them as one-line rows alongside the
untried strategy families.

## Experiments Conducted

Four rounds, all in `series-000`, all testing `H-016`, all at `f64_screen` on the same
instrument: **`sqsearch` 0.1.0**, an annealer minimising
`required_side + λ·total_overlap` with a single-square move set, 8 chains, 5
deterministic seeds, 100M moves per chain.

No round has yet been run at the `polished` or `exact` tier, so **no result below claims
anything about a record**, and none may.

### Roll-up

Every figure is lifted from the round’s frontmatter, which in turn is lifted from the
JSONL archive beside it.

| Round | Date | `n` | Role | Best `best_side` | Standing best | Gap | Median across 5 seeds | Seed range | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [exp-001](campaign/series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md) | 2026-08-22 | 10 | positive control | `3.7075262001` | `3.7071067812` | `+4.194e-04` | `3.7076711818` | `[3.7075262, 3.7091188]` | **rejected** |
| ” | ” | 11 | target | `3.9144165418` | `3.8770835900` | `+3.733e-02` | `3.9279396177` | `[3.9144165, 3.9361125]` | ” |
| ” | ” | 12 | negative control | `4.0000000000` | `4.0000000000` | `+0.000e+00` | `4.0000000000` | `[4.0, 4.0]` | ” |
| [exp-002](campaign/series/series-000-smoke-and-calibration/experiments/exp-002-baseline-n10-positive-control.md) | 2026-08-23 | 10 | positive control | `3.7075262001` | `3.7071067812` | `+4.194e-04` | `3.7076711818` | `[3.7075262, 3.7091188]` | **rejected** |
| [exp-003](campaign/series/series-000-smoke-and-calibration/experiments/exp-003-baseline-n11-target.md) | 2026-08-23 | 11 | target | `3.9144165418` | `3.8770835900` | `+3.733e-02` | `3.9279396177` | `[3.9144165, 3.9361125]` | **rejected** |
| [exp-004](campaign/series/series-000-smoke-and-calibration/experiments/exp-004-baseline-n12-negative-control.md) | 2026-08-23 | 12 | negative control | `4.0000000000` | `4.0000000000` | `+0.000e+00` | `4.0000000000` | `[4.0, 4.0]` | **accepted** |

`exp-002` through `exp-004` re-run `exp-001`’s three cells one per round on a corrected
instrument and archive.
Their numbers are identical to `exp-001`’s, which is the intended behaviour of a
deterministic engine on fixed seeds, and is itself the reproducibility check.

**Cost and provenance.**

| Round | Budget | Wall | Engine commit | Archive |
| --- | --- | --- | --- | --- |
| exp-001 | 12,000,000,000 moves | 302.4 s | `d6a1057` (**orphaned**) | [15 lines, summaries only](campaign/series/series-000-smoke-and-calibration/results/exp-001-baseline.jsonl) |
| exp-002 | 4,000,000,000 moves | 93.5 s | `1e70bc8` | [45 lines, 40 with configurations](campaign/series/series-000-smoke-and-calibration/results/exp-002-baseline-n10-positive-control.jsonl) |
| exp-003 | 4,000,000,000 moves | 107.2 s | `1e70bc8` | [45 lines, 40 with configurations](campaign/series/series-000-smoke-and-calibration/results/exp-003-baseline-n11-target.jsonl) |
| exp-004 | 4,000,000,000 moves | 108.8 s | `1e70bc8` | [45 lines, 40 with configurations](campaign/series/series-000-smoke-and-calibration/results/exp-004-baseline-n12-negative-control.jsonl) |

### What the four rounds jointly establish

**The instrument works.** The positive control lands in the right basin at `n = 10` — a
proved optimum that is *not* the grid, so recovering it exercises the tilted part of the
search. The negative control returns exactly `4.0` at `n = 12` on all five seeds and
never below, so the geometry is not manufacturing packings that do not exist.
Overlap is recomputed from each stored configuration rather than read off the annealer’s
accumulator, and comes back `0.0` everywhere.

**The target is genuinely hard, and the failure has a shape.** At `n = 11` the five seed
results span `2.2e-02`, which is **five times narrower than the `3.73e-02` still
separating them from Trump**. Every seed lands well short, in a band of its own.
That is not a search that is nearly there; it is what a sampler repeatedly finding the
same wrong funnel looks like.
It is weak evidence for [H-012](campaign/hypotheses/H-012-record-basins-are-rare.md)’s
premise — consistent with it, but a single configuration of a single method, and it
measures no basin volume directly.

**The `n = 10` miss is the more actionable result.** `4.19e-04` inside the correct basin
is a refinement failure, and `T-2` says refinement is a linear program.

### Known defects in the record

Recorded because the convention is that the record is corrected by addition.

- **`exp-001`’s archive is not reproducible.** The run script filtered output to summary
  lines, discarding the per-chain configurations.
  Every number in the artifact was re-derived from the archive and matched, but the
  *packings* cannot be recovered, so its `checked_by` guard is not auditable from the
  archive. `exp-002`–`exp-004` are the rounds to cite for anything configuration-level.
- **`exp-001`’s engine commit is unreachable**, orphaned by a rebase, so the exact
  binary cannot be rebuilt from the recorded provenance.
  The provenance rule now requires a commit that is an ancestor of the branch being
  merged, and `test.sh` reports orphans and requires an annotation.
- **`exp-001` records one instance but measured three.** The ledger therefore shows two
  of H-016’s sweep cells as unfilled.
  Nothing about the measurement is wrong; the shape of the record misreports it, and
  later sweep rounds are split one cell per round.
- **A draft of `exp-001` called `n = 10` a confirmation** because the search plainly
  found the right basin.
  It did not meet the declared criterion.
  The generated frontmatter contradicted the prose, which is what caught it.

## Where This Stands

One instrument is finished, one theoretical result is established with a consequence
nobody has exploited yet, one hypothesis is refuted informatively, and the queue is
almost entirely gated on a single unbuilt component.

**The bottleneck is [H-002](campaign/hypotheses/H-002-lp-in-cell-polish.md).** It is
tier S, needs only Python and scipy, has its hard half already verified (T-2), and
blocks the census, the rarity measurement, the angle-class proposer, and every
descriptor the atlas would carry.
T-3 tells its angle loop what shape of minimum to expect.

**Two measurements are runnable today and have not been run**: basin entry
([H-018](campaign/hypotheses/H-018-basin-entry.md)), which costs under a minute and
produces a number either way, and the `n = 17` calibration cell, which is the only
registered target that speaks to record-*finding* rather than machinery.

**The premise is not yet tested.** Everything the strategy layer recommends rests on
record basins being rare in quench measure, and
[H-012](campaign/hypotheses/H-012-record-basins-are-rare.md) is the measurement that
would refute it. It is scheduled early and cheaply for exactly that reason, and until it
runs, the cartography program is a well-argued bet rather than a finding.

## References

Primary sources are archived locally under [`resources/`](resources/README.md); the
citation keys below resolve there and in the per-case [`frontier/`](frontier/README.md)
artifacts.

- Stromquist, W. (2003). *Packing 10 or 11 unit squares in a square.* Electronic Journal
  of Combinatorics 10(1), R8. — `s(10)`, the `s(11)` lower bound, and the `0°`/`45°`
  class bound.
- Trump, W. (1979). The `n = 11` packing, as published on the *Squares in Squares*
  record page with Ellsworth’s exact solution in the SVG source.
  — the standing upper bound.
- Friedman, E. (2009). *Packing Unit Squares in Squares: A Survey and New Results.*
  Electronic Journal of Combinatorics, DS7. — the survey the corpus is checked against.
- Erdős, P. and Graham, R. L. (1975). *On packing squares with equal squares.* — the
  asymptotic waste line of work.
- Nagamochi, H. (2005). *Packing unit squares in a rectangle.* — the general lower bound
  that covers 63 of the 65 open cases in the corpus.
- Montanher, T. et al.
  (2018). *Rigorous packing of unit squares into a circle.* — the only rigorous
  computer-assisted optimality proof for rotatable unit squares in any container, and
  the scope limit on what `sqpack` claims.
- Doye, J. P. K., Miller, M. A. and Wales, D. J. (1999). The double funnel energy
  landscape of the 38-atom Lennard-Jones cluster.
  — the precedent behind the rarity premise.
- Stillinger, F. H. and Weber, T. A. (1982). Inherent structures and the quench map.
  — the decomposition T-2 supplies an exact version of.
- Mouret, J.-B. and Clune, J. (2015). *Illuminating search spaces by mapping elites.* —
  the precedent behind H-015.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
