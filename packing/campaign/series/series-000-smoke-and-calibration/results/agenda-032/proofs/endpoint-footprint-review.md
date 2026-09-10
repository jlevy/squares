# Endpoint Footprint Proof Review

**Verdict:** the endpoint-intersection claim, explicit vertices, and area formula are
correct under the stated sector-width constraint.
No counterexample was found in this analytic review.
No scientific target or numerical geometry check was run.

**Actual routing:** this is a second derivation by the existing GPT-6 Astra agent at
extra-high reasoning.
The attempted separate GPT-6 Astra reviewer at max reasoning could not start because the
agent thread limit was reached.
This is therefore not an independent-agent review of the enlargement.
The earlier triangle lemma had its separately reported review; that status must not be
transferred automatically to this new polygon result.

## Coordinate Derivation

Translate the owned mark to the origin and rotate the earlier endpoint ray to a=(1,0).
Write the later ray as b=(c,s), with c²+s²=1 and 0≤s≤c. Thus its angular distance from a
is δ∈[0,π/4]. Put h=B/2>0 and t=c/(1+s)=(1−s)/c.

The two anchored squares are

Q_a={0≤x≤h, 0≤y≤h},

Q_b={0≤cx+sy≤h, 0≤−sx+cy≤h}.

Their intersection is exactly the polygon given by these four inequalities:

`x≥0`, `y≤h`, `cy−sx≥0`, `cx+sy≤h`.

To check the omitted constraints: x≥0 and cy≥sx give y≥0; then cx+sy≥0. Substituting
y≥sx/c into cx+sy≤h gives x≤hc≤h. Finally cy−sx≤cy≤ch≤h. The converse containment is
immediate because the four retained inequalities occur among the original eight.

The vertices, in counterclockwise order, are

`(0,0), (hc,hs), (ht,h), (0,h)`.

Indeed, the second vertex is the intersection of cy−sx=0 and cx+sy=h. The third solves
y=h and cx+sy=h. Also c−st=t>0 and ct+s=1, so all vertices satisfy the four
inequalities. Translating and rotating back gives exactly

`m, m+h*b, m+h*(t*a+J(a)), m+h*J(a)`.

The two nonzero shoelace contributions are both h²t: `det((hc,hs),(ht,h))=h²(c−st)=h²t`
and `det((ht,h),(0,h))=h²t`. Hence the area is

`h²*t = h²*(a·b)/(1+det(a,b))`.

The denominator is at least one and c>0 on the specified range; there is no division
singularity. At δ=0 the formula gives the whole h-square, not a degenerate polygon.
At δ=π/4 it gives area (sqrt(2)−1)h². Relative to the triangle’s h²/4, that is a factor
4(sqrt(2)−1), or approximately 65.7% additional area.
With narrower endpoint separation the area is larger still.
These are geometric areas, not guaranteed measure masses.

## Why No Intermediate Square Cuts the Polygon

It remains to check every intermediate angle θ∈[0,δ]. Convexity reduces the problem to
the four vertices. The origin is automatic.
The vertex hb has projections h cos(δ−θ) and h sin(δ−θ), both in [0,h]. The vertex hJ(a)
has projections h sinθ and h cosθ, also in [0,h].

For the remaining vertex h(t,1), the normalized projections are

`f(θ)=t cosθ+sinθ`, `g(θ)=cosθ−t sinθ`.

Here g decreases from 1 to c−ts=t>0. Thus f'=g>0, and f increases from t to tc+s=1. Both
projections stay in [0,1]. Every polygon vertex therefore belongs to every intermediate
anchored square. Since the endpoints themselves occur in the direction family, their
intersection equals the intersection over all retained intermediate directions.
In fact, it equals the intersection over the continuous angular interval between them.

## Endpoint Selection and Boundary Cases

- Assert exact unit lengths, `s=det(a,b)≥0`, `c=a·b>0`, and `s≤c`. Reversed endpoints or
  an incorrect wraparound order violate these guards.
  The derivation also works more widely below π/2, but the instrument should enforce its
  registered π/4 contract.
- Use the full retained owner direction family and its signed unit axes.
  A coarse residual screen’s direction subset is not a valid source for enlarged owner
  footprints.
- Closed sector bins may share a boundary ray.
  This duplicates admissible cases without creating a gap.
  Wraparound ordering must use the sector’s local order, not raw signed angle values.
- A singleton endpoint set gives Q_a exactly.
  An empty endpoint set denotes an empty class; it does not justify inventing default
  endpoints. The current full net has nonempty sectors.
- The slightly overshooting rational 45-degree net endpoint must remain on its exact
  side of the sector boundary.
  Clamping it to 45 degrees changes the contract.
- If a mark lies on a core edge or vertex, the signed-axis construction still has length
  at least h available in both chosen directions.
  When a displacement coefficient is zero, choose a unit signed axis explicitly; a
  library’s zero-valued `sign(0)` must not produce the zero vector.
- The triangle belongs to every anchored square in the whole nominal sector.
  The enlarged polygon intersects only the retained endpoint interval within that
  sector, so it contains the triangle.
  This argument does not require either endpoint to coincide with a nominal sector
  boundary.

## Strict Residual Domain

The footprint is a subset of its owner’s selected closed B-core.
Each selected core is compact and lies strictly inside its unit parent.
Distinct parents have disjoint interiors, so distinct selected cores are disjoint
compact sets and have positive distance.
Every actual remaining core therefore has positive distance from the owner footprint.
Each selected core also lies strictly inside the container: an interior point of a
parent contained in the container is an interior point of that container.

At a fixed residual orientation, write F=rot(footprint)+[-h,h]² and let C be the closed
contained-centre polygon.
Actual residual centres lie in `int(C) \ F`. This is open.
Each actual centre consequently has a two-dimensional feasible neighbourhood, even
though no uniform clearance across all packings is asserted.

Dropping zero-area closures of exterior-half-plane pieces is safe for covering this
strict family: a point strictly exterior through an edge has a neighbourhood on that
side. If a centre also lies on an atom-event line, nearby generic feasible centres
suffice. With finitely many nonnegative atoms, atoms outside its closed core remain
outside under sufficiently small perturbations, while boundary atoms may be lost.
Its mass is therefore at least that of sufficiently close generic placements.
Coverage of all feasible open event cells implies coverage at the actual event-boundary
centre.

This does not prove coverage of every isolated contact admitted by the larger weak
domain C minus int(F). Such contact is unnecessary for the packing argument.
The reader must state which domain it verifies rather than silently asserting the
stronger one. Likewise, a dual survivor filter must require strict separation from the
closed footprint; equality is not a strict survivor.

## Implementation Consequences

The explicit polygon formula and a separately written exact intersection of the two
endpoint squares are suitable independent instrument controls.
Check exact vertex equality after canonical cyclic ordering and the shoelace area
identity. A right-angle endpoint pair must be rejected by the π/4 guard.
Coincident endpoints exercise the square and area conventions; a retained rational
nonzero sector exercises the general case.
These controls would validate implementation, not establish a numerical cover.

No correction to the endpoint formula is needed.
The material cautions are full-owner-net endpoint selection, exact sector ordering,
nonzero signed axes, and the strict-domain scope of event-cell verification.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
