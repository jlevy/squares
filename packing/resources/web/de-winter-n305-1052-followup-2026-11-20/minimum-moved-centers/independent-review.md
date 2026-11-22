# Independent Review of the 305-Square Moved-Center Minimum

**Accepted within the submitted hypotheses.** The minimum number of
moved centers is nine, separately when square 43 keeps its original direction and when
it is snapped. This concerns the original exact side, the 36 specified near-axis snaps,
every other direction held fixed, and each center coordinate displaced by at most
`1/50000000000`. It does not establish a minimum with unrestricted movements or
rotations, or a lower bound on the container side.

The reviewer worked independently of the proof authors.
I reviewed the original exact poses and submitted cohorts, the row construction,
deciding duals and branch trees, and the retained witness admissions identified in the
[source inventory](review-inventory-20261121.json).
I then wrote a [separate checker](programs/independent_review_check.py.txt) for the proof
arithmetic, used geometric premises, witness hypotheses and finite covering problem.
The [independent receipt](receipts/independent-mathematical-review-20261121.json)
records the successful recheck and scientific-input digests.

Every cohort has distinct 1-based square IDs and a fixed group contained in it.
Every included center outside that fixed group retains both displacement variables; none
of the omitted squares is implicitly fixed.
With displacement written as `rho * z`, the box is exactly `-1 <= z <= 1`. Container
walls and square separation are closed inequalities, so boundary contact remains
allowed. For an axis `n`, separation uses
`n·(z_i-z_j) <= ((p_j-p_i)·n-h_i(n)-h_j(n))/rho`, with each support value obtained from
the square corners. The four edge axes and both signs cover the separating-axis
disjunction. A row `a·z <= b` is impossible on the box only when `-sum(abs(a)) > b`; it
is automatic only when `sum(abs(a)) <= b`. These tests preserve the full bounded
disjunction, including equality cases.

The independent checker reused the packet’s row enumeration, then separately derived
corner projections for every nonzero dual premise and every branched clause.
It checked normalized coordinate bounds, mandatory wall and pair rows, complete clause
alternatives, nonnegative rational multipliers, exact coefficient cancellation and
strictly negative combined right-hand sides.
Every branch has a checked child for every alternative.
Empty and negative multiplier controls and an omitted branch were refused.
The mandatory-row duals for cohorts 12 and 15 close their roots directly; the earlier
capped branch search is not needed to complete those exclusions.
Square 43 is absent from every cohort, and the regenerated local models coincide in both
modes. This covers all 17 groups in both modes: 34 local premises.

Any admissible full packing that leaves a cohort’s fixed group unchanged restricts to a
feasible point of that local system: removing the outside squares only drops
constraints. Its certified contradiction therefore forces a moved center in the fixed
group. No constraint involving an outside square is needed.
Consequently, the moved-center set must hit all 17 groups.
A separate exact subset dynamic program over their 24 distinct IDs found minimum
cardinality nine and 1,581 minimizers (14,350 states).
Moving centers outside that union cannot reduce this requirement.

Both retained full-packing witnesses were bound to the original side and all prescribed
directions, coordinate by coordinate.
Each moves exactly IDs 108, 140, 141, 142, 143, 150, 153, 164 and 175; every other
center is unchanged.
Each maximum coordinate movement is strictly below the radius; the receipt retains its
exact rational value and positive slack.
These witnesses attain nine in their respective modes.
Their full-packing feasibility relies on the retained exact positive replays, whose
input correspondence and admission were checked again.
I did not repeat their 46,360 pair checks.
This is an explicit dependency of the upper-bound half of the minimum conclusion.

The single guarded recheck passed in 8.301 seconds of worker time and 8.884 seconds
including supervision.
The [supervision receipt](receipts/independent-mathematical-review-supervision-20261121.json)
records eight samples, maximum observed process-tree footprint 0.09 GiB and kernel
pressure 1 throughout.
Worker and observer exited zero, with no intervention.
The launch required a fresh pressure-1 sample; limits were 180 seconds, 0.30 GiB, and
stop at pressure 2. The guard was observe-only and the supervisor enforced the limits.
The run checked the retained proof, geometric premises and witness correspondence.
This archived program is the original review checker.

Use the [assembly replay environment](README.md#replay-the-assembly) and run
`programs.independent_review_check` with a fresh output path. Also decompress
`minimum-scope-audit-20261121.json.gz` in the scratch copy for this review.
The inventory records the inputs used by the review. The archived programs
retain their observed bytes and use the original `.py` filenames in the replay copy.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
