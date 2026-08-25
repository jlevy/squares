---
type: is
id: is-01m0vh8q9q2pzs4hvqyk5fdb4t
title: Use common borders and certified contact marks in packing SVGs
kind: feature
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels: []
dependencies: []
created_at: 2026-08-25T04:01:16.590Z
updated_at: 2026-08-25T04:32:11.876Z
closed_at: 2026-08-25T04:32:11.875Z
close_reason: Implemented shared dark boundaries, exact certified contact extraction and typed point/segment overlays, default-on/removable rendering, final-frame motion reveal, CLI/docs/gallery integration, and 67 focused controls; full 31-step gate passes.
resolution: null
duplicate_of: null
---
Preserve the existing square fill palette, replace misleading white square strokes with the same dark border used by the container, and add typed certified contact geometry. Plan and implement robust point and segment contact extraction outside the renderer, make display optional while attaching known contacts by default, enable it for retained examples if visually clear, update CLI/docs/spec, regenerate the gallery, and validate exact/contact semantics and document rendering.
