---
type: is
id: is-01m0r50x1ms53tfamwwmc5qw2z
title: Classify unrecognised quench endpoints before atlas promotion
kind: task
status: open
priority: 0
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - pr-14
  - ambiguity
  - endpoint-classification
dependencies: []
parent_id: is-01m0qxpbheswp54a9p12640g1z
created_at: 2026-08-23T20:29:34.131Z
updated_at: 2026-08-23T20:29:34.131Z
---
PR #14 ambiguity 2. A missing short closed form does not distinguish a higher-degree optimum from an interrupted descent, a coordinatewise stationary saddle, a point on a flat terminal component, or a quantization split of a known solution. Acceptance: retain the full pose and active set for every endpoint; rerun each singleton through a predeclared precision/budget ladder; require independent validity, complete free sweeps, KKT or directional residuals, active-set stability, and identity stability; classify each result as censored, unresolved duplicate, non-isolated stationary component, isolated stationary candidate, certified local minimum, or exactly promoted; use high-precision algebraic reconstruction and interval Newton or Krawczyk certification where applicable; and never use recognition or rediscovery alone as a convergence oracle.
