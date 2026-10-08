---
type: is
id: is-01m4d3f7m7sjk09cjas4yjsbj8
title: "PR #433 A1: mutation-worker source exceeds 192 MiB cap"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4d3eryja3jhzk668anzbtwd
hold: null
hold_until: null
created_at: 2026-10-08T06:33:35.110Z
updated_at: 2026-10-08T06:34:06.037Z
started_at: 2026-10-08T06:34:06.036Z
---
High finding A1 in review A https://github.com/jlevy/squares/pull/433#pullrequestreview-5452512279. At head 52adbb0e6d37e1fcdf8ed76c78e1a8775f95ccb0 suite-a run 37737159148/job 113179212924 reports 201417439 bytes against 201326592. Locations packing/devtools/run_negative_controls.py:1063 and packing/tests/test_negative_controls.py:434. Audit unconsumed snapshot inputs, retain research/Git evidence and dependency rescue, preserve cap/assertions, verify omission/rescue and hosted gate.
