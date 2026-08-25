---
type: is
id: is-01m0v0ypqc2shhf313140pqsmk
title: Render document-ready overview and comparison SVGs
kind: task
status: closed
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - tdd
dependencies:
  - type: blocks
    target: is-01m0v0z1kj1v09bzcd9qqk45ap
  - type: blocks
    target: is-01m0v0z3ve6y0n6bc9e0ddwh1w
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:11.115Z
updated_at: 2026-08-25T03:00:04.873Z
closed_at: 2026-08-25T03:00:04.873Z
close_reason: Implemented and validated the deterministic SVG toolkit, exact and numerical adapters, safe serializer, static and animated views, typed overlays, CLI, retained gallery, n=3 migration, documentation, and full gate.
resolution: null
duplicate_of: null
---
Files: sqpack/render/style.py, sqpack/render/packing.py, exports in __init__.py, and geometry/accessibility controls in tools/check_svg_rendering.py. Implement the fixed paper theme, evidence tokens, stable palette, layout metrics, render_packing_svg, document builder, overview/comparison frame selection, shared scale, coordinate projection, container/square glyphs, captions, and exact/summary/none annotations. Materialize portable presentation attributes and keep claim labels closed over EvidenceTier. Done when overview/comparison trees are accessible, geometry checks reproject every corner, start/final panels share scale, invalid profile combinations fail, and base figures remain compact and self-contained.
