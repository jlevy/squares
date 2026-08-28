# Research: Algorithms and Tooling for Square Packing

**Date:** 2026-08-22 (last updated 2026-08-25)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

## Overview

This document surveys the *machinery* of the unit-square packing problem: the programs,
algorithms, data formats, and proof techniques used to find packings of `n` unit squares
in a smallest enclosing square, to turn a numerical packing into an exact algebraic one,
to verify a proposed packing exactly, and to prove bounds with computational aids.

It is the companion to `research-2026-08-22-packing-11-unit-squares.md`, which covers
the mathematics of the `n = 11` case.
That document answers *what is known*; this one answers *how it is computed and
checked*.

Three findings shape everything below and are worth stating at the top.

1. **Searching and verifying are different problems with disjoint tool stacks.** Search
   is a hard nonconvex global optimization over `3n` continuous variables and is
   dominated by stochastic methods.
   Verification is a decision problem that is trivial numerically and delicate exactly.
   Almost all published tooling addresses search.

2. **Exact verification is delicate for one specific reason: optimal packings touch.** A
   valid packing is one whose squares have disjoint *interiors*, which is a *closed*
   condition. In a record packing many squares touch exactly, so the separation is
   exactly zero. Floating point and interval arithmetic can prove a strict inequality but
   can never prove an equality, so neither can certify a tight packing on its own.
   Exact real algebraic arithmetic is required.
   [A reference implementation and measurements are given below.](#exact-verification-over-a-real-algebraic-number-field)

3. **The programs that hold the records are not public.** The current record engine for
   `n` in the low hundreds is a GPU simulated-annealing program written by Thomas Schadt
   and modified by David Ellsworth.
   It is not published, and no open-source tool is aimed at this problem.
   The open-source packing ecosystem targets industrial nesting, where the objective,
   tolerances, and instance sizes are all different.

## Questions to Answer

1. What open-source tooling exists for searching for and testing square packings?
2. What algorithms are used to *search*, and what actually produces the records for `n`
   in the tens and low hundreds?
3. Given `n` unit squares and a proposed placement, what is the fastest known way to
   confirm exactly that it is a valid packing?
4. How is a numerically-found packing converted into an exact symbolic one?
5. How are bounds proved with computational aids, and which computational aids have
   actually been used on which cases?

## Scope

**Included:** packing `n` congruent unit squares into a smallest enclosing square with
unrestricted rotation; the algorithms, programs, file formats, and solver stacks used
for search, symbolic refinement, exact verification, and computer-assisted proof;
adjacent computational literature (circle packing, Heilbronn, nesting) where it supplies
the technique or the only available cost data.

**Excluded:** the mathematics of specific values of `s(n)` (see the companion document);
packing unequal or consecutively-sized squares; bin packing and its complexity theory;
online packing; covering problems.

## Findings

### The problem, stated computationally

Fix `n`. A configuration is a vector

```
(x_1, y_1, θ_1, …, x_n, y_n, θ_n, s) ∈ R^(3n+1)
```

placing unit square `i` centred at `(x_i, y_i)` rotated by `θ_i`, inside `[0,s]²`. It is
a **valid packing** iff

- **containment:** every square is a subset of `[0,s]²`; and
- **non-overlap:** every pair of squares has disjoint interiors.

Both are conjunctions of polynomial inequalities in the variables and in `sin θ_i`,
`cos θ_i`, so validity defines a closed semialgebraic set once the trigonometric
functions are rationalised (below).
Minimising `s` over that set is a nonconvex global optimization problem with an
`n!·4^n`-fold symmetry group from relabelling and quarter-turns.

Two properties drive everything:

- **Validity is closed, optimality is attained on the boundary.** At an optimum many
  constraints are active — squares touch each other and the walls.
  Every downstream difficulty in exact verification traces back to this.
- **Rotations rationalise.** With `u_i = tan(θ_i/2)`, `cos θ_i = (1-u_i²)/(1+u_i²)` and
  `sin θ_i = 2u_i/(1+u_i²)`, so the whole feasible set is semialgebraic over `Q` with no
  transcendental functions.
  This is what makes exact methods possible at all.

### Verifying a proposed packing

#### The predicate: the separating axis theorem

For two convex polygons, the interiors are disjoint iff some line separates them, and a
separating line can always be taken parallel to an edge of one of the two polygons.
This is the **separating axis theorem** (SAT), and it makes the pairwise test finite:
for two squares there are only four candidate axes (two per square, since opposite edges
are parallel).

On axis `a`, project both squares and compare intervals: the pair is separated iff

```
max ⟨a, A⟩ ≤ min ⟨a, B⟩   or   max ⟨a, B⟩ ≤ min ⟨a, A⟩
```

The non-strict `≤` is essential — it is what admits touching squares.
The whole check is `4·(4+4)` dot products per pair, with no divisions and no square
roots, so every quantity tested is a *polynomial* in the configuration variables.
That is why the test transfers to exact arithmetic unchanged.

Containment is the same predicate against the four container edges.

**Complexity.** Naively `Θ(n²)` pairs.
Because the objects are unit squares and the container has side `Θ(√n)`, a uniform grid
of cell size ~2 reduces this to `Θ(n)` candidate pairs, each square having `O(1)`
neighbours. So exact verification is linear in `n` up to the cost of one field operation
— the quadratic term is an artifact of not bucketing, not an intrinsic cost.

**An alternative formulation** appears in the rigorous-proof literature: Montanher,
Neumaier, Markót, Domes, and Schichl use *sentinels* — nine points per square (four
vertices, four edge midpoints, the centre) — and prove that two congruent squares are
non-overlapping iff the sentinels of each avoid the interior of the other.
This converts overlap testing into containment testing, which is what their interval
branch-and-bound machinery consumes.
SAT is cheaper for a one-shot check; the sentinel form is better inside a solver that
needs every constraint in the same syntactic shape.

#### Why floating point cannot certify a tight packing

In a record packing the separations are exactly zero on many pairs.
A float64 evaluation of a quantity that is mathematically zero returns something of
order `10⁻¹⁶`, of either sign, so implementations use a slack tolerance `tol` and accept
a pair when the separation exceeds `-tol`. That tolerance is exactly the blind spot.

Measured on Trump’s `n = 11` packing (details in [Methodology](#methodology)), sliding
one square by `δ` into its neighbour and asking each verifier whether the result is
still a valid packing:

| verifier | valid packing accepted? | `δ = 10⁻⁶` | `10⁻⁹` | `10⁻¹²` | `10⁻¹⁵` | `10⁻¹⁸` |
| --- | --- | --- | --- | --- | --- | --- |
| float64 SAT, `tol = 10⁻⁹` | yes | reject | reject | **accept** | **accept** | **accept** |
| float64 SAT, `tol = 10⁻¹²` | yes | reject | reject | reject | **accept** | **accept** |
| float64 SAT, `tol = 0` | **no** | reject | reject | reject | reject | reject |
| exact, algebraic | yes | reject | reject | reject | reject | reject |

The exact verifier also rejects `δ = 10⁻³⁰` and `δ = 10⁻¹⁰⁰`, and would reject any
`δ > 0`.

The three float rows are the point for this tolerance-based SAT predicate on Trump’s
rounded algebraic coordinates.
With `tol = 0` it rejects the *true* packing because rounding makes some true zeros come
out slightly negative.
With any `tol > 0` it accepts overlaps smaller than `tol`. **There is no tolerance in
this predicate that both accepts the rounded exact packing and rejects all violations**,
so a small f64 residual is not an equality proof.
Raising precision shrinks the blind spot without identifying exact zero.

Generic interval evaluation (`Arb`, `MPFI`, `filib++`) does not identify an unknown
contact from approximate coordinates.
It gives a rigorous enclosure, so an enclosure lying strictly above zero *is* a proof of
strict separation, while a finite-width enclosure around a near-zero residual usually
cannot distinguish equality from a tiny violation.
Structural simplification can return `[0,0]`, and interval-Newton or related methods can
certify a root of declared contact equations.
What interval evaluation alone cannot do is promote a small numerical residual to an
unrecognised exact contact.

#### Exact verification over a real algebraic number field

The correct procedure is to work in the number field the packing actually lives in.
A reusable implementation of everything in this section, with the negative controls and
benchmarks, is in [`explorations/packing/`](../../../README.md).

1. **Recover the field.** The coordinates of a rigid packing are algebraic.
   Put the whole configuration in `Q(α)` for a single primitive element `α`, with a
   known minimal polynomial `m` and an isolating interval for the intended real root.
   The half-angle substitution keeps everything rational in `α`.
2. **Represent elements** as polynomials of degree `< deg m` with rational coefficients,
   reduced modulo `m`. Addition, multiplication, and inversion are exact; inversion is a
   `deg m × deg m` linear solve or an extended-Euclid step.
3. **Decide equality exactly.** `β = 0` iff its reduced representative is the zero
   polynomial. This is where touching contacts get certified.
4. **Decide sign exactly.** For `β ≠ 0`, evaluate its representative on the isolating
   interval with rational interval arithmetic; if the enclosure straddles zero, bisect
   the isolating interval and repeat.
   This terminates because `deg β < deg m` and `β ≢ 0` together force `β(α) ≠ 0`.
5. **Run SAT and containment** using only those two decisions.

Steps 3 and 4 together are a complete decision procedure.
No floating point appears anywhere.

**Applied to Trump’s 11-square packing** (reference implementation written for this
document; see [Methodology](#methodology)):

| quantity | result |
| --- | --- |
| Field | `Q(u)`, `u = tan(a/2)`, `deg = 8` |
| Minimal polynomial of `u` | `5u⁸ − 10u⁷ − 2u⁶ + 14u⁵ + 12u⁴ − 6u³ + 2u² + 2u − 1` |
| All 11 pieces are unit squares (exact side and right angle) | verified |
| Containment in `[0,s]²` | verified; **20** corner coordinates lie exactly on the boundary |
| Pairwise interior-disjointness (55 pairs) | verified; **14** pairs separated with *exactly zero* gap, 41 strictly |
| `P(s) = 0` for the published degree-8 polynomial | verified exactly |
| `s` | `3.87708359002281417730789706010096270637645…` |
| Interval refinements needed | 0 (the initial isolating interval `[0.36, 0.37]` sufficed) |
| Wall time (pure Python, `fractions.Fraction`) | **0.35 s** |

Two things are worth noting.
The 14 zero-gap pairs are precisely what no floating-point verifier can certify — they
were decided by the exact zero test, not by any numerical comparison.
And the recovered 43 digits agree with the 33 digits published in Ellsworth’s SVG, which
is an independent check of the record data.

**Scaling with algebraic degree.** The dominant cost is one multiplication in `Q(α)`,
which grows faster than `deg(m)²` because rational coefficients also grow.
Measured for the degrees that actually occur in the record table:

| degree of `s(n)` | occurs at | ms per field multiplication | relative |
| --- | --- | --- | --- |
| 8 | `s(11)` | 0.34 | 1× |
| 18 | `s(17)` | 2.20 | 6.5× |
| 40 | `s(300)` | 13.69 | 40× |
| 62 | `s(1453)` | 39.69 | 117× |

These are pure-Python numbers; a C implementation over `fmpq_poly` (FLINT) or CGAL’s
algebraic kernel is two to three orders of magnitude faster and would put even the
degree-62 cases in the second-to-minute range.
The practical conclusion is that **exact verification of any known record packing is
cheap** — seconds to minutes — *provided the exact algebraic description is available*.
Recovering that description is the expensive step, not checking it.

#### The exact-arithmetic tool stack

Nobody has published a tool specific to this problem, so an exact verifier is assembled
from general components.

| layer | what it must do | production options |
| --- | --- | --- |
| Real algebraic numbers | exact `+ − × ÷`, zero test, sign | CGAL `Algebraic_kernel_d` / `Exact_predicates_exact_constructions_kernel_with_sqrt` (via CORE or LEDA); FLINT/Calcium (`ca_t`); `msolve`; PARI/GP; SymPy `CRootOf`; Mathematica `Root` |
| Certified numerics | rigorous enclosures for the strict inequalities | Arb (now in FLINT), MPFI, filib++, Moore, C-XSC, Ibex |
| Polynomial system solving | contact equations → minimal polynomial | `msolve` (F4 plus real root isolation, the fastest open-source option), Singular, Macaulay2, Maple `Groebner`, Magma, `FGb` |
| Solution certification | prove a numerical solution is a true isolated root | `HomotopyContinuation.jl`’s `certify` (Krawczyk plus interval arithmetic; Breiding–Rose–Timme), `alphaCertified` (Smale α-theory), Macaulay2 `NumericalCertification` |
| Quantifier elimination | decide statements over the reals directly | QEPCAD B, Redlog, Mathematica `Reduce`, Z3’s `nlsat`, dReal (δ-complete) |
| Approximate geometry | fast, non-certifying overlap tests | Boost.Geometry, GEOS/Shapely, JTS, Clipper2 (integer-exact but fixed-point), the SAT loop written directly |

For the specific question “what is the *fastest* exact verifier”, the honest answer is
that no benchmarked implementation exists, and the fastest available construction is:
grid-bucket the squares to get `Θ(n)` candidate pairs, then run SAT with predicates
evaluated in `Q(α)` using a filtered kernel — a fast floating-point evaluation with an
error bound, falling back to exact arithmetic only when the sign is in doubt.
That is exactly CGAL’s `Exact_predicates_*` design, and it is the right architecture
because in a record packing only the `O(n)` contacts actually need the exact path; the
remaining pairs are separated by a wide margin and are settled in floating point.

For calibration, the approximate check is negligible, and grid bucketing removes the
quadratic term outright.
Measured with the same verifier running its float64 backend (pure Python, so not a tuned
C implementation) on grid packings:

| `n` | pairs, quadratic | time | pairs, bucketed | time |
| --- | --- | --- | --- | --- |
| 11 | 55 | 0.4 ms | 55 | 0.5 ms |
| 100 | 4,950 | 21.5 ms | 1,302 | 8.4 ms |
| 324 | 52,326 | 204 ms | 4,838 | 29 ms |
| 1000 | 499,500 | 1,790 ms | 15,936 | 98 ms |

**Validity checking is never the bottleneck in a search; it is the inner loop, and it is
cheap.**

#### What the record data actually gives you

The canonical record data lives on David Ellsworth’s *Squares in Squares* page (formerly
Erich Friedman’s Packing Center), which covers all `n ≤ 324` plus selected larger cases.
Each packing is an SVG, and the SVG *source* is the data format:

- a `<!DOCTYPE>` internal DTD defining the side length, tilt angle, and derived offsets
  as **33-digit decimal entities**;
- nested `<g transform="translate(…) rotate(…)">` elements placing unit `<rect>`s;
- an XML comment carrying attribution, history, and — for the analytically solved cases
  — the **Mathematica source** that produced the exact solution, plus the minimal
  polynomial of `s` as a `Root[…]` object.

For `s(11)` the comment carries the two contact equations, the `RootReduce[Solve[…]]`
calls,
`s = Root[-6865 + 12420# - 6754#² - 496#³ + 1923#⁴ - 842#⁵ + 178#⁶ - 20#⁷ + #⁸, 2]`, and
the closed form `s = 2 + (2 + sin a)/(cos a + sin a)`.

This has two consequences for anyone wanting to verify records.
The good news: for analytically optimized packings the exact algebraic data is present
and sufficient — the verification above was reconstructed entirely from that SVG. The
bad news: it is prose in an XML comment in a Mathematica dialect, not a machine-readable
schema, and **32 of the 184 pictured packings are flagged “Not yet analytically
optimized”** — for those, only high-precision decimals exist, and no exact verification
is possible until the contact structure is solved.

### Finding packings

#### Perturbed billiard / inflation (Gensane–Ryckelynck, 2005)

The first algorithm that worked for squares.
Friedman’s survey is explicit that “the computer-aided methods available for circles did
not generalize for squares, until recently when an effective algorithm was found.”

The method links `s(n)` to the supremum over admissible configurations of the maximal
*inflation* `ω(C)` — how far you can grow the squares before an overlap — and then
maximises `ω` by a stochastic billiard.
Gensane’s companion paper on spheres in a cube spells out the algorithm, in four layers:

1. **Random Walking(P, N_a, ε, α):** repeatedly pick an object, propose a displacement
   uniform in a ball of radius `ε`, project back into the container if it leaves, and
   accept only if no overlap results.
   Objects move one at a time; the radius `α` is held fixed for the sweep.
2. **Stochastic Billiard(P, ε₁, ε₂, N_a):** run Random Walking; if the separation
   improved, double `ε` and raise `α`, otherwise halve `ε`; stop when `ε < ε₂`. Unlike
   classical billiard algorithms this never computes collision directions explicitly.
3. **Perturbation(P, ε):** displace *all* objects simultaneously by uniform draws of
   magnitude `ε`.
4. **With Perturbations(P, ε₁, ε₂, factor):** alternate 3 and 2, restoring the previous
   configuration and shrinking `ε` on failure.
   Gensane reports using `factor = 10⁵`.

The role of layer 3 is the key idea.
Layer 2 converges to configurations that are *solid* (no single object can be moved to
improve the packing) but not necessarily locally optimal.
Simultaneous perturbations let the search walk along a continuous path of solid
configurations to a genuine local optimum.
Gensane found this necessary in three dimensions and expected it to matter generally.

Results: improved `n = 11, 29, 37` and an alternative optimal `n = 18`;
`s(11) ≤ 3.8772`, `s(29) < 5.9648`, `s(37) ≤ 6.603236`. Notably it *recovered* Trump’s
1979 `n = 11` packing rather than beating it — the first computer packing plausibly
optimal.

#### GPU simulated annealing — the current record engine

The programs actually setting records today are simulated annealers.
The lineage on the record page is: **Thomas Schadt** wrote the annealing program;
**David Ellsworth** runs modified versions of it (versions 2 and 3 are referenced by
name). Of the 184 pictured packings, 47 credit simulated annealing.

Concrete performance data is published for two cases, and it is the only hard data of
its kind for this problem.
Both runs used an **NVIDIA RTX 3080 Ti with the annealer configured for 65,536
threads**:

| case | run | outcome |
| --- | --- | --- |
| `s(51)` | 9 sessions, Jan 31 – Feb 1 2026 | 3,004 basins found; only **4** refine to the record `7.70079923541701…`. 23.6 s per basin. Expected **4.9 hours** of GPU time to hit the record basin once. |
| `s(55)` | 5 sessions, Feb 4–5 2026 | 1,893 basins below `s = 8.0`; the record basin found 3 times. 2.6 s per basin. Expected **41 minutes** to hit a basin that both beats the previous record and refines to the current one. |

Ellsworth’s own words for `s(51)`: the record basin is “an exceedingly rare find.”
This is the characteristic shape of the problem — the objective landscape has a vast
number of nearly-equal local optima, and the record is a needle among thousands of
basins that look almost as good.

The workflow around the annealer matters as much as the annealer:

- **Seeding.** Runs start “from randomness”, or from a neighbouring record with squares
  removed and some straightened (e.g. `s(303)` was found from the `s(305)` record “with
  2 squares removed and 8 straightened”), or from an analytically constructed state.
- **Refinement.** The annealer’s output is a *basin*, not a packing.
  A separate refinement step drives it to the local optimum, and a further analytic step
  (next section) produces the exact value.
- **Statistics-driven search.** The `.stats.txt` files show basins being classified and
  counted so that expected time-to-record can be estimated before committing GPU hours.

None of this code is public.

#### Pattern construction and extension

A large fraction of the table is not search output at all.
Göbel’s 1979 diagonal-strip family, the `s(n²−n−1)` pattern, “Göbel squares”, and “Göbel
strips” give closed-form packings for infinite families, and most entries above
`n ≈ 100` are described as *extending* a smaller record ("Extends the `s(85)` found by
Erich Friedman in 1997") or *adding an L* to a neighbour.
Arslanov, Mustafin, and Shangitbayev’s 2021 proof that `s(n²−n) < n` for all `n > 12` is
a purely constructive argument with hand-derived contact equations and no computer
search.

For large `n` this is the dominant mode: **construct, then locally optimize**, with
search used only to discover the primitive pattern.

#### General-purpose global optimization

The 2026 line of work by Berthold, Kamp, Mexi, Pokutta, and Pólik asks whether
off-the-shelf global solvers can compete, using **FICO Xpress 9.8** and **SCIP 10.0**
with models generated through PySCIPOpt in `.nl` format, a 10,000 s time limit preceded
by a 5,000 s multistart, on a 48-core Xeon Gold 6342.

Their non-overlap formulation for polygons is worth knowing because it is compact and
solver-friendly.
By **Farkas’ lemma**, a system of strict linear inequalities `Ax > b` is
infeasible iff there exist multipliers `y ≥ 0`, `y ≠ 0`, with `yᵀA = 0` and `yᵀb ≥ 0`.
Applying this to “the interiors of polygons `i` and `j` intersect” yields, per pair,
`2m` nonnegative multipliers whose positive-weight combinations of the two polygons’
edge normals must be equal and opposite — which is precisely a separating axis,
recovered as solver variables rather than as an enumeration.
At most two adjacent multipliers per polygon are needed, independent of vertex count.
The alternative in the literature is the **phi-function / quasi-phi-function** technique
of Stoyan, Romanova, and Pankratov, which encodes non-overlap and containment for
objects under continuous rotation as explicit analytic functions; the Farkas form is a
compact special case for polygons.

The results, restricted to squares in a square (their `ℓ = m = 4` family, where the
reported outer circumradius equals `s(n)` exactly), are the clearest available
measurement of how far general-purpose global optimization gets on this problem:

| `n` | SCIP/Xpress best | best known `s(n)` | verdict |
| --- | --- | --- | --- |
| 5 | 2.70711 | 2.70710678… | matches |
| 10 | 3.70711 | 3.70710678… | matches |
| 11 | 3.87709 | 3.87708359… | matches |
| 16 | 4.00001 | 4 | misses the *trivial* grid packing |
| 17 | 4.67682 | 4.67553009… | worse |
| 19 | 4.88638 | 4.88561808… | worse |
| 26 | 5.62273 | 5.62132034… | worse |
| 27 | 5.82848 | 5.70710678… | much worse — it returns Göbel’s `3 + 2√2 ≈ 5.82843` arrangement, which holds 28 |
| 28 | 5.88678 | 5.82444462… | worse |
| 29 | 6.00000 | 5.93383346… | worse (finds the trivial packing) |

So: state-of-the-art general-purpose global optimization, given hours per instance,
reproduces the known records up to about `n = 16` and then falls behind, sometimes
badly. It also fails to reach exactly 4 at `n = 16` and exactly 5 at `n = 24`, returning
`4.00001` and `5.00001` — a reminder that these are numerical optima under a `10⁻⁸`
feasibility tolerance, not certified values.
The same authors *did* improve records for triangles-in-squares (`n = 12`) and several
polygon-in-pentagon families, so the negative result for squares-in-squares is specific,
not a general weakness of the approach.

The authors also name the structural obstacle: pairwise non-overlap constraints grow
quadratically, “a computational obstacle when one moves towards instances with hundreds
or thousands of objects,” and propose lazy separation of violated constraints as the
fix. Their solution database is open (`DominikKamp/Packing`).

#### LLM-driven and evolutionary search

Google DeepMind’s **AlphaEvolve** (May 2025) applied LLM-generated-code evolutionary
search to a benchmark of 67 mathematical problems spanning analysis, combinatorics,
geometry and number theory, rediscovering the best known solution in most cases and
improving it in several.
Among them were circle and hexagon packing: it improved the packing of 11 unit regular
hexagons in a hexagon to side `3.931`, against a human record of `3.943` (2019). It is a
genuinely relevant data point, because the mechanism it found — tilting inner pieces at
varying angles rather than aligning them — is the same mechanism that makes square
packing hard.

**What has happened since, as of August 2026.** The benchmark AlphaEvolve published has
become a small competitive ecosystem, and its trajectory is worth tracking closely
because it is the closest thing to a live experiment in whether this class of method can
move a geometric packing record.

- **Open replications** appeared quickly (`OpenEvolve`, `ShinkaEvolve`, `CodeEvolve`),
  and were followed by a steady run of successor systems: ThetaEvolve
  (arXiv:2511.23473), the FM Agent (arXiv:2510.26144), ImprovEvolve (arXiv:2602.10233),
  Helix (arXiv:2603.07642), SeaEvo (arXiv:2604.24372), and a flow-based generative
  approach to extremal structure discovery (arXiv:2601.18005).
- **Classical solvers answered, and largely won.** Berthold, Kamp, Mexi, Pokutta and
  Pólik revisited the AlphaEvolve benchmark with off-the-shelf global optimization
  (arXiv:2601.05943, January 2026) and report that FICO Xpress and SCIP “reproduce, and
  in several cases improve upon, the best solutions previously reported in the
  literature, including the recent LLM-driven discoveries.”
  Their follow-up (arXiv:2605.04850, May 2026) adds an S-lemma containment formulation
  for ellipses and Farkas-lemma non-overlap for polygons and Platonic solids, and
  reports new incumbents across those families.
  In the OpenEvolve replication the LLM had itself converged on writing an
  *optimization* program — SciPy SLSQP from multiple starts — rather than a bespoke
  heuristic, which is the same conclusion arrived at from the other direction.
- **Individual humans remain competitive at the margin.** On the `n = 26`
  circles-in-a-square sum-of-radii benchmark, an independent worker beat AlphaEvolve’s
  `2.63586275` with `2.63592717` after roughly six weeks, using a genuinely different
  configuration rather than a refinement; the flow-based system later pushed the same
  benchmark to `2.63598308`.

**The conclusion for this problem is unchanged, and is the interesting part: none of
this activity has touched squares-in-squares.** No AlphaEvolve-class result for `s(n)`
has been reported by any system in the ecosystem, and the benchmark suite does not
include it. Meanwhile the actual `s(n)` records continue to be set by one closed-source
simulated annealer run by one person.
The adjacent benchmarks are crowded and contested to the fifth decimal place; this
problem is uncontested and has no open baseline at all.
That asymmetry is an opportunity rather than a verdict — see
[Recommendations](#recommendations).

#### Industrial nesting engines

The mature open-source packing code targets *nesting*: cutting shapes from stock.
It is the closest thing to a reusable library, and it is worth knowing exactly why it
does not solve this problem.

| project | language / licence | what it is | fit for this problem |
| --- | --- | --- | --- |
| `jagua-rs` | Rust, MPL-2.0 | Collision detection engine for 2D irregular C&P; quadtree, hazard proximity grid, fail-fast surrogates; continuous rotation and translation; “millions of collision queries per second”; INFORMS J. Computing paper | Best available *geometry backend*. Tolerance-based, not exact. |
| `sparrow` | Rust | State-of-the-art nesting optimizer built on `jagua-rs` | Strip packing objective, not min-enclosing-square |
| `packingsolver` | C++, MIT | Rectangle, guillotine, box, boxstacks, 1D, and irregular; tree search and column generation; irregular solver supports continuous rotation | Bin/knapsack/strip objectives; not tuned for congruent-square min-container |
| `libnest2d`, `deepnest`, `SVGnest` | C++/JS | No-fit-polygon nesting used in slicers and laser cutting | Discrete rotation sets in practice; industrial tolerances |
| OR-Tools CP-SAT (`no_overlap_2d`) | C++/Python, Apache-2.0 | Exact integer 2D no-overlap | Axis-aligned only — cannot express the tilt that makes `s(11)` interesting |

The mismatch is structural.
Nesting minimizes strip length or bin count under a manufacturing tolerance, with
hundreds of distinct shapes; this problem minimizes a container dimension to 30
significant digits with `n` identical shapes.
A nesting engine will happily return a packing that is `10⁻⁶` infeasible, which is fatal
here and irrelevant there.

`jagua-rs` is nonetheless the sensible foundation if someone wanted to build a modern
open-source searcher: it solves the collision-detection engineering properly, and the
annealing or billiard layer on top is comparatively simple.

### From a numerical packing to an exact one

This is the step that turns a 15-digit float vector into `s = Root[…]`, and it is where
symbolic computation enters.

#### The contact-equation formulation

Read the contact structure off the numerical solution: which square corner touches which
square edge, which corner touches which container wall.
Each contact is one polynomial equation.
The unreduced system contains centre coordinates as well as `s` and the angles.
In the structured constructions discussed by Ellsworth, the contact graph lets those
centres be eliminated, leaving `s` and the distinct non-axis-aligned angles—usually far
fewer than `3n`. That elimination is a property to derive from each graph, not a
consequence of angle classes alone.
Ellsworth’s reduced notation names the angles `a, b, c, …` and the constraints
`f1, f2, f3, …`; `s(17)` then has three unknowns `{s, a, b}`, `s(55)` has eight.

If the number of constraints equals the number of unknowns, the system is square, and
`FindRoot[]` (multivariate Newton) refines to arbitrary precision, or `Solve[]` gives a
closed form outright.

#### The underdetermined case and the Jacobian-determinant trick

Frequently there are *fewer* constraints than unknowns — the contact structure leaves a
one-parameter family, and `s` must be minimized along it.
Ellsworth’s solution, worked out in December 2024, is to add the missing constraint(s)
analytically rather than resort to `FindMinimum[]`:

```
grad = Grad[{s, f1, f2, f3}, {s, a, b, c}]
Det[grad] == 0
```

The reasoning: the matrix maps variable deltas to deltas of `s` and of the constraint
values.
If the matrix is invertible it can hit the target vector `{1,0,0,0}`—a delta that
decreases `s` while holding every constraint at zero—so an extremum forces the matrix to
be singular. A local extremum of `s` on the constraint manifold therefore satisfies
`Det[grad] = 0`. The condition is necessary rather than sufficient: a rank drop can
occur away from an extremum, and spurious roots are culled when the candidate is
verified. When the deficiency is two or more, nest the construction:

```
f2 = Det[Grad[{s, f1     }, {s, a     }]];
f3 = Det[Grad[{s, f1, f2 }, {s, a, b  }]];
```

In the two-variable/one-constraint case this collapses to `D[f1, a] == 0`, which
explains why that ad-hoc rule had worked earlier for `s(39)`, `s(87)`, and `s(41)`. This
is a rediscovery of the Lagrange/Fritz-John first-order conditions in determinant form,
and it matters practically: it keeps the problem a *root-finding* problem, which
`FindRoot` solves to thousands of digits, instead of a *minimization* problem, which
does not reach the precision needed for the next step.

#### Numeric-to-symbolic recovery

With `s` to a few hundred or thousand digits, an integer relation algorithm recovers the
minimal polynomial: `RootApproximant[]` in Mathematica, `algdep` in PARI/GP,
`minimal_polynomial`/`nsimplify` in SymPy, PSLQ or LLL directly.
This is why the precision matters — `FindMinimum[]` output is not precise enough for
`RootApproximant[]` on complicated packings, but `FindRoot[]` output is.

The degrees that come out are large and grow with the complexity of the contact graph: 8
for `s(11)`, 18 for `s(17)`, 4 for `s(302)`, **40** for `s(300)`, **62** for `s(1453)`.
The `s(300)` polynomial has 41 integer coefficients, the largest with 56 digits;
`s(128)` and `s(205)` are the same degree-40 family with 48- and 52-digit coefficients,
which is what “extending a smaller record” costs algebraically.

#### Elimination

The alternative is pure elimination: write the contact equations, compute a Gröbner
basis in a lexicographic order or take resultants, and read off the univariate
polynomial for `s`. Gensane and Ryckelynck did this for `s(11)` in 2004 by “eliminating
with a system of 14 equations”.
Ellsworth’s note that the same result follows from two equations is a fair criticism of
the formulation, not of the method — elimination is exponential in the number of
variables, so the formulation is the whole game.
`msolve` is the current fastest open-source implementation; Singular, Macaulay2, Maple,
and Magma are the alternatives.

#### The published template: Heilbronn

The closest thing to a written-down, reproducible version of this pipeline is not in the
square-packing literature at all — it is the 2026 Heilbronn triangle work, which calls
it **optimize-then-refine**:

1. Solve a mixed-integer nonlinear model to certified global optimality with Gurobi,
   obtaining matching bounds and a numerical configuration (`n = 9` in ~15 minutes,
   versus ~1 day for the prior approach).
2. Read the *critical* structure off that solution — which triangles achieve the minimum
   area, which points lie on which edges.
3. Convert that structure to a square polynomial system and solve it exactly: SymPy’s
   symbolic solver for `k ≤ 6`; a lexicographic Gröbner basis for the cubic-extension
   case; and for the largest case, recognise the number field (`Q(√65)`) from the
   numerics and re-express all coordinates in it with `nsimplify`.
4. **Verify every candidate by exact substitution into the full polynomial system**,
   because “numerical proximity does not guarantee algebraic correctness” — their
   certified values carry only about six significant digits.

Step 4 is the transferable discipline.
Applied to square packing it is exactly the exact-verification procedure described
above.

### Proving bounds with computational aids

Here the honest summary is short: **in the published literature, essentially no proof
for squares in a square has been computer-assisted.** Within this repository that is no
longer true of the lower bound: exp-017 carries an exact computer-assisted certificate
of `s(11) ≥ 2 + 4/√5` (the synopsis’s T-4), not externally reviewed.

#### Lower bounds: unavoidable points, by hand

Every proved value of `s(n)` rests on the *unavoidable point set* method, due to
Stromquist and developed by Friedman.
To show `s(n) ≥ k`, exhibit a set `P` of `n − 1` points in a square of side `k` such
that *every* unit square placed in it contains a point of `P`. Shrinking by `1 − ε/k`
makes the containment strict, so at most `n − 1` disjoint unit squares fit in side
`k − ε`, hence `s(n) > k − ε` for all `ε`, hence `s(n) ≥ k`.

Friedman’s proofs of `s(2) = s(3) = 2`, `s(5)`, `s(8) = 3`, `s(15) = 4`, `s(24) = 5`,
`s(35) = 6` each consist of an explicit list of points plus a citation to two or three
lemmas about where a unit square with its centre in a given cell must reach.
The harder cases `s(7) = 3` and `s(14) = 4` add *almost* unavoidable sets, forcing two
squares into identified regions, then enumerate the placements up to symmetry — 2 cases
for `n = 7`, 5 for `n = 14`, with sub-cases — and supply a fresh unavoidable set for
each. Wolfram Bentz’s proofs of `s(13) = 4`, `s(46) = 7` (2010) and `s(22) = 5`,
`s(33) = 6` (arXiv 2016; proof dated Oct 2018 by the catalogue) strengthen the method by
replacing fixed point sets with “continuously varying families of such sets.”
Nagamochi’s `s(n² − 1) = s(n² − 2) = n` for all `n ≥ 2` is a counting argument about how
many unit squares fit in an `a × b` rectangle.

The lemmas themselves are single-variable calculus — minimise `D(θ)`, differentiate,
find the critical angle — done by hand.
Everything is checkable by a referee with a pencil.
Nothing here required a computer, and nothing here has been formalised.

Note that *verifying* a claimed unavoidable set is itself a natural computational
problem: “does every unit square in `[0,k]²` contain a point of `P`?” is a decision over
three parameters `(x, y, θ)` and is exactly the kind of statement an interval
branch-and-bound or a nonlinear-arithmetic SMT solver is built for.
No published work does this.

#### The only rigorous computer-assisted result for rotatable unit squares

Montanher, Neumaier, Markót, Domes, and Schichl (*J. Global Optimization*, 2018) give
the first — and as far as this research found, still the only — computer-assisted
optimality proof for packing rotatable unit squares in any container.
The container is a **circle**, and the result is for **three squares**:

```
r_3 ∈ [1.288470508005_47, 1.288470508005_53]
```

Their machinery, which is what a square-container attack would have to look like:

- **Interval branch and bound** in C++ over `filib++`, with the results reproduced over
  the `Moore` library; code published with the paper.
- **Containment** by convexity: a rotated square lies in the disc iff its four vertices
  do.
- **Non-overlap** by the sentinel construction described earlier.
- **Symmetry breaking by tiling:** the search box is cut into 36 isosceles triangles
  with base `< 1`, guaranteeing at most one centre per triangle; the first square’s
  angle is fixed at `0`. Rotations and reflections then reduce the `C(36,3) = 7,140`
  triples of triangles to **12** subproblems needing rigorous verification — under 1% of
  the total.
- **Cost:** phase 3 (three squares) took **628 s** for the decisive subproblem on a
  laptop, with earlier phases hitting 3,600 s time limits.

The authors state plainly that “packing of unit squares into a container is considerably
harder to solve than their circle packing counterparts” because of the rotation angles,
and that the existing square-in-square optimality proofs (`n = 5…10, 13, 46`) do *not*
rely on computer assistance.

Three squares in a circle taking ten minutes, against `s(11)`'s eleven squares with a
degree-8 irrational optimum, is the measurement that explains why nobody has attacked
`s(11)` this way.

#### What the circle-packing literature achieves, for calibration

Circles are the control group: same style of problem, no rotation variables, and there
the interval methods work.

- Markót and Csendes (*SIAM J. Optimization*, 2005) proved optimality for **28, 29, 30**
  circles in a unit square by a fully interval-arithmetic global optimization method,
  taking about **53, 50, and 21 CPU hours**.
- Markót’s improved method (*J. Global Optimization*, 2021) proved **31, 32, 33** in
  **26, 61, and 13 CPU hours** using the **C-XSC** library — a 40–100× speedup over the
  2005 method, which would have needed 3–6 CPU *months* for the same cases.
  The ingredients: interval branch and bound; an “active areas” polygon-representation
  elimination step; and tiling the unit square into a 6×8 grid, processed in three
  phases, cutting a ~`10¹²` combination space to something tractable.
  Final enclosures are accurate to 13–15 digits.

The lesson transfers directly.
A rigorous proof for a square-packing case would need the same three ingredients —
tiling for symmetry, a strong local elimination test, and staged phases — plus a fourth
that has no circle analogue: handling the angle variables, which is the part that costs
Montanher et al. their factor of hundreds.

#### Proof assistants

Nothing in the square-packing literature has been formalised in a proof assistant, and
no project to do so was found.
The relevant precedents, in increasing order of ambition:

- **Flyspeck** — Hales’s formal proof of the Kepler conjecture in HOL Light and
  Isabelle, completed 2014, published 2017. The template for formalising a packing proof
  whose informal version already depends on large computations.
- **Sphere packing in dimensions 8 and 24 in Lean 4** — the formalisation of Viazovska’s
  proof, led by Birkbeck, Hariharan, Mehta, and Lee.
  A sorry-free dimension-8 proof was announced 23 February 2026; the autoformalisation
  agent *Gauss* (Math, Inc.)
  closed the remaining goals, taking the codebase from ~20,000 to ~60,000 lines in five
  days, with dimension 24 optimality and periodic uniqueness following in about two
  weeks. This is the strongest evidence that formalising a hard packing result is now
  feasible on a months-not-decades timescale.
- **Verified interval arithmetic inside proof assistants** — `Coq.Interval`, Isabelle’s
  `approximation` method, PVS NASALib, Kodiak.
  These are what a formal version of the Montanher-style proof would run on.

The gap for square packing is not the proof assistant.
For *lower* bounds the missing informal computer-assisted proof now has a first
in-repository instance—exp-017’s exact certificate—so the formalisation target exists,
though nothing has been formalised.
For *upper* bounds there is no gap at all: a packing is a finite algebraic witness, and
formalising `s(11) ≤ 3.877084…` is available today and unclaimed — see
[Lean for Square-Packing Proofs and Validation](research-2026-08-22-lean-for-packing-proofs-and-validation.md).

### Who holds the records, and with what

Erich Friedman’s dynamic survey DS7 (last revised 2009) covers `n ≤ 100` and remains the
citable reference for the method and the lower bounds.
The live record table is David Ellsworth’s continuation of Friedman’s Packing Center,
covering **all `n ≤ 324`** plus special larger cases (`626`, `1453`, `1765`, `1850`,
`2043`), with SVG layouts, minimal polynomials, and rigidity flags.
For `n ≤ 324` not pictured, the trivial grid packing is the best known.

Attribution counts across the 184 pictured entries, by the verb the page uses.
One entry often carries several credits, so rows do not sum to 184.

| contributor | “Found by” | “Improved by” | “Proved by” |
| --- | --- | --- | --- |
| David Ellsworth | 46 | 39 | — |
| Thomas Schadt | 9 | 2 | — |
| Frits Göbel | 7 | — | 3 |
| M.Z. Arslanov et al. | 7 | — | — |
| Károly Hajba | 6 | — | — |
| David W. Cantrell | 5 | 16 | — |
| Evert Stenlund | 4 | — | — |
| Erich Friedman | 3 | — | 6 |
| Hiroshi Nagamochi | — | — | 21 |
| Wolfram Bentz | — | — | 4 |
| Kearney and Shiu, Stromquist, Trump, Bidwell, Morandi, DeVincentis, Hämäläinen | 1–2 each |  |  |

The shape of the table is the story: one person, David Ellsworth, is credited with
finding or improving a majority of the pictured records, running a program written by
another individual, Thomas Schadt.

Method mix: **47** entries credit simulated annealing (all for `n` between 28 and 307),
**7** credit an unnamed “computer program he/they wrote”, and the rest are pattern
constructions, extensions of smaller records, or hand analysis.
**32** entries are flagged “Not yet analytically optimized” — all with `n ≥ 103`, in
clusters near 103–110, 131–132, 154–156, 179–182, 206–210, 238–241, 270–273, and 297–307
— meaning the record is a refined numerical configuration with no exact algebraic form
yet.

The state of proofs, stated completely (which the commonly cited summaries are not):
`s(n)` is proved for

- all perfect squares `n = k²`;
- `n = k² − 1` and `n = k² − 2` for every `k ≥ 2` (Nagamochi 2005) — an *infinite*
  family, which subsumes 2, 3, 7, 8, 14, 15, 23, 24, 34, 35, 47, 48, 62, 63, …, 322,
  323;
- `n = k² − 3` for `k = 3, 4, 5, 6, 7` only: 6 (Kearney–Shiu 2002), 13 and 46 (Bentz
  2010), 22 and 33 (Bentz, arXiv 2016);
- `n = 5` (Göbel 1979) and `n = 10` (Stromquist 2003).

`n = 11` is the smallest unresolved case.

## Key Insights

1. **Exactness is a property of the *representation*, not of the precision.** The reason
   a 30-digit float vector cannot certify a packing is not that 30 digits is too few —
   it is that the tight constraints are equalities, and no finite-precision
   representation can distinguish an exact zero from a tiny nonzero.
   Once the configuration is expressed in its number field, verification becomes easy
   and fast. All the difficulty migrates into recovering that field.

2. **Verification is cheap; certification of *optimality* is astronomically expensive.**
   Confirming that a proposed packing is valid took 0.35 s of unoptimised Python for
   `n = 11`. Proving that *no better packing exists* is the problem that has consumed 47
   years and, in its only rigorous computational form, manages three squares in a circle
   in ten minutes. These two questions are routinely conflated in popular accounts of
   this problem.

3. **The Jacobian-determinant constraint is the quietly important technique.** It
   converts “minimise `s` along a constraint manifold” into “solve a square root-finding
   problem,” which is what makes thousand-digit precision — and hence integer-relation
   recovery of degree-40 and degree-62 minimal polynomials — reachable at all.
   It is documented on a personal website, not in a journal.

4. **The general-purpose global optimization frontier stops around `n = 16`.** SCIP 10
   and FICO Xpress 9.8, with a Farkas-lemma non-overlap formulation and hours of CPU per
   instance, match the records up to `n ≈ 16` and then lose ground, badly at `n = 27`
   and `n = 29`. The same tools *beat* AlphaEvolve on adjacent problems, so this is a
   statement about squares-in-squares specifically: the landscape has too many
   near-degenerate local optima for spatial branch and bound to prune.

5. **The record engine is a GPU annealer with a statistics-driven workflow, and it is
   closed source.** The published basin statistics are the most informative artifact in
   the whole field — 4 record basins out of 3,004 for `s(51)` quantifies exactly how
   needle-like these optima are — and they exist only because one person chose to
   publish them.

6. **The source record data format remains a liability.** Exact algebraic descriptions
   exist for most packings but are embedded as Mathematica expressions in XML comments
   inside SVGs, with no schema, no coordinate list, and no machine-readable link between
   a packing and its minimal polynomial.
   This repository’s `Witness/v2` supplies a clean interchange and exact checker once a
   packing has been normalized, but importing much of the SVG corpus still requires
   case-specific source interpretation.

7. **Proof-assistant formalization remains open, but there are now concrete targets.**
   The proof assistants are ready (Flyspeck, and the Lean sphere-packing project
   finishing dimensions 8 and 24 in 2026), as is proof-producing interval arithmetic
   (`Coq.Interval`, Isabelle `approximation`). This repository now has exact algebraic
   upper-bound witnesses and exp-017’s exact lower-bound certificate.
   Neither has been encoded in a proof assistant.

## Comparison Matrix

Tooling by task, with the honest verdict for this specific problem.

| Task | Best open-source option | Best option overall | Gap |
| --- | --- | --- | --- |
| Approximate validity check | SAT written directly, or `jagua-rs` | same | none; microseconds per pair, and linear in `n` once bucketed |
| Exact validity check | this repository’s `Witness/v2` checker for rational and supported real-algebraic witnesses | CGAL exact kernels + `msolve`/FLINT for broader systems | automatic corpus import and general interval-to-existence certification remain open |
| Record search | none | Schadt/Ellsworth GPU annealer (closed) | **no open equivalent** |
| General search | SCIP 10 + Farkas non-overlap | FICO Xpress, Gurobi | competitive only to `n ≈ 16` |
| Nesting-style search | `jagua-rs` + `sparrow`, `packingsolver` | same | wrong objective and tolerance regime |
| Symbolic refinement | SymPy + `msolve` (+ PARI `algdep`) | Mathematica (`FindRoot`, `RootApproximant`, `RootReduce`) | SymPy is far slower at high-degree `RootApproximant`-style recovery |
| Rigorous optimality proof | `filib++`/C-XSC/Ibex branch and bound | same | scales to 3 squares (in a circle) |
| Formal proof | Lean 4 + mathlib, Coq + `Coq.Interval`, Isabelle | same | no *lower-bound* proof to formalise yet; the **upper bound is formalisable today** — see [the Lean study](research-2026-08-22-lean-for-packing-proofs-and-validation.md) |

## Recommendations

**These are superseded in build order, not in content, by**
[Infrastructure for Square-Packing Exploration](research-2026-08-22-infrastructure-for-packing-exploration.md),
which turns them into a layered design with measured performance budgets and decides the
language boundary. Read that document for *what to build first*; read this section for
*why each piece matters*.

For anyone wanting to work on this computationally, in rough order of value per unit of
effort:

1. **Complete the exact corpus pipeline.** Normalize the remaining SVG layouts into
   `Witness/v2` with their algebraic definitions and minimal polynomials, then extend
   the checker with a filtered kernel and interval-existence certificates where direct
   exact reconstruction is unavailable.
   The current repository covers rational and supported single-generator real-algebraic
   witnesses; source import and promotion at the exact reported values remain the
   missing halves.
2. **Build an open GPU annealer on `jagua-rs`.** The collision-detection engineering —
   the part that is genuinely hard to get both fast and correct — is already solved
   there, under MPL-2.0, with continuous rotation support.
3. **Attempt a rigorous computer-assisted proof of a small unsolved case.** Not `s(11)`:
   its optimum is an irrational of degree 8, and every technique in the rigorous
   literature certifies thresholds built from unit distances and container coordinates.
   A case with an *integer* optimum and few tilted squares is the realistic target,
   following the Montanher tiling-plus-sentinels design.
4. **Automate the verification of unavoidable point sets.** Checking “every unit square
   in `[0,k]²` contains a point of `P`” is a three-parameter decision problem well
   within reach of interval branch and bound or `nlsat`. It would let the existing human
   proofs be machine-checked, and would let candidate point sets be searched for rather
   than constructed by hand — the plausible route to a new lower bound.

## Open Questions

- [ ] Is Thomas Schadt’s annealing program described anywhere in writing — cooling
  schedule, move set, acceptance rule, how the GPU threads are used?
  Everything known about it here is inferred from the record-page annotations and the
  two published `.stats.txt` files.
- [ ] What refinement step converts an annealed basin into the local optimum, and how
  does it reach the precision `RootApproximant[]` needs?
  The record pages distinguish “found”, “refined”, and “analytically optimized” but do
  not describe the middle step.
- [ ] Does the Berthold et al.
  supplement contain `ℓ = m = 4` results beyond `n = 30`, and were any
  squares-in-squares records approached with a longer time limit?
- [ ] Has anyone run `msolve`, `HomotopyContinuation.jl` `certify`, or `alphaCertified`
  on a square-packing contact system?
  The degree-40 and degree-62 cases would be a good benchmark for those tools and none
  appears in their published examples.
- [ ] Could the Farkas-lemma non-overlap formulation be combined with the Montanher
  sentinel formulation inside a rigorous interval solver, rather than a floating-point
  spatial branch-and-bound one?
- [ ] Wikipedia’s list of proved cases
  (`n = 2, 3, 5, 6, 7, 8, 10, 13, 14, 15, 24, 34, 35, 46, 47, 48` plus perfect squares)
  omits 22, 23, and 33 and truncates Nagamochi’s infinite `k² − 1`, `k² − 2` family.
  Worth correcting upstream.

## Methodology

Research was conducted on 2026-08-22 by web search, direct retrieval of primary sources,
and original computation.
Every numeric claim attributed to a measurement below was run in this session.

**Sources read in full rather than through summaries.** Friedman’s DS7 survey (HTML,
converted to text locally) for the lower-bound method and the record history; the
*Squares in Squares* record page and its companion pages on analytic minimization and
rigid packings; the SVG source of the `n = 11` packing, including its Mathematica
comment block; Gensane’s spheres-in-a-cube paper (PDF, text extracted with `pypdf`) for
the perturbed billiard algorithm, which is the published description of the method used
for squares; Arslanov et al.
(2021); the arXiv HTML full texts of the Berthold et al.
global optimization paper and the Heilbronn optimize-then-refine paper.

**Original computation: exact verification of Trump’s `n = 11` packing.**

1. Reconstructed the configuration from the record SVG: six axis-aligned unit squares
   and a five-square block rotated by `a`, with the offsets `x0, r1, u1, v1, v2` given
   there as closed forms.
2. Derived the number field independently.
   With `u = tan(a/2)`, the tilted-block contact gives `s = (6u + 4)/(−u² + 2u + 1)`.
   Substituting into the published degree-8 minimal polynomial of `s` and clearing
   denominators gives a degree-16 polynomial in `u` which factors over `Q` into two
   irreducible degree-8 factors; the one with a root in `(0.36, 0.37)` is
   `5u⁸ − 10u⁷ − 2u⁶ + 14u⁵ + 12u⁴ − 6u³ + 2u² + 2u − 1`. Confirmed with SymPy that the
   degree-8 polynomial for `s` is irreducible over `Q` and has exactly two real roots,
   `−1.8530324789725079` and `3.8770835900228142`.
3. Implemented exact arithmetic in `Q(u)` from scratch (`fractions.Fraction`, reduction
   modulo the minimal polynomial, inversion by exact Gaussian elimination), with
   equality by zero-representative test and sign by rational interval Horner evaluation
   with bisection refinement.
   No floating point in the decision path.
4. Verified: all 11 pieces are exactly unit squares with exact right angles; all 44
   corners satisfy `0 ≤ x ≤ s` and `0 ≤ y ≤ s`, with 20 coordinates exactly on the
   boundary; all 55 pairs are interior-disjoint by SAT, 14 of them with exactly zero
   gap; and `P(s) = 0` exactly for the published polynomial.
   Wall time 0.34 s.
5. Recovered `s = 3.87708359002281417730789706010096270637645…`, whose first 33 digits
   match the value published in the SVG.

**Negative controls.** The verifier was re-run on configurations perturbed by sliding
one square into its neighbour by `δ ∈ {10⁻⁶, 10⁻¹², 10⁻¹⁵, 10⁻¹⁸, 10⁻³⁰, 10⁻¹⁰⁰}`. The
exact verifier rejected every one, identifying the offending pair.
A float64 SAT verifier was run on the same inputs at tolerances `10⁻⁹`, `10⁻¹²`, and
`0`, producing the table in
[Why floating point cannot certify a tight packing](#why-floating-point-cannot-certify-a-tight-packing).
Without a negative control the exact verifier’s “OK” would carry no information; this is
the check that shows it discriminates.

**Benchmarks.** The float64 SAT sweep was timed on grid packings at
`n = 11, 100, 324, 1000`, with and without grid bucketing, using the same verifier with
its float backend.
Exact field-multiplication cost was measured at degrees 8, 18, 40, and
62 — the degrees that actually occur in the record table — with fixed operands to
isolate the reduction cost from rational-coefficient growth.
All timings are from this container and are indicative of relative cost, not of what
tuned C would achieve.

**Reproducibility.** The verifier, the reference packing, the field derivation, the
negative controls, and the benchmarks are packaged in
[`explorations/packing/`](../../../README.md); `packing-validate` there reruns the full
validation surface and asserts the results quoted above.
The verifier is standard library only; only the derivation script needs SymPy.

**Record-page statistics** (184 pictured packings, 47 mentioning simulated annealing, 32
flagged “Not yet analytically optimized”, attribution counts) were extracted by parsing
the record page programmatically rather than by reading, so they are counts of
annotation text and may under-count entries phrased differently.

**Comparison of global-optimization results to records.** The `ℓ = m = 4` rows of the
Berthold et al. solution database were fetched and compared against the record values
parsed from the record page.
Their objective is the outer circumradius for inner polygons of unit circumradius, which
for `m = ℓ = 4` equals `s(n)` exactly; this was confirmed against the known values at
`n = 5, 10, 11` before drawing conclusions from the other rows.

**Not established.** No description of Schadt’s annealer beyond the record-page
annotations was found.
The Gensane–Ryckelynck squares paper itself is paywalled and was read only through its
abstract, Friedman’s description, and Ellsworth’s commentary; the algorithmic detail
above comes from Gensane’s open-access companion paper on spheres, which describes the
same perturbed billiard method.
Springer, ResearchGate, and Academia.edu returned 403 or authentication redirects to
automated fetches throughout.

**Link audit.** All 26 cited URLs were checked with `curl` on 2026-08-22. Eighteen
returned HTTP 200. Eight return 403 to an automated checker but are valid in a browser
and were read successfully during this research through other means: the six github.com
links, the CGAL documentation page (re-confirmed by a separate fetch), and the SIAM
article page.

**Confidence.** High for the exact verification and benchmarks (run here, with negative
controls); high for the record-page facts and the Berthold et al., Montanher et al.,
Markót, and Heilbronn results (primary sources read directly); medium for the
attribution counts (parsed by regular expression over the page text, not audited entry
by entry — names are line-broken in the source HTML, which an earlier naive count got
wrong) and for the Gensane–Ryckelynck algorithmic details (inferred from the companion
paper).

## References

Records, data, and surveys:

- [David Ellsworth, “Squares in Squares”](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
  — the live record table, `n ≤ 324`, with SVG layouts, minimal polynomials, and
  rigidity flags. Continuation of Erich Friedman’s Packing Center.
- [David Ellsworth, “Squares in Squares: Analytic Minimization of Underdetermined Nonlinear Systems”](https://kingbird.myphotos.cc/packing/squares_in_squares__analytic_minimization.html)
  — the Jacobian-determinant technique.
- [David Ellsworth, “Squares in Squares: Rigid packings”](https://kingbird.myphotos.cc/packing/squares_in_squares__rigid.html)
- [Erich Friedman, “Packing Unit Squares in Squares: A Survey and New Results”, *Electron. J. Combin.*, Dynamic Survey DS7](https://erich-friedman.github.io/papers/squares/squares.html)
  — the unavoidable-point method and the `n ≤ 100` tables.
- [Wikipedia, “Square packing”](https://en.wikipedia.org/wiki/Square_packing) — note the
  incomplete list of proved cases, discussed above.

Search algorithms:

- [T. Gensane and P. Ryckelynck, “Improved Dense Packings of Congruent Squares in a Square”, *Discrete Comput. Geom.* 34 (2005) 97–109](https://link.springer.com/article/10.1007/s00454-004-1129-z)
  — the inflation algorithm; paywalled, not read in full.
- [T. Gensane, “Dense Packings of Equal Spheres in a Cube”, *Electron. J. Combin.* 11 (2004), #R33](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v11i1r33/pdf)
  — open-access companion describing the perturbed billiard algorithm in full.
- [T. Berthold, D. Kamp, G. Mexi, S. Pokutta, I. Pólik, “Out-of-the-Box Global Optimization for Packing Problems”, arXiv:2605.04850](https://arxiv.org/abs/2605.04850)
  — Farkas-lemma non-overlap, SCIP 10 and FICO Xpress 9.8.
- [Same authors, “Global Optimization for Combinatorial Geometry Problems Revisited in the Era of LLMs”, arXiv:2601.05943](https://arxiv.org/abs/2601.05943)
  — comparison against AlphaEvolve.
- [Solution database for the above](https://github.com/DominikKamp/Packing) — includes
  the `ℓ = m = 4` results used in the comparison table.
- [M.Z. Arslanov, S.A. Mustafin, Z.K. Shangitbayev, “Improved packings of n(n−1) unit squares in a square”, *Electron. J. Combin.* 28(4) (2021) #P4.22](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v28i4p22/pdf/)
- Y. Stoyan, T. Romanova, A. Pankratov et al., quasi-phi-functions for packing with
  continuous rotations — e.g.
  [“Quasi-phi-functions and optimal packing of ellipses”, *J. Global Optim.* 65 (2016)](https://link.springer.com/article/10.1007/s10898-015-0331-2).

Exact verification and computer-assisted proof:

- [T. Montanher, A. Neumaier, M.C. Markót, F. Domes, H. Schichl, “Rigorous packing of unit squares into a circle”, *J. Global Optim.* 73 (2019) 547–565](https://pmc.ncbi.nlm.nih.gov/articles/PMC6394747/)
  — the only rigorous computer-assisted proof for rotatable unit squares; `n = 3`.
- [M.C. Markót, “Improved interval methods for solving circle packing problems in the unit square”, *J. Global Optim.* 81 (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8550790/)
  — `n = 31, 32, 33` in 26, 61, 13 CPU hours with C-XSC.
- [M.C. Markót and T. Csendes, “A New Verified Optimization Technique for the Packing Circles in a Unit Square Problems”, *SIAM J. Optim.* 16 (2005)](https://epubs.siam.org/doi/10.1137/S1052623403425617)
  — `n = 28, 29, 30`.
- [Heilbronn’s Triangle Problem on the Unit Square Using Mixed-Integer Optimization, arXiv:2603.11107](https://arxiv.org/abs/2603.11107)
  — the optimize-then-refine pipeline, and the discipline of verifying symbolically by
  substitution.
- [P. Breiding, K. Rose, S. Timme, “Certifying zeros of polynomial systems using interval arithmetic”, *ACM TOMS* 49 (2023); arXiv:2011.05000](https://arxiv.org/abs/2011.05000)
  — the `certify` function in HomotopyContinuation.jl.
- [CGAL, `Exact_predicates_exact_constructions_kernel_with_sqrt`](https://doc.cgal.org/latest/Kernel_23/classCGAL_1_1Exact__predicates__exact__constructions__kernel__with__sqrt.html)
  — the filtered-exact kernel design.

Formalisation precedents:

- [Formalising Sphere Packing in Lean](https://thefundamentaltheor3m.github.io/Sphere-Packing-Lean/)
  and [the repository](https://github.com/math-inc/Sphere-Packing-Lean) — dimensions 8
  and 24, sorry-free as of February 2026.
- [Progress in Formalizing Sphere Packing in Dimension 8, arXiv:2604.23468](https://arxiv.org/abs/2604.23468)

Open-source packing and nesting tooling:

- [`jagua-rs`](https://github.com/JeroenGar/jagua-rs) — collision detection engine,
  MPL-2.0, continuous rotation;
  [paper, arXiv:2508.08341](https://arxiv.org/abs/2508.08341), *INFORMS J. Computing*.
- [`sparrow`](https://github.com/JeroenGar/sparrow) — nesting optimizer on top of
  `jagua-rs`.
- [`packingsolver`](https://github.com/fontanf/packingsolver) — C++/MIT, tree search and
  column generation, irregular solver supports continuous rotation.
- [`leove4/Square-packing-simulation`](https://github.com/leove4/Square-packing-simulation)
  — MIT, Python, an interactive simulation; illustrative rather than record-capable, and
  representative of what exists on GitHub for this specific problem.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
