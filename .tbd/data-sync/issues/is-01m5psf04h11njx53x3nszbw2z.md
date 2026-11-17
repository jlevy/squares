---
type: is
id: is-01m5psf04h11njx53x3nszbw2z
title: "PR #789 (merge): senior review of the #763 import (PR A, T-240) and its code (couzo_763_claims, beyond_horizon_replay PUSHED_LATER)"
kind: task
status: closed
priority: 1
version: 4
delegate: c-rev-789-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T11:06:47.825Z
updated_at: 2026-10-24T11:32:54.556Z
started_at: 2026-10-24T11:06:53.903Z
closed_at: 2026-10-24T11:32:54.555Z
close_reason: "Review A posted https://github.com/jlevy/squares/pull/789#issuecomment-6383682934 at 3773d6025: approve after A1, A2 (Medium); A3-A11 Low; claim map, margins, restatement boundary and a third exact route verified; a dedicated correctness review of claim_map_walk_sources and declared_rows recommended."
resolution: null
duplicate_of: null
---

## Notes

2026-10-24 c-rev-789-1024: Review A (senior, round 1) of #789 published as a PR comment at head 3773d6025, base f354a34f5: https://github.com/jlevy/squares/pull/789#issuecomment-6383682934. Verdict: approve after A1 and A2; no Blocker or High. A1 Medium: T-240 claim (results.yaml:33514-33516) and the reply state the selection rule as a disjunction. A2 Medium: T-240 'smallest report at each count' and next_rung ignore evand 8a8879a's 268 (think-l49q). Low: A3 the 303 ceding words are in 43f666c's commit message, not its README; A4 268 credit question absent from T-240, Q8 sources; A5 credit line breadth; A6 unrequested rows cite the issue key; A7 the stage 2 rule's scope; A8 test binds PUSHED_LATER[-1], which breaks when think-gn29 adds the 06:10:44Z push; A9 claim_map_walk_sources hard-codes #763; A10 reply duplicated in think-ptkk notes; A11 PR checkbox. Independent checks: own claim-map derivation equal to the receipt at all 451 rows; third exact SAT route over 196 certificates, all accepted, all 392 controls refused, pairs and least gaps equal to the receipts; push dating verified with a negative control. Scratch: /tmp/claude-0/-home-user-squares/d57983cc-21aa-53cd-a24f-c90463a5a3c0/scratchpad/rev-789/.
