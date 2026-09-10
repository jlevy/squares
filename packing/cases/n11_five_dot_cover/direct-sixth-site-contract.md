# Direct Sixth-Site Feasibility Versus a Bounded Candidate Loop

**Selected design, 2026-09-09.** Exp152 returned a nonempty two-dimensional
intersection. H151/exp153 now tests direct support-extrema feasibility; its target
remains unrun. This is a design decision based on retained source and measurements; no
new target geometry has been evaluated.
The exp152 source admission is separately recorded in
[the retained review](sixth-site-screen-source-admission.md).

## Exact Characterization

Keep D and the selected tuple (0,0,0,7) fixed.
At each of the 361 retained residual directions, let U be the open container-centre
domain minus the nine closed collision polygons: four selected owner patches and the
five original dots. For its orthonormal axes u,v and h=B/2, a common sixth site p must
satisfy

$$\sup_{c\in U}u\cdot c-h\ \leq\ u\cdot p\ \leq\ \inf_{c\in U}u\cdot c+h,$$

and the same inequalities for v. If U is empty, this direction contributes no
constraint.
These four inequalities are necessary and sufficient for p to belong to every
closed B-core at that direction whose centre is in U. Intersecting them over all 361
directions therefore computes exactly the feasible-site set I*, including a possible
segment or point.

Initialize with the nonempty two-core intersection I2 from exp152. Those two actual
D-missed cores already contain I*, so this does not restrict the true answer.
The instrument can bind and replay the same four source receipts and reconstruct I2 with
the admitted helpers; a new exp152 parser is unnecessary.
All operations must share the new experiment’s single absolute deadline, including
reconstruction and replay.

## Why the Existing Decomposition Supplies Exact Extrema

The inspected `multi_owner_domains.vertical_decompose` cuts at polygon vertices and all
isolated edge intersections.
Within each open slab, every relevant boundary ordering is constant.
It merges closed occupied vertical intervals, including tangencies, then emits the
closures of the positive-width free strips.
The interior of every emitted full-dimensional polygon lies in U. Away from the finitely
many vertical cut lines, these interiors exhaust U. A point of U on a cut line has an
open free neighbourhood, so it is a limit of points in neighbouring strips.
Consequently the finite union of the emitted component closures is exactly the closure
of U.

This equality is the premise needed for negative inference.
A mere closed overapproximation would not suffice: it could impose constraints from
unattainable centres and falsely remove every site.
The source’s slab construction supplies the stronger equality.
This argument should be part of the new instrument’s mathematical admission, with
existing decomposition controls and a small focused support test set.

Take extrema over **all vertices of all component closures**. `component_means` alone
cannot provide these extrema.
A support-attaining vertex may be a forbidden tangency, but it is a limit of strict
admissible centres. Requiring a site to belong to every closed core at strict centres is
equivalent, by continuity, to requiring the same for these limits.
Including such boundary extrema is exact.

Discarding zero-area decomposition pieces is safe because U is open in the plane: there
is no isolated line or point of strict admissible centres.
In contrast, the feasible-site intersection must preserve zero-dimensional and
one-dimensional sets.
Use the existing closed half-plane clipper, not an area-only intersection routine.

## Smallest Prospective Instrument and Verdicts

Add one fixed-tuple support adapter.
Reuse bound input loaders, `core_offsets`, the exact container and Minkowski collision
constructors, `vertical_decompose`, closed clipping, and the existing six-site
independent union/replay routines.
Construct only the nine original-D obstacles at each support direction.
There is no 64-class mask broadcast, tuple enumeration, candidate bank, LP, or generic
dot-search interface.

For each nonempty direction, retain its index, exact axes, component count, four
extrema, and the component/vertex that attains each extremum.
Retain the exact four half-planes and the resulting closed site intersection.
A support vertex is labelled as a closure attainer, not as a strict escape.
The final source review must check the minimum/maximum signs explicitly.
Lower bounds use the maximum centre projection; upper bounds use the minimum centre
projection.

- **An empty intersection after any processed prefix is a complete family refutation.**
  The retained exact necessary half-planes, source-bound extrema, and closed clipping
  supply the proof. Unprocessed directions cannot restore a point.
  An independently replayable rational half-plane infeasibility certificate is a useful
  compact audit supplement, but is not a substitute for the closure-domain premise.
- **A nonempty intersection after fewer than 361 directions is unresolved.** Preserve it
  as a necessary-site region; neither its area nor its dimension supplies a verdict.
- **A nonempty intersection after all 361 directions supplies a candidate.** Choose the
  mean of its distinct vertices, verify every retained closed inequality, and
  independently run all 361 exact union checks with D plus that site and ceiling 1023.
  Accept a cover only if all deficits are zero and the shared deadline still permits the
  final checks. A positive deficit contradicts the completed support construction and is
  an invalid/inconsistent result requiring preserved evidence, not a reason to select
  another site within this experiment.

Freeze one internal 240-second budget after input loading and an external 300-second
whole-process guard plus the existing termination grace.
The internal clock covers I2 replay, support construction, candidate membership,
optional positive union confirmation, and terminal verification.
Atomic completed-support-direction checkpoints preserve progress; they are writes within
one immutable-source experiment, with no clock reset.
Confirmation progress is retained on cooperative return; an external kill can leave only
the last support checkpoint.
A late or externally killed run does not acquire a complete verdict.
If positive confirmation returns cooperatively without finishing, retain its support
result, candidate and completed union prefix, but leave cover acceptance unresolved.
An external kill during confirmation can leave the candidate unset in the retained
support checkpoint; it can be reconstructed from the exact final region later.
No retry or adaptive candidate loop is part of this slice.

An empty support intersection need not come with an identified pair or triple of strict
escape cores. Closure attainers are not automatically strict witnesses.
If a short actual-core obstruction is desired later, move appropriate attainers
rationally toward their free-component interior means, independently replay the
resulting cores, and verify that their common intersection remains empty.
The Helly existence argument does not identify that certificate or license labelling
boundary vertices as escapes.

## Cost and Information Gain

The direct method performs at most 361 decompositions of nine small collision polygons,
then at most one 361-direction, ten-obstacle union confirmation.
An eight-candidate loop can require eight such full union passes and still remain
unresolved. The direct method also avoids repeated escape extraction and candidate
provenance machinery.
Its new mathematical obligation is the complete-domain support argument above; its
implementation is a fixed two-dimensional half-plane intersection around existing
geometry.

Retained measurements make a 240-second bounded attempt reasonable, but do not establish
its runtime: exp145’s nine-obstacle full-net union took about 38.74 internal seconds;
exp149’s first-direction test took about 0.085; exp151’s seven ten-obstacle checks and
escape took about 0.712. Full source-bound process times for exp149 and exp151 were much
larger, so the external guard must continue to cover loading.
Exp148 spent about 66.18 seconds in its incomplete seed bank with no completed seed.
Its source rebuilds and tests 64 class/corner collision polygons for each candidate
centre, independently replays SAT against footprints with many vertices, and constructs
Cartesian-product bitsets.
There are no retained per-stage timings distinguishing decomposition from broadcast.
Calling broadcasting the measured bottleneck would overstate the evidence.
The direct instrument omits that work entirely and can record decomposition versus
projection time during its one registered pass.

Either terminal result remains about this fixed D and selected footprint relaxation.
A confirmed sixth site can exclude eleven squares in the selected owner branch under the
admitted snapping and four-distinct-selected-owner premises.
It does not settle the remaining owner labels or global routing.
An empty I* refutes preserving D while adding one site; it does not refute repositioning
six sites, mass-below-seven weighted certificates, or a tighter owner model.
No old D witness masks or D4 invariance transfer to an arbitrary new six-site
certificate. T023 and the global n11 bound do not change merely because this conditional
experiment is selected.

The structure of a later obstruction matters for weighted continuation.
Three pairwise-intersecting cores with empty triple intersection forbid one new atom,
but their three witness constraints alone admit added mass 3/2: put weight 1/2 at one
site in each pair intersection.
Every core then receives unit weight.
This does not certify the rest of the residual family.
In contrast, a disjoint pair forces added nonnegative mass at least two: the two core
masses sum to at most the total added mass.
Since both cores miss all five original sites, preserving the five original unit atoms
would then require total mass at least seven.
Thus an empty two-core screen also supplies that stronger fixed-five-unit-atoms
obstruction, whereas a general empty I* need not.
No three-core obstruction alone should be reported as refuting all weighted
continuations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
