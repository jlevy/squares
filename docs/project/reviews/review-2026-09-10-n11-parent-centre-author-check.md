# Unit-Parent Centre Restriction: Author-Lane Proof Check

**2026-09-10. Read-only analytic check; no target geometry or measurement.** This is a
second pass by the lane that derived the formula, not an independent reviewer’s audit.
Independent proof review remains outstanding.
This report does not admit an implementation, register a target, promote a theorem, or
change T023.

## Definitions and Retained Premises

The reviewed document is
[unit-parent-centre-contract.md](../../../packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md).
The physical container is `[0,q]^2`, with the retained `q=96/25`. A physical unit square
has centre c and a unit axis w. Its selected B-core is concentric, has `B=9977/10000`,
half-side `h=B/2`, and retained unit axis r.

The snapping premise is more specific than concentric containment: after folding, select
a nearest retained direction and undo the same fold on parent and core.
The principal angular discrepancy satisfies `abs(delta)<pi/4` and
`tan(abs(delta))<=D=207107/90000000`. The retained strict inequality `B*(1+D)<1` places
the closed core strictly inside its parent.
These are the premises in
[fixed-cover-transfer-review.md](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/fixed-cover-transfer-review.md),
lines 43–75. The centre-preservation part does not require symmetry of any dot set.

For one retained owner frame, write

`Z_B = [h*S,q-h*S]^2 intersect (mark+[0,h]r+[0,h]Jr)`,

where `Jr=(-r.y,r.x)` and `S=abs(r.x)+abs(r.y)`. This is a necessary centre domain for
the selected core and its local owner class, not a set of certified physical unit-parent
placements.

## Check of the Inequality

A unit parent’s coordinate half-extent is `E(w)=norm_1(w)/2`. Since w is a unit vector,
`E(w)>=1/2`. Centre preservation therefore proves the closed universal restriction
`[1/2,q-1/2]^2` for its selected core.

For the frame-aware estimate, require an exact unit r and a supplied rational bound
`0<=d<1` covering every possible selected-parent discrepancy for that frame.
Set `T=abs(abs(r.x)-abs(r.y))`, so `S>=1` and `0<=T<=1`. A sign vector sigma attaining
`sigma dot r=S` satisfies `abs(sigma dot Jr)=T`, including when a coordinate of r is
zero. With `t=tan(abs(delta))`, the positive-cosine premise gives

$$
\|w\|_1\geq S\cos\delta-T|\sin\delta|
=\frac{S-Tt}{\sqrt{1+t^2}}.
$$

One alternative scalar check of the final comparison is

$$
\frac{d}{dt}\frac{S-Tt}{\sqrt{1+t^2}}
=-\frac{T+St}{(1+t^2)^{3/2}}\leq0.
$$

Thus the expression is at least `(S-Td)/sqrt(1+d*d)`. Its numerator is strictly positive
because `S-Td>=1-d>0`; replacing the denominator by the larger positive `1+d*d/2`
preserves a lower bound.
Dividing by two yields precisely

$$L(r,d)=\frac{S-Td}{2+d^2}.$$

This is an exact rational **lower bound**, not a claim to the sharp minimum parent
extent over the cell.
The additional principal-angle assumption in the document is necessary: a tangent bound
alone does not establish the required cosine sign.

Both necessary container bounds must hold.
Consequently `e=max(h*S,1/2,L(r,d))` and `Z_B intersect [e,q-e]^2` have the correct
direction of inclusion.
Replacing the old B-core box by the one-half box alone would be unsound when `h*S>1/2`.

## Cells, Provenance, and Transport

The optional cell formulas agree with
[adaptive.py](../../../packing/src/sqpack/fractional/adaptive.py), lines 31–82. If a
retained angle is `theta_j=2*atan(t_j)`, the nearest-angle seam is the midpoint of
adjacent angles; its whole-angle tangent is `(t_(j-1)+t_j)/(1-t_(j-1)*t_j)`. The tangent
of the discrepancy from a boundary b is `abs(v_j-b)/(1+v_j*b)`. Angular distance from a
fixed angle attains its maximum over a closed cell at an endpoint, so both boundaries
suffice without an angular sweep.

The source requires exact, strictly increasing half-tangents starting at zero in
`[0,1)`, endpoint bracketing, and increasing seams ending at one.
In particular, `1-t_j*t_j>0`, `1-t_(j-1)*t_j>0`, and `1+v_j*b>0`. A future adapter must
also retain the document’s explicit `d_j<1` and strict-core condition `B*(1+d_j)<1`.
Closed seams include both tie choices safely, including the final frame beyond the
folded endpoint.

[owner_footprints.py](../../../packing/devtools/owner_footprints.py), lines 150–178,
accumulates all folded-index and reflection sources of a canonical orientation.
Every contributing parent cell must be covered.
Taking their maximum mismatch bound is sufficient; choosing one source or the minimum is
not. Quarter-turns and reflections preserve absolute angular mismatch and S,T. Hence the
bound transports with the complete source set, and the symmetric centre restriction
commutes with the admitted corner maps.
The owner’s snapped sector must not be used to truncate the continuous parent cell.

For a reflection, the right-handed axes become `(LJr,Lr)`. Transforming the centre and
mark together swaps the two anchored displacement coordinates without changing their
closed `[0,h]` constraints.
This matches
[wall_owner_escape_compatibility.py](../../../packing/devtools/wall_owner_escape_compatibility.py),
lines 155–176.

## Equality Cases and Required Implementation Semantics

- At `d=0`, the formula gives the exact parent extent `S/2`. On an axis, S=T=1; for
  positive d the universal one-half bound remains necessary even if L is smaller.
  Zero coordinates of r do not invalidate either choice of the unused sign.
- Parent-wall contact is allowed, so the centre inequalities must remain closed.
  A clipped point or segment is a valid necessary domain.
  In a generalized adapter, `e=q/2` gives a singleton box and `e>q/2` an empty box;
  neither is a numerical error or permission to reverse bounds.
  No such target case was evaluated here.
- Extrema over an empty frame are undefined.
  Record that frame as empty, preserve its identity and provenance, and exclude it from
  numerical extrema. A completely empty class is impossible in the necessary model; it
  has no numerical maximum slack and must not be assigned an invented strictly negative
  margin.
- The existing frame extremum can be composed for nonempty restricted domains.
  The current positive and universal replay routines reconstruct **only** `Z_B`
  (`wall_owner_escape_compatibility.py`, lines 288–290 and 380–387), and the current
  class evaluator rejects empty frames (lines 418–425). They cannot be reused unchanged
  to certify the new restriction.
  A derived wrapper must independently reconstruct the added parent box, handle exact
  empty dispositions, and verify every original frame identity before a universal
  result. No shared-helper change is required by this observation.

The SAT sign in the contract is correct.
For fixed residual centre x and a signed axis n, maximizing
`n dot (x-z)-rho_owner-rho_residual` over allowed owner centres uses `min(n dot z)`. All
signed owner and residual axes are required.
A positive maximum is an existential separated B-core witness in a necessary model.
A complete nonpositive maximum over nonempty domains rules out strict coexistence with
that selected class: actual distinct selected cores are disjoint compact sets because
they lie strictly inside physical parents with disjoint interiors.
Zero therefore suffices for this fixed-pose exclusion but supplies no positive
neighbourhood radius.
A strictly negative maximum still needs the stated margin argument for neighbourhood
exclusion. A positive core witness does not establish a joint physical realization; the
negative conclusion remains conditional on this residual pose and selected class.

## Disposition

The author-lane check found no error in the analytic inequality, centre transfer,
intersection direction, or all-source bound.
The empty-frame and derived-replay rules above should be explicit in any implementation
contract before source admission.
The current document correctly separates this derivation from measured footprint gain,
escape elimination, and a global n11 conclusion.
Independent review, implementation admission, and any preregistered target measurement
remain separate outstanding work.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
