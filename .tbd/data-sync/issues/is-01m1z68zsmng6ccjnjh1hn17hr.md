---
type: is
id: is-01m1z68zsmng6ccjnjh1hn17hr
title: "Phase 1: frame record and the Version 1 player"
kind: feature
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m1z694scw2vnhs9rdetpmfe8
  - type: blocks
    target: is-01m1z6992dd1tvwmckn1j93zyf
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-08T00:21:50.510Z
updated_at: 2026-09-08T00:22:27.289Z
---
sqpack/known_best_video/record.py and devtools/build_known_best_video_data.py write atlas/known-best/video/known-best-video.json (schema, pose_decimals declared, refusals on count or angle mismatch between witness and rendering). devtools/kpress_assets.py extracted from render_explainer.py. devtools/render_known_best_video.py inlines record, assets and faces into known-best-1-324-video.html with the motion lab's CSP plus font-src data:, window.atlasVideo {seek, stateKey, schedule, setMode}, slideshow mode, cards, browser controls. Tests: record shape, refusals, Node-executed model at segment boundaries, byte budget from measurement, self-containment, determinism. Both --check steps on the checks tier with budget entries. Closes on packing-validate --checks green and --check byte-identical in two fresh processes. Decisions D1-D7, D13.
