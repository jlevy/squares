---
type: is
id: is-01m45f4kg50gr27hwf79rwn4a6
title: "PR #350 B3 (Medium): port the repository's PR sections from #361 and add validation at the rebased head"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-10-02-n17-bulk-exclusion-design.md
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m45f4dj0p0t4bsxjnxcz5whv
hold: null
hold_until: null
created_at: 2026-10-05T07:23:34.277Z
updated_at: 2026-10-05T07:27:37.183Z
started_at: 2026-10-05T07:27:29.558Z
closed_at: 2026-10-05T07:27:37.183Z
close_reason: "Fixed in #350's body, edited 2026-10-05T07:01:17Z by jlevy: it now has 'Where n = 17 stands', Results and Dispositions, Changes by Purpose, Documentation and Replanning and the guideline footer, no PUSH350 placeholder, and local validation at the rebased head 9179aab7d (records tier, 219 passed / 16 skipped in the branch's tests, DATA_REVISION a824fcb72), with #307-history results kept as historical (checked 07:40 UTC). The hosted line is still pending because run 37275173288 was cancelled; that is tracked by think-umlx. Body edit, no branch commit."
resolution: null
duplicate_of: null
---
Review B finding B3 on jlevy/squares#350 (https://github.com/jlevy/squares/pull/350#pullrequestreview-5411026984), at head 9179aab7d. Missing: 'Where n = 17 stands', Results and Dispositions, Changes by Purpose, Documentation and Replanning, and the guideline footer. Validation covers only 290488836 and 09a52bc64 on #307's history; nothing covers the rebased head, where the native step now runs in measure-verifier. The closed #361 carried these sections for the identical diff (tree fbe696117). Fix: port them without #361's leftover PUSH350 placeholder, and add validation at the current head.
