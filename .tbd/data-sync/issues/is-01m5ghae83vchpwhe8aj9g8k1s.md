---
type: is
id: is-01m5ghae83vchpwhe8aj9g8k1s
title: Preserve profile integration through upstream T-223 and T-225 releases
kind: task
status: in_progress
priority: 1
version: 6
delegate: profiles-pr-coordinator
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-22T00:49:03.234Z
updated_at: 2026-10-22T06:54:19.189Z
started_at: 2026-10-22T00:49:10.707Z
---
Resolve newly landed origin/main d7923b8d8 conflicts after the button fix. Preserve upstream adoption and release history, reconcile profile identity joins and shared resource descriptions, regenerate URL/data views, validate, and keep PR578 reviewable without merging it.

## Notes

Core merge b6e062d61 with main7359fa8b6 and data pin0755e2fe9 is committed. Final UI b3646ac72 is committed with normal hooks and a clean worktree. Senior review accepted merge and frozen UI/tests;13focused ranking/summary/nativebrowser/asset checks and26Node sorter tests pass (heading regression also passed separately), Python/JS formattinglint/types clean. Required combined pushgate now running (--since14afe72eb,3jobs,1800s) in final-718-push-gate.log; fullpreview worker runs finalb364. PRremote still8077 until gateacceptance/push. Do not mergePR/deploy. Currentcounts75people/217Results/714Credits/112authoredRecords; allsource coverageclean.
