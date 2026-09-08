---
type: is
id: is-01m1w4mhajnd9mzgx2rctgegh6
title: "PR #100 review R13: BC-200 cutting floors are asserted exact after the D-477 repair"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:28.466Z
updated_at: 2026-09-06T20:02:07.930Z
closed_at: 2026-09-06T20:02:07.930Z
close_reason: "Replayed bc-200-family-191-50, bc-200-family-77-20 and bc-232-leg-01 from their bytes through the repaired verifier: recorded vertex counts reproduced, exact max depth 1, floors stand. Added devtools.replay_ceiling_family --check and cited the replay in the review, D-476 and D-478."
resolution: null
duplicate_of: null
---
The PR qualifies BC-206's floor as unreplayable but leaves the BC-200 floors at 3.82 and 3.85 asserted as exact in CERTIFICATE-REACH.md, X-016 and exp-060. D-477 is a small-coordinate defect. BC-200's state is retained, so a replay is possible; disposition pending that replay.
