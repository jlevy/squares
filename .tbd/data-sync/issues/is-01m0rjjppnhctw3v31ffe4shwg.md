---
type: is
id: is-01m0rjjppnhctw3v31ffe4shwg
title: "PR #16 R16-4: n=5 rank correction needs precise conditions"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels: []
dependencies: []
parent_id: is-01m0rj3jzb99380az12g72g6n8
created_at: 2026-08-24T00:26:28.948Z
updated_at: 2026-08-24T00:38:52.714Z
closed_at: 2026-08-24T00:38:52.713Z
close_reason: "Fixed in the response addendum and handoff: equality rank is not sufficient for a feasible connected optimal family, and the exact n=3 witness—not a converse of record rigidity—establishes non-isolation. D-078 and D-079 record the errors."
resolution: null
duplicate_of: null
---
PR 16 response lines 161-174 correctly retract the rank-free five-dimensional-family claim, but gradient independence alone would not establish a connected feasible optimal family. Fixing the objective, unilateral constraints, tangent cones, higher-order obstruction, and continuation matter. Align with D-041; also remove the remaining suggestion that record-implies-rigid presupposes anything about non-records.
