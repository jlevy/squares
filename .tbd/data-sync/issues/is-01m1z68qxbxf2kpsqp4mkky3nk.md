---
type: is
id: is-01m1z68qxbxf2kpsqp4mkky3nk
title: "Spike: Version 1 slideshow player with a deterministic seek clock"
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m1z68zsmng6ccjnjh1hn17hr
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-08T00:21:42.441Z
updated_at: 2026-09-08T00:22:25.672Z
---
Phase 0 (in flight). Single-file HTML slideshow of the 324 renderings with window.atlasVideo.seek(), the kpress faces (PT Serif, Source Sans 3) inlined, and the poster's card facts from composite-figure.json as readable text. NOTES.md records: player bytes and bytes per square; whether one frame captured twice in one headless-shell browser agrees byte for byte; per-frame screenshot cost at 1080p and 4K. Findings fold into the plan's 'Spike findings' subsection and decide D6 and D8.
