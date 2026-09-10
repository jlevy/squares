---
type: is
id: is-01m23pq090zw7s6ctbc2fqxcdy
title: "H-149: run the sixteen-sector owner patch screen"
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-09T18:26:04.704Z
updated_at: 2026-09-10T04:08:27.913Z
closed_at: 2026-09-10T04:08:27.913Z
close_reason: |
  Run and answered on 2026-09-10. Registered as H-157 (renumbered from H-149 when the codex
  line took H-148 through H-151), measured as exp-154, retained as agenda-034 lane X4.

  REFUTED on its own registered direction. The criterion refutes on one surviving class, and
  six survive: of the eight refined sixteen-sector subclasses of the four neutral
  eight-sector classes, six read exact survivor weight 10 and only two drop, to 19/2 rather
  than the predicted 79/8. Over all thirty-two sixteen-bin classes the maximum is exactly 10.

  The mechanism is present and irrelevant. The guaranteed wedge does widen from pi/4 to
  3pi/8, the refined patch does contain its parent vertex for vertex, is 1.6165x to 1.6175x
  its area, and lies inside Q_phi(m) for every one of the 87 to 94 retained rays in its
  closed bin. What does not move is the reach: the squared distance from patch to nearest
  surviving core is the rational identity

    d^2 = 75308842465387162009/335694834731568400000000    d = 0.014977891

  bit-identical for the eight-sector parent and both sixteen-sector children at both marks,
  because the minimising vertex is the mark itself. The 0.014978 the hypothesis was built on
  is a gap to the mark, not to the patch boundary, and no angular conditioning moves the mark.

  Two theorems came out of it and they are the durable result, stated in X-026 section 5.1
  over the retained transported mass-eleven ceiling family and the screened endpoint patches:

    T1 (angular). Every closed angular bin containing one of the 135 neutral rays has
    survivor weight exactly 10, at any bin count. Unconditional -- it needs only that some
    neutral ray exists, since any partition assigns it to some nonempty bin.

    T2 (pose). The class containing the pose of mark-clique member 59 has survivor weight
    exactly 10 under any conditioning by pose, at any refinement.

  What they establish: patch refinement is ruled out as the lever, at every angular
  resolution and at pose level. What they do NOT establish (PR 139 finding R3): that the
  conditional strategy fails. That strategy needs one closed owner selection per packing, not
  every class closed, and owner labels and valid selections can overlap. X-026 escape 1 is
  therefore NARROWED, not closed; whether the neutral classes are ever forced stays open
  beside escape 2 (emptiness).

  Scope: deletions, not atoms. The conditional threshold line, H-155, is untouched.

  Cost: five measured steps totalling 356.1 s, plus a sixth recorded only as under 5 s.
  Every headline read twice, by SAT and by exact convex clipping, 12 of 12 agreeing.

  A false start is on the record too: an exact vertex-to-edge polygon distance is not a
  disjointness test because it misses containment, and it reported weight 11 for all twelve
  classes. Retained as lane-x4-crosscheck.py.txt.
resolution: null
duplicate_of: null
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
