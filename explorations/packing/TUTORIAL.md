# Tutorial: Square Packing from First Principles

**Audience:** anyone arriving at this directory without a background in the problem.

**Owns:** the conceptual on-ramp—what the objects are, why the approach is shaped the
way it is, and what the research has and has not established.

**Does not own:** the state of the program.
Every result, status, count and verdict lives in [`SYNOPSIS.md`](SYNOPSIS.md), which is
authoritative wherever the two appear to differ.

## 1. The Problem

`s(n)` is the side of the smallest square that contains `n` non-overlapping unit
squares, each free to translate **and rotate**.

Two bounds are immediate:

- **Area:** `s(n) ≥ √n`, because `n` unit squares have area `n`.
- **Grid:** `s(n) ≤ ⌈√n⌉`, by the axis-aligned grid packing.

At `n = 11` those give `3.3166… ≤ s(11) ≤ 4`, and the whole subject lives in that gap.
For a perfect square `s(m²) = m` and there is nothing to say.
The interest is just *above* a perfect square, where the leftovers must be tilted in.

Three features make this different from most optimization problems.

**Touching is legal, and good packings touch constantly.** Disjointness is required of
*interiors* only.
In the best known `n = 11` packing, 14 of the 55 pairs are separated by
exactly zero and 20 corner coordinates lie exactly on the container boundary.
Optima are jammed configurations, not interior critical points, which is why exactness
here is representational rather than numerical ([§5](#5-algebra-versus-numerics)).

**Every upper bound in the history of the subject is a construction.** No
non-constructive upper bound has ever been obtained.
So “searching for a better packing” is not one method among several for improving the
upper bound—it is the only one anybody has.

**`n = 11` is the first case where tilt provably matters.** Stromquist proved that
packings restricted to `0°`/`45°` orientations cannot beat `2 + (4/3)√2 ≈ 3.885618`,
which is *worse* than the best known packing at `≈ 3.877084`. That is not a
contradiction—it is the content of the theorem, and it is the sharpest available
statement of why `n = 11` is structurally unlike the small proved cases.
Everything in [§7](#7-how-the-search-is-approached-and-why) follows from that sentence.

### The state of `n = 11`, in one table

|  | value | status |
| --- | --- | --- |
| best known packing (upper bound) | `3.87708359002281417730789706010096…` | Trump 1979, a construction |
| best lower bound | `2 + 4/√5 = 3.788854382…` | see the note below |
| gap | `0.088229208023` | open since 2003 |

**The lower bound carries a story this project produced.** Stromquist’s 2003 Theorem 2
is the published source, and this repository found that its printed proof is **false as
printed**: an exact open box of side `10001/10000` fits the claimed container and
strictly avoids all twelve printed Figure 14 points.
A separately preregistered, source-distinct repair—moving one point from `(.8, 1.85)` to
`(.79, 1.85)`—restores the whole argument and certifies the same inequality exactly.
The inequality stands; the printed derivation of it does not.
The synopsis records the repair as **T-4** and the falsification as the round that
terminally refuted the hypothesis it was registered against.

Two lessons in that episode generalize: **a published proof is a source, not an
oracle**, and **the cheapest way to learn something is to try to break a thing you
believe.**

## 2. The Configuration Space

A configuration is a centre `(xᵢ, yᵢ)` and an angle `θᵢ ∈ [0, π/2)` for each square,
plus the container side `s`. That is `3n + 1` real coordinates—**34 at `n = 11`**.

Read naively this is a 34-dimensional nonconvex problem with `C(11,2) = 55` disjunctive
constraints, and it is not obvious where to push.
The central structural insight of this project is that the naive reading is the wrong
decomposition.

### The cell decomposition

Two convex polygons are disjoint exactly when some line separates them, and for polygons
it suffices to test lines parallel to their edges.
A square has two distinct edge normals, so each pair of squares has four candidate axes,
plus a choice of which square lies on the low side.

> A **cell** of configuration space is a choice, for each of the `C(n,2)` pairs, of one
> candidate separating axis together with an order.
> A configuration *lies in* a cell when those choices genuinely separate those pairs in
> that order.

Now fix the angle vector `θ` **and** fix a cell.
Four things become true at once:

1. Once `θᵢ` is fixed, the corner offsets are **constants**, so every corner is an
   affine function of the centre alone.
2. Containment, `0 ≤ xᵢ + oᵢₖ,ₓ ≤ s`, is **linear**—and note `s` appears here, and only
   here, as a variable.
3. Separation along a *fixed* axis is a **linear** inequality.
4. The objective is `s` itself, which is **linear**.

So minimising `s` over a fixed cell at fixed angles is a **linear program** in the
`2n + 1` variables `(x₁…xₙ, y₁…yₙ, s)`. That is the result the synopsis calls **T-2**.

**All the nonconvexity has been pushed into exactly two places**: the trigonometric
dependence of the offsets and axes on the angles, and the *discrete* choice of cell.
That factorisation—a small continuous part times a large combinatorial part—is the
premise underneath almost everything else here.

The check that makes it concrete: read the cell off the exact certificate for the best
known `n = 11` packing (eleven angles and fifty-five axis choices, and nothing else),
rebuild the linear program from scratch, and solve it.
**The centres are never given to the solver**—they are what it reconstructs.
It returns the published side to `4.4e-16` and every centre to `1.3e-15`.

### Thirty-four dimensions become one

Trump’s packing uses only **two distinct angles**: `0°` on six squares and `a*` on five.
Hold the cell fixed, vary that single free angle, and you get a function

```
φ(a) = the LP optimum of Trump's cell with the five tilted squares at angle a
```

which is the entire problem, restricted to this cell, in **one** variable.
A scan of `[38°, 42°]` puts its minimum one grid step from `a*`.

Trump’s angle is not an input to that computation.
It is **the argument that minimises a one-dimensional function anyone can plot.** That
is the concrete content of the claim that the honest continuous dimension is the number
of distinct *angle classes*—empirically one or two at small `n`—rather than `3n + 1`.

## 3. Cells, Basins, and Two Traps

The project is most careful here, because both traps were walked into and both cost real
work.

### The quench map

Borrowed from Stillinger and Weber’s *inherent structure* decomposition: the **quench
map** sends a configuration to the local optimum that a deterministic refinement carries
it to. A **basin** is the preimage of one quench endpoint—the set of configurations that
land in the same place.

This project’s quench is three stages: **solve the LP in the current cell → re-read the
cell and re-solve to a fixed point → move the angles → repeat.**

Two derived words carry the project’s central diagnostic:

- **Polish:** refinement *within* the basin you are already in.
  This is what the quench does, and all it does.
- **Exploration:** reaching a *different* basin.
  Nothing in the toolkit does this reliably at `n = 11`.

A gap therefore decomposes into a **polish failure** (right region, weak refinement) or
an **exploration failure** (wrong region, and refinement cannot help).
Which one a number represents **cannot be read off the number**; you establish it by
running the refiner and seeing whether the gap moves.

### Trap 1—a cell is not a basin

A cell **fixes the angles**. A basin **does not**, because the quench moves them.
So a configuration can sit at *exactly* its cell’s optimum and still be far from its
basin’s optimum, with all the remaining gap in the angles and none in the centres.

The dangerous consequence is a reading that feels safe and is backwards: **a fixed-angle
solve that stops improving has not converged to a local optimum of the problem—it has
run out of things it is allowed to move.** Watching it flatten and concluding “wrong
basin” is exactly what the *right* basin looks like when the residual is angular.

That is not hypothetical.
An agent built a fixed-angle probe, called it “the quench”, and **retracted a correct
finding** when it stalled.
On one `n = 10` start: the annealer output and the fixed-angle solve agree to every
digit at `+5.6440e-04`, and the full quench with its angle half reaches `+4.4409e-16`.

### Trap 2—a flat optimum is not a basin either

“The preimage of one quench **endpoint**” presupposes the endpoint is a **point**. It is
not always.

At `n = 3` the exact side-2 optimum contains a connected **sliding family**: centres
`(1/2,1/2)`, `(3/2,1/2)`, and `(t, 3/2)` for `t ∈ [1/2, 3/2]`. One connected optimal
component, infinitely many distinct coordinate keys.
The quench lands wherever in the flat region it happened to enter, and every symptom
mimics a real discovery—distinct coordinates, distinct keys, two rows in the store—while
the side agrees exactly and, along the family’s open stratum, so does the contact
certificate (the wall endpoints carry a different one).

The project’s term for this is a **terminal family**, and its definition is deliberately
strict: local dimension is the nullity of the appropriate independent active-constraint
Jacobian, after quotienting symmetries and accounting for inequalities and stratum
changes. **Raw contact counts cannot supply that rank**—contacts may be dependent, one
contact description may encode several scalar conditions, and angles and cells may
change along a motion.
Subtracting contacts from variables is not a rigidity calculation, and the project has a
logged defect for having done it.

### The generalized lesson, learned twice

- **First version.** Whatever defines a basin must be independent of the *search’s* own
  knobs. A quench that merged nearby angles would make “basin” depend on a merge
  tolerance.
- **Second version.** It must also be independent of the *representation’s* knobs, and
  must not presume a structure—discreteness—that the mathematics does not supply.

Both are the same shape as Trap 1: **an object that fixes more than the mathematics
does, mistaken for the mathematics.** The first was written down; the second was
available from the same argument and was not, and that is why it cost more.

## 4. The Corner

`φ(a)` is not smooth at its minimum.
Measuring one-sided slopes and refining the step, both sides converge—to **different**
values near `0.1747` and `0.384` per radian, stable over five decades.
Two independent LP formulations agree: `0.1747`/`0.3839` at a ratio of `2.1973`, and
`0.1747`/`0.3841` at a ratio of `2.198`. **The derivative does not vanish at the
optimum; it jumps.**

**Why.** Where the LP’s optimal *basis* is locally constant, `φ` is smooth and its
derivative reads off the active constraints.
A corner is a **change of optimal basis**—the set of contacts that bind switches as the
angle crosses `a*`.

**What it bought.** Replacing smooth descent with a **bracketing search over merged
angle classes**—a method that tolerates non-smoothness—and changing nothing else took
`n = 5` from `3.4e-08` to `2.2e-15` and `n = 10` from `5.3e-03` to `1.3e-15`.

**What it did not buy.** Nothing at `n = 11`, which moved only `8.8e-02 → 6.3e-02`. And
it is *not* a theorem that derivative-free methods must fail: Powell and Nelder–Mead did
worse than descent on the tested starts, in this implementation, which is
method-selection evidence and not an impossibility result.
The kink also lives on a one-dimensional slice, so it is **not** by itself a rigidity
proof for the full packing.

This chain—a measurement, a mechanism, a prediction, and a method built on the
prediction that works—is the campaign operating as designed, and it is the single best
worked example to read in full in the synopsis.

## 5. Algebra Versus Numerics

### Why exactness is not optional

Floating point can certify a strict inequality.
**It cannot certify an equality.**

A float verifier needs a tolerance to accept true contacts, and that tolerance is a
blind spot that also accepts overlaps smaller than itself; setting it to zero rejects
the true packing instead.
Both failure modes are demonstrated by a negative control in this directory.
**There is no tolerance that both accepts the exact packing and rejects all
violations**, and raising precision shrinks the blind spot without closing it.

Interval and ball arithmetic do not fix this either.
An enclosure lying strictly above zero *is* a proof of strict separation—but an
exactly-zero separation always yields an enclosure straddling zero, at any precision.
**Interval arithmetic can prove `>`, never `=`.** With 14 of 55 pairs at exactly zero,
that rules interval methods out as the final verifier here.

The fix is therefore **representational rather than numerical**: work in the real
algebraic number field the packing actually lives in, where equality is decidable.

### The number field

1. **Recover the field.** Put the configuration in `ℚ(α)` for one primitive element with
   a known minimal polynomial and an isolating interval for the intended real root.
2. **Represent** elements as polynomials of degree `< deg m` with rational coefficients,
   reduced modulo `m`. Arithmetic is exact.
3. **Decide equality exactly**—`β = 0` iff its reduced representative is the zero
   polynomial. *This is where touching contacts get certified.*
4. **Decide sign exactly**—evaluate on the isolating interval with rational interval
   arithmetic, bisecting when the enclosure straddles zero.
   This terminates because `deg β < deg m` and `β ≢ 0` force `β(α) ≠ 0`.
5. **Run separation and containment** using only those two decisions.
   No floating point appears anywhere.

For Trump’s packing the field is `ℚ(u)` with `u = tan(a/2)`, degree 8. A useful
subtlety: `cos a`, `sin a`, `tan(a/2)` and `s` are all algebraic, but **the angle `a`
itself, in radians, is transcendental** by Lindemann–Weierstrass.
The algebra lives in the trigonometric values, never in the angle.

### The three evidence tiers

The rule is **never extrapolate across a tier boundary**.

| Tier | What it means |
| --- | --- |
| `f64_screen` | a candidate was proposed |
| `polished` | a quench endpoint valued to solver precision—a floor of about `1e-11` in the side |
| `exact` | validity decided over the packing’s own number field |

**A record may be claimed only at `exact`.** A negative gap below that tier is solver
noise, never a discovery—a rule that has already caught a critical defect, when a loose
LP tolerance returned a packing violating its own separation constraint and so a side
below the standing record.

### From a numeric solution to an exact one

This is the step that turns a 15-digit float vector into an algebraic number, and the
mechanism is not the obvious one.

You cannot “solve the constraints in the field”, for two independent reasons: you do not
know the field yet—it is the *output*—and the packing constraints are **inequalities**,
whose minimiser is not a solution of the constraint system.

The actual trick:

> **The numerical solution’s job is to say which inequalities are tight.
> Then you throw the numbers away and solve an equality system.**

Only *discrete* data crosses the float-to-exact boundary—the contact structure.
That is what dodges both problems: once you know which constraints are active, the
inequalities become equalities, and an equality system is something algebra can solve.

1. **Numeric solve**—propose, then quench.
2. **Read off the contact structure**—which corner touches which edge, which corner
   touches which wall, which squares share an angle class.
   Everything downstream rests on this guess.
3. **Write the contact equations.** The unknowns are `s` and the *distinct* non-axis-
   aligned angles, not `3n + 1` coordinates—two unknowns at `n = 11`, three at `n = 17`.
4. **Close an underdetermined system analytically.** A local extremum of `s` on the
   constraint manifold forces a rank drop, so the missing equations are
   Jacobian-determinant conditions—Lagrange/Fritz-John in determinant form.
   The condition is necessary rather than sufficient; roots that are not extrema are
   culled when the reconstruction is verified.
   The practical point is not elegance: it keeps the problem **root-finding**, which
   reaches thousands of digits, rather than **minimization**, which does not reach the
   precision the next step needs.
5. **Solve exactly**—either by elimination (Gröbner basis in lex order, or resultants)
   or by high-precision Newton followed by an **integer relation** algorithm (PSLQ/LLL)
   that recognises the minimal polynomial.
6. **Certify.** Both routes produce *guesses*, and both guesses must be discharged.

**The two guesses, and why they matter more than the algebra.**

- *The contact structure.* Step 2 decided a separation of `3.7e-12` was exactly zero.
  It might not be. Nothing in steps 3–5 rechecks this, so the reconstruction must be
  re-verified independently—numerical proximity does not guarantee algebraic
  correctness.
- *The minimal polynomial.* Integer relation finds a **relation**, not a proof.
  A degree-8 relation holding to 500 digits is overwhelming evidence and zero proof.
  Irreducibility over `ℚ` must be checked, the intended real root must be isolated from
  the others, and the result substituted back exactly.

Certified numerics—interval-Newton, Krawczyk, Smale’s α-theory—are a genuine and
complementary discharge for the second guess’s root-isolation half.
They are **not** a substitute: they never yield the number field, and they can never
certify a contact.

How much of that pipeline exists here decides what the word “exact” can mean in this
directory, and the answer is in [§6](#6-what-is-built-and-what-is-not).

## 6. What Is Built, and What Is Not

The synopsis owns the authoritative status; this is its shape.
A documented method here is not necessarily an available one, and the difference decides
what any result can claim.

**The exact half is real.** Exact `ℚ(α)` arithmetic, the separating-axis verifier
generic over its scalar type, the negative controls, the independently rebuilt LP, the
class-bracketing quench, the Rust screening annealer, and a thirty-step gate all exist,
and the whole gate runs in one to two minutes.
So do the exact results built on them: the lower-bound falsification and its repair, the
exact optimal configuration spaces at `n = 3` and `n = 4`, and the local-isolation
theorem for Trump’s pose.

**The recovery half is not built.** There is **no executable path from a numerical
candidate to a reconstructible exact result**. Every exact configuration in the
repository—Trump’s packing, the `n = 3` and `n = 4` optimal families—was authored from
published data or derived analytically, none recovered from a search output.
Steps 2 through 6 of the pipeline above exist as a tracked, unbuilt work item.
Until they exist, “verify exactly” means *check something already known exactly*, not
*promote something we found*.

**Three instruments run but are not admissible for the claims they look like they
support.** The endpoint store, the canonical identity keys, and the census all execute,
but an endpoint key is not a certified terminal component, and the synopsis names the
blocking defect for each.
Counting rows in that store is not counting basins.

Every capability here is in one of three states: *built*, *built but not admissible*, or
*documented and unbuilt*. The three are genuinely different, and the synopsis marks
them.

## 7. How the Search Is Approached, and Why

There are two layers: the catalogue of everything anyone has ever used, and the strategy
this project actually adopted.

### The catalogue

Twenty search strategies in four families, each cited by the hypotheses that use them,
so the ledger can report which whole families remain untried:

- **Constructive:** grids, hand geometric insight, `45°` tilted families, diagonal
  strips, strip-plus-L augmentation, rational-slope tilts, composition and
  self-similarity, parametric families, asymptotic border constructions.
  *Every record before 2000 came from here.*
- **Stochastic search:** simulated annealing (the current workhorse), billiard and
  inflation, basin hopping, nonlinear programming, SAT/CP, branch and bound over contact
  classes, evolutionary methods.
- **Exact refinement:** fixing the contact graph and solving the polynomial system,
  rigidity-guided enumeration, interval-verified local optima.
- **Workflow:** the human-computer loop against a public record table, which is how the
  tables actually advance.

A parallel catalogue of thirty proof strategies in six families covers the lower-bound
side.

### The strategy: why pointing should beat scaling

> **A validated map of terminal components is the intended deliverable, and records are
> corollaries.**

The reasoning: annealing-class methods sample basins roughly in proportion to their
**volume at the sampling temperature**, so they find the funnel whose *entropy* wins,
not the funnel whose *optimum* wins.
The canonical precedent is the 38-atom Lennard-Jones cluster, whose global minimum sits
at the bottom of a narrow funnel beside a broad one that captures almost every unbiased
run.

If that transfers, scaling the same proposer merely multiplies samples against a small
fixed probability, and the response is to point search rather than enlarge it.

**That reasoning is a precedent, not a measurement.** It enters as a reason to expect a
direction to be productive, never as a fact about this landscape.
Contact counts do not establish rigidity; rigidity does not establish rare attraction;
another author’s basin counts are a property of *their* proposer, not of the problem.
The premise is registered as a hypothesis with a kill criterion—if record basins turn
out to be hit at rates comparable to the modal basin, the cartography program stands
down and the campaign reverts to throughput.

### Steering: keep the loss, change what you keep

The obvious response to “the objective does not reward what we want found” is to reshape
the objective. Two things are wrong with it.

**Auxiliary losses are hackable, and this problem hacks them immediately.** The most
contact-rich arrangements are grid-like, so a naive contact reward steers search *into*
the wide grid funnel—the exact opposite of the intent.
Note the shape of the trap, because it recurs: the grid is high-contact *and common*;
the record is high-contact *and rare*. **Any single scalar they share cannot separate
them.**

**A reshaped loss changes the minimizers**, so what the search finds relates to the
auxiliary objective rather than to `s`, and the exact layer can no longer say what the
result means.

The alternative keeps the objective and changes *what is retained*: a quality-diversity
archive keyed by structural descriptors, whose degenerate cheap version is a taboo on
canonical keys—**never pay twice to rediscover something you have already named.** The
intelligence and the risk concentrate in descriptor design: descriptors must come from
verified canonical data rather than raw floats, must be axes of *mechanism*, and must be
combined so as to separate the grid funnel from oblique structure.

### Relaxation ladders: turn rare-event search into path-following

Embed the hard instance in a one-parameter family whose far end is easy, then track
solutions along the parameter instead of searching for them cold.

| Ladder | Parameter | Easy end | What to watch |
| --- | --- | --- | --- |
| container inflation | slack `δ` in side `s* + δ` | large `δ`: few broad basins | basin splits and merges; the `δ` at which a target basin first exists |
| superdisk | exponent `p` | `p = 1`: circles, orientation-free | where orientation symmetry breaks |
| boundary layer | frozen grid bulk | the pure grid | whether a sheared band re-synchronizes |

Container inflation is the primary one, and it pays three ways from one computation: a
method that can *walk into* regions direct sampling never hits, the barrier scale a map
wants anyway, and a **scalar hardness measure**—“how much slack makes `n = 11` easy” is
a well-posed, reportable number.
Boundary-layer reduction is strictly a *reduction*, not a relaxation: the slice may
exclude the true optimum, and that risk is stated rather than hidden.

### Calibration must match mechanism, not just difficulty

The proved cases used as positive controls, `n = 5` and `n = 10`, are both `45°`
mechanisms (the other proved small cases are plain grids).
They validate **machinery**, not **strategy**—an engine can take them to machine
precision and remain structurally blind to the irrational oblique tilt that `n = 11`
demands and that no proved case exercises.

So record-*finding* needs its own targets, chosen by mechanism: the nearest case whose
record uses genuinely oblique structure, the target at small inflation (which gives a
progress metric that **moves continuously**, unlike binary found/not-found), and
basin-entry tests that separate “search cannot find the region” from “the refiner cannot
hold it”—two failures with identical symptoms and different fixes.

The result that most sharpened this: the annealer, pointed at `n = 17`, returns
**exactly `5.0`**—the trivial grid—on every seed, against a record of `4.6755`. Because
that miss is at a second, independent cell whose record needs oblique structure, the
failure is not specific to `n = 11`; whether it covers every oblique target is an
inference the registry states as such, not a theorem.

### Near-misses are the data

A serious campaign produces thousands of non-record endpoints.
They are not waste—they are the map, the training set for descriptors, the sample for
structure-versus-rarity laws, and the denominator for any coverage claim.

## 8. What Is Known, and What Is Not

What has been established, with the exact limit of each claim, and then what is
genuinely open, ranked by how much of the program rests on it.
Evidence tiers are the ones in [§5](#5-algebra-versus-numerics).

### Established

| Result | Tier | What it does *not* say |
| --- | --- | --- |
| Fixing the angles and every pair’s separating axis makes minimising `s` a linear program | proved | Nothing about *which* cell is best; that choice is the combinatorial hard part |
| Trump’s 1979 packing is valid, over `ℚ(u)` of degree 8, with 14 pairs at exactly zero separation | exact | Nothing about optimality; it is an upper bound |
| `s(11) ≥ 2 + 4/√5` | exact | Not attributed to Stromquist, not externally peer-reviewed, and it does not close the gap to Trump |
| Stromquist’s *printed* 2003 argument fails: an exact **open** box of side `10001/10000` fits the claimed container and avoids all twelve printed Figure 14 points | exact | It refutes the printed derivation, not the inequality, which the repaired cover independently certifies |
| Trump’s pose is locally isolated: 128 branchwise linearized systems, each of exact rank 33 with a strictly positive exact stress | exact | Not global optimality, and not an explicit isolation radius. It holds in the anchored pose-side chart, modulo finite symmetries |
| The one-dimensional class-angle optimum is a corner, with one-sided slopes of `0.1747` and `0.384` per radian | verified (f64) | It is one slice. It is not a rigidity proof, and not a theorem that every derivative-free method fails |
| The exact optimal configuration spaces at `n = 3` and `n = 4` | exact | Only those two cases; `n = 5` and `n = 6` are unsolved |
| Refinement is not the current bottleneck: the same refiner takes the tested proved-control starts to the analytic optima (residuals `≈1e-15`) and leaves the tested `n = 11` starts `6e-02` short | polished | The tier guarantees only `≈1e-11` in the side, so read the residuals as “at the floor”; and it does not establish *why* the `n = 11` starts are far away |

### Open

**1. What a basin is.** The definition presumes each terminal set is a point, and at
`n = 3` an exact connected sliding family shows it need not be.
So the store counts endpoint keys, which may split one component into several rows, and
the denominator of “rare” is not yet a number.
This makes the rarity premise **untestable rather than merely untested**, which is a
stronger objection than doubting it.
Settling it takes Jacobian nullity, feasible tangent directions, and certified
continuation. It is not a code change; it is the shape of the deliverable.

**2. Whether record packings are rare under a named proposer.** The cartography strategy
rests on this, and it has never been measured, because it is a query over the census in
(1). The kill criterion is written down: if record basins are hit at rates within about
ten times the modal basin’s, the strategy stands down and the campaign reverts to
throughput.

**3. Whether any proposer can reach an oblique record.** Two negative measurements: at
`n = 11` five seeds land in a band five times narrower than the remaining gap, and at
`n = 17` the annealer returns the trivial `5×5` grid on every seed against a record of
`4.6755`. What is unknown is whether the named alternatives, none of which is built,
would do better.

**4. What `s(11)` actually is.** The interval `[3.788854, 3.877084]` has stood since
2003 and neither end is known to be tight.
The upper bound is a construction nobody has beaten; the lower bound is now certified
here but is not claimed to be sharp.

**5. What a `polished` number means below `1e-11`.** The float LP solver has a noise
floor there, many rounds sit on it, and no comparison finer than the floor is
admissible. The fix is an exact rational LP, which is unbuilt.

**6. Whether endpoint results reproduce across machines.** Endpoint identity depends on
floating-point behaviour in a degenerate linear program, and the same seed can reach a
different endpoint under a different toolchain.
This is why portable mathematical predicates and provenance-bound characterization are
being separated into different surfaces.

Items 1 and 2 are the ones that decide whether the strategy is sound.
Items 3 through 6 are tractable with known techniques and enough effort.

## 9. A Vocabulary Card

Everything below is used narrowly here.
[`SYNOPSIS.md`](SYNOPSIS.md#terminology) is the authority; this is the short form.

| Term | Means |
| --- | --- |
| **configuration** | `3n + 1` coordinates: a centre and angle per square, plus the side |
| **cell** | a choice of separating axis and order for every pair. Always the configuration-space object; a sweep position is an *instance cell* |
| **quench** | the map from a configuration to the local optimum a refinement carries it to—and this project’s implementation of it. Includes the angle half |
| **basin** | the preimage of one quench endpoint. Defined relative to a specific quench, and presupposes the endpoint is a point |
| **terminal family** | a local-optimal terminal set that is not an isolated point |
| **polish** | refinement within the basin you are in |
| **exploration** | reaching a different basin |
| **corner** / **kink** | a point where one-sided derivatives differ, so the derivative fails to exist rather than becoming large |
| **angle class** | a set of squares constrained to share one angle |
| **gap** | always `best_side − standing_best`, signed |
| **standing best** | the best side ever published for that `n`—an upper bound, not known to be optimal in the open cases |
| **evidence tier** | `f64_screen`, `polished`, `exact`—what a number is permitted to claim |
| **atlas** / **census** | the deduplicated store of endpoints, and an enumeration run to saturation |

## 10. Where to Go Next

| If you want | Read |
| --- | --- |
| the state of the program, and every result with its status | [`SYNOPSIS.md`](SYNOPSIS.md)—**start here after this page** |
| what is in the directory and how to run it | [`README.md`](README.md) |
| every rule the directory runs on, and which are machine-checked | [`conventions.md`](conventions.md) |
| what has gone wrong and what now stops it recurring | [`defects.md`](defects.md) |
| the mathematics of `s(11)` in depth | [Packing 11 Unit Squares](docs/project/research/research-2026-08-22-packing-11-unit-squares.md) |
| how packings are found, refined and verified | [Algorithms and Tooling](docs/project/research/research-2026-08-22-square-packing-algorithms-and-tooling.md) |
| why pointing should beat scaling | [A Search Philosophy](docs/project/research/research-2026-08-23-search-philosophy-and-landscape-cartography.md) |
| what is known for every `n ≤ 100` | [`frontier/`](frontier/README.md) |

The documents here are unusually willing to say what they have *not* established.
That is deliberate: most of the soundness failures logged here pointed in the
**flattering** direction, where the error looks like success.
A hedge in this directory is usually carrying weight.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
