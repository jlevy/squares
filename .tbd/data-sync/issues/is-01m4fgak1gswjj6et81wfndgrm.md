---
type: is
id: is-01m4fgak1gswjj6et81wfndgrm
title: Repair publication date and atlas pin gate regressions
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e36h18crs5ws6c0fm80afy
hold: null
hold_until: null
created_at: 2026-10-09T04:56:43.310Z
updated_at: 2026-10-09T13:44:10.627Z
started_at: 2026-10-09T05:02:27.020Z
closed_at: 2026-10-09T13:44:10.627Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
Full push at818c4c372 reported two artifact-date failures and the atlas shared-version/data-commit contract failure. PDF lane owns diagnosis and minimal repair; preserve user typography/card geometry and honest data pin. Do not edit until original gate stops; focused verification then required full rerun. Owner/root synchronization under site-cleanup epic.
