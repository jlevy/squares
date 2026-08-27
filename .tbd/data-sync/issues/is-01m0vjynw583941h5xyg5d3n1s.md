---
type: is
id: is-01m0vjynw583941h5xyg5d3n1s
title: Add a slackened rational promotion path for strict upper-bound improvements
kind: feature
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - exact-promotion
  - focus-correctness
dependencies: []
parent_id: is-01m0tyy5k7e4ags20c1fxqth7f
created_at: 2026-08-25T04:30:44.612Z
updated_at: 2026-08-27T07:05:07.878Z
---
The current promotion plan aims first at recovering sharp contact algebra, but a strict numerical improvement can be certified more cheaply. Given a valid pose at side s below the standing best S, choose a dilation lambda with lambda*s<S. Dilating centers and the container makes all wall and pair contacts strict; rational points on the unit circle and rational centers are dense, so approximate inside the certified slack and verify the resulting pose exactly over Q. Formalize the margin argument, implement float pose -> bounded dilation -> rational orientation/center approximation -> exact separating witnesses, and calibrate on n=5, n=10, Trump n=11, and imported n=17 poses. The tool must either emit a replayable exact rational packing below a declared threshold or reject with the limiting margin. Register the theorem/tooling slice in the idea/hypothesis record before measurement. Sharp algebraic contact reconstruction remains a later rung rather than a prerequisite for certifying a strict new upper bound.
