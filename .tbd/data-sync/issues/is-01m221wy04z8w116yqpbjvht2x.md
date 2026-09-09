---
type: is
id: is-01m221wy04z8w116yqpbjvht2x
title: Remove inline-code decoration in print
kind: bug
status: closed
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-09T03:03:04.450Z
updated_at: 2026-09-09T03:57:45.489Z
closed_at: 2026-09-09T03:57:45.489Z
close_reason: "Implemented in Squares PR #140 (head d6f1cce6): semantic apparatus frames, prefix-only caption emphasis, and print inline-code decoration removal with renderer and live typography regressions."
resolution: null
duplicate_of: null
---
For print/PDF only, remove the background and border from inline monospace code while preserving Planetaire font, size, weight, baseline, wrapping, and screen decoration. Update the existing typography/print regression so representative serif and sans-support contexts verify transparent background, no border, and unchanged baseline.
