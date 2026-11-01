---
type: is
id: is-01m68d0t3gpq5ftvzkakhjmm3h
title: "Efficiency: parallel records PRs all append to RELEASE_NO_PUBLIC_CHANGES in release.py and conflict on every merge"
kind: task
status: open
priority: 2
version: 1
labels:
  - efficiency
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T07:15:39.760Z
updated_at: 2026-10-31T07:15:39.760Z
---
Observed 2026-10-31: #835, #848, #833, #834 each appended a no-public-change record to the same tuple at the end of packing/src/sqpack/release.py; each merge to main made every other open records PR conflict there, costing a re-merge, a re-measure and a full ~20 min CI cycle per PR (OR-14). Candidate fixes: one file per record (e.g. a directory of YAML records read in sorted order), or a union-merge gitattributes driver for that block. Measure before choosing.
