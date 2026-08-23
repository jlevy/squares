# Glossary

Terms this project uses in a specific sense, defined once so they cannot drift.
Where two terms are easy to confuse, the confusion is named explicitly — every such pair
below has already caused a wrong conclusion at least once.

[`conventions.md`](conventions.md) covers process rules; this file covers vocabulary.

## Why this file exists

[D-024](defects.md) is the motivating case.
A probe implemented a *single LP solve at fixed angles*, called it “the quench”, found
it did not reach the analytic optimum at `n = 10`, and concluded the search had been in
the wrong basin. It had not been.
The optimum needed different *angles*, which that probe held frozen by construction.

The mistake was entirely a vocabulary mistake: **cell** was treated as a synonym for
**basin**, and the first step of an operation was called by the operation’s name.
Both are defined below.

## The configuration space

**Pose.** One square’s position and orientation: `(x_k, y_k, θ_k)`.

**Configuration.** The poses of all `n` squares — `3n` numbers.
It does not include the container side.

**Required side.** `s(config)`, the side of the smallest axis-aligned square containing
every square of a configuration.
Computable from the configuration alone, which is why the container is not a search
variable.

**Pair-test.** One evaluation of the separating-axis predicate on one pair of squares.
The campaign’s budget currency, because it is machine-independent and comparable across
proposers whose move semantics differ.

## Cells and basins — the pair that caused D-024

**Cell.** *At fixed angles*, an assignment to every pair of **which** of the four
candidate separating axes separates it and **on which side**. Each such assignment picks
out a convex polyhedron in the `2n+1` space of centres and side; the feasible set at
those angles is the union of all of them.
At `n = 11` there are `8^55 ≈ 5 × 10⁴⁹` assignments, most of them empty.

A cell is defined **only at fixed angles**. Change an angle and you are asking about a
different family of polyhedra.

**Basin.** The set of configurations that **quench** to the same local optimum.
A basin ranges over the angles too.

> **A cell is not a basin.** A cell is a slice at frozen angles; a basin is the full
> attractor including angular freedom.
> A configuration can sit exactly at its cell’s optimum and still be far from its
> basin’s optimum, with all the remaining error in the angles.
> That is precisely what D-024 misread.

## The quench

**Quench.** The map from an arbitrary configuration to the local optimum of its basin.
Borrowed from Stillinger and Weber’s inherent-structure decomposition, where a quench
sends a configuration to the minimum at the bottom of its basin.
Here it has **three parts**, and the word names all three:

1. **Cell solve** — minimise `s` over one cell.
   A linear program: at fixed angles the corners are affine in the centres, the
   separating-axis conditions are linear inequalities, containment is linear, and
   `min s` is linear. At `n = 11` that is 23 variables and 99 constraints.
2. **Cell re-read to a fixed point** — solving moves the centres, which can change which
   axis has the widest margin for some pair, i.e. change the cell.
   Re-read and re-solve until it stops changing.
3. **Angle refinement** — move the angles and repeat.
   Without this the quench cannot leave its starting angles, and therefore cannot reach
   any optimum that needs different ones.

**Cell solve** alone is *not* a quench, and calling it one is D-024.

**Descent quench.** A quench whose angle half is finite-difference descent.
Measured to stall five orders short of the optimum, because of the kink below.

**Bracketing quench.** A quench whose angle half merges angles into **classes** and
brackets (golden section) rather than descends.
Reaches the analytic optimum to machine precision at `n = 5` and `n = 10` where descent
does not.

## Gaps — the second confusable pair

For a run scored against a known optimum:

```
total gap  =  polish gap  +  exploration gap
```

**Polish gap.** `(where the run stopped) − (the optimum of the basin it is in)`. A
convergence shortfall: the right basin, unfinished.

**Exploration gap.** `(the optimum of the basin it is in) − (the global optimum)`. A
wrong-basin shortfall, which no local refinement can close.

> **Neither is measurable without a quench that actually reaches the basin optimum** —
> which means a quench including its angle half.
> Splitting the total gap by eye, from its magnitude, is what D-024 did.

Settled by the sweep: `n = 5` and `n = 10` are polish gaps (the bracketing quench
finishes them to `~1e-15`); `n = 11` is an exploration gap (nothing local crosses
`8.8e-02`).

## Landscape structure

**Kink.** The angle objective `s(θ)` has **distinct one-sided derivatives** at its
optimum — measured at `n = 11` as slopes `0.175` and `0.384` — because the active
contact set changes there.
The optimum is a corner, not a smooth minimum, which is fatal to any method assuming a
smooth local model.

**Angle class.** A set of squares constrained to share one angle.
Trump’s `n = 11` uses two classes: six at `0°` and five at `≈40.182°`.

**Rigid.** A packing whose contact conditions determine `s` exactly, with no slack
anywhere. Rigidity is what makes the algebraic value computable, and is the reason to
expect the basin to be small.

**Contact graph.** Which square/wall pairs touch, and along which edge classes.
Up to isomorphism it is the structural identity of a packing — what “the same packing”
means in the record catalogue.

**Atlas.** The deduplicated store of known basins, keyed by canonical identity, with
exact side lengths and quench frequencies.
The campaign’s deliverable.

## Instruments and tiers

**Proposer.** Anything that generates candidate configurations — annealing, multistart,
δ-continuation, an archive, a constructor program.
A proposer never quenches, canonicalizes, decides validity, or writes the atlas.

**Spine.** The shared pipeline every proposer runs through: quench → canonicalize →
verify → atlas.

**Tier.** What a number is allowed to claim, recorded as `subject.precision`:

| Tier | Instrument | May claim |
| --- | --- | --- |
| `f64_screen` | `sqsearch` | a candidate was proposed |
| `polished` | the quench | this is the basin, named and exactly valued |
| `exact` | `sqpack` over ℚ(α) | validity — and only here, a record |

**Standing best.** The best known value for an instance, read from
[`frontier/`](frontier/README.md) and never retyped into a round.

**Analytic optimum.** The proved or published exact value, where one exists.
Distinct from the standing best only in that a standing best may be unproved.

## Record vocabulary

Defined in [`conventions.md`](conventions.md) and named here only so the two files
agree: **campaign**, **series**, **round** (`exp-NNN`), **hypothesis** (`H-NNN`),
**exploration report** (`X-NNN`), **defect** (`D-NNN`).

## Rules for adding a term

- A term goes here the first time two people, or two documents, could read it
  differently.
- If a term names an operation with parts, say whether the term means the whole or a
  part. Most of the trouble is here.
- When a defect turns out to be a vocabulary failure, the fix includes an entry here and
  the defect’s `regression` says so.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
