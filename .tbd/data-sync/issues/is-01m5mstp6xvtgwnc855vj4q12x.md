---
type: is
id: is-01m5mstp6xvtgwnc855vj4q12x
title: "PR #754 A7: one loader for the retained Göbel program (suggestion)"
kind: bug
status: open
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m5mstad6tr1k9t825pe62ptr
created_at: 2026-10-23T16:34:42.013Z
updated_at: 2026-10-23T17:01:41.155Z
---
Review A of PR #754 (https://github.com/jlevy/squares/pull/754#issuecomment-6369572454); see the review for file:line references and the suggested fix.

## Notes

2026-10-23 c-answers-1023: deferred from #754 (review A, A7), per coord-intake-1023's call. The four loaders all read the same retained file unchanged, so the program they run is the same; the duplication is not a correctness issue. Merging them touches couzo_678_replay and couzo_715_replay, whose replays and frozen receipts are outside the owner-answers change. Do it with think-v022 (A2), which adds more Göbel readers: one loader (intake_ledger._goebel / GOEBEL_PROGRAM) that the replays import, with a test that each module's program object is the same.
