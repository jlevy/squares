---
type: is
id: is-01m0wc0aqb4cjkwkc9ytnjxt53
title: Repair the stale canonical defect count
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0w9a47h5zrn7jf16pp2kpxs
created_at: 2026-08-25T11:48:33.130Z
updated_at: 2026-08-25T11:57:20.648Z
closed_at: 2026-08-25T11:57:20.648Z
close_reason: "Completed: corrected defects.yaml from 282 to the full 299-row total after this review tranche. The fail-fast cross-field schema check and rendered-view check now pass."
resolution: null
duplicate_of: null
---
The committed defects.yaml declares count 282 while containing D-001 through D-293. The generated view derives 293 directly from the rows, so render checks stayed green and hid the canonical soft-schema mismatch. Update the count with this tranche and retain the existing schema validator as the regression; record the focused-gate omission in the logbook.
