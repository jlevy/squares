---
type: is
id: is-01m4fgam2ghc99ka4m1nbjwt4c
title: Repair website token and frontier layout gate regressions
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
created_at: 2026-10-09T04:56:44.363Z
updated_at: 2026-10-09T13:44:10.847Z
started_at: 2026-10-09T05:02:28.665Z
closed_at: 2026-10-09T13:44:10.847Z
close_reason: Implemented, independently reviewed and qualified for PR474 source 6ccbbf000f0c9b48f2985c07c9893f98fe73ba92 against main 6a0499ba4; combined tree c65da41410e89a8dedffe93d3c1e153adb05096d. Local named push 65/65 and hosted 93 fast + 13 actual deferred (106) plus Pages passed; final readiness receipts recorded.
resolution: null
duplicate_of: null
---
Full push at818c4c372 reported a literalblack atlas angle-label CSS token violation and three frontier-table layout failures at1024/1280. Web lane owns minimal token-preserving correction and diagnosis of baseline-vs-branch layout measurements, with meaningful focused verification; no assertion relaxation. MediumTriangle/Grid and shared legend must remain. Required full rerun before PR.
