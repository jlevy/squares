# Research: Packing 11 Unit Squares in a Square

**Date:** 2026-08-22 (last updated 2026-08-22, expanded with strategy catalogues)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

## Overview

This document records everything that could be established about the problem of packing
11 unit squares into the smallest possible enclosing square.
It is written to support *full technical understanding* of the problem and its
literature, not to introduce the topic pedagogically.
Claims are separated by evidential status: proved, computationally verified, best known,
or asserted-but-unverified.

The motivating observation is that `n = 11` is the smallest case of a natural,
easily-stated geometry problem that remains **unsolved** after nearly fifty years.
The best known packing dates from 1979 and has never been improved; the best proved lower
bound dates from 2003 and has never been improved.
A gap of roughly 0.088 in the side length separates them.
Understanding precisely *where* that gap comes from — and why the available proof
technique cannot close it — is the substance of this document.

The document also catalogues, at length, the two inventories that define the field's
reach: the **search strategies** that have produced every known packing, and the **proof
strategies** that have produced every known bound.
The asymmetry between them is the clearest available explanation of why the problem is
stuck.
A dedicated section assesses whether the Kirchhoff/Tutte electrical-network method famous
from the squared-square literature can be brought to bear here; the conclusion is that it
provably cannot, though the instinct behind it does survive in another form.

A secondary purpose is corrective.
Widely circulated summaries of this problem, including the briefing that prompted this
research, state that Stromquist's 2003 paper *proved* Walter Trump's 11-square packing
optimal.
That is false, and the error is consequential enough to be worth stating precisely.
See [Corrections to Common Summaries](#corrections-to-common-summaries).

## Questions to Answer

1. What exactly is the state of knowledge for `s(11)` — what is proved, and what is only
   conjectured?
2. What is Trump's packing, and what is its exact algebraic characterization?
3. What did Stromquist actually prove in 2003, and what was Gardner's conjecture?
4. What proof technique establishes lower bounds, and why has it stalled at `n = 11`?
5. Which cases *are* solved, by whom, and by what methods?
6. What computational work has attacked this, and what did it find?
7. How does the asymptotic theory of square packing relate to small cases like `n = 11`?
8. What would a resolution of `n = 11` plausibly require?
9. What is the full inventory of *search* strategies used to find packings, and which
   have actually produced records?
10. What is the full inventory of *proof* strategies used for bounds over the last
    century, and which remain untried here?
11. Does the Kirchhoff/Tutte electrical-network method for squared squares transfer to
    this problem?

## Scope

**Included:** packing `n` *unit* (equal, congruent) squares into a smallest enclosing
square, with unrestricted rotation; the exact case `n = 11`; the proof machinery for
lower bounds; the historical record; computational searches; the asymptotic
wasted-space literature insofar as it bears on the problem's structure.

**Included by contrast:** the squared-square dissection tradition (Dehn, Moroń, Sprague,
the Trinity Four, Duijvestijn), covered specifically to establish whether its machinery
transfers. See [The squared-square tradition](#the-squared-square-tradition-kirchhoff-tutte-and-why-the-method-does-not-transfer).

**Excluded:** packing *unequal* or consecutively-sized squares as a research goal in its own right (a distinct problem —
see [Adjacent Problems](#adjacent-problems-deliberately-out-of-scope)); packing squares
into circles, triangles, or rectangles except where cited for contrast; circle packing;
online/streaming packing algorithms; bin-packing complexity theory.

## Findings

### Notation and trivial bounds

Following the standard convention established in Friedman's survey and used throughout
the literature:

> `s(n)` is the side of the smallest square into which `n` unit squares can be packed.

Packings permit arbitrary rotation and translation, and require only non-overlapping
interiors.
Two elementary bounds hold for all `n`:

- **Area (lower):** `s(n) ≥ √n`, since `n` unit squares have total area `n`.
- **Grid (upper):** `s(n) ≤ ⌈√n⌉`, by the axis-aligned grid packing.

For `n = 11` these give `3.31662… ≤ s(11) ≤ 4`.
Both are far from tight.
The entire difficulty of the problem lies between them.

### The state of knowledge for n = 11

| Quantity | Value | Status | Source |
| --- | --- | --- | --- |
| Area lower bound | `√11 ≈ 3.316625` | Trivial | — |
| **Best proved lower bound** | `2 + 2√(4/5) = 2 + 4/√5 ≈ 3.788854` | **Proved** | Stromquist 2003, Thm 2 |
| **Best known packing (upper bound)** | `≈ 3.877084` | **Construction only** | Trump 1979 |
| Lower bound for 0°/45°-only packings | `2 + (4/3)√2 ≈ 3.885618` | **Proved** | Stromquist 2003, Thm 3 |
| Grid upper bound | `4` | Trivial | — |

The open interval is `[3.788854…, 3.877084…]`, of width `≈ 0.088230`.

Two facts about this table are worth stating explicitly because they are frequently
garbled:

1. **`s(11)` is not known.** It is the smallest `n` for which `s(n)` is undetermined.
2. **The 0°/45° bound (3.8856) exceeds the best known packing (3.8771).** This is not a
   contradiction — it is the entire point of Theorem 3, and the mechanism by which
   Gardner's conjecture was settled. See below.

### Trump's packing (1979): structure and exact characterization

The best known packing of 11 unit squares was found by **Walter Trump** in 1979, a German
physics teacher and recreational mathematician.
It improved an earlier packing of Göbel's.
Friedman's survey notes that "many people have independently discovered this packing,"
so priority is shared in practice even though 1979/Trump is the standard attribution.

**Geometry.** The configuration places most squares axis-aligned, with a group of middle
squares tilted at approximately **40.182°** — an angle that is neither 0° nor 45°, and
which has no simple closed form.
Friedman's survey describes it as: "The middle squares are tilted about 40.182°, and
there is a small gap between these squares."
The reported high-precision value of the tilt is

```
40.18193729032971646523034236806062154252265849634355838751445324…°
```

Trump reportedly computed this in 1979 on a Hewlett-Packard HP-67 programmable RPN
pocket calculator and sent the result to Martin Gardner.

**Exact side length.** The container side length is the algebraic number

```
s = 3.877083590022814…
```

which is a root of the degree-8 polynomial

```
s⁸ − 20s⁷ + 178s⁶ − 842s⁵ + 1923s⁴ − 496s³ − 6754s² + 12420s − 6865 = 0
```

*Independently verified during this research* (see [Methodology](#methodology)):

- The polynomial is **irreducible over ℚ**. The conjectured `s(11)` is therefore an
  algebraic number of degree exactly 8.
- It has exactly **two real roots**: `≈ −1.853032478972508` and
  `≈ 3.877083590022814`. The second is the packing value.
- Substituting the published 15-digit value gives `P(s) ≈ −6.4 × 10⁻¹³`, consistent with
  it being the root to available precision.

**Rigidity.** Both Friedman's survey and the Kingbird catalogue mark this packing as
**rigid**: the squares admit no continuous deformation, and the configuration is pinned
by vertices of unit squares lying on edges of other unit squares or of the container.
Rigidity is what makes the exact algebraic value computable at all — the contact
conditions form a determined polynomial system — and it is evidence of local optimality.
It is *not* evidence of global optimality, and this distinction is the crux of the open
problem.

### What Stromquist actually proved (2003)

Walter Stromquist, "Packing 10 or 11 Unit Squares in a Square," *The Electronic Journal
of Combinatorics* **10** (2003), #R8.
Submitted 26 Nov 2002; accepted 26 Feb 2003; published 18 Mar 2003.
MR subject classifications 05B40, 52C15.

The paper contains **three** theorems, and conflating them is the source of most public
confusion.

**Theorem 1.** Ten pairwise non-intersecting boxes cannot exist in the interior of a
square of side `s = 3 + √(1/2)`.
Consequently

```
s(10) = 3 + ½√2 ≈ 3.707107
```

This *is* an exact determination — `n = 10` is solved.

**Theorem 2.** Let `s = 2 + 2√(4/5) ≈ 3.789`.
Then eleven non-intersecting boxes cannot exist inside a square of side `s`.
Consequently

```
s(11) ≥ 2 + 2√(4/5) = 2 + 4/√5 ≈ 3.788854
```

This is a **lower bound only**.
It does not match Trump's `≈ 3.877084`, and Stromquist makes no claim that it does.

**Theorem 3.** Let `s = 2 + (4/3)√2 ≈ 3.886`.
Then eleven non-intersecting boxes cannot exist inside a square of side `s` *if each box
has orientation 0° or 45° with respect to the container*.
So any **45° packing** of 11 squares needs side at least `2 + (4/3)√2 ≈ 3.885618`.
The abstract writes this constant equivalently as `2 + 2√(8/9)`; the two agree, since
`2√(8/9) = 4√2/3`.
This bound is realized — hence tight — by a packing due to **Pertti Hämäläinen**
(correspondence, 20 April 1980).

#### The Gardner conjecture argument

Martin Gardner conjectured (*Scientific American*, "Mathematical Games," October 1979,
with follow-ups in November 1979, March 1980, and November 1980) that `n = 11` is the
first case in which an optimal packing *requires* orientations other than 0° and 45°.

The proof is a two-line comparison, and it is elegant precisely because it sidesteps
determining `s(11)`:

- By Theorem 3, **any** packing restricted to 0°/45° needs side `≥ 3.885618`.
- Trump's packing achieves side `≈ 3.877084 < 3.885618`, using a `≈ 40.182°` tilt.
- Therefore no 0°/45° packing can be optimal: a non-45° packing strictly beats every
  45° packing.

Stromquist's closing line: this "establishes the truth of Martin Gardner's conjecture."

**The logical shape matters.** The conjecture is about the *necessity of oblique
orientations*, not about the *value* of `s(11)`.
It is settled by bracketing a restricted class from below and exhibiting an unrestricted
construction that beats it.
`s(11)` itself is untouched by the argument and remains open.

For contrast, the two smaller cases with tilted squares — `n = 5` and `n = 10` — both use
45° tilts, which is why 11 is the first case where genuinely oblique angles are forced.

### The lower-bound method: boxes, nonavoidance lemmas, unavoidable points

Stromquist's technique, inherited from his own 1984 memoranda and from Friedman's
survey, is the standard machinery for square-packing lower bounds.

**The box device.** A **box** is defined as the interior of any square of side *strictly
greater than 1*.
To establish `s(n) ≥ a`, one proves the equivalent statement that `n` non-overlapping
boxes cannot be packed inside a square of side exactly `a`.
As Stromquist puts it, "we treat boxes as if they were unit squares, and rely on the
extra margin of size to convert equations into inequalities as needed."
This converts a closed-condition problem into an open-condition one and removes
degenerate boundary cases.

**Unavoidable point sets.** The core idea:

> Find a set `P` of points inside the container `S` such that **every** box placed inside
> `S` must contain at least one point of `P`.
> Such a `P` is called *unavoidable*.
> If `|P| = n − 1`, then `n` non-overlapping boxes are impossible: by pigeonhole two
> boxes would have to contain the same point, contradicting non-overlap.

For Theorem 2, Stromquist exhibits **ten** unavoidable points in a square of side
`2 + 2√(4/5)`, which rules out eleven boxes.
Four of the points sit at coordinates including `(1, 1)` and points at `s/2`; the rest are
placed symmetrically.
The vertical distance between the rows of points is `√(4/5) ≈ 0.894`, and the triangles
in the construction are congruent with sloping sides of length exactly 1.

**Nonavoidance lemmas.** Proving that a candidate set is genuinely unavoidable requires
geometric lemmas of the form "if the *center* of a box lies in region `R`, the box must
intersect a specified part of `∂R`."
Stromquist presents six such lemmas (Lemmas 1–6), of which Lemmas 1–3 are taken from
Friedman's survey, plus two further lemmas (7 and 8) specific to the 45° analysis.
Representative statements:

- **Lemma 1.** For `a ≤ 1` and `b ≤ 1`, any box whose center is in the rectangle
  `[0,a] × [0,b]` must intersect the x-axis, the y-axis, or the point `(a,b)`.
- **Lemma 2.** If `T` is a triangle with all sides of length at most 1, any box whose
  center is in the interior of `T` must contain one of the vertices of `T`.
- **Lemma 5.** A specialized statement about the pentagon with vertices `(1,0)`, `(1,1)`,
  `(2,1)`, `(2.12,0.9)`, `(2.12,0)`, needed for the `n = 10` argument.

The 45°-restricted case (Theorem 3) uses a **twelve**-point unavoidable set, exploiting
the fact that the projections of a 45° unit vector are at most 1, which brings the
triangle lemmas into play in a stronger form.

**Why this method has a ceiling.** The unavoidable points are placed at coordinates built
from the container side `s` and from unit distances — that is, from rational functions of
`s` and square roots.
The bound one can prove is therefore naturally an algebraic number of low degree.
Both proved constants in this paper — `3 + ½√2` and `2 + 4/√5` — are degree-2 algebraic
numbers.
The conjectured `s(11)` is degree **8** (verified above).
There is no evident way for a finite unavoidable-point configuration with low-degree
coordinates to certify a degree-8 threshold.
This is, in our assessment, the structural reason the method stalls well short of
`3.877084`, and it is the single most useful insight in this document.

### The landscape of solved cases

Exact values of `s(n)` known as of this research:

| `n` | `s(n)` | Attribution |
| --- | --- | --- |
| perfect squares `m²` | `m` | Trivial |
| 1 | 1 | Trivial |
| 2, 3, 4 | 2 | Classical |
| **5** | `2 + ½√2 ≈ 2.707107` | Göbel |
| 6, 7, 8, 9 | 3 | first published proof of `s(6)=3` by Kearney & Shiu (2002), who also treat `s(7)` |
| **10** | `3 + ½√2 ≈ 3.707107` | Stromquist 2003 |
| **11** | **OPEN** — in `[3.788854, 3.877084]` | — |
| 13 | 4 | Bentz 2010 |
| 22 | 5 | Bentz 2016 |
| 33 | 6 | Bentz 2016 |
| 46 | 7 | Bentz 2010 |

General families:

- **Nagamochi:** `s(m² − 1) = s(m² − 2) = m` for `m ≥ 2`.
- **`s(m² − 3) = m`** established for `m = 3, 4, 7`, extended by Bentz to `m = 5, 6`
  (via `s(22) = 5` and `s(33) = 6`), supporting the conjecture that it holds for all
  `m ≥ 3`.

Friedman's survey supplies relatively simple proofs for `n = 2, 3, 5, 8, 15, 24, 35` and
more complicated ones for `n = 7, 14`.
Stromquist's 2003 abstract notes that at that time, for larger `n`, published proofs of
exact values existed "only for `n = 14, 15, 24, 35`, and when `n` is a square."

**A structural observation.** Every solved non-trivial case has `s(n)` equal to either an
integer or a degree-2 algebraic number of the form `k + ½√2`.
No case with a higher-degree answer has ever been resolved.
`n = 11` would be the first, and this is likely not a coincidence but a reflection of the
proof technology's reach.

*Note on source discrepancies:* enumerations differ between sources.
Wikipedia lists `n = 2, 3, 5, 6, 7, 8, 10, 13, 14, 15, 24, 34, 35, 46, 47, 48`, omitting
`n = 23`, which Nagamochi's family supplies from `m = 5`.
Other enumerations do include it: `2, 3, 5, 6, 7, 8, 10, 13, 14, 15, 22, 23, 24, 33, 34,
35`.
The union across sources, plus Nagamochi's family stated in general form, is the safe
reading; `n = 23` **is** covered by the theorem, and Wikipedia's omission appears to be
an incomplete enumeration rather than a mathematical subtlety.

### Catalogue of search strategies for finding packings (upper bounds)

Every entry in the record tables is a **construction**.
No upper bound in this subject has ever been obtained non-constructively: to show
`s(n) ≤ a` somebody must exhibit a packing.
The strategies below are ordered roughly from human to machine, and the table records
which are known to have produced records.

| # | Strategy | Mechanism | Produced records? |
| --- | --- | --- | --- |
| 1 | Axis-aligned grid | The `⌈√n⌉` trivial packing | Yes — optimal for perfect squares and `m²−1`, `m²−2`, `m²−3` |
| 2 | Hand geometric insight | Human construction, often on paper | Yes — Trump `n=11`, Göbel, Hämäläinen, Bidwell `n=17` |
| 3 | 45° tilted families | A block of squares rotated a half-turn diagonal | Yes — `n=5`, `n=10` |
| 4 | Diagonal strips of width `k` | A tilted band crossing the container, corners filled | Yes — Stenlund `n=66` (width-3 strip) |
| 5 | Strip + "L" augmentation | Extend a strip packing with an L-shaped border block | Yes — best known `n=83` from the `n=66` strip |
| 6 | Rational-slope tilts | Tilts at `arctan(p/q)` making contacts commensurate | Yes — e.g. `arctan(8/15)`, `arcsin((√7−1)/4)` for `n=18` |
| 7 | Composition / self-similarity | Combine copies of a smaller good packing | Yes — Ellsworth Dec 2025 joined two `s(50)` copies for `s = 13 + 4/7` |
| 8 | Parametric families for structured `n` | Formulas for `n = m²−k`, `n = m²−m`, `n(n−1)` | Yes — Arslanov et al. on `n(n−1)` |
| 9 | Asymptotic border constructions | Tilt squares near the boundary to absorb fractional waste | Yes — Erdős–Graham and successors, asymptotic only |
| 10 | Simulated annealing | Stochastic perturbation with a cooling schedule | **Yes — the current workhorse.** Schadt's program; Ellsworth's modified version |
| 11 | Billiard / inflation | Grow squares to a jammed state, perturb, repeat | Yes — Gensane–Ryckelynck (`n = 29, 37`; alternative `n = 18`) |
| 12 | Basin hopping / multistart | Many random starts into local optimisation | Standard in packing generally |
| 13 | Nonlinear programming | Continuous variables with pairwise non-overlap constraints | Standard; scales poorly with `n` |
| 14 | SAT / constraint programming | Reduce feasibility at a fixed side to a Boolean or CP instance | Used for 2D orthogonal packing; awkward under free rotation |
| 15 | Branch and bound over contact classes | Enumerate combinatorial structures, optimise within each | Used in exact cutting-and-packing |
| 16 | Genetic / evolutionary search | Population methods over configurations | Used in the wider packing literature |
| 17 | Exact algebraic refinement | Fix the contact graph, solve the polynomial system | **How exact values are obtained** — see below |
| 18 | Rigidity-guided enumeration | Enumerate rigid contact graphs, then solve each | Standard in sphere/disk packing; the natural analogue here |
| 19 | Interval-verified local optima | Certify a local optimum with interval arithmetic | Used for circle packing; not seen applied to `s(11)` |
| 20 | Catalogue-driven record chasing | Human-computer loop against a public record table | Yes — how the tables actually advance |

**On strategy 17, exact algebraic refinement.**
This is the step that turns a numerical packing into a theorem-shaped object, and it is
how the degree-8 polynomial for `n = 11` exists at all.
Once a numerical search has converged, the *combinatorial* structure is read off: which
square touches which, and along which edge.
Each contact becomes a polynomial equation in the positions and tilt angles.
If the configuration is **rigid**, the resulting system is zero-dimensional, and
eliminating variables (classically by resultants, in modern practice by a Gröbner basis)
yields a univariate polynomial whose relevant root is the exact side length.
For Trump's packing that eliminant is the irreducible degree-8 polynomial recorded above.
Note what this gives and does not give: an *exact* value for that contact class, and no
information whatsoever about other contact classes.

**On strategy 10, simulated annealing.**
The record tables are, in practice, maintained by annealing.
The activity is current and competitive: David Ellsworth found `s(131) =
11.95654869347733` in January 2026 using a modified version of Thomas Schadt's simulated
annealing program, starting from a packing Károly Hajba found in November 2024; `s(156)`
was improved by Arslanov, Mustafin and Shangitbayev (2019), then by Ellsworth (Dec 2024),
then Cantrell (Mar 2025), then Ellsworth again (Jan 2026).
Best-known packings are catalogued to `n = 324`.

**The significance for `n = 11`.** Strategies 10, 11, 12 and 13 have all been pointed at
this case, and none has beaten a configuration found by hand in 1979 and refined on a
pocket calculator.
That is about as strong as purely empirical evidence gets.
It is also, by construction, evidence that cannot become a proof: a search that fails to
find something better has certified nothing.

### Catalogue of proof strategies for bounds

Lower bounds are where the mathematics lives, and the inventory is strikingly short.
Almost every proved value of `s(n)` rests on one idea — unavoidable point sets — with
successive papers refining rather than replacing it.

| # | Strategy | Mechanism | Used on this problem? |
| --- | --- | --- | --- |
| 1 | Area counting | `s(n) ≥ √n` | Yes — trivially, never tight for non-squares |
| 2 | **Unavoidable point sets** | Place `n−1` points every unit square must hit; pigeonhole | **Yes — the workhorse for nearly every proved case** |
| 3 | Nonavoidance lemmas | Geometric sublemmas certifying a set is unavoidable | Yes — Friedman's Lemmas 1–3; Stromquist's 1–6 |
| 4 | The "box" relaxation | Use squares of side strictly `>1` so conditions are open | Yes — Stromquist's framing device |
| 5 | Duality / lattice rotation | Rotate the unavoidable lattice a quarter turn; colour argument | Yes — Kearney–Shiu, for `s(6) = s(7) = 3` |
| 6 | "Almost unavoidable" sets + forcing | Force squares into positions, then derive further points | Yes — Friedman, for the harder `n = 7, 14` |
| 7 | **Continuously varying families** | Replace a fixed point set by a parametrised family | Yes — Bentz 2016, for `s(22)=5`, `s(33)=6` |
| 8 | Generalised unavoidable points | Nagamochi's extension of the method | Yes — `s(m²−1) = s(m²−2) = m` |
| 9 | Restricted-orientation analysis | Prove a bound for a *subclass* of packings | Yes — Stromquist Thm 3 (0°/45°), settling Gardner |
| 10 | Exhaustive case analysis | Enumerate combinatorial configurations | Yes — inside most of the above |
| 11 | Symmetry reduction | Quotient the search by the container's symmetry group | Yes — standard within case analyses |
| 12 | Area-charging / measure arguments | Assign waste to regions and integrate | Yes — but asymptotically (Roth–Vaughan) |
| 13 | Analytic number theory | Bound waste via `√(x − ⌊x⌋)` behaviour | Yes — Roth–Vaughan, asymptotic only |
| 14 | "Good square" reduction | Show near-axis-aligned squares suffice asymptotically | Yes — asymptotic only (arXiv:2504.09489) |
| 15 | Interval arithmetic + branch and bound | Rigorously exclude all configurations numerically | **No — but proven feasible for circles in a square** |
| 16 | SOS / Positivstellensatz certificates | Certify semialgebraic infeasibility via SDP | **No known application to this problem** |
| 17 | LP/SDP relaxation with dual certificates | Bound via a relaxation's dual solution | No known application |
| 18 | Machine-checked formal proof | Verify a case analysis in Lean/Coq | No — but precedented by Flyspeck for Kepler |
| 19 | Electrical-network / Kirchhoff methods | Linear circuit laws on a dissection graph | **Not applicable — see below** |
| 20 | Graph encodings of dissections (c-nets) | Enumerate planar graphs of a tiling | Not applicable — dissection-only |

**The shape of the inventory.** Strategies 2–11 are one family: place points, prove they
are unavoidable, count.
Strategies 12–14 are a separate family that only speaks asymptotically.
Strategies 15–18 are general-purpose modern machinery that, as far as this research
found, **nobody has aimed at `s(11)`**.
Strategies 19–20 belong to a different problem entirely.

That is the honest state of the field: one technique does nearly all the work, and it has
not moved on `n = 11` since 2003.

**Strategy 15 deserves particular attention.** Computer-assisted optimality proofs by
interval arithmetic with branch and bound have already succeeded for the densest packings
of equal *circles* in a square — a problem of comparable flavour, also with irrational
optima and continuous degrees of freedom.
The obstruction for squares is that a square has a rotational degree of freedom that
enters the non-overlap conditions non-smoothly (the separating-axis condition is a
disjunction), which makes interval branch-and-bound branch far more heavily than in the
circle case, where non-overlap is a single smooth inequality per pair.
No attempt on `s(11)` by this route was found.
It is, in our assessment, the most plausible untried line of attack.

### Computational attacks

**Gensane & Ryckelynck (2005).** "Improved Dense Packings of Congruent Squares in a
Square," *Discrete & Computational Geometry*.
They introduce a **maximal inflation function** and an algorithm analogous to the
*billiard* methods used for packing congruent disks or spheres in a bounded domain:
configurations are perturbed and "inflated" until they jam.
Secondary sources report that they improved the best known packings for `n = 11, 29, 37`
and gave an alternative optimal packing of 18 squares.

**The n = 11 claim, and its resolution.** The status of their `n = 11` result requires
care, and we were unable to obtain the primary text (Springer paywall; ResearchGate and
Academia.edu returned HTTP 403).
What the accessible secondary record shows:

- Gensane and Ryckelynck "thought in 2004 that their program could slightly improve the
  packing from 1979."
- In **February 2023**, Thierry Gensane confirmed by correspondence that their program
  **could not** improve the 1979 packing.
- Every current record catalogue — Friedman's survey, the Kingbird catalogue, Wikipedia —
  still credits `n = 11` to **Trump, 1979**, at `≈ 3.877084`.
- The `explainxkcd` annotation describes the case as "discovered by Walter Trump in 1979
  and refined by Gensane et al. in 2004," which is consistent with a *numerical
  refinement of the same configuration* rather than a better configuration.

The best reading of the evidence is that the 2004/2005 `n = 11` entry was a refinement or
a marginal numerical artifact of the same geometric arrangement, later clarified as not
constituting an improvement.
**This should be confirmed against the primary DCG text before being relied upon.**

**A 2023 note.** A document titled "Packing of 11 unit squares in a square with minimum
size" was posted (ResearchGate, March 2023; author almost certainly Walter Trump, whose
ResearchGate profile hosts it).
Accessible excerpts state that the packing is "exactly defined by vertices of unit squares
laying on edges of other unit squares or the large square, making the geometrical object
absolutely rigid," and that the 1979 packing "cannot be improved by computer programs as
long as the same geometrical arrangement of the unit squares is used."
The full text was not retrievable (403).
Note the important qualifier — *as long as the same arrangement is used* — which is a
statement about local, not global, optimality.

**Interpretation.** Nearly fifty years of search, including modern global-optimization
methods, has failed to beat a configuration found by hand on a pocket calculator in 1979.
This is strong empirical evidence that Trump's packing is optimal, and correspondingly
weak evidence about how to *prove* it.

### The squared-square tradition: Kirchhoff, Tutte, and why the method does not transfer

There is a second, older, and far more successful body of work on "squares in squares"
which is frequently — and understandably — mistaken for this one.
It deserves a careful treatment here both because its machinery is genuinely beautiful
and because the temptation to import it is strong.

#### What the Trinity Four actually did

In the 1930s four Cambridge undergraduates — R. L. Brooks, C. A. B. Smith, A. H. Stone
and W. T. Tutte — attacked the problem of **dissecting** a rectangle into squares of
*distinct* sizes with *no gaps* (a "perfect" squared rectangle).
Their 1940 paper, "The dissection of rectangles into squares" (*Duke Math. J.* **7**,
312–340), reformulated the geometry as an electrical network, via what is now called a
**Smith diagram**.

The correspondence, verified against squaring.net's exposition, is exact:

| Circuit object | Geometric object |
| --- | --- |
| Node / terminal | A maximal horizontal line segment in the dissection |
| Wire / edge | A component square, joining the node of its top edge to that of its bottom edge |
| Current magnitude | The side length of that square |
| Potential difference across the wire | The height of that square (equal to its side) |
| Potential difference between the poles | The vertical side of the whole rectangle |
| Resistance | Unit (1 ohm) on every wire |
| Kirchhoff's current law at a node | Total width of squares resting on a seam equals total width hanging beneath it |
| Kirchhoff's voltage law around a circuit | Net change in level around any closed path is zero |

With unit resistance, Ohm's law `V = IR` collapses to `V = I` — voltage equals current —
which is precisely the statement that height equals width, i.e. that the tile is a
*square* rather than a rectangle.
That is the pivot of the whole construction.
Solving the resulting linear system by matrix algebra yields the currents, hence the side
lengths; because the system is linear with rational coefficients, the solution is
**always rational**, and clearing denominators produces integer squared rectangles.

So the account given to you is accurate on the mechanism.
Two historical refinements are worth recording:

- **Priority for the first perfect squared *square* belongs to Roland Sprague, not the
  Trinity Four.** Sprague, in Berlin, assembled perfect rectangles (including Moroń's
  33×32 and 65×47) into an order-55 compound squared square of side 4205, published in
  1939 — before Brooks, Smith, Stone and Tutte published theirs. The Cambridge group
  built the *theory*; Sprague got the first square into print.
- The lowest-order simple perfect squared square is **order 21, side 112**, found by
  A. J. W. Duijvestijn on 22 March 1978 by computer search over c-nets, and it is unique.

#### Why it cannot be carried over to `s(11)`

The method has three structural prerequisites, and the 11-unit-squares problem violates
all three.

1. **It requires a gapless tiling.** Nodes are *maximal horizontal seams*; the network
   exists only because every point of the rectangle is covered and the seams partition
   it. Trump's packing is 73.18% dense — the container has area 15.0318 against 11 units
   of square, leaving 4.0318 of waste, about 26.8%. There are no spanning seams to become
   nodes, and no conservation law across a gap.
2. **It requires squares of distinct size.** The information content of a Smith diagram
   is that different currents flow through different wires. With eleven *equal* squares
   every current is identical, the network is degenerate, and the linear system says
   nothing.
3. **It requires axis-aligned squares.** Kirchhoff's current law translates into a
   statement about widths meeting along a *horizontal* seam. A square tilted at
   `≈ 40.182°` has no horizontal edge and belongs to no seam.

There is a fourth objection, and it is decisive on its own.
**The method produces rational answers by construction.**
Linear equations with rational coefficients have rational solutions; that rationality is
exactly why the Trinity Four could scale their dissections to integers, and it is the
source of the method's power.
But the conjectured `s(11)` is a root of an *irreducible degree-8* polynomial over ℚ
(verified in this research).
A technique whose output is always rational cannot, even in principle, produce an
irrational algebraic number of degree 8.
This is not a matter of the method being unwieldy here — it is provably the wrong
codomain.

#### What the right analogue actually is

The productive way to hold the intuition is this.
Tutte's insight was: *impose the contact structure as a system of equations and solve
algebraically, rather than searching geometrically.*
That insight **does** transfer.
It is exactly strategy 17 in the construction catalogue above, and it is how the degree-8
polynomial for Trump's packing is obtained: read off the contact graph, write each
tangency as a polynomial equation, and eliminate.
The same programme is standard in the rigidity-theoretic study of sphere and disk
packings, where contact graphs, rigidity, and Gröbner-basis elimination are routine
tools.

What changes is the *algebra*, and the change is the whole difficulty:

| | Squared rectangles (Tutte) | Unit squares packed with gaps |
| --- | --- | --- |
| Contact conditions | Linear (seam widths sum) | Quadratic and trigonometric (tilt angles) |
| Solution field | ℚ — always rational | Algebraic of high degree (8 for `n = 11`) |
| Structure | Planar graph + linear algebra | Semialgebraic variety |
| Gaps | None permitted | Essential — 26.8% here |
| Right tool | Kirchhoff's laws, matrix algebra | Elimination theory, real algebraic geometry |

So the promising direction is real, but it is not Kirchhoff's laws.
It is the modern descendant of the same instinct: treat the packing as a semialgebraic
set and bring real algebraic geometry to bear — elimination for the constructions
(already done, and it is where the degree-8 polynomial comes from), and
Positivstellensatz-style infeasibility certificates for the bounds (strategy 16, and as
far as this research found, never attempted here).
That, together with interval branch-and-bound (strategy 15), is where we would look.

### Asymptotic theory, and why it does not help

A parallel and much more active literature studies `W(x)`, the **wasted area** when
packing unit squares into a large square of side `x`.

| Result | Bound on `W(x)` | Approx. exponent |
| --- | --- | --- |
| Erdős & Graham (1975) | `O(x^{7/11})` | 0.636 |
| Roth & Vaughan (1978), lower bound | `W(x) > 10⁻¹⁰⁰ √(x − ⌊x⌋)` | — |
| Montgomery | `O(x^{(3−√3)/2})` | 0.634 |
| Chung & Graham (2009) | `O(x^{(3+√2)/7} log x)` | 0.631 |
| Chung & Graham (2020, claimed) | `O(x^{3/5})` | 0.600 |
| McClenagan (2026), Bui (2025) | `O(x^{3/5})` | 0.600 |

The Erdős–Graham result is the historical origin of the insight that **tilted** unit
squares beat axis-aligned ones — the same phenomenon that makes `n = 11` interesting,
appearing asymptotically.
Roth and Vaughan's lower bound shows waste is unavoidable and is proportional to at least
the square root of the distance from `x` to the nearest integer; they also introduced the
notion of a **good square** (inclination at most `10⁻¹⁰`), and it has since been shown
that for computing the asymptotic growth of wasted space it suffices to consider packings
with only good squares (arXiv:2504.09489).
Recent activity is brisk: arXiv:2508.04603 ("Square packing with `O(x^{0.6})` wasted
area") and arXiv:2602.01484 (McClenagan, "Optimally Packing a Large Square by Unit
Squares," 1 Feb 2026, from a 2024 thesis).

**Why this is irrelevant to `n = 11`.** These are asymptotic statements with unspecified
or astronomically weak constants — Roth and Vaughan's explicit `10⁻¹⁰⁰` is emblematic.
They describe behaviour as `x → ∞` and carry no information at `x ≈ 3.88`.
The small-case and asymptotic branches of this subject share an origin and a moral (tilting
helps) but are methodologically disjoint.
No asymptotic improvement will ever settle `n = 11`.

### Corrections to common summaries

The briefing that prompted this research, and many secondary summaries, contain errors
worth recording so they are not propagated.

| Claim | Verdict | Correct statement |
| --- | --- | --- |
| Stromquist's paper "mathematically proves Walter Trump's 11-square breakthrough" | **False** | It proves a lower bound `s(11) ≥ 3.7889`, which does not match Trump's `3.8771`. `s(11)` is unresolved. |
| The paper "verifies that 11 is the first instance where the optimal configuration forces a non-45-degree tilt" | **True** | This is exactly Gardner's conjecture, settled via Theorem 3 plus Trump's construction. |
| `s(10) = 3 + √3 ≈ 3.707`, `s(11) ≤ 2 + 2√3 ≈ 3.789` (seen in an AI-generated search summary) | **False** | Arithmetically impossible: `3 + √3 ≈ 4.732`. The correct constants are `3 + ½√2` and `2 + 4/√5`. A LaTeX-mangling artifact. |
| `n = 11` is "the smallest example where the best known packing contains squares at three different angles" | **False** | That is `n = 17` (Bidwell, 1998). `n = 11` uses two orientation classes: axis-aligned and `≈ 40.182°`. |
| The Trinity Four "discovered the first Perfect Squared Squares" | **Misattributed** | Roland Sprague published the first perfect squared square (order 55, side 4205) in 1939, ahead of Brooks–Smith–Stone–Tutte. The Cambridge group built the theory. |
| Kirchhoff's-law / Smith-diagram methods are a promising route to new bounds here | **False** | The method requires a gapless tiling by distinct axis-aligned squares and yields rational answers by construction. All four conditions fail for `s(11)`. See the dedicated section. |

The third row is a useful caution: at least one automated summarizer produced
self-contradictory arithmetic while citing a correct source.
Every numeric constant in this document was re-derived or checked numerically.

### Cultural and expository record

- **Martin Gardner**, "Mathematical Games," *Scientific American*, October 1979, with
  follow-ups November 1979, March 1980, November 1980.
  This is where the problem entered wide circulation and where the conjecture was posed.
  Trump's packing reached Gardner by correspondence in 1979 and was first published
  correctly in one of Gardner's books.
- **xkcd 2740, "Square Packing."** Depicts "improving" the `n = 11` record with a
  hydraulic press, citing `s < 3.877084`; the joke is that crushed squares are no longer
  squares. The explainxkcd annotation correctly notes the packing is unproven.
- **Stand-up Maths (Matt Parker)**, "The Insane World of Polygon Packings" — visual
  treatment of how grid patterns give way to tilted arrangements.
- **Erich Friedman's Packing Center** and the **Kingbird "Squares in Squares"
  catalogue** are the two live record directories; Kingbird supplies exact minimal
  polynomials and SVG layouts, and marks configurations rigid or not.

### Adjacent problems (deliberately out of scope)

These are frequently conflated with the present problem in casual sources:

- **Packing consecutive/unequal squares** (sides `1, 2, …, n`) — a different problem with
  its own literature (e.g. guillotine-cutting asymptotics, *Optimization Letters* 16
  (2022) 2775–2785). A search for "square packing" papers will surface these; they say
  nothing about `s(11)`.
- **Squared squares / perfect dissections** (gapless tilings by *distinct* squares) — the
  Tutte–Kirchhoff tradition, treated at length above because its machinery is so often
  assumed to apply here. It does not.
- **Covering** a square by squares (as opposed to packing) — different objective.
- **Packing unit squares in a circle, triangle, or rectangle** — related technique
  (unavoidable points), different constants.

## Key Insights

1. **The problem is open, and the gap is structural, not incidental.** `s(11)` is pinned
   only to `[3.788854, 3.877084]`. Both endpoints have stood unimproved for over two
   decades (lower) and nearly five (upper).

2. **Gardner's conjecture was settled without solving the problem.** Stromquist proved
   the *necessity* of oblique tilts by bounding the 0°/45° class from below at `3.885618`
   and pointing at Trump's `3.877084`. This is a clean example of resolving a qualitative
   question while the quantitative one stays open — and it is the single most
   misunderstood point in the popular literature.

3. **Algebraic degree is the likely obstruction.** Every solved case has `s(n)` of degree
   ≤ 2 over ℚ. The conjectured `s(11)` is a root of an irreducible degree-8 polynomial
   (verified in this research). Unavoidable-point arguments certify thresholds built from
   unit distances and container coordinates, which naturally produce low-degree
   constants. Closing the `n = 11` gap by that method would require certifying a
   degree-8 threshold — no such argument is known, and it is not obvious one exists.

4. **Rigidity explains computability but not optimality.** Trump's packing is rigid, so
   its contact conditions determine `s` exactly as an algebraic number. Rigidity implies
   local optimality within its combinatorial contact class. It says nothing about whether
   a different contact class does better, which is precisely what a proof must exclude.

5. **The failure of computation is informative in one direction only.** Fifty years of
   search, including a purpose-built billiard/inflation algorithm, has not beaten a
   hand-computed 1979 configuration. That raises confidence in the *conjecture* and
   provides no leverage on the *proof*.

6. **Bentz's technique is the most plausible route forward.** His proofs of `s(22) = 5`
   and `s(33) = 6` replace fixed unavoidable point sets with "continuously varying
   families of such sets." That is a genuine strengthening of the method's expressive
   power. Whether it can reach an irrational, high-degree target rather than an integer
   one is, as far as this research found, untested.

7. **The two literatures do not meet.** Asymptotic wasted-space bounds (now at
   `O(x^{3/5})`) and exact small-case results share the tilting insight and nothing else.
   Progress on `n = 11` will not come from that direction.

8. **The proof inventory is far narrower than the search inventory.** Twenty distinct
   construction strategies have produced records; essentially *one* proof idea —
   unavoidable point sets — underlies nearly every proved value, with later papers
   refining it (duality, forcing, continuously varying families) rather than replacing
   it. A field with one load-bearing technique stalls when that technique reaches its
   limit, which is what appears to have happened at `n = 11`.

9. **The Kirchhoff/Tutte method is provably the wrong tool, not merely an awkward one.**
   Beyond needing a gapless tiling of distinct axis-aligned squares — three conditions
   `n = 11` violates outright — the method solves *linear* systems and therefore always
   returns *rational* side lengths. The conjectured `s(11)` is irrational of degree 8.
   No amount of adaptation lets a rational-output method emit a degree-8 irrational.
   What does survive is Tutte's deeper instinct — impose contacts as equations and solve
   algebraically — which is exactly how the degree-8 polynomial is derived. The algebra
   just stops being linear, and that is the whole difficulty.

10. **Two modern general-purpose techniques appear genuinely untried here.** Rigorous
    interval branch-and-bound has already produced computer-assisted optimality proofs
    for equal *circles* in a square, and Positivstellensatz/SOS certificates are the
    standard machinery for certifying semialgebraic infeasibility. Neither appears in the
    `s(11)` literature. The square's rotational degree of freedom makes non-overlap a
    disjunctive rather than smooth condition, which is a real obstacle for the first —
    but "harder than circles" is not "impossible", and nobody seems to have tried.

## Open Questions

- [ ] Can the unavoidable-point method, or Bentz's continuously-varying refinement, prove
      any lower bound of algebraic degree > 2? This appears to be the key methodological
      question gating `n = 11`.
- [ ] What *is* the best lower bound obtainable in principle from a finite unavoidable
      point set in a container of side `≈ 3.877`? Is there a proved ceiling below
      `3.877084`?
- [ ] Could a rigorous computer-assisted proof (interval arithmetic plus branch-and-bound
      over contact classes, as used for rigorous circle packing in a circle) close the
      gap? This has been done for related packing problems but no attempt on `s(11)` was
      found.
- [ ] Verify the Gensane–Ryckelynck `n = 11` entry against the primary DCG text and
      determine exactly what was claimed in 2004/2005 versus retracted in 2023.
- [ ] Obtain the full text of the March 2023 "Packing of 11 unit squares in a square with
      minimum size" note and the exact coordinates of all 11 squares (extractable from the
      Kingbird SVG source).
- [x] ~~Resolve the `n = 23` discrepancy~~ — **resolved**: `n = 23` is covered by
      Nagamochi's `s(m²−1) = s(m²−2) = m` at `m = 5`, and other enumerations list it
      explicitly. Wikipedia's list is simply incomplete.
- [ ] Has any Positivstellensatz/SOS infeasibility certificate ever been attempted for a
      square-packing lower bound, in any case, at any `n`? Nothing was found.
- [ ] What is the practical branching cost of interval branch-and-bound on `s(11)` given
      the disjunctive separating-axis condition? Is the case explosion merely large or
      genuinely prohibitive?
- [ ] Did Gensane–Ryckelynck's inflation algorithm ever explore contact classes for
      `n = 11` other than Trump's, and is that enumeration recorded anywhere?
- [ ] Confirm whether Packomania covers squares-in-squares records or is circle-focused;
      it was listed in the source briefing but not verified here.

## Methodology

Research was conducted on 2026-08-22 by web search and direct retrieval of primary
sources, with numerical and symbolic verification of every constant.

**Primary sources retrieved in full.** Stromquist's 2003 paper was downloaded as PDF and
its text extracted locally (via `pdfminer.six`, after repairing a broken `cffi`
installation) so that theorem statements, lemma statements, and the reference list could
be read directly rather than through summaries.
This proved essential: the abstract's mathematical notation is mangled by every automated
summarizer encountered, and one search summary returned arithmetically impossible
constants.

**Independent verification performed.**

- Confirmed `3 + √(1/2) = 3.7071067811865475`, `2 + 2√(4/5) = 2 + 4/√5 =
  3.7888543819998315`, and `2 + 4√2/3 = 2 + 2√(8/9) = 3.885618083164127`, establishing
  that the abstract's two forms of the Theorem 3 constant agree.
- Evaluated the degree-8 polynomial at the published side length: `P(3.87708359002281) ≈
  −6.4 × 10⁻¹³`, consistent to available precision.
- Factored the polynomial symbolically (SymPy): **irreducible over ℚ**, with exactly two
  real roots, the positive one being `3.877083590022814`.
- Computed the open interval width: `0.08822920802297851`.

**Sources that could not be retrieved.** ResearchGate (HTTP 403), Academia.edu (403), ACM
Digital Library (403), and Springer (authentication redirect) blocked access to the
Gensane–Ryckelynck primary text and the March 2023 note.
Claims resting on those are marked as secondary and flagged in
[Open Questions](#open-questions).

**Link validation.** All 26 cited URLs were re-checked with `curl` after the second pass.
Twenty-four return HTTP 200.
Two return bot-blocking codes to automated checkers but are valid in a browser:
ScienceDirect (403) and YouTube (429).
Two defects found in the first pass were fixed: a citation pointing at the wrong
Electronic Journal of Combinatorics article, and a dead author-hosted copy of
Erdős–Graham (1975) — the latter now resolves to the Stanford technical report
CS-TR-75-483, which is live.

**Second research pass (same day).** The strategy catalogues, the squared-square section,
and the Kirchhoff transferability assessment were added in a second pass.
The Smith-diagram correspondence was verified line by line against squaring.net's
exposition rather than reproduced from memory or from the briefing; the priority question
(Sprague vs. the Trinity Four) was checked separately and the briefing's attribution
corrected.
The non-transferability argument rests on four independent conditions, of which the
rationality objection is self-contained and decisive: it follows from the linearity of
Kirchhoff's laws together with the degree-8 irreducibility established in the first pass.
The `n = 23` question left open after the first pass was resolved.

**Confidence.** High for everything sourced to the Stromquist paper (read directly),
Friedman's survey, and the numeric verifications.
Medium for the Gensane–Ryckelynck history and the 2023 correspondence, which rest on
secondary reporting.
High for the Smith-diagram correspondence and the squared-square history (checked against
a specialist primary-facing source).
The claims that interval branch-and-bound and SOS certificates have *never* been applied
to `s(11)` are negative results from search, and negative results from search are weak:
they mean nothing was found, not that nothing exists.

## References

Primary literature:

- [Walter Stromquist, "Packing 10 or 11 Unit Squares in a Square," *Electron. J. Combin.* 10 (2003), #R8](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8) — the central paper; read in full.
- [Erich Friedman, "Packing Unit Squares in Squares: A Survey and New Results," *Electron. J. Combin.*, Dynamic Survey DS7](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html) — the standard survey and record table.
- [Wolfram Bentz, "Optimal Packings of 13 and 46 Unit Squares in a Square," *Electron. J. Combin.* 17 (2010), #R126](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1r126/pdf/)
- [Wolfram Bentz, "Optimal Packings of 22 and 33 Unit Squares in a Square," arXiv:1606.03746](https://arxiv.org/abs/1606.03746)
- [Michael J. Kearney and Peter Shiu, "Efficient packing of unit squares in a square," *Electron. J. Combin.* 9 (2002), #R14](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v9i1r14) — introduces a duality method, giving the first published proof that `s(6) = 3`, and also treats `s(7) = 3`.
- [Thierry Gensane and Philippe Ryckelynck, "Improved Dense Packings of Congruent Squares in a Square," *Discrete Comput. Geom.* (2005)](https://link.springer.com/article/10.1007/s00454-004-1129-z) — paywalled; not read directly.
- Martin Gardner, "Mathematical Games," *Scientific American*, October 1979 (also November 1979, March 1980, November 1980) — origin of the conjecture.
- Pertti Hämäläinen, correspondence, 20 April 1980 — the optimal 45° packing of 11 squares.
- Stromquist, "Packing unit squares inside squares," I–III, Daniel H. Wagner Associates Memoranda, 1984 — unpublished precursors; memorandum III covers `n ≤ 65` and Gardner's conjecture for `n = 11`.

Asymptotic wasted-space literature:

- [K. F. Roth and R. C. Vaughan, "Inefficiency in packing squares with unit squares," *JCTA* (1978)](https://www.sciencedirect.com/science/article/pii/0097316578900055)
- [P. Erdős and R. L. Graham, "On packing squares with equal squares," *J. Combin. Theory Ser. A* **19** (1975), 119–123 — Stanford tech report CS-TR-75-483](http://i.stanford.edu/pub/cstr/reports/cs/tr/75/483/CS-TR-75-483.pdf)
- [M. Z. Arslanov, S. A. Mustafin, Z. K. Shangitbayev, "Improved packings of n(n−1) unit squares in a square," *Electron. J. Combin.* 28(4)](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v28i4p22/pdf/)
- [Rory McClenagan, "Optimally Packing a Large Square by Unit Squares," arXiv:2602.01484](https://arxiv.org/abs/2602.01484)
- [Square Packing with Asymptotically Smallest Waste Only Needs Good Squares, arXiv:2504.09489](https://arxiv.org/pdf/2504.09489)
- [Square packing with O(x^0.6) wasted area, arXiv:2508.04603](https://arxiv.org/pdf/2508.04603)

The squared-square dissection tradition (for contrast — a different problem):

- [R. L. Brooks, C. A. B. Smith, A. H. Stone, W. T. Tutte, "The dissection of rectangles into squares," *Duke Math. J.* 7 (1940), 312–340](https://projecteuclid.org/euclid.dmj/1077492259)
- [squaring.net — Brooks, Smith, Stone and Tutte, II](http://www.squaring.net/history_theory/brooks_smith_stone_tutte_II.html) — the precise Smith-diagram correspondence, verified against this source.
- [squaring.net — Roland Percival Sprague (1894–1967)](http://www.squaring.net/history_theory/sprague.html) — priority for the first published perfect squared square.
- [squaring.net — Simple Perfect Squared Squares, Order 21](http://www.squaring.net/sq/ss/spss/o21/spsso21.html) — Duijvestijn's unique lowest-order example.
- [Trinity Mathematical Society — The Squared Square](https://tms.soc.srcf.net/about-the-tms/the-squared-square/)
- [Wolfram MathWorld — Perfect Square Dissection](https://mathworld.wolfram.com/PerfectSquareDissection.html)
- [Compound Perfect Squared Squares of the Order Twenties, arXiv:1303.0599](https://arxiv.org/abs/1303.0599)

Record catalogues and reference works:

- [Erich Friedman's Packing Center — Packing Unit Squares in Squares](https://erich-friedman.github.io/papers/squares/squares.html)
- [Kingbird, "Squares in Squares"](https://kingbird.myphotos.cc/packing/squares_in_squares.html) — exact minimal polynomials, rigidity flags, SVG layouts.
- [Kingbird, "Squares in Squares: Older / Alternative Packings"](https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html) — supersession history, showing which records fell to which method and when.
- [Wikipedia, "Square packing"](https://en.wikipedia.org/wiki/Square_packing)

Expository:

- [xkcd 2740, "Square Packing"](https://www.explainxkcd.com/wiki/index.php/2740:_Square_Packing)
- [Stand-up Maths, "The Insane World of Polygon Packings"](https://www.youtube.com/watch?v=jWT08JVb-fk)
- [Wikimedia Commons: Packing 11 unit squares in a square with side length 3.87708359…](https://commons.wikimedia.org/wiki/File:Packing_11_unit_squares_in_a_square_with_side_length_3.87708359....svg)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
