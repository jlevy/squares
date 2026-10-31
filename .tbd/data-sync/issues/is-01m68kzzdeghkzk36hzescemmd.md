---
type: is
id: is-01m68kzzdeghkzk36hzescemmd
title: Register the candidates below the new houses at 130, 293 and 307 (regularizer solves and the 260 + L strip), then review and adopt; the 172 review-queue view to the owner
kind: task
status: in_progress
priority: 2
version: 3
delegate: bold-ritchie-l2
labels:
  - validation
  - regularization
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-10-31T09:17:32.462Z
updated_at: 2026-10-31T11:48:22.810Z
started_at: 2026-10-31T11:48:22.244Z
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

## Notes

2026-10-31 (bold-ritchie-l2; A3 and A8 of the senior review of #852, https://github.com/jlevy/squares/pull/852#pullrequestreview-5722530514):
- A third register candidate, at 293: the committed s260_1028.cert (T-257's house at 260) plus one axis-aligned L strip of 16 + 16 + 1 squares in [S, S+1]x[0, S+1] U [0, S+1]x[S, S+1] proves s(293) <= 8816991251060941991251052624833/(5*10^29) = 17.6339825021218840..., 8.98e-13 below the adopted 293 house (T-257's s293_1028.cert) and across its 12-place print (...122 against ...123). The reviewer built it and the maintained independent route accepted it (42,778 pairs; scratchpad/rev9-scripts/lstep_293.py). Credit Evan Daniel (his 260, as his 293 is his 260 plus an L). Register with the 130 and 307 regularizer solves, review, then adopt. A scan of L steps into and out of the eight re-housed counts found no other improvement.
- For the owner's section 5 review (regularization policy), not a candidate: Evan Daniel's same-side view at 172 (run evand-regularize-adopt-2026-10-31-n130-307-evand) went to review at row 7, "2 per-square counts fell while no total did". It draws 0 uneven and 0 near-axis squares, 4 angle classes and 4 hues; the drawn grid-slack view has 21 classes and 20 hues. result-import.md sends such a view to the owner; the count is settled on its current drawing and the view waits in the review queue (receipt review_queue: [172]).
