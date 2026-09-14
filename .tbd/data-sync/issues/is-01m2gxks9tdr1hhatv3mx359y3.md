---
type: is
id: is-01m2gxks9tdr1hhatv3mx359y3
title: Build starts from structure, keeping the record's internal offsets
kind: feature
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2gxkvbndg46r6pjy3352cb8
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-14T21:36:46.852Z
updated_at: 2026-09-14T21:41:16.191Z
---
The one use of structure with positive evidence is constructing the start: building face groups first lifted a cold projection solve from 1/8 to 5/8 at +10% side and from 2/8 to 4/8 at +4% (commit 2d2a7790). Nothing got within +2%.

`known_structure.assemble_from_faces` does it with exact unit offsets on the first free side, which invents the block shape. The record's flush groups are slid sideways, not on lattice offsets (exp-046), so the construction should keep each block's internal offsets from the extraction.

Deliverable: a start proposal per rung (partition, graph, typed, merged blocks, partial poses) in the package's `start-proposals`, deterministic per seed, with a validity check that the start itself is a packing in its inflated box.
