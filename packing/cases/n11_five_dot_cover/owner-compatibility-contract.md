# Saved-Escape Owner Compatibility: Mathematical Admission Contract

**Design admission, 2026-09-09.** The proposed BC320 experiment is sound under the
contracts below. This admits a bounded implementation and source review, not an
unreviewed instrument or a target run.
No target geometry, pose compatibility, or new escape has been evaluated here.
The implementation plan is owned by the separate planning lane.

## Fixed Question and Model

Freeze exp149’s axis escape, tuple (0,0,0,7), and the published exp143/exp146 inputs.
Test selected corners in order TR, BL, BR, TL. The hypothesis is

$$\exists c\quad\forall o\in\mathcal F_c\quad\forall z\in Z_{c,o}:
(z+S_o)\cap(x+S_\theta)\ne\varnothing.$$

Here both squares have side B=9977/10000, h=B/2; theta is saved orientation zero; and
$\mathcal F_c$ is the complete retained signed-frame family of the selected class.
The centre sets are closed.
This asks whether some selected owner class excludes the particular residual pose in the
necessary snapped-core model.
It does not ask whether that owner class is impossible, whether the entire tuple is
excluded, or whether D covers its remaining domain.

Every hypothetical unit packing has selected full-net B-cores strictly inside its
parents by the retained $B(1+D_{\rm net})<1$ theorem.
BC303 supplies four distinct such owners containing the corner-pair marks.
Their selected-core classes use the complete finite frame list.
Universal exclusion over that list is therefore sufficient under those existing
premises. The 181 class frames are not a sample standing in for arbitrary continuous
unit-owner angles.
Positive core witnesses do not establish contained unit parents, joint
owner feasibility, or a complete packing.

## Corner and Frame Transport

Use one world coordinate system, with

$$F_{\rm BL}=I,\quad F_{\rm BR}=H,\quad F_{\rm TL}=V,\quad F_{\rm TR}=R,$$

where H(x,y)=(q-x,y), V(x,y)=(x,q-y), R(x,y)=(q-x,q-y). Write F(z)=Lz+b. Transport the
mark and centre polygon by F. For a stored local ray r, choose the right-handed world
frame

$$r_c=Lr\quad(\det L=1),\qquad r_c=L(Jr)\quad(\det L=-1),$$

with second axis $Jr_c$. In the reflected case $Jr_c=Lr$: the positive displacement
coordinates exchange.
Merely reflecting r and recomputing its quarter-turn changes the anchored quadrant under
H/V. Alternatively, retaining both axes (Lr,LJr) is sound, but class replay must use
that same possibly left-handed pair.
Freeze one convention.

Class indices remain the reflected local labels in (0,0,0,7); do not apply a diagonal
class permutation during these corner placements.
Keep local frame provenance plus explicit world axes.
The residual centre and frame remain in their saved world position.

## Exact Separation Test

For each owner frame use the eight signed axes in this fixed order:

$$N=(r_c,-r_c,Jr_c,-Jr_c,u_\theta,-u_\theta,v_\theta,-v_\theta).$$

Repeated geometric axes may be retained; never drop a negative axis without an
equivalent interval test.
With $\rho_o(n)=h(|n\cdot r_c|+|n\cdot Jr_c|)$ and analogous $\rho_\theta(n)$, define

$$\delta_{o,n}=n\cdot x-\min_{z\in Z_{c,o}}n\cdot z-\rho_o(n)-\rho_\theta(n).$$

There exists a strictly separated owner in frame o exactly when some $\delta_{o,n}>0$.
SAT supplies the finite axes, and the existential centre quantifier gives the
**minimum** owner projection.
Replacing it by a maximum is unsound.
Every minimum is attained at a stored rational vertex; choose the lexicographically
first minimizer for reproducibility.

Equality is contact and fails strict separation.
Actual selected cores from distinct parents are positively separated, so strict
separation is the correct necessary condition.
Keep mark containment, centre-set membership, and owner containment in the container
closed, as safe enlargements of the physical model.
Keep nonempty point and segment centre sets; the extremum formula is valid for them.

## Input Authority and Exhaustiveness

Bind the clean implementation revision and exact published input blobs.
The exp149 input must be the completed selected-cover refutation for (0,0,0,7), with
matching endpoint and wall sources.
Its escape must name the positive-deficit direction and resolve to the retained exact
direction. Replay that saved centre against the open residual container, the five closed
dot-hit conditions, and the four selected closed patches before using it.
There is no new union-area computation or residual search.

For exp146, reuse the admitted loader and expose the saved frame/centre data.
Match all sixteen class identities and frozen settings, and every selected class’s frame
sequence to the generated full manifest: ray, canonical orientation index, quarter-turn,
and complete folded-source list.
A count of 181 alone is insufficient.
Duplicates, omissions, unresolved frames, and inconsistent dispositions are invalid.
The frozen selected classes are possible; do not manufacture a universal result from an
absent polygon or empty list.

The negative inference additionally needs each saved Z to equal, or safely enclose,
$K_r\cap(m+[0,h]r+[0,h]Jr)$. For this exact-source experiment that premise comes from
the admitted exp146 constructor and its bound receipt.
The reused loader checks frame provenance, dimensions, and support consistency, but does
not independently reconstruct every centre set.
Do not describe those structural checks alone as proving Z exhaustive.
A future unadmitted receipt would need its own constructor admission or a reconstruction
with the existing centre-set helper.
Checking only that its vertices lie in K and Q proves the wrong inclusion for universal
exclusion.

## Positive Witness Replay and Results

For a positive slack, retain the frame, signed axis, minimizing centre, projection
bound, and slack.
Pull the centre back by the inverse corner map and independently verify

$$z\in K_r,\qquad 0\le(z-m)\cdot r\le h,\qquad
0\le(z-m)\cdot Jr\le h.$$

These are the physical closed B-core container and the exact class displacement box.
Verify the owned mark lies in the constructed B-core and use the existing polygon/core
SAT replay to check strict disjointness from the saved residual.
This replay must agree with the optimization predicate.
A failed replay is invalid, not a reason to hide the witness and try another centre.

| Per-class result | Required evidence |
| --- | --- |
| Compatible in the snapped-core model | One positive slack and a passing independent witness replay; early frame exit is permitted. |
| Incompatible with this residual | Every required nonempty frame and all signed axes completed, all slacks nonpositive. Store the exact full maximum and attaining row. |
| Partial or invalid | An unfinished enumeration, deadline, missing premise, or failed guard; no universal conclusion. |

The experiment accepts after one complete incompatible class.
It refutes the hypothesis only after four compatible class witnesses.
Otherwise it is unresolved or invalid.
Stop at the first decisive incompatible class; do not add classes, residual poses, or a
second attempt. A compatible class’s inspected prefix maximum is not its full maximum.
Separate visited frames, exhausted frames, checked axes, and planned counts.

For a complete incompatible class, a strictly negative maximum proves that a
neighbourhood of the saved residual centre is also excluded.
A zero maximum establishes the exact-pose result but not positive-area improvement.
Neither outcome alone closes a cover.

For the receipt interface, one row per fully evaluated frame is sufficient: exact
maximum over all eight signed axes, attaining axis and minimizing vertex, axes checked
equal to eight, and complete corner/frame provenance.
There are at most 724 frame rows.
Derive a complete class maximum from those rows.
Storing all eight slacks inside each row is optional; the bound inputs and admitted
evaluator permit their replay.
If a class exits early on a positive axis, retain that witness and its actual prefix
separately. Zero allowed frames in a selected class are invalid for this frozen
possible-class experiment, not a vacuous acceptance.

## Budget and Minimum Admission Controls

The 90-second shared internal clock starts after input binding/parsing and covers saved
escape replay, corner transport, support calculations, witness replay, and the complete
decision before return.
JSON serialization, fsync and atomic publication fall under the 120-second external
bound. It never resets per class.
Check it during frame/axis traversal and after final work before any complete verdict.
The 120-second external process bound covers loading and output publication too.
The larger BC320 insight slice remains 30 minutes.
Timeout is operationally unresolved, with no automatic extension or target retry.

Use a fresh atomic-on-return JSON receipt.
Preserve exact fractions, source bindings, corner/class/frame provenance, every
completed universal-test row, positive witnesses, counts, timings, and errors.
External termination may leave no JSON; retain process status and receipt absence rather
than interpreting either as a mathematical result.

Before publication, controls must catch: min/max reversal; strict tangency and positive
separation; oblique H/V transport with swapped displacement axes; point/segment extrema;
omitted or duplicate frames; wrong mark/sector/source; failed witness membership; and
expiry after the final geometric operation.
Synthetic records can have smaller frame families through a clear test seam; the target
entry still requires the exact frozen family.
No broad geometry engine, all-angle unit-owner claim, or class refinement is part of
this source admission.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
