---
type: is
id: is-01m1s43b9fbdvnq4g3evnjmh30
title: "BC-213: the remaining m = 5 rung at 973/200, which settles H-062's bracket"
kind: task
status: closed
priority: 0
version: 2
labels:
  - agenda-022
dependencies: []
created_at: 2026-09-05T15:48:21.934Z
updated_at: 2026-09-05T17:28:01.520Z
closed_at: 2026-09-05T17:28:01.519Z
close_reason: |-
  BC-213 complete. Both constructions wall at 973/200 = 4.865 for n = 20 -- uniform grids refuted at LP round 16 (20.001502, 543 placements violated), the seeded set at LP round 34 (20.000223, 213 violated), each by H-062's pre-registered early-refutation clause. Neither converged, so nothing was frozen and cases/n20_fractional_certificate/ is untouched.

  Bracket left: [97/20, 973/200], width 0.015 against the 0.02 H-062 registered, lower end T-021's retained certificate, upper end this wall, 0.1235 below the ceiling 9977/2000. H-062 is ACCEPTED on its own threshold -- the first covering wall this project has pinned to the width its hypothesis asked for.

  Recorded in exp-062 and packing/campaign/series/series-000-smoke-and-calibration/results/bc-213-m5-midpoint-register.txt.
resolution: null
duplicate_of: null
---
Agenda 022. The midpoint of [97/20, 39/8] by the pre-registered rule; either outcome brings the m = 5 covering-wall bracket to at most 0.015, inside H-062's registered 0.02.
