---
type: is
id: is-01m32htpba7kdtdb0gmh6b1k81
title: Cut ascent videos at 60 fps by default
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-21-video-delivery-profiles.md
labels: []
dependencies: []
created_at: 2026-09-21T17:57:10.119Z
updated_at: 2026-09-21T18:13:16.230Z
closed_at: 2026-09-21T18:13:16.229Z
close_reason: --fps default is 60; deliverables re-cut at 60.
resolution: null
duplicate_of: null
---
Owner's call after comparing the two cuts of n = 1..100: 60 fps reads better and costs little. Measured 14.9 MB against 11.7 MB for the same 111.4 s -- 28 per cent more bytes for twice the frames, because the tweens are smooth enough to encode cheaply. Both conform to the social profile and both measure 53.28 dB PSNR.

Make 60 the default for a cut, and re-cut the deliverables at 60 once the annealing and rigidity fixes land. Capture cost roughly doubles: 335 s against 173 s for the excerpt, so the full n = 1..324 master runs about 20 minutes.
