# Synopsis: The `s(n)` Program

**Date:** 2026-08-24 (last updated after terminal `series-000` round 15)

**Status:** Living document, revised whenever a result lands.

**Owns:** The single technical account of what this project knows, how it knows it, and
what it is doing next.

> Every number here also appears in a schema-validated artifact in this directory, or is
> reproducible by a command given in the text, and the artifact is authoritative where
> the two differ. `tools/check_synopsis.py` enforces that in the gate.

## Overview

`s(n)` is the side of the smallest square that contains `n` non-overlapping unit
squares, which may be rotated freely.
The motivating case is `n = 11`, the smallest instance nobody has solved.

This project works under four independent principles, defined at the top level in
[`README.md`](README.md#operating-principles): **Correctness** (Soundness) owns
mathematical truth and may veto promotion; **Process** (Discipline) owns reproducible
research operations and may veto an unreconstructable run; **Insight** (Creativity) owns
hypotheses and strategy but cannot certify them; and **Efficiency** (Infrastructure)
owns stable, measured throughput without relaxing Correctness or Process controls.
An agent normally focuses on one dimension at a time and hands explicit artifacts to the
next.

Those principles govern four capabilities built so far:

1. **Know the frontier.** A schema-validated record of the best known packing and the
   best proved lower bound for every `n ≤ 100`, with provenance, plus a local archive of
   the primary literature.
2. **Verify exactly.** A separating-axis verifier that decides validity over the
   packing’s own algebraic number field, so a configuration with contacts at *exactly*
   zero separation can be certified rather than guessed at.
3. **Search, under an experiment contract.** A hypothesis registry with kill criteria
   written before the run, a metric vector, an accept rule, a declared timebox, and a
   ledger generated from the artifacts rather than typed.
4. **Account for what goes wrong.** A defect log with the same discipline as the
   experiment record, because most soundness failures found so far pointed in the
   *flattering* direction and none was caught by the automated gate.

Capability 2 is narrower than it sounds and the difference matters: this directory can
**check** a packing whose exact algebraic description it is given, and cannot yet
**produce** that description from a packing it found.
[What Is Built](#what-is-built) states, component by component, what runs, what runs but
cannot support the claim it appears to, and what is documented and unbuilt.
Read it before citing any capability here.

The strategy that organises lanes 3 and 4 is stated in
[A Search Philosophy for Square Packing](docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md):
**a validated map of terminal components is the intended deliverable, and records are
corollaries.** The current endpoint map remains provisional while identity and local
certification are unresolved.
The argument for it, and the measurement registered to kill it if it is wrong, are in
[Theoretical Results](#theoretical-results) and
[The Hypothesis Registry](#the-hypothesis-registry) below.

[Terminology](#terminology) below fixes the sense of every word this project uses
narrowly—quench, basin, polish, exploration, gap, tier—and disambiguates the one word
used for two different things.
Those definitions apply in the campaign artifacts and the beads too, not only here.

### Document map

Each document owns one thing.
Nothing here duplicates what another owns.

| Document | Owns |
| --- | --- |
| [`TUTORIAL.md`](TUTORIAL.md) | The conceptual on-ramp for a newcomer: the objects, why the approach is shaped this way, and what is established versus open. Owns no status—it defers here for all of it |
| **This synopsis** | The state of the program: results, their status, the roll-up of rounds |
| [Historical quench-spine handoff](docs/project/handoff-2026-08-23-quench-spine.md) | A superseded 2026-08-23 checkpoint retained as provenance. Do not use it for current priority; use the basin confidence ladder and launch agenda |
| [`README.md`](README.md) | The four-principle operating charter, what is in the directory, how to run it, and the index of the six research reports |
| [`conventions.md`](conventions.md) | Every rule the directory runs on, and which are machine-checked |
| [`defects.md`](defects.md) | Every bug and record defect, what caught it, and what now stops it recurring |
| [Soundness postmortem](docs/project/postmortems/postmortem-2026-08-23-soundness-class.md) | Why D-014 was possible, and rules R1–R4 that apply to code not yet written |
| [`frontier/`](frontier/README.md) | What is known about `s(n)` for every `n ≤ 100`, one artifact per case |
| [`resources/`](resources/README.md) | The primary literature, local and greppable |
| [Packing 11 Unit Squares](docs/project/research/research-2026-08-22-packing-11-unit-squares.md) | The mathematics of `s(11)`: what is proved, what is conjectured, why the proof technique stalls |
| [Algorithms and Tooling](docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md) | How packings are found, refined to exact form, and verified |
| [FrankenSim as a Rust Toolkit](docs/project/research/research-2026-08-22-frankensim-rust-toolkit-for-square-packing.md) | First-hand study of one Rust framework as a source of parts |
| [Infrastructure for Packing Exploration](docs/project/research/research-2026-08-22-infrastructure-for-packing-exploration.md) | The build order, the language boundary, what not to build |
| [Lean for Packing Proofs](docs/project/research/research-2026-08-22-lean-for-packing-proofs-and-validation.md) | Where a proof assistant fits, and what it would be pointed at first |
| [A Search Philosophy](docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md) | The strategy layer: why pointing should beat scaling |
| [Standing review](docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md) | The experimental method, and the register `H-001`–`H-015` in prose |
| [Plan spec](docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md) | The seven build phases, and a revision note recording what building the quench corrected |
| [Campaign runbook](campaign/README.md) | The contract every round runs under, frozen while rounds run |
| [Idea board](campaign/ideas.md) | The whole idea space on one page, including dead ends |
| [Ledger](campaign/ledger.md) | Generated roll-up of series, registry, rounds and effort |

The code that produces the numbers: [`sqpack/verify.py`](sqpack/verify.py) decides
validity exactly, [`sqpack/quench.py`](sqpack/quench.py) is the LP-in-cell quench,
[`lp_cell.py`](lp_cell.py) is a second, independent implementation of the quench’s
linear program, and [`sqsearch/`](sqsearch/) is the screening annealer.

## What Is Built

A documented method here is not necessarily an available one, and implementation status
has three values rather than two.

| Status | Means |
| --- | --- |
| **built** | Exists, runs, and is exercised by `./test.sh` |
| **built, not admissible** | Runs and produces output, but that output cannot yet support the claim it looks like it supports. The blocking defect is named |
| **unbuilt** | Documented, tracked as a bead, and not implemented. No result may assume it |

Most of the risk in this project lives in the middle row, because a component that runs
and prints a plausible number is the shape of every flattering soundness defect logged
here.

### The exact layer—built

| Component | What it does |
| --- | --- |
| [`sqpack/field.py`](sqpack/field.py) | Exact arithmetic in `ℚ(α)`: exact zero test, exact sign by rational interval bisection |
| [`sqpack/verify.py`](sqpack/verify.py) | Separating-axis validity, generic over the scalar type—exact or `f64` from one predicate |
| [`sqpack/packings/trump11.py`](sqpack/packings/trump11.py) | The `n = 11` witness, exactly, in `ℚ(u)` |
| [`derive_field.py`](derive_field.py) | Re-derives the degree-8 field from the published polynomial, factors over `ℚ`, and selects the root by isolating interval |
| [`negative_control.py`](negative_control.py) | Demonstrates both float failure modes against the same packing |

**One caveat, and it is critical.** [D-053](defects.md) is open: `NumberField` documents
an irreducible minimal polynomial and an interval containing exactly one real root, but
checks only an endpoint sign change.
The built-in `n = 11` witness is independently checked, so **T-1** is unaffected.
The *generic* path—bring your own packing and your own field—is not yet sound, and no
third-party field metadata should be trusted through it until a Sturm-sequence check
lands.

### The refinement layer—built, with a floor

[`sqpack/quench.py`](sqpack/quench.py) is the LP-in-cell quench with class bracketing,
and [`lp_cell.py`](lp_cell.py) is an independent second formulation of the same feasible
set. Both are built and agree to `4.4e-16` on Trump’s cell.

Three named limits travel with every number they produce:

- [D-021](defects.md)—the float LP solver has a noise floor of about `1e-11` in the
  side. Nothing at the `polished` tier may claim a difference finer than that.
  The general fix is an **exact LP over certified rational or algebraic coefficients,
  which is unbuilt**; it is purely rational only for rational-coefficient cells.
- [D-052](defects.md)—coordinatewise stopping is not a certified local optimum.
  A quench that stops has stopped; it has not proved stationarity.
- [D-126](defects.md)—the work budget is wall-clock time, so contention changes how many
  LP solves a run performs.
  Price basin experiments by retained work units, not by the clock.

### The proposer layer—one instrument, and the interface is unbuilt

[`sqsearch/`](sqsearch/) is the `f64` screening annealer, and it is the only proposer
the campaign has run.
Uniform multistart draws exist inside the census and the checkers, with the census
declaring its regime; the proposer *interface*—the contract that would make two
proposers comparable—is unbuilt.

**Unbuilt, and each is a registered hypothesis with nothing behind it yet:** the
proposer interface itself, the pair-test **meter** (so no two proposers have ever been
compared at equal budget), δ-continuation, angle-class search *as a search*,
neighbour-transfer seeding, MAP-Elites retention, and billiard/inflation.

This is the campaign’s live bottleneck.
The refiner takes the tested proved-control starts to residuals of `1e-15` and leaves
the tested `n = 11` starts at `6e-02`, so proposal is where the gap is—and proposal is
the layer with the fewest built parts.

### The map layer—built, not admissible

| Component | Runs | Why its output is not yet the thing it looks like |
| --- | --- | --- |
| [`sqpack/canonical.py`](sqpack/canonical.py) | yes | Tolerance grouping and exact hash pairs do not form a stable equivalence relation ([D-048](defects.md)); canonicalization is factorial on sparse symmetric endpoints ([D-049](defects.md)) |
| [`sqpack/atlas.py`](sqpack/atlas.py) | yes | Promotes non-converged stopping points and cannot reconstruct discovery order ([D-050](defects.md)); frequencies merge without regime or identity provenance ([D-051](defects.md)) |
| [`tools/basin_census.py`](tools/basin_census.py) | yes | An admissible `BasinEvent/v3` event certifies the producer contract and a terminal outcome, not a terminal component—identity stays blocked ([D-034](defects.md), [D-048](defects.md)). The twelve historical v2 poses remain inadmissible under the since-fixed [D-165](defects.md) |

**`distinct_basins` is a count of endpoint keys, not of connected terminal components.**
The exact `n = 3` sliding family shows one connected optimal set producing many keys, so
the store can split a single component.
Until [D-034](defects.md) is resolved the discovery curve cannot plateau, the census
cannot saturate, and the rarity premise is **untestable rather than untested**.

Cheap endpoint summaries such as angle signatures and contact counts exist.
A validated terminal-component descriptor interface is unbuilt, so steering strategies
that depend on component identity or descriptor distances remain unbuilt too.

### The promotion pipeline—unbuilt, and it is the largest structural gap

There is **no executable path from a numerical candidate to a reconstructible exact
result.** The repository can verify a packing whose exact algebraic description it is
already given; it cannot produce that description from a packing it found.

Concretely, none of the following exists: corner–edge incidence classification from a
polished pose (the quench records which *pairs* touch, not which corner meets which
edge), contact-equation assembly, rank-closure of an underdetermined system,
high-precision root-finding, algebraic recognition, interval uniqueness, or certificate
emission. The tracked acceptance criterion is that, **starting only from archived
floating poses**, one command recovers or explicitly rejects `n = 5, 10, 11, 17` and
several rational-grid controls, and records recognition failures rather than guessing.

Two consequences bind every other lane:

- **`exact` currently means “checked something already known exactly”.** Every exact
  configuration here—Trump’s packing, the `n = 3` and `n = 4` optimal families—was
  authored from published data or derived analytically; none was recovered from a
  numerical search output.
- **No admissible endpoint exists at an open `n`, so the pipeline would have nothing new
  to promote.** The early quench archives (exp-006 through exp-009) retain angles and a
  contact *count* but not centres; the twelve historical v2 poses remain inadmissible
  under the since-fixed [D-165](defects.md).
  The latest complete `BasinEvent/v3` control blocks contain four admissible events at
  `n = 3` (exp-021 and exp-022) and four at `n = 4` (exp-024); exp-023 preserves the
  earlier three-of-four n=4 block that exposed D-171. They are all at proved values, so
  they are known-answer material for the pipeline, not candidates.

The record corpus has the same shape of gap: [`frontier/`](frontier/README.md) records
each case’s **side value** algebra—minimal polynomials where they are published—and **no
geometry**. An importer for the catalogue’s layouts is unbuilt.

### The proof lane—built and producing theorems

This is the lane that moved furthest in the most recent rounds: it now carries exact
results, not only instruments.

| Tool | What it establishes |
| --- | --- |
| [`tools/check_stromquist_theorem2.py`](tools/check_stromquist_theorem2.py) | The printed `n = 11` lower-bound proof is false as printed (exp-016) |
| [`tools/check_stromquist_repair.py`](tools/check_stromquist_repair.py) | A source-distinct repair certifies `s(11) ≥ 2 + 4/√5` exactly (**T-4**, exp-017) |
| [`tools/check_trump_tangent.py`](tools/check_trump_tangent.py) | Trump’s pose is locally isolated in the anchored chart (exp-013) |
| [`tools/check_small_n_moduli.py`](tools/check_small_n_moduli.py) | Exact optimal configuration spaces at `n = 3, 4` (exp-014, exp-015) |
| [`tools/check_kingbird_svg.py`](tools/check_kingbird_svg.py) | High-precision (160-digit) numerical reconstruction of the `n = 29` record source, refuting H-024’s three-class claim. Not an exact optimality certificate—the retained SVG is numerical, and exp-012 says so (exp-012) |

**Unbuilt on this lane:** the `PoseBox` scalar and the interval branch-and-bound hook,
LP duals as unavoidable-set generators, and any Lean formalization.

### Compiled acceleration—unbuilt, deliberately

`sqpack-core`, the filtered kernel, the FLINT-backed algebraic scalar, and the language
bindings are all unbuilt.
That is a scheduling decision made by measurement rather than an omission: the current
pipeline is quench-dominated, and moving only the geometry kernel to another language
would not remove the measured LP-solver and wrapper cost.
Direct solver bindings or a compiled batch path may still matter; the phase begins by
re-measuring and builds only what the profile names.

### Reading the gate

`./test.sh` runs thirty steps.
A green gate means every *built* component behaves as its checks describe; it says
nothing about the unbuilt ones, and it does not upgrade an inadmissible output.

**The gate is not environment-independent.** Endpoint identity depends on floating-point
behaviour in a degenerate linear program, so the same seed can reach a different
endpoint under a different toolchain, and a check written around one observed endpoint
can fail elsewhere. Separating portable mathematical predicates from stochastic
characterization is open work ([D-059](defects.md)).

## Terminology

These words are used in a narrow sense throughout this directory, the campaign
artifacts, and the beads.
Two of them carry more than one sense—**cell** and **quench**—and for each, the rule for
which to write is stated with the definition.
Nothing below is a synonym for anything else below.

### The objects

**Configuration.** A placement of all `n` squares: a centre `(xᵢ, yᵢ)` and an angle
`θᵢ ∈ [0, π/2)` for each, together with a container side `s`. That is `3n + 1` real
coordinates, 34 at `n = 11`. A configuration is *valid* when the interiors are pairwise
disjoint and all squares lie in `[0, s]²`; touching is valid.

**Cell**—always a *cell of configuration space*: a choice, for each of the `C(n,2)`
pairs, of one candidate separating axis together with an order (which square is on the
low side). A configuration *lies in* a cell when those choices genuinely separate those
pairs in that order.
Fixing the angles and a cell turns the problem into a linear program; that is
[T-2](#the-cell-decomposition).

**Instance cell**—an `n` carrying a declared role in the sweep: `n = 10` positive
control, `n = 11` target, `n = 12` open-case calibration, `n = 17` mechanism-matched
calibration.
A **control cell** is an instance cell whose answer is known before the run,
and a breach of one rejects the round regardless of outcome.

> The two senses collide, and both appear in this document.
> **Write “cell” for the configuration-space object and “instance cell”—never bare
> “cell”—for a sweep position.** In running prose about a round, prefer naming the `n`.

**Basin (point-basin where the distinction matters).** The preimage of one pose returned
by a deterministic quench: the set of configurations the refiner carries to that
numerical endpoint. A point-basin is therefore defined *relative to a specific quench*,
which is why basin identity may not inherit the search’s tuning parameters—a quench that
merged nearby angles would make the word depend on the merge tolerance
([D-020](defects.md)). The current quench gives each terminal pose a reproducible
numerical candidate, but that does not make the terminal set discrete or decide whether
two candidates belong to one connected component.
D-021 bounds error in the scalar side only; it is not a pose- or component-resolution
theorem ([D-039](defects.md)).

**The point-basin exists, but it can be the wrong counted object.** A deterministic
quench returns a pose even when that pose lies on a connected terminal family.
Different neutral coordinates then produce different point-preimages and keys inside one
terminal component. D-034 records why a component census must quotient that family using
independently validated connectivity rather than declare the quench map undefined.

**The ladder.** The proved instances used as controls—`n = 5` and `n = 10`, both `45°`
mechanisms with closed-form optima.
The ladder validates *machinery*: no proved case exercises an irrational oblique angle,
so passing it says nothing about strategy at `n = 11`.

### The operations

**Quench.** Two senses, both in use, and they do not conflict.
As a *map*, in Stillinger and Weber’s sense: the function sending a configuration to the
local optimum a deterministic refinement carries it to.
As a *component*, [`sqpack/quench.py`](sqpack/quench.py): this project’s implementation
of that map—solve the LP in the current cell, move the angles, re-solve, until fixed.
Say “the quench map” where the distinction matters.

**Polish.** Refinement *within* the basin a configuration is already in—driving the side
down to the local optimum without changing which local optimum that is.
This is what the quench does, and all it does.

**Exploration.** Reaching a different basin.
No amount of polish performs it, and nothing currently in the toolkit does it reliably
at `n = 11`.

**Proposer** and **refiner**. The two halves of the loop, named separately because the
measurement that matters is which one is failing.
The proposer emits candidate configurations (today: the `sqsearch` annealer); the
refiner is the quench.
Building a better refiner cannot fix a proposer failure.

**Angle class.** A set of squares constrained to share one angle.
Trump’s packing has two classes at `n = 11`: six squares at `0°`, five at `a*`. **Class
bracketing** is the angle search that optimises over merged classes by bracketing rather
than by gradient, which is what a corner requires; `class_tol` is the tolerance that
decides which angles merge into one class.

**Corner** (equivalently *kink*). A point where the LP optimum as a function of the
angles has distinct one-sided derivatives, so no method assuming a smooth local model
converges to it. Measured at `n = 11`: `0.1747` and `0.384` per radian, through two
independent implementations ([T-3](#the-corner-and-the-method-it-forced)). Not a synonym
for “sharp minimum”—the derivative does not become large, it fails to exist.

**Rigidity.** A packing that has no non-trivial feasible infinitesimal or local motion
under the declared quotient and container condition.
Contact counts and visual pinning are candidates for this property, not proofs; they
require an active-constraint rank or stronger local certificate.
Exp-013 supplies that stronger certificate for Trump’s packing: every complete
branchwise fixed-side linearized cone is zero, and a finite-branch argument proves local
isolation. It does not quantify the neighborhood or prove global optimality.

**Terminal family** (called a *flat basin* in older campaign prose).
A local-optimal terminal set that is not an isolated point.
Its local dimension is the nullity of the appropriate independent active-constraint
Jacobian after quotienting symmetries and accounting for inequalities and stratum
changes. Raw contact counts cannot supply that rank: contacts may be dependent, one
contact description may encode several scalar conditions, and angles and separating
cells may change along a motion.

At `n = 3`, the exact family with centres `(1/2,1/2)`, `(3/2,1/2)`, and `(t,3/2)` for
`t ∈ [1/2,3/2]` proves that terminal continua occur and that the current endpoint key
splits one connected optimum component.
At `n = 5`, two rows share side and contact summaries but differ geometrically.
That is an unresolved identity signal, not a proof of a five-dimensional connected
family ([D-034](defects.md), [D-041](defects.md)).

**This distinction should have existed from the first day.** “Rigidity” was treated as
an informal visual property of the target while the census silently assumed every
terminal was isolated.
The exact `n = 3` control falsifies that assumption directly.
That is a documentation failure before it is a code one, and it is why
[D-034](defects.md) was found by reading a census output rather than by reading the
plan.

### The measurements

**Gap.** Always `best_side − standing_best`, in units of the container side, and always
signed. A *negative* gap below the `exact` tier is solver noise, never a discovery.

**Standing best.** The best side ever published for that `n`, read from
[`frontier/`](frontier/README.md)—an upper bound, and for the open cases not known to be
optimal. Distinct from the **analytic optimum**, which exists only where the case is
proved. At `n = 5` and `n = 10` they coincide; at `n = 11` the standing best is Trump’s
construction and the optimum is unknown.

**Polish failure** and **exploration failure.** The decomposition of a gap, and the
campaign’s central diagnostic.
A **polish failure** is a gap that the declared refiner closes, as `n = 10` was, from
`4.19e-04` to `1.33e-15`. An **exploration-or-model failure** is a gap that remains
after that local procedure, as the tested `n = 11` starts did, from `8.85e-02` to
`6.29e-02`. Neither numerical behavior proves a terminal-component relation.
“Right basin” and “wrong basin” require the component evidence tracked by H-021 through
H-023.

**`reached_basin`.** A recorded outcome meaning `best_side − standing_best < 1e-4`. It
is a **numerical proxy** for “found the right combinatorial class”, not evidence of
it—establishing the class means comparing contact graphs.
A round claiming `reached_basin` must say which it means.

**Pair-test.** The budget currency: one evaluation of one pair of squares for overlap.
Machine-independent, unlike wall clock or moves, which is why proposer comparisons are
denominated in it. Tiers S/M/L are `1e9`/`1e11`/`1e13`.

**Evidence tier.** What a number is permitted to claim, fixed by how it was produced:
`f64_screen` (a candidate was proposed), `polished` (a quench endpoint candidate was
valued to solver precision—a floor of about `1e-11` in the side, [D-021](defects.md)),
`exact` (validity decided over the packing’s own number field).
**`beat_record: true` may be written only at `exact`.** Never extrapolate across a tier
boundary. The tiers are set out in full under
[Theoretical Results](#theoretical-results).

### Not used here

Two coinages appear in side work and are deliberately **not** adopted, because the
project already has clearer words for both.

- **“polish gap” / “exploration gap.”** Write **polish failure** and **exploration-or-
  model failure** for the scoped procedure outcome.
  Reserve *right basin* / *wrong basin* for a state supported by a declared
  terminal-component relation.
  A gap is a number; whether it is polish or exploration is a *conclusion about* that
  number, and the two-word compound hides the inference.
  Neither compound occurs anywhere in this directory and neither should start.
- **“the quench” for a fixed-angle solve.** A quench includes its angle half.
  See
  [A cell is not a basin](#a-cell-is-not-a-basin-and-this-trap-has-been-walked-into)—the
  conflation cost a correct finding ([D-029](defects.md)).

### The deliverables, and what each one currently is

These four words name the cartography strategy’s intended outputs.
Two now have code behind them and two do not, and neither pair has yet produced the
object the word promises.
[What Is Built](#what-is-built) is the component-level view.

**Atlas.** The deduplicated store of known basins for an `n`, keyed by canonical basin
identity. The stated deliverable of the cartography strategy.
*Code exists; it stores endpoint keys, which are not certified terminal components.*

**Census.** An enumeration of the basins at one `n`, run to saturation.
*Code exists; saturation is unreachable while the thing being counted is undefined.*

**Descriptors.** Structural coordinates of a packing—contact counts, angle classes,
symmetry—used to steer search toward diversity rather than toward loss.
*Unbuilt, and every steering strategy waits on them.*

**Meter.** The instrument that counts pair-tests, so two proposers can be compared at
equal budget. *Unbuilt, so no two proposers have been compared at equal budget.*

### The record

**Round.** One executed experiment against one registered hypothesis, with a declared
timebox and a pre-registered accept rule, recorded as a schema-validated artifact plus
its JSONL archive.
**Series.** An ordered group of rounds sharing a runbook; only one may
be open at a time.

**Soundness perimeter.** The rule that every component emitting a configuration is
checked by `sqpack` through code it does not share, enforced by
`tools/perimeter_test.py`. A component joins it in the same change that introduces
it—not doing so is how [D-014](defects.md) was possible.

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
| Best certified lower bound | `2 + 4/√5 = 3.788854382…` | exp-017 exact source-distinct repair; value stated by Stromquist 2003, whose printed proof has gap D-152 |
| Published gap | `0.088229208023` | the fourth-smallest open gap at `n ≤ 100` in this corpus |

The current audit found an explicit strict box avoiding all twelve printed Figure 14
points, so the paper’s unavoidability subclaim is false as printed
([D-152](defects.md)). Exp-017 independently certifies the same numerical inequality by
moving only `G=(.8,1.85)` to the source-distinct `G'=(.79,1.85)` and replaying the
complete finite cover and capacity argument.
The repaired coordinate and certificate are results of this repository, not claims
attributed to Stromquist.

Trump’s packing is six axis-aligned squares plus a block of five tilted at
`a* ≈ 40.181937290329714°`. The container side is an algebraic number of degree 8, the
root of

```
s⁸ − 20s⁷ + 178s⁶ − 842s⁵ + 1923s⁴ − 496s³ − 6754s² + 12420s − 6865 = 0
```

lying in `[3.87, 3.88]`. Exp-013 exactly certifies every complete branchwise fixed-side
linearized cone and proves the pose locally isolated by a finite-branch subsequence
argument. This qualitative local theorem does not provide an explicit radius or explain
the global search difficulty.

### Why exactness is not optional

Disjoint *interiors* means touching is legal, and record packings touch a great deal.
In Trump’s packing 14 of the 55 pairs are separated by exactly zero, and 20 corner
coordinates lie exactly on the container boundary.

Floating-point evaluation can certify a strict inequality when a sound error bound stays
away from zero. It cannot infer that an unrecognised near-contact is exactly equal to
zero merely because a computed residual is small.
A tolerance-based f64 verifier therefore needs a tolerance to accept Trump’s rounded
algebraic contacts, and that tolerance is a blind spot that also accepts overlaps
smaller than itself; setting it to zero rejects this true packing instead.
Both failure modes are demonstrated by `negative_control.py`.

The fix is representational rather than numerical: express the configuration in the real
algebraic number field it actually lives in, where equality is decidable.
That is what `sqpack` does, and it is why the evidence tiers below make `exact` the only
tier permitted to say **record**.

This is not an abstract concern.
The same failure reappeared *inside the refiner* eight rounds later: an LP solver at its
default tolerance returned a packing violating its own separation constraint, and so a
side below Trump’s ([D-014](defects.md), critical, caught by the pre-registered rule
that beating the record means you have a bug).

## The Lay of the Land, by `n`

Where the program has spent effort, and what came of it.

| `n` | Status | Standing best | Role here | What has been done |
| --- | --- | --- | --- | --- |
| 5 | proved, `2 + ½√2` | `2.70710678…` | positive control | `sqsearch --selftest` recovers it on every run. [exp-007](campaign/series/series-000-smoke-and-calibration/experiments/exp-007-quench-bracket-n5.md): the bracketing quench refines annealer output to `2.22e-15`—the analytic value to machine precision |
| 8 | proved, `3` | `3` | census kill line | The `n` at which [H-011](campaign/hypotheses/H-011-small-n-census.md)’s discovery curve must plateau, or enumeration is abandoned. No rounds |
| **10** | **proved**, `3 + ½√2` | `3.70710678…` | **positive control** | Four rounds. The annealer stops `4.19e-04` short ([exp-002](campaign/series/series-000-smoke-and-calibration/experiments/exp-002-baseline-n10-positive-control.md)); angle descent barely helps; [exp-008](campaign/series/series-000-smoke-and-calibration/experiments/exp-008-quench-bracket-n10.md) closes it to `1.33e-15`—**twelve orders** |
| **11** | **open** | `3.87708359…` (Trump 1979) | **target** | Exact verification over `ℚ(u)` (**T-1**); the cell decomposition (**T-2**), corner (**T-3**), and repaired lower-bound certificate (**T-4**); nine rounds. Search remains `≈ 6e-02` short, exp-013 proves Trump’s exact pose locally isolated, exp-016 rejects Stromquist’s printed proof, and exp-017 independently restores its numerical bound |
| **12** | open; `4` believed optimal | `4` | **open-case calibration** | Two rounds. Returns exactly `4.0` on all five seeds, which is baseline evidence rather than a known-answer guard. Also where the search and proof lanes are planned to meet |
| 16 | proved, `4` | `4` | proved not-below control | The valid replacement for the old `n=12` guard: any reported side below `4` is known to be invalid |
| 17 | open | `4.67553009…` (Bidwell 1998) | mechanism-matched calibration | The nearest case whose record uses genuinely oblique structure—tilts of `0°`, `+39.80496°`, and `−36.62379°`. One round: [exp-011](campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md) reports `5.0`, the trivial `5×5` grid, on all five f64-screen seeds |
| 61, 78, 97 | open, `m² − 3` | `8`, `9`, `10` (grids) | opportunistic slot | The narrowest gaps in the table. An analytic Cleemann-style attempt at `arctan(3/4)` is registered and **not yet made** |
| 1–100 | 35 proved, 65 open | — | the corpus | One schema-validated artifact per case in [`frontier/`](frontier/README.md); 63 of the 65 open cases are bounded below by Nagamochi’s general theorem |

Three facts about this table drive the strategy.

**Every proved case in the ladder is a 45° mechanism.** `n = 5` and `n = 10` are
symmetric arrangements that blind search reaches without help.
`n = 11` needs an oblique core at an irrational angle, which **no proved case
exercises**, so the ladder validates *machinery*, not *strategy*.

**The ladder now discriminates sharply, and the target does not move.** The bracketing
quench takes `n = 5` and `n = 10` to machine precision and leaves `n = 11` essentially
where the annealer put it.
That is the cleanest statement of where the difficulty lives: the refiner is not the
problem.

**`n = 17` adds one mechanism-matched negative result.** It was the only registered
instance cell testing record-*finding* rather than machinery, and it was the last one
never run.
[exp-011](campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md)
ran it: the annealer reports `5.0` on all five f64-screen seeds—the trivial `5×5`
grid—against Bidwell’s `4.67553`, a gap of `+0.324`. The retained final states do not
leave the grid basin.

That scopes one failure at a second cell: this implementation, five seeds, and the
registered `1e8` moves per chain did not reach Bidwell’s oblique record at `n = 17`. The
retained final best does not show which orientations the trajectory visited, and a
single budget cannot establish that no larger budget or related proposer can reach
oblique records as a class
([H-020](campaign/hypotheses/H-020-oblique-record-finding-n17.md)).

## Theoretical Results

Status is recorded on the same tiers the campaign uses for measurements, so a claim’s
evidential standing is never ambiguous.

| Tier | Meaning |
| --- | --- |
| **proved** | A mathematical argument, checkable by reading |
| **exact** | Decided by exact arithmetic over the relevant number field; a proof, mechanised |
| **polished** | An LP cell optimum at *solver* precision—about `1e-11` in the side, and no better ([D-021](defects.md), open) |
| **verified (f64)** | Computed in floating point; strong evidence, not a proof |

### Results relied on from the literature

Cited near the claims they support in the
[`n = 11` report](docs/project/research/research-2026-08-22-packing-11-unit-squares.md);
listed here so the dependencies of this program are explicit.

- **`s(10) = 3 + ½√2`**, Stromquist 2003, Theorem 1. Ten unavoidable points, then case
  analysis. Not pigeonhole alone.
- **The published statement `s(11) ≥ 2 + 4/√5`**, Stromquist 2003, Theorem 2. D-152 and
  exp-016 give a strict counterexample to the printed Figure 14 unavoidability claim, so
  the published proof is not relied on as complete.
  The same inequality is established independently as **T-4** below, using H-041’s
  separately preregistered source-distinct repaired point set.
- **`s(11) ≤ 3.877083590022814…`**, Trump 1979, by construction.
  Every upper bound in this subject is a construction; no non-constructive upper bound
  has ever been obtained.
- **The `0°`/`45°` class cannot achieve it.** Stromquist bounds that orientation class
  below at `2 + (4/3)√2 ≈ 3.885618`, which Trump’s oblique packing beats.
  This makes `n = 11` the first case where genuinely oblique tilt is proved to improve
  on the `0°`/`45°` class, and is the sharpest available statement of why the target
  differs structurally from the ladder.

### Results established here

| Id | Statement | Tier | Where it lives | Reproduce with |
| --- | --- | --- | --- | --- |
| **T-1** | Trump’s 1979 packing is valid: 11 unit squares in a square of side `s`, the degree-8 algebraic number above, with 14 of 55 pairs touching at exactly zero separation and 20 corner coordinates exactly on the boundary | **exact** | `sqpack` | `python3 verify_trump11.py` |
| **T-2** | Fixing every angle and every pair’s separating axis reduces the problem to a **linear program** in the centres and the side. All nonconvexity lives in the angles and in the combinatorial choice of cell | **proved**; instantiated at **polished** | [R-2](docs/project/reviews/review-2026-08-23-toolkit-docs-and-first-experiments.md#r-2), built as [`sqpack/quench.py`](sqpack/quench.py) | `uv run --frozen python lp_cell.py` |
| **T-3** | On Trump’s fixed contact cell, the one-dimensional LP optimum obtained by varying the five tilted squares’ shared angle has a **corner** at the published tilt—distinct one-sided slopes—so a smooth local model is misspecified on that slice | **verified (f64)** | [H-019](campaign/hypotheses/H-019-angle-optimum-is-a-kink.md), confirmed by [exp-010](campaign/series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md) | `uv run --frozen python lp_cell.py` |
| **T-4** | The source-distinct replacement `G=(.8,1.85) → G'=(.79,1.85)` restores the complete Figure 13 localization, A-triple forcing, repaired Figure 14 unavoidability, and `3+9` capacity chain, proving `s(11) ≥ 2 + 4/√5` | **exact** | [H-041](campaign/hypotheses/H-041-repaired-stromquist-point-set.md), confirmed by [exp-017](campaign/series/series-000-smoke-and-calibration/experiments/exp-017-h-041-stromquist-repaired-figure14.md) | `uv run --frozen python tools/check_stromquist_repair.py --replay campaign/series/series-000-smoke-and-calibration/results/exp-017-h-041-stromquist-repaired-figure14.json` |

**T-1** is also an independent check of the published record: the 33 digits on the
*Squares in Squares* record page agree with the value computed here from the field.
No other public tool is known to check a record packing exactly, and the 14 zero-gap
pairs are precisely the ones no floating-point verifier can decide.

**T-2** originated in the standing review as observation R-2 and has now been
implemented twice, independently—see below for why that matters.
**T-3** was found while building the quench, registered as `H-019` *before* the round
that observed it was recorded, and confirmed as its own round.
Under the directory’s ownership rule the registry artifact decides both; the `T-` ids
here are this document’s shorthand.

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
> is a linear program in the `2n + 1` variables `(x₁,…,xₙ, y₁,…,yₙ, s)`.

### Why

Four observations, each immediate once the angles are fixed.

1. **Corners are affine in the centres.** Corner `k` of square `i` is `(xᵢ, yᵢ) + oᵢₖ`
   with `oᵢₖ` constant.
2. **Containment is linear.** Each corner must satisfy `0 ≤ xᵢ + oᵢₖ,ₓ ≤ s` and
   `0 ≤ yᵢ + oᵢₖ,ᵧ ≤ s`. Note that `s` appears here, and only here, as a variable.
3. **Separation along a *fixed* axis is linear.** For axis `ν` and order `(i before j)`,
   separation says every corner of `i` projects at or before every corner of `j`:
   `⟨ν, (xᵢ,yᵢ) + oᵢₖ⟩ ≤ ⟨ν, (xⱼ,yⱼ) + oⱼₗ⟩` for all `k, l`. Since `ν` is a constant
   vector, each is a linear inequality in four of the variables.
4. **The objective is linear**, being `s` itself.

The nonlinearity of the original problem is entirely in two places: the trigonometric
dependence of `oᵢₖ` and `ν` on the angles, and the *discrete* choice of cell.
Neither is present once both are fixed.

Note what the statement does **not** claim.
The LP optimises within one cell.
A different cell may have a lower optimum, and finding the best cell is the
combinatorial part of the problem, which none of this makes easy.

### A cell is not a basin, and this trap has been walked into

The statement above fixes the angles and a cell.
A **point-basin** does not: it is the preimage of a quench endpoint, and the quench
moves the angles and may cross cells.
So a configuration can sit at exactly its fixed-angle cell optimum and still be far from
its quench endpoint, with every remaining unit of gap in the angles and none of it in
the centres.

### Nor does a point-basin classify a flat terminal component

The section above separates a fixed-angle cell solve from the full quench.
There is a second separation, discovered later and the harder of the two: the quench
returns a point, while [the terminal optimum need not be isolated](#terminology).

Where the optimum is flat, two quenches into the same connected terminal component can
legitimately stop at different places in it.
Every symptom then mimics a real discovery—distinct coordinates, distinct geometric
keys, two rows in the atlas—while the side agrees exactly and an open stratum can share
one contact graph. Neither the key nor that graph alone decides component identity; wall
strata can change inside the same connected family.
That is [D-034](defects.md), and the shape of the error is the same as the cell/basin
trap: an object that fixes more than the mathematics does, mistaken for the mathematics.

The consequence is a reading that looks safe and is not: **a fixed-angle solve that
stops improving has not converged to a local optimum of the problem—it has run out of
things it is allowed to move.** Watching it flatten and concluding “wrong basin” is
exactly backwards, and it is what the right basin looks like when the residual is
angular.

That is not hypothetical.
Checking exp-001’s polish/exploration split, an agent built a probe doing one LP solve
at fixed angles, called it “the quench”, and retracted a correct finding when it stalled
([D-029](defects.md)). On exp-002’s seed 2:

|  | gap to `s(10) = 3 + ½√2` |
| --- | ---: |
| annealer output, as found | `+5.6440e-04` |
| fixed-angle solve, carried to its cell fixed point | `+5.6440e-04`—*no improvement at all* |
| `quench_bracket`, with the angle half | `+4.4409e-16` |

**“Quench” names all three stages**—solve the cell, re-read the cell to a fixed point,
refine the angles. The cell solve alone is one third of it and answers a different
question. `tools/regression_test.py` pins this discrimination under D-029.

### Two implementations, on purpose

The row count depends on how separation is written, and this directory now has both
forms:

| Implementation | Separation rows per pair | Total rows at `n = 11` |
| --- | --- | --- |
| [`sqpack/quench.py`](sqpack/quench.py) | 1, from projected half-extents | small |
| [`lp_cell.py`](lp_cell.py) | 16, one per ordered corner pair | 1,056 = 16 × (11 + 55) |

Both are correct formulations of the same feasible set, and neither shares
constraint-assembly code with the other.
That redundancy is deliberate, and it is the postmortem’s rule **R1**: *a component
checked against its own model of correctness is checked against the thing most likely to
be wrong.* [D-014](defects.md) happened precisely because the quench was validated only
against its own constraint rows.

### The instance: Trump’s cell

`lp_cell.py` reads the cell off `sqpack`’s exact certificate—eleven angles and
fifty-five axis choices, and nothing else—rebuilds the LP from scratch, and solves it.
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

`sqpack.quench`’s single-cell solve at the same angles agrees to the digit—`4.441e-16`,
recorded as a mechanism result of
[exp-006](campaign/series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md).
**The cell containing Trump’s packing, solved as a linear program, is Trump’s packing**,
through two unrelated constraint sets.

### What “exact” does and does not mean here

The formulation is exact; the *build* is not, and conflating the two caused a critical
defect. Three corrections, recorded in the
[plan spec’s revision note](docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md):

- **A float LP solver does not deliver the cell optimum.** At its default primal
  feasibility tolerance of `1e-7` HiGHS returned a packing violating its own separation
  constraint by `9.876e-08`, and so a side below Trump’s ([D-014](defects.md)). Pinned
  at the solver’s floor of `1e-10`, and with every returned solution post-checked
  against the constraints imposed on it, the residual in the side is about `1e-11`. That
  floor is [D-021](defects.md), still open, and eight rounds sit on it.
- **The polish step does not produce exact output.** R-2 said it produced rational
  output; HiGHS returns floats.
  Exact output needs an exact LP over the cell’s certified rational or algebraic
  coefficients, which is unbuilt and tracked.
- **The `polished` tier means exact within a cell to solver precision.** Algebraic
  exactness stays with `sqpack`, and every promotion routes through it.

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

Trump’s angle is not an input to this computation.
It is **the argument that minimises a one-dimensional function anyone can plot.** For
this structured cell, the centre coordinates remain LP variables and only one nonlinear
angle parameter remains.
This demonstrates a useful compression, not a theorem that angle-class count equals the
local dimension of the full packing problem; other records already use more classes, and
each reduction must be derived from its contact structure.

## The Corner, and the Method It Forced

The most useful result the campaign has produced, because it is a full loop: a
measurement, a mechanism, a prediction, and a method built on the prediction that works.

### The measurement

`φ` is not smooth at its minimum.
Measuring one-sided slopes and refining the step:

| `h` (deg) | left, per deg | right, per deg | left, per rad | right, per rad |
| --- | --- | --- | --- | --- |
| `1e-02` | `3.049623e-03` | `6.702833e-03` | `0.1747` | `0.3840` |
| `1e-03` | `3.049503e-03` | `6.700977e-03` | `0.1747` | `0.3839` |
| `1e-04` | `3.049491e-03` | `6.700791e-03` | `0.1747` | `0.3839` |
| `1e-05` | `3.049490e-03` | `6.700772e-03` | `0.1747` | `0.3839` |

Both converge, and they converge to **different** values, ratio `2.1973`. The derivative
does not vanish at `a*`; it jumps.

[exp-010](campaign/series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md)
measured the same quantity through `sqpack.quench`—a different LP formulation, a
different code path—and recorded `0.1747` and `0.3841`, ratio `2.198`, stable over five
decades on each side.
Two implementations, one number.

### The mechanism

Where the LP’s optimal basis is locally constant, `φ` is smooth and its derivative is
read off the active constraints.
A corner is a **change of optimal basis**: the set of contacts that bind switches as `a`
crosses `a*`. The switch at the minimum establishes a kink in this one-dimensional
class-angle objective.
It does not by itself prove rigidity of the full packing; that requires ruling out every
other feasible motion, not just motion along this slice.

### The prediction, and what it cost to ignore

A kink invalidates derivative-based smooth local models, but does not imply that every
derivative-free method must fail.
In this implementation and from these starts,
[exp-006](campaign/series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md):
finite-difference descent stalled five orders short, and **Powell and Nelder-Mead both
did worse than descent** (`+1.06e-02` and `+3.34e-06` against descent’s `+2.78e-07`).

### The method, and what it bought

Replace the smooth descent with a **bracketing search over merged angle classes**—a
method that tolerates non-smoothness—and hold everything else fixed.
On the same annealer output:

| `n` | annealer | + angle descent | + class bracketing |
| ---: | ---: | ---: | ---: |
| 5 | `3.4274e-08` | `3.1875e-08` | **`2.2204e-15`** |
| 10 | `5.318e-03` | `4.507e-03` | **`1.3323e-15`** |
| 11 | `8.846e-02` | `6.999e-02` | `6.2894e-02` |

Seven orders at `n = 5` and twelve at `n = 10`, from changing only *how the angle half
searches*. At `n = 5` both quenches find the same contact structure and the same two
angle classes, so the difference is entirely in whether the search can land on the
corner.

This is strong method-selection evidence, not a convergence theorem.
The successful bracketing run and the failed tested alternatives justify the current
implementation choice; [H-019](campaign/hypotheses/H-019-angle-optimum-is-a-kink.md)
does not prove that every derivative-free method fails or that bracketing is necessary.

### And what it did not buy

Nothing at `n = 11`. The bracketing quench moves the target from `8.85e-02` to
`6.29e-02`
([exp-009](campaign/series/series-000-smoke-and-calibration/experiments/exp-009-quench-bracket-n11.md)),
against machine precision on both proved instance cells.
The tested starts remain far from Trump’s construction after the local procedure.
An LP-in-cell solve is local: it returns the best packing in the cell it is given.
That explains the lack of rescue without deciding whether the endpoints belong to a
distinct terminal component.

### Other consequences

- **The refiner is an LP solve per cell**, at solver precision, and it is built.
  That is the campaign’s middle tier, and it is real.
- **Basins become nameable.** A local minimum stops being tolerance-dependent and
  becomes a discrete object with a side length good to `≈1e-11`, which is what makes a
  census, an atlas, and basin statistics well defined.
  Basin identity must not inherit the search’s knobs—a quench that merges nearby angles
  would make “basin” depend on the merge tolerance ([D-020](defects.md)), fixed by a
  free-angle pass that certifies the landing point.
- **The search space factorises** into a small continuous part (the angles) and a
  combinatorial part (the cell), which is the premise of
  [H-001](campaign/hypotheses/H-001-angle-class-reduction.md)—now with a concrete prior,
  since the class-constrained search reached the solver floor in **70 LP solves** where
  free descent needed **1,024** and landed five orders worse.
- **Rational-slope tilts would need no number field.** At a Pythagorean angle such as
  `arctan(3/4)` every coordinate and the cell optimum are rational, so exact
  verification would be `ℚ`-arithmetic at degree 1. Realising that needs the exact
  rational LP, which is unbuilt.

### Reproducing all of it

```bash
cd explorations/packing
python3 verify_trump11.py       # T-1: exact verification over Q(u)
uv run --frozen python lp_cell.py        # T-2 and T-3, through independent constraint rows
uv run --frozen python run_quench.py     # the campaign's own quench, both angle methods
./test.sh                       # all of the above, plus every other gate
```

`lp_cell.py` asserts every figure quoted above, including agreement with `H-019`’s
registered slopes, so a change that breaks one fails the gate rather than silently
editing the record.

## The Program So Far

Deliberately historical: it records the order in which things were done and why, because
several decisions were made by measurement and the measurements are why later work is
shaped as it is.

**Establish the frontier, then the mathematics.** The `n ≤ 100` corpus was built first,
one validated artifact per case, so that “the standing best” is a fact read from a file
rather than a number retyped into a paragraph.
Retrieving the primary sources corrected the record in ways secondary summaries had not:
one widely-repeated explicit constant appears in no primary paper at all.
That episode is why the grounding rule for every later lane is that nothing enters a
prompt or an artifact unverified.

**Build the exact verifier before the search.** Rigidity means a float check cannot
decide record packings, and the tolerance blind spot is a correctness concern rather
than a rounding one.
`sqpack` was written, validated against Trump’s packing (**T-1**), and given a negative
control demonstrating both float failure modes.

**Price the stack rather than argue it.** The pipeline spans seven orders of magnitude,
from a `0.025 µs` annealer move to a `129 ms` exact verification, and its middle—the LP
quench at `1.28 ms`—is where nearly every planned strategy spends its time, at the same
rate in any language.
So the spine is Python, and compiled code is deferred to a phase scoped by a profile of
a campaign that has actually run.

**Write the search engine; two formulations failed first.** Fixing a container side and
asking whether the squares fit needs an outer loop that decides when an anneal has
failed, and it starts from the trivial grid, which is exactly jammed.
Two versions were built and measured: the first crawled, the second never left the grid
basin ([D-001](defects.md)). The replacement removes the container from the variables,
minimising `required_side + λ·total_overlap` with a linear penalty.

**Run the baseline, and discover the instrument was lying.** A restart cap stopped every
chain before the declared move budget did, so `--budget-moves` was inert and two
strategies compared “at equal budget” would have had unequal work ([D-002](defects.md)).
The tell was that results got *worse* at a larger declared budget.

**Add the method, and find the missing stage.** A standing review audited the toolkit
documents and found that all of them presumed a refinement stage none of them built.
In looking for it, the review found **T-2** and supplied the experimental method the
project lacked: a hypothesis register with kill criteria written before the run, a run
protocol, and a seven-series plan.

**Adopt a strategy, and register the premise so it can fail.** Record packings may be
unusually constrained and may have low hit probability under specified baseline
proposers. If so, scaling the same proposer multiplies effort against the measured
probability. Because the whole strategy rests on that argument, the measurement that
would refute it ([H-012](campaign/hypotheses/H-012-record-basins-are-rare.md)) is
registered in the cheapest tier and scheduled early.

*Ask what the premise silently assumes about its denominator.* Optima need not be
isolated: the exact `n = 3` terminal family proves that one connected optimal component
can produce many endpoint keys.
So the census that is supposed to establish rarity is counting representation-dependent
objects, and the denominator of “rare” is not yet a number ([D-034](defects.md)). The
premise may well be true.
It is not yet *measurable*, which is a stronger objection than doubting it.

**Ask whether the basin has a wall, and get a better question back.**
[exp-005](campaign/series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md)
started *inside* Trump’s packing and walked outward.
There is no wall to find: the return distance is linear in the perturbation over four
decades with no threshold, and halves when effort is multiplied by ten.
What was measured is the refiner’s convergence rate, not a basin radius.
The sharper result was incidental—started `1e-5` from a configuration that has stood
since 1979, the campaign’s **default annealing schedule wanders off and lands with a
median side gap of `0.27`**, worse than it reaches from cold starts.

**Build the quench, and have it beat the record.** The first working version reported a
side *below* Trump’s. The runbook’s pre-registered rule held—a run that beats the record
has found a bug—and it had ([D-014](defects.md)). The fix pinned the solver tolerance
and post-checks every solution against its own constraints; the postmortem generalised
it into four rules and a soundness perimeter that every configuration- emitting
component now joins.

**Follow the corner.** The quench’s angle half stalled, the reason turned out to be
geometric rather than numerical, and acting on it took the two proved instance cells to
machine precision. That chain runs
[exp-006](campaign/series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md)
to [H-019](campaign/hypotheses/H-019-angle-optimum-is-a-kink.md) to
[exp-007](campaign/series/series-000-smoke-and-calibration/experiments/exp-007-quench-bracket-n5.md)–[exp-010](campaign/series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md),
and is the campaign working as designed.

### How rounds are run

The full contract is the [runbook](campaign/README.md); the parts that matter for
reading the results below:

- **Evidence tiers**, and a number’s tier decides what it may claim: `f64_screen` (a
  candidate was proposed), `polished` (a quench endpoint candidate was valued to solver
  precision), `exact` (validity, and only here a record).
  Basin or terminal-component identity requires additional evidence beyond the tier
  label. **`beat_record: true` may only be written at `exact`.**
- **Four instance cells with different jobs**: `n = 10` positive control, `n = 11`
  target, `n = 12` open-case calibration, `n = 17` mechanism-matched calibration.
  A guard breach rejects a round regardless of outcome, because it means the instrument
  is wrong rather than the strategy good.
- **Five seeds minimum per cell**, median and min–max range both reported.
  Overlapping ranges mean *no detectable effect*, never “a small win”.
- **Every round declares a timebox before it starts** and records an `effort`
  block—`wall_seconds`, `agent_minutes`, and `stopped_by`. A round that stopped on its
  `criterion` answered its question; one that stopped on its `timebox` did not, and must
  name where a successor resumes.
- **Three terminal states are distinct**: `rejected` (measured and missed), `abandoned`
  (budget gone, no determination, resumable), `exhausted` (re-running under this regime
  would add nothing).
- **Negative results are kept**, and a defective artifact is corrected by dated
  annotation rather than rewriting.

## The Hypothesis Registry

Forty-one claims or open questions are codified as artifacts.
The standing review’s complete H-001 through H-015 block is now in the registry; later
ids carry campaign-native claims and seven explicit open questions.
The [ledger](campaign/ledger.md) is generated from the artifacts and is the current
view; this section is the reading of it.

| Id | Status | Claim, in short | Rounds | Effort |
| --- | --- | --- | --- | --- |
| [H-019](campaign/hypotheses/H-019-angle-optimum-is-a-kink.md) | **confirmed** | Trump’s tested shared-tilt slice has a corner at the published optimum | 1 | 10m agent |
| [H-002](campaign/hypotheses/H-002-lp-in-cell-polish.md) | **refuted** as stated | LP-in-cell polish refines *any* annealer output to the analytic value | 4 | 190m agent, 4.9m wall |
| [H-016](campaign/hypotheses/H-016-stock-annealer-reaches-standing-best.md) | **refuted** | The stock annealer reaches the standing best on every instance cell | 4 | 10.2m wall |
| [H-018](campaign/hypotheses/H-018-basin-entry.md) | **refuted** as stated | Perturbed starts return to Trump’s packing at least half the time | 1 | 75m agent, 1.3m wall |
| [H-020](campaign/hypotheses/H-020-oblique-record-finding-n17.md) | **refuted** | The annealer reaches the standing best at `n = 17`, the nearest oblique record | 1 | 6.6m wall |
| [H-001](campaign/hypotheses/H-001-angle-class-reduction.md) | blocked | An angle-class proposer beats free-coordinate annealing | 0 | — |
| [H-003](campaign/hypotheses/H-003-basin-frequency-and-contacts.md) | blocked | Contact count predicts component attraction frequency on held-out data | 0 | — |
| [H-004](campaign/hypotheses/H-004-neighbor-transfer-seeding.md) | blocked | Neighbor-transfer seeds improve paired `n=11` search | 0 | — |
| [H-005](campaign/hypotheses/H-005-m2-minus-3-construction.md) | blocked | A 3-4-5-tilt construction packs 97 squares below side 10 | 0 | — |
| [H-006](campaign/hypotheses/H-006-lp-dual-unavoidable-sets.md) | blocked | LP dual support yields refinement-stable proof candidates | 0 | — |
| [H-007](campaign/hypotheses/H-007-saturation-curves.md) | blocked | Coverage models predict held-out component discovery | 0 | — |
| [H-008](campaign/hypotheses/H-008-false-basin-rate.md) | blocked | The stronger-verifier rejection rate is measurable across `n` | 0 | — |
| [H-009](campaign/hypotheses/H-009-symmetry-dedup-ratio.md) | blocked | Symmetry quotienting materially changes endpoint counts | 0 | — |
| [H-010](campaign/hypotheses/H-010-stromquist-triple.md) | **refuted** | Stromquist’s five-node Theorem 2 mechanism reproduces | 1 | 180m agent, 0.55s wall |
| [H-011](campaign/hypotheses/H-011-small-n-census.md) | blocked | The small-`n` landscape is censusable | 0 | — |
| [H-012](campaign/hypotheses/H-012-record-basins-are-rare.md) | blocked | Record basins are rare in quench measure | 0 | — |
| [H-013](campaign/hypotheses/H-013-delta-continuation.md) | blocked | Delta-continuation improves target-component arrival | 0 | — |
| [H-014](campaign/hypotheses/H-014-superdisk-continuation.md) | blocked | Superdisk continuation imports new square components | 0 | — |
| [H-015](campaign/hypotheses/H-015-map-elites-illumination.md) | blocked | MAP-Elites improves certified component discovery rate | 0 | — |
| [H-017](campaign/hypotheses/H-017-budget-scaling.md) | open | 100× the budget reaches Trump’s basin | 0 | — |
| [H-021](campaign/hypotheses/H-021-endpoint-identifiability.md) | blocked | At least 95% of small-`n` endpoint support is classifiable | 0 | — |
| [H-022](campaign/hypotheses/H-022-trump-local-geometry.md) | open question | What quantitative neighborhood and transferable stress structure follow after exp-013’s local-isolation theorem? | 0 | — |
| [H-023](campaign/hypotheses/H-023-n5-terminal-connectivity.md) | open question | How are the observed `n=5` endpoint candidates connected? | 0 | — |
| [H-024](campaign/hypotheses/H-024-record-angle-class-count.md) | **refuted** | Verified record packings through `n=30` use at most three angle classes; exp-012 verifies six at `n=29` | 1 | 12m agent, 0.158s wall |
| [H-025](campaign/hypotheses/H-025-record-angle-compressibility.md) | blocked | At least 80% of verified records are approximated by three angle classes within `1e-4` side loss | 0 | — |
| [H-026](campaign/hypotheses/H-026-trump-first-order-rigidity.md) | **confirmed** | Trump has no nonzero direction in any branchwise fixed-side linearized cone | 1 | 100m agent, 57.308s wall |
| [H-027](campaign/hypotheses/H-027-record-angle-cones.md) | blocked | The imported `n=11,17` record cells have positive class-angle directional cones | 0 | — |
| [H-028](campaign/hypotheses/H-028-reference-cell-angle-sheets.md) | blocked | Each published point is the sole refined local minimum on its declared reference-cell angle sheet, with a boundary margin | 0 | — |
| [H-029](campaign/hypotheses/H-029-adaptive-splitting.md) | blocked | Calibrated adaptive splitting beats restarts on rare target events | 0 | — |
| [H-030](campaign/hypotheses/H-030-public-parent-surgery.md) | blocked | Construction surgery reproduces at least two of six hidden public record improvements | 0 | — |
| [H-031](campaign/hypotheses/H-031-load-guided-block-moves.md) | blocked | LP-load-guided block moves beat coordinate-only moves per pair-test | 0 | — |
| [H-032](campaign/hypotheses/H-032-small-n-optimal-moduli.md) | open; `n=3,4` solved | What are the exact optimal configuration spaces for `n=3…6`? | 2 | 35m agent, 1.28s wall |
| [H-033](campaign/hypotheses/H-033-m2-minus-3-at-n61.md) | open question | Can the `m²−3` theorem be extended to `s(61)=8`? | 0 | — |
| [H-034](campaign/hypotheses/H-034-fractional-piercing-ceiling.md) | blocked | The fractional piercing value at Trump’s side is greater than ten | 0 | — |
| [H-035](campaign/hypotheses/H-035-asymptotic-primitive-finite-transfer.md) | blocked | Current asymptotic construction primitives improve a finite public parent | 0 | — |
| [H-036](campaign/hypotheses/H-036-robust-restricted-orientation.md) | blocked | Stromquist’s restricted-orientation gap survives a `0.25°` neighborhood | 0 | — |
| [H-037](campaign/hypotheses/H-037-asymptotic-waste-exponent.md) | open question | What is the asymptotic waste exponent between `1/2` and `3/5`? | 0 | — |
| [H-038](campaign/hypotheses/H-038-record-number-fields.md) | open question | Which exact fields and elimination mechanisms occur in verified records? | 0 | — |
| [H-039](campaign/hypotheses/H-039-s12-proof-frontier.md) | open question | Can the lower bound for `s(12)` be improved and ultimately closed at four? | 0 | — |
| [H-040](campaign/hypotheses/H-040-active-cell-neighbor-walk.md) | blocked | Active-cell neighbor walks beat multistart in new verified cells per LP solve | 0 | — |
| [H-041](campaign/hypotheses/H-041-repaired-stromquist-point-set.md) | **confirmed** | Moving Figure 14 point `G.x` from `.8` to `.79` restores the complete lower-bound mechanism | 1 | 90m agent, 0.70s wall |

### Confirmed

**[H-019](campaign/hypotheses/H-019-angle-optimum-is-a-kink.md)—Trump’s tested shared-
tilt slice is non-smooth at the published optimum.** Registered by the runner of
`exp-006` *before* recording that round, because the round measured something `H-002`
did not predict; confirmed by
[exp-010](campaign/series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md).
Elaborated in [The Corner](#the-corner-and-the-method-it-forced) above.
It is the campaign’s first confirmed claim, and the one that changed a method.

### Refuted, and what each refutation bought

**[H-016](campaign/hypotheses/H-016-stock-annealer-reaches-standing-best.md).** The
null: a serious budget on a general-purpose annealer finds the best known packing.
Within `1e-4` only at `n = 12`. The refutation is not the interesting part—the two
failures were different in kind.
At `n = 10` later cell polishing showed the candidate had the record’s declared
structure and stopped `4.19e-04` short (**polish**); at `n = 11` it remained `3.73e-02`
above Trump and no terminal-component relation was measured.
That operational distinction set the next four rounds without proving a topological one.

**[H-002](campaign/hypotheses/H-002-lp-in-cell-polish.md).** Claimed that alternating LP
solves with local angle moves refines *any* annealer output to the analytic value.
Refuted as stated, and the cell-level split is the result:

| Cell | Round | Outcome |
| --- | --- | --- |
| `n = 5` | [exp-007](campaign/series/series-000-smoke-and-calibration/experiments/exp-007-quench-bracket-n5.md) | **accepted**—`2.22e-15`, machine precision |
| `n = 10` | [exp-008](campaign/series/series-000-smoke-and-calibration/experiments/exp-008-quench-bracket-n10.md) | **accepted**—`1.33e-15`, twelve orders of improvement |
| `n = 11` | [exp-009](campaign/series/series-000-smoke-and-calibration/experiments/exp-009-quench-bracket-n11.md) | **rejected**—`6.29e-02`; tested starts remain far from Trump after the local procedure |
| all three | [exp-006](campaign/series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md) | **rejected**—the original free-angle descent, 1.1–1.3× everywhere |

The word that failed is *any*. The quench is a **polisher, not a rescue**: it makes the
declared cell optimum reproducible to solver precision, which is an input to the census
and atlas, and it does not lift the burden of finding a competitive region off the
proposer.

**[H-018](campaign/hypotheses/H-018-basin-entry.md).** Predicted an `ε` at which the
return rate collapses, which would be the basin’s radius.
Observed rate at the registered `ε = 1e-3`: 0 of 40 in every arm.
The residual scaled approximately linearly with `ε` under the tested finite schedules
and decreased with more effort.
That diagnoses incomplete convergence of this refiner; it does not prove an attracting
basin through `ε = 1e-1`, distinguish an isolated endpoint from a terminal family, or
establish component membership for the perturbed trajectories.

### Blocked, and on what

The priority-1 agenda has two independent bottlenecks.
The basin lane is blocked on the measurement system around the quench:
terminal-component identity, endpoint classification, event provenance, coverage
estimation, independent validity, and a named proposer regime.
The proof lane now has both halves of its calibration: exp-016 falsifies Stromquist’s
printed certificate, while exp-017 certifies a complete source-distinct repair.
The same two-sided falsifier/certificate architecture can now target a new lower bound
at `n=12`.

- **[H-011](campaign/hypotheses/H-011-small-n-census.md)** (census at `n ≤ 10`) needs
  H-021’s classification evidence, event records, and a coverage estimator.
- **[H-012](campaign/hypotheses/H-012-record-basins-are-rare.md)** (the premise the
  cartography programme rests on) needs H-011’s machinery plus an explicit `n=11`
  sampling cell. Kill: record-basin probability within ~10× of the modal basin’s, in
  which case the cartography program stands down and the campaign reverts to throughput.
  **Still untested**, which is the largest open question about the strategy.
- **[H-001](campaign/hypotheses/H-001-angle-class-reduction.md)** (angle classes) now
  has a strong prior from `exp-006` but remains unmeasured as a *search* claim: the
  class-constrained arm assumed the answer’s own structure, so it shows the angle search
  method decides the outcome, not that an unguided method would find that structure.
- **[H-010](campaign/hypotheses/H-010-stromquist-triple.md)** (Stromquist calibration)
  is terminally refuted by exp-016. An exact strict box avoids every printed Figure 14
  point, so the five-node conjunction fails at its fourth node.
  The result rejects the published proof as printed, not the numerical lower bound.
- **[H-041](campaign/hypotheses/H-041-repaired-stromquist-point-set.md)** (proof repair)
  is confirmed by exp-017 after moving only `G.x` from `.8` to `.79`. The complete exact
  repair proves the same lower bound with 26 repaired Figure 14 faces and thirteen
  passing mutations; it does not make the published proof correct as printed.

**[H-017](campaign/hypotheses/H-017-budget-scaling.md)** (100× budget) stays open and
demoted behind a short response curve.
It is operationally shaped but not admissible unattended while D-044 remains open.

The [idea board](campaign/ideas.md) carries the full registered portfolio alongside raw
ideas and dead ends.
The registry artifact, not the review’s historical prose or this summary, owns each
current criterion and kill rule.

The mutable size-by-size run order lives in the
[basin-map confidence ladder](campaign/agendas/agenda-001-basin-confidence-ladder.md),
not in this status document.
It labels every cell as tool validation, measurement validation, or genuine research.
The exact and event controls at `n = 3,4` are complete; BC-003 is the next `n = 5`
tool-validation cell.
Component and census claims remain blocked on the later identity and coverage rows.

## Experiments Conducted

There are 24 rounds registered in `series-000`; all are terminal.
They record 758 agent-minutes and 25.3 wall-minutes.
Their instruments are `sqsearch` 0.1.0 (the `f64` screening annealer), `sqpack.quench`
(0.1.0 with angle descent and 0.2.0 with class bracketing), the high-precision Kingbird
SVG reconstruction, the exact Trump linearized-cone checker, the exact small-moduli
checker, the exact Stromquist printed-set falsifier, and the exact repaired-cover
certificate.

No search round has been run at the `exact` tier, so **no result below claims a new
record**. Exp-012 is an exploratory reconstruction of a published record witness; its
six-class determination does not certify that witness as exact or optimal.

### Roll-up

Every figure is lifted from the round’s frontmatter, which is lifted from the JSONL
archive beside it.

| Round | `n` | Role | H | Instrument | Headline number | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| [exp-001](campaign/series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md) | 10, 11, 12 | sweep | H-016 | annealer | gaps `+4.19e-04`, `+3.73e-02`, `0` | rejected |
| [exp-002](campaign/series/series-000-smoke-and-calibration/experiments/exp-002-baseline-n10-positive-control.md) | 10 | positive control | H-016 | annealer | `3.7075262001`, gap `+4.194e-04` | rejected |
| [exp-003](campaign/series/series-000-smoke-and-calibration/experiments/exp-003-baseline-n11-target.md) | 11 | target | H-016 | annealer | `3.9144165418`, gap `+3.733e-02` | rejected |
| [exp-004](campaign/series/series-000-smoke-and-calibration/experiments/exp-004-baseline-n12-negative-control.md) | 12 | open-case calibration | H-016 | annealer | exactly `4.0`, all five seeds | accepted |
| [exp-005](campaign/series/series-000-smoke-and-calibration/experiments/exp-005-basin-entry-n11.md) | 11 | target | H-018 | annealer | 0/40 returns; `max_dev ≈ 11·ε`, no threshold | rejected |
| [exp-006](campaign/series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md) | 5, 10, 11 | sweep | H-002 | quench 0.1.0 | 1.1–1.3× only; single cell `4.441e-16` | rejected |
| [exp-007](campaign/series/series-000-smoke-and-calibration/experiments/exp-007-quench-bracket-n5.md) | 5 | positive control | H-002 | quench 0.2.0 | `3.19e-08 → 2.2204e-15` | **accepted** |
| [exp-008](campaign/series/series-000-smoke-and-calibration/experiments/exp-008-quench-bracket-n10.md) | 10 | positive control | H-002 | quench 0.2.0 | `4.507e-03 → 1.3323e-15` | **accepted** |
| [exp-009](campaign/series/series-000-smoke-and-calibration/experiments/exp-009-quench-bracket-n11.md) | 11 | target | H-002 | quench 0.2.0 | `6.999e-02 → 6.2894e-02` | rejected |
| [exp-010](campaign/series/series-000-smoke-and-calibration/experiments/exp-010-angle-kink-n11.md) | 11 | target | H-019 | quench 0.2.0 | slopes `0.1747` / `0.3841`, ratio `2.198` | **accepted** |
| [exp-011](campaign/series/series-000-smoke-and-calibration/experiments/exp-011-h-020-n17.md) | 17 | mechanism-matched | H-020 | annealer | reported `5.0` on all five f64-screen seeds, gap `+3.245e-01` | rejected |
| [exp-012](campaign/series/series-000-smoke-and-calibration/experiments/exp-012-h-024-n29-angle-classes.md) | 29 | target | H-024 | SVG reconstruction + SAT | six classes; minimum class gap `0.296067°` | **rejected** |
| [exp-013](campaign/series/series-000-smoke-and-calibration/experiments/exp-013-h-026-trump-tangent.md) | 11 | target | H-026 | exact branchwise linearization | 128/128 exact zero-cone certificates | **accepted** |
| [exp-014](campaign/series/series-000-smoke-and-calibration/experiments/exp-014-h-032-n3-optimal-moduli.md) | 3 | positive control | H-032 | exact configuration space | two labelled circles → one quotient interval | **accepted** |
| [exp-015](campaign/series/series-000-smoke-and-calibration/experiments/exp-015-h-032-n4-optimal-moduli.md) | 4 | positive control | H-032 | exact configuration space | 24 labelled points → one quotient point | **accepted** |
| [exp-016](campaign/series/series-000-smoke-and-calibration/experiments/exp-016-h-010-stromquist-printed-figure14.md) | 11 | proof calibration | H-010 | exact source-bound falsifier | strict side `1.0001` box avoids all 12 printed points | **rejected** |
| [exp-017](campaign/series/series-000-smoke-and-calibration/experiments/exp-017-h-041-stromquist-repaired-figure14.md) | 11 | proof calibration | H-041 | exact repaired cover | 26-face cover; complete five-node certificate | **accepted** |
| [exp-018](campaign/series/series-000-smoke-and-calibration/experiments/exp-018-h-021-n3-basin-event-calibration.md) | 3 | positive control | H-021 | full-pose event replay | 4 valid; 3 producer-converged; 0 admissible | **blocked** |
| [exp-019](campaign/series/series-000-smoke-and-calibration/experiments/exp-019-h-021-n4-basin-event-calibration.md) | 4 | positive control | H-021 | full-pose event replay | 4 valid; 2 producer-converged; 0 admissible | **blocked** |
| [exp-020](campaign/series/series-000-smoke-and-calibration/experiments/exp-020-h-021-n5-basin-event-calibration.md) | 5 | positive control | H-021 | full-pose event replay | 4 valid; 4 producer-converged; 0 admissible | **blocked** |
| [exp-021](campaign/series/series-000-smoke-and-calibration/experiments/exp-021-h-021-n3-basin-event-v3.md) | 3 | positive control | H-021 | BasinEvent/v3 semantic replay | 1 valid; 2,037/2,037 fixed-point evaluations settled; 1 admissible | **baseline** |
| [exp-022](campaign/series/series-000-smoke-and-calibration/experiments/exp-022-h-021-n3-basin-event-v3-completion.md) | 3 | positive control | H-021 | BasinEvent/v3 semantic replay | 3 valid; 8,364/8,364 evaluations settled; 3 admissible | **baseline** |
| [exp-023](campaign/series/series-000-smoke-and-calibration/experiments/exp-023-h-021-n4-basin-event-v3.md) | 4 | positive control | H-021 | BasinEvent/v3 semantic replay | 4 valid; 3 converged/admissible; one typed unsettled stop | **baseline** |
| [exp-024](campaign/series/series-000-smoke-and-calibration/experiments/exp-024-h-021-n4-basin-event-v3-repair.md) | 4 | positive control | H-021 | BasinEvent/v3 semantic replay | 4 valid; 14,301/14,301 evaluations settled; 4 admissible at side 2 | **baseline** |

### Cost and provenance

| Round | Budget | Wall | Agent | Stopped by | Engine commit |
| --- | --- | --- | --- | --- | --- |
| exp-001 | 12e9 moves | 302.4 s | — | criterion | `d6a1057` (**orphaned**) |
| exp-002 | 4e9 moves | 93.5 s | — | criterion | `1e70bc8` |
| exp-003 | 4e9 moves | 107.2 s | — | criterion | `1e70bc8` |
| exp-004 | 4e9 moves | 108.8 s | — | criterion | `1e70bc8` |
| exp-005 | 720 trials | 77.1 s | 75 m | criterion | `8b450a1` |
| exp-006 | 20,135 LP solves | 72.8 s | 115 m | criterion | `8b450a1` |
| exp-007 | 5 seeds, 30 s each | 3.4 s | 25 m | criterion | `8b450a1` |
| exp-008 | 5 seeds, 30 s each | 67.0 s | 20 m | criterion | `8b450a1` |
| exp-009 | 5 seeds, 30 s each | 150.0 s | 30 m | criterion | `8b450a1` |
| exp-010 | 11 probes | 1.0 s | 10 m | criterion | `8b450a1` |
| exp-011 | 4e9 moves | 397.474 s | 0 m | criterion | `60a50cc` |
| exp-012 | one SVG, 406 pairs | 0.158 s | 12 m | criterion | `5384209` |
| exp-013 | 512 raw branches | 57.308 s | 100 m | criterion | `faba023` |
| exp-014 | 64 raw separation branches | 0.63 s | 30 m | criterion | `257cb0d` |
| exp-015 | 4,096 raw separation branches | 0.65 s | 5 m | criterion | `257cb0d` |
| exp-016 | exact printed-set escape + replay | 0.55 s | 180 m | criterion | `178fc6b` |
| exp-017 | exact repaired cover + replay | 0.70 s | 90 m | criterion | `c6d036b` |
| exp-018 | 4 seeds, 10 s each | 10.025 s | 12 m | dependency | `ee3acc1` |
| exp-019 | 4 seeds, 10 s each | 13.322 s | 5 m | dependency | `ee3acc1` |
| exp-020 | 4 seeds, 10 s each | 14.821 s | 5 m | dependency | `ee3acc1` |
| exp-021 | 1 seed, 10 s cap | 1.897 s | 15 m | criterion | `8f20908` |
| exp-022 | 3 seeds, 10 s each | 6.274 s | 6 m | criterion | `8f20908` |
| exp-023 | 4 seeds, 10 s each | 12.506 s | 8 m | criterion | `8f20908` |
| exp-024 | 4 seeds, 10 s each | 16.967 s | 15 m | criterion | `f15d036` |

### What the twenty-four rounds jointly establish

**The numerical basin event trust boundary is now admissible on two proved positive
controls; component classification is not.** Exp-018 through exp-020 retain twelve
independently valid historical v2 poses at `n=3` through `n=5`, including four at the
proved `n=3` and `n=4` optima, but D-165 correctly remains recorded on those artifacts.
Exp-021 adds one v3 `n=3` event whose 2,037 fixed-point evaluations are all retained and
settled, whose pose independently verifies, and whose admissibility claim replays.
Exp-022 completes the four-seed v3 block at 4/4 admissible: three endpoints reach side 2
and one reaches the valid nonoptimal side 2.362735797795. These events are evidence for
the producer contract and terminal outcomes, not terminal-component counts.
Exp-023 reaches proved side 2 on three of four n=4 starts and preserves the fourth
event’s post-check rejection.
That stop exposed D-171: two rows were already outside the screen before an argmax-only
retry. Exp-024 applies one complete offending-set retry and reaches side 2 on all four
starts, with 14,301 of 14,301 evaluations settled and all four events admissible.
None of the four `n=5` starts finds its proved optimum.
The exact small-moduli controls remain valid; component identity is the next blocked
layer. The `n=12` calibration returns exactly `4.0`, but that is not a known-answer
guard. The runner’s full-pose independent verification boundary remains open under
[D-044](defects.md); a producer-reported overlap scalar does not close it.

**Trump’s exact pose is locally isolated.** Exp-013 retains all 512 raw active-feature
selections as 128 derivative-distinct matrices.
Every matrix has exact rank 33 and a strictly positive exact `Q(u)` stress, so every
branchwise fixed-side linearized cone is zero.
A finite-branch subsequence argument upgrades that result to local isolation and strict
local side optimality in the anchored pose–side chart, modulo finite symmetries.
It does not prove global optimality or give an explicit isolation radius.

**The optimal configuration spaces at `n = 3,4` are now exact controls.** Exp-014 proves
that `F_3(2)` is two labelled circles, its `S3` quotient is one circle, and its
`D4 x S3` quotient is an interval whose corner endpoint changes the active signature and
whose midpoint only changes the stabilizer.
Exp-015 proves that `F_4(2)` is 24 isolated labelled grids and both declared quotients
are one point. Arbitrary rotations add no side-2 configurations in either case.
Generation plus complete replay costs 1.28 wall seconds, so both controls belong in
every gate. H-032 remains open at `n = 5,6`.

**The published `n = 11` lower-bound proof is false as printed.** Exp-016 exactly
certifies an open box of side `10001/10000` that fits Stromquist’s claimed container and
strictly avoids all twelve printed Figure 14 points.
This rejects the registered five-node H-010 conjunction but not the numerical lower
bound itself.

**The numerical lower bound now has an independent exact certificate.** Exp-017 moves
only Figure 14 point `G.x` from `.8` to `.79` and exactly certifies the complete
five-node argument. Its 18-cell Figure 13 cover plus four Klein-four-related exceptions,
26-face repaired Figure 14 tiling, exact lemma premises, and `3+9` count prove
`s(11) ≥ 2 + 4/√5`. This source-distinct computer-assisted result is not attributed to
Stromquist, is not externally peer-reviewed, and does not close the gap to Trump.

**The tested class-bracketing refiner separates the proved controls from the target.**
It takes the tested `n = 5` and `n = 10` starts to `1e-15` and leaves the tested
`n = 11` starts at `6e-02`. That makes proposer quality the next empirical bottleneck;
it does not certify general local optimality or finish the quench contract (D-052).

**The `n = 11` failure is consistent with an exploration problem.** Five annealer seeds
land in a band five times narrower than the remaining gap and the local quench improves
those tested starts by only 1.3×. Starting near Trump’s reference, the default schedule
moves far away; that is refinement evidence, not a certified basin-membership test.

**Two rounds have been re-read by later ones.** `exp-005`’s finite-quench residual is
now scoped to the tested refiner and no longer called component attraction (D-083).
`exp-003`’s `n = 11` result is therefore a combined proposer/refinement observation, not
a pure basin-finding diagnosis.

### Known defects in the record

The full log is [`defects.md`](defects.md); these are the ones that bear on reading the
table above.

- **`exp-001`’s archive carries no configurations** and its engine commit was orphaned
  by a rebase ([D-006](defects.md), [D-010](defects.md)). Cite `exp-002`–`exp-004` for
  anything configuration-level.
- **`exp-001` and `exp-006` each record a three-cell sweep as one cell**
  ([D-010](defects.md), [D-017](defects.md)—the second a verbatim repeat of the first,
  because the first fix left no regression check).
  Their numbers stand; the ledger’s sweep coverage misreported them until the successor
  rounds split the cells.
- **[D-021](defects.md) is contained.** The `polished` tier has a noise floor of about
  `1e-11` in the side, and eight rounds sit on it.
  Nothing at that tier may claim a difference smaller than the floor.

## The Defect Record

Kept with the same discipline as the experiment record, because the aggregate says
things no individual bug report can.
The log contains 182 defects, [one line each](defects.md), generated from `defects.yaml`
and checked in the gate.

| Class | Count | The system … |
| --- | ---: | --- |
| soundness | 61 | asserted something false about the mathematics |
| validity | 53 | was correct, but the measurement did not bear on the question |
| bookkeeping | 49 | recorded something its own evidence contradicts |
| robustness | 14 | did not finish, or finished only by luck |
| performance | 5 | worked, but cost far more than it should |

Two observations the log exists to make.

**Forty-five of the fifty-five soundness defects pointed in the *flattering*
direction**, where the error looks like a success.
That is the dangerous class, and it is the majority of it.

**The automated gate has caught six defects in one hundred sixty-one, and no soundness
defect ever.** Every soundness failure was found by a control cell whose answer was
known in advance, a rule written down before the measurement, a generated view
contradicting its source, or someone reading carefully.
Gates confirm what you already thought to check; these were found by devices built to be
*surprised*. The six the gate did catch ([D-024](defects.md), [D-064](defects.md),
[D-106](defects.md), [D-107](defects.md), [D-125](defects.md), and [D-130](defects.md))
are bookkeeping or robustness defects, found by contiguity, integration,
mutation-anchor, and reconciliation checks—which is the pattern, not an exception: gates
are good at the mechanical classes and have never once caught the mathematics being
wrong.

The entries from D-030 onward sharpen the point rather than softening it.
D-030 and D-031 were caught by proved control cells while structural store checks stayed
green; D-032 and D-033 came from rehearsing recovery paths that had shipped unrun; D-034
found the endpoint-isolation assumption; D-035 found destructive negative-control
residue; D-036 found a timeout reported as convergence; and D-037 separated real census
counts from a checker’s synthetic re-offers.
D-038 separated scalar recognition from an oracle; D-039 separated side precision from
component resolution; D-040 made rarity conditional on a durable `P/Q/E` regime; D-041
rejected rank-free rigidity and dimension claims; and D-042 exposed `n = 12` as an open
target masquerading as a negative control.

The systematic crosswalk then records every remaining technical finding from the PR #14
review. D-043 closes the archive-before-validation path; D-044 leaves independent pose
validity open; D-045 tracks criterion-specific evaluators; D-046 tracks the incomplete
runner state machine; D-047 closes contact-key reflection; D-048 retains unstable
tolerance/equality semantics; D-049 tracks factorial canonicalization; D-050 and D-051
separate observation promotion from regime-safe merging; D-052 narrows quench
stationarity; D-053 protects the generic exact-field boundary; D-054 separates budgets
and final-best records from trajectory claims; D-055 and D-056 correct the angle and
`m²-3` theorems; D-057 scopes H-020; D-058 reconciles the local handover; D-059 keeps
the golden oracle/characterization split open; D-060 restores producer-level strict
checks; and D-061 preserves evidence for unrecognised endpoints.
D-062 catches the executable `n=12` rejection that survived the first D-042 correction;
D-063 removes a false contrapositive from the rigidity premise; and D-064 keeps a
read-only runner preflight executable inside the gate that mutation-tests it without
opening the gate to live campaign execution.
D-065 removes the last repeated numeric gate claim from the README and reconciles its
remaining qualitative claim to the defect source.

D-066 catches the active baseline script repeating the stale `n=12` control claim.
D-067 and D-068 restore the omitted eleventh-round wall time and stop calling elapsed
time CPU time; D-069 reconciles H-002 with the four rounds that already measured its
quench; and D-070 restores exp-011’s execution revision and makes future timing and
provenance survive the execute/record boundary.
D-071 remains open because the numerical runner’s generated session report still
overwrites its predecessor; versioned agent-session artifacts now preserve the outer
delegation loop separately.
D-072 closes the two direct runner commands that bypassed the cooperative gate marker,
and D-073 wires those new session artifacts into the filename/id invariant.
D-074 corrects the first D-070 regression claim: receipt parsing alone did not exercise
the terminal artifact mapping, which is now centralized and mutation-tested.
D-075 narrows PR #16’s cross-environment mismatch to what its aggregate output actually
establishes; D-076 keeps the `n=5` six-of-six observation from deciding among identity,
landscape, stationarity, and numerical explanations; D-077 replaces a stale serial
handoff with current parallel lanes; and D-078/D-079 complete the rank and implication
corrections in that response.
D-080 replaces a vacuous neighbor-transfer target; D-081 keeps a nonempty but
underfilled queue from counting as overnight readiness; D-082 records the second
overgeneralization of H-020; D-083 retracts an attraction claim inferred from a finite-
quench residual; D-084 removes unsupported rigidity and gap-rank facts from the `n=11`
frontier artifact; D-085 freezes living uv commands; and D-086 replaces stale overnight
and handoff state with the current launch agenda.
D-087 separates the angle-class algorithm, corpus law, and single-cell kink claims.
D-088 through D-105 are source, geometry, identity, and hypothesis-design corrections
from the first creativity pass; D-106 and D-107 are the mutation-anchor and synopsis
reconciliation failures its first gate attempts caught.
D-108 through D-119 are the second-pass corrections: the missing piercing paper, false
isostatic and self-stress arguments, fixed-budget and fixed-cell overreach, topology and
fractional-LP mistakes, unsupported novelty, stale registry state, the H-012/H-017
estimand conflation, and an impossible continuity-blind angle-sheet criterion.
D-120 through D-138 record the engineering delta and first post-merge runs:
ulp-sensitive cell selection, gate boundary and skip-contract failures, the per-step
worker cap, bounded portable snapshots, a parallel negative-control race, wall-clock
scientific budgeting, stale review status, the missing targeted edit loop, unbounded
checker children, and a nonunique mutation-control anchor, followed by a lint floor that
accepted type-checker warnings and a fixed-cell solver that does not expose whether it
settled or hit its cap ([D-132](defects.md)), then the search-only determination
vocabulary that could not record the H-024 result, the omitted `n=29` source provenance
that the falsifier exposed, the roll-up’s obsolete blanket claim about exploratory
record evidence, the distinction between a branch linearization and a true Bouligand
motion, and a certificate replay that did not require one-to-one branch coverage.
The next tranche, D-139 through D-171, records the missing hard-square topology
literature, a stale closed-family contact claim, exact-moduli integration errors,
Stromquist source transcription and proof-chain mistakes, stale campaign effort, the
paper’s extraneous Lemma 4 root, and the escaping Figure 14 box.
D-153 records that the three 1984 memoranda were directly hosted while the source ledger
called them unavailable; D-154 and D-155 close exact-field metadata and cross-platform
record gaps in the first uncommitted H-010 checker.
D-156 through D-158 close tiling-containment, sign-preservation, and provenance-scope
gaps in the H-041 repair checker before any H-041 evidence could land.
D-159 keeps immutable scanned PDFs out of Git’s text-whitespace path while preserving
strict whitespace checks for the associated hand-written reading aids.
D-160 records a D-145 recurrence caught in this round’s own diff: a broad scalar match
attached H-010’s regression text to D-002 before an ID-scoped correction restored both.
D-161 records the stale forty-hypothesis synopsis count exposed when H-041 became the
forty-first artifact; the current consistency check now derives that count from the
registry. D-162 records the first consequence exposed by typed fixed-cell termination: a
deep rebuild reduces the converged totals at `n=3`, `n=4`, and `n=5`, and exposes
unsettled ladder evaluations at `n=9` and `n=10`. Their full poses remain useful
evidence, but the small-`n` convergence totals must be rebuilt before any such event can
be promoted to a terminal component.
D-163 records the gate failure that first hid that evidence: the historical-regression
step continued after its checker failed and returned the status of a later successful
probe. The step now propagates the checker failure immediately.
D-164 separates one source of the newly visible nonconvergence: a successful HiGHS solve
missed the fixed-cell post-check by about `2e-11` beyond its cutoff and was labeled
mathematically infeasible.
Typed outcomes now retain the cause, rows, residuals, retry margins, and actual
solver-call count.
A single retry tightens the complete initial offending set, leaves the
`1e-10` acceptance screen unchanged, restores the proved n=3 and n=10 controls, and is
replayed against the original LP rows.
D-165 records the bounded implementation’s stop condition: initial cell-solve failures
still bypass D-132’s typed result and become dummy objectives inside the angle search.
That code path is now typed, D-168 closes the n=10 cell degeneracy, and BasinEvent/v3
routes every fixed-point evaluation through one audited path.
Exp-021 retains and replays a balanced 2,037-evaluation receipt, so D-165 is fixed; the
older exp-018 through exp-020 artifacts remain correctly blocked under their historical
v2 contract. D-166 removes the resulting false certificate from BasinEvent/v1. Version 2
retains the full stopping event and independent validity screen but marks every current
event promotion-blocked by D-165, and replay refuses a forged admissible flag.
D-167 adds the missing per-event wall time, so subsequent seed blocks and larger `n`
values can be selected from measured throughput rather than command-level guesses.
D-168 separates an equal-objective finite cell closure from a genuinely unresolved
cycle. The n=10 control closes after enumerating at most eight adjacent cells; exp-021
then records the new typed path without rewriting the historical blocked events.
D-169 fixes a second post-check hole found while typing those failures: containment rows
were never replayed.
Every accepted cell now passes the full original LP residual vector.
D-170 gives D-165 its own bead after the defect log was found to reference the unrelated
D-132 tracker; the older bead remains unchanged.
D-171 records why the former argmax-only repair left one n=4 event unsettled: rows 16
and 21 already violated the screen together.
The complete offending-set retry closes the exact regression, and exp-024 completes the
n=4 v3 block at 4/4 admissible without weakening the screen.

Both claims are computed from `defects.yaml` rather than written down, so neither can
drift from the log it describes ([D-028](defects.md)).

Sixty-eight fixes left no regression check behind, and that list has already predicted a
recurrence once. The
[postmortem](docs/project/postmortems/postmortem-2026-08-23-soundness-class.md) on D-014
turns this into four rules—oracle coverage through unshared code, tolerances stated
relative to what they govern, a discovery treated as a defect until an independent layer
agrees, and new components inheriting the perimeter—that apply to code not yet written.

## Where This Stands

The middle tier is built and works.
Two instruments now agree on the cell decomposition to `4.4e-16` and on the corner’s
slopes to three decimals.
Polish is solved on both proved instance cells to machine precision.
One hypothesis is confirmed, four are refuted informatively, and the campaign has a
defect log good enough to predict its own regressions.

**The bottleneck has moved from polish to proposal.** Nothing in the current toolkit
reaches Trump’s standing side, and the refiner cannot rescue the tested starts by
construction; no terminal-component relation has been measured.
The named candidates are δ-continuation, angle-class search as a *search* rather than an
assumption, neighbour-transfer seeding, and quality-diversity retention—none built.

**The premise is still untested, and now blocked on a harder question than expected.**
Everything the strategy layer recommends rests on record basins being rare in quench
measure, and [H-012](campaign/hypotheses/H-012-record-basins-are-rare.md) is the
measurement that would refute it.
The quench supplies one needed instrument, but full event retention, independent pose
validity, and terminal identity are not ready.
What is not settled is what a basin *is*.

[D-034](defects.md) is the open defect that says so.
The exact `n=3` side-2 sliding family proves that one connected optimal set produces
many geometric keys.
Its open stratum retains one contact certificate, but the wall endpoint has a different
certificate after node attributes were restored; exp-014 fixes the stale closed-family
claim recorded as [D-140](defects.md).
At `n=5`, two rows also share side, short form, contact certificate, angle signature,
and contact count while differing geometrically.
That is strong evidence of unresolved terminal identity, but raw contact counts do not
prove an exact family dimension and matching side/contact data do not prove the two rows
are path-connected; generalized tangent evidence and certified continuation must decide
those claims.

So `distinct_basins` currently counts family members, the discovery curve cannot
plateau, and H-011’s saturation criterion is unreachable until the definition is fixed.
The three candidate definitions are written up on `think-1s0h`; none is a code tweak,
because this is the deliverable’s own shape.
Until that is settled and the census runs, the cartography program is a well-argued bet
rather than a finding.

The
[mathematical-frontier review](docs/project/reviews/review-2026-08-23-mathematical-frontier-strategy.md)
now keeps several independent routes alive rather than making the census spine the whole
program: Trump’s nonsmooth local geometry, exact small-`n` quotient spaces, held-out
construction surgery, pure-point piercing limits, robust restricted-angle proofs,
`s(12)`, `s(61)`, exact record fields, and the asymptotic waste exponent.

**The small-`n` lane was missing its direct prior art.** [D-139](defects.md) records the
omission. Two primary hard-square configuration-space papers are now archived; the
Plakhta paper remains explicitly publisher-blocked, so no novelty language is permitted
until its scope is checked from a lawful primary copy.

**The first fast rotation is cheap and high-information.** Exp-012 refuted H-024,
exp-013 confirmed H-026 and locally isolated Trump’s pose, and exp-014/015 solved the
exact `n=3,4` quotient controls in 1.28 wall seconds.
Next regenerate the `n = 5` equal-side pair with full poses and a declared component
relation; reproduce Stromquist’s complete mechanism; and hide the UnitSquare `n = 68,69`
children for the first parent-surgery test.
The quantitative Trump successor is an explicit isolation radius or minimal-support
stress analysis, not another rank count.
No hour-scale lane is promoted without a known-answer response, independent validity,
and a result that changes a decision.

**One open measurement defect constrains timing forecasts.** [D-101](defects.md): the
historical exp-007/008 round-level wall times disagree with retained per-call durations.
Price the first maps from raw calls or a current receipt until those aggregates are
reconstructed.

**One contained defect constrains every polished number.** [D-021](defects.md): the
solver floor is about `1e-11` in the side, so the `polished` tier cannot resolve finer.
The general fix is an exact LP over certified rational or algebraic coefficients; the
rational special case alone is not a universal remedy.

**The destructive negative-control path is closed.** [D-035](defects.md): `negctl` now
mutates bounded private source snapshots, so a killed control can abandon only temporary
data and cannot leave deliberate sabotage in the checkout.

**Checker timeouts remain open.** [D-129](defects.md): a stuck negative-control command
can still stall the gate and leave a shell descendant alive.
This is operational robustness, not a live-source isolation risk; `think-cns0` owns
bounded process-group cleanup.

**One open defect makes quench evidence load-dependent.** [D-126](defects.md): the
scientific work budget is still wall-clock time, so contention changes the number of LP
solves and probes performed.
Price and compare basin experiments by retained work units; use the wall clock only as a
recorded outer deadline.

## References

Primary sources are archived locally under [`resources/`](resources/README.md); the
citation keys below resolve there and in the per-case [`frontier/`](frontier/README.md)
artifacts. Each entry names what this project relies on it for.

- Stromquist, W. (2003). *Packing 10 or 11 unit squares in a square.* Electronic Journal
  of Combinatorics 10(1), R8. Supplies `s(10)`, states the `s(11)` lower-bound value,
  and proves the `0°`/`45°` class bound.
  Exp-016 refutes its printed unrestricted Figure 14 cover; exp-017 independently
  certifies the same value with a source-distinct repair.
- Trump, W. (1979). The `n = 11` packing, as published on the *Squares in Squares*
  record page with Ellsworth’s exact solution in the SVG source.
  The standing upper bound.
- Friedman, E. (2009). *Packing Unit Squares in Squares: A Survey and New Results.*
  Electronic Journal of Combinatorics, DS7. The survey the corpus is checked against.
- Erdős, P. and Graham, R. L. (1975). *On packing squares with equal squares.* The
  asymptotic waste line of work.
- Nagamochi, H. (2005). *Packing unit squares in a rectangle.* The general lower bound
  covering 63 of the 65 open cases in the corpus.
- Montanher, T. et al.
  (2018). *Rigorous packing of unit squares into a circle.* The only rigorous
  computer-assisted optimality proof for rotatable unit squares in any container, and
  the scope limit on what `sqpack` claims.
- Doye, J. P. K., Miller, M. A. and Wales, D. J. (1999). The double funnel energy
  landscape of the 38-atom Lennard-Jones cluster.
  The precedent behind the rarity premise.
- Stillinger, F. H. and Weber, T. A. (1982). Inherent structures and the quench map.
  The decomposition T-2 supplies a cell-exact version of.
- Mouret, J.-B. and Clune, J. (2015). *Illuminating search spaces by mapping elites.*
  The precedent behind H-015.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
