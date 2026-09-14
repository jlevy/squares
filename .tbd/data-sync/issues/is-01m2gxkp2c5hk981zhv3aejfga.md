---
type: is
id: is-01m2gxkp2c5hk981zhv3aejfga
title: "Kernel mechanics for staged structure: weld and release, aligning torque, range, per-body shake, pins"
kind: feature
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2gxkvbndg46r6pjy3352cb8
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-14T21:36:43.591Z
updated_at: 2026-09-14T21:41:16.154Z
---
The mechanics a staged, structure-informed run needs and no engine has (survey 2026-09-14):

- **weld and release on a schedule**: the kernel already supports multi-square rigid bodies (`SimulationBodyDefinition`, `packages/workbench/src/simulation/kernel.ts` on PR #160), but `pack.ts` always builds one body per square and nothing releases a weld mid-run;
- **an aligning torque** for pairs typed flush, since a central pull brings pairs together corner-to-side (n = 17's target pair ended 1.93 degrees apart; a full-side contact needs 0.5);
- **attraction range as a parameter**, since the shipped 0.25 of a side cannot reach target pairs 1-4 units apart;
- **per-body shake amplitude**, so welded blocks can hold while loose squares shake;
- **partial pins** for the partial-pose rung (today there is one pin and one global stiffness);
- constraints as **bands, never equalities**: exact tangency repels, which X-025 measured.

Each is a parameter of a Pack run, so Pack, Search and Animate share it. Every mechanic ships with a unit test in the package, and a snapped control must still end on the record.
