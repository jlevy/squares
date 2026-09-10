---
type: is
id: is-01m23pq090zw7s6ctbc2fqxcdy
title: "H157: admit and test the sixteen-sector owner patch refinement"
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
created_at: 2026-09-09T18:26:04.704Z
updated_at: 2026-09-10T04:30:12.582Z
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
H157 (renumbered from this strand's earlier H149) proposes a sixteen-sector refinement of the four neutral endpoint-owner classes. The active record is packing/campaign/hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md; sources and scripts are under results/agenda-034, not agenda033.

Before any target run, admit exact refined wedge geometry, containment, nesting and direction representation. Exact pi/8 unit vectors are not rational; use a proved algebraic representation or certified rational enclosures. The global metric is maximum survivor mass over all required refined subclasses, because the claim requires every one below10. The original compound claim's 0.015 geometric reach needs a separately defined and verified condition; survivor success alone confirms only the screened neutrality break. A failed construction or incomplete run stays unresolved.

Run against the declared mass-eleven source after valid source admission. An exact survivor10 in one admitted refined class refutes the all-subclasses claim for this family; it does not refute all conditional point proofs or owner routing. A survivor below10 removes this source obstruction but does not construct a cover. The unconditional core cap has no automatic conditional transfer. Stronger wall/unit-parent domains and richer charges remain independent alternatives. Under-hour runtime is an initial estimate, not a completed measurement.
