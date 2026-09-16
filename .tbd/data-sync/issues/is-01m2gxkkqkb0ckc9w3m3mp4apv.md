---
type: is
id: is-01m2gxkkqkb0ckc9w3m3mp4apv
title: Extract each rung's hint from a record at declared tolerances, one implementation
kind: feature
status: open
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2gxkp2c5hk981zhv3aejfga
  - type: blocks
    target: is-01m2gxks9tdr1hhatv3mx359y3
  - type: blocks
    target: is-01m2gxkvbndg46r6pjy3352cb8
  - type: blocks
    target: is-01m2gxkzqdxb01e2h4tpkvczw7
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-14T21:36:41.202Z
updated_at: 2026-09-16T21:23:37.216Z
---
One implementation that turns a record's poses into each rung's hint, at declared tolerances, retained as data per n and shared by the Python search lane and the workbench.

Per record:
- **touching-cluster partition**, which nothing computes today (the existing "partition" rung means angle classes, and the chunk census joins only flush same-angle contacts);
- **contact graph**, square-square and square-wall: `known_structure.contact_edges` / `wall_contacts` exist in Python at 1e-9, while the workbench's `contactFacts` sees only aligned full sides (4 edges at n = 17 against 24 real contacts);
- **typed contacts**, edge-edge / corner-edge / corner-corner: exact only for n = 11 and 29 in `contact-structures.json`, and `known_structure.contact_kinds` miscounts n = 11 (8 edge-edge where the exact count is 7);
- **near-flush merged blocks** at a declared coarse tolerance, keeping each block's internal offsets from the record, which is the owner's simplified parallel level (the spike's `frame_clusters`, 4 degrees and centres within 1.2, is the closest existing grouping);
- **remaining degrees of freedom** once the hint's constraints are imposed, from the constraint rank at the record (the chunk census's `2m - rank - 2` is the pattern), so rungs compare across n.

Acceptance: fixture records n = 5, 11, 17, 29 reproduce the exact counts where they are known; tolerances are recorded with the output; the same data is readable from Python and TypeScript.

Also feeds think-hk37: the same extraction is what decides rigidity marks.

## Notes

2026-09-16 requirement transfer from duplicate think-1han: extraction must include oriented face-pair targets, symmetry/correspondence rules, declared ambiguity handling, and refusal when a target cannot be interpreted uniquely enough for the requested rung. Reuse the contact atlas feature representation.
