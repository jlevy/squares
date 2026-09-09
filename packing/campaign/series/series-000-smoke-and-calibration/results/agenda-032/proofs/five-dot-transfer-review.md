# Exp143 Five-Dot Candidate: Mathematical Review

**Status:** independent analytic and saved-atom scrutiny by the existing GPT-6 Astra
agent at extra-high reasoning, 2026-09-09. The coordinator completed a separate
algebraic review before exp144: the endpoint vertices satisfy every intermediate
quarter-square inequality, the net shrink is strict, and positive equal-weight coverage
gives the five-dot pigeonhole exclusion.
No coverage target, numerical optimization, or full-net replay was run here.

The candidate is potentially a conditional packing certificate.
It is not yet a certificate: the producer checked nine residual orientations, and its
exact-validation field is null.
The following reduction specifies the decisive exact check.

## The Exact Candidate

The endpoint arm in the saved exp143 receipt contains precisely five atoms:

| Site | Coordinates |
| --- | --- |
| 1 | $(73/75,187/90)$ |
| 2 | $(793/450,43/15)$ |
| 3 | $(48/25,48/25)$ |
| 4 | $(187/90,73/75)$ |
| 5 | $(43/15,793/450)$ |

Every weight is $\beta=1000001/1000000$, so $M=5\beta=1000001/200000$. Independent
rational arithmetic confirmed that all sites lie in the container and outside the closed
union of the four saved endpoint polygons.
No additional banked-mass subtraction is needed.

For a generic rational cover, a verified full-domain minimum $m$ would give effective
mass $M/m$, and the seven-core contradiction requires

$$m>M/7=1000001/1400000.$$

The phrase “$m>5/7$” is exact only after dividing these weights by $\beta$. There is a
stronger simplification for this particular candidate: every core’s mass belongs to
$\{0,\beta,2\beta,\ldots,5\beta\}$. Therefore a positive exact minimum is at least
$\beta$. A positive full-net result certifies five unit piercing dots after dividing by
$\beta$, with total mass five.
If every orientation domain is empty, the branch is already impossible; an empty
individual orientation is vacuous, not a zero score.

This needs feasibility only.
Neither an LP dual bound nor proof of the numerical optimum is required.
Five disjoint-core demands exhaust five dots, so six or more disjoint residual cores are
impossible. The target branch requires seven.

## Which Branch This Would Exclude

At each physical corner, use the reflected image of the bottom-left owner class with
mark $m=(3152/3175,2336/3175)$ and signed-axis sector zero.
Reflect the footprint by $(x,y)$, $(q-x,y)$, $(x,q-y)$, and $(q-x,q-y)$, with $q=96/25$.
This is one prescribed combination of four distinct owners from the corner-pair theorem.
That theorem does not force every packing into this combination.

For the bottom-left endpoint polygon, the first ray is $(1,0)$ and the last retained ray
in the closed sector is

$$
(c,s)=\left(\frac{207107000000}{292893309449},
\frac{207106690551}{292893309449}\right).
$$

The rational checks give $c^2+s^2=1$ and $0<s<c$. With $h=B/2$ and $t=c/(1+s)$, the
independently derived vertices

$$m,\quad m+h(c,s),\quad m+h(t,1),\quad m+h(0,1)$$

match the saved polygon exactly.
The reviewed endpoint-intersection proof puts this polygon inside every anchored
half-side square from the class’s retained signed axes.
The signed-axis construction puts that anchored square inside its owner core, even when
the mark is on a core boundary.
Reflection transfers the proof to the other three corners.
Endpoint selection must continue to use the full owner manifest, with the rational
near-45-degree endpoints kept on their exact sides of the sector boundary.

## Full-Angle and Boundary Transfer

The reader must use all 361 canonical residual orientations and the saved nonnegative
weights unchanged. The five-dot set has diagonal and central symmetry, but lacks
horizontal and vertical symmetry.
The four-footprint union has horizontal and vertical symmetry, but lacks diagonal
symmetry. These facts do not justify an 181-direction fold for the pair.
A simultaneous global symmetry may transport a completed certificate to another branch;
it cannot repair an omitted direction in this replay.

For each residual orientation, rotate each footprint into the core-axis coordinates and
form its closed collision polygon $F_i=A_i+[-h,h]^2$. The required centre domain is
$\operatorname{int}(C)\setminus\bigcup_iF_i$. The exact vertical decomposition covers
this open set by separate positive-area polygon closures.
Retaining separate pieces prevents a fictitious bridge across an occupied gap.
Dropping contact-only components is safe for the strict physical domain.

The canonical-core transfer uses the existing bound

$$B(1+D)=899996306539/900000000000<1,
\qquad D=207107/90000000.$$

Each physical parent therefore contains its selected rational-net core strictly.
The four owner footprints lie in their selected cores.
Every remaining selected core is compact, strictly inside its own parent and the
container, and positively separated from the four footprints.
Its centre has an open feasible neighbourhood.
Nonnegative atomic mass at a closed-core event boundary is at least the mass of
sufficiently near generic placements, so exact coverage of the reachable open event
cells suffices.

This transfer conditions on the selected cores’ owner classes.
It does not require the continuous-angle parents themselves to lie in the rational
sector interval.

## How to Extend a Successful Certificate

The most direct extension is containment: a certificate for occupied union $A$ covers
any other class with guaranteed union $A'\supseteq A$, because its residual domain is
smaller.
Check union containment, rather than comparing area or assuming one polygon must
contain its same-index counterpart.
Exact global square symmetries provide more certificates by transforming both the dot
pattern and occupied regions together.

Then reuse the small dot patterns on unresolved classes before solving new LPs.
Five sites give few atomic event lines.
Shared direction geometry and exact uncovered centre witnesses can screen many classes;
a witness that remains outside a class’s footprint union disproves that dot pattern for
the class, without proving that the class is feasible.
Refine or optimize the uncovered classes and keep an explicit coverage ledger for the
exhaustive branch family.
A blind $16^4$ collection of full LP solves is unnecessary.

If the full-net replay finds zero, retain its exact direction and centre as a missing
coverage constraint.
That defeats these five dots on the declared relaxed domain, not the conditional-cover
approach or the impossibility of the branch.
A revised dot pattern or tighter owner-pose condition remains a meaningful next
experiment.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
