---
type: is
id: is-01m68d0t3gpq5ftvzkakhjmm3h
title: "Efficiency: parallel records PRs all append to RELEASE_NO_PUBLIC_CHANGES in release.py and conflict on every merge"
kind: task
status: in_progress
priority: 2
version: 4
delegate: bold-ritchie-l17
labels:
  - efficiency
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
hold: null
hold_until: null
created_at: 2026-10-31T07:15:39.760Z
updated_at: 2026-11-01T21:59:36.796Z
started_at: 2026-11-01T20:50:56.742Z
---
Observed 2026-10-31: #835, #848, #833, #834 each appended a no-public-change record to the same tuple at the end of packing/src/sqpack/release.py; each merge to main made every other open records PR conflict there, costing a re-merge, a re-measure and a full ~20 min CI cycle per PR (OR-14). Candidate fixes: one file per record (e.g. a directory of YAML records read in sorted order), or a union-merge gitattributes driver for that block. Measure before choosing.

## Notes

L17 (bold-ritchie-l17): draft PR #873 (https://github.com/jlevy/squares/pull/873), head bd0fe349c, hosted CI green (packing 41353672001, pages 41353671991, mergeability 41353667883). Measured with devtools.merge_conflicts: 174 merges 24 Oct-1 Nov, 82 conflicted, the tuple in 64 (33 PRs), alone in 31. Union driver refused (25 of 41 tuple-only merges do not compile; 0 match the resolution). Records now one file each in packing/release-records/no-public-change/ (247, 0000-0246 in tuple order, incl. #872's; new ones <YYYY-MM-DD>-<slug>.yaml). Follow-up candidate: DATA_REVISION conflicts (32 merges, 20 PRs). Not closed: awaits merge.
