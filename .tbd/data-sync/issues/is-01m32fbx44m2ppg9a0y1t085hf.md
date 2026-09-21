---
type: is
id: is-01m32fbx44m2ppg9a0y1t085hf
title: Cut the full-ascent video, n = 1..324, and a 1..100 social excerpt
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels: []
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-21T17:14:08.387Z
updated_at: 2026-09-21T17:14:08.387Z
---
End-to-end run of `workbench_tools.capture_video` over the whole retained corpus and over n = 1..100, producing linkable MP4s with their receipts.

Found and fixed D-492 on the way: `rangeDuration` priced a range without the `fastSimple` speed-up, so `price_steps` refused every capture.

Measured on this host (Playwright 1.62.0, Chromium 151.0.7922.34, ffmpeg 7.1.1, 1920x1080, 30 fps):
- n = 1..100: 99 steps, 111.4 s, 3342 frames, 11.7 MB, 183 s of capture, every step on its record.
- Frames and outputs staged on an external volume; PNG frames run about 55 KB each.
