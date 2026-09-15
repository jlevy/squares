---
type: is
id: is-01m2hg185xq257tkha93q3agpg
title: "PR #160 review D41: resume can never finish a cancelled or timed-out slot"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:58:42.492Z
updated_at: 2026-09-15T02:58:53.609Z
closed_at: 2026-09-15T02:58:53.608Z
close_reason: "Fixed on PR #160 in 38d9f21b: resume keeps only completed and failed outcomes, so cancelled and timed-out slots rerun; tests cover a slot cancelled mid-run and a second resume that visits nothing."
resolution: null
duplicate_of: null
---
Canonical defect D41 from the 2026-09-14 stack triage. Source finding: #160 R11 (Medium).

Resume could never finish a cancelled or timed-out slot. `packages/workbench/src/search/scheduler.ts:72-79` retained every outcome except `not-started`, and Cancel marks the in-flight slot `cancelled` (`:131-144`), so "Resuming exact saved plan" skipped that slot on every resume and `completionRate` stayed below 1 unless the plan id changed. Test file: `tests/search-scheduler.test.ts`.
