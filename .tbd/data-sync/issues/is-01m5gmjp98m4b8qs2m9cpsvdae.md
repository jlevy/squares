---
type: is
id: is-01m5gmjp98m4b8qs2m9cpsvdae
title: Register the project's solved view at 204, 8.91e-12 below T-225 (row 3 register candidate)
kind: task
status: closed
priority: 2
version: 4
labels:
  - regularization
  - result-import
dependencies: []
parent_id: is-01m5frzavxzvcqht1tf2edbfxp
created_at: 2026-10-22T01:45:59.336Z
updated_at: 2026-10-23T00:24:38.738Z
closed_at: 2026-10-23T00:24:38.738Z
close_reason: "#725 merged e929137a8"
resolution: null
duplicate_of: null
---
Register candidate (regularization policy row 3) from the think-ql4v adoption runs of 22 October 2026: Evan Daniel's regularizer (vendored at evand/square-packing@675a5ea, run evand-regularize-adopt-2026-10-22-n204-260-evand, retained in packing/cases/regularized_drawings/think-ql4v-2026-10-22/) solved T-225's 204 witness to a side 8.91e-12 below it (selection-adopt-2026-10-22-n204-260.md, "Register candidates"), with the same light, uneven and near-axis squares (6 / 34 / 6) and shared sides (509 / 555) as the witness. By the house rule ("A regularized view below the house best packing's side is a smaller packing") it is registered as a result (by: project, as T-155 was through devtools.register_regularized_bounds) and taken through stages 3 and 4 before any drawing takes it; then adopted at 204 with both strong generators.

Not drawn: SETTLED[204] records the count decided no better on T-225's witness.
Done when: the view is registered (or found to be rounding, with the reason recorded), validated and, if smaller, adopted.

## Notes

2026-10-22 c-lane-stage4-1022: superseded by T-229's adoption at 204 in draft PR #725 (pass dated 2026-10-23). The project's solved view of T-225 at 204 (8.91e-12 below T-225) lies above T-229, and SETTLED[204] leaves default_drawings. The coordinator closes this bead after #725 merges, as the PR body says.

2026-10-23 00:25Z coord-intake-1021b: #725 merged as e929137a8 (head a623e7585, packing-required and pages-required green; review A dispositions plus coordinator delta check https://github.com/jlevy/squares/pull/725#issuecomment-6354340587). Stage 7 replies on #670/#672/#675/#719 follow the verified deploy.
