---
type: is
id: is-01m4czyz3dcym64x6y3v715kdw
title: "PR #395 C6: update typography checks for shared prepared math assets"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4cecqqmt13gys8265mpra32
hold: null
hold_until: null
created_at: 2026-10-08T05:32:16.364Z
updated_at: 2026-10-08T05:32:34.708Z
started_at: 2026-10-08T05:32:34.707Z
---
Final-head hosted Pages typography fails compare_math_fonts check because it still assumes inline PT Serif faces. Audit every affected browser/math gate for shared-font and prepared-math integration, preserve real metric and geometry controls, and verify corrected source in focused checks and hosted CI. Run 37732462251, typography job 113164599936.
