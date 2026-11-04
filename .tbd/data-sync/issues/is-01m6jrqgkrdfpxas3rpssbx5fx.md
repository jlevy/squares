---
type: is
id: is-01m6jrqgkrdfpxas3rpssbx5fx
title: Register the regularizer's solves below the new houses at 204 and 299 (row 3 candidates), then review and adopt
kind: task
status: open
priority: 2
version: 2
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-04T07:52:42.360Z
updated_at: 2026-11-04T07:52:55.647Z
---
Evan Daniel's regularizer (regularize_evand run, run adopt-2026-11-04-n204-299-evand, retained under packing/cases/regularized_drawings/think-ybep-2026-11-04/ on #897) solved both witnesses the 4 November adoption wrote to exact points below the house best packing's side:

- n = 204: below T-264's certificate (Doğa Özden's further arrangement of Evan Daniel's T-257 packing) by 4.82e-16.
- n = 299: below T-263's certificate (Özden's further arrangement of Daniel's T-258 packing) by 1.56e-12.

The decision table held both at row 3 (register first), and the selection lists them as register candidates and never admits them (regularization-process.md, "Register Candidates"). Each is a smaller packing: register them as one batch result through the import runbook's stages 3 and 4 (devtools.register_regularized_bounds, as T-155), crediting the packings' finder (Evan Daniel at both), the further arrangement (Özden) and Daniel's regularizer; check whether any earlier certificate or the next count's ceiling already states each side (first_certified_in); take them through a stage 4 review; then adopt them under the house rule with both regularizations. As think-ruu2 does for 130 and 307.

## Validation
- Claim: s(204) and s(299) at the regularizer's solved sides, 4.82e-16 and 1.56e-12 below T-264 and T-263, from the receipts of run adopt-2026-11-04-n204-299-evand.
- Run: devtools.register_regularized_bounds for the two counts, both exact routes with controls, a separately prompted stage 4 review, then the adoption and both strong generators on the new witnesses.
- Cost: the registration and replay minutes; the regularization 10 to 50 CPU-minutes for two counts; an estimate.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Possible subset under the cap: not needed.
- Depends on: #897 merging (T-263 and T-264 on main).
- Done when: the batch result is registered at V3/C3 with an accepted review and the two counts are adopted and regularized.
- Machine note: minutes of CPU; at most two cores.
