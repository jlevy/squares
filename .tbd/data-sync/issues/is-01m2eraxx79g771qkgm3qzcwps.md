---
type: is
id: is-01m2eraxx79g771qkgm3qzcwps
title: Maintain BC303 Q0 equipment and label controls
kind: task
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - validation
dependencies:
  - type: blocks
    target: is-01m2evnx0hq9wt4st1a6vcm2cm
parent_id: is-01m2agbyn3sd63v0j87jer8vz0
created_at: 2026-09-14T01:26:04.966Z
updated_at: 2026-09-14T02:24:30.223Z
---
Build a maintained exact geometry control for Q0 source-cell uniqueness, both axis aliases, complete closed-bin labels, and fixed-parent product gluing; include a correlated-equipment negative control. This validates implementation of the analytic result, not local availability or eleven-parent extension.

## Notes

2026-09-14: Source-distinct equipment review think-jb87 closed. Sol committed clean target-free control branch codex/bc303-q0-geometry-controls at af8996e0bc414342a90b34692cf7139196c7d2c6, based on H162 f58. Exact checker and 4 focused tests validate Q0 source cell 0, both physical axis aliases/common core, closed labels {3,4,11,12}, cross-corner separation, four mirrored partial parents, product gluing, and a correlated-choice negative fixture. Ruff, BasedPyright, and edit tier 45/74 green. No target, extension, or bound. Stack on X032 and obtain hosted CI before closure.
