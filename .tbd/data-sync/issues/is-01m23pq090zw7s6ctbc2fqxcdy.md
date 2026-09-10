---
type: is
id: is-01m23pq090zw7s6ctbc2fqxcdy
title: "H-149: run the sixteen-sector owner patch screen"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T18:26:04.704Z
updated_at: 2026-09-09T18:26:04.704Z
---
H-149, registered from X-026 section 5, escape 1. The one measurement that could overturn
the neutrality reading behind the corner-conditioning result, and it has never been run.

What to measure. Refine the corner-owner angular bins from eight to sixteen, rebuild the
guaranteed patch for each refined subclass of the four neutral eight-sector classes
(m1:j3, m1:j4, m2:j3, m2:j4) at q = 96/25, transport the mass-eleven ceiling family
(results/agenda-033/ceiling-family-191-50.json) with devtools.transport_ceiling_family at
scale 1 and shift 1/100, delete the cores meeting each refined patch with screen_footprint
from devtools.screen_corner_dual_salvage, and read the exact survivor weight per subclass.

Criterion, as registered. Confirm when every refined subclass of every neutral class has
exact survivor weight strictly below 10; refute when any refined subclass still reads
exactly 10, since a case split needs every class closed. The nearest survivor to the j3
patch is a weight-1/8 wall placement centred at (1.50658, 0.50885) at a separating gap of
0.014978, so the refined patch has to reach 0.015 further to delete it and take the
survivor to 79/8.

Why it should work. An owner anchored at angle phi covers the wedge of directions
[phi, phi + pi/2]; intersecting over a closed bin of width w leaves a guaranteed wedge of
width pi/2 - w. At eight bins that is pi/4 wide, at sixteen bins 3pi/8 -- half again as
wide, so the inscribed rational fan reaches further between the parent's two rays. Same
containment argument, different rational vectors.

The missing piece. devtools/owner_footprints.py hard-codes eight bins:
owner_branch_manifest iterates range(8), and triangle_footprint and endpoint_footprint
reject sector >= 8. It needs a bin-count parameter and the pi/8 wedge vectors, with the
sector-footprint proof (results/agenda-031/proofs/corner-owner-sector-footprints.md)
restated at sixteen bins. Everything downstream exists and runs in seconds. Under an hour
end to end.

Scope. A confirmation reopens single-corner point-cover conditioning at sixteen sectors
and no more -- X-026's Step 6, the rank-one cap of 3.868983 on the conditional method at
every m, never used the patch and is untouched. A refutation closes the conditional
point-cover line at both resolutions. Either way it decides a scope question in the
record rather than a bound. Do not screen any family other than the mass-eleven ceiling
family; screening a short family is exactly D-489.

Record: packing/campaign/hypotheses/H-149-refined-owner-sector-patch-breaks-neutrality.md,
packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md.
