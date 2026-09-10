# After the Direct Sixth-Site Decision

**2026-09-09. Read-only strategy and prospective source contract.** Exp153 is a complete
fixed-D-plus-one-site family refutation at source
`da1e42ac84619d05499326da084b6a99ae7987a2`. Its 188 completed support directions end at
187 with an empty site region; no candidate confirmation was required.
Recorded times are 8.889535 seconds for decomposition, 0.620317 for projection, and
12.623588 internally.
This note reads retained rows only.
It does not construct target cores, evaluate a new separation gap, perturb a target
centre, or replay any target geometry.

## Unrun Proposal: One Fixed Two-Attainer Construction

This proposal asks a different question from a generic triple extractor or another dot
search. Their comparative research productivity has not been measured.
The proposed fixed-pair hypothesis asks whether the following fixed construction yields
two strictly x-separated D-missed cores in the selected relaxed tuple (0,0,0,7):

| Role | Exp153 direction | Attainer | Component, vertex |
| --- | --- | --- | --- |
| Right core R | 0, owner-000 | u_max | 0, 1 |
| Left core L | 187, owner-187 | u_min, identical to v_max | 0, 0 |

These identifiers are frozen.
Direction 0 already records the necessary site inequality `x >= 28423/10000`. At
direction 187 the recorded component count rises from the previous row’s one component
to seventeen, and the selected new component supplies both u_min and v_max. This makes
the fixed x-axis test one possible fixed discriminator.
A positive separation gap has not been measured here.

Bind the clean implementation revision, retained endpoint blob
`cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19`, wall blob
`e54fa98133db5f2135cae8875188f51b7db26e12` and constructor
`915758898a97c92793f51e62b7a6b17f846895ca`, and exp153 receipt blob
`aedfcf4e053ea84c0493f5cfd2440f6594923eaa` with its implementation above.
Use three inputs: endpoint, wall, and exp153. The old exp149 and exp151 receipts are
selection history; this new finite-witness proof need not load or replay them.
The source-bound exp153 reader checks the fixed tuple, q, B, source chain, complete
family-refutation status, 188-row consecutive prefix, and the two exact attainer
identities. It need not re-run or independently certify all 188 supports.

Reconstruct only the original-D nine-obstacle domains at directions 0 and 187 using the
admitted container, collision and vertical-decomposition helpers.
Select the specified components and vertices, check exact equality with the saved
attainers and their projections, and require full-dimensional positive-area components.
Build the two corresponding closed B-cores from their own directions.
No added sixth dot enters these domains or their replay.

Write z_R,z_L for the saved centres, h=B/2, and `r_i = h*(abs(u_i.x)+abs(u_i.y))` for
each core’s x radius.
Compute exactly

$$g=(z_R.x-r_R)-(z_L.x+r_L).$$

If g is nonpositive, return complete refutation of this **fixed positive-limit-gap
x-separator construction**. Do not try another axis, another attainer, or another
perturbation. This does not refute disjointness of the same pair on some other SAT axis,
the existence of a different disjoint pair, or exp153’s already established family
refutation.

If g is positive, let m_R,m_L be the means of the distinct vertices of the two selected
component closures, and d_i=m_i-z_i. Set

$$M=|d_R.x|+|d_L.x|,\qquad
\epsilon=\begin{cases}1/2,&M=0,\\
\min(1/2,g/(2M)),&M>0.\end{cases}$$

Use this one common, exact rational epsilon and the centres `c_i = z_i + epsilon*d_i`.
There is no halving loop or second candidate.
Because each component is full dimensional, its vertex mean is interior; every positive
interpolation from a closure vertex toward that mean is strictly interior.
The new x gap satisfies

$$g_\epsilon=g+\epsilon(d_R.x-d_L.x)\geq g-\epsilon M\geq g/2>0.$$

Independently replay both new centres against the open container, all five original
closed-dot collision sets, and all four selected closed owner patches using direct dot
membership and square-polygon SAT. Independently verify strict square-square SAT and the
positive x gap from the new core vertices.
Accept only when every equality, strict avoidance, separation check, and final deadline
check succeeds. A failed replay or contradictory geometry is invalid, not a scientific
refutation. Preserve the exact centres, directions, component means, g, M, epsilon,
perturbed gap, and SAT separator.

Use one 90-second internal clock after loading and a 120-second external process bound
plus two-second termination grace.
All reconstruction, perturbation, independent replay and the final decision share the
clock. One registered target, no retry or sweep.
Cooperative expiry is partial; an external kill may leave no final receipt.
Source preparation has been performed without a target.
The current interpretation block schedules no scientific execution.
Any later run needs its own registered experiment and prospective allocation after
source admission and publication.

Minimum target-blind controls cover positive, zero and negative limit gaps; M=0; both
epsilon branches; the oblique (3/5,4/5) x radius; closed-dot/patch tangency rejection;
correct original-D and selected-patch routing; changed attainer/component/source
bindings; and expiry after the final successful SAT check.
Reuse the existing exact decomposition, core construction, membership and SAT routines.
This is a fixed wrapper, not a general pair search or geometry engine.

## What a Pair or a Triple Would Establish

Two independently replayed disjoint cores each avoid all five unit-weight original
sites.
Any extra nonnegative site weight covering both must have total mass at least two,
since no site belongs to both disjoint closed cores.
Therefore preserving all five original unit atoms forces nominal total covering mass at
least seven in this relaxation.
A conclusion about available mass after banking also requires the original five sites
outside the guaranteed occupied union, or separate accounting for any original mass
inside that union. That rules out nominal total mass below seven; the available-mass
version has the additional banking premise just stated.
It does not prohibit changing the original weights or positions, using a tighter owner
model, or a different proof method.
These relaxed cores are not asserted to have compatible unit parents or jointly
compatible physical owners.

If the fixed pair construction fails, a possible later follow-up is a compact three-core
certificate extracted from the final empty support cut.
Each support half-plane is a face inequality of its recorded closure-attainer core.
Together with the two initial cores, those finite cores have empty intersection.
A two-dimensional infeasibility certificate can select at most three inequalities:
nonnegative exact coefficients lambda_i with `sum(lambda_i*a_i)=0` and
`sum(lambda_i*b_i)=-gamma<0`. The last nonempty region’s supporting vertex/facets guide
selection; verify the coefficients exactly.
Degenerate selection can be bounded and return unresolved instead of adding a general
solver.

For at most three selected cores, move closure vertices toward their component means.
With `M=sum(lambda_i*abs(a_i·d_i))`, the same rule `epsilon=min(1/2,gamma/(2M))` (or 1/2
at M=0) preserves a negative combined bound.
Keep actual initial witnesses fixed.
Independently replay the resulting strict cores and their empty intersection; test only
their at most three pairs.
A found disjoint pair supplies the stronger mass obstruction.
If that triple is pairwise intersecting, its three constraints alone admit added mass
3/2: place weight 1/2 in each pair intersection.
Thus a triple obstruction forbids a single new atom but does not by itself forbid
weighted extra mass below two.
Failure to find a pair in that selected triple is not a universal no-disjoint-pair
result.

H151 retains the completed family refutation.
A future compact strict replay can support a separate obstruction claim, with the
weighted-mass statement only if a pair succeeds.
If only a triple is retained, the claim remains the fixed-D single-added-atom barrier.
Do not create a new global bound, upgrade T023, or multiply theorem entries merely for
source or timing milestones.
A compact obstruction can justify one separate T claim and evidence packet for this
methodological limitation.

## Separate Proposal: Unit-Parent Centre Restrictions

One additional necessary physical restriction is that a unit square contained in [0,q]^2
has its centre in `[1/2,q-1/2]^2`, regardless of orientation.
The retained snapping preserves the centre, so this box supplies an additional necessary
restriction on each saved owner-centre set.
The [parent-centre derivation](unit-parent-centre-contract.md) describes the proposed
intersection and stronger angular bound; that derivation awaits independent audit.
This is a necessary parent condition and can enlarge the guaranteed owner footprint.
The point is to test whether an additional necessary physical condition removes any
retained relaxed witness.
Removal and unit-parent realizability are both unmeasured.

After the compact obstruction is known, one possible test is whether one of its fixed
strict residual cores becomes universally incompatible with one selected owner class
under this added centre condition.
Reuse the owner-compatibility extremum/replay adapter with all 181 bound frames for any
universal negative.
A strictly negative separation margin can support a separately proved
positive-area neighbourhood exclusion; zero alone does not.
Independent feasible core examples remain only necessary-model witnesses: they do not
establish unit-parent realizability or joint compatibility.

Do not substitute the snapped frame’s unit-square extent for a continuous parent’s
extent without proof.
A frame-specific improvement needs a safe lower bound on the parent extent over the
entire admitted nearest-frame selection cell.
The universal one-half box is available without that additional angular argument.
This fallback is separate from perturbing the saved pair and must have its own source
and hypothesis.

## Inactive Covered and Partial Branches

Had exp153 produced a complete confirmed cover, one possible follow-up would transport
the entire six-site certificate, its four patches and the complete direction manifest
under all eight container symmetries.
The tuple orbit consists of one 7 among three zeros, or one 8 among three fifteens, with
the exceptional label in each corner; diagonal reflection uses the admitted class
involution. With the two retained five-dot baselines this gives ten distinct labels, not
a packing fraction. Require every exact map and source binding before adding that scope
to a new conditional exclusion claim.
All sites move together; no invariance of the new site pattern is assumed.
Global owner routing remains open.

Had exp153 been partial with fewer than 361 support rows, first use its recorded stage
times and exact prefix to register a bounded suffix continuation with a fresh budget.
Bind the prior prefix and replay its closed-constraint accumulation; never silently
reset the old experiment.
If all supports were complete but confirmation stopped, one possible successor would be
a full-net confirmation of the exact canonical site, using explicit candidate provenance
and the original endpoint/wall geometry.
Zero deficits accept that candidate; a replayed deficit refutes it and exposes a
support/union inconsistency if the completed support premise is valid.
A stable-looking partial region is not a cover.
These branches are inactive: the actual exp153 is a complete family refutation, so
neither a resumed support pass nor another sixth-site candidate is selected now.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
