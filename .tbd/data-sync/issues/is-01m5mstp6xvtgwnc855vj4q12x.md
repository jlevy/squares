---
type: is
id: is-01m5mstp6xvtgwnc855vj4q12x
title: "PR #754 A7: one loader for the retained Göbel program (suggestion)"
kind: bug
status: open
priority: 2
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m5mstad6tr1k9t825pe62ptr
created_at: 2026-10-23T16:34:42.013Z
updated_at: 2026-10-23T23:15:51.792Z
---
Review A of PR #754 (https://github.com/jlevy/squares/pull/754#issuecomment-6369572454); see the review for file:line references and the suggested fix.

## Notes

2026-10-23 c-answers-1023: deferred from #754 (review A, A7), per coord-intake-1023's call. The four loaders all read the same retained file unchanged, so the program they run is the same; the duplication is not a correctness issue. Merging them touches couzo_678_replay and couzo_715_replay, whose replays and frozen receipts are outside the owner-answers change.

What it waits on (rewritten 2026-10-23 by c-fix-754b-1023 for review B of #754, B4; the earlier text said "Do it with think-v022 (A2), which adds more Göbel readers"): nothing outside its own scope. think-v022 is fixed in #754 (c3f5dc604) and added no loader: `upper_bound_reports.goebel_construction` and `beyond_horizon_replay.standing_sides` read the program through `intake_ledger.construction_side`. The four loaders are still `intake_ledger._goebel` and `_goebel_program` in `beyond_horizon_replay`, `couzo_678_replay` and `couzo_715_replay`. The work is its own change to the couzo_678 and couzo_715 replays: one loader (`intake_ledger._goebel` / `GOEBEL_PROGRAM`) that they import, a test that each module's program object is the same, and both replays' frozen receipts re-checked unchanged.
