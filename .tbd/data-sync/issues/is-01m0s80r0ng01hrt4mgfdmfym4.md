---
type: is
id: is-01m0s80r0ng01hrt4mgfdmfym4
title: "PR #17 review E13: record the negative-control worker-tree race"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - focus-infrastructure
dependencies: []
parent_id: is-01m0rwwt8912eq5f3507d581e1
created_at: 2026-08-24T06:41:09.140Z
updated_at: 2026-08-24T07:13:46.082Z
closed_at: 2026-08-24T07:13:46.081Z
close_reason: "Merged in PR #18 at b3545d0: explicit worker-tree checkout queue prevents concurrent reuse; width sweep and D-125 retain the race and fix."
resolution: null
duplicate_of: null
---
The first parallel negctl implementation assigned trees by index and allowed two controls to mutate the same tree. The fix uses an explicit available-tree queue. Add the substantive concurrency/measurement bug to defects.yaml with the exact regression that prevents recurrence.
