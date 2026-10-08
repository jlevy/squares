---
type: is
id: is-01m4d3f7m7sjk09cjas4yjsbj8
title: "PR #433 A1: mutation-worker source exceeds 192 MiB cap"
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4d3eryja3jhzk668anzbtwd
hold: null
hold_until: null
created_at: 2026-10-08T06:33:35.110Z
updated_at: 2026-10-08T06:50:42.245Z
started_at: 2026-10-08T06:34:06.036Z
---
High finding A1 in review A https://github.com/jlevy/squares/pull/433#pullrequestreview-5452512279. At head 52adbb0e6d37e1fcdf8ed76c78e1a8775f95ccb0 suite-a run 37737159148/job 113179212924 reports 201417439 bytes against 201326592. Locations packing/devtools/run_negative_controls.py:1063 and packing/tests/test_negative_controls.py:434. Audit unconsumed snapshot inputs, retain research/Git evidence and dependency rescue, preserve cap/assertions, verify omission/rescue and hosted gate.

## Notes

A1 fix pushed at 97b3c3a995bac5d7d8279da9d0eef42def3ca9cb. Remote PR head matches; source tree clean. Disposition: https://github.com/jlevy/squares/pull/433#issuecomment-6054206251. Exact original Git files retained: Session 177 receipts/profile-packet.json (358,041 bytes) and exp-063 bc-201-n11-tight-cell-census.json (440,375 bytes), total 798,416. Whole-record audit found only command text in Session 177 README and plain output/record/prose references in agenda 021, Session 087 and exp-063; no registered control, checked inline link or result dependency. Code/test additions: 5,103 bytes. Predicted hosted total: 200,624,126 bytes with 702,466 bytes of headroom under the unchanged 201,326,592 cap; not a locally reproduced full snapshot. Red: 1 failed / 1 passed in 12.77 s; final focused selection: 9 passed in 15.19 s; Ruff check/format clean; BasedPyright: 0 errors / 0 warnings with project Python 3.14.7. No hook bypass. Actual private copier/index/counter fixture confirms omission plus byte-for-byte indexed restoration through both link and result rescue routes. Fresh hosted fast 37739532201, deferred 37739532146, certificate 37739532142, and mergeability 37739529678 were queued at the last check. Remain in progress by coordinator instruction until hosted confirmation; coordinator owns final CI, dedicated reviews, closing and sync. No further source edits.
