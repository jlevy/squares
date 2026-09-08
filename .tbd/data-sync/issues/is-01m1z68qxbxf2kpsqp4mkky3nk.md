---
type: is
id: is-01m1z68qxbxf2kpsqp4mkky3nk
title: "Spike: Version 1 slideshow player with a deterministic seek clock"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies:
  - type: blocks
    target: is-01m1z68zsmng6ccjnjh1hn17hr
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-08T00:21:42.441Z
updated_at: 2026-09-08T00:48:34.243Z
closed_at: 2026-09-08T00:48:34.227Z
close_reason: Slideshow candidate built at 3,594,925 bytes (68 bytes per square) with a deterministic seek clock; the coordinator measured 42 to 53 ms per 1080p frame and 145 to 167 ms at 4K in the pinned headless shell with six captures of one instant byte-identical, and one defect, the panel ghosting mid-fade, now a Phase 1 requirement.
resolution: null
duplicate_of: null
---
Phase 0 (in flight). Single-file HTML slideshow of the 324 renderings with window.atlasVideo.seek(), the kpress faces (PT Serif, Source Sans 3) inlined, and the poster's card facts from composite-figure.json as readable text. NOTES.md records: player bytes and bytes per square; whether one frame captured twice in one headless-shell browser agrees byte for byte; per-frame screenshot cost at 1080p and 4K. Findings fold into the plan's 'Spike findings' subsection and decide D6 and D8.
