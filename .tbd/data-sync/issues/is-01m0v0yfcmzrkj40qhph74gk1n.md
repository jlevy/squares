---
type: is
id: is-01m0v0yfcmzrkj40qhph74gk1n
title: Adapt numerical and exact packing records into render frames
kind: task
status: open
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - adapters
dependencies:
  - type: blocks
    target: is-01m0v0z1kj1v09bzcd9qqk45ap
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:03.603Z
updated_at: 2026-08-24T23:23:54.437Z
---
Files: sqpack/packings/n5_equal_side_face.py, sqpack/render/adapters.py, focused adapter controls in tools/check_svg_rendering.py, and the corresponding import refactor in tools/check_n5_equal_side_face.py. Define the renderer-independent EqualSideFace fixture plus build_equal_side_face and centres_at, then implement frame_from_pose_arrays, frames_from_basin_event, frame_from_gobel10, frame_from_trump11, trajectory_from_n5_equal_side_face, enclosing-side, and normalization helpers as mapped in the spec. Preserve BasinEvent/v3 storage ownership in basin_census.py, retain exact number-field coefficients and formulas, derive the n=5 endpoints/midpoint from Q(sqrt(2)), and never upgrade input evidence. Done when the certificate checker and every adapted frame independently verify and schema/evidence/parameter mutations fail.
