---
type: is
id: is-01m0yeadp3k5y10cmvr9q99hdx
title: Instrument quench with zero-behavior-change trace events
kind: task
status: closed
priority: 1
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md
labels:
  - packing
  - motion-lab
dependencies:
  - type: blocks
    target: is-01m0yeb5drm2xkfnjp9krxvdwx
parent_id: is-01m0yd38q3mxynbc38k3gyxt7f
created_at: 2026-08-26T07:07:29.858Z
updated_at: 2026-08-26T07:33:13.920Z
closed_at: 2026-08-26T07:33:13.907Z
close_reason: Added read-only quench_bracket observations for fixed points, angle probes, accepted angles, cell changes, and stops; projected them into QuenchTrace/v1 without additional solver calls. Traced and untraced results match exactly in regression tests, and fast packing validation passed (146 tests).
resolution: null
duplicate_of: null
---
Add optional observation hooks around existing fixed-point solves, angular probes, accepted steps, cell changes, and terminal outcomes. Emit QuenchTrace/v1 without extra solver calls. Tests must prove tracing on and off returns identical endpoint arrays, counters, convergence, and stop reason.
