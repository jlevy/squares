---
type: is
id: is-01m0v0zahjq54tvtm1sxr0c9yx
title: Gate static SVG safety, determinism, and retained replay
kind: task
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - testing
dependencies: []
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:31.409Z
updated_at: 2026-08-24T23:16:31.409Z
---
Files: tools/check_svg_rendering.py and test.sh. Complete build_fixtures, model/number/XML/geometry controls, run_determinism_matrix, replay_fixture, and main for the static spine, then add read-only step_svg_rendering to the gate table. Render in fresh processes across hash seeds, time zones, available locales, and shuffled source-map order; compare bytes rather than same-process hashes. Add mutation controls for missing squares, duplicate IDs, altered exact values, unsafe nodes/attributes, stale SVG, and failed atomic replacement. Done when the focused step, Ruff, BasedPyright, and existing n=3 replay pass and each new control has been observed failing.
