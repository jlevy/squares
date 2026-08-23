---
type: is
id: is-01m0p6bxaqdehm17bjtek76985
title: "PR #5 review F-3: the 32 beads never reached the shared store"
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m0p6bwcyve6zdv41ezr08e3g
created_at: 2026-08-23T02:14:34.582Z
updated_at: 2026-08-23T02:30:04.716Z
closed_at: 2026-08-23T02:30:04.716Z
close_reason: FIXED. tbd sync landed all beads; the old tree is reconciled (think-q3hl and think-pmhe closed as superseded, think-lpse and think-19gf updated with cross-references).
---
The PR body and the revised spec both point readers at 'tbd list --spec plan-...'; after tbd sync against origin/tbd-sync none of the named beads exist and the listing returns the OLD 16-bead tree describing the pre-revision plan. The revised plan is un-executable as written until synced. The old tree also needs reconciling, not just replacing: think-q3hl, think-pmhe, think-lpse, think-19gf restate the same work.
