---
type: is
id: is-01m2ey0d8smw4f4w72hyay9070
title: "Route C: orientation-class structure theorem near Trump's packing"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-14T03:05:11.704Z
updated_at: 2026-09-14T03:05:11.704Z
---
Prove that any packing beating 3.877 needs at least three distinct orientations: exact disjunctive LP at fixed angles, robust Farkas covers over angle intervals, and the BC-240 isolation theorem near Trump's angle. Precedent: Stromquist's 0/45-degree theorem. First test: solve 6+5 globally at Trump's angle (must return U), then 1-degree bins at 3.87 to measure the exceptional window. A 150 s plain big-M HiGHS probe found no layout, so this needs seeded layouts or custom branching on the cell LP.
