---
type: is
id: is-01m0yeakhe19nh62258eqbr3d3
title: Extract the shared Motion Lab shell and migrate the exact n=5 scenario
kind: task
status: closed
priority: 1
version: 4
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
updated_at: 2026-08-26T07:47:16.878Z
closed_at: 2026-08-26T07:47:16.853Z
close_reason: Extracted package-owned Motion Lab CSS and JavaScript assets, adapted the retained exact n=5 manifest to the shared scenario contract, embedded a scenario registry, applied the compact tbd-derived visual vocabulary and complete publication palette, regenerated the standalone artifact, and preserved all exact-model parity contracts. Fast validation passed (151 tests).
resolution: null
duplicate_of: null
---
Move the reusable stage, controls, timeline, evidence panel, scenario registry, JavaScript, and CSS out of the one-off generator. Preserve the n=5 analytic formulas, source evidence, stable artifact path, deterministic generation, and parity controls. Use sqpack.render.style for square colors and the documented compact UI token subset.
