---
type: is
id: is-01m0yeakhe19nh62258eqbr3d3
title: Extract the shared Motion Lab shell and migrate the exact n=5 scenario
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-generalized-motion-lab.md
labels:
  - packing
  - visualization
  - motion-lab
dependencies:
  - type: blocks
    target: is-01m0yebd9ks8n9kjn3adq8npdv
parent_id: is-01m0yd38q3mxynbc38k3gyxt7f
created_at: 2026-08-26T07:07:35.853Z
updated_at: 2026-08-26T07:08:02.214Z
---
Move the reusable stage, controls, timeline, evidence panel, scenario registry, JavaScript, and CSS out of the one-off generator. Preserve the n=5 analytic formulas, source evidence, stable artifact path, deterministic generation, and parity controls. Use sqpack.render.style for square colors and the documented compact UI token subset.
