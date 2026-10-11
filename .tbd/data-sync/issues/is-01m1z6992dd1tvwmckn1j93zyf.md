---
type: is
id: is-01m1z6992dd1tvwmckn1j93zyf
title: "Phase 3: transition record and the Version 2 player"
kind: feature
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m1z69by99pw12bxj1kf1p0g5
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-08T00:22:00.012Z
updated_at: 2026-10-06T08:32:07.046Z
closed_at: 2026-10-06T08:32:07.045Z
close_reason: |
  Superseded (bead review 2026-10-06, origin/main eb43ffe9a): Plan's Current Phase Routing on origin/main routes films through the workbench Animate tab and capture adapters; transitions live in packages/workbench (test_transitions.py, check_transitions.py) and the Version 2 ascent films shipped as v0.4.1/v0.4.2
resolution: canceled
duplicate_of: null
---
sqpack/known_best_video/transitions.py: prefix (verified equality of the first n poses), shared-picture (the one index whose removal makes the tuples equal, refuse otherwise), assignment (scipy linear_sum_assignment on squared centre displacement plus weighted squared shortest-arc turn mod 90 degrees, ties by id); the builder writes transitions with pairs, new_square, displacement and turn statistics and intermediate_frames: illustrative-tween. Test: every one of the 323 correspondences is a bijection onto all but one of n+1's ids, method census (160, 5, 158). tween.js and transition mode: linear centres and side, shortest-arc angles, OkLCh cross-fade of the retained fills, the new square fading in over the last third, the persistent 'illustrative transition, not a packing' label; Node model test at a mid-transition. The continuous angle ramp behind a record flag only if the owner asks. Decisions D10, D11, D12.
