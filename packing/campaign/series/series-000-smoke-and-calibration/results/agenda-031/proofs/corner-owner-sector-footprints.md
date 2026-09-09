# Corner-Owner Sector Footprints

**Status, 2026-09-08:** analytic derivation by GPT-6 Astra at extra-high reasoning,
independently reviewed by GPT-6 Astra at max reasoning.
No numerical target, exact reader, or certified pipeline result accompanies this note.
The $n=11$ bracket is unchanged.

## Ownership Premise

Set $q=96/25$, $K=[0,q]^2$, $B=9977/10000$, and $h=B/2$.
[BC-303’s corner-pair replay](../../agenda-030/bc-303-first-wave-selection.md#3-replay-of-the-corner-pair-theorem-lane-c)
establishes four distinct selected core owners in every hypothetical eleven-square
packing. Each owner’s closed $B$-core contains at least one mark of its corner pair.
The bottom-left marks are

$$
m_1=(3152/3175,2336/3175),\qquad m_2=(2336/3175,3152/3175);
$$

the other pairs are their container-symmetry images.
The replay verifies that each pair’s mass exceeds the available uncovered mass, and that
cross-corner distances exceed $B\sqrt2$. Selected cores lie strictly inside their unit
parents. Mark containment in a core may be on its boundary; no positive clearance is
assumed.

## A Uniform Triangle From One Owned Mark

Write an owner’s core as $P=z+[-h,h]u+[-h,h]v$, with orthonormal axes, and
$m-z=\alpha u+\beta v$, where $|\alpha|,|\beta|\le h$. Choose each signed axis toward
the centre: $e_1=-\operatorname{sgn}(\alpha)u$ and $e_2=-\operatorname{sgn}(\beta)v$.
Either sign is allowed when its coefficient is zero.
The available distances from $m$ along these rays are $h+|\alpha|$ and $h+|\beta|$,
respectively. Consequently,

$$
m+[0,h]e_1+[0,h]e_2\subseteq P.
$$

Swap the rays if necessary so that $e_2$ is the counterclockwise quarter-turn of $e_1$.
Let $\phi$ be the first ray’s angle modulo $2\pi$. For each closed bin
$\phi\in[j\pi/4,(j+1)\pi/4]$, $j=0,\ldots,7$, every such anchored square contains the
radius-$h$ wedge with directions $[(j+1)\pi/4,(j+2)\pi/4]$. Define the rational vectors

$$
\begin{aligned}
r_0&=(h,0),&r_1&=(h/2,h/2),&r_2&=(0,h),&r_3&=(-h/2,h/2),\\
r_4&=(-h,0),&r_5&=(-h/2,-h/2),&r_6&=(0,-h),&r_7&=(h/2,-h/2).
\end{aligned}
$$

With indices modulo eight, the common footprint is

$$
T_j(m)=\operatorname{conv}\{m,m+r_{j+1},m+r_{j+2}\}\subseteq P,
\qquad |T_j(m)|=h^2/4=B^2/16.
$$

Both nonzero vectors lie in the common wedge and have norm at most $h$; convexity proves
containment. Their determinant proves the area formula.
Closed bins cover axis, diagonal, and wraparound boundaries, including marks on core
edges or vertices. Overlapping bin membership is harmless.
Rational net-axis signs and comparisons of absolute coordinates determine bins without
numerical inverse trigonometry.

## Exhaustive Branches and Sound Banking

Two possible owned marks and eight sector bins give sixteen classes per corner.
Choosing one class at each corner gives $16^4=65,536$ raw branches.
Every packing belongs to at least one branch; no enumeration or feasibility pruning has
been run. Owning both marks does not create a second owner.
The four distinct owners come from the premise, not from the sector construction.

Fix a branch and its four triangles $T_i$. Each lies in its owner’s selected core, so it
is both an obstacle for remaining cores and a region whose mass can be counted
separately. This is stronger than containment only in a unit parent.
The actual closed cores are pairwise disjoint because they lie strictly inside
disjoint-interior parents.
Intersecting guaranteed triangles therefore make a branch impossible, even if they only
touch; such pruning requires an exact intersection decision.
Triangle disjointness alone does not establish compatibility of the owners.

For an unpruned branch, let $D_\sigma$ contain every contained $B$-core, over the full
net direction family, whose interior is disjoint from all four triangles.
Allowing touching makes this a safe enlargement of the actual residual family.
A nonnegative atomic measure $\mu$ excludes the branch if

$$
\mu(P)\ge1\quad(P\in D_\sigma),\qquad
\mu(K)-\mu\!\left(\bigcup_iT_i\right)<7.
$$

Indeed, the seven remaining cores avoid the triangle union entirely, so their mass plus
the union’s mass cannot exceed $\mu(K)$. For pairwise disjoint triangles the union term
equals $\sum_i\mu(T_i)$. Using the union avoids accidental double credit.
The simpler condition $\mu(K)<7$ also suffices with residual coverage.

No triangle is guaranteed mass one.
Four distinct owners justify the residual count seven; their tiny guaranteed footprints
do not guarantee a four-unit saving from an unconditional cover.
Every retained branch still needs complete centre coverage and the valid nearest-net
shrink transfer before it yields a packing exclusion.

A branch generally lacks D4 symmetry.
Use its actual stabilizer or the full direction family; a generic D4-folded reader
cannot be reused unchanged.
Container symmetries may identify equivalent whole branches, not independently reorient
their corners.

## Relation to Existing Work and Next Discriminator

[Lane A’s penetration-depth Theorem B](../../agenda-030/lane-a-corner-structure.md#theorem-b-complete-corner-cover-by-penetration-depth-sound-unrun)
obtains parent boxes $[d,1]^2$, then requires separately justified core insets for
banking. The sector lemma directly supplies a core footprint without a penetration
assumption. Corner-pair owners must not be identified automatically with penetration
occupants.

[Stromquist’s Theorem 1, Figures 8–12](../../../../../../resources/papers/stromquist-2003-packing-10-or-11-unit-squares.md)
uses unavoidable-point ownership to force further occupied segments.
This is a published precedent for the strategy; the sector lemma here is a new project
derivation.

The smallest next discriminator fixes only the bottom-left corner and tests its sixteen
classes. Each class seeks complete residual-core coverage with $\mu(K)-\mu(T_j(m))<10$.
All sixteen must pass or be exactly excluded to close that partition globally; one
success excludes only its class.
Failure to find a measure is inconclusive.
This unrun test measures whether guaranteed triangles provide useful gain before funding
the four-corner branch family.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
