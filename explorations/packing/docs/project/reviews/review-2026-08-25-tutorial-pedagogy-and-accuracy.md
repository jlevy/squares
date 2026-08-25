# Review: `TUTORIAL.md`, Read as Its Declared Audience

**Date:** 2026-08-25

**Author:** Claude (agent), from a reader’s questions

**Status:** Current — findings only.
No edit has been made to [`TUTORIAL.md`](../../../TUTORIAL.md); each finding names a
proposal and leaves the wording open.

**Scope:** the tutorial’s own job — the conceptual on-ramp.
[`SYNOPSIS.md`](../../../SYNOPSIS.md) remains authoritative for every result, status,
count, and verdict, and nothing here proposes moving status prose into the tutorial.

**Basis:** re-verified twice — after merging the deterministic SVG rendering toolkit,
and again after merging the frontier-assurance and witness branch of
[#31](https://github.com/jlevy/thinking-scratchpad/pull/31). The SVG merge added four
figures and changed no prose; all four image paths resolve.
The #31 merge rewrote §5, §6, §8, and §9, replacing the three evidence tiers with an
assurance/method/precision split.
Every finding below was re-checked against the merged text.
**TR-2 is resolved** by #31 and is retained struck through rather than deleted, so the
record shows what the branch fixed.
TR-1 and TR-11 are revised.
TR-15 is new, raised by the migration itself.

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

### TR-1. The gate has thirty-two steps, and every document says thirty-one

§6 now says “a thirty-one-step gate all exist.”
#31 moved this line from “thirty”, so it was touched — it just landed on the synopsis’s
already-stale value rather than the code’s.

The `STEPS` tuple in `src/sqpack/cli/validate.py` — which
[`conventions.md`](../../../conventions.md) §10 names as “the only registration point” —
holds **thirty-two** entries.
The `deterministic SVG rendering` step arrived with the SVG toolkit and no prose count
moved with it:

| Source | Says |
| --- | ---: |
| `TUTORIAL.md` §6 | thirty-one |
| [`SYNOPSIS.md`](../../../SYNOPSIS.md) (“Reading the gate”) | thirty-one |
| [`conventions.md`](../../../conventions.md) §10 | thirty-one |
| `STEPS` in `src/sqpack/cli/validate.py` | **thirty-two** |

Now that all three agree with each other and disagree with the code, the count reads as
settled and is not. `SYNOPSIS.md`’s “all 31 normal-gate steps in 103.91 wall-seconds” is
a different kind of statement — a recorded checkpoint measurement — and should be left
alone rather than edited to 32.

This is the argument for the tutorial not carrying the number at all.
A count restated in three documents is a count that will drift again, and the document’s
own preamble says it does not own values of this kind.
The gate has a `synopsis agrees with the artifacts` step and it did not catch this,
consistent with the repository’s own finding that no soundness defect in the log was
caught by the gate.

Raised on
[#31](https://github.com/jlevy/thinking-scratchpad/pull/31#issuecomment-5407514755) as
item 1, and tracked for the status documents as `think-4b9m`.

### TR-2. ~~“None recovered from a search output” is superseded~~ — resolved by #31

**Resolved.** The sentence is gone.
§6 previously said every exact configuration “was authored from published data or
derived analytically, none recovered from a search output”, which exp-033 had already
falsified.

#31 replaced that whole paragraph with **“Reported-value recovery remains unbuilt and
may be mathematically contingent,”** which states the real limit — the tool cannot infer
a contact model, certify existence near a contact solution, or recover a general
algebraic witness at the reported value — without the absolute that was wrong.
It also names the typed `checker-not-built` gap the command returns.

Retained here rather than deleted so the record shows what the branch fixed.

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

The SVG merge sharpens this rather than settling it.
Trap 2 now carries a figure — the exact `n = 3` quotient map — so the toy case gained a
picture while the non-toy case still has no mention, and the retained
`n5-exact-face-trajectory.svg` that would illustrate it appears in `SYNOPSIS.md` only.

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

### TR-11. Precision is now named but still not dimensioned

**Substantially addressed by #31, and the remainder is narrower.**

The original finding was that §5 argued for exactness without saying what precision to
work at, how the regimes relate to hardware, or what each costs, and that it collapsed
arbitrary-precision floating point into “exact”.
#31’s **Assurance, method, and precision** section fixes the classification half, and
does it better than this review proposed: assurance (`reported`, `numerically-checked`,
`verified`) is separated from method (`numerical-f64`, `numerical-multiprecision`,
`interval-certified`, `exact-algebraic`) and from actual precision and tolerance, with
the decisive sentence stated outright — **“A numerical result remains numerical at
tolerance `1e-100`.”** The `numerical-multiprecision` gloss adds that it “must state the
actual digits or bits and tolerance; it does not mean unlimited precision.”

Three parts of the finding survive.

**The costs are still absent.** The document says which arithmetic decides what, and
never what any of it costs, so a reader cannot answer “what precision should I work at”
for their own task:

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
problem is hardest. That is the standing constraint against putting it inside a search
loop. The three latency tiers from the infrastructure report — agent (1–10 s, genuinely
free), interactive (10 ms – 1 s), inner loop (10 ns – 1 µs executed `1e9`–`1e12` times)
— are the frame that makes this a decision rather than a table.

**The `1e-11` floor still has no cause.** §8’s open item 5, now “What a floating LP
result means below `1e-11`”, says only that “the solver has a noise floor there”.
A reader who knows `f64` will assume machine epsilon and be wrong by five orders.
It is the LP solver’s feasibility tolerance, pinned at HiGHS’s strictest `1e-10`
([D-021](../../../defects.md)); at the default `1e-7` the solver returned a packing
violating its own separation constraint by `9.876e-08`, and so a side below Trump’s
([D-014](../../../defects.md)). The quench nonetheless reaches `1.33e-15` at `n = 10`,
so the floor is what the method *guarantees*, not what runs achieve.

**One architectural fact went missing rather than getting explained.** Every quantity
the separating-axis test evaluates is a polynomial in the configuration variables — four
candidate axes, eight dot products per axis, no divisions and no square roots — so one
implementation is correct over `f64`, over intervals, and over an exact field, with only
the scalar type changing.
§6 used to call the verifier “generic over its scalar type” without saying why that was
available; #31 replaced the phrase with “rational and algebraic separating-axis
verification”, so the claim is gone and the reason still is not there.
It is worth one sentence, because it is why “work exactly” is an affordable policy
rather than a rewrite.

**And one open item is a consequence, not a separate complaint.** §8’s item 6 — the same
seed reaching a different endpoint under a different toolchain — follows from operating
a degenerate linear program in `f64`, and reads as unrelated engineering trouble where
it is placed.

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

### TR-14. §9’s vocabulary card has no stated discipline

§9 says “[`SYNOPSIS.md`](../../../SYNOPSIS.md#terminology) is the authority; this is the
short form.” It has fourteen rows chosen by no stated rule, and the omissions are not
marginal terms.

**Six terms are used in the body and absent from the card**, with body occurrence
counts:

| Term | Uses | Where it matters |
| --- | ---: | --- |
| **proposer** | 6 | §8’s open item 2 is “whether record packings are rare **under a named proposer**”; §7’s strategy argument turns on it |
| **rigidity** | 5 | §3 and §4 both scope claims by it, and the synopsis defines it carefully because contact counts are *not* it |
| **refiner** | 3 | The other half of the proposer/refiner pair, named separately in the synopsis “because the measurement that matters is which one is failing” |
| **descriptor** | 3 | §7’s steering section is built on it, and it is one of the four cartography deliverables |
| **polish failure** / **exploration failure** | 1 each | §3 introduces them as “the campaign’s central diagnostic”, and the synopsis carries a “Not used here” entry warning against the near-miss coinages |
| **quench map** | 1 | The synopsis says “Say ‘the quench map’ where the distinction matters”; the card’s single `quench` row merges the map and the component |

**Four rows drift from the declared authority.** `gap` is defined as
`best_side − standing_best` while §1’s own table uses `gap` for upper bound minus lower
bound, so the card contradicts the document it sits in (also TR-8). `atlas / census`
compounds two different deliverables with two different statuses into one row, and drops
the caveat the synopsis attaches to both — code exists, and it stores endpoint keys that
are not certified terminal components, which is the point §6 spends a paragraph making.
`exploration` is one of the three words the synopsis marks as carrying controlled
multiple senses — with `cell` and `quench` — and the card flags `cell` correctly,
`quench` partially, and `exploration` not at all.
`terminal component` is defined through “terminal set”, which has no row.

**And the order is unstated.** The card opens in dependency order — configuration, cell,
quench, basin — then drifts, so `angle class` lands after `corner` though the corner is
a property of the class-angle objective.

On `basin` in particular: it is present, as the compound row **basin / point-basin**.
But at 26 body occurrences it is the document’s most-used technical term, and the card
defines it through `quench` and then defines `polish` and `exploration` through it —
circular for the first reader the card exists to serve.

**Proposal.** Give the card a coverage rule and apply it; state an order and hold it;
split `atlas` from `census` while keeping the genuine synonym pairs
`basin / point-basin` and `corner / kink`; flag the three controlled-sense words with
their write-this-form rule; and say what the card does not cover, since symbols belong
in the notation table from TR-8 and the synopsis remains complete.

### TR-15. The assurance vocabulary is adopted but not yet self-consistent

#31 migrated the tutorial off `f64_screen` / `polished` / `exact` and onto the
assurance/method/precision split, and the migration is complete — no tier language
survives anywhere in the document.
Three token-level inconsistencies came with it.
All three are also raised on
[#31](https://github.com/jlevy/thinking-scratchpad/pull/31#issuecomment-5407514755),
where they originated; they are recorded here because they are `TUTORIAL.md` edits
whichever branch makes them.

The canonical values are the schema enums in `witnesses/witness.schema.yaml`: assurance
is `reported | numerically-checked | verified`, and method is
`numerical-f64 | numerical-multiprecision | interval-certified | exact-algebraic`.

- **§9’s card drops the hyphen.** The vocabulary card renders the middle assurance value
  as `` `numerically checked` ``, while §5’s table and the schema both use
  `numerically-checked`. The two neighbours in the same cell are exact enum values, so
  the middle one reads as one too.
- **§8 mixes registers inside one table.** The corner row is annotated
  `numerically checked (`numerical-f64`)` and the row directly below it is
  `numerically checked (floating LP)`. `floating LP` is not one of the four method
  values.
- **Two method tokens are used before being introduced.** §5 tokenizes only
  `numerical-f64` and `numerical-multiprecision`, then describes the formal side in
  prose — “exact algebraic replay, rigorous interval certification, and scoped proof”.
  §8 then uses `` `exact-algebraic` `` five times as a token, and `interval-certified`
  exists in the schema without appearing at all.
  Listing all four values in §5 makes the table self-contained and removes a fresh
  instance of the TR-8 problem.

Two things I checked here and withdrew, recorded so they are not re-raised: §6’s “The
retained Schadt `n = 29` decimal pose is numerically checked at 300 digits and tolerance
`1e-100`” is correct — `E-n029-schadt-numerical` in `frontier/evidence.yaml` carries
`assurance: numerically-checked`, `performed_by: repository`, and
`replay_status: passed` at exactly those parameters, distinct from the source’s
`E-n029-schadt-report`. And the three `n = 29` side values that look divergent across
`frontier/n-029.md` and the witness are three different objects, the last deliberately
weaker.

## W2 Correctness Pass, 2026-08-25

An independent correctness-only pass over the rework, under `W2 factual-review`.
Findings are dispositions on claims the rework *introduced*, checked against primary
sources in this directory rather than against the review that proposed them.

### Confirmed

**Every measured number.** The `f64` and exact-arithmetic costs (57 ns, 2,726 ns, 215.5
µs, 1.2 µs, 13 ms, 0.35 s), the 177× and 578× ratios, and the three latency budgets all
match `research-2026-08-22-infrastructure-for-packing-exploration.md`, which records
13,490.5 µs at degree 62 and itself writes “more than 13 ms”.
`1.28 ms`, `2n + 1 = 23`, `1,056 = 16 × (11 + 55)`, and `8^55 ≈ 4.7 × 10⁴⁹` all check.

**The quench description.** Re-read against `sqpack.research.quench`. Variable order
`[s, x₀…x_{n−1}, y₀…y_{n−1}]`, four containment rows per square, one separation row per
pair because the cell fixes axis *and* sign, the cell fixed point, golden-section
bracketing over merged classes, and the free pass are all as described.
The window-narrowing rule is confirmed exactly: it narrows only when a whole sweep fails
to improve, which the module records as the fix for D-030.

**HiGHS.** Both LP implementations call `scipy.optimize.linprog` with `method="highs"`,
so “reached through SciPy” is right.

**Attainment.** `frontier/proof-strategies.yaml` entry 27, “Compactness / limit
arguments”, carries mechanism “Guarantee the optimum is attained”, status `used`, and
cites Martin 2000. The §1 attribution stands.

**Weak separation.** Interior-disjointness holds exactly when a weakly separating line
exists, in both directions, and edge-normal candidates suffice for convex polygons.

**The primitive element argument.** Characteristic zero gives separability, and a finite
separable extension is simple, so one `α` always suffices.

### Corrected

**A collision the rework introduced.** Moving the minimal polynomial to `μ` freed `m`,
but the perfect-square root had already been moved to `k`—which is also the corner index
in `oᵢₖ`. The rework therefore traded one collision for another, and diverged from
`SYNOPSIS.md`, which still writes `s(m²) = m`. Reverted: the perfect-square root is `m`
again, `k` means only the corner index, and the notation card carries both.

**An over-claim on the semialgebraic argument.** TR-12 flagged this as unverified, and
the tutorial asserted the conclusion without naming the step that carries it.
The mathematics is standard and correct—the feasible set is semialgebraic over `ℚ` after
the half-angle substitution, its projection is semialgebraic by **Tarski–Seidenberg**,
and a semialgebraic subset of `ℝ` has algebraic endpoints—so the fix is attribution
rather than retraction.
The theorem is now named, marked as an argument this directory does not otherwise use,
and given a further-reading entry.

**A false completeness claim.** §9’s preamble said the synopsis “is the authority and is
complete”. Two rows are not in it: **terminal set**, which the synopsis uses without
defining, and **feasibility tolerance**, which belongs to the solver.
The preamble now says which rows are local.

**Two terms in `README.md`.** Its Essential Terms table called polish “local
refinement”, a name no other document uses—`SYNOPSIS.md` defines **Polish** and uses it
fifteen times. And it spelled the assurance value `numerically checked` where the schema
enum is `numerically-checked`, the same defect fixed in the tutorial as TR-15. Both
corrected.

### Recorded, not fixed

**The `gap` split has no owner.** The tutorial now distinguishes **bound gap** from
**search gap**, and both `SYNOPSIS.md` and `README.md` define a single unqualified `gap`
as `best_side − standing_best`—which is the tutorial’s *search* gap.
The split is a genuine disambiguation and the tutorial is not wrong, but it introduces
two terms the declared authority does not define.
Deciding whether the split propagates, or whether the tutorial marks the terms local, is
an ownership question and belongs to `think-segx` rather than to a correctness pass.

**Cross-document symbol collisions persist**, as the notation card already records: the
`n = 11` report uses `θ` for the tutorial’s `a`, `u_i` for a per-square parameter, and
`α` for two further things.
Out of scope here; recorded on `think-segx`.

**No document links to the tutorial’s section anchors**, only to the file, so
renumbering to §12 broke nothing.

## Bead Map

The epic is `think-ysoj`. Every finding above lands on exactly one bead.

| Bead | Covers | Kind |
| --- | --- | --- |
| `think-czye` | TR-1, TR-3 … TR-7 (TR-2 resolved by #31) | bug |
| `think-8hdt` | TR-8 | task |
| `think-ejgd` | TR-9 | task, after `think-8hdt` |
| `think-ap15` | TR-10 | task |
| `think-i22v` | TR-11 | task |
| `think-g5o3` | TR-12 | task, after `think-8hdt` |
| `think-i3wv` | TR-13 | task, after `think-ejgd` and `think-i22v` |
| `think-sofa` | TR-14 | task, after `think-8hdt` |
| `think-po3b` | TR-15 | bug, after `think-8hdt` |

The dependencies are notation-first on purpose: TR-9, TR-12, and TR-14 all need terms or
symbols that TR-8 fixes, and TR-13’s reference groups follow from what TR-9 and TR-11
decide to explain.

One half of TR-1 is out of scope here and carries its own bead outside the epic: the
synopsis and conventions both say thirty-one where the code now has thirty-two, which is
drift in the status documents rather than in the tutorial.
That is `think-4b9m`.

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
