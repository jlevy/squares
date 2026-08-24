---
type: is
id: is-01m0v0ztwy527bxhn4wr64xbka
title: Add typed square, contact, and active-feature overlays
kind: task
status: open
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - overlays
dependencies:
  - type: blocks
    target: is-01m0v102z22dxytc6atqpnszdz
  - type: blocks
    target: is-01m0v10ekmcac6c3v3wm9qtsda
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:48.157Z
updated_at: 2026-08-24T23:17:08.339Z
---
Files: model.py overlay/feature types, packing.py overlay emitters, motion semantics for frame-varying features, and focused controls. Implement square IDs plus contact and active-feature overlays only from typed source input; never infer them from projected proximity. Preserve stable semantic IDs and noncolor encodings, define how features enter/leave across frames, and keep the none/summary/exact profiles visually bounded. Done when mutations that change, omit, or attach a feature to an unknown square fail, monochrome remains readable, and overlays do not change underlying packing geometry or evidence tier.
