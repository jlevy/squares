---
type: is
id: is-01m23fmp1gcge5np6ctyrfkqnz
title: Compare structural and arrangement-vertex site generation
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-09T16:22:28.656Z
updated_at: 2026-09-10T04:30:12.501Z
closed_at: 2026-09-10T04:08:49.191Z
close_reason: |
  Run and answered on 2026-09-10, retained as agenda-034 lane A6. The instrument works, and
  the answer it returns is that the premise behind this bead was inverted.

  The instrument. A structural site generator: depth is piecewise constant on the cells of
  the arrangement of a family's placement edge lines, so the scan levels are the midpoints of
  consecutive distinct placement-corner ordinates -- one line strictly inside every slab --
  and the same in x, and every maximal run of the exact depth profile above one contributes
  its MIDPOINT, a point interior to a deep cell rather than a vertex on its boundary, so it
  stays a separating site when the dual moves within the optimal face. It runs over all seven
  retained duals of the 153/40 optimal face at once. 37,368 raw candidates, 37,055 distinct,
  all 37,055 exactly above depth one, 17,885 D4 orbits, in 14.6 s -- against the vertex
  oracle's 60,000 vertices screened, 300 kept, 204 s a round. Selection is spatial (round
  robin over coarse 0.02 cells), not by depth.

  It is better than the oracle and it does not matter. Adding 1,400 structural orbits (10,848
  sites, none of them a point the oracle had ever sampled over four rounds) takes the LP from
  17,389 sites in 2,250 orbits to 28,237 in 3,650, and the cold solve returns 11.000000000 in
  404.9 s against the control's 10.999999999999945.

  THE SITE SIDE IS CLOSED, and there is a certificate. Maximising total weight over the
  280-placement support of the 1/25-integral family, weights tied over its 35 D4 orbits,
  subject to depth at most one at all 139,521 structural sites and all 2,566 atom orbits,
  returns exactly 11. The optimum is a D4-symmetric family of 64 admissible placements, total
  exactly 11, exact maximum depth exactly 1 over all 14,344 arrangement vertices, charging
  every one of the 2,566 atom orbits at ratio exactly 1. The plateau reader holds K0 through
  K3 rather than refusing it, an independent exact atom check finds none violated, and
  verify_ceiling proves it separately. A depth-one family is dual-feasible for EVERY site
  set, so on this atom set the rows-complete LP at 153/40 is at least eleven for every site
  set whatsoever. That measurement cost 18 s of LP and 80 s of plateau reader.

  So the lever is the atom set. Lane A4's 24 atoms entered at primal weight zero because an
  atom separated from a DUAL VERTEX need not cut the optimal PRIMAL family, and an atom that
  does not cut the primal optimum cannot move the objective. Separated from the certificate
  instead, six atoms -- two two-of-three and four three-of-five, budget 1 each -- take the
  blocking support from exactly 11 to 10.4210526, bracketed exactly between a feasible
  325657893/31250000 and a dual bound 2605263163/250000000 with A^T u >= cost in Fractions.

  Three readings worth carrying. Stop adding sites at 153/40. The deep region is three
  structures, not two: wall-column seam 46.7 per cent, interior 30.1 per cent, NEITHER 22.0
  per cent, wall band 1.0, diagonal 0.2 -- and the "sliver 0.0006 wide" is one cell of a
  full-height column with 1,123 distinct deep abscissae over a width of 0.0196 and ordinates
  spanning [0.0663, 3.7631]. And the finest deep cells are about 3e-4 wide with typical ones
  near 5e-3, so a net meeting every deep cell needs of order 1e6 sites against the 1e4 the LP
  can carry.

  Left open, and tracked separately: the joint support-and-atom iteration this points to, and
  round two of the LP (4,000 orbits, 8,815 columns, 63.6 M nonzeros) which was still in
  simplex at 71 minutes when the lane closed. Round two is OPEN, not a result, and nothing
  depends on it.
resolution: null
duplicate_of: null
---
Compare structural site generation with the retained arrangement-vertex baseline under a declared matched budget, site/atom family, solver setup and stopping rule. Evidence comes from agenda034 lanes A3 and A4; the old agenda033 paths and claim that sites are proved to be the general limiting factor are superseded.

The retained runs added site or atom columns without an objective improvement, and their excess-depth witnesses moved. Those observations diagnose the particular restricted LPs. They do not prove that the full atom language, all vertex-based site strategies, or conditional methods cannot improve the bound.

Candidate: generate exact crossing loci for the observed near-axis wall families and tilted-pair incidences, with D4 images. Control: the existing admitted arrangement-vertex generator, with matched initial sites/atoms and solver settings. If the candidate retains the baseline sites, document the superset construction; do not infer a performance gain merely from adding columns.

Predeclare per-arm time and column limits, exact source identities and the primary comparison metric. Report restricted objective change, completed coverage/pricing status, exact maximum depth where computed, and measured solver cost separately. A numeric objective below11 is a candidate requiring frozen all-pose exact verification; a dual with depth above1 is not a global obstruction. Failure to improve in the bounded comparison is a result for those arms only.

Archive candidate/control sites, solver outputs, exact rationalized candidates, controls and provenance in the next admitted experiment. Primary sources: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a3-threshold-loop-at-383-100.md and lane-a4-separating-the-plateau-dual-at-153-40.md. Priority remains a revisable allocation, not a theorem about method productivity.
