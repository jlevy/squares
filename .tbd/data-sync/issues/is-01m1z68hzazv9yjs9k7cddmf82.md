---
type: is
id: is-01m1z68hzazv9yjs9k7cddmf82
title: A video of every known-best packing, n = 1..324, in two versions
kind: epic
status: open
priority: 2
version: 9
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m0typjn7s866m042zsemybj6
child_order_hints:
  - is-01m1z68qxbxf2kpsqp4mkky3nk
  - is-01m1z68tv7zs38z067x55e61x5
  - is-01m1z68zsmng6ccjnjh1hn17hr
  - is-01m1z694scw2vnhs9rdetpmfe8
  - is-01m1z6992dd1tvwmckn1j93zyf
  - is-01m1z69by99pw12bxj1kf1p0g5
created_at: 2026-09-08T00:21:36.326Z
updated_at: 2026-09-09T04:10:09.219Z
---
Two videos from one deterministic HTML player: a slideshow of all 324 known-best packings with the poster's card facts as readable text (Version 1), and an animated step from n to n+1 with squares sliding, turning and cross-fading (Version 2). The player reads composite-figure.json for facts, the witnesses for poses and the renderings for fills; frames are captured at seek(t) through the pinned Playwright headless shell and encoded by ffmpeg under a receipt; videos are release assets, never committed. Intermediate frames of Version 2 are labelled illustrative tweens. Owner-directed 2026-09-07; runs beside think-0juv. Plan: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md

## Notes

Updated 2026-09-08. Phase 0 exceeded its brief: the Version 2 spike became a solver workbench. Ownership is now split. This epic keeps the video artefacts -- frame record and player, capture pipeline, transition record and tween, publication. The solver (force law, relationship graph, growth, annealing dial, hand editing, the unbuilt Calibrate mode) and every research question it raised belong to think-qn6l under the exploration packing/campaign/explorations/X-025-hunting-by-hand-and-the-move-set-threads.md. The plan records the split in 'What Phase 0 became, and where its parts now live', closes the relaxed-intermediate investigation in D11 on a measured negative, and adds D16 on what snapping does and does not establish.
