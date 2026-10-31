---
type: is
id: is-01m68kzzdeghkzk36hzescemmd
title: Register the regularizer's solved views below the new houses at 130 and 307 (2.5e-13 and 3.75e-12), then review and adopt them
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T09:17:32.462Z
updated_at: 2026-10-31T09:17:32.462Z
---
Evan Daniel's regularizer (regularize_evand run, run adopt-2026-10-31-n130-307-evand, retained under packing/cases/regularized_drawings/think-3guf-2026-10-31/ on #852) solved two of the new witnesses the 31 October adoption wrote to exact KKT local minima below the house best packing's side:

- n = 130: below T-259's certificate (Polkovskyi's re-solve of Couzo's #843 packing) by 2.500e-13; strict modulo 29 exact flat motions.
- n = 307: below T-256's certificate (Couzo's #844 refinement of ntumlnoob's packing) by 3.752e-12; strict modulo 57 exact flat motions.

The decision table held both at row 3 (register first), and the selection lists them as register candidates and never admits them (regularization-process.md, "Register Candidates"). Each is a smaller packing: register them as one batch result through the import runbook's stages 3 and 4 (devtools.register_regularized_bounds, as T-155), crediting the packings' finders (Couzo at both, after PR #574's finders at 130 and ntumlnoob at 307) and Daniel's regularizer, check whether any earlier certificate or the next count's ceiling already states each side (first_certified_in), take them through a stage 4 review, then adopt them under the house rule with both regularizations.

## Validation
- Claim: s(130) and s(307) at the regularizer's solved sides, 2.500e-13 and 3.752e-12 below the houses of 31 October; the run's solve/witness.cert at each count.
- Run: register_regularized_bounds, the maintained exact routes, a stage 4 review, then the adoption and its regularization.
- Cost: minutes of CPU for the replay; the review a lane of its own; the regularization 5 to 25 CPU-minutes a count by the runbook's receipts; an estimate, not a receipt.
- Budget status: runnable, under the owner's standing 40 CPU-hour item cap.
- Depends on: #852 merging (it holds the run and the new houses).
- Done when: the batch result is registered, reviewed and adopted at both counts, or the record says why a side proves no new bound.
