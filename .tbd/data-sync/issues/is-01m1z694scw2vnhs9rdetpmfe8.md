---
type: is
id: is-01m1z694scw2vnhs9rdetpmfe8
title: "Phase 2: capture tool and the first Version 1 video"
kind: feature
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m1z69by99pw12bxj1kf1p0g5
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-08T00:21:55.619Z
updated_at: 2026-09-08T00:22:27.979Z
---
devtools/capture_known_best_video.py: headless-shell launch as render_explainer_pdf does (SQPACK_CHROMIUM honoured), fixed viewport and device scale factor 1, seek(k/fps) loop with stateKey deduplication into an ffmpeg concat list, H.264 MP4 and VP9 WebM encodes with the host or runner ffmpeg (the bundled ffmpeg-1011 is VP8 only), <stem>.receipt.json (player sha256, commit, mode, timeline, viewport, Playwright version, browser revision, ffmpeg version and args, frame counts, intermediate_frames statement) and <stem>.timings.json (per-frame ms, encode wall, host shape); --stand-in (three frames) and --check (self-agreement in one browser). Measure per-frame cost at 1920x1080 and 3840x2160 and record both. .github/workflows/video.yml: stand-in on pull requests under CAPTURE_INPUTS with the filter test, full capture and release upload on workflow_dispatch. First full slideshow capture on the host for the owner's review. Decisions D8, D9, D14.
