---
type: is
id: is-01m0yeadp3k5y10cmvr9q99hdx
title: Instrument quench with zero-behavior-change trace events
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md
labels:
  - packing
  - motion-lab
dependencies:
  - type: blocks
    target: is-01m0yeb5drm2xkfnjp9krxvdwx
parent_id: is-01m0yd38q3mxynbc38k3gyxt7f
created_at: 2026-08-26T07:07:29.858Z
updated_at: 2026-08-26T07:07:54.154Z
---
Add optional observation hooks around existing fixed-point solves, angular probes, accepted steps, cell changes, and terminal outcomes. Emit QuenchTrace/v1 without extra solver calls. Tests must prove tracing on and off returns identical endpoint arrays, counters, convergence, and stop reason.
