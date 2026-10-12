---
type: is
id: is-01m4fdxwz8wxkhxwc1kpbene5s
title: Integrate main 3213 into stack 430 by normal merges and re-pin DATA_REVISION per layer
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T04:14:50.343Z
updated_at: 2026-10-09T04:20:36.105Z
started_at: 2026-10-09T04:20:33.410Z
closed_at: 2026-10-09T04:20:36.105Z
close_reason: "Integration merged and pushed through #466; #468 merge owned by think-cmjh"
resolution: null
duplicate_of: null
---
Merge origin/main into #442 (codex/import-ry-xu-432), propagate normal merges through #468; resolve #468 pages.yml conflict keeping main survey job and the opt-in diagnostic; re-pin DATA_REVISION where the merge is the data commit; single publisher of stack branches.

## Notes

2026-10-09 cloud session: normal-merged origin/main 3213d651b into #442 (2a9466018) and propagated: #443 cee195cb0, #448 83edc69dd, #449 cc9320a7e, #450 3f4723851, #459 31a7397e1, #460 791f304e3, #463 814491bd3, #466 7c6af968f; pushed. Main did not touch DATA_PATHS; every layer's DATA_REVISION unchanged (verified). #468 conflicts in pages.yml; delegated to think-cmjh.
