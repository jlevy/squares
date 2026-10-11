---
type: is
id: is-01m3s1n0yn7v1x1rqvn3raqhem
title: Summarize retained nonfield batch execution costs without mixing parallel walls
kind: task
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3rp1yjrw96h7yy6azcahx2w
created_at: 2026-09-30T11:36:59.092Z
updated_at: 2026-09-30T12:07:44.066Z
closed_at: 2026-09-30T12:07:44.066Z
close_reason: Implemented, independently reviewed, pushed in01572bb8b, and all hosted PR checks pass. CIselector optimized with68focusedtests and measured cold-profile improvement; proofcostreporter covers17retained batches with fivecontrols and unknownmetric handling.
resolution: null
duplicate_of: null
---
Build a small reusable source-bound summary over selected retained nonfield batch summaries and case receipts: actual batch executor wall, sum of case checker wall and CPU, invocation-minus-checker overhead, complete/refused inventories, rows/facets, and per-case costs. Keep parallel case-wall sums distinct from batch wall. Use focused synthetic controls and no broad replay.

## Notes

Focused 4 tests pass; Ruff/format/BasedPyright zero. Actual retained A1 integer sample: batch wall384.301s, summed invocation1138.621s, summed checker1137.425s, summed checker CPU972.983s. Bookkeeping only; batch wall and overlapping case-wall sums remain distinct. Parent reviewed scope and will retain selected report.
