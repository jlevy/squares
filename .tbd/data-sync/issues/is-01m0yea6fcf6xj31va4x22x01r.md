---
type: is
id: is-01m0yea6fcf6xj31va4x22x01r
title: Define shared Motion Lab scenario and trace contracts
kind: task
status: closed
priority: 1
version: 7
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md
labels:
  - packing
  - visualization
  - motion-lab
dependencies:
  - type: blocks
    target: is-01m0yeadp3k5y10cmvr9q99hdx
  - type: blocks
    target: is-01m0yeakhe19nh62258eqbr3d3
  - type: blocks
    target: is-01m0yeaxpks55vzbyz0kg2xf7f
  - type: blocks
    target: is-01m0yeb5drm2xkfnjp9krxvdwx
parent_id: is-01m0yd38q3mxynbc38k3gyxt7f
created_at: 2026-08-26T07:07:22.474Z
updated_at: 2026-08-26T07:21:29.568Z
closed_at: 2026-08-26T07:21:29.564Z
close_reason: Added versioned immutable Motion Lab scenario, frame, overlay, request, event, result, and trace contracts with deterministic serialization, strict Phase 1 payload parsing, resource bounds, and focused red-green tests. Fast packing validation passed (144 tests).
resolution: null
duplicate_of: null
---
Create the versioned scenario, pose-frame, capability, timeline-event, quench-request, and quench-trace contracts used by analytic, recorded, and interactive-solver scenarios. Establish deterministic serialization and evidence fields before changing solver or UI behavior. Add focused red-green contract tests.
