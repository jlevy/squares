---
type: is
id: is-01m0v0zahjq54tvtm1sxr0c9yx
title: Gate static SVG safety, determinism, and retained replay
kind: task
status: closed
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - testing
dependencies:
  - type: blocks
    target: is-01m0v0zjrb1y43g07ppbgp6qhf
  - type: blocks
    target: is-01m0v10ekmcac6c3v3wm9qtsda
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:31.409Z
updated_at: 2026-08-25T03:00:04.895Z
closed_at: 2026-08-25T03:00:04.895Z
close_reason: Implemented and validated the deterministic SVG toolkit, exact and numerical adapters, safe serializer, static and animated views, typed overlays, CLI, retained gallery, n=3 migration, documentation, and full gate.
resolution: null
duplicate_of: null
---
Files: tools/check_svg_rendering.py and test.sh. Complete build_fixtures, model/number/XML/geometry controls, run_determinism_matrix, replay_fixture, and main for the static spine, then add read-only step_svg_rendering to the gate table. Render in fresh processes across hash seeds, time zones, available locales, and shuffled source-map order; compare bytes rather than same-process hashes. Add mutation controls for missing squares, duplicate IDs, altered exact values, unsafe nodes/attributes, stale SVG, and failed atomic replacement. Done when the focused step, Ruff, BasedPyright, and existing n=3 replay pass and each new control has been observed failing.
