---
type: is
id: is-01m51wa1heq5bfskfrqyyeyjd7
title: "Irregular drawings no bead owns: 292, 131, 273, 126, 259 and others still draw 14 to 36 light + uneven squares after the strong generators decided them"
kind: task
status: in_progress
priority: 2
version: 2
delegate: user-eb-reg-leftovers
labels:
  - regularization
dependencies: []
parent_id: is-01m50wdrbfnwsq05w150az5z88
hold: null
hold_until: null
created_at: 2026-10-16T08:12:28.077Z
updated_at: 2026-10-16T08:12:39.279Z
started_at: 2026-10-16T08:12:39.279Z
---
Found by the ugliness audit of lane D (user-eb-reg-leftovers, think-0ut1) on 16 October 2026: the 25 counts n = 1..324 whose drawn default picture is worst by light + uneven + near-axis squares, read from `packing/atlas/known-best/default-drawings.json` (`states`, measured by `regularize_select.today`, i.e. `census_drawing_regularity.regularity` on the drawn picture) and cross-checked with `python -m devtools.census_drawing_regularity --workers 2` over all 324 counts (agrees on 323; at 176 the census reads the held axis view, which #644 replaces).

Most of the top 25 are owned (think-la7h / #644, think-kpm3, think-3zi3, think-yk2h for 290/291). These are not: the strong generators have decided them, so no record defers them and no bead runs them.

Regularized, a strong view drawn (light / uneven / near-axis, classes / hues, drawn by):
- 292: 6 / 30 / 0, 4 / 4, grid-slack-on518 (0.5 deg)
- 131: 7 / 21 / 0, 14 / 14, grid-slack-on518
- 273: 8 / 18 / 0, 22 / 19, evand-regularize-same2 (solved)
- 126: 4 / 21 / 0, 2 / 2, evand-regularize-refreshed-adopt518-v2
- 259: 4 / 20 / 0, 4 / 4, evand-regularize-refreshed-adopt518-v2
- 238: 7 / 15 / 0, 13 / 13, grid-slack-deg5-1013-a
- 239: 6 / 16 / 0, 19 / 19, grid-slack-deg5-1013-b
- 307: 7 / 14 / 0, 27 / 19, grid-slack-on518
- 171, 198: 4 / 15 / 0, 3 / 3, evand-regularize-refreshed-full

Decided no better (SETTLED), drawn by the axis tool's view or the house:
- 272: 9 / 18 / 0 and 204: 5 / 20 / 0 and 303: 3 / 16 / 0 (think-la7h's runs of 16 October, #644)
- 263: 3 / 18 / 0 (house, T-146), 123: 1 / 16 / 0, 180: 5 / 10 / 0 (think-0ut1's runs of 16 October)

What the census says the residue is: no square tilted 0.5 to 2 degrees in any of them except 307 (2), so a wider grid-slack threshold has nothing to straighten. Their light faces are mostly `tilted-neighbour` (a real rotation at a grid region's edge, shaded lighter by the packing itself), with some `offset` and `misaligned` faces (slack inside a region) that grid-slack's MILP did not close within its trust region at the thresholds tried. Cheap probe run (within the policy, nothing admitted): grid-slack at 1 and 5 degrees on 307 (runs grid-slack-leftovers-audit-deg1-1016 / -deg5-1016, 209 CPU-s, scratch only) straightens nothing and draws exactly the drawn view's measures (7 / 14 / 0, 27 / 19).

Open question for the owner, not a run: are these acceptable as drawn, or is a further generator wanted (a joint placement beyond grid-slack's trust region, or one that re-poses whole tilted groups)? Until then nothing here is pending under the policy.
