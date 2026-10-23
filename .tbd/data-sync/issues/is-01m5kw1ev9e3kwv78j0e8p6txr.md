---
type: is
id: is-01m5kw1ev9e3kwv78j0e8p6txr
title: "Owner decision (Q13): keep a rational strong view just above an algebraic U at 153, 207, 259 and 302, or the house drawings?"
kind: task
status: open
priority: 2
version: 4
labels:
  - decision
  - regularization
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-23T07:54:06.569Z
updated_at: 2026-10-23T16:18:46.114Z
---
The owner's question 13 at four counts the algebraic adoption re-housed (packing/campaign/result-import.md, "The House Rule": "Keeping a rational view just above an algebraic U is a question 13 decision, put to the owner once with the counts it concerns, and it holds no adoption").

On 23 October 2026 the adoption of the algebraic houses (think-ot5c, branch claude/intake-2026-10-23-algebraic-houses) moved 153 and 207 to PR #574's algebraic certificates (T-174) and 259 and 302 to issue 639's exact forms (T-193). The strong views drawn there were views of the earlier rational houses, now above the new U by 1.57e-14 (153, Evan Daniel's regularizer), 2.42e-12 (207, his regularizer), 1.56e-31 (259, his regularizer) and 1.79e-39 (302, grid-slack at 5 degrees). Each lapsed with its witness, and each count draws its house drawing:

- 153 and 207: the new house drawings have no uneven and no near-axis square (3 classes each), where the lapsed views were drawn as an improvement on the old houses;
- 259 and 302: the new house drawings are irregular (163 and 204 uneven, 26 and 29 near-axis squares) where the lapsed views were not.

The strong runs on the new witnesses draw nothing at or below U: grid-slack has no exact frame on a number-field witness, and Evan Daniel's driver's certificates are rational sides above U (row 4, held). No number-field view is decided on two exact routes (policy obligation 1; think-mbdw).

The question: keep the house drawings (the status quo the adoption leaves), or name the earlier strong views at some of 153, 207, 259 and 302 in regularize_axis_components.ABOVE_U, as at 18, 26, 66 and 85, and draw them (a later change restores the views from the layer's history and its index's lapsed records)? No adoption waits on the answer.

## Notes

2026-10-23 coord-intake-1023: put to the owner in plain terms (in conversation): (a) keep the lapsed tidied views at 259 and 302 only via ABOVE_U, (b) keep all four, (c) house drawings everywhere; recommended (a). New fact from c-houses-1023's first driver run on the new houses (retained under packing/cases/regularized_drawings/think-ot5c-2026-10-23/): Evan Daniel's driver now draws rational views just above the new U at 102 (1.06e-19), 123 (1.16e-19), 153 (1.29e-19) and 207 (1.49e-19), held at row 4; at 153 and 207 these sit far closer to U than the lapsed views (1.57e-14, 2.42e-12). 258 also held at row 4 in the rerun; 259 and 302 still solving. Awaiting the owner's answer; house drawings are the default meanwhile.

2026-10-23 coord-intake-1023: OWNER ANSWER (in conversation, 23 October), in the owner's terms: there is only regularized or not regularized. Regularization minimizes the diversity of angles and packs in an organized fashion; it generally does not change the side, and may change it only as a strict improvement. The best record is always the best record; prefer exact packings and convert inexact ones to exact; always regularize, and track regularization separately (pre- and post-regularization versions). Applied here: a regularized drawing larger than the record is not a regularization of the record, so the lapsed views at 153, 207, 259 and 302 are not kept (no ABOVE_U entry); each count draws its exact house, and regularization of the exact houses stays owed until a regularizer produces an exact view at or below the record's side (number-field regularization, think-mbdw).

2026-10-23 c-houses-1023: QUESTION ANSWERED, applied on claude/intake-2026-10-23-algebraic-houses at e0c2bf255. No ABOVE_U entry was added. The lapsed views at 153, 207, 259 and 302, and the seven row-4 views of the new witnesses (102 1.06e-19, 123 1.16e-19, 153 1.29e-19, 207 1.49e-19, 258 1.66e-19, 259 1.66e-19, 302 1.79e-19 above U), are not kept or drawn. Each of the seven counts draws its exact house. Each `default_drawings.SETTLED` entry keeps state decided-no-better on its new witness and names `owed` = "think-mbdw: the regularization of the exact house, since no regularizer yet draws an exact view at or below the record's side on a number-field witness; until one does, the exact house is drawn". That is the record's "owed with an owner" form: check_bead_tree holds think-mbdw open through `default_drawings.deferrals`. PENDING_ALLOWED was not usable, since `deferral_problems` refuses a deferral for a count whose house an adoption moved. 70 and 295 read regular as published, so nothing is owed there. The runbook's house-rule bullet (packing/campaign/result-import.md), the atlas README and the run README record the answer. The bead is left to the coordinator.
