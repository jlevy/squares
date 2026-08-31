---
type: is
id: is-01m0v102z22dxytc6atqpnszdz
title: Retain benchmark gallery and decide pinned raster QA
kind: task
status: closed
priority: 2
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - visual-qa
dependencies:
  - type: blocks
    target: is-01m0v10ekmcac6c3v3wm9qtsda
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:56.417Z
updated_at: 2026-08-25T03:00:04.921Z
closed_at: 2026-08-25T03:00:04.921Z
close_reason: Implemented and validated the deterministic SVG toolkit, exact and numerical adapters, safe serializer, static and animated views, typed overlays, CLI, retained gallery, n=3 migration, documentation, and full gate.
resolution: null
duplicate_of: null
---
Files: atlas/rendering/trump11-overview.svg, gobel10-source-return-comparison.svg, n5-exact-face-trajectory.svg, metrics.json, and portability/metric controls. Generate the three new fixtures plus the existing n=3 control. Byte-replay only deterministic metrics: SVG bytes, element count, renderer/version, viewport, and optional pinned PNG bytes. Record observed serialization latency separately in atlas/rendering/README.md with host/runtime fingerprint. Review at thumbnail, screen, print, monochrome, reduced-motion, Chrome, and one nonbrowser path against the cited strong examples. Spike pinned resvg with --skip-system-fonts and explicit digest-pinned fonts; make raster goldens a gate only if hermetic and stable, otherwise record the evidence and keep raster review manual. Decide MathJax paths only from a demonstrated recurring formula need.
