---
type: is
id: is-01m5h8ywbnz0bwpa535jvnwws7
title: Make action ink alignment check portable across font rasterizers
kind: bug
status: in_progress
priority: 2
version: 2
delegate: project_attribution_fix
labels: []
dependencies: []
parent_id: is-01m5h7me41y7pa91sts7g214vg
hold: null
hold_until: null
created_at: 2026-10-22T07:42:10.291Z
updated_at: 2026-10-22T07:43:42.834Z
started_at: 2026-10-22T07:43:42.832Z
---
Hosted frontend at02b4 failed two action-ink checks: ALL NEWS centerOffset0.140625px exceeds0.1px on Linux Chromium151, with479other tests passing. Diagnose layout versus font-rasterizer quantization; retain meaningful visible centering, icon alignment and hit-area guards. Do not blindly retry or change product styling without evidence. Use controlled offset sensitivity to establish any justified tolerance.
