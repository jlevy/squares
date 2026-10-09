---
type: is
id: is-01m4fgam2ghc99ka4m1nbjwt4c
title: Repair website token and frontier layout gate regressions
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e36h18crs5ws6c0fm80afy
hold: null
hold_until: null
created_at: 2026-10-09T04:56:44.363Z
updated_at: 2026-10-09T05:02:28.666Z
started_at: 2026-10-09T05:02:28.665Z
---
Full push at818c4c372 reported a literalblack atlas angle-label CSS token violation and three frontier-table layout failures at1024/1280. Web lane owns minimal token-preserving correction and diagnosis of baseline-vs-branch layout measurements, with meaningful focused verification; no assertion relaxation. MediumTriangle/Grid and shared legend must remain. Required full rerun before PR.
