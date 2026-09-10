# Independent Review of the Unit-Parent Centre Bound

**2026-09-10 UTC. Verdict: PASS for the analytic restriction; CONDITIONAL PASS for
implementation admission.** The formula is a valid necessary restriction under the
hypotheses below. I found no counterexample to it.
A derived adapter can be implemented against this contract, but its source admission
requires the reconstruction, provenance, boundary, and completion controls listed below.
This review admits no scientific target or experimental result.

This is a bounded independent correctness review within the parent phase.
I did not author the proposal or the author-lane check.
I read both as review subjects and reconstructed the inequality and its quantifiers
directly. I inspected the linked snapping, ownership, domain, and transport sources; I
did not rerun their retained scientific measurements.
No target computation, repository edit, registry change, commit, or external publication
was performed.

The reviewed checkout was `codex/n11-combined-finalization` at
`d21c27b90be18ba5e96d2e712e673c0b30efd9a2`. The reviewed contract, author check,
compatibility reader, wall constructor, and adaptive-cell source had no local changes
when inspected.

## Exact Hypotheses and Derivation

The subject is
[unit-parent-centre-contract.md](../../../packing/cases/n11_five_dot_cover/unit-parent-centre-contract.md),
with the separate
[author-lane check](review-2026-09-10-n11-parent-centre-author-check.md).
Let a physical unit square have centre c, unit axis w, and closed containment in
`[0,q]^2`. Its selected closed B-core has the same centre, side `B=9977/10000`,
half-side `h=B/2`, and exact unit axis r. Choose equivalent square-axis representatives
so that

$$w=\cos\delta\,r+\sin\delta\,Jr,\qquad
|\delta|<\pi/4,\qquad 0\leq\tan|\delta|\leq d<1.$$

The mismatch bound must cover every parent source represented by this core frame.
Concentric containment alone does not supply that bound.
The retained nearest-frame selection supplies it with `d=D=207107/90000000`; the
[fixed-cover transfer](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/fixed-cover-transfer-review.md)
also establishes `B*(1+D)<1`. Folding and undoing the same affine map on the parent and
core preserves their common centre.
These are geometric facts independent of the fixed-four-corner obstacle specialization
elsewhere in that transfer document.

Set `S=|r.x|+|r.y|` and `T=||r.x|-|r.y||`. The unit-ray condition gives `S>=1` and
`0<=T<=1`. For a coordinate sign vector sigma attaining `sigma dot r=S`, one has
`|sigma dot Jr|=T`, including either permitted choice at a zero coordinate.
With `t=tan|delta|`,

$$
\|w\|_1\geq\sigma\cdot w
\geq S\cos\delta-T|\sin\delta|
=\frac{S-Tt}{\sqrt{1+t^2}}.
$$

Every numerator in the following comparison is positive because `S-Td>=1-d>0`. Therefore

$$
\frac{S-Tt}{\sqrt{1+t^2}}
\geq\frac{S-Td}{\sqrt{1+d^2}}
\geq\frac{S-Td}{1+d^2/2}.
$$

The first step decreases the numerator and increases its positive denominator.
The second uses `(1+d^2/2)^2>=1+d^2`. The parent coordinate half-extent is
`E(w)=||w||_1/2`, so

$$E(w)\geq L(r,d)=\frac{S-Td}{2+d^2},\qquad E(w)\geq\frac12.$$

This independently establishes the proposed rational bound.
It is generally weaker than the sharp minimum over a parent cell.
At `d=0`, it gives exactly `S/2`. A tangent bound must be paired with the
principal-angle representative in the derivation.

The B-core’s container half-extent is `h*S`. Its old owner domain is

$$Z_B(r)=[hS,q-hS]^2\cap\bigl(m+[0,h]r+[0,h]Jr\bigr).$$

Intersecting all necessary bounds yields

$$e(r,d)=\max\{hS,1/2,L(r,d)\},\qquad
Z_{\rm parent}(r)=Z_B(r)\cap[e,q-e]^2.$$

This direction of intersection is correct.
The original anchored displacement box, mark, class, core side, and B-core container
restriction remain part of the domain.
For example, `(3/5,4/5)` has `h*S=69839/100000>1/2`; a one-half box by itself does not
reproduce the old B-core containment condition.

## Source Quantifiers, Owners, and Residual Cores

The nearest cores must be selected for all eleven parents before applying ownership and
class routing. This is compatible with
[BC-303’s corner-pair argument, section 3](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-030/bc-303-first-wave-selection.md):
its mass argument applies to the resulting eleven disjoint cores, each covered by the
retained measure. It does not require choosing a different core after an owner has been
identified. The owner sector classifies the snapped signed frame.
It does not restrict the continuous parent angle, so truncating a parent cell to that
sector is unjustified.

For a frame with contributing source bounds `d_i`, a parent comes from one source whose
identity need not be known.
Hence use `d_frame=max_i d_i`. Equivalently, the allowed parent family is a union of
source families. Indeed,

$$\frac{\partial L}{\partial d}
=\frac{-T(2-d^2)-2Sd}{(2+d^2)^2}\leq0.$$

Thus larger d gives a weaker extent bound and a larger necessary centre domain.
Taking the minimum d, the maximum source extent, or an unchecked first source can
discard a represented parent.
The full folded-index and reflection-source tuple in
[owner_footprints.py](../../../packing/devtools/owner_footprints.py) must survive
canonicalization and signed-frame transport.
Cardinality alone does not establish that completeness.

The local-cell formulas also pass analytic review.
For `theta_j=2*atan(t_j)`, an adjacent nearest-angle seam is their angle midpoint, whose
tangent is `(t_(j-1)+t_j)/(1-t_(j-1)*t_j)`. The discrepancy tangent from an endpoint b
is `|v_j-b|/(1+v_j*b)`, with `v_j=2*t_j/(1-t_j^2)`. Maximum angular distance on a closed
cell occurs at an endpoint.
Under the endpoint-bracketing and strictly increasing-seam checks in
[adaptive.py](../../../packing/src/sqpack/fractional/adaptive.py), the displayed
denominators are positive and both closed seam choices are covered.
That in-memory API does not itself admit a retained local-cell receipt.
A global-D implementation can leave local-cell input unsupported.

**The same restriction applies to residual selected cores.** For any such core with axis
r and source bound d, its centre lies in `[e(r,d),q-e(r,d)]^2`. The residual domain also
retains its existing strict B-core containment and closed-obstacle avoidance conditions.
It does not acquire an owner’s mark or anchored displacement box.
A general branch requires the full 361 canonical residual orientations and their source
provenance, as the
[five-dot transfer review](../../../packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/five-dot-transfer-review.md)
specifies. Symmetry of this scalar centre box does not supply symmetry of the complete
branch’s obstacles or dot set.
The 181 signed frames in a selected owner class are a different enumeration.

The present proposal specifies an owner restriction at one frozen residual pose.
That is a valid narrow discriminator.
Extending its verdict to a model that restricts all parents needs an explicit
residual-domain rule and replay.
A frozen pose outside its own parent box is excluded by that necessary condition
already; report that separately from elimination through an owner class.
A pose inside the box is still not a certified unit-parent placement.
Neither this review nor the author check evaluated the retained escape against the new
box.

## Closed Boundaries, Empty Frames, and Compatibility

Parent-wall contact is legal.
Every added parent inequality is closed.
A point or segment in `Z_parent` remains a nonempty necessary domain and must
participate in support and separation extrema.
The optional zero-area pruning argument for the old wall domain relies on the core
centre lying in the interior of the B-core container; it cannot be transferred unchanged
to a parent box that may contain a wall-contact centre on its boundary.

For an empty frame, retain its exact identity, source list, derived box, and empty
disposition, with no numerical support or maximum slack.
If every required frame is proved empty, the class is impossible in this necessary
model. That verdict has no invented negative margin.
A missing frame or a failed computation is unresolved, not empty.
For mixed classes, extrema range over every nonempty frame while the complete frame
manifest includes the empty dispositions.

At the frozen scale, `e<=S/2<=sqrt(2)/2<q/2`; this follows from `B<1`, `S>=1`, and
`L<=S/2`. Hence the residual parent box itself is full dimensional.
If a later residual union checker proves exact zero uncovered area in that box against a
finite closed collision union, the existing
[closed-union argument](../../../packing/cases/n11_five_dot_cover/union-contract.md)
covers its boundary as well: the closed box is the closure of its interior.
A generic adapter supporting `e=q/2` or `e>q/2` must instead represent a singleton or
empty box exactly; area zero alone cannot decide coverage of a singleton.

The admitted corner maps preserve the symmetric centre box, S, T, and absolute angular
mismatch. Under a reflection L, the ordered frame is `(LJr,Lr)` and the two anchored
displacement coordinates exchange.
The physical corner map keeps the selected local class label; a separately declared
diagonal certificate transport has its own class involution.

For a fixed residual centre x and a signed owner or residual axis n, the maximum
separation slack is correctly

$$n\cdot x-\min_{z\in Z_{\rm parent}}n\cdot z
-\rho_{\rm owner}(n)-\rho_{\rm residual}(n).$$

The minimum owner projection gives the maximum gap.
All eight signed SAT axes must be considered, although some may coincide.
A positive result supplies a separated B-core pair in the necessary model.
If every frame is empty or its full maximum is nonpositive, the fixed residual core
cannot coexist with a selected owner in that class.
Actual selected cores are disjoint compact sets because they lie inside disjoint parent
interiors, and therefore would require a strictly positive SAT gap.
Zero suffices for this fixed-pose exclusion, but gives no neighbourhood radius.
A negative margin requires a separate continuity estimate for any neighbourhood claim.

## A Counterexample to an Undersized Mismatch Bound

This is an analytic synthetic control, not target geometry or an assertion that the
frozen manifest has these two source bounds.
Let `r=(3/5,4/5)` and rotate it by the positive angle with

$$\cos\delta=\frac{999999}{1000001},\quad
\sin\delta=\frac{2000}{1000001},\quad
d_{\rm large}=\tan\delta=\frac{2000}{999999}.$$

The resulting parent extent is

$$E=\frac{6997993}{10000010},$$

while the incorrect smaller supplied value `d_small=1/1000` gives

$$L(r,d_{\rm small})=\frac{1399800}{2000001}>E>hS.$$

The first comparison has positive cross-product difference `2021000007`. Moreover,

$$B(1+d_{\rm large})
=\frac{9996944023}{9999990000}<1.$$

Thus the B-core lies strictly inside its unit parent, and the parent can have centre
`(E,E)` while touching two container walls.
The smaller d would remove this valid centre.
A bound covering `d_large`, including the retained global D, does not.
This tests the mathematical failure behind minimum-source or missing-source aggregation.

## Admission Conditions

The following conditions belong in the implementation contract before its source is
admitted. The global-D route requires no local angle-cell receipt or angle sweep.

| Condition | Required control or refusal |
| --- | --- |
| Exact scalar inputs | Reject non-rational accepted representations, nonunit or zero rays, invalid q or B, and `d<0` or `d>=1`. Bind the frozen q, B, h, D, and selection rule. Test axes, `(3/5,4/5)`, signed coordinate permutations, `d=0`, and the undersized-bound fixture above. |
| Complete source binding | Reconstruct original signed frames, sectors, quarter-turn selectors, and every folded/reflection source from the bound manifest. Reject a wrong ray, missing second source, missing frame, duplicate replacing another frame, or altered original receipt. Global D must derive from the admitted net; arbitrary d requires separately admitted provenance. |
| Local-cell option, if exposed | Reconstruct all exact seams and endpoint mismatches, enforce endpoint bracketing, increasing seams, `d_j<1`, and strict-core transfer, and aggregate with maximum d. Reject forged cells, incomplete source sets, and a minimum-d mutation. Otherwise reject this option as unsupported. |
| Derived domain | Independently rebuild `Z_B`, intersect the closed parent box, normalize, and compare the exact set and dimension. Keep the original h and displacement box. Test a B-core box stronger than one half, unchanged clipping, wall tangency, point, segment, empty, and generalized `e=q/2` and `e>q/2` cases. |
| Derived supports and footprints | Recompute every consumed support or rectangle from the restricted vertices. Test literal support extrema, stale-support rejection, mark containment, and exact nesting of the old footprint in each possible derived class. Empty classes require explicit impossibility rather than a polygon or area gain. |
| Physical transport | Test both determinant signs with an oblique ray, swapped displacement coordinates, physical corner class identity, and transported source bindings. Compare restriction before and after transport. |
| Compatibility replay | Use a derived wrapper that rebuilds the new domain. Independently replay positive witnesses and universal maxima with literal square vertices. Test max/min reversal, all signed axes, zero slack, mixed empty/nonempty frames, and complete all-empty classes. |
| Residual scope | State whether the target restricts owners only or also residual parents. For the latter, bind the residual source and check its own closed parent box alongside the existing strict escape replay. Distinguish residual self-exclusion, B-only incompatibility, and exclusion attributable to the new owner restriction. |
| Completion and time | Preserve the complete expected manifest separately from processed rows. Inject expiry before final acceptance, during replay, and before an all-empty verdict. Only completed and independently replayed evidence can receive a universal result; partial work retains an unresolved status. Keep the prospectively frozen clock and witness order. |

The current
[wall_owner_escape_compatibility.py](../../../packing/devtools/wall_owner_escape_compatibility.py)
positive and universal replays rebuild only `Z_B`, and its class evaluator rejects empty
frames. Its numerical extremum helper is composable on nonempty derived sets; those
unchanged replays and class verdicts are not an admission path for the new restriction.
A small derived wrapper can address this without changing the admitted shared helper.

After these controls and a separate source review pass, a prospectively registered
bounded target may test an owner footprint change or fixed-pose elimination at its
declared scope. This analytic review establishes neither gain nor joint owner
feasibility, and supplies no global n11 conclusion or change to T023.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
