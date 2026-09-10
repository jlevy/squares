# Necessary Unit-Parent Centre Restrictions

**2026-09-09. Analytic derivation for independent audit; no target geometry evaluated.**
The retained snapping proof permits a stricter necessary owner-centre domain.
This note derives the restriction, specifies a small prospective instrument, and does
not report an enlarged footprint or a removed escape.
Source admission and a registered target remain separate.
The frame-aware derivation below awaits its own independent proof audit; it is not a
promoted verified claim.

## Preserved Centre and the Universal Restriction

The retained
[fixed-cover transfer review](../../campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/fixed-cover-transfer-review.md)
selects a **concentric** B-square at a nearest retained direction, with `B=9977/10000`,
`h=B/2`, and `D=207107/90000000`. It proves `tan(abs(delta)) <= D` and
`B*(1+D)=899996306539/900000000000 < 1`, so that the selected closed core lies strictly
inside its physical unit parent.
Undoing the fold applies the same affine map to both centres and preserves their
equality.

A unit square with parent-axis direction w has coordinate half-extent
`E(w)=(abs(w.x)+abs(w.y))/2 >= 1/2`. Containment of that parent in `[0,q]^2` therefore
requires its centre to lie in the closed box `[1/2,q-1/2]^2`. This applies to its
selected core centre, including at a parent-wall contact.

The existing [wall constructor](../../devtools/wall_owner_footprints.py) uses
`Z_B(r)=K_B(r) intersect (mark+[0,h]r+[0,h]Jr)`, where `K_B(r)=[h*S,q-h*S]^2` and
`S=abs(r.x)+abs(r.y)`. The safe new domain is

`Z_parent(r) = Z_B(r) intersect [1/2,q-1/2]^2`.

Intersect with the old box; do not discard it.
At oblique frames the old B-core half-extent can exceed one half.
A tighter necessary centre set may enlarge a common footprint; neither an enlargement
nor a packing exclusion from that change has been measured.

## Rational Bound for an Entire Nearest-Frame Parent Cell

Choose the nearest-frame representative with `abs(delta)<pi/4` and
`0<=tan(abs(delta))<=d<1`, so cosine is positive.
Let r be the retained rational unit ray, `Jr=(-r.y,r.x)`, and let the corresponding
parent axis be `w=cos(delta)*r+sin(delta)*Jr`. A quarter-turn or reversal can be chosen
without changing the square.
Define

`S=abs(r.x)+abs(r.y)` and `T=abs(abs(r.x)-abs(r.y))`.

Suppose the admitted selection rule supplies `0 <= d < 1` and `tan(abs(delta)) <= d`.
Select a sign vector sigma with `sigma dot r=S`; either sign is permitted at a zero
coordinate. Then `abs(sigma dot Jr)=T`. Consequently, with `t=tan(abs(delta))`, the
signed L1 estimate gives

$$
\|w\|_1 \geq \sigma\mathbin{\cdot}w
\geq S\cos\delta-T|\sin\delta|
=\frac{S-Tt}{\sqrt{1+t^2}}
\geq\frac{S-Td}{1+d^2/2}.
$$

The last step uses `S>=1`, `0<=T<=1`, and `d<1`, so every numerator is positive; also
`sqrt(1+t*t)<=sqrt(1+d*d)<=1+d*d/2`. The last inequality follows by squaring positive
quantities. These conditions justify both denominator comparisons; there is no
signed-division reversal.
Thus the exact rational parent half-extent lower bound is

$$L(r,d)=\frac{S-Td}{2+d^2}.$$

Use the derived extent

`e(r,d)=max(h*S, 1/2, L(r,d))`

and the domain `Z_B(r) intersect [e(r,d),q-e(r,d)]^2`. Keep the box closed, retain
segment and point intersections, and record an empty intersection exactly.
Using the proved global `d=D` already covers every retained nearest-frame source and
requires no new angle-cell implementation.

This angular estimate applies to cores selected by the declared nearest-frame rule.
Concentric containment alone does not imply its mismatch bound.
The universal one-half restriction needs only centre preservation.
Any use of the stronger rule in a physical theorem must explicitly select nearest cores
before applying owner routing.
The owner class constrains the snapped frame; the continuous parent angle need not
belong to that sector.
Do not intersect the parent-angle cell with the owner sector.

## Optional Local Mismatch Bounds and Their Provenance

The existing [adaptive controls](../../src/sqpack/fractional/adaptive.py) derive exact
closed nearest-angle cells.
They are in-memory controls, not a retained JSON authority.
For strictly increasing half-tangents `t_j` in `[0,1)`, their whole-angle tangent
boundaries are `b_0=0`, `b_N=1`, and `b_j=(t_(j-1)+t_j)/(1-t_(j-1)*t_j)` internally.
With `v_j=2*t_j/(1-t_j*t_j)`, the exact mismatch bound is

`d_j=max(abs(v_j-b)/(1+v_j*b) for b in (b_j,b_(j+1)))`.

The supplied manifest must satisfy the existing endpoint-bracketing and increasing-seam
checks. All displayed denominators are positive under those checks.
Physical folded angles lie in `[0,pi/4]`; the last retained frame may lie beyond the
endpoint. Closed cells conservatively include both sides of a seam, regardless of the
declared tie owner. Require `0<=d_j<1` and, when used for the strict-core transfer,
`B*(1+d_j)<1`.

[Full owner direction provenance](../../devtools/owner_footprints.py) retains every
folded index and reflection source contributing to a canonical orientation.
A universal bound must cover **all** sources of each signed frame: use the maximum d_j
over their transported cells.
Neither a first-source choice nor the minimum d_j is sound.
Bind every folded index, reflection flag, orientation, quarter-turn, and ray to the
complete manifest. Global D avoids this extra cell derivation.
Local sharpening would need separate provenance and source checks; neither option has a
measured target gain here.

## Corner Maps, Class Membership, and Quantifiers

The [admitted corner maps](../../devtools/wall_owner_containment.py) are BL identity, BR
horizontal reflection, TL vertical reflection, and TR central rotation.
The symmetric centre box is invariant under these maps, and S and T are unchanged by
signed coordinate permutations.
Correctly transported mismatch-source sets preserve the d bound.
Restriction therefore commutes with physical corner placement.

The [owner compatibility transport](../../devtools/wall_owner_escape_compatibility.py)
uses axes `(Lr,LJr)` when the map has determinant +1, and `(LJr,Lr)` when it has
determinant -1. In the latter case the two nonnegative displacement coordinates
exchange. Replay `0 <= (centre-mark) dot r <= h` and its Jr counterpart with the correct
transformed axes. Keep the selected local class label under corner placement; the
diagonal class involution belongs only to a separately declared diagonal certificate
transport.

For a fixed strict residual B-core, the existing exact extremum uses each signed owner
or residual SAT axis n:

`slack(n)=n dot residual_centre - min(n dot z for z in Z_parent) - rho_owner(n) - rho_residual(n)`.

A positive maximum supplies an existential separated **core** witness.
Independently replay the new box, old class, container, transformed frame, and strict
separation.
A universal no-positive result needs every bound frame of the selected class,
with complete source provenance and exact derived centre domains.
These 181 frames cover the finite snapped family through the transfer theorem; they are
not samples from which an all-angle parent conclusion follows by interpolation.

If a complete selected class has no positive separation, the fixed residual core cannot
coexist with an actual selected owner in that class under this necessary parent model.
A strictly negative maximum may support a positive-area neighbourhood after a separate
margin/Lipschitz proof.
Zero alone supports no such neighbourhood.
An independently feasible core does not establish any compatible unit-parent angle,
jointly feasible owners, or a physical packing.

## Prospective Instrument and Target

Implement a small derived-frame adapter: `unit_parent_extent_lower(ray,d)` and
`restrict_owner_centres(frame,rule,q)`. Reuse the existing exact closed clipping, frame
transport, and compatibility extrema.
Bind the original wall receipt without changing its bytes; record the restriction rule,
d and its provenance, extent, old frame reference, and new centre-set dimension.
Do not mutate a frame while retaining stale support fields or represent the restricted
polygon as the original exp146 centre set.
Recompute all derived fields actually consumed by the adapter.

For a footprint comparison, a thin new constructor can keep every original frame
identity, clip its bound centre set, and reuse `OwnerFrameFootprint`,
`support_rectangle`, and `combine_frame_footprints`. Recompute supports for each
nonempty reduced set; retain exact empty-frame dispositions and the existing
impossible-class semantics.
The half-side and anchored owner displacement box remain the original B-core values.
Compare the derived footprint with the bound exp146 footprint, and keep the new
receipt’s provenance separate.
No admitted shared helper needs to change.

Minimal synthetic controls cover an axis, the oblique rational ray `(3/5,4/5)`,
signed/reflected rays, d=0, rejected d<0 or d>=1, a frame whose old box is stronger than
one half, closed tangency, point/segment/empty intersections, an omitted second
provenance source, reflected displacement exchange, min/max reversal, and expiry before
the final universal decision.
No numerical angle sweep is required.

A prospective fixed-witness test can freeze one retained strict residual core, its
source receipt, the selected tuple, and a deterministic class/frame order.
Ask whether the parent restriction eliminates that fixed escape through one selected
owner class. Compare the B-only baseline and the global-D restriction at the same pose.
Attribute a gain to the new restriction only when a B-only positive witness
independently replays and the restricted class has an exhaustive nonpositive result.
If every selected class remains individually compatible, refute only this rule’s
individual elimination of this fixed escape.
Old-model incompatibility is a separate finding.

Use one 90-second shared internal clock after input loading, with a 120-second external
bound and two-second grace; freeze budgets and witness order before target execution.
Preserve partial results without upgrading them to universal negatives.
There is no new residual search or broad case census in this test.
An all-16 footprint comparison is a separately registered alternative.
That comparison and fixed-escape compatibility measure different effects of the
restriction; this note does not register either target.

The compact pair replay and this restriction are separate unrun proposals.
Their comparative cost and mathematical gain have not been measured.
Global owner routing, joint-owner compatibility, and the n11 conclusion remain open;
T023 is unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
