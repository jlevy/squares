---
type: is
id: is-01m2hh8gy4w3eyzrtzs7e0a854
title: "PR #160 review D49: a frame's colours depend on seek history"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:09.411Z
updated_at: 2026-09-15T03:32:51.458Z
closed_at: 2026-09-15T03:32:51.457Z
close_reason: "Fixed on PR #160 in 05c25df3 (runs merge at 48 fixed checkpoints read from the poses the scene would draw; direct, walked and revisited seeks paint alike at the steps into 26, 110 and 272) and fcca803c (checkpoints span only the moving-palette window, matching old 60 fps playback within 0-8 of 110 fills)."
resolution: null
duplicate_of: null
---
Canonical defect D49 from the 2026-09-14 stack triage (Medium). Source: #125 F13.

A frame's colours depended on seek history: the scrub reset restored the moving palette's union-find but not `groupSlot`, and runs merged on every painted frame, so a direct seek and a walked seek to the same instant differed (8 of 26 fills at 25->26, 69 of 110 at 109->110). `capture_stills` (direct seek) and `capture_video` (walk) painted different colours at one instant.

Files: `packages/workbench/src/application.js` (~:802-807, ~:841, comment ~:1217 @bb3f7c99); a direct-versus-walked seek probe.
