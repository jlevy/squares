# After exp150: Fixed Six-Dot Cover Contract

**Design admission, 2026-09-09 18:00 UTC.** Exp150’s complete result selects the fixed
six-dot experiment below, proposed as H149/exp151. No new target geometry has been
evaluated and no implementation begun in this lane.
Source admission and publication are still required before that separate target run.

The reviewer read the retained exp150 receipt at implementation
`49b6d6ff22e99269c475594660057d46a98a3edb`. It records four compatible classes, each
with a strictly positive frame-zero witness and passing independent membership and SAT
replay. This refutes H148: every selected class admits an individual B-core separated
from x149. Four visited frames are sufficient for those four existential claims; the
unused 720 frame slots are not unfinished universal work.
The recorded prefix maxima are correctly not labelled global maxima.

This means individual-owner tightening cannot remove this particular witness.
It does not establish joint owner compatibility, unit parents, a packing, or the absence
of tightening elsewhere.
The incompatible-class alternative at the end is retained as a design note and is not
selected for execution.

## Four Individually Compatible Classes: Fixed Six-Dot Cover

Freeze tuple (0,0,0,7), the existing four exp146 wall patches, and

$$D_6=D\cup\{x_{149}\},\qquad
x_{149}=\left(\frac{7641479337977841787}{2367233010000000000},
\frac{11240556076810055587}{4734458945995860000}\right).$$

**Question:** Does this particular six-dot set hit every residual B-core avoiding the
four selected patches, at every retained direction?
There is one candidate and no optimization, owner broadcast, replacement dot, or second
tuple.
Adding the saved centre certainly hits the saved escaping core and preserves every
previous dot hit; it does not establish coverage of its surrounding deficit.

Bind the exact exp143, exp146, and exp149 blobs and their implementation sources.
Their retained blob identities are respectively
`cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19`, `e54fa98133db5f2135cae8875188f51b7db26e12`,
and `83ec897738d6d1b228623c3ac4c10cd9170d5940`. Reuse the admitted exp149 reader and
replay its saved escape against the original five-dot input before constructing D6.
Require six distinct sites, the unchanged first five sites, the added site equal to the
bound saved centre, and the full exact 361-direction manifest.
The exp150 outcome justifies choosing this experiment; its witnesses are not premises of
six-dot cover soundness, so no additional exp150 geometry parser is needed in this
wrapper.

For each direction in manifest order, measure the union of four owner-collision and six
dot-collision polygons inside the residual-centre container using
`independent_union.measure_direction`, with `max_subsets=1023`. Accept only after all
361 exact uncovered areas are zero and the final deadline check passes.
The retained closed-obstacle/full-dimensional-container argument turns zero area into
the required cover; no angular subsampling or floating tolerance is permitted.

At the first positive exact deficit, stop the direction loop, extract one rational
component witness, and independently replay strict open-container membership, avoidance
of all six closed dot-hit conditions, and strict disjointness from the four selected
patches. That refutes this fixed D6 cover only.
A failed replay is invalid; expiry before replay completes is partial, retaining the
measured prefix. Do not continue to another direction or candidate.
H146’s original five-dot existence question is unchanged by either result.

The smallest source delta is a fixed-purpose wrapper around the admitted selected cover
path: compose `replace(source, footprints=selected, dots=source.dots+(x149,))`, use 1023
instead of 511, and adapt the strict escape helper’s nine-obstacle guard to ten.
Pass the augmented source to **both** union measurement and escape replay; passing the
original five-dot source to replay would test the wrong claim.
`measure_direction`, `exact_union_area`, `component_means`, and the independent SAT
helpers already accept these inputs.
The union engine needs no new algorithm or configurable dot-search API. Retain the
original five-dot reader semantics.

Minimum controls: a ten-obstacle toy union accepted at 1023 and refused at 511; an
escape rejected because the sixth site lies inside its core; unchanged six-dot ordering
and source bindings; first-deficit stop/replay; and expiry after the final direction
producing a partial result.
Record exact sites, selected polygons, per-direction areas, counts, source links, and
any new strict escape in a fresh atomic-on-return receipt.

**Budget:** propose 240 seconds shared internally after input loading, 300 seconds
externally for the whole process, one attempt.
The retained exp145 five-dot full-net check took 38.742509 seconds internally and 39.06
seconds externally. Exp149’s one direction took 0.085299 seconds internally, with 11.41
seconds total process time.
Doubling the subset ceiling gives a rough 78-second reference only; the different TR
patch and the added point’s large rational denominators prevent a reliable twofold
runtime bound. The proposed limits provide room for that uncertainty and strict replay.
Deadline means unresolved, without an extension or automatic retry.
Exp150 also measured 8.551670 seconds for loading and its very small compatibility run,
including 0.015891 seconds internally; its external duration was 9.01 seconds.
That supports keeping loading inside the external allowance, without treating the
compatibility timing as a full-net cover estimate.

## Why Six Dots Can Exclude Eleven in This Branch

Under the admitted snapping and BC303 owner-selection premises, an eleven-square packing
yields four distinct selected B-core owners and seven other B-cores, all strictly
contained in their unit parents and positively separated.
Every residual core avoids every selected owner’s common patch.
A complete D6 cover therefore assigns one of six dots to each of the seven residual
cores. Two would share a dot, contradicting their separation.
Equivalently, this owner branch permits at most four owners plus six residual squares.

This conclusion remains conditional on the selected tuple.
Four individually compatible exp150 witnesses neither establish a joint owner placement
nor undermine the counting argument.
A global n11 result still needs every hypothetical packing to admit a valid
owner/mark/sector selection in a completely excluded tuple family, or an exhaustive
disposition of the other selections.
Overlapping labels are not different physical packings.

The previous five-dot witness masks and their 7,936-label candidate restriction cannot
be inherited by D6: the new site can hit those witnesses.
Nor does D6 automatically retain D’s diagonal/central invariance.
Any D4 reuse must transport the entire certificate, including x149, and validate the
direction and class maps.
A successful one-tuple result alone does not change the global bound or T023 grade.

## Inactive Alternative: An Incompatible Class

Bind the completed incompatible class, its full 181-frame source, and its exact global
maximum M. Let the saved residual direction remain fixed.
For each frame and signed SAT axis write

$$a_{o,n}=\min_{z\in Z_o}n\cdot z+\rho_o(n)+\rho_r(n),\qquad
\delta_{o,n}(y)=n\cdot y-a_{o,n}.$$

If **M<0**, put epsilon=-M and choose the explicit rational square

$$Q=x_{149}+[-\epsilon/4,\epsilon/4]^2.$$

Every tested axis is unit length, hence its coordinate absolute sum is at most two.
For y in Q, every slack is at most $-\epsilon+2(\epsilon/4)=-\epsilon/2<0$. Thus Q is
universally incompatible with that owner class, without constructing its entire
forbidden-centre polygon.
Clip Q to the residual-centre container, and use the existing exact union routine with
the original nine obstacles and ceiling 511 to measure the area left outside those
obstacles. That area is a certified local improvement over the old relaxation.
It must be positive: x149 is strictly inside the old uncovered set and Q has positive
radius. A verified zero here would signal inconsistent premises or an instrument error,
not contrary geometric evidence.

If **M=0**, this radius is zero and proves no area gain.
The smallest next area test is confined to the same class and residual direction:
intersect the container with every half-plane $n\cdot y\le a_{o,n}$, then measure its
area outside the same nine obstacles.
Use the existing rational clipping/intersection primitives.
Positive exact area establishes local improvement; zero area refutes that specific
positive-area improvement, while retaining the exact-pose exclusion.
Empty or lower-dimensional intersections have area zero and must not be passed to a
union routine requiring a nondegenerate container.

For either variant, require complete source/replay authority, retain the exact polygon,
area and margins, and use one prospective 90-second internal / 120-second external run
with no extra class or direction.
This is an isolated necessary-domain improvement, not a completed residual cover,
owner-class impossibility, or tuple exclusion.
Full-net work is justified only after this local gain is recorded.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
