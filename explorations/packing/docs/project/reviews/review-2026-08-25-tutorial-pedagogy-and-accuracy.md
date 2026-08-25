# Review: `TUTORIAL.md`, Read as Its Declared Audience

**Date:** 2026-08-25

**Author:** Claude (agent), from a reader’s questions

**Status:** Current — findings only.
No edit has been made to [`TUTORIAL.md`](../../../TUTORIAL.md); each finding names a
proposal and leaves the wording open.

**Scope:** the tutorial’s own job — the conceptual on-ramp.
[`SYNOPSIS.md`](../../../SYNOPSIS.md) remains authoritative for every result, status,
count, and verdict, and nothing here proposes moving status prose into the tutorial.

The tutorial declares its audience as “anyone arriving at this directory without a
background in the problem.”
This review reads it as that person, records where the document stops being followable,
and separately re-checks its claims against the record.

Two groups, because the difference matters here.
**Accuracy** findings are claims that no longer match the record.
**Exposition** findings are places where the document is not wrong but cannot be
followed by the reader it names.

## What Holds

Stated first so the scope of the checking is clear, and because most of the document
survives it.

Verified against [`SYNOPSIS.md`](../../../SYNOPSIS.md),
[`conventions.md`](../../../conventions.md), the frontier artifacts, and the source: the
`n = 11` bounds, the gap of `0.088229208023`, and the degree-8 minimal polynomial; the
14-of-55 exactly-zero pair separations and 20 boundary corner coordinates;
`2 + (4/3)√2 ≈ 3.885618` for the `0°`/`45°` class, and the claim that `n = 11` is the
first case where oblique tilt is proved to beat it; the `4.4e-16` agreement between the
two independent LP implementations and the `1.3e-15` worst centre error; the D-029
`n = 10` figures (`+5.6440e-04` for both the annealer and the fixed-angle solve,
`+4.4409e-16` for the full quench); the 2,001-point `[38°, 42°]` scan landing one grid
step from `a*`; the corner’s one-sided slopes and the two implementations’ ratios; six
angle classes at `n = 29`; the `n = 3` sliding family and its stratum-dependent contact
certificate; the catalogue counts — 20 search strategies in four families (9
constructive, 7 stochastic, 3 exact refinement, 1 workflow) and 30 proof strategies in
six families, each checked against `frontier/search-strategies.yaml` and
`frontier/proof-strategies.yaml`; and the two-then-three unknowns after centre
elimination at `n = 11` and `n = 17`, which matches Bidwell’s two non-axis-aligned
tilts.

Every relative link in the document resolves.

The document’s editorial stance also holds up.
Its closing claim — that a hedge here is usually carrying weight — is supported by the
hedges themselves: the `n = 5`/`n = 10` controls are correctly described as validating
machinery rather than strategy, the corner is correctly scoped to one slice rather than
a rigidity proof, and the lower-bound repair is correctly not attributed to Stromquist.

## Accuracy

### TR-1. The gate has thirty-one steps, not thirty

§6 says “a thirty-step gate all exist, and the whole gate runs in one to two minutes.”

[`SYNOPSIS.md`](../../../SYNOPSIS.md) (“Reading the gate”) and
[`conventions.md`](../../../conventions.md) §10 both say `packing-validate` runs
**thirty-one** steps, and the recorded checkpoint is “all 31 normal-gate steps in 103.91
wall-seconds.”

The timing is right; the count is one low.
Worth considering whether the tutorial should carry the number at all, since it is
exactly the kind of value the document’s own preamble says it does not own.

### TR-2. “None recovered from a search output” is superseded

§6 says every exact configuration in the repository “was authored from published data or
derived analytically, none recovered from a search output.”

[`SYNOPSIS.md`](../../../SYNOPSIS.md) now says `exact` **almost always** means checking
something already known exactly, and names the exception: exp-033’s pair of exact
`n = 5` endpoints, recovered from retained *search* poses at their shared nonoptimal
side, through a dedicated single-instance checker rather than a general tool.

The paragraph’s headline claim — that there is no general executable path from a
numerical candidate to an exact result — is unaffected and remains correct.
The absolute sentence beneath it is not, and it is the sentence a careful reader will
quote back.

### TR-3. §4 credits the wrong baseline column

§4 says that replacing smooth descent with class bracketing “took `n = 5` from `3.4e-08`
to `2.2e-15` and `n = 10` from `5.3e-03` to `1.3e-15`.”

Those baselines are the **annealer** column of the synopsis’s table, not the descent
column:

| `n` | annealer | + angle descent | + class bracketing |
| ---: | ---: | ---: | ---: |
| 5 | `3.4274e-08` | `3.1875e-08` | `2.2204e-15` |
| 10 | `5.318e-03` | `4.507e-03` | `1.3323e-15` |

The endpoints are right and the conclusion is unaffected.
Either name the annealer output as the starting point or use the descent figures.
The same mismatch appears in §4’s `n = 11` sentence — `8.8e-02 → 6.3e-02` spans annealer
to bracketing, while descent sits at `6.999e-02` — though there the synopsis phrases it
the same way, so fixing one should fix both.

### TR-4. The separating-axis statement drops the word the section rests on

§2 says “Two convex polygons are **disjoint** exactly when some line separates them.”

[`SYNOPSIS.md`](../../../SYNOPSIS.md) writes it correctly: “Two squares have **disjoint
interiors** exactly when some line separates them.”

The distinction is the tutorial’s own §1 headline.
Touching is legal, 14 of 55 pairs touch, and the separation that matters is therefore
weak rather than strict.
As printed, the sentence describes the case this project does not have, four paragraphs
after arguing that the case it does have is what makes the subject hard.

### TR-5. The `n = 5` terminal-family lane is absent

exp-033 through exp-036 landed on 2026-08-24, the same day as the tutorial’s last edit,
and the tutorial does not mention them.
They are the campaign’s current frontier: the synopsis gives them their own section
(“The Current `n = 5` Handoff”) and leads “Where This Stands” with them.

Between them they establish an exact fixed-angle optimal face shared by two retained
poses after a `D4` action and relabelling, an exact two-parameter angle-and-slide sheet
containing that face, complete active first-order systems admitting one direction
outside the sheet, and an exact second-order obstruction excluding that direction from
the true Bouligand tangent cone.

This matters for the tutorial specifically, not only for completeness.
§3’s Trap 2 is argued entirely from the `n = 3` sliding family, which a reader can
dismiss as a degenerate toy — three squares, side 2, an obvious slack square.
The `n = 5` sheet is the same phenomenon at a size that is not obviously trivial, and it
is where the project is actually working now.
§6’s account of what is built and §8’s account of what is open are both shaped by it.

### TR-6. Minimum versus infimum, deliberately or not

§1 defines `s(n)` as “the side of the **smallest** square that contains `n`
non-overlapping unit squares.”
[`SYNOPSIS.md`](../../../SYNOPSIS.md) defines it as “the **infimum** of the `s` for
which one exists.” [`README.md`](../../../README.md) uses “smallest.”

Both readings are in use and they agree only because the infimum is attained, which
follows from compactness and has an archived primary source
(`resources/papers/martin-2000-compactness-theorems-geometric-packings.pdf`).

A tutorial is the right place for the one clause that makes the two words agree on
purpose. Filed as a judgement call rather than an error.

### TR-7. One record is attributed and another is not

§1’s table attributes `3.877083…` to Trump 1979. §7 and §8 give `n = 17`’s `4.6755` with
no source. It is Bidwell 1998, per the synopsis’s lay-of-the-land table, and `n = 17`
carries more weight in the argument than its single mention suggests — it is the only
mechanism-matched calibration cell in the campaign.

## Exposition

### TR-8. Notation is never collected, and several symbols are never defined

The document has no symbol table, and a reader meets each symbol where it is first used.

**Never defined anywhere.**

- `oᵢₖ,ₓ`, in §2’s containment row `0 ≤ xᵢ + oᵢₖ,ₓ ≤ s`. Neither the offset `o`, the
  corner index `k`, nor the `,ₓ` component convention is introduced.
  The synopsis does this properly — corners are `(xᵢ, yᵢ) + Rᵢ·(±½, ±½)`, write
  `oᵢₖ ∈ ℝ²` for the four corner offsets, `k = 1…4`. The tutorial dropped the setup and
  kept the consequence.
- `β`, in §5 step 3. The step opens “`β = 0` iff its reduced representative is the zero
  polynomial” without ever saying that `β` is an element of `ℚ(α)`. A second problem
  rides on the first: `β` is then used three ways in two lines — `β = 0` the field
  element, `deg β` the degree of its representative, and `β(α) ≠ 0` that representative
  evaluated at `α`. `src/sqpack/field.py` keeps element and representative distinct in
  its docstring; the tutorial collapses them.
- `a*`, introduced only as “`0°` on six squares and `a*` on five,” so a reader learns it
  is an angle and nothing more.
  It is the *minimising* value of `a`, which is what §2 and §4 then rely on.
- `s*`, one occurrence, in §7’s relaxation-ladder table (`slack δ in side s* + δ`). Here
  the same `*` decoration means the standing-best side rather than a minimiser.
  Two meanings for one mark, neither written down.

**One letter, two meanings.**

- `m` is the integer in `s(m²) = m` (§1) and the minimal polynomial in `deg m`,
  `reduced modulo m`, `deg β < deg m` (§5).
- `α` is the primitive element of `ℚ(α)` (§5, §6) and **Smale’s α-theory** (§5) — four
  paragraphs apart inside one section.
- **gap** carries three senses.
  §1’s table row is upper bound minus lower bound; §3’s “a gap decomposes into a polish
  failure or an exploration failure” and §8’s “the remaining gap” are
  `best_side − standing_best`; §1’s “the whole subject lives in that gap” is informal.
  Only the second matches §9’s vocabulary card.
  The bound gap and the search gap are different quantities and should be named
  differently.

**Scalar versus vector.** §2 introduces only `θᵢ`, per square, then says “fix the angle
vector `θ`.” The vector `θ = (θ₁, …, θₙ)` is never written, so “fix an angle `θ`” reads
as one angle rather than one per square.
The same gap applies to the centres: the LP variable list `(x₁…xₙ, y₁…yₙ, s)` is the
only place a reader learns these are `2n` separate scalars.
One stated rule — subscript `i` means one square, bare means the whole `n`-vector —
fixes every instance.

**Introduced out of order.**

- `a*` is used before `a` exists; `a` appears only in the following paragraph, inside a
  code fence, as part of a sentence rather than a definition.
- The relation between `a` and `θ` is never stated.
  `a` is the shared angle of Trump’s five-square class, so `θ = (0,0,0,0,0,0,a,a,a,a,a)`
  up to labelling. Without that, a reader cannot tell whether `a` is a new object or a
  coordinate on the old one.
- `s(n)` is defined in §1 as the optimal value and bare `s` appears in §2 as a decision
  variable, with the distinction never drawn — though it is load-bearing at “note `s`
  appears here, and only here, as a variable.”
- `φ` is defined inside a code fence, with no domain, no codomain, and its dependence on
  the fixed cell only in the surrounding prose.
  §4 then reasons about `φ` throughout.

**Cross-document collisions**, lower priority and out of the tutorial’s control, but a
glossary should either match the other documents or say it is local:

| Symbol | Here | Elsewhere |
| --- | --- | --- |
| `θ` | per-square angle | the tilt of the five central squares in the `n = 11` report — this document’s `a` |
| `u` | the single primitive element `tan(a/2)` | the per-square rationalising parameter `u_i = tan(θ_i/2)` in the algorithms report |
| `α` | primitive element | a gap distance, and the Roth–Vaughan real parameter, both in the `n = 11` report |
| `ν` | separating axis (synopsis) | the matching number of a hypergraph in the `n = 11` report |

Subscripts are Unicode here and in the synopsis, ASCII in the algorithms report; `ℚ`
here, `Q` there.

**Proposal.** A short notation section early — before or at the top of §2, since §1 is
deliberately prose — giving each symbol, its type (scalar, per-square, `n`-vector, field
element), and whether it is fixed or free.
Then remove the collisions, say what `*` decorates, introduce `a` before `a*`, and state
the subscript rule once.
§9’s vocabulary card covers prose terms, not symbols; the two should stay separate and
cross-link.

### TR-9. The linear program is never written, and §4 depends on a term §2 never defines

T-2 is the tutorial’s central structural claim and §2 presents it as four observations
plus an assertion.

**The program itself is missing.** §2 gives one constraint row — the containment row,
with `o` undefined per TR-8 — and never gives the separation row, which is the
interesting half. It appears only in the synopsis:

> for axis `ν` and order `(i before j)`, `⟨ν, (xᵢ,yᵢ) + oᵢₖ⟩ ≤ ⟨ν, (xⱼ,yⱼ) + oⱼₗ⟩` for
> all `k, l`

A reader of the tutorial alone never sees what a separation constraint looks like, so
“separation along a fixed axis is a linear inequality” has to be taken on faith — and it
is the step the whole decomposition turns on.

**The shape is missing too.** `2n + 1 = 23` variables at `n = 11` is never evaluated,
though `3n + 1 = 34` is.
Row count is worth giving precisely because it is *not* unique: the synopsis records one
separation row per pair in `sqpack.research.quench` against `1,056 = 16 × (11 + 55)` in
`cases.trump11.independent_lp_cell`, two correct formulations of one feasible set.
That contrast teaches something the assertion cannot — that “the LP” is a modelling
choice.

**The cell count is implied and never stated.** Four candidate axes times two orders is
eight choices per pair, so at most `8^C(n,2)` cells — `8^55 ≈ 4.7 × 10⁴⁹` at `n = 11`,
and most of those are empty, since the choices must be jointly realisable by an actual
configuration. Even as a crude upper bound it is what makes “all the nonconvexity is in
the angles and the discrete choice of cell” read as a statement about difficulty rather
than as reassurance.

**No LP background, and §4 silently needs it.** The document never says what a linear
program is or why being one is good news.
The decisive case is §4, whose mechanism for the corner is:

> Where the LP’s optimal **basis** is locally constant, `φ` is smooth and its derivative
> reads off the active constraints.
> A corner is a **change of optimal basis**.

“Basis” is used three times and never defined.
The explanation of the single most-developed result in the document is therefore opaque
to exactly the audience the document names.

What a short on-ramp needs to cover: a linear objective over linear constraints, the
feasible set a polyhedron with an optimum at a vertex; polynomial-time solvability and
`1.28 ms` in practice at this size, against the 34-dimensional nonconvex problem it
replaces; that an LP can be solved **exactly** over rational coefficients, which is why
[D-021](../../../defects.md)’s float floor is an implementation limit rather than a
mathematical one; and one sentence on duality, which the project already leans on —
exp-033 uses an exact dual to prove a cell’s side minimal, and LP duals as
unavoidable-set generators is registered as H-006.

### TR-10. The quench is described too vaguely to follow, and its two loops are collapsed into one

§3 spends most of its length on what the quench is *not* — not a fixed-angle solve (Trap
1), not a component classifier (Trap 2) — and gives the map itself one line:

> This project’s quench is three stages: **solve the LP in the current cell → re-read
> the cell and re-solve to a fixed point → move the angles → repeat.**

Read cold, that sentence leaves four questions unanswered, and it miscounts its own
structure: stage 1 is the first iteration of stage 2’s loop, and there are two nested
repeats rather than one.
A reader also cannot tell whether “the quench map” names a class of deterministic
refinements or one particular algorithm.
It is one particular algorithm.

From [`sqpack.research.quench`](../../../src/sqpack/research/quench.py):

**What type of solve.** A linear program over `2n + 1` variables ordered
`[s, x₀…x_{n−1}, y₀…y_{n−1}]`. Containment is four inequalities per square against the
variable side. Separation is **one** inequality per pair — not four — because the cell
fixes the axis *and* the sign, and fixing the sign is precisely what removes the
absolute value and leaves something linear.
Solved through `scipy.optimize.linprog` over HiGHS at a pinned `1e-10` feasibility, with
every returned solution re-checked against the rows it was given rather than trusting
the solver’s success flag ([D-014](../../../defects.md)).

**What determines the current cell.** `choose_cell` reads it off the *incoming pose*.
For each pair it evaluates all four candidate axes, computes the signed gap (the centre
difference projected on the axis, minus the summed projected half-extents), and takes
the axis of greatest separation together with the sign saying which square is on the low
side. The cell is therefore a function of the current configuration, not an independent
input. That fact is what makes stage 2 necessary, and the tutorial never states it.

**What “move the angles” means.** Cyclic coordinate search over the merged angle
*classes*, one class at a time, each minimised by golden-section search inside a window
that narrows only when a whole sweep fails to improve.
Derivative-free deliberately, because §4’s corner makes a smooth local model
misspecified. An optional final free pass brackets each of the `n` angles individually,
to test whether a class-converged point is genuinely stationary or an artifact of the
merge tolerance.

**Repeat until when, and why.** Two loops.
The inner one repeats solve-and-re-read until `choose_cell` returns the same cell it was
given — a cell fixed point — capped at twelve iterations, and can also stop *unsettled*
with a typed reason: a cell cycle, which first attempts an adjacent-cell closure; a
re-read that came back worse; an LP refusal; or the cap.
An unsettled incumbent may be used as exploratory data, but a caller “may not call an
outer quench converged from it.”
The outer loop sweeps the angle classes until no sweep improves and the window has
shrunk below its floor, or a tolerance is met, or a sweep backstop or the wall-clock
budget runs out.

**Why the inner loop exists** is the missing “why,” and the module docstring states it:
a single cell solve optimises the cell suggested by the incoming centres, but its own
solution may lie in a different cell, so its value is a path-dependent upper bound.
That makes `s(θ)` ill-defined, and an angle search over an ill-defined objective
optimises a moving target — measured here as the cause of Powell and Nelder–Mead doing
worse than plain descent, which is the fact §4 reports without explaining.
Iterating to a cell fixed point removes the path dependence.

Two consequences make this more than a missing detail.

**The basin decomposition depends on which refiner is chosen.** The synopsis is explicit
that a point-basin “is defined *relative to a specific quench*,” and there are two here:
`quench` descends on the angles, `quench_bracket` brackets.
§4 reports swapping one for the other moving `n = 5` seven orders, without noting that
this also changes what “basin” refers to in §3.

**It sharpens §3’s own lesson rather than undercutting it.** §3 says whatever defines a
basin “must be independent of the *search’s* own knobs,” and then describes a quench
that has knobs — a class-merge tolerance, a window schedule, a sweep cap, a wall-clock
budget. The tension is real and already resolved in the record:
[D-020](../../../defects.md) is that defect, and the free pass exists precisely to test
for merge-tolerance artifacts.
Saying so turns an apparent contradiction into the point being made.

### TR-11. Precision is argued but never dimensioned

§5 argues that exactness is not optional and describes the `ℚ(α)` machinery, but never
says what precision to work at, how the regimes relate to hardware, or what each costs.
§5’s evidence-tier table names `f64_screen`, `polished`, and `exact` without saying what
arithmetic sits behind each.

**Four regimes, not two.** The document reads as float versus exact.
There are four, and the third is the one that goes missing:

1. Hardware `f64`, machine epsilon `2.2e-16` — screening and search.
2. `f64` with an error bound, or outward-rounded intervals — proves strict separation
   when the enclosure clears zero, never equality.
   §5 covers this well.
3. **Arbitrary-precision floating point.** §5 already relies on it — high-precision
   Newton before integer relation, and `cases.kingbird29.verify_svg` is a 160-digit
   reconstruction — but never names it as a distinct regime, and so never says the thing
   that matters: more digits is still not exactness.
   §5’s own “a degree-8 relation holding to 500 digits is overwhelming evidence and zero
   proof” is exactly this point, made without the category that would generalise it.
4. Exact `ℚ(α)`, where equality is decidable, and the only tier permitted to say
   *record*.

**The architectural fact that makes exactness affordable is missing.** Every quantity
the separating-axis test evaluates is a polynomial in the configuration variables — four
candidate axes, eight dot products per axis, no divisions and no square roots — so one
implementation is correct over `f64`, over intervals, and over an exact field, with only
the scalar type changing.
That is why `verify_packing(..., sign=exact_sign)` and `sign=float_sign(1e-9)` share one
predicate. §6 calls the verifier “generic over its scalar type” without ever saying why
that genericity is available.

**The costs are measured and absent.**

| Operation | Cost |
| --- | --- |
| Separating-axis pair test, Rust `f64` | 57 ns |
| Same test, Python float backend | 2,726 ns |
| `ℚ(α)` multiplication, degree 8 (`s(11)`), pure Python | 215.5 µs |
| Same, python-flint | 1.2 µs |
| `ℚ(α)` multiplication, degree 62, pure Python | 13 ms |
| Full exact verification of Trump’s packing, 55 pairs, pure Python | 0.35 s |

Two readings follow, and both belong in a tutorial.
Exactness is free where it is used — 0.35 s against a model turn of seconds, so
optimising it is optimising noise.
And the cost is not uniform: the exact-to-float ratio grows with algebraic degree, 177×
at degree 8 and 578× at degree 62, so exact arithmetic is worst exactly where the
problem is hardest. That is the standing constraint against ever putting it inside a
search loop. The three latency tiers from the infrastructure report — agent (1–10 s,
genuinely free), interactive (10 ms – 1 s), inner loop (10 ns – 1 µs executed
`1e9`–`1e12` times) — are the frame that makes this a decision rather than a table.

**The `1e-11` floor invites a wrong reading.** §5 and §8 give the `polished` tier “a
floor of about `1e-11` in the side” with no cause.
A reader who knows `f64` will assume machine epsilon and be wrong by five orders.
It is the LP solver’s feasibility tolerance, pinned at HiGHS’s strictest `1e-10`
([D-021](../../../defects.md)); at the default `1e-7` the solver returned a packing
violating its own separation constraint by `9.876e-08`, and so a side below Trump’s
([D-014](../../../defects.md)). The quench nonetheless reaches `1.33e-15` at `n = 10`,
so the floor is what the tier *guarantees*, not what runs achieve — which §8 says
correctly and §5 does not.

**And one open item is a consequence, not a separate complaint.** §8’s item 6 — the same
seed reaching a different endpoint under a different toolchain — follows from operating
a degenerate linear program in `f64`. It reads as unrelated engineering trouble where it
is placed.

### TR-12. How many polynomial roots a solution needs is never addressed

Every worked example extrapolates from Trump’s packing, which lives in `ℚ(u)` with a
single primitive element of degree 8. Nothing says whether “one `α`” is a fact about
square packings, a fact about Trump, or an artifact of the example.
The natural reading is that the number could be anything, and that reading is wrong in a
way worth one paragraph.

Three questions hide behind it.

**How many primitive elements: always one.** By the primitive element theorem every
finite extension of `ℚ` is simple, since characteristic zero makes every finite
extension separable.
So however many algebraic coordinates a packing has — `3n + 1` of them, each with its
own degree — a single `α` generates all of them, and every coordinate becomes a
polynomial in `α` with rational coefficients.
This is the load-bearing fact under §5 step 1, which currently reads as though putting
the configuration in `ℚ(α)` for one primitive element were obviously available.
It is available, for a reason worth stating.
It pairs naturally with the point §5 already makes well: only one *root* of that minimal
polynomial is the intended one, which is why an isolating interval is part of the field
data and why isolating the intended real root is one of the two guesses to discharge.

**Of what degree: unbounded, and an open question here.** The theorem gives no bound.
The degree is whatever the active contact system forces after elimination: 8 at
`n = 11`, and the record table reaches 62, which is also where pure-Python exact
arithmetic is worst.
[H-038](../../../campaign/hypotheses/H-038-record-number-fields.md) registers exactly
this — which fields, degrees, Galois groups and discriminants occur, and how they follow
from the active cell and angle-class mechanism — and notes that degree is a descriptor
rather than a ceiling.
The counterpoint already in the record is worth keeping beside it: at a Pythagorean tilt
such as `arctan(3/4)` every coordinate is rational and the degree is 1. Degree is a
property of the mechanism, not of `n`.

**Is a packing guaranteed to be algebraic at all: not pointwise.** This is the answer
that connects to the document’s own Trap 2. The optimal *side* is algebraic: with the
half-angle substitution the feasible set is semialgebraic over `ℚ` with no
transcendental functions anywhere, so the set of feasible sides is a projection of a
semialgebraic set and its infimum is algebraic.
An individual optimal *configuration* need not be — where the optimum is a
positive-dimensional terminal family, the family is cut out by polynomials but a point
of it carries a free parameter, and the `n = 3` family’s `t ∈ [1/2, 3/2]` may be
transcendental. The `n = 5` angle-and-slide sheet is a two-parameter version of the same
thing.

So “recover the field” is well posed for a rigid optimum whose active constraints pin it
down, and is not well posed for an arbitrary point on a family.
That is the same distinction §3 draws between a point-basin and a terminal component,
reached from the algebraic side.

> **Unverified.** The semialgebraic argument in the third paragraph is this review’s,
> not the directory’s. The closest existing statements are the
> semialgebraic-feasible-set remarks in the algorithms report, which stop short of the
> projection step. It should pass a W2 review before entering the tutorial, and
> attainment should be attributed to the archived compactness source rather than
> asserted.

### TR-13. No prerequisites, and no references at all

The document names, in passing: linear programming, primitive elements and minimal
polynomials, Gröbner bases in lex order, resultants, PSLQ and LLL integer relation,
Lagrange and Fritz-John conditions in determinant form, Jacobian nullity, Bouligand
tangent cones, interval-Newton, Krawczyk, Smale’s α-theory, Lindemann–Weierstrass, and
Stillinger–Weber inherent structures.

There is nowhere a reader can go to learn any of them.
§10’s table points only to other documents inside this directory, and the document has
no reference list.
A tutorial that says “Stromquist proved” three times does not link the
paper, though a local copy is archived.

Two additions serve two different moments.
A short **prerequisites** note early, covering the four or five concepts §2 and §5 need,
so neither section is read cold.
A **further reading** section near §10 grouping the rest — linear programming; real
algebraic number fields; certified and interval numerics; symbolic elimination; integer
relation; optimality conditions and why a rank drop supplies the missing equations;
energy landscapes, where both Stillinger–Weber and the Doye–Miller–Wales 38-atom cluster
are already cited in the synopsis and invoked here with no pointer; and the problem’s
own literature, all of it archived under [`resources/`](../../../resources/README.md).

**And what implements the exact arithmetic here**, which is a fair question for a reader
deciding whether to trust or reuse it, and which the document never answers:

- Exact `ℚ(α)` is hand-rolled and standard library only — elements are polynomials with
  `fractions.Fraction` coefficients reduced modulo the minimal polynomial, equality is a
  zero-representative test, and sign is rational-interval bisection over an isolating
  interval. No computer algebra system is involved in the decision path.
- SymPy is optional and marginal: only `cases.trump11.derive_field` uses it, to
  re-derive a constant the verifier already carries.
- The LP is `scipy.optimize.linprog` over HiGHS, whose feasibility tolerance is the
  origin of the `polished` floor (TR-11).
- The screening annealer is Rust.
- Named but deliberately unbuilt: python-flint as an accelerated algebraic scalar,
  `msolve` for F4 Gröbner elimination and real root isolation, and any Lean
  formalisation.

The last point earns its place: a reader will assume a project doing exact algebra
depends on a CAS, and it does not.

## Bead Map

The epic is `think-ysoj`. Every finding above lands on exactly one bead.

| Bead | Covers | Kind |
| --- | --- | --- |
| `think-czye` | TR-1 … TR-7 | bug |
| `think-8hdt` | TR-8 | task |
| `think-ejgd` | TR-9 | task, after `think-8hdt` |
| `think-ap15` | TR-10 | task |
| `think-i22v` | TR-11 | task |
| `think-g5o3` | TR-12 | task, after `think-8hdt` |
| `think-i3wv` | TR-13 | task, after `think-ejgd` and `think-i22v` |

The dependencies are notation-first on purpose: TR-9 and TR-12 both need symbols that
TR-8 defines, and TR-13’s reference groups follow from what TR-9 and TR-11 decide to
explain.

## What This Review Does Not Do

It does not edit the tutorial, and it does not decide wording.
Several findings have more than one acceptable fix — TR-1 could correct the count or
drop it, TR-3 could change the verb or the numbers — and the choice belongs with the
edit.

It does not audit `SYNOPSIS.md`, `README.md`, or the research reports.
The cross-document notation collisions in TR-8 were found incidentally and are recorded
because a tutorial glossary has to decide whether to match them; they are not a finding
against those documents.

It does not review the mathematics of the campaign.
Where a claim is checked, it is checked against this directory’s own record, not against
the primary literature — with TR-12’s single exception, which is flagged as unverified.

## Method

`TUTORIAL.md` read in full, then each substantive claim cross-checked against
`SYNOPSIS.md`, `conventions.md`, `defects.md`, the referenced `exp-NNN` artifacts, the
frontier YAML for the catalogue counts, and `src/sqpack/` for the quench, field, and
verifier behaviour. Every relative link resolved programmatically.
The reading order was the document’s own, so the exposition findings record where a
first reader stops rather than where a re-reader would.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
