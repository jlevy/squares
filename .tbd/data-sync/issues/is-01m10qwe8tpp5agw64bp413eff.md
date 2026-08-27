---
type: is
id: is-01m10qwe8tpp5agw64bp413eff
title: "W7: build and price the CG-010 target-free full cell"
kind: feature
status: in_progress
priority: 0
version: 4
spec_path: explorations/packing/campaign/agendas/agenda-003-balanced-ten-hour-research-program.md
labels:
  - packing
  - focus-correctness
dependencies: []
created_at: 2026-08-27T04:33:06.328Z
updated_at: 2026-08-27T07:30:15.998Z
---
Own the constructive-enumeration successor to completed BC-019. Define and exercise one target-free full fixed-angle cell with declared walls, one frozen separating axis per non-edge, canonical ties, typed caps, and explicit pricing for angle assignments, wall seatings, non-edge axes, and symmetry orbits. This is reusable W7 instrumentation only: do not consult atlas geometry, run n=11, claim H-044/H-045, or infer geometry or feasibility from the 11,013 abstract scaffolds.

## Notes

Session 026 completed CG-010's first structural implementation slices. FullFixedAngleCellLabel/v1 is intentionally axis-aligned and source-free: the literal n=3 L has a complete partition, all 12 square-wall decisions, an exhaustive two-contact/one-nonedge pair inventory, one oriented axis per pair, joint D4-by-relabeling canonicalization over 48 images, and a derived price that separates an eight-branch candidate domain from one selected raw cell. The generated ContactFullCellControl/v1 artifact and seven focused negative controls are green; LP solves remain zero. Next: independent W2 audit and W3 decision between BC-016 and BC-017. Numerical row compilation, mixed angles, atlas geometry, H-044/H-045 verdicts, and n=11 execution remain out of scope.
