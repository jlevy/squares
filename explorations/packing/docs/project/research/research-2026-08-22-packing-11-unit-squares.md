# Research: Packing 11 Unit Squares in a Square

**Date:** 2026-08-22 (last updated 2026-08-22, expanded with strategy catalogues)

**Author:** Claude (agent), for samanthadrakova@gmail.com

**Status:** Complete

## How to read the citations

Claims in this document carry an inline key in bold brackets, e.g.
**[Stromquist 2003]**. Every key resolves in two places:

1. The [References](#references) section below, with full bibliographic detail and a
   URL.
2. **A local copy** in [`resources/`](../../../resources/README.md) — the original PDF,
   a cleaned Markdown transcription, and the unedited extraction it was cleaned from.

So every cited source can be read and grepped locally without re-fetching:

```bash
grep -rn "unavoidable" explorations/packing/resources/papers/*.md
```

Where a claim rests on a source that could **not** be retrieved, it is marked
**[secondary]** and the obstacle is recorded in the resources README. Those claims are
the weakest in this document and are flagged again in [Open Questions](#open-questions).

## Overview

This document records everything that could be established about the problem of packing
11 unit squares into the smallest possible enclosing square.
It is written to support *full technical understanding* of the problem and its
literature, not to introduce the topic pedagogically.
Claims are separated by evidential status: proved, computationally verified, best known,
or asserted-but-unverified.

The motivating observation is that `n = 11` is the smallest case of a natural,
easily-stated geometry problem that remains **unsolved** after nearly fifty years.
The best known packing dates from 1979 and has never been improved; the best proved
lower bound dates from 2003 and has never been improved.
A gap of roughly 0.088 in the side length separates them.
Understanding precisely *where* that gap comes from — and why the available proof
technique cannot close it — is the substance of this document.

The document also catalogues, at length, the two inventories that define the field’s
reach: the **search strategies** that have produced every known packing, and the **proof
strategies** that have produced every known bound.
The asymmetry between them is the clearest available explanation of why the problem is
stuck.
A dedicated section assesses whether the Kirchhoff/Tutte electrical-network method
famous from the squared-square literature can be brought to bear here; the conclusion is
that it provably cannot, though the instinct behind it does survive in another form.

A secondary purpose is corrective.
Widely circulated summaries of this problem, including the briefing that prompted this
research, state that Stromquist’s 2003 paper *proved* Walter Trump’s 11-square packing
optimal. That is false, and the error is consequential enough to be worth stating
precisely. See [Corrections to Common Summaries](#corrections-to-common-summaries).

## Questions to Answer

1. What exactly is the state of knowledge for `s(11)` — what is proved, and what is only
   conjectured?
2. What is Trump’s packing, and what is its exact algebraic characterization?
3. What did Stromquist actually prove in 2003, and what was Gardner’s conjecture?
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
lower bounds; the historical record; computational searches; the asymptotic wasted-space
literature insofar as it bears on the problem’s structure.

**Included by contrast:** the squared-square dissection tradition (Dehn, Moroń, Sprague,
the Trinity Four, Duijvestijn), covered specifically to establish whether its machinery
transfers. See
[The squared-square tradition](#the-squared-square-tradition-kirchhoff-tutte-and-why-the-method-does-not-transfer).

**Excluded:** packing *unequal* or consecutively-sized squares as a research goal in its
own right (a distinct problem — see
[Adjacent Problems](#adjacent-problems-deliberately-out-of-scope)); packing squares into
circles, triangles, or rectangles except where cited for contrast; circle packing;
online/streaming packing algorithms; bin-packing complexity theory.

## Findings

### Notation and trivial bounds

Following the standard convention established in Friedman’s survey and used throughout
the literature:

> `s(n)` is the side of the smallest square into which `n` unit squares can be packed.

Packings permit arbitrary rotation and translation, and require only non-overlapping
interiors. Two elementary bounds hold for all `n`:

- **Area (lower):** `s(n) ≥ √n`, since `n` unit squares have total area `n`.
- **Grid (upper):** `s(n) ≤ ⌈√n⌉`, by the axis-aligned grid packing.

For `n = 11` these give `3.31662… ≤ s(11) ≤ 4`. Both are far from tight.
The entire difficulty of the problem lies between them.

### The state of knowledge for n = 11

| Quantity | Value | Status | Source |
| --- | --- | --- | --- |
| Area lower bound | `√11 ≈ 3.316625` | Trivial | — |
| **Best proved lower bound** | `2 + 2√(4/5) = 2 + 4/√5 ≈ 3.788854` | **Proved** | **[Stromquist 2003]**, Thm 2; still the recorded bound in **[Friedman DS7]** |
| **Best known packing (upper bound)** | `≈ 3.877084` | **Construction only** | Trump 1979, via **[Friedman DS7]**, **[Kingbird]** |
| Lower bound for 0°/45°-only packings | `2 + (4/3)√2 ≈ 3.885618` | **Proved** | **[Stromquist 2003]**, Thm 3 |
| Grid upper bound | `4` | Trivial | — |

The open interval is `[3.788854…, 3.877084…]`, of width `≈ 0.088230`.

Two facts about this table are worth stating explicitly because they are frequently
garbled:

1. **`s(11)` is not known.** It is the smallest `n` for which `s(n)` is undetermined.
2. **The 0°/45° bound (3.8856) exceeds the best known packing (3.8771).** This is not a
   contradiction — it is the entire point of Theorem 3, and the mechanism by which
   Gardner’s conjecture was settled.
   See below.

### Trump’s packing (1979): structure and exact characterization

The best known packing of 11 unit squares was found by **Walter Trump** in 1979, a
German physics teacher and recreational mathematician.
It improved an earlier packing of Göbel’s. Friedman’s survey notes that “many people
have independently discovered this packing,” so priority is shared in practice even
though 1979/Trump is the standard attribution.

**Geometry.** The configuration places most squares axis-aligned, with a group of middle
squares tilted at approximately **40.182°** — an angle that is neither 0° nor 45°, and
which has no simple closed form.
**[Friedman DS7]** describes it as: “The middle squares are tilted about 40.182°, and
there is a small gap between these squares.”
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
- It has exactly **two real roots**: `≈ −1.853032478972508` and `≈ 3.877083590022814`.
  The second is the packing value.
- Substituting the published 15-digit value gives `P(s) ≈ −6.4 × 10⁻¹³`, consistent with
  it being the root to available precision.

**Rigidity.** Both **[Friedman DS7]** and **[Kingbird]** mark this packing as **rigid**:
the squares admit no continuous deformation, and the configuration is pinned by vertices
of unit squares lying on edges of other unit squares or of the container.
Rigidity is what makes the exact algebraic value computable at all — the contact
conditions form a determined polynomial system — and it is evidence of local optimality.
It is *not* evidence of global optimality, and this distinction is the crux of the open
problem.

#### The exact construction: contact equations, coordinates, and closed form

The full defining data of Trump’s packing is recoverable, and was reconstructed and
independently re-verified during this research from **[Ellsworth SVG]** — the annotated
source of the `n = 11` diagram in David Ellsworth’s catalogue, archived locally at
`explorations/packing/resources/papers/kingbird-square-11-provenance.svg`.

**Composition.** The eleven squares split as **six axis-aligned and five tilted**. The
axis-aligned six are: one in a corner, one mirrored against the opposite side, one
offset along the top at `x₀`, and an L-shaped block of three.
The five tilted squares form a single rigid group, all at the same angle `a`, rotated
about the point `(1,1)` and offset by `r₁`.

**The tilt angle.** `a = 40.1819372903297164652303423680606…°`, and `sec a` is a root of

```
x⁸ − 2x⁷ − x⁴ + 2x³ + 8x² − 12x + 5 = 0
```

The algebraic quantities `sec a`, `cos a`, `sin a`, `tan(a/2)`, and `s` lie in the
degree-8 number field used by the exact verifier.
The angle `a` itself, measured in radians, is transcendental: if a non-zero `a` were
algebraic, Lindemann–Weierstrass would make `exp(i a)` transcendental, whereas algebraic
`cos a` would make it a root of `z² - 2 cos(a)z + 1` and therefore algebraic.

**The two contact equations.** The entire configuration is pinned by just two equations
in `s` and `a`:

```
(s − 2)·cos a + (s − 3)·sin a = 2

cos a + (s − 1 + (s − 2)·cot a)·csc a − cot a·(3 + 2·cot a) − sin a − (2 − (s − 2)·sin a)·tan a = 1
```

Eliminating `a` between them yields the degree-8 minimal polynomial for `s`.

**A closed form for `s` in terms of `a`.** Solving the first equation alone gives a
strikingly compact relation:

```
s = 2 + (2 + sin a) / (cos a + sin a)
```

This is the cleanest available characterisation of the packing: one elegant identity
plus one messy transcendental constraint, whose joint elimination is degree 8.

**Derived constants** (the offsets that place the tilted block):

| Constant | Closed form | Value |
| --- | --- | --- |
| `s` | root of the degree-8 polynomial | `3.87708359002281417730789706010096` |
| `a` | `arcsec` of the degree-8 root | `40.1819372903297164652303423680606°` |
| `x₀` | `1 + 2·sec a − (s−2)·tan a` | `2.03255831434961478706261630031475` |
| `r₁` | `1 − (s−3)·cos a` | `0.329908598887370278746514124701845` |
| `u₁` | `((1+r₁)·cos a − 1)·csc a` | `0.024874535025596953980475509175010` |
| `v₁` | `cos a − sin a` | `0.118782607549453467521102077399075` |
| `v₂` | `(s−1)·csc a − r₁ − (3+u₁)·cot a` | `0.547441432087314221163298461396782` |

*Verified independently in this research at 40-digit precision:* both contact equations
hold with residuals below `10⁻³²`; the closed form for `s` reproduces the published
value to the same precision; all five derived constants match their closed forms; and
`sec a` satisfies the degree-8 polynomial above with residual `≈ 3 × 10⁻³³`.

**History of the exact solution — distinct from the packing itself.** This deserves
separating, because conflating the two is the source of the “Gensane–Ryckelynck improved
`n = 11`” confusion:

- **1979 — Walter Trump** finds the packing.
  Published in Gardner’s collection *Fractal Music, Hypercards and More* (1991).
- **1980 — independent rediscovery** by Mats Gustafsson and Magnus Thulin, in the
  Swedish periodical *Ronden*; also reported by Gardner in November 1980
  **[Ellsworth SVG]**. Note the nuance: **[Friedman DS7]** records that the *original
  discovery* “has been incorrectly attributed to Gustafson and Thule,” i.e. priority is
  Trump’s and theirs was a rediscovery.
  Friedman also notes many independent rediscoveries generally.
- **Before 19 May 2004 — Gensane and Ryckelynck** compute the first *exact algebraic*
  solution, in the DCG paper (p. 10 of 13). They eliminate using a system of **14
  equations**. They do not publish `s` in reduced root form: only the cosine of one
  angle (offset by 45°), with a formula in terms of that root given for `2/s` rather
  than `s`, though presented as a formula for `s`.
- **4 June 2023 — David Ellsworth** obtains the reduced root form — the degree-8 minimal
  polynomial recorded throughout this document — and shows the elimination needs only
  **two** equations rather than fourteen.
- **4 June 2023, some 13 hours later — Boris Alexeev** independently confirms it by a
  substantially different method.

### What Stromquist actually proved (2003)

**[Stromquist 2003]** — Walter Stromquist, “Packing 10 or 11 Unit Squares in a Square,”
*The Electronic Journal of Combinatorics* **10** (2003), #R8. Submitted 26 Nov 2002;
accepted 26 Feb 2003; published 18 Mar 2003. MR subject classifications 05B40, 52C15.

The paper contains **three** theorems, and conflating them is the source of most public
confusion.

**Theorem 1.** Ten pairwise non-intersecting boxes cannot exist in the interior of a
square of side `s = 3 + √(1/2)`. Consequently

```
s(10) = 3 + ½√2 ≈ 3.707107
```

This *is* an exact determination — `n = 10` is solved.

**Theorem 2.** Let `s = 2 + 2√(4/5) ≈ 3.789`. Then eleven non-intersecting boxes cannot
exist inside a square of side `s`. Consequently

```
s(11) ≥ 2 + 2√(4/5) = 2 + 4/√5 ≈ 3.788854
```

This is a **lower bound only**. It does not match Trump’s `≈ 3.877084`, and Stromquist
makes no claim that it does.

**Theorem 3.** Let `s = 2 + (4/3)√2 ≈ 3.886`. Then eleven non-intersecting boxes cannot
exist inside a square of side `s` *if each box has orientation 0° or 45° with respect to
the container*. So any **45° packing** of 11 squares needs side at least
`2 + (4/3)√2 ≈ 3.885618`. The abstract writes this constant equivalently as
`2 + 2√(8/9)`; the two agree, since `2√(8/9) = 4√2/3`. This bound is realized — hence
tight — by a packing due to **Pertti Hämäläinen** (correspondence, 20 April 1980).

#### The Gardner conjecture argument

Martin Gardner conjectured (*Scientific American*, “Mathematical Games,” October 1979,
with follow-ups in November 1979, March 1980, and November 1980) that `n = 11` is the
first case in which an optimal packing *requires* orientations other than 0° and 45°.

The proof is a two-line comparison, and it is elegant precisely because it sidesteps
determining `s(11)`:

- By Theorem 3, **any** packing restricted to 0°/45° needs side `≥ 3.885618`.
- Trump’s packing achieves side `≈ 3.877084 < 3.885618`, using a `≈ 40.182°` tilt.
- Therefore no 0°/45° packing can be optimal: a non-45° packing strictly beats every 45°
  packing.

Stromquist’s closing line: this “establishes the truth of Martin Gardner’s conjecture.”

**The logical shape matters.** The conjecture is about the *necessity of oblique
orientations*, not about the *value* of `s(11)`. It is settled by bracketing a
restricted class from below and exhibiting an unrestricted construction that beats it.
`s(11)` itself is untouched by the argument and remains open.

For contrast, the two smaller cases with tilted squares — `n = 5` and `n = 10` — both
use 45° tilts, which is why 11 is the first case where genuinely oblique angles are
forced.

### The lower-bound method: boxes, nonavoidance lemmas, unavoidable points

The technique of **[Stromquist 2003]**, inherited from his own 1984 memoranda and from
**[Friedman DS7]**, is the standard machinery for square-packing lower bounds.

**The box device.** A **box** is defined as the interior of any square of side *strictly
greater than 1*. To establish `s(n) ≥ a`, one proves the equivalent statement that `n`
non-overlapping boxes cannot be packed inside a square of side exactly `a`. As
Stromquist puts it, “we treat boxes as if they were unit squares, and rely on the extra
margin of size to convert equations into inequalities as needed.”
This converts a closed-condition problem into an open-condition one and removes
degenerate boundary cases.

**Unavoidable point sets.** The core idea:

> Find a set `P` of points inside the container `S` such that **every** box placed
> inside `S` must contain at least one point of `P`. Such a `P` is called *unavoidable*.
> If `|P| = n − 1`, then `n` non-overlapping boxes are impossible: by pigeonhole two
> boxes would have to contain the same point, contradicting non-overlap.

**Theorem 2 is a two-stage argument, not a single pigeonhole.** This is worth setting
out exactly, because the simplified version — “ten unavoidable points, eleven boxes,
done” — misses the device that carries the proof.

*Stage one.* Stromquist places **ten** points in the square of side `2 + 2√(4/5)`. Four
sit at `(1, 1)`, `(s/2, 1)`, `(3/2 − s/4, s/2)` and `(1/2 + s/4, s/2)`; the rest are
placed symmetrically.
The vertical distance between the rows is `s/2 − 1 = √(4/5) ≈ 0.894`, and the triangles
in the construction are congruent with sloping sides of length exactly 1. These ten
points are **not** an unavoidable set, and the paper says so: “Nonavoidance lemmas apply
to all of the regions shown *except for the rectangles at the top and bottom*.” A box
can evade all ten, but only by sitting in one of those two rectangles.

*Stage two.* A second configuration of **twelve** points is introduced, chosen so that
the escaping box — pinned to the top or bottom rectangle up to symmetry, by Lemmas 4 and
6 — must contain **all three** of the points marked `A`:

```
A = { (1, .9),  (s/2, .9) ≈ (1.894, .9),  (1 + √(1/5), 1.12) ≈ (1.447, 1.12) }
```

Nonavoidance lemmas cover every region of that second figure, so the twelve points *are*
unavoidable. One box swallowing three of them leaves nine points for the remaining ten
boxes, and the pigeonhole closes: “Since three of the twelve points are in one box,
there cannot be eleven nonintersecting boxes.”

**Theorem 3 has exactly the same shape** — ten points as in the first figure but at the
new `s`, the 45°-strengthened Lemma 7 forcing an escaping box into a known position, and
then twelve points of which one box must contain three ("Again these 12 points form an
unavoidable set in the context of 45° packings, and since three of them are in one
box…"). The `A`-points move to `(1, s−3)`, `(s/2, s−3)`, `(1.5, 1.3)`.

**Why the correction matters.** The three-points-in-one-box step is a *threshold*
certificate: a box is charged **three** units of resource rather than one.
That is already a departure from plain hitting-set counting, and it means the
resource-starvation generalisation catalogued below — weighted points, sliding points,
measured segments, continuously varying families — does not begin with **[Bentz 2010]**.
It is present, in a discrete form, in the 2003 proof that defines the field’s frontier
for `n = 11`. Stromquist also notes the second figure is *robust*: “any point in the
figure could be moved by a small amount in almost any direction without causing the
argument to fail. The critical distances are all in [the first figure]” — i.e. the
binding constraints are the stage-one geometry, and stage two has slack.
(All quotations and coordinates here are from the archived transcription of
**[Stromquist 2003]**, checked against its raw extraction.)

**Nonavoidance lemmas.** Proving that a candidate set is genuinely unavoidable requires
geometric lemmas of the form “if the *center* of a box lies in region `R`, the box must
intersect a specified part of `∂R`.” Stromquist presents six such lemmas (Lemmas 1–6),
of which Lemmas 1–3 are taken from Friedman’s survey, plus two further lemmas (7 and 8)
specific to the 45° analysis.
Representative statements:

- **Lemma 1.** For `a ≤ 1` and `b ≤ 1`, any box whose center is in the rectangle
  `[0,a] × [0,b]` must intersect the x-axis, the y-axis, or the point `(a,b)`.
- **Lemma 2.** If `T` is a triangle with all sides of length at most 1, any box whose
  center is in the interior of `T` must contain one of the vertices of `T`.
- **Lemma 5.** A specialized statement about the pentagon with vertices `(1,0)`,
  `(1,1)`, `(2,1)`, `(2.12,0.9)`, `(2.12,0)`, needed for the `n = 10` argument.

**A source-table correction.** Stromquist’s middle numerical row for Lemma 4 chooses the
smaller root of a cubic obtained after squaring the stationarity equation.
At `a = √(4/5)`, that root gives `θ ≈ 24.0788°` but violates the unsquared sign
condition `cos θ ≤ a`. The true minimum is at `θ ≈ 31.45595°`, with
`f(a) ≈ 0.9145377886`, rather than the printed `.926`. Theorem 2 still goes through
because its application needs only `.9 < f(a)`.

The 45°-restricted case (Theorem 3) exploits the fact that the projections of a 45° unit
vector are at most 1, which brings the triangle lemmas into play in a stronger form
(Lemmas 7 and 8); its counting stage is the same twelve-point, three-points-in-one-box
argument described above.

**Why this method has a ceiling.** The unavoidable points are placed at coordinates
built from the container side `s` and from unit distances — that is, from rational
functions of `s` and square roots.
The bound one can prove is therefore naturally an algebraic number of low degree.
Both proved constants in this paper — `3 + ½√2` and `2 + 4/√5` — are degree-2 algebraic
numbers. The conjectured `s(11)` is degree **8** (verified above).
There is no evident way for a finite unavoidable-point configuration with low-degree
coordinates to certify a degree-8 threshold.
This is, in our assessment, the structural reason the method stalls well short of
`3.877084`, and it is the single most useful insight in this document.

#### The unifying abstraction: resource starvation

Reading the primary papers rather than their summaries reveals that the field already
has a general name for what all its lower-bound proofs are doing.
**[Bentz 2016]** states it plainly:

> Optimality proofs for square packing utilize arguments based on *resource starvation*.
> Subsets of a containing square are associated with numerical resources in such a way
> that each packed box uses up a certain amount of resources (by intersecting the subset
> corresponding with the resource).
> The overall amount of resource available limits the number of boxes that can be
> packed.

This is the correct level of generality, and it organises the whole inventory.
A lower-bound proof chooses a **resource measure** on the container and shows each box
must consume a fixed quantum of it:

| Resource | Quantum per box | Where used |
| --- | --- | --- |
| A finite point set, each point worth 1 | 1 point | The classical unavoidable-points method: **[Friedman DS7]**, **[Stromquist 2003]** |
| A point set with one **sliding point** on a segment | 1 point, for every placement of the slider | **[Bentz 2010]** |
| **Line segments, measured by length of intersection** | A minimum intersection length | **[Bentz 2010]**, Corollary 7 |
| **Weighted points, segments, and a rectangular area combined** | A weighted quantum | A “more complex configuration” cited by **[Bentz 2016]** |
| A **continuously varying family** of point sets | 1 point, uniformly along the family | **[Bentz 2016]**, Theorem 8 |

The progression is a steady weakening of the discreteness assumption, and it matters for
the transversal reading below: the field has *already* moved from counting points to
measuring lengths.
**[Bentz 2010]**'s Corollary 7 is a genuinely fractional statement — a
box whose centre lies in a certain rectangle without containing its vertices must
intersect two specified segments with total intersection length at least
`2√2 − 2 ≈ 0.828`. That is a measure-valued transversal condition, not a hitting-set
condition.

**The ε-shrinking step.** **[Friedman DS7]** gives the precise mechanism by which an
unavoidable set yields a bound, and it is worth quoting because it is where compactness
enters:

> To show that `s(n) ≥ k`, we will find a set `P` of `(n−1)` points in a square `S` of
> side `k` so that any unit square in `S` contains an element of `P` (possibly on its
> boundary). Shrinking these by a factor of `(1 − ε/k)` gives a set `P'` of `(n−1)`
> points in a square `S'` of side `(k − ε)` …

The rescaling converts a statement about the closed container into one about every
slightly smaller container, which is exactly what forces `s(n) ≥ k` rather than
`s(n) > k − ε` for each `ε` separately.

#### Kearney–Shiu’s duality, precisely

**[Kearney–Shiu 2002]** is the one genuinely different idea in the lower-bound
literature, and the mechanism is elegant enough to record exactly.

Their proof of `s(6) = 3` and `s(7) = 3` starts from a 7-point unavoidable set in the
square of side 3 — essentially Friedman’s, whose own `s(7) = 3` proof needed a more
complicated “almost unavoidable set” of 5 points.
Then:

1. Colour those 7 points **green**; call it the green lattice in `S`.
2. Rotate the lattice a **right angle** about the centre `(3/2, 3/2)`, giving 7 **red**
   points.
3. Because `S` is a *square*, the rotated configuration is also unavoidable.
   The red lattice is therefore the **dual** of the green one.
4. The two lattices share the centre, so their union has **13 distinct points**, in
   three classes: the centre (the **C-point**, which is both green and red), the **8
   A-points** furthest from it, and the **4 B-points** at distance `1/2` from it.
   Each lattice is thus four A-points, two B-points and the C-point.
5. Any unit square covering the C-point must also cover a point of the other colour; the
   case analysis closes from there.

The move is to exploit the container’s own symmetry group to manufacture a second
certificate for free, then reason about the *interaction* of the two.
It is a genuinely different lever from placing better points, and it is the only place
in this literature where symmetry is used as a proof engine rather than merely to reduce
cases.

Kearney and Shiu also prove constructive results in the other direction, by applying
simultaneous Diophantine approximation to their construction.
With `δ_n` defined by `s(n² + 1) ≤ n + δ_n` and `n_r` the smallest `n` such that
`δ_n ≤ 1/r`, they prove

```
n_r ≤ p(⌈τ⌉) ≤ p(⌈3r/2⌉) = 27r³/2 + O(r²),   where p(t) = 4t³ + 4t² + 3t + 1
```

— *cubic* in `r`, not `r^{3/2}` (an earlier draft of this document misread the displayed
fraction). They give `4 ≤ n₂ ≤ 43`, and by the same ideas `n₃ ≤ 239`, `n₄ ≤ 625`,
`n₅ ≤ 1320`, `n₆ ≤ 2493`, `n₇ ≤ 4072`; for large `r` Erdős–Graham gives the stronger
`n_r ≪ r^{11/4}`. They also show `δ₈ < 0.536`, `δ₄₂ < 0.507` and `δ₄₃ < 1/2`, and remark
that improving either bound “represents an interesting challenge”.

### The landscape of solved cases

Exact values of `s(n)` known as of this research:

| `n` | `s(n)` | Attribution |
| --- | --- | --- |
| perfect squares `m²` | `m` | Trivial |
| 1 | 1 | Trivial |
| 2, 3, 4 | 2 | Classical |
| **5** | `2 + ½√2 ≈ 2.707107` | Göbel, via **[Friedman DS7]** |
| 6 | 3 | **[Kearney–Shiu 2002]** — first *published* proof (see the priority ledger below) |
| 7, 8 | 3 | **[El Moumni 1999]** — earliest published proof; also **[Friedman DS7]**, **[Kearney–Shiu 2002]** |
| 9 | 3 | Trivial (`3²`) |
| **10** | `3 + ½√2 ≈ 3.707107` | **[Stromquist 2003]**, Thm 1 |
| **11** | **OPEN** — in `[3.788854, 3.877084]` | — |
| 13 | 4 | **[Bentz 2010]** |
| 22 | 5 | **[Bentz 2016]** |
| 33 | 6 | **[Bentz 2016]** |
| 46 | 7 | **[Bentz 2010]** |

General families:

- **Nagamochi (2005):** `s(m² − 1) = s(m² − 2) = m` for `m ≥ 2`. **Retrieved and read**;
  the paper is open access in the *Electronic Journal of Combinatorics* (an earlier pass
  of this research recorded it as unlocated, which was wrong).
  It is titled *Packing Unit Squares in a Rectangle*, and the square-container result is
  a corollary of a rectangle theorem — see the general bound immediately below.
- **`s(m² − 3) = m`** established for `m = 3, 4, 7`, extended by Bentz to `m = 5, 6`
  (via `s(22) = 5` and `s(33) = 6`), supporting the conjecture that it holds for all
  `m ≥ 3`.

#### Nagamochi’s general lower bound — the only closed-form bound beyond area

Nagamochi’s theorem is stated for rectangles, and it is the one general-purpose lower
bound in this literature that applies to every `N` without a bespoke construction.
For real `a, b ≥ 2`, no more than

```
ab − (a + 1 − ⌈a⌉) − (b + 1 − ⌈b⌉)
```

unit squares can be packed in any `a′ × b′` rectangle with `a′ < a` and `b′ < b`. From
this he deduces that for any integer `N ≥ 4`,

```
s(N) ≥ min{ ⌈√N⌉,  √(N − 2⌊√N⌋ + 1) + 1 }
```

and in particular `s(n²) = s(n² − 1) = s(n² − 2) = n` for every `n ≥ 2`.

For `n = 11` this gives `min{4, √6 + 1} ≈ 3.449`, which is **weaker than Stromquist’s
`3.7889`** and so changes nothing for the headline case.
Its value is elsewhere: for most open `n` it is the best lower bound in print that does
*not* require someone to construct an unavoidable point set by hand, which makes it the
default entry in the [open-frontier table](#the-open-frontier-what-is-actually-unknown)
below. The same paper records a conjecture of Friedman’s worth tracking: once
`s(n² − k) = n` holds for some `n` and `k`, then `s((n+1)² − k) = n + 1`.

#### Priority, claims, and what was actually published

This subject’s history is unusually full of unpublished, lost, and late-surfacing work,
and attributions in secondary sources are correspondingly unreliable.
**[Friedman DS7]** puts it plainly: “The number of claims far outweighs the number of
published results in this area.”
The ledger, as best it can be reconstructed:

| Result | Claimed by | Published proof |
| --- | --- | --- |
| `s(7) = s(8) = 3` | Bajmóczy, per Schrijver, per Göbel (unpublished) | **El Moumni (1999)**, *Studia Sci. Math. Hungar.* 35, 281–290 — unnoticed for years |
| `s(6) = 3` | Stromquist 1984 memoranda; also Trevor Green (2000, private) — neither published | **[Kearney–Shiu 2002]** |
| `s(10) = 3 + ½√2` | Stromquist 1984 memoranda | **[Stromquist 2003]** |
| `s(14) = s(15) = 4`, `s(24) = 5` | Stromquist “claimed to know how to prove” (1984) | **[Friedman DS7]**; `s(15)` also El Moumni (1999) |
| `s(11) = 3.877084…` | conjectured since 1979; never claimed as proved | **none — open** |
| `n = 11` packing | Trump 1979; independently rediscovered many times, incl. Gustafsson–Thulin 1980 | construction only |

Two consequences. First, **El Moumni holds published priority for `s(7) = s(8) = 3` and
`s(15) = 4`**, three years before Kearney–Shiu, and is absent from most summaries of
this field including earlier drafts of this document; Kearney–Shiu’s genuine first is
`s(6) = 3`. Second, Stromquist’s 1984 Daniel H. Wagner Associates memoranda I–III sit
behind a remarkable share of the claim column and have never been published; memorandum
III covers `n ≤ 65` and Gardner’s conjecture for `n = 11`, and remains the single most
valuable unretrieved document in this subject.

Friedman’s survey supplies relatively simple proofs for `n = 2, 3, 5, 8, 15, 24, 35` and
more complicated ones for `n = 7, 14`. Stromquist’s 2003 abstract notes that at that
time, for larger `n`, published proofs of exact values existed “only for
`n = 14, 15, 24, 35`, and when `n` is a square.”

**A structural observation.** Every solved non-trivial case has `s(n)` equal to either
an integer or a degree-2 algebraic number of the form `k + ½√2`. No case with a
higher-degree answer has ever been resolved.
`n = 11` would be the first, and this is likely not a coincidence but a reflection of
the proof technology’s reach.

**`n = 11` is the smallest open case, but not the only small one — `n = 12` is open
too.** This is worth stating because at least one secondary summary asserts `s(12) = 4`
on the bogus ground that “12 squares fit in a 4×4 arrangement”, which establishes only
`s(12) ≤ 4`. The catalogue **[Kingbird]** is unambiguous about proof status: its
`n = 10` entry reads “Proved by Walter Stromquist in 2003”, its `n = 13` entry “Proved
by Wolfram Bentz”, and its **`n = 11` entry carries no proof attribution at all** — only
“Found by Walter Trump in 1979” and “Rigid.”
For `n = 12`, note the direction of implication: since 12 squares are easier to pack
than 13, proving `s(12) = 4` is **strictly stronger** than proving `s(13) = 4`.
`s(13) = 4` is proved; `s(12) = 4` is not, and 12 appears in no published list of
settled cases. So the open region begins at 11 and continues at 12.

**A cautionary counterexample.** It was conjectured that `s(n² − n) = n` for small `n`.
**[Friedman DS7]** records the smallest known counterexample, due to **Lars Cleemann**:
`s(17² − 17) < 17`, i.e. 272 unit squares fit in a square of side 17 with room to spare.
Three of its squares are tilted at 45°, and *the other tilted squares* at `arctan(8/15)`
— most of the 272 remain axis-aligned.
The lesson generalises well beyond that family: plausible patterns in this subject fail
at sizes far beyond where intuition or small-case data would suggest, which is a
standing argument against believing `s(11) = 3.877084…` merely because nothing has
beaten it.

*Note on source discrepancies:* enumerations differ between sources.
Wikipedia lists `n = 2, 3, 5, 6, 7, 8, 10, 13, 14, 15, 24, 34, 35, 46, 47, 48`, omitting
`n = 23`, which Nagamochi’s family supplies from `m = 5`. Other enumerations do include
it: `2, 3, 5, 6, 7, 8, 10, 13, 14, 15, 22, 23, 24, 33, 34, 35`. The union across
sources, plus Nagamochi’s family stated in general form, is the safe reading; `n = 23`
**is** covered by the theorem, and Wikipedia’s omission appears to be an incomplete
enumeration rather than a mathematical subtlety.

### The open frontier: what is actually unknown

The solved cases above are the exceptions.
This table is the complement — **every open `n ≤ 100`** — and it is the spine of any
systematic attack on this problem, because it shows at a glance where the proof
machinery stops and how far short it falls.

Upper bounds are the best known packings from **[Kingbird]**; `grid` in the *how* column
marks an `n` the catalogue does not picture, where the trivial `⌈√n⌉` packing is still
the best known. `deg` is the algebraic degree of the conjectured optimum where the
catalogue records a minimal polynomial.
Lower bounds are the strongest of four sources: the area bound `√n`, Nagamochi’s general
closed form, monotonicity from the largest proved `m ≤ n`, and Stromquist’s Theorem 2
for `n ≥ 11`.

This table and the solved-case table below are **generated** from
[`explorations/packing/frontier/`](../../../frontier/README.md), where the same facts
live as one schema-validated artifact per `n` with provenance, links into the local
archive, and an editorial note on each case.
The duplication is deliberate — this report should be readable end to end without
opening the data — and it is safe because the tables are rendered by
`tools/render_tables.py`, which `test.sh` re-checks.
Use the structured form to query or plot; use these tables to read.

<!-- BEGIN GENERATED: frontier-open (tools/render_tables.py) -->

| `n` | best known `s(n)` | how | deg | best proved lower bound | from | gap |
| --- | --- | --- | --- | --- | --- | --- |
| 11 | 3.87708359 | hand | 8 | 3.788854 | unavoidable points | 0.0882 |
| 12 | 4 | grid | — | 3.788854 | monotone from `s(11)` | 0.2111 |
| 17 | 4.67553009 | hand | 18 | 4.162278 | Nagamochi | 0.5133 |
| 18 | `(7/2) + (1/2)√7` = 4.82287566 | hand | — | 4.316625 | Nagamochi | 0.5063 |
| 19 | `3 + (4/3)√2` = 4.88561808 | hand | — | 4.464102 | Nagamochi | 0.4215 |
| 20 | 5 | grid | — | 4.605551 | Nagamochi | 0.3944 |
| 21 | 5 | grid | — | 4.741657 | Nagamochi | 0.2583 |
| 26 | `(7/2) + (3/2)√2` = 5.62132034 | extension | — | 5.123106 | Nagamochi | 0.4982 |
| 27 | `5 + (1/2)√2` = 5.70710678 | strip | — | 5.242641 | Nagamochi | 0.4645 |
| 28 | 5.82444462 | annealing | 6 | 5.358899 | Nagamochi | 0.4655 |
| 29 | 5.93383346 | annealing | — | 5.472136 | Nagamochi | 0.4617 |
| 30 | 6 | grid | — | 5.582576 | Nagamochi | 0.4174 |
| 31 | 6 | grid | — | 5.690416 | Nagamochi | 0.3096 |
| 32 | 6 | grid | — | 5.795832 | Nagamochi | 0.2042 |
| 37 | 6.59861961 | hand | 8 | 6.09902 | Nagamochi | 0.4996 |
| 38 | `6 + (1/2)√2` = 6.70710678 | strip | — | 6.196152 | Nagamochi | 0.511 |
| 39 | 6.81072208 | annealing | 5 | 6.291503 | Nagamochi | 0.5192 |
| 40 | `4 + 2 √2` = 6.82842712 | hand | — | 6.385165 | Nagamochi | 0.4433 |
| 41 | 6.92669309 | annealing | 42 | 6.477226 | Nagamochi | 0.4495 |
| 42 | 7 | grid | — | 6.567764 | Nagamochi | 0.4322 |
| 43 | 7 | grid | — | 6.656854 | Nagamochi | 0.3431 |
| 44 | 7 | grid | — | 6.744563 | Nagamochi | 0.2554 |
| 45 | 7 | grid | — | 6.830952 | Nagamochi | 0.169 |
| 50 | `7 + (4/7)` = 7.57142857 | annealing | — | 7.082763 | Nagamochi | 0.4887 |
| 51 | 7.70079924 | annealing | 12 | 7.164414 | Nagamochi | 0.5364 |
| 52 | `7 + (1/2)√2` = 7.70710678 | strip | — | 7.244998 | Nagamochi | 0.4621 |
| 53 | `(13/2) + (1/2)√7` = 7.82287566 | annealing | — | 7.324555 | Nagamochi | 0.4983 |
| 54 | 7.84666719 | hand | — | 7.403124 | Nagamochi | 0.4435 |
| 55 | 7.94577101 | annealing | — | 7.480741 | Nagamochi | 0.465 |
| 56 | 8 | grid | — | 7.557439 | Nagamochi | 0.4426 |
| 57 | 8 | grid | — | 7.63325 | Nagamochi | 0.3668 |
| 58 | 8 | grid | — | 7.708204 | Nagamochi | 0.2918 |
| 59 | 8 | grid | — | 7.78233 | Nagamochi | 0.2177 |
| 60 | 8 | grid | — | 7.855655 | Nagamochi | 0.1443 |
| 61 | 8 | grid | — | 7.928203 | Nagamochi | 0.0718 |
| 65 | `5 + (5/2)√2` = 8.53553391 | hand | — | 8.071068 | Nagamochi | 0.4645 |
| 66 | `3 + 4 √2` = 8.65685425 | hand | — | 8.141428 | Nagamochi | 0.5154 |
| 67 | `8 + (1/2)√2` = 8.70710678 | strip | — | 8.211103 | Nagamochi | 0.496 |
| 68 | 8.80338307 | — | — | 8.28011 | Nagamochi | 0.5233 |
| 69 | 8.82720551 | — | — | 8.348469 | Nagamochi | 0.4787 |
| 70 | 8.88166676 | hand | 4 | 8.416198 | Nagamochi | 0.4655 |
| 71 | 8.94407156 | annealing | — | 8.483315 | Nagamochi | 0.4608 |
| 72 | 9 | grid | — | 8.549834 | Nagamochi | 0.4502 |
| 73 | 9 | grid | — | 8.615773 | Nagamochi | 0.3842 |
| 74 | 9 | grid | — | 8.681146 | Nagamochi | 0.3189 |
| 75 | 9 | grid | — | 8.745967 | Nagamochi | 0.254 |
| 76 | 9 | grid | — | 8.81025 | Nagamochi | 0.1898 |
| 77 | 9 | grid | — | 8.874008 | Nagamochi | 0.126 |
| 78 | 9 | grid | — | 8.937254 | Nagamochi | 0.0627 |
| 82 | `6 + (5/2)√2` = 9.53553391 | hand | — | 9.062258 | Nagamochi | 0.4733 |
| 83 | 9.63482562 | extension | 24 | 9.124038 | Nagamochi | 0.5108 |
| 84 | `9 + (1/2)√2` = 9.70710678 | strip | — | 9.185353 | Nagamochi | 0.5218 |
| 85 | `(11/2) + 3 √2` = 9.74264069 | hand | — | 9.246211 | Nagamochi | 0.4964 |
| 86 | `(17/2) + (1/2)√7` = 9.82287566 | extension | — | 9.306624 | Nagamochi | 0.5163 |
| 87 | 9.83881744 | annealing | 44 | 9.3666 | Nagamochi | 0.4722 |
| 88 | 9.88815305 | hand | 20 | 9.42615 | Nagamochi | 0.462 |
| 89 | `5 + (7/2)√2` = 9.94974747 | hand | — | 9.485281 | Nagamochi | 0.4645 |
| 90 | 10 | grid | — | 9.544004 | Nagamochi | 0.456 |
| 91 | 10 | grid | — | 9.602325 | Nagamochi | 0.3977 |
| 92 | 10 | grid | — | 9.660254 | Nagamochi | 0.3397 |
| 93 | 10 | grid | — | 9.717798 | Nagamochi | 0.2822 |
| 94 | 10 | grid | — | 9.774964 | Nagamochi | 0.225 |
| 95 | 10 | grid | — | 9.831761 | Nagamochi | 0.1682 |
| 96 | 10 | grid | — | 9.888194 | Nagamochi | 0.1118 |
| 97 | 10 | grid | — | 9.944272 | Nagamochi | 0.0557 |

<!-- END GENERATED: frontier-open -->

**The solved cases, for contrast.**

<!-- BEGIN GENERATED: frontier-solved (tools/render_tables.py) -->

| `n` | `s(n)` | established by | source |
| --- | --- | --- | --- |
| 1 | `1` | perfect square | classical |
| 2 | `2` | elementary | classical |
| 3 | `2` | elementary | classical |
| 4 | `2` | perfect square | classical |
| 5 | `2 + (1/2)√2` | unavoidable points | Frits Göbel (1979) |
| 6 | `3` | unavoidable points | Michael Kearney, Peter Shiu (2002) |
| 7 | `3` | unavoidable points | Said El Moumni (1999) |
| 8 | `3` | unavoidable points | Said El Moumni (1999) |
| 9 | `3` | perfect square | classical |
| 10 | `3 + (1/2)√2` | unavoidable points | Walter Stromquist (2003) |
| 13 | `4` | unavoidable points | Wolfram Bentz (2010) |
| 14 | `4` | unavoidable points | Erich Friedman (2009) |
| 15 | `4` | unavoidable points | Said El Moumni (1999) |
| 16 | `4` | perfect square | classical |
| 22 | `5` | unavoidable points | Wolfram Bentz (2016) |
| 23 | `5` | Nagamochi | Hiroshi Nagamochi (2005) |
| 24 | `5` | unavoidable points | Erich Friedman (1999) |
| 25 | `5` | perfect square | classical |
| 33 | `6` | unavoidable points | Wolfram Bentz (2016) |
| 34 | `6` | Nagamochi | Hiroshi Nagamochi (2005) |
| 35 | `6` | unavoidable points | Erich Friedman (1999) |
| 36 | `6` | perfect square | classical |
| 46 | `7` | unavoidable points | Wolfram Bentz (2010) |
| 47 | `7` | Nagamochi | Hiroshi Nagamochi (2005) |
| 48 | `7` | Nagamochi | Hiroshi Nagamochi (2005) |
| 49 | `7` | perfect square | classical |
| 62 | `8` | Nagamochi | Hiroshi Nagamochi (2005) |
| 63 | `8` | Nagamochi | Hiroshi Nagamochi (2005) |
| 64 | `8` | perfect square | classical |
| 79 | `9` | Nagamochi | Hiroshi Nagamochi (2005) |
| 80 | `9` | Nagamochi | Hiroshi Nagamochi (2005) |
| 81 | `9` | perfect square | classical |
| 98 | `10` | Nagamochi | Hiroshi Nagamochi (2005) |
| 99 | `10` | Nagamochi | Hiroshi Nagamochi (2005) |
| 100 | `10` | perfect square | classical |

<!-- END GENERATED: frontier-solved -->

**What the table says.** Five things, none of them visible from the list of solved cases
alone.

1. **`n = 11` has the smallest gap of any case with a non-trivial record — but not the
   smallest gap outright.** At `0.0882` it is far ahead of the next such case, `n = 19`
   at `0.4215`, nearly five times wider.
   Three cases *do* have smaller gaps: `n = 97` (`0.0557`), `n = 78` (`0.0627`) and
   `n = 61` (`0.0718`), all still held by the trivial grid with Nagamochi’s bound nearly
   tight. An earlier hand-written version of this table claimed `n = 11` was the smallest
   outright; generating the data corrected it.
   Those three are `10² − 3`, `9² − 3` and `8² − 3` — **consecutive unproved members of
   the family `s(m² − 3) = m`**, which is proved exactly for `m = 3, 4, 5, 6, 7`. Their
   conjectured optima are integers, their gaps are the narrowest in the table, and they
   are essentially undiscussed.
   On this evidence they, not `n = 11`, are the most tractable unproved cases at
   `n ≤ 100`.
2. **Nagamochi’s bound is doing nearly all the work.** For 63 of the 65 open cases it is
   the best lower bound in print.
   Only `n = 11` and `n = 12` are governed by a bespoke argument — Stromquist’s — and
   that argument has never been extended.
   The lower-bound frontier is, almost everywhere, a *general* theorem that nobody has
   improved on in twenty years.
3. **`n = 12` is the worst-served small case.** Its best proved lower bound is
   Stromquist’s `s(11)` bound inherited by monotonicity; nothing specific to 12 has ever
   been proved, leaving a gap of `0.2111` against the trivial grid packing.
   Note the direction of implication: since 12 squares are easier to pack than 13, and
   `s(13) = 4` *is* proved, proving `s(12) = 4` is **strictly stronger** than the
   published Bentz result.
4. **Algebraic degree explodes immediately past 11.** `s(11)` is degree 8; `s(17)` is
   degree 18. Every *solved* case is degree ≤ 2. Whatever certifies these values will
   not be an unavoidable point set with coordinates built from unit distances.
5. **The grid is still the record for 31 of the 65 open cases**, in ranges where no
   tilted construction has ever been found to beat it.
   These are where a modern search program has the most obvious room to contribute — and
   also where a *proof* is most plausibly within reach of the existing technique,
   because the conjectured optimum is an **integer**.

Point 5 is the practical one: if the object is to prove something new rather than to
find something new, the targets are the open cases with integer conjectured optima, not
`n = 11`.

#### `n = 12` to `n = 16`: the next targets after 11

The five cases immediately above `n = 11` deserve separate treatment, because they are
where a realistic proof attempt would start and they are consistently skipped in
summaries that stop at “11 is the first open case.”

| `n` | best known | conjectured optimum | proved? | why it is interesting |
| --- | --- | --- | --- | --- |
| 12 | `4` (grid) | integer `4` | **open** | Strictly stronger than the proved `s(13) = 4`; no bespoke bound exists |
| 13 | `4` | integer `4` | **proved** — **[Bentz 2010]** | The template: an integer optimum reached by continuously varying families |
| 14 | `4` | integer `4` | **proved** — **[Friedman DS7]** | Almost-unavoidable sets plus a 5-case enumeration |
| 15 | `4` | integer `4` | **proved** — **[El Moumni 1999]**, **[Friedman DS7]** | Also covered by Nagamochi (`4² − 1`) |
| 16 | `4` | integer `4` | **proved** (perfect square) | Trivial |

The striking feature is that **`n = 12` is the only open case in this range**, it is
surrounded on both sides by proved values of exactly `4`, and its own optimum is
near-certainly `4` as well.
It is the closest thing this subject has to low-hanging fruit, and the reason it is
unpicked is instructive: 13 is *easier* to prove than 12, because a lower-bound argument
must exclude packings of `n` squares, and excluding 12 squares from a side-4 container
is a strictly stronger statement than excluding 13. The unavoidable-point method’s
difficulty scales with how *few* squares must be excluded, which inverts the usual
intuition that small `n` is easy.

For a computational proof effort, `n = 12` is therefore the recommended first target: an
integer optimum (so no high-degree algebraic threshold is needed, which is the specific
obstruction at `n = 11`), a container of modest size, and a result that would be the
first new proved value of `s(n)` since 2018.

### Catalogue of search strategies for finding packings (upper bounds)

Every entry in the record tables is a **construction**. No upper bound in this subject
has ever been obtained non-constructively: to show `s(n) ≤ a` somebody must exhibit a
packing. The strategies below are ordered roughly from human to machine, and the table
records which are known to have produced records.

<!-- BEGIN GENERATED: search-strategies (tools/render_tables.py) -->

| # | Strategy | Family | Mechanism | Produced records? |
| --- | --- | --- | --- | --- |
| 1 | Axis-aligned grid | constructive | The `⌈√n⌉` trivial packing | Yes — optimal for perfect squares and the general `m²−1`, `m²−2` families; `m²−3` is proved only for `m = 3, 4, 5, 6, 7` |
| 2 | Hand geometric insight | constructive | Human construction, often on paper | Yes — Trump `n=11`, Göbel, Hämäläinen, Bidwell `n=17` |
| 3 | 45° tilted families | constructive | A block of squares rotated a half-turn diagonal | Yes — `n=5`, `n=10` |
| 4 | Diagonal strips of width `k` | constructive | A tilted band crossing the container, corners filled | Yes — Stenlund `n=66` (width-3 strip) |
| 5 | Strip + “L” augmentation | constructive | Extend a strip packing with an L-shaped border block | Yes — best known `n=83` from the `n=66` strip |
| 6 | Rational-slope tilts | constructive | Tilts at `arctan(p/q)` making contacts commensurate | Yes — e.g. `arctan(8/15)`, `arcsin((√7−1)/4)` for `n=18` |
| 7 | Composition / self-similarity | constructive | Combine copies of a smaller good packing | Yes — Ellsworth Dec 2025 joined two `s(50)` copies for `s = 13 + 4/7` |
| 8 | Parametric families for structured `n` | constructive | Formulas for `n = m²−k`, `n = m²−m`, `n(n−1)` | Yes — Arslanov et al. on `n(n−1)` |
| 9 | Asymptotic border constructions | constructive | Tilt squares near the boundary to absorb fractional waste | Yes — Erdős–Graham and successors, asymptotic only |
| 10 | Simulated annealing | stochastic search | Stochastic perturbation with a cooling schedule | Yes — the current workhorse. Schadt’s program; Ellsworth’s modified version |
| 11 | Billiard / inflation | stochastic search | Grow squares to a jammed state, perturb, repeat | Yes — Gensane–Ryckelynck (`n = 29, 37`; alternative `n = 18`) |
| 12 | Basin hopping / multistart | stochastic search | Many random starts into local optimisation | Standard in packing generally |
| 13 | Nonlinear programming | stochastic search | Continuous variables with pairwise non-overlap constraints | Standard; scales poorly with `n` |
| 14 | SAT / constraint programming | stochastic search | Reduce feasibility at a fixed side to a Boolean or CP instance | Used for 2D orthogonal packing; awkward under free rotation |
| 15 | Branch and bound over contact classes | stochastic search | Enumerate combinatorial structures, optimise within each | Used in exact cutting-and-packing |
| 16 | Genetic / evolutionary search | stochastic search | Population methods over configurations | Used in the wider packing literature |
| 17 | Exact algebraic refinement | exact refinement | Fix the contact graph, solve the polynomial system | How exact values are obtained — see below |
| 18 | Rigidity-guided enumeration | exact refinement | Enumerate rigid contact graphs, then solve each | Standard in sphere/disk packing; the natural analogue here |
| 19 | Interval-verified local optima | exact refinement | Certify a local optimum with interval arithmetic | Used for circle packing; not seen applied to `s(11)` |
| 20 | Catalogue-driven record chasing | workflow | Human-computer loop against a public record table | Yes — how the tables actually advance |

<!-- END GENERATED: search-strategies -->

**On strategy 17, exact algebraic refinement.** This is the step that turns a numerical
packing into a theorem-shaped object, and it is how the degree-8 polynomial for `n = 11`
exists at all. Once a numerical search has converged, the *combinatorial* structure is
read off: which square touches which, and along which edge.
Each contact becomes a polynomial equation in the positions and tilt angles.
If the configuration is **rigid**, the resulting system is zero-dimensional, and
eliminating variables (classically by resultants, in modern practice by a Gröbner basis)
yields a univariate polynomial whose relevant root is the exact side length.
For Trump’s packing that eliminant is the irreducible degree-8 polynomial recorded
above. Note what this gives and does not give: an *exact* value for that contact class,
and no information whatsoever about other contact classes.

**On strategy 10, simulated annealing.** The record tables are, in practice, maintained
by annealing. The activity is current and competitive: David Ellsworth found
`s(131) = 11.95654869347733` in January 2026 using a modified version of Thomas Schadt’s
simulated annealing program, starting from a packing Károly Hajba found in November
2024; `s(156)` was improved by Arslanov, Mustafin and Shangitbayev (2019), then by
Ellsworth (Dec 2024), then Cantrell (Mar 2025), then Ellsworth again (Jan 2026).
Best-known packings are catalogued to `n = 324`.

**The significance for `n = 11`.** Strategies 10, 11, 12 and 13 have all been pointed at
this case, and none has beaten a configuration found by hand in 1979 and refined on a
pocket calculator. That is about as strong as purely empirical evidence gets.
It is also, by construction, evidence that cannot become a proof: a search that fails to
find something better has certified nothing.

### Catalogue of proof strategies for bounds

Lower bounds are where the mathematics lives, and the inventory is strikingly short.
Almost every proved value of `s(n)` rests on one idea — unavoidable point sets — with
successive papers refining rather than replacing it.

<!-- BEGIN GENERATED: proof-strategies (tools/render_tables.py) -->

| # | Strategy | Family | Mechanism | Used on this problem? |
| --- | --- | --- | --- | --- |
| 1 | Area counting | elementary | `s(n) ≥ √n` | Yes — trivially, never tight for non-squares |
| 2 | Unavoidable point sets | unavoidable points | Place `n−1` points every unit square must hit; pigeonhole | Yes — the workhorse for nearly every proved case |
| 3 | Nonavoidance lemmas | unavoidable points | Geometric sublemmas certifying a set is unavoidable | Yes — Friedman’s Lemmas 1–3; Stromquist’s 1–6 |
| 4 | The “box” relaxation | unavoidable points | Use squares of side strictly `>1` so conditions are open | Yes — Stromquist’s framing device |
| 5 | Duality / lattice rotation | unavoidable points | Rotate the unavoidable lattice a quarter turn; colour argument | Yes — Kearney–Shiu, for `s(6) = s(7) = 3` |
| 6 | “Almost unavoidable” sets + forcing | unavoidable points | Force squares into positions, then derive further points | Yes — Friedman, for the harder `n = 7, 14` |
| 7 | Continuously varying families | unavoidable points | Replace a fixed point set by a parametrised family | Yes — Bentz 2016, for `s(22)=5`, `s(33)=6` |
| 8 | Generalised unavoidable points | unavoidable points | Nagamochi’s extension of the method | Yes — `s(m²−1) = s(m²−2) = m` |
| 9 | Restricted-orientation analysis | unavoidable points | Prove a bound for a *subclass* of packings | Yes — Stromquist Thm 3 (0°/45°), settling Gardner |
| 10 | Exhaustive case analysis | unavoidable points | Enumerate combinatorial configurations | Yes — inside most of the above |
| 11 | Symmetry reduction | unavoidable points | Quotient the search by the container’s symmetry group | Yes — standard within case analyses |
| 12 | Area-charging / measure arguments | asymptotic | Assign waste to regions and integrate | Yes — but asymptotically (Roth–Vaughan) |
| 13 | Analytic number theory | asymptotic | Bound waste via `√(x − ⌊x⌋)` behaviour | Yes — Roth–Vaughan, asymptotic only |
| 14 | “Good square” reduction | asymptotic | Show near-axis-aligned squares suffice asymptotically | Yes — asymptotic only (arXiv:2504.09489) |
| 15 | Interval arithmetic + branch and bound | modern machinery | Rigorously exclude all configurations numerically | Yes for circles (n≤33); yes for unit squares with rotation but only n=3 |
| 16 | SOS / Positivstellensatz certificates | modern machinery | Certify semialgebraic infeasibility via SDP | No application to `s(n)` was found in the retrieved corpus |
| 17 | LP/SDP relaxation with dual certificates | modern machinery | Bound via a relaxation’s dual solution | No application to `s(n)` was found in the retrieved corpus |
| 18 | Machine-checked formal proof | modern machinery | Verify a case analysis in Lean/HOL Light/Isabelle | No machine-checked `s(n)` proof was found in the retrieved corpus; adjacent precedents include Flyspeck (2014) and sphere packing in dimension 8 (Feb 2026) |
| 19 | Electrical-network / Kirchhoff methods | dissection tradition | Linear circuit laws on a dissection graph | Not applicable — see below |
| 20 | Graph encodings of dissections (c-nets) | dissection tradition | Enumerate planar graphs of a tiling | Not applicable — dissection-only |
| 21 | Transversal / hitting-set theory | transversal and wider | `τ ≥ ν`; bound the piercing number | Applied explicitly by Bašić–Slivková (2018), who study the piercing number of all unit-square poses in a square, connect it to s(n), and derive a specialized n=61 lower bound. Classical unavoidable-point proofs are the integral special case. |
| 22 | Fractional transversals and LP duality | transversal and wider | Relax piercing to an LP; use the dual fractional packing | No application to `s(n)` was found in the retrieved corpus; this is not an exhaustive negative claim |
| 23 | Integrality-gap bounds (Wegner-type) | transversal and wider | Bound `τ/ν` for families of squares | Bounds exist for squares [Caoduro–Sebő]; no connection to `s(n)` was found in the retrieved corpus |
| 24 | Gallai- and Helly-type theorems | transversal and wider | Structural results forcing small transversals | No application to `s(n)` was found in the retrieved corpus |
| 25 | Delsarte/Cohn–Elkies LP bounds | transversal and wider | Auxiliary functions certifying density bounds | Powerful for lattice sphere packing; no bounded-container `s(n)` analogue was found in the retrieved corpus |
| 26 | SDP hierarchies (Lasserre/de Laat et al.) | transversal and wider | Strengthen LP bounds via moment relaxations | Applied to packing density (arXiv:2001.00256, arXiv:1308.4893); no bounded-container `s(n)` analogue was found in the retrieved corpus |
| 27 | Compactness / limit arguments | transversal and wider | Guarantee the optimum is attained; justify the box device | Yes — foundationally [Martin 2000] |
| 28 | Discharging | transversal and wider | Assign and redistribute local charges | Used in combinatorial geometry; no `s(n)` application was found in the retrieved corpus |
| 29 | Probabilistic method | transversal and wider | Random constructions or averaging | No exact small-`n` application was found in the retrieved corpus |
| 30 | Chromatic / clique-ratio arguments | transversal and wider | Bound `χ/ω` for square intersection graphs | Adjacent [Caoduro–Sebő]; the retrieved result is not a bound on `s(n)` |

<!-- END GENERATED: proof-strategies -->

**The shape of the inventory.** Strategies 2–11 are one family: place points, prove they
are unavoidable, count.
Strategies 12–14 are a separate family that only speaks asymptotically.
Strategies 15–18 are general-purpose modern machinery, of which only 15 has been aimed
at rotating unit squares at all (reaching `n = 3`). Strategies 19–20 belong to a
different problem entirely.
Strategies 21–30 are the wider packing-and-covering toolkit; 21 is the same idea the
field already uses, under a name that connects it to a literature it has never drawn on
— see
[The transversal reformulation](#the-transversal-reformulation-what-the-unavoidable-points-method-really-is).

That is the honest state of the field: one technique does nearly all the work, and it
has not moved on `n = 11` since 2003.

**Why elimination succeeds on the construction but cannot attack the problem.** This is
the sharpest structural point in the catalogue, and it explains an apparent paradox: the
exact value of Trump’s packing falls out of *two* equations, yet the problem is
intractable.

The resolution is that elimination operates **after** the combinatorial structure is
fixed. Trump’s configuration has a known contact graph; imposing it collapses the
configuration space to two free parameters (`s` and `a`), and eliminating one gives a
degree-8 univariate polynomial.
Cheap.

A *proof* must instead quantify over **every** contact structure — including ones nobody
has drawn. Attacking that directly means deciding a semialgebraic formula over the full
configuration space: for eleven squares that is `11 × 3 = 33` variables (a centre and an
angle each) plus the container side, so **34 variables**, under a disjunctive
non-overlap condition for each of the 55 pairs.
Cylindrical algebraic decomposition, the general decision procedure for such formulas,
is **doubly exponential in the number of variables** in the worst case.
At 34 variables that is not a large computation; it is an impossible one.

This is the same wall from a different direction as the `n = 3` ceiling on rigorous
interval methods. Fixing the combinatorics makes the algebra trivial; quantifying over
the combinatorics makes it astronomical.
Every viable proof strategy in this subject is therefore a way of **partitioning the
combinatorial possibilities cheaply** — which is exactly what unavoidable point sets do,
and exactly why the field has one technique.

**Rigidity theory offers the closest structural handle.** In the disk-packing
literature, the space of packings with a *fixed* contact graph is known to be a smooth
manifold (via the Cauchy–Alexandrov stress lemma), and generic-radius packings of `n`
disks admit at most `2n − 3` contacts.
Analogous counting for tilted unit squares would bound how many contact structures are
even candidates for rigidity, which is the natural way to make the combinatorial
enumeration finite and small.
No such enumeration for squares was found.

**Strategy 18 is newly credible.** Formal verification of major packing theorems has
gone from heroic to routine within a decade:

- **Flyspeck (2014)** — Hales and collaborators completed a computer-verified formal
  proof of the **Kepler conjecture** on densest sphere packing in three dimensions,
  using HOL Light and Isabelle, after roughly a decade of effort.
- **Dimension 8 (February 2026)** — a project launched in March 2024 by Hariharan and
  Viazovska formally verified in **Lean** that the `E₈` lattice packing is optimal, with
  the final stages completed by an autoformalization model (arXiv:2604.23468).

Both are packing optimality results with heavy case analysis and interval arithmetic —
structurally the same kind of object an `s(11)` proof would be.
The caveat as first written here was that **formalisation only verifies a proof that
already exists** — neither project discovered its theorem.
That remains true of *those* projects and is **no longer true in general**: AlphaProof
Nexus (arXiv:2605.22763, May 2026) resolved 9 of 353 open Erdős problems and 44 of 492
open OEIS conjectures autonomously, at a few hundred dollars each, by pairing a frontier
model with the Lean compiler in a loop.
The correction matters less than it sounds for `s(11)` specifically — those problems had
short proofs once found — but formal proof search is now a *search* method with a
correctness guarantee attached, not only a transcription method.

For `s(11)` there is still no candidate proof to formalise, so this strategy remains
downstream of a gap nobody has closed.
What *is* available today is the other direction: the **upper bound** is a finite
algebraic statement and could be formalised now, which would be the first formal theorem
about `s(n)` for any non-trivial `n`. See
[Lean for Square-Packing Proofs and Validation](research-2026-08-22-lean-for-packing-proofs-and-validation.md)
for what is reachable when, and for the certificate pattern that makes a result
verifiable by a third party who does not trust our code.

**Strategy 15, revised.** An earlier draft of this document called rigorous interval
branch-and-bound “the most plausible untried line of attack.”
That assessment was wrong, and the correction is the most useful calibration in this
research.

The technique is not untried — it is *developed*, and its ceiling for rotating squares
is brutally low.

- **For circles**, it is mature.
  Markót and collaborators produced computer-assisted optimality proofs for the densest
  packings of equal circles in a square at `n = 28, 29, 30` (roughly 53, 50 and 21 CPU
  hours respectively) and later `n = 31, 32, 33`, using interval branch-and-bound with
  dedicated acceleration.
- **For unit squares with free rotation**, the state of the art is Montanher, Neumaier,
  Markót, Domes and Schichl, “Rigorous packing of unit squares into a circle” (*J.
  Global Optim.*, 2018). They use an interval branch-and-bound framework with
  forward-backward constraint propagation, implemented in C++ over the Filib++ and Moore
  interval libraries. Rotation is handled by giving each square an angle `θ ∈ [0, π/2)`
  and fixing `θ₁ = 0` without loss of generality.
  Non-overlap is handled by a **sentinels** method: nine designated points per square
  are checked for penetration into other squares, reducing the pairwise condition to
  nine non-smooth function evaluations.
- **They rigorously solved `n = 3`.** The result is
  `r₃ ∈ [1.288470508005₄₇, 1.288470508005₅₃]`, obtained on an ordinary laptop.
  They state the method generalises to any number of squares, but the published rigorous
  frontier for *rotating* unit squares is three.

The gap between `n = 3` and `n = 11` is the entire point.
Rotation costs an extra continuous dimension per square *and* turns non-overlap from one
smooth inequality (circles) into a disjunctive condition, and the configuration space
grows accordingly. Eleven squares is not a modest extrapolation from three; it is eight
additional rotational degrees of freedom on top of sixteen positional ones.

So the honest assessment is the reverse of the earlier one: this is the most *developed*
of the modern approaches, it has been aimed at rotating unit squares, and it currently
falls short of `n = 11` by a very large margin.
That makes it a benchmark for how hard rigorous certification of `s(11)` would be,
rather than a promising shortcut.

### The transversal reformulation: what the unavoidable-points method really is

One observation reframes the entire lower-bound literature, and it does not appear to be
made explicitly in the packing sources surveyed here.

**An unavoidable point set is a transversal.** In geometric combinatorics, given a
family `F` of sets, a *transversal* (equivalently a *piercing set* or *hitting set*) is
a set of points meeting every member of `F`. Its minimum size is the **piercing number**
`τ(F)`. The maximum number of pairwise disjoint members is the **packing number**
`ν(F)`. Trivially `τ ≥ ν` [Caoduro–Sebő 2024].

Now take `F` to be the family of *all* unit squares (at all positions and all angles)
contained in a container square `S` of side `a`. Then:

- A set of points that every unit square in `S` must contain is precisely a
  **transversal of `F`**.
- Friedman’s and Stromquist’s “unavoidable set of `n−1` points” is exactly a transversal
  of size `n−1`, witnessing `τ(F) ≤ n−1`.
- The pigeonhole step — `n` disjoint squares would force two to share a point — is
  precisely the inequality `ν(F) ≤ τ(F) ≤ n−1`, hence `ν(F) < n`, hence `s(n) > a`.

So every lower-bound proof in this subject is a **`τ`-upper-bound certificate**, and
`s(n) > a` is the statement `ν < n` for the container of side `a`. The method is not
merely *like* a hitting-set argument; it is one.

**Why the reframing is worth making.** Geometric transversal theory is a substantial
field with its own machinery and its own open problems, and it has apparently never been
pointed at computing `s(n)`:

- **Gallai’s theorem**: for intervals on the line, `τ = ν` exactly.
  The plane is where the gap opens.
- **Wegner’s conjecture (1965)**: for finite families of axis-parallel rectangles,
  `τ ≤ 2ν − 1`. The best general upper bound is `τ = O(ν·(log log ν)²)`
  [Correa–Feuilloley–Pérez-Lantero–Soto].
- **Wegner’s conjecture is false** [Counterexamples 2026]: an explicit triangle-free
  family of 64 rectangles has `ν = 16` and `τ ≥ 32`, and the constant 2 itself fails —
  the LP integrality gap can approach `5/2`, giving `τ ≥ (5/2 − ε)ν`. **Crucially, the
  counterexamples are rectangles; the paper says nothing about squares**, so the square
  case remains open.
- **For squares specifically**, Caoduro and Sebő prove `τ/ν ≤ 6` for unit squares under
  *arbitrary rotation* — the first non-trivial bound for unconstrained orientations —
  and `≤ 10` for varying sizes, with constructions attaining 3 and 4. For axis-parallel
  unit squares the supremum of `τ/ν` is known only to lie in `[3/2, 2]`.

**The catch, stated honestly.** These `τ/ν` results concern *finite* families of squares
given in advance, whereas the packing problem needs the *infinite* family of all unit
squares placeable in `S`. The quantities are not interchangeable, and a `τ/ν` ratio
bound does not directly yield an `s(n)` bound.
What the reframing supplies is not an immediate theorem but a **vocabulary and a body of
technique** — LP relaxations of hitting set, integrality gaps, Helly- and Gallai-type
results, fractional transversals — that the `s(n)` literature has developed
independently and in isolation, one unavoidable point set at a time.

**And the field is already halfway there without saying so.** The resource-starvation
progression above — points worth 1, then sliding points, then *line segments measured by
intersection length* **[Bentz 2010]**, then a combined system of **weighted** points,
segments and a rectangular *area*, then continuously varying families **[Bentz 2016]** —
is precisely a drift from integral transversals toward **fractional, measure-valued**
ones. A system of *weighted* points is a fractional transversal in the most literal
sense: it assigns each point a value in `[0,1]` and requires the total collected by any
box to reach a threshold, which is exactly the LP relaxation `τ*` of the hitting-set
problem. Bentz’s Corollary 7, requiring a minimum total intersection *length* of
`2√2 − 2` rather than a point hit, is a fractional certificate in all but name.
That the field arrived there independently, without the transversal vocabulary, is
suggestive: `τ*` (fractional piercing) is an LP whose dual is a fractional packing, and
LP duality is exactly the kind of certificate this literature currently lacks and keeps
re-deriving by hand.

Whether anything crosses over is untested.
We flag it as the most interesting *conceptual* gap found in this research, distinct
from the most promising *computational* one.

**Where to start, concretely.** The entry points into that literature, for anyone who
wants to test the crossover rather than admire it, are: the **fractional Helly**
theorems and their `(p, q)` consequences; the **Alon–Kleitman** bounded-`τ*/ν`
machinery, which is the canonical route from a fractional transversal bound to an
integral one for families with Helly-type structure; and the LP-duality pairing of `τ*`
with fractional packing, which is the exact certificate shape **[Bentz 2010]**'s
Corollary 7 and **[Bentz 2016]**'s continuously varying families keep re-deriving by
hand.
The obstacle to a direct import is stated above and is real — those results concern
finite families given in advance, and `s(n)` needs the infinite family of all placeable
unit squares — but the infinite family here is *parametrised by a compact
three-manifold* `(x, y, θ)`, which is exactly the setting in which fractional Helly
arguments are usually made to work.

### A foundational point usually skipped: is `s(n)` attained?

Nearly every source writes `s(n)` as “the side of the smallest square into which `n`
unit squares can be packed”, presupposing a minimum rather than an infimum.
The presupposition is correct but not quite free.

The configuration space is compact — `n` centres range over a closed bounded region and
`n` angles over a circle — and the non-overlap condition is closed, so a limit of valid
packings is a valid packing and the infimum is attained.
Compactness results of exactly this type are established in general form by
[Martin 2000], who shows that “for every `ε`” packing statements are equivalent to their
exact counterparts: if a collection packs into every `(1+ε)`-expansion of a compact set,
it packs into the set itself.

This is also the technical reason Stromquist’s **box** device is legitimate.
Defining a box as the interior of a square of side *strictly* greater than 1, and
proving that `n` boxes cannot fit in a container of side exactly `a`, yields `s(n) ≥ a`
precisely because of the limiting argument: were `s(n) < a`, one could inflate a
witnessing packing slightly and obtain `n` boxes in the container.
The device converts closed conditions into open ones, which is what makes the
nonavoidance lemmas usable, and compactness is what makes the conversion sound.

### Computational attacks

**[Gensane–Ryckelynck 2005]** — “Improved Dense Packings of Congruent Squares in a
Square,” *Discrete & Computational Geometry* **34** (2005) 97–109. **Retrieved and read
in full** (Springer serves the PDF openly; an earlier pass of this research recorded it
as paywalled, which was wrong — see [Methodology](#methodology)). They link `sₙ` to the
supremum of the maximal **inflation** `ω(C)` over admissible configurations `C`, and
derive from its properties an algorithm analogous to the *billiard* methods used for
packing congruent disks or spheres in a bounded domain: configurations are perturbed and
inflated until they jam.

**What they actually did at `n = 11`, from the paper itself.** This is the origin of the
persistent “Gensane–Ryckelynck improved `n = 11`” confusion, and with the primary in
hand it can be stated exactly.
Their abstract does claim an improvement — “We improve the best known packings of `n`
equal squares for `n = 11, 29` and `37`” — and §7 explains what that means for 11:

> The best known packing is due to Trump and apparently to many other people.
> In [3] we find that `s₁₁ ≤ 3.8772` for a packing given in Fig.
> 3. We have obtained **this packing** several times with `s₁₁ = 3.87708359…`, a result
> which is slightly better.

So the improvement is to the **recorded numerical bound** — Friedman’s rounded `3.8772`
sharpened to `3.87708359…` — for the **same configuration**, Trump’s, which their figure
reproduces. No denser arrangement was found.
Both readings in circulation are therefore half-right, and the resolution is that
“improved the packing” and “improved the published number for the packing” were
conflated somewhere downstream.

**Their exact solution.** They also computed the algebraic characterization, by
“eliminating with Maple a system of **14 polynomial equations**” whose unknowns are the
square side, `z = cos θ`, `z' = sin θ`, the coordinates `(aᵢ, bᵢ)` of the five tilted
squares, and `α > 0`, the distance between the two upper detached squares.
The result they publish is the cosine of the angle `θ` of the five central squares, as a
real root `z₀` of a polynomial *irreducible over* `ℚ(√2)`:

```
80z⁸ − 128√2·z⁷ − 32z⁶ + 144√2·z⁵ + 72z⁴ − 112√2·z³ + 40z² − 12√2·z − 7
```

*Verified in this research:* this polynomial has exactly two real roots, and the
relevant one is

```
z₀ = 0.99646642997738577107…,   arccos z₀ = 4.81806270967028353…°
```

which is exactly `45° − 40.1819372903297164652…°`. **Their `θ` is the complement of the
standard tilt angle against the diagonal**, so the paper reports `cos(45° − a)` where
the catalogues report `a ≈ 40.182°`. That offset, plus a normalization in which their
`s` is the *side of the small squares* inside a container `[−L, L]²` (with `s = c√2` for
`c` the half-diagonal) rather than the container side for unit squares, is why the
published formula does not look like a formula for `s(11)` and cannot be read off as
one. It is the same packing and the same algebraic number, in a different frame.

Two further details worth recording.
Their “crucial relation”, obtained from the distance between two dashed sides of their
figure, is a compact expression of the form `s = √2·4z/(2 + 5z − z')` as printed; the
displayed fraction does not survive PDF extraction unambiguously and the reconstruction
above does not reproduce `s(11)` under any normalization tried here, so **it should be
read from the PDF before being relied on** — the polynomial and the angle, which are
verified above, are the load-bearing results.
And at `n = 17` they report `s₁₇ = 4.6755300960455` from a four-equation degree-7 system
in `cos θ₁, cos θ₂, sin θ₁, sin θ₂`, remarking that Friedman’s rounded `4.6755` “seems
to be false”; the current catalogue value is `4.67553009360455…`, so the two agree only
to nine decimals and one of the two transcriptions carries a slip.

**Consistency with the record.** Nothing was retracted, every catalogue continues to
attribute `n = 11` to Trump 1979, and in **February 2023** Thierry Gensane confirmed by
correspondence that their program **could not** improve the 1979 packing — consistent
with §7, which describes recovering it rather than beating it.
The `explainxkcd` annotation’s “discovered by Walter Trump in 1979 and refined by
Gensane et al. in 2004” is, read carefully, correct: *refined*, not replaced.

**A 2023 note.** A document titled “Packing of 11 unit squares in a square with minimum
size” was posted (ResearchGate, March 2023; author almost certainly Walter Trump, whose
ResearchGate profile hosts it).
Accessible excerpts state that the packing is “exactly defined by vertices of unit
squares laying on edges of other unit squares or the large square, making the
geometrical object absolutely rigid,” and that the 1979 packing “cannot be improved by
computer programs as long as the same geometrical arrangement of the unit squares is
used.” The full text was not retrievable (403). Note the important qualifier — *as long
as the same arrangement is used* — which is a statement about local, not global,
optimality.

**Interpretation.** Nearly fifty years of search, including modern global-optimization
methods, has failed to beat a configuration found by hand on a pocket calculator in
1979\. This is strong empirical evidence that Trump’s packing is optimal, and
correspondingly weak evidence about how to *prove* it.

### The squared-square tradition: Kirchhoff, Tutte, and why the method does not transfer

There is a second, older, and far more successful body of work on “squares in squares”
which is frequently — and understandably — mistaken for this one.
It deserves a careful treatment here both because its machinery is genuinely beautiful
and because the temptation to import it is strong.

#### What the Trinity Four actually did

In the 1930s four Cambridge undergraduates — R. L. Brooks, C. A. B. Smith, A. H. Stone
and W. T. Tutte — attacked the problem of **dissecting** a rectangle into squares of
*distinct* sizes with *no gaps* (a “perfect” squared rectangle).
Their 1940 paper, “The dissection of rectangles into squares” (*Duke Math.
J.* **7**, 312–340), reformulated the geometry as an electrical network, via what is now
called a **Smith diagram**.

The correspondence, verified against **[squaring.net BSST]**, is exact:

| Circuit object | Geometric object |
| --- | --- |
| Node / terminal | A maximal horizontal line segment in the dissection |
| Wire / edge | A component square, joining the node of its top edge to that of its bottom edge |
| Current magnitude | The side length of that square |
| Potential difference across the wire | The height of that square (equal to its side) |
| Potential difference between the poles | The vertical side of the whole rectangle |
| Resistance | Unit (1 ohm) on every wire |
| Kirchhoff’s current law at a node | Total width of squares resting on a seam equals total width hanging beneath it |
| Kirchhoff’s voltage law around a circuit | Net change in level around any closed path is zero |

With unit resistance, Ohm’s law `V = IR` collapses to `V = I` — voltage equals current —
which is precisely the statement that height equals width, i.e. that the tile is a
*square* rather than a rectangle.
That is the pivot of the whole construction.
Solving the resulting linear system by matrix algebra yields the currents, hence the
side lengths; because the system is linear with rational coefficients, the solution is
**always rational**, and clearing denominators produces integer squared rectangles.

So the account given to you is accurate on the mechanism.
Two historical refinements are worth recording:

- **Priority for the first perfect squared *square* belongs to Roland Sprague, not the
  Trinity Four** **[squaring.net Sprague]**. Sprague, in Berlin, assembled perfect
  rectangles (including Moroń’s 33×32 and 65×47) into an order-55 compound squared
  square of side 4205, published in 1939 — before Brooks, Smith, Stone and Tutte
  published theirs. The Cambridge group built the *theory*; Sprague got the first square
  into print.
- The lowest-order simple perfect squared square is **order 21, side 112**, found by A.
  J. W. Duijvestijn on 22 March 1978 by computer search over c-nets, and it is unique.

#### Why it cannot be carried over to `s(11)`

The method has three structural prerequisites, and the 11-unit-squares problem violates
all three.

1. **It requires a gapless tiling.** Nodes are *maximal horizontal seams*; the network
   exists only because every point of the rectangle is covered and the seams partition
   it. Trump’s packing is 73.18% dense — the container has area 15.0318 against 11 units
   of square, leaving 4.0318 of waste, about 26.8%. There are no spanning seams to
   become nodes, and no conservation law across a gap.
2. **It requires squares of distinct size.** The information content of a Smith diagram
   is that different currents flow through different wires.
   With eleven *equal* squares every current is identical, the network is degenerate,
   and the linear system says nothing.
3. **It requires axis-aligned squares.** Kirchhoff’s current law translates into a
   statement about widths meeting along a *horizontal* seam.
   A square tilted at `≈ 40.182°` has no horizontal edge and belongs to no seam.

There is a fourth objection, and it is decisive on its own.
**The method produces rational answers by construction.** Linear equations with rational
coefficients have rational solutions; that rationality is exactly why the Trinity Four
could scale their dissections to integers, and it is the source of the method’s power.
But the conjectured `s(11)` is a root of an *irreducible degree-8* polynomial over ℚ
(verified in this research).
A technique whose output is always rational cannot, even in principle, produce an
irrational algebraic number of degree 8. This is not a matter of the method being
unwieldy here — it is provably the wrong codomain.

#### What the right analogue actually is

The productive way to hold the intuition is this.
Tutte’s insight was: *impose the contact structure as a system of equations and solve
algebraically, rather than searching geometrically.* That insight **does** transfer.
It is exactly strategy 17 in the construction catalogue above, and it is how the
degree-8 polynomial for Trump’s packing is obtained: read off the contact graph, write
each tangency as a polynomial equation, and eliminate.
The same programme is standard in the rigidity-theoretic study of sphere and disk
packings, where contact graphs, rigidity, and Gröbner-basis elimination are routine
tools.

What changes is the *algebra*, and the change is the whole difficulty:

|  | Squared rectangles (Tutte) | Unit squares packed with gaps |
| --- | --- | --- |
| Contact conditions | Linear (seam widths sum) | Quadratic and trigonometric (tilt angles) |
| Solution field | ℚ — always rational | Algebraic of high degree (8 for `n = 11`) |
| Structure | Planar graph + linear algebra | Semialgebraic variety |
| Gaps | None permitted | Essential — 26.8% here |
| Right tool | Kirchhoff’s laws, matrix algebra | Elimination theory, real algebraic geometry |

So the promising direction is real, but it is not Kirchhoff’s laws.
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
| Erdős–Graham (1975), upper | `O(x^{7/11})` | 0.6364 |
| Montgomery (unpublished), upper | `O(x^{(3−√3)/2 + ε})` | 0.6340 |
| Chung–Graham (2009), upper | `O(x^{(3+√2)/7} log x)` | 0.6306 |
| **Wang–Dong–Li (2016)**, upper | `O(x^{5/8})` | 0.6250 |
| Chung–Graham (2020), upper — **claim withdrawn in effect** | `O(x^{3/5})` | 0.6000 |
| Bui (2025), McClenagan (2026), upper | `O(x^{3/5})` | 0.6000 |
| **Roth–Vaughan (1978), lower** | `w(α) ≫ (‖α‖·α)^{1/2}` when `α(α−[α]) > 1/6`; `‖α‖` = distance to the nearest integer | ≥ 0.5 at half-integers |

The Erdős–Graham result is the historical origin of the insight that **tilted** unit
squares beat axis-aligned ones — the same phenomenon that makes `n = 11` interesting,
appearing asymptotically.
Their paper also poses a conjecture that remains open in its own right: with `f(a)` the
maximal total circumference of `a` non-overlapping squares packed in a unit square,
`f(k² + 1) = 4k`.

**The upper-bound chain, stated carefully.** Two corrections to the version of this
history that circulates in secondary summaries.
The step from `0.631` to `0.600` was not a single move: **Wang, Dong and Li**
(arXiv:1603.02368, 2016) improved Chung–Graham’s `O(x^{(3+√2)/7} log x)` to
`O(x^{5/8})`, and did the same for the dual *covering* problem, taking the minimum
number of unit squares needed to cover the large square from
`x² + O(x^{(3+√2)/7} log x)` to `x² + O(x^{5/8})` **[Wang–Dong–Li 2016]**. And the
`O(x^{3/5})` bound claimed by Chung and Graham in 2020 **contains an error**: McClenagan
states it flatly — “this result has an error in it, which brings the best known bound
back” — and the point of both 2025–26 papers is to *establish* `O(x^{3/5})` by a new
route, not to re-derive an already-sound one **[McClenagan 2026]**,
**[Waste-0.6 2025]**. Treat `O(x^{3/5})` as dating from 2025, not 2020.

**The Roth–Vaughan lower bound, stated from the paper.** The 1978 paper was retrieved
after earlier passes failed, and its theorem settles a question three secondary sources
disagreed about. In full:

> **THEOREM.** Suppose that `α(α − [α]) > 1/6`. Then
> 
> ```
> w(α) ≫ (‖α‖ α)^{1/2}
> ```
> 
> where `‖α‖` denotes the distance of `α` from the nearest integer.

with `w(α) = α² − sup_𝒜 |𝒜|` over packings `𝒜` of unit squares into a square of side
`α`. Three points, each correcting something previously written here or in the secondary
literature:

1. **The side condition uses the fractional part; the bound uses the distance to the
   nearest integer.** They are different quantities and the theorem uses both, which is
   how renderings that pick one and apply it to the other go wrong.
2. **There is no `10⁻¹⁰⁰` constant.** The relation is Vinogradov `≫` — an implied
   absolute constant, never given a numerical value anywhere in the paper.
   Both **[Friedman DS7]** and **[McClenagan 2026]** report an explicit `10⁻¹⁰⁰`; that
   constant appears nowhere in Roth and Vaughan.
   An earlier draft of this document repeated it and called it “emblematic” of how weak
   these constants are — a rhetorical point resting on a number the source does not
   contain.
3. **The complementary case is covered by a remark, not left open.** If
   `α(α − [α]) ≤ 1/6` then `sup_𝒜 |𝒜| = [α]²`, so `w(α) ≫ α(α − [α])`, and Roth and
   Vaughan note this is essentially best possible.

The headline corollary, which is how the abstract states it: *in packing a square of
side `n + ½` with unit squares, the wasted space always has area `≫ n^{1/2}`.* This is
what rules out `W(x) = O(x^α)` for any `α < 1/2`, the form the rest of the literature
quotes (**[Good-Squares 2025]** writes it `W(x) ∉ o(x^{1/2})`).

Two further things the paper settles in passing.
It records **Montgomery’s** unpublished improvement as `(3 − √3)/2 + ε = 0.633974… + ε`,
confirming the corrigendum **[Friedman DS7]** issued in March 2023 and contradicting
**[McClenagan 2026]**, which attributes `(3+√2)/7` to Montgomery.
And it records that Erdős and Graham *speculated* the truth is `O(α^{1/2})`; Roth and
Vaughan say they are “dubious as to the validity of such a small bound” but prove that
if it is true, it is essentially best possible.

Roth and Vaughan also introduced the notion of a **good square** — one whose inclination
is at most `10⁻¹⁰` — and it has since been shown that for computing the asymptotic
growth of wasted space it suffices to consider packings with only good squares
**[Good-Squares 2025]**.

**Why this is irrelevant to `n = 11`.** These are asymptotic statements with unspecified
constants — Roth and Vaughan’s bound is stated with Vinogradov `≫` and never evaluates
its implied constant at all.
They describe behaviour as `x → ∞` and carry no information at `x ≈ 3.88`. The
small-case and asymptotic branches of this subject share an origin and a moral (tilting
helps) but are methodologically disjoint.
No asymptotic improvement will ever settle `n = 11`.

### Corrections to common summaries

The briefing that prompted this research, and many secondary summaries, contain errors
worth recording so they are not propagated.

| Claim | Verdict | Correct statement |
| --- | --- | --- |
| Stromquist’s paper “mathematically proves Walter Trump’s 11-square breakthrough” | **False** | It proves a lower bound `s(11) ≥ 3.7889`, which does not match Trump’s `3.8771`. `s(11)` is unresolved. |
| The paper “verifies that 11 is the first instance where the optimal configuration forces a non-45-degree tilt” | **True** | This is exactly Gardner’s conjecture, settled via Theorem 3 plus Trump’s construction. |
| `s(10) = 3 + √3 ≈ 3.707`, `s(11) ≤ 2 + 2√3 ≈ 3.789` (seen in an AI-generated search summary) | **False** | Arithmetically impossible: `3 + √3 ≈ 4.732`. The correct constants are `3 + ½√2` and `2 + 4/√5`. A LaTeX-mangling artifact. |
| `n = 11` is “the smallest example where the best known packing contains squares at three different angles” | **False** | That is `n = 17` (Bidwell, 1998). `n = 11` uses two orientation classes: axis-aligned and `≈ 40.182°`. |
| The Trinity Four “discovered the first Perfect Squared Squares” | **Misattributed** | Roland Sprague published the first perfect squared square (order 55, side 4205) in 1939, ahead of Brooks–Smith–Stone–Tutte. The Cambridge group built the theory. |
| Kirchhoff’s-law / Smith-diagram methods are a promising route to new bounds here | **False** | The method requires a gapless tiling by distinct axis-aligned squares and yields rational answers by construction. All four conditions fail for `s(11)`. See the dedicated section. |
| Gensane and Ryckelynck (2004/05) improved the `n = 11` packing | **False** | They computed its first *exact algebraic solution*, not a denser packing. The 1979 configuration is unchanged. |
| *Our own earlier draft:* rigorous interval branch-and-bound is “the most plausible untried line of attack” | **Wrong — corrected** | It is not untried. It has been applied to rotating unit squares (Montanher et al. 2018) and rigorously reaches `n = 3`. It is the most *developed* modern approach and falls far short of `n = 11`. |
| *Our own earlier draft:* the Roth–Vaughan bound is `W(x) ≥ 10⁻¹⁰⁰√(x·\|x − ⌊x⌋ + 1/2\|)`, “stated precisely in [Friedman DS7]” | **Wrong — corrected against the primary** | The theorem is `w(α) ≫ (‖α‖ α)^{1/2}` under `α(α − [α]) > 1/6`. The bound uses distance to the **nearest integer**; the side condition uses the **fractional part**; and there is **no explicit constant at all**. |
| **[Friedman DS7]** and **[McClenagan 2026]**: the Roth–Vaughan bound carries an explicit `10⁻¹⁰⁰` | **False** | No such constant appears anywhere in Roth and Vaughan. The relation is Vinogradov `≫`, whose implied constant is never evaluated. Two independent secondary sources carry the same phantom number. |
| **[McClenagan 2026]**: Montgomery’s improvement is `O(x^{(3+√2)/7})` | **False** | Roth and Vaughan record it as `(3 − √3)/2 + ε = 0.633974… + ε`, matching the corrigendum **[Friedman DS7]** issued 1 March 2023. `(3+√2)/7` is Chung–Graham’s 2009 exponent. |
| *Our own earlier draft:* Kearney–Shiu prove `n_r ≤ 27r^{3/2} + O(r²)` | **Wrong — corrected** | The bound is `27r³/2 + O(r²)` — cubic in `r`, from `p(⌈3r/2⌉)` with `p(t) = 4t³ + 4t² + 3t + 1`. A misread fraction. |
| *Our own earlier draft:* Stromquist’s Theorem 2 is “ten unavoidable points, eleven boxes, pigeonhole” | **Wrong — corrected** | The ten points are *not* unavoidable; the proof is two-stage and finishes with twelve points of which one box must contain **three**. Same for Theorem 3. See [What Stromquist actually proved](#what-stromquist-actually-proved-2003). |
| *Our own earlier draft:* Gensane–Ryckelynck and Nagamochi could not be retrieved | **Wrong — corrected** | Both are freely available: Springer serves the Gensane–Ryckelynck PDF openly, and Nagamochi is open access in *Electron. J. Combin.* 12 #R37. Both are now in the local archive and read. |
| *Our own earlier draft:* Kearney–Shiu gave the first published proof for `n = 6, 7, 8, 9` | **Partly wrong — corrected** | Their first is `s(6) = 3`. **El Moumni (1999)** holds published priority for `s(7) = s(8) = 3` and `s(15) = 4`. See the [priority ledger](#priority-claims-and-what-was-actually-published). |

The third row is a useful caution: at least one automated summarizer produced
self-contradictory arithmetic while citing a correct source.
Every numeric constant in this document was re-derived or checked numerically.

### Cultural and expository record

- **Martin Gardner**, “Mathematical Games,” *Scientific American*, October 1979, with
  follow-ups November 1979, March 1980, November 1980. This is where the problem entered
  wide circulation and where the conjecture was posed.
  Trump’s packing reached Gardner by correspondence in 1979 and was first published
  correctly in one of Gardner’s books.
- **xkcd 2740, “Square Packing.”** Depicts “improving” the `n = 11` record with a
  hydraulic press, citing `s < 3.877084`; the joke is that crushed squares are no longer
  squares. The explainxkcd annotation correctly notes the packing is unproven.
- **Stand-up Maths (Matt Parker)**, “The Insane World of Polygon Packings” — visual
  treatment of how grid patterns give way to tilted arrangements.
- **Erich Friedman’s Packing Center** and the **Kingbird “Squares in Squares”
  catalogue** are the two live record directories; Kingbird supplies exact minimal
  polynomials and SVG layouts, and marks configurations rigid or not.

### Adjacent problems (deliberately out of scope)

These are frequently conflated with the present problem in casual sources:

- **Packing consecutive/unequal squares** (sides `1, 2, …, n`) — a different problem
  with its own literature (e.g. guillotine-cutting asymptotics, *Optimization Letters*
  16 (2022) 2775–2785). A search for “square packing” papers will surface these; they
  say nothing about `s(11)`.
- **Squared squares / perfect dissections** (gapless tilings by *distinct* squares) —
  the Tutte–Kirchhoff tradition, treated at length above because its machinery is so
  often assumed to apply here.
  It does not.
- **Covering** a square by squares (as opposed to packing) — different objective.
- **Packing unit squares in a circle, triangle, or rectangle** — related technique
  (unavoidable points), different constants.

## Key Insights

1. **The problem is open, and the gap is structural, not incidental.** `s(11)` is pinned
   only to `[3.788854, 3.877084]`. Both endpoints have stood unimproved for over two
   decades (lower) and nearly five (upper).

2. **Gardner’s conjecture was settled without solving the problem.** Stromquist proved
   the *necessity* of oblique tilts by bounding the 0°/45° class from below at
   `3.885618` and pointing at Trump’s `3.877084`. This is a clean example of resolving a
   qualitative question while the quantitative one stays open — and it is the single
   most misunderstood point in the popular literature.

3. **Algebraic degree is the likely obstruction.** Every solved case has `s(n)` of
   degree ≤ 2 over ℚ. The conjectured `s(11)` is a root of an irreducible degree-8
   polynomial (verified in this research).
   Unavoidable-point arguments certify thresholds built from unit distances and
   container coordinates, which naturally produce low-degree constants.
   Closing the `n = 11` gap by that method would require certifying a degree-8 threshold
   — no such argument is known, and it is not obvious one exists.

4. **Contact equations explain computability but not global optimality.** Trump’s
   contact conditions determine the displayed algebraic side value.
   Exp-013 now certifies all complete branchwise fixed-side linearized cones and proves
   qualitative local isolation by a finite-branch argument.
   It supplies no explicit radius and says nothing about whether a different contact
   class does better, which is precisely what a global proof must exclude.

5. **The failure of computation is informative in one direction only.** Fifty years of
   search, including a purpose-built billiard/inflation algorithm, has not beaten a
   hand-computed 1979 configuration.
   That raises confidence in the *conjecture* and provides no leverage on the *proof*.

6. **Bentz’s technique is the most plausible route forward.** His proofs of `s(22) = 5`
   and `s(33) = 6` replace fixed unavoidable point sets with “continuously varying
   families of such sets.”
   That is a genuine strengthening of the method’s expressive power.
   Whether it can reach an irrational, high-degree target rather than an integer one is,
   as far as this research found, untested.

7. **The two literatures do not meet.** Asymptotic wasted-space bounds (now at
   `O(x^{3/5})`) and exact small-case results share the tilting insight and nothing
   else. Progress on `n = 11` will not come from that direction.

8. **The proof inventory is far narrower than the search inventory.** Twenty distinct
   construction strategies have produced records; essentially *one* proof idea —
   unavoidable point sets — underlies nearly every proved value, with later papers
   refining it (duality, forcing, continuously varying families) rather than replacing
   it. A field with one load-bearing technique stalls when that technique reaches its
   limit, which is what appears to have happened at `n = 11`.

9. **The Kirchhoff/Tutte method is provably the wrong tool, not merely an awkward one.**
   Beyond needing a gapless tiling of distinct axis-aligned squares — three conditions
   `n = 11` violates outright — the method solves *linear* systems and therefore always
   returns *rational* side lengths.
   The conjectured `s(11)` is irrational of degree 8. No amount of adaptation lets a
   rational-output method emit a degree-8 irrational.
   What does survive is Tutte’s deeper instinct — impose contacts as equations and solve
   algebraically — which is exactly how the degree-8 polynomial is derived.
   The algebra just stops being linear, and that is the whole difficulty.

10. **Rigorous certification is developed, and its ceiling for rotating squares is
    `n = 3`.** This corrects an earlier assessment in this document.
    Interval branch-and-bound is mature for circles (optimality proofs to `n = 33`) and
    has been applied to unit squares *with free rotation* by Montanher et al.
    (2018), who rigorously settled three squares in a circle using a sentinels
    formulation of non-overlap.
    Eleven squares means eight more rotational degrees of freedom on top of sixteen
    positional ones, against a disjunctive non-overlap condition.
    The technique is therefore a **measure of the difficulty** of certifying `s(11)`,
    not a shortcut past it.
    Positivstellensatz/SOS certificates remain, as far as this research found, genuinely
    unattempted.

11. **The lower-bound literature has one abstraction and four instantiations.**
    **[Bentz 2016]** names it: *resource starvation*. Associate a numerical resource
    with subsets of the container, show each packed box must consume a quantum of it,
    and count. The instantiations are points worth 1, points with a slider, line segments
    measured by intersection length, and continuously varying families.
    Seen this way the field’s apparent single technique is really one idea being
    progressively de-discretised — and the natural next step, an explicitly fractional
    LP certificate, is the one nobody has taken.

12. **Kearney–Shiu is the only place symmetry is used as a proof engine.** Their duality
    rotates an unavoidable lattice a quarter-turn about the container’s centre; because
    the container is a *square*, the rotated set is unavoidable too, giving a second
    certificate for free, and the proof reasons about the interaction of the two.
    Every other proof in the literature uses symmetry only to reduce case counts.

13. **Plausible patterns here fail late.** The conjecture `s(n² − n) = n` survives small
    cases and then dies at `n = 17`, where Cleemann packed 272 unit squares into a
    side-17 square with room to spare.
    That is a direct argument against inferring `s(11)` from the fact that fifty years
    of search has not beaten Trump.

14. **The packing is fully explicit, and the algebra is small.** The whole configuration
    — six axis-aligned squares and five tilted at a common angle — is pinned by just
    **two** contact equations, from which the degree-8 polynomial follows by
    elimination. One of them reduces to the compact
    `s = 2 + (2 + sin a)/(cos a + sin a)`. Gensane and Ryckelynck needed fourteen
    equations in 2004; Ellsworth showed two suffice in 2023. The obstruction to proving
    optimality is emphatically *not* that the candidate is complicated — it is that
    nothing rules out the configurations nobody has thought of.

## A Research Program

The preceding sections describe what is known.
This one describes what to do about it, ordered by value per unit of effort, and it is
written on the assumption that the work will be done with modern computational tooling
and coding agents rather than by hand.

It rests on one observation that the
[open-frontier table](#the-open-frontier-what-is-actually-unknown) makes unavoidable:
**the search side of this problem is healthy and the proof side is not.** Records move
monthly; the lower-bound frontier is a 2005 general theorem plus one 2003 argument that
covers two values of `n`. Any program should be weighted accordingly.

### Foundations: finish the archive and the survey

1. **Retrieve the remaining primaries.** Roth–Vaughan (1978) first — it is the only
   source in this document whose statement could not be pinned down, and three secondary
   renderings of it disagree.
   Then El Moumni (1999), Stromquist’s 1984 memoranda, Chung–Graham (2009), and
   Arslanov–Bui (2025). Each per the three-format archive discipline in
   [`resources/`](../../../resources/README.md).
2. **Machine-readable record corpus.** A first version now exists:
   [`frontier/`](../../../frontier/README.md) carries one schema-validated artifact per
   `n ≤ 100`, built by parsing the catalogue’s *prose* for upper bounds and computing
   lower bounds from four sources.
   What it does not yet carry is geometry — the next step is parsing the catalogue SVGs
   into `(x, y, θ)` triples with their algebraic definitions, which is what would let
   every record be independently audited by the exact verifier.
   Extending the corpus past `n = 100` is mechanical for the structured fields; the
   editorial is the part that does not automate.

### The verifier, and why it comes before the searcher

3. **Ship the exact verifier as a real tool.** The layered design, the language boundary
   and the measured budgets are in
   [Infrastructure for Square-Packing Exploration](research-2026-08-22-infrastructure-for-packing-exploration.md).
   The reference implementation in [`explorations/packing/`](../../../README.md)
   certifies `s(11)` exactly in 0.35 s of pure Python; the production version is a
   filtered exact-predicate kernel over `ℚ(α)` on top of FLINT or CGAL. Its value is not
   the checking — it is that a search program with an exact oracle can *publish claims
   that mean something*, which no current record-setting program can do.

### Search: an open baseline where none exists

4. **Build an open GPU/many-core annealer.** The collision-detection engineering is
   already solved by `jagua-rs` under MPL-2.0 with continuous rotation; the annealing
   layer on top is comparatively simple.
   Copy the determinism discipline recorded in the FrankenSim study — counter-based RNG
   keyed by `(seed, kernel, tile, index)`, fixed-slot reductions in tile order — so that
   basin statistics are reproducible and citable.
5. **Point the modern evolutionary-search stack at `s(n)`.** As the companion tooling
   document records, the AlphaEvolve benchmark ecosystem is active, open, contested to
   the fifth decimal on adjacent problems, and **has never been aimed at
   squares-in-squares**. Seeded with the record corpus and scored by the exact verifier,
   it would test directly whether that class of method can rediscover Trump’s basin and
   the low-`n` records — a question nobody has asked.
   Success would be informative; failure would be more informative.

Where to *point* this machinery is its own question, taken up in
[A Search Philosophy for Square Packing](research-2026-08-23-search-philosophy-and-landscape-cartography.md):
the registered premise is that record constructions may have low hit probability under
named baseline proposers, so the first search artifact should be a provisional endpoint
atlas over the LP-quench map, steered by structural diversity rather than by reshaping
the loss — boiled down to testable form in the standing review’s register (H-11–H-15,
series S6).

### Proof: the lane where nothing automated has ever run

This is the part of the program with no incumbents at all.

6. **Machine-verify the existing unavoidable sets.** “Does every unit square in `[0,k]²`
   contain a point of `P`?” is a decision problem in three parameters `(x, y, θ)` — well
   inside the reach of interval branch-and-bound or an SMT solver with nonlinear
   arithmetic. Every published lower bound in this subject rests on such sets, checked
   only by referees with pencils.
   Nobody has ever machine-checked one.
7. **Search for new unavoidable configurations, targeting `n = 12`.** Per
   [the `n = 12`–`16` analysis](#n--12-to-n--16-the-next-targets-after-11), `n = 12` is
   the only open case in its range, its optimum is near-certainly the integer `4`, and
   an integer target sidesteps the degree-8 obstruction that blocks `n = 11`. The search
   is discrete-continuous — place points, verify unavoidability, minimise count — which
   is the same shape as item 5 but aimed at proofs rather than packings.
   Two lessons from this document constrain the design usefully: threshold certificates
   (a box charged three points, as in Stromquist’s Theorem 2) are admissible and already
   classical, and weighted or measure-valued resources (Bentz) are the direction the
   field was already drifting.
8. **Test the transversal crossover.** The fractional-transversal literature has
   machinery — fractional Helly, Alon–Kleitman, LP duality — that this field has been
   hand-deriving for forty years without naming.
   Even a negative result would be worth writing down.
9. **Formalise one small existing proof.** Friedman’s Lemmas 1–3 plus `s(2) = s(3) = 2`,
   then Stromquist’s Theorem 1, in Lean.
   Small, self-contained, and it would surface any informal gaps in the lemma layer that
   every other result stands on.
   The precedent is now strong: dimension-8 sphere packing went sorry-free in February
   2026, with an autoformalisation agent closing the remaining goals in five days.

### Two calibrations to keep the program honest

**Do not target `s(11)` with a rigorous solver.** The only computer-assisted optimality
proof for rotatable unit squares in any container covers **three** squares in a circle,
and took ten minutes to do it.
Eleven squares is eight more rotational degrees of freedom on top of sixteen positional
ones, against a disjunctive non-overlap condition and a degree-8 irrational target.
That ceiling is a measurement of the difficulty, not an invitation.

**Search cannot settle this problem.** Fifty years of it has not beaten a 1979 hand
construction, which raises confidence in the conjecture and provides no leverage on the
proof. A search that fails to find something better has certified nothing.
Every item in the proof lane above exists because of this.

## Open Questions

- [ ] Can the unavoidable-point method, or Bentz’s continuously-varying refinement,
  prove any lower bound of algebraic degree > 2? This appears to be the key
  methodological question gating `n = 11`.
- [ ] What *is* the best lower bound obtainable in principle from a finite unavoidable
  point set in a container of side `≈ 3.877`? Is there a proved ceiling below
  `3.877084`?
- [ ] Could a rigorous computer-assisted proof (interval arithmetic plus
  branch-and-bound over contact classes, as used for rigorous circle packing in a
  circle) close the gap?
  This has been done for related packing problems but no attempt on `s(11)` was found.
- [x] ~~Verify the Gensane–Ryckelynck `n = 11` entry~~ — **resolved**: they produced the
  first exact algebraic solution of Trump’s packing (14-equation elimination, publishing
  a formula for `2/s`), not an improved packing.
  Nothing was retracted; the secondary literature mis-described an exact-solution result
  as a record improvement.
- [x] ~~Obtain the exact coordinates of all 11 squares~~ — **resolved**: extracted from
  the catalogue SVG source and re-verified at 40-digit precision.
  See
  [The exact construction](#the-exact-construction-contact-equations-coordinates-and-closed-form).
- [x] ~~Retrieve the Gensane–Ryckelynck primary text~~ — **resolved**: Springer serves
  the PDF openly; retrieved, read, archived, and its `n = 11` section is now quoted
  directly above rather than through Ellsworth’s annotations.
  Their published polynomial and its `45°`-offset angle were independently verified
  here.
- [x] ~~Locate Nagamochi (2005)~~ — **resolved**: open access as *Packing Unit Squares
  in a Rectangle*, *Electron.
  J. Combin.* **12** #R37. Archived; its general lower bound is now recorded and used
  throughout the [open-frontier table](#the-open-frontier-what-is-actually-unknown).
- [x] ~~Obtain Roth & Vaughan (1978) and settle the exact form of the lower bound~~ —
  **resolved**: the paper was supplied and is archived.
  The theorem is `w(α) ≫ (‖α‖ α)^{1/2}` under `α(α − [α]) > 1/6`, with `‖α‖` the
  distance to the nearest integer, and **there is no `10⁻¹⁰⁰` constant** — the relation
  is Vinogradov `≫`, and both **[Friedman DS7]** and **[McClenagan 2026]** report a
  constant the paper does not contain.
  See [the asymptotic section](#asymptotic-theory-and-why-it-does-not-help).
- [ ] Obtain El Moumni (1999), *Studia Sci.
  Math. Hungar.* **35** 281–290, and confirm what it proves and how; it holds published
  priority for three values and no summary of this field describes its method.
- [ ] Obtain Stromquist’s 1984 Wagner Associates memoranda I–III. Memorandum III covers
  `n ≤ 65` and Gardner’s conjecture for `n = 11`, and sits behind a large share of the
  claim column in the
  [priority ledger](#priority-claims-and-what-was-actually-published).
- [ ] Obtain the full text of the March 2023 “Packing of 11 unit squares in a square
  with minimum size” note (ResearchGate 403).
- [ ] Read the “crucial relation” of **[Gensane–Ryckelynck 2005]** off the PDF directly:
  its displayed fraction does not survive text extraction unambiguously, and the
  reconstruction attempted here does not reproduce `s(11)` under any normalization
  tried.
- [ ] Reconcile the two published values for `s(17)`: **[Gensane–Ryckelynck 2005]**
  report `4.6755300960455`, **[Kingbird]** `4.67553009360455…`. They agree to nine
  decimals; one transcription carries a slip.
- [ ] Locate Boris Alexeev’s independent June 2023 derivation and record the
  “substantially different method” it used.
- [ ] Trace the 1980 Gustafsson–Thulin rediscovery to the primary Swedish source
  (*Ronden*); Ellsworth notes he has not read it directly either.
- [x] ~~Resolve the `n = 23` discrepancy~~ — **resolved**: `n = 23` is covered by
  Nagamochi’s `s(m²−1) = s(m²−2) = m` at `m = 5`, and other enumerations list it
  explicitly. Wikipedia’s list is simply incomplete.
- [ ] Has any Positivstellensatz/SOS infeasibility certificate ever been attempted for a
  square-packing lower bound, in any case, at any `n`? Nothing was found.
- [ ] What is the practical branching cost of interval branch-and-bound on `s(11)` given
  the disjunctive separating-axis condition?
  Is the case explosion merely large or genuinely prohibitive?
- [ ] Did Gensane–Ryckelynck’s inflation algorithm ever explore contact classes for
  `n = 11` other than Trump’s, and is that enumeration recorded anywhere?
- [ ] Confirm whether Packomania covers squares-in-squares records or is circle-focused;
  it was listed in the source briefing but not verified here.

## Source Availability

Every source this document cites is either in the local archive under
[`resources/`](../../../resources/README.md) or listed here.
The structured form is
[`frontier/source-availability.yaml`](../../../frontier/source-availability.yaml); the
tables below are generated from it.

**Re-test this list rather than inheriting it.** A “not retrievable” verdict is a
negative search result, and this document has now been wrong about one five times.
Three sources recorded as unavailable turned out to be freely downloadable when
re-tested; a fourth was open access at PMC the whole time; and the fifth — the most
consequential of all — was supplied on request.

<!-- BEGIN GENERATED: sources-recovered (tools/render_tables.py) -->

| Source | How it was recovered |
| --- | --- |
| **[Roth–Vaughan 1978]** Inefficiency in Packing Squares with Unit Squares | Supplied by the requester after ScienceDirect refused automated clients. |
| **[Markót 2021]** Improved interval methods for solving circle packing problems in the unit square | Open access at PMC; the earlier pass recorded it unretrieved without testing. |
| **[Gensane–Ryckelynck 2005]** Improved Dense Packings of Congruent Squares in a Square | Springer serves the PDF openly at its /content/pdf/ URL; the earlier attempt fetched the article landing page. |
| **[Nagamochi 2005]** Packing Unit Squares in a Rectangle | Open access in Electron. J. Combin.; cited by exact title in the archived DS7 reference list all along. |
| **[Wang–Dong–Li 2016]** A New Result on Packing Unit Squares into a Large Square | On arXiv. |

<!-- END GENERATED: sources-recovered -->

### Still unretrieved

Ordered by how much rests on them.
`Obstacle` records the mechanism, not a guess: `paywall` means a landing page was served
in place of the PDF on a re-test, not that access was assumed to be blocked.

<!-- BEGIN GENERATED: sources-unretrieved (tools/render_tables.py) -->

| Source | Year | Where | Obstacle | What rests on it |
| --- | --- | --- | --- | --- |
| **[Stromquist 1984]** Packing unit squares inside squares, I-III | 1984 | Daniel H. Wagner Associates Memoranda | unpublished | A large share of the claim column in the priority ledger. The single most valuable unretrieved document in this subject. |
| **[Arslanov–Bui 2025]** Note on “efficient packings of unit squares in a large square” | 2025 | Discrete Comput. Geom. | paywall | Current continuation of the Kearney-Shiu delta_n / n_r line. |
| **[El Moumni 1999]** Optimal Packings of Unit Squares in a Square | 1999 | Studia Sci. Math. Hungar. 35, 281-290 | print only | Published priority for s(7) = s(8) = 3 and s(15) = 4. No summary of this field describes its method. |
| **[Plakhta 2021]** Configuration spaces of squares in a rectangle | 2021 | Algebraic & Geometric Topology 21, 1445-1478 | bot-blocked | H-032’s literature routing for affine Morse-Bott analysis of square configuration spaces in a rectangle; it is context and method, not a classification of the exact optimal-moduli spaces asked there. |
| **[Trump 2023]** Packing of 11 unit squares in a square with minimum size | 2023 | ResearchGate | bot-blocked | Accessible excerpts confirm rigidity and state the packing “cannot be improved by computer programs as long as the same geometrical arrangement is used” -- a statement about local, not global, optimality. |
| **[Chung–Graham 2009]** Packing equal squares into a large square | 2009 | J. Combin. Theory Ser. A 116, 1167-1175 | paywall | The O(x^{(3+sqrt(2))/7} log x) step in the asymptotic chain. |
| **[Chung–Graham 2020]** Efficient packings of unit squares in a large square | 2020 | Discrete Comput. Geom. | paywall | The claimed O(x^{3/5}) bound that McClenagan states “has an error in it”. Reading it would let us describe the error rather than relay the claim. |
| **[Gardner 1979]** Mathematical Games | 1979 | Scientific American, Oct 1979 (also Nov 1979, Mar 1980, Nov 1980) | print only | Origin of the conjecture Stromquist settled. |
| **[BSST 1940]** The dissection of rectangles into squares | 1940 | Duke Math. J. 7, 312-340 | paywall | The Smith-diagram correspondence, currently sourced to squaring.net -- an excellent specialist source but a secondary one. The rationality argument that makes the non-transferability section decisive does not depend on it. |
| **[Markót 2004]** Optimal Packing of 28 Equal Circles in a Unit Square - The First Reliable Solution | 2004 | Numerical Algorithms | paywall | Calibration only. Its successor, Markót 2021, is archived and carries the same method at n = 31, 32, 33. |
| **[Gustafsson–Thulin 1980]** Problem Ronden | 1980 | Ronden (Swedish periodical), Apr/Sep/Dec 1980 | obscure periodical | The independent 1980 rediscovery of Trump’s packing. Priority is Trump’s regardless; this would only settle the rediscovery’s details. |
| **[Hämäläinen 1980]** Correspondence, 20 April 1980 | 1980 | private correspondence | private correspondence | The optimal 45-degree packing of 11 squares realising the Theorem 3 bound. |

<!-- END GENERATED: sources-unretrieved -->

**What this list is for.** It is the fact-checking boundary of this research.
Every claim in this document either traces to a file in `resources/` — where the
original PDF, a cleaned transcription and a faithful raw extraction sit side by side, so
a formula can be checked against the extraction it came from — or traces to something in
the table above, and is marked **[secondary]** where it does.
A reader auditing a claim should be able to tell which case they are in without leaving
the repository.

The two highest-priority acquisitions are both about **provenance rather than
mathematics**: Stromquist’s 1984 memoranda sit behind a large share of the claim column
in the [priority ledger](#priority-claims-and-what-was-actually-published), and El
Moumni (1999) holds published priority for three values of `s(n)` that most summaries of
this field credit to someone else.

## Methodology

Research was conducted on 2026-08-22 by web search and direct retrieval of primary
sources, with numerical and symbolic verification of every constant.

**Primary sources retrieved in full.** Stromquist’s 2003 paper was downloaded as PDF and
its text extracted locally (via `pdfminer.six`, after repairing a broken `cffi`
installation) so that theorem statements, lemma statements, and the reference list could
be read directly rather than through summaries.
This proved essential: the abstract’s mathematical notation is mangled by every
automated summarizer encountered, and one search summary returned arithmetically
impossible constants.

**Independent verification performed.**

- Confirmed `3 + √(1/2) = 3.7071067811865475`,
  `2 + 2√(4/5) = 2 + 4/√5 = 3.78885438199983176…`, and
  `2 + 4√2/3 = 2 + 2√(8/9) = 3.885618083164127`, establishing that the abstract’s two
  forms of the Theorem 3 constant agree.
- Evaluated the degree-8 polynomial at the published side length:
  `P(3.87708359002281) ≈ −6.4 × 10⁻¹³`, consistent to available precision.
- Factored the polynomial symbolically (SymPy): **irreducible over ℚ**, with exactly two
  real roots, the positive one being `3.877083590022814`.
- Computed the open interval width: `0.088229208022982…` (re-derived at 50-digit
  precision; an earlier draft quoted a float64 value correct only to ~12 digits).

**Sources that could not be retrieved.** ResearchGate (HTTP 403), Academia.edu (403),
ACM Digital Library (403), and Springer (authentication redirect) blocked access to the
Gensane–Ryckelynck primary text and the March 2023 note.
Claims resting on those are marked as secondary and flagged in
[Open Questions](#open-questions).

**Link validation.** All 30 cited URLs were re-checked with `curl` after the third pass.
Twenty-eight return HTTP 200. Two return bot-blocking codes to automated checkers but
are valid in a browser: ScienceDirect (403) and YouTube (429). Two defects found in the
first pass were fixed: a citation pointing at the wrong Electronic Journal of
Combinatorics article, and a dead author-hosted copy of Erdős–Graham (1975) — the latter
now resolves to the Stanford technical report CS-TR-75-483, which is live.

**Second research pass (same day).** The strategy catalogues, the squared-square
section, and the Kirchhoff transferability assessment were added in a second pass.
The Smith-diagram correspondence was verified line by line against squaring.net’s
exposition rather than reproduced from memory or from the briefing; the priority
question (Sprague vs.
the Trinity Four) was checked separately and the briefing’s attribution corrected.
The non-transferability argument rests on four independent conditions, of which the
rationality objection is self-contained and decisive: it follows from the linearity of
Kirchhoff’s laws together with the degree-8 irreducibility established in the first
pass. The `n = 23` question left open after the first pass was resolved.

**Third research pass (bead-tracked).** Work was decomposed into a tbd epic hierarchy so
that no strand is lost, and this pass executed the highest-priority beads.
It produced the exact construction data, resolved the Gensane–Ryckelynck question from
the catalogue’s own cited provenance, and overturned this document’s earlier claim that
rigorous interval branch-and-bound was untried.
All contact equations and derived constants were re-verified at 40-digit precision with
mpmath; residuals are below `10⁻³²` throughout.

**Fourth pass — technical review and remediation (same day).** The document was reviewed
end to end against its own archive, every substantive claim class was re-verified, and
the findings were applied here rather than kept in a separate review document.
What that pass changed:

- **Re-verified independently** (SymPy and mpmath, 50 digits): the degree-8 polynomial’s
  irreducibility and real roots; mutual consistency of the three degree-8 polynomials
  for `s`, `sec a` and `tan(a/2)` by resultant elimination; both contact equations; the
  closed form; the tilt angle; all five derived constants (residuals below `10⁻⁴⁷`); and
  the Stromquist constants.
  All held. The packaged verifier’s `test.sh` was re-run and passed.
- **Retrieved two sources previously recorded as unavailable.** Springer serves the
  **[Gensane–Ryckelynck 2005]** PDF openly at its `/content/pdf/` URL — the earlier pass
  had fetched the article landing page and concluded paywalled.
  **[Nagamochi 2005]** is open access in the *Electronic Journal of Combinatorics*; its
  citation was in the archived **[Friedman DS7]** reference list the whole time.
  **[Wang–Dong–Li 2016]** was also retrieved.
  All three are archived with their PDF and a faithful `pdfminer.six` extraction;
  cleaned transcriptions are still to be written, and the archive README records that.
  (The extraction again required repairing a broken `cffi` installation.)
- **Read the Gensane–Ryckelynck `n = 11` section directly** and rewrote it from the
  paper: the 14-equation Maple elimination, the polynomial over `ℚ(√2)`, and the fact
  that their claimed “improvement” at `n = 11` is a sharpening of the recorded *number*
  for Trump’s configuration, not a better packing.
  Their published root was verified here to be `cos(45° − a)`, which explains why the
  formula does not look like one for `s(11)`.
- **Corrected five substantive errors**, each recorded in
  [Corrections to Common Summaries](#corrections-to-common-summaries): the Roth–Vaughan
  formula and its attribution, the Kearney–Shiu exponent, the two-stage structure of
  Stromquist’s Theorems 2 and 3, the retrievability conclusions, and the El Moumni
  priority omission.
- **Built the [open-frontier table](#the-open-frontier-what-is-actually-unknown)** by
  parsing the archived record catalogue programmatically for upper bounds, degrees and
  analytic status, and evaluating four lower-bound sources per `n`. Counts quoted in the
  surrounding analysis (65 open cases, 63 governed by Nagamochi, 31 where the grid is
  still the record) were recomputed from the parse rather than estimated.
  The same caveat as the other parsed statistics applies: these are counts of annotation
  text and may miscount entries phrased unusually.
- **Re-checked currency** by search: no change to either `s(11)` bound was found, the
  catalogue’s `n = 11` entry still carries no proof attribution, and no result for
  squares-in-squares has come out of the AlphaEvolve benchmark ecosystem.
  Negative results from search remain weak evidence, per the standard below.

**Confidence.** High for everything sourced to the Stromquist paper (read directly),
Friedman’s survey, and the numeric verifications.
Medium for the Gensane–Ryckelynck history and the 2023 correspondence, which rest on
secondary reporting.
High for the Smith-diagram correspondence and the squared-square history — with the
caveat that these were checked against squaring.net, an excellent specialist source but
still a secondary one; the BSST 1940 primary remains unretrieved (Project Euclid, not
open access), and the rationality objection that makes the section decisive does not
depend on it.
The claims that interval branch-and-bound and SOS certificates have *never*
been applied to `s(11)` are negative results from search, and negative results from
search are weak: they mean nothing was found, not that nothing exists.
The fourth pass supplies a concrete cautionary instance of exactly this: two sources
this document had recorded as *unavailable* turned out to be freely downloadable, one of
them open access in the same journal as much of the rest of the bibliography.
A “not retrievable” conclusion is itself a negative search result and should be
re-tested rather than inherited.

## References

Every key below resolves to a local copy under
[`resources/`](../../../resources/README.md) unless marked **[not retrieved]**. Local
stems are given as `papers/<stem>` or `web/<stem>`; each stem has a `.pdf`/`.html`
original, a cleaned `.md`, and for papers a faithful `.raw.md` extraction.

### Core literature on `s(n)`

- **[Stromquist 2003]** — Walter Stromquist, “Packing 10 or 11 Unit Squares in a
  Square,” *Electron. J. Combin.* **10** (2003), #R8.
  [Online](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v10i1r8) ·
  local `papers/stromquist-2003-packing-10-or-11-unit-squares`. *The central paper; read
  in full during this research.*
- **[Friedman DS7]** — Erich Friedman, “Packing Unit Squares in Squares: A Survey and
  New Results,” *Electron.
  J. Combin.*, Dynamic Survey DS7. Last substantive revision 14 Aug 2009; the archived
  HTML also carries a **corrigendum dated 1 March 2023** correcting the typeset
  Montgomery exponent to `(3−√3)/2`, which is the form used above.
  [Online](https://www.combinatorics.org/files/Surveys/ds7/ds7v5-2009/ds7-2009.html) ·
  local `papers/friedman-ds7-packing-unit-squares-in-squares`,
  `web/friedman-ds7-survey-2009-html`.
- **[Kearney–Shiu 2002]** — M. J. Kearney and P. Shiu, “Efficient packing of unit
  squares in a square,” *Electron.
  J. Combin.* **9** (2002), #R14.
  [Online](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v9i1r14) ·
  local `papers/kearney-shiu-2002-efficient-packing-unit-squares`. *Duality method;
  first published proof that `s(6) = 3`, and treats `s(7)`.*
- **[Bentz 2010]** — Wolfram Bentz, “Optimal Packings of 13 and 46 Unit Squares in a
  Square,” *Electron. J. Combin.* **17** (2010), #R126.
  [Online](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v17i1r126/pdf/)
  · local `papers/bentz-2010-optimal-packings-13-and-46`.
- **[Bentz 2016]** — Wolfram Bentz, “Optimal Packings of 22 and 33 Unit Squares in a
  Square,” arXiv:1606.03746. [Online](https://arxiv.org/abs/1606.03746) · local
  `papers/bentz-2016-optimal-packings-22-and-33`. *Continuously varying families of
  unavoidable sets.* **On the date:** cited throughout this document by its arXiv year,
  2016; **[Kingbird]** dates the proof October 2018 and the companion tooling document
  once wrote “Bentz 2018”. Same result, three defensible dates — arXiv 2016 is the
  convention here.
- **[Arslanov et al.]** — M. Z. Arslanov, S. A. Mustafin, Z. K. Shangitbayev, “Improved
  packings of n(n−1) unit squares in a square,” *Electron.
  J. Combin.* **28**(4).
  [Online](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v28i4p22/pdf/)
  · local `papers/arslanov-improved-packings-n-n-1`.
- **[Gensane–Ryckelynck 2005]** — T. Gensane and P. Ryckelynck, “Improved Dense Packings
  of Congruent Squares in a Square,” *Discrete Comput.
  Geom.* **34** (2005) 97–109.
  [Article](https://link.springer.com/article/10.1007/s00454-004-1129-z) ·
  [open PDF](https://link.springer.com/content/pdf/10.1007/s00454-004-1129-z.pdf) ·
  local `papers/gensane-ryckelynck-2005-improved-dense-packings`. *The inflation /
  stochastic-billiard algorithm; the 14-equation elimination and the `ℚ(√2)` polynomial
  for `cos(45° − a)`.* **Retrieved and read in full** — earlier passes recorded it as
  paywalled after fetching the article landing page rather than the `/content/pdf/` URL.
- **[Nagamochi 2005]** — Hiroshi Nagamochi, “Packing Unit Squares in a Rectangle,”
  *Electron. J. Combin.* **12** (2005), #R37 (submitted 29 Sep 2004, published 30 Jul
  2005).
  [Online](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v12i1r37) ·
  local `papers/nagamochi-2005-packing-unit-squares-in-a-rectangle`. *The general
  rectangle theorem, the closed-form lower bound for every `N ≥ 4`, and the
  `s(n²) = s(n²−1) = s(n²−2) = n` corollary.* **Open access** — an earlier pass of this
  research recorded it as unlocated, which was wrong.
- **[El Moumni 1999]** — Said El Moumni, “Optimal Packings of Unit Squares in a Square,”
  *Studia Sci. Math. Hungar.* **35** (1999), no.
  3–4, 281–290. **[not retrieved]** — print-only; known through **[Friedman DS7]** ref
  [12], which credits it with `s(7) = s(8) = 3` and `s(15) = 4`. Holds published
  priority for those three values.
- **[Gardner 1979]** — Martin Gardner, “Mathematical Games,” *Scientific American*,
  October 1979 (also Nov 1979, Mar 1980, Nov 1980). Origin of the conjecture.
  **[not retrieved]** — print.
- **Pertti Hämäläinen**, correspondence, 20 April 1980 — the optimal 45° packing of 11
  squares. **[not retrieved]** — cited by **[Stromquist 2003]**.
- **Stromquist**, “Packing unit squares inside squares,” I–III, Daniel H. Wagner
  Associates Memoranda, 1984. **[not retrieved]** — unpublished; memorandum III covers
  `n ≤ 65` and Gardner’s conjecture for `n = 11`.

### Rigorous computational methods (the certification frontier)

- **[Montanher et al. 2018]** — T. Montanher, A. Neumaier, M. C. Markót, F. Domes, H.
  Schichl, “Rigorous packing of unit squares into a circle,” *J. Global Optim.*
  [Online](https://pmc.ncbi.nlm.nih.gov/articles/PMC6394747/) · local
  `web/montanher-2018-rigorous-packing-unit-squares-circle`. *Interval branch-and-bound
  with sentinels; the rigorous frontier for rotating unit squares, at `n = 3`.*
- **[Markót 2004]** — M. C. Markót, “Optimal Packing of 28 Equal Circles in a Unit
  Square — The First Reliable Solution,” *Numerical Algorithms*.
  [Online](https://link.springer.com/article/10.1023/B:NUMA.0000049472.75023.0a) ·
  **[not retrieved]**.
- **[Markót 2021]** — M. C. Markót, “Improved interval methods for solving circle
  packing problems in the unit square,” *J. Global Optim.* **81** (2021).
  [Online](https://pmc.ncbi.nlm.nih.gov/articles/PMC8550790/) · local
  `web/markot-2021-improved-interval-methods-circle-packing`. *Optimality proofs for 31,
  32 and 33 circles.* **Open access** — an earlier pass recorded it unretrieved without
  testing.

### Transversal / hitting-set theory

- **[Basic-Slivkova 2018]** — Bojan Bašić and Anna Slivková, “On optimal piercing of a
  square,” *Discrete Applied Mathematics* **247** (2018), 242–251.
  [Online](https://doi.org/10.1016/j.dam.2018.03.048) · local
  `papers/basic-slivkova-2018-optimal-piercing-square`. *Defines the piercing number of
  all unit-square poses in a square, applies it directly to `s(n)`, and derives a
  case-specific `n=61` bound that is weaker than Nagamochi’s 2005 general bound.*
- **[Caoduro–Sebő]** — Marco Caoduro and András Sebő, “Packing, Hitting, and Colouring
  Squares,” arXiv:2206.02185. [Online](https://arxiv.org/abs/2206.02185) · local
  `papers/caoduro-sebo-packing-hitting-colouring-squares`. *`τ/ν ≤ 6` for unit squares
  under arbitrary rotation.*
- **[Wegner-CE 2026]** — “Counterexamples to Wegner’s Conjecture for Rectangles,”
  arXiv:2606.17854. [Online](https://arxiv.org/abs/2606.17854) · local
  `papers/wegner-counterexamples-rectangles`. *Refutes `τ ≤ 2ν − 1` for rectangles;
  squares untouched.*
- **[Martin 2000]** — Greg Martin, “Compactness Theorems for Geometric Packings,”
  arXiv:math/0005054. [Online](https://arxiv.org/abs/math/0005054) · local
  `papers/martin-2000-compactness-theorems-geometric-packings`.

### Asymptotic wasted-space literature

- **[Erdős–Graham 1975]** — P. Erdős and R. L. Graham, “On packing squares with equal
  squares,” *J. Combin.
  Theory Ser. A* **19** (1975), 119–123; this copy is Stanford tech report CS-TR-75-483.
  [Online](http://i.stanford.edu/pub/cstr/reports/cs/tr/75/483/CS-TR-75-483.pdf) · local
  `papers/erdos-graham-1975-on-packing-squares-with-equal-squares`.
- **[Roth–Vaughan 1978]** — K. F. Roth and R. C. Vaughan, “Inefficiency in packing
  squares with unit squares,” *J. Combin.
  Theory Ser. A* **24** (1978), 170–186 (received 1 Nov 1976; Imperial College London).
  [Online](https://www.sciencedirect.com/science/article/pii/0097316578900055) · local
  `papers/roth-vaughan-1978-inefficiency-packing-squares`. *The only lower bound in the
  asymptotic literature.* **Retrieved 2026-08-22**; ScienceDirect still refuses
  automated clients, so the copy was supplied directly.
  The archived transcription is deliberately **partial** — abstract, introduction and
  Theorem read from the page image; the 1978 scan’s OCR is too degraded to transcribe
  Sections 2–7 without reconstructing mathematics.
- **[McClenagan 2026]** — Rory McClenagan, “Optimally Packing a Large Square by Unit
  Squares,” arXiv:2602.01484. [Online](https://arxiv.org/abs/2602.01484) · local
  `papers/mcclenagan-2026-optimally-packing-large-square`.
- **[Wang–Dong–Li 2016]** — Shuang Wang, Tian Dong, Jiamin Li, “A New Result on Packing
  Unit Squares into a Large Square,” arXiv:1603.02368 (Jilin University).
  [Online](https://arxiv.org/abs/1603.02368) · local
  `papers/wang-dong-li-2016-new-result-packing-unit-squares`. *The `O(x^{5/8})` step,
  for both the packing-waste and covering-waste problems.*
- **[Arslanov–Bui 2025]** — M. Z. Arslanov, H. D. Bui, “Note on ‘efficient packings of
  unit squares in a large square’,” *Discrete Comput.
  Geom.* (2025),
  [doi:10.1007/s00454-025-00767-w](https://doi.org/10.1007/s00454-025-00767-w).
  **[not retrieved]** — Springer; cited by **[Waste-0.6 2025]**. *Current continuation
  of the Kearney–Shiu `δₙ`/`n_r` line.*
- **[Good-Squares 2025]** — “Square Packing with Asymptotically Smallest Waste Only
  Needs Good Squares,” arXiv:2504.09489. [Online](https://arxiv.org/pdf/2504.09489) ·
  local `papers/square-packing-good-squares-2504.09489`.
- **[Waste-0.6 2025]** — “Square packing with O(x^0.6) wasted area,” arXiv:2508.04603.
  [Online](https://arxiv.org/pdf/2508.04603) · local
  `papers/square-packing-x06-wasted-area-2508.04603`.

### Record catalogues (where the numbers actually live)

- **[Kingbird]** — “Squares in Squares,” exact minimal polynomials, rigidity flags, SVG
  layouts. [Online](https://kingbird.myphotos.cc/packing/squares_in_squares.html) · local
  `web/kingbird-squares-in-squares`.
- **[Kingbird-compared]** — “Older / Alternative Packings”: which record fell to which
  method, and when.
  [Online](https://kingbird.myphotos.cc/packing/squares_in_squares__compared.html) ·
  local `web/kingbird-squares-in-squares-compared`.
- **[Ellsworth SVG]** — `square-11.svg`. Its XML comments carry David Ellsworth’s
  provenance notes, the two contact equations, the derived constants, and the
  exact-solution history.
  **The single most information-dense source found on this case.**
  [Online](https://kingbird.myphotos.cc/packing/square-11.svg) · local
  `papers/kingbird-square-11-provenance.svg`.
- **[Friedman Center]** — Erich Friedman’s Packing Center, squares page.
  [Online](https://erich-friedman.github.io/papers/squares/squares.html) · local
  `web/friedman-packing-center-squares`.
- **[Kingbird]** is also the clearest source on *proof status*: entries carry an
  explicit “Proved by …” line where one exists, and `n = 11` carries none.
  Its records are live — several were improved by David Ellsworth as recently as
  February 2026.
- **[Wikipedia]** — “Square packing.”
  [Online](https://en.wikipedia.org/wiki/Square_packing) · local
  `web/wikipedia-square-packing`.

### The squared-square dissection tradition (a different problem, for contrast)

- **[BSST 1940]** — R. L. Brooks, C. A. B. Smith, A. H. Stone, W. T. Tutte, “The
  dissection of rectangles into squares,” *Duke Math.
  J.* **7** (1940), 312–340. [Online](https://projecteuclid.org/euclid.dmj/1077492259) ·
  **[not retrieved]**.
- **[squaring.net BSST]** — the precise Smith-diagram correspondence.
  [Online](http://www.squaring.net/history_theory/brooks_smith_stone_tutte_II.html) ·
  local `web/squaring-net-brooks-smith-stone-tutte-II`.
- **[squaring.net Sprague]** — priority for the first published perfect squared square.
  [Online](http://www.squaring.net/history_theory/sprague.html) · local
  `web/squaring-net-sprague`.
- **[CPSS 2013]** — “Compound Perfect Squared Squares of the Order Twenties,”
  arXiv:1303.0599. [Online](https://arxiv.org/abs/1303.0599) · local
  `papers/compound-perfect-squared-squares-1303.0599`.
- [squaring.net — Simple Perfect Squared Squares, Order 21](http://www.squaring.net/sq/ss/spss/o21/spsso21.html)
  — Duijvestijn’s unique lowest-order example.
- [Trinity Mathematical Society — The Squared Square](https://tms.soc.srcf.net/about-the-tms/the-squared-square/)
- [Wolfram MathWorld — Perfect Square Dissection](https://mathworld.wolfram.com/PerfectSquareDissection.html)

### Expository

- [xkcd 2740, “Square Packing”](https://www.explainxkcd.com/wiki/index.php/2740:_Square_Packing)
- [Stand-up Maths, “The Insane World of Polygon Packings”](https://www.youtube.com/watch?v=jWT08JVb-fk)
- [Wikimedia Commons: Packing 11 unit squares in a square with side length 3.87708359…](https://commons.wikimedia.org/wiki/File:Packing_11_unit_squares_in_a_square_with_side_length_3.87708359....svg)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
