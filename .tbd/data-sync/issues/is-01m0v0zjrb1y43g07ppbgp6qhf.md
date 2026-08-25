---
type: is
id: is-01m0v0zjrb1y43g07ppbgp6qhf
title: Add certified and illustrative accessible SVG trajectories
kind: task
status: closed
priority: 1
version: 6
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-deterministic-svg-rendering-toolkit.md
labels:
  - packing
  - visualization
  - animation
  - tdd
dependencies:
  - type: blocks
    target: is-01m0v0ztwy527bxhn4wr64xbka
  - type: blocks
    target: is-01m0v102z22dxytc6atqpnszdz
  - type: blocks
    target: is-01m0v10ekmcac6c3v3wm9qtsda
parent_id: is-01m0tzzrpy2hcdcjs6ncbx7b0d
created_at: 2026-08-24T23:16:39.818Z
updated_at: 2026-08-25T03:00:04.903Z
closed_at: 2026-08-25T03:00:04.903Z
close_reason: Implemented and validated the deterministic SVG toolkit, exact and numerical adapters, safe serializer, static and animated views, typed overlays, CLI, retained gallery, n=3 migration, documentation, and full gate.
resolution: null
duplicate_of: null
---
Files: sqpack/render/motion.py, trajectory branch in packing.py, n5-face CLI path, and animation controls in tools/check_svg_rendering.py. Implement stable track matching, normalized keyframe percentages, square-angle unwrapping modulo pi/2, nested final-state translate/rotate attributes, deterministic CSS transform keyframes, changing-container motion, one pass with forwards fill, and explicit illustrative endpoint mode. Motion is enabled only inside prefers-reduced-motion: no-preference; unsupported CSS and reduced-motion settings must show the final underlying frame. Make the certified Q(sqrt(2)) n=5 endpoint/midpoint/endpoint path the first known-answer fixture. Reject mismatched square sets, reordered identities, unsafe CSS, invalid durations/times, missing motion poses, and unmarked interpolation; no interpolated state inherits verification evidence.
