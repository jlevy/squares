---
type: is
id: is-01m0w1smaswpm335vd33tcrnnj
title: Prove exp-038 owner-axis exhaustion with valid interval logic
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-038-h-023-n5-fixed-angle-polytope.md
labels: []
dependencies: []
parent_id: is-01m0vyhtzd0j8gnfwm5k040ff1
created_at: 2026-08-25T08:50:07.820Z
updated_at: 2026-08-25T08:56:00.479Z
closed_at: 2026-08-25T08:56:00.478Z
close_reason: "Fixed before target: checker now proves expected zero axes by fixed signed projections and all other (2,4)/(3,4) owner axes by convex endpoint bounds; final exact record/replay audit passed."
resolution: null
duplicate_of: null
---
D-256. The first exact checker inferred an identically zero axis gap from zero endpoint gaps and labeled every SAT gap affine/fixed-sign. That inference is invalid for |affine|, and several a- projections actually change sign. Before any retained target: require expected zero axes to have a fixed strict signed projection and zero endpoint gaps, hence identically zero; prove every other gap strictly negative by exact endpoint bounds and convexity of |affine|-constant; narrow the claim to contacts (2,4)/(3,4); retain a falsifying control; run exact record/replay.
