---
type: is
id: is-01m0w1smncwkj357mjr0aj8dz0
title: Derive exp-038 stress polynomial degree before interpolation
kind: bug
status: closed
priority: 0
version: 2
spec_path: explorations/packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-038-h-023-n5-fixed-angle-polytope.md
labels: []
dependencies: []
parent_id: is-01m0vyhtzd0j8gnfwm5k040ff1
created_at: 2026-08-25T08:50:08.171Z
updated_at: 2026-08-25T08:56:00.718Z
closed_at: 2026-08-25T08:56:00.717Z
close_reason: "Fixed before target: checker structurally derives source-row and weight slopes, cancels exact degree-at-most-two coefficient polynomials, and uses samples only as fixtures; final audit passed."
resolution: null
duplicate_of: null
---
D-257. The first exact checker sampled each stress identity at three epsilon values but merely asserted the degree<=2 premise. Before any retained target: derive executably that centers and selected-axis contact-row coefficients are affine on each path under fixed signed projections and stable tied-row topology, derive affine multipliers, form every pose/side coefficient polynomial of degree<=2, and require all exact coefficients zero. Three samples may remain fixtures but cannot be the proof premise. Preserve strict multiplier bounds, controls, and exact record/replay.
