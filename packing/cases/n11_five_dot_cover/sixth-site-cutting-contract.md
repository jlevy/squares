# Sixth-Site Feasibility and a Bounded Exact Cutting Loop

**Design analysis, 2026-09-09.** Exp151 completely refutes D plus x149 at direction 6,
after six zero deficits.
Its strict escape is a second retained core avoiding D and the selected patches.
This note admits the mathematical two-escape screen and describes a conditional later
cutting loop. No new target geometry is evaluated.

## Current H150/exp152: Two Escapes Only

Bind exp149’s blob `83ec897738d6d1b228623c3ac4c10cd9170d5940` and exp151’s blob
`46d34b1e295d9f5178379b02780a8c598c1a73e5`, together with their implementation and
endpoint/wall sources.
The latter receipt must be the complete fixed-six-dot refutation at source
`c8cd38dad502c78840144bcae42df4294ba7f3d0`, with consecutive directions 0 through 6,
zero deficits before the last, and a positive final deficit.
No new cover or escape search is part of this screen.

Replay exp149 against original D and its selected patches.
Replay exp151 against the correctly augmented D plus x149 and those same patches.
Construct the two closed B-core squares Q0 and Q1 in their saved world coordinates and
directions. The mathematical question is exactly whether I2=Q0 intersect Q1 is nonempty.

Accept nonemptiness with the exact closed intersection, its dimension, and the mean of
its distinct vertices, independently verified to lie in both cores.
Point and segment intersections are valid.
Refute nonemptiness only when the intersection is empty and independent strict
square-square SAT agrees.
An intersection/SAT disagreement is invalid.
Nonempty proves only that these two witnesses admit a common sixth site, not that the
site covers the residual domain.

Use `owner_footprints.convex_polygon_intersection`, with point/segment controls; the
independent union engine’s area-only intersection deliberately discards such sets and
cannot decide this question.
Empty refutes every fixed-D-plus-one-site cover of the selected relaxed tuple.
It does not refute arbitrary six-dot sets, weighted certificates, the owner tuple, or
n11. This design admission is separate from the forthcoming source/test admission and
target result.

## The Exact Feasibility Reformulation

Let R be the family of all closed B-cores on the complete retained net whose centres lie
in the strict residual container and whose cores avoid D and the four selected closed
owner patches. Define

$$I_* = \bigcap_{Q\in R} Q.$$

A point p makes D plus p a cover of this relaxed domain **if and only if** p lies in I*.
This is a convex feasibility problem in two coordinates, even though the family R has
infinitely many possible centres.
The original D and owner tuple remain fixed.
A nonempty I* may be a polygon, segment, or single point.

Every actual negative oracle output is a member of R. Its additional strict avoidance of
the tested sixth site says p is outside that closed Q. Therefore intersecting the
retained feasible-site polygon with Q is a sound cut and removes the tested point.
It never removes a point from I*.

## Why Three Cores Can Certify Impossibility

If I* is empty, there is an empty intersection of finitely many members of R: anchor the
argument on the compact retained Q0, and take a finite subcover from the relative open
complements of the other cores.
A minimal finite empty family then has at most three members by the following planar
convexity argument.

If a minimal empty family had at least four sets, for four chosen indices i take a point
xi in every set except the ith.
Four planar points have an affine dependence; splitting its positive and negative
coefficients gives a point in the convex hulls of two disjoint groups of those points.
For any set, one group omits its exceptional xi, so that group’s convex hull lies in the
set. The common point would lie in every set, a contradiction.
Thus at most three closed cores suffice.
This is the planar Helly conclusion, with the compactness step made explicit rather than
assuming the infinite-family version automatically.

The strict residual domain is open.
Any finite empty intersection of compact cores has positive separation from simultaneous
feasibility, so sufficiently small perturbations of their centres retain emptiness.
Rational centres are dense in the admitted strict domain and the net directions are
rational. Consequently a rational two- or three-core obstruction exists whenever this
fixed-D-plus-one-site family is infeasible.

These facts describe the size of a final certificate, **not the number of oracle
iterations needed to find it**. An oracle can supply redundant or weak cuts; vertex
means can converge toward a boundary feasible point without reaching it.
No three-iteration termination theorem follows.
Three cores also need not be pairwise disjoint: pairwise intersections can be nonempty
while their common intersection is empty.

## Prospective Bounded Loop, Only After a Nonempty exp152

Freeze the initial two-core intersection and a new source/experiment before the loop.
The proposed first version permits at most eight new site candidates and one 240-second
internal budget shared by the entire loop, with a 300-second external process bound plus
the coordinator’s two-second termination grace.
Parse the bound inputs once.
Every oracle, intersection, replay, and final verdict uses the same absolute deadline;
there is no per-candidate reset.
The launch must fit that full bound inside the allocated phase.
No budget or iteration count changes after observing a result.

For each iteration:

1. Retain the full exact intersection of all saved witness cores, including
   lower-dimensional cases.
   If empty, retain and replay that complete finite witness obstruction; report the
   fixed-D family refuted.
   Helly guarantees that a subfamily of at most three exists, but finding and
   independently replaying such a smaller certificate is a separate task.
   Do not report a specific minimal obstruction until it has been identified.
2. Otherwise choose the mean of the distinct intersection vertices, verify its closed
   membership in every saved core, and require a new candidate.
   A repeated candidate after a valid strict cut is an invariant failure.
3. Invoke the full 361-direction D-plus-p exact union oracle at ceiling 1023. Complete
   zero deficits prove a valid sixth site.
   On the first positive deficit, require a new independently replayed strict escape and
   append its closed core to the witness family.
   Confirm that it excludes p before cutting.
4. Atomically checkpoint the exact new intersection and retained evidence inside the run
   before any next candidate.
   This is one predeclared experiment with immutable source, not a Git publication
   between iterations. On iteration or time exhaustion, return unresolved with the
   remaining feasible-site polygon and all witnesses.
   Never infer infeasibility from a small area, thin segment, repeated float estimate,
   or a stopped loop.

Check the intersection produced by the last permitted cut before declaring the iteration
cap unresolved, provided the shared deadline still permits its required replay.
Preserve exact checkpoints after completed iterations; external termination can
otherwise leave no receipt for the current incomplete operation.
The candidate rule remains the vertex mean used by exp152. An area-centroid rule and a
quantified area-reduction theorem are unnecessary for this bounded contract.

Both terminal outcomes are meaningful: a cover excludes eleven squares in this owner
branch; an empty intersection refutes every possible location of one extra site while
preserving D. The latter is still about the footprint relaxation, not a physical packing
construction.
Even a complete failure does not rule out moving the original five sites or
using an atomic measure with exact normalized mass below seven.

## Minimal Source Reuse and a Possible Later Alternative

The current six-dot CLI intentionally fixes its added site to x149. Do not mutate its
exp149 evidence object or pretend a new site was that saved escape.
A later loop should extract a small reusable cover function accepting one explicitly
bound six-site candidate and shared deadline, while keeping the existing fixed CLI
intact. Each candidate receipt must identify the intersection and witness prefix that
generated its site. Existing exact union, extraction, membership, SAT, and closed
clipping suffice; there is no need for an LP, generic dot search, or owner-frame
enumeration in the loop.

An eventual complete direct construction is also mathematically available.
At one residual direction, intersecting the squares over every D-missed admissible
centre x is equivalent to the four support inequalities

$$\sup_x u\cdot x-h\le u\cdot p\le\inf_x u\cdot x+h,$$

and the same inequalities for v. The existing exact residual decomposition could provide
those extrema from component closures; directions with no admissible centre impose no
constraint. Intersecting the resulting inequalities over all 361 directions computes I*
directly, including boundary feasible sites.
This would need its own admitted full-domain support instrument and budget.
It is a later completeness option, not part of the tiny screen or a reason to expand the
current implementation before its result.

The global routing gap and T023’s scope remain unchanged.
Old five-dot masks cannot be reassigned to a changed site set, and symmetry reuse must
transport the whole certificate or witness family.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
