# Review: The Fibonacci-Torus Contact Geometry

An independent reconstruction confirms a bounded version of the abstract’s
contact-family minimum and its linear stability estimate.
In the explicit family below, on $u\in[9/25,37/100]$ and $L\in[387/100,389/100]$,
exactly two inequalities characterize feasibility, their unique minimum is Trump’s side,
and $L-T_*\geq |u-u_*|/4$. The
[retained verifier](../../../packing/cases/fibonacci_torus/geometry.py) proves the
identities and interval inequalities with rational arithmetic and SymPy.
The [retained receipt](../../../packing/cases/fibonacci_torus/geometry-result.json)
records the passing exact run.
This reconstructs geometry from the repository’s Trump coordinates; it does not verify
the screenshot manuscript’s torus map or identify its full parameter domain.

## The Family and Its Two Clearances

Use the labels and coordinate formulas in
[`trump11/packing.py`](../../../packing/cases/trump11/packing.py), replacing its
prescribed enclosing side by a free variable $L$. Put

$$
c=\frac{1-u^2}{1+u^2},\qquad s=\frac{2u}{1+u^2},\qquad
r=1-(L-3)c,\qquad b=\frac{(1+r)c-1}{s},
$$

$$
v=c-s,\qquad h=\frac{L-1}{s}-r-\frac{(3+b)c}{s},\qquad
x=1+\frac2c-\frac{(L-2)s}{c}.
$$

The six aligned squares have lower-left corners $(0,0)$, $(L-1,0)$, $(x,L-1)$,
$(0,L-1)$, $(1,L-1)$ and $(0,L-2)$. For each of
$(p,q)=(0,0),(b,-1),(1,v),(b+1,v-1),(b+2,-h)$, form the square with origin
$(1,1)+R_\theta(p,q-r)$ and edge vectors $(c,s)$ and $(-s,c)$. Here $u=\tan(\theta/2)$,
so these are unit squares.

The two signed clearances, with zero-based square labels, are

$$
g_1=(L-2)(c+s)-2-s\quad\text{for pair }(1,9),
$$

$$
g_2=-sx+c(L-2)-1+h+r\quad\text{for pair }(2,10).
$$

For $g_1$, square 9 lies beyond square 1 in direction $(-s,c)$. For $g_2$, square 2 lies
beyond square 10 in that direction.
These are the minimum separating-axis projection gaps, including the supporting corner
choices; they are not distances between the centers.
Writing $w=cs$ gives the exact identities

$$
g_1=(c+s)(L-f_1(u)),\qquad
g_2=\frac{1+w-w^2}{cs^2}(L-f_2(u)),
$$

where

$$
f_1(u)=\frac{6u+4}{1+2u-u^2},\qquad
f_2(u)=\frac{4(u+1)(u^6-2u^5+2u^4+7u^3-2u^2+u+1)}{D(u)},
$$

$$
D(u)=u^8-2u^7-2u^5+14u^4+2u^3+2u+1.
$$

The Fibonacci determinant therefore has a direct contact interpretation:
$\partial g_2/\partial L=\det(I+wQ)/(cs^2)$ for
$Q=\left(\begin{smallmatrix}0&1\\1&1\end{smallmatrix}\right)$. This identity alone does
not supply the torus representation.

The verifier proves the following on the entire closed parameter rectangle:

- All 44 supporting wall inequalities hold.
- Each of the other 53 square pairs has a separating axis throughout the rectangle.
- For each of the two active pairs, all seven alternative oriented separating-axis
  features are strictly unavailable.
  The remaining feature is exactly $g_1$ or $g_2$.

Thus both directions of the feasibility equivalence hold there:
$\text{feasible}\iff g_1\geq0\text{ and }g_2\geq0$. Boundary contacts remain allowed.
Selection of a convenient axis at a rational reference point supplies no evidence by
itself; the verifier certifies its inequality on the whole rectangle.

## The Minimum and the Cusp Bound

Clearing the positive denominators gives

$$
f_1-f_2=\frac{2uP(u)}{(1+2u-u^2)D(u)},
$$

$$
P(u)=5u^8-10u^7-2u^6+14u^5+12u^4-6u^3+2u^2+2u-1.
$$

The verifier checks this against the exact witness’s polynomial, proves $P'>0$ on the
angle interval and verifies opposite endpoint signs.
Hence there is exactly one crossing $u_*$. It also proves, on the same closed interval,
$f_1'>1/4$ and $f_2'<-1/4$. For $u\geq u_*$, integrate the first inequality; for
$u\leq u_*$, integrate the second.
Since feasibility requires $L\geq\max(f_1,f_2)$, both give $L-T_*\geq |u-u_*|/4$, with
$T_*=f_1(u_*)=f_2(u_*)$. The crossing lies inside the certified side interval, so it is
feasible and is the unique minimizing parameter pair.
Substitution also verifies the published degree-eight polynomial of $T_*$ exactly.

Every sign bound uses Bernstein coefficients on the angle interval.
After mapping it to $[0,1]$, a power polynomial $\sum_j a_jt^j$ of degree $n$ has
coefficients $b_k=\sum_{j\leq k}a_j\binom{k}{j}/\binom{n}{j}$ in the nonnegative
Bernstein basis, whose sum is one.
The smallest coefficient is therefore a lower bound.
All geometric numerators are affine in $L$, so checking the two side endpoints covers
its entire interval.
Denominators receive separate strictly positive bounds.
Two retained negative controls reject a polynomial positive at both endpoints but
negative inside, and a rational function whose denominator has interior zeros.

From `packing/`, the reconstruction emits its complete JSON receipt with
`uv run --frozen --all-extras --group dev python -m cases.fibonacci_torus.geometry`. Its
two refusal controls run with
`uv run --frozen --all-extras --group dev pytest cases/fibonacci_torus/geometry.py`. The
receipt expressly leaves manuscript verification and unrestricted global capture false.

## Physical Symmetry and Global Capture

The eleven original squares have no nontrivial contact-graph automorphism.
The [exact contact atlas](../../../packing/atlas/known-best/contact-structures.json) has
fourteen edges. Its degree-four vertices 6, 8 and 9 have distinct neighbor-degree
multisets $(1,2,3,4)$, $(2,3,4,4)$ and $(1,2,2,4)$, which fix those vertices.
Their neighbors then fix every remaining vertex; the verifier reproduces this as
invariant color refinement to eleven singleton classes.
Consequently a nontrivial action on eleven torus cells cannot preserve the contacts of
the eleven original squares.
The
[uniqueness review](review-2026-10-06-n11-uniqueness-fix-check.md#u-9-non-blocking-exactly-eight-and-the-1984-count)
also checks that the planar packing’s container-symmetry stabilizer is trivial.
The abstract’s action on all 55 unordered pairs concerns labels; only fourteen pairs are
contacting in the plane.

The unrestricted theorem is already
[T-060, with uniqueness T-112](../../../packing/frontier/n-011.md).
Its
[proof, sections 6–8](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md#6-the-exact-d4-reduction-to-case438),
first forces an occupancy case, then captures all 33 placement coordinates in a local
rectangle. The local argument covers 128 derivative branches and allows independently
varying angles and broken contacts.
The family above fixes six orientations, makes the other five equal, and imposes twelve
contacts as identities.
The torus representation can shorten the construction and its family minimum; replacing
the global proof requires an additional reduction that sends every competing packing
into this family without increasing its enclosing side.
A reversible representation of the family supplies no such reduction.

The corresponding obstacle at 17 is larger.
The
[current witness](../../../packing/frontier/n-017.md#three-orientation-classes-and-a-correction)
uses ten aligned squares, six at $+39.8049589798^\circ$ and one at
$-36.6237863834^\circ$. The
[endpoint analysis](../n17-optimality-explainer.md#the-local-half) has three individual
slides and a free square, yielding six free directions; its target is a family.
One point on a fixed two-dimensional torus cannot continuously parameterize an open
six-dimensional family reversibly.
An extension needs additional marks or varying torus data.
This does not obstruct an encoding with enough parameters, and it does not decide the
still-open global optimum at 17.

The next useful checks are to verify the manuscript’s forward and inverse maps on all
corners and lattice seams, then compare its exact parameter domain with the rectangle
certified here. For proof simplification, a bounded test should try to recover this
two-clearance argument from each of the existing 128 local branches without imposing the
common-angle or persistent-contact assumptions.
Any omitted branch is an unresolved proof obligation, even when its planar contact graph
resembles the retained optimum.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
