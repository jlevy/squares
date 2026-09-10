---
type: is
id: is-01m22b979eff0y13xdew7kpa6y
title: Expose the three optimisation primitives as separate buttons in Pack
kind: feature
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:47:04.365Z
updated_at: 2026-09-09T05:47:04.365Z
---
The workbench currently offers one blended Optimize. The owner's decomposition is the repository's own, and separating it gives real control:

1. LP at fixed angles. sqpack.research.quench.solve_cell fixes every orientation and the separating axis holding each pair apart, then solves a linear program over the container side and all centres, minimising the side. Exact for that cell, not a heuristic. Cannot change orientations or which pairs touch. solve_to_fixed_point iterates it as the cell is re-read.

2. Rotational optimisation. The angle half of quench_bracket: merge angles into classes, bracket each by golden section. Golden section rather than gradient for a measured reason, H-019 confirmed the side as a function of angle has corners rather than smooth minima.

3. Physics, moving positions and angles together, approximately. Its distinct strength is that it can change which squares touch, which the LP cannot because the contact structure is fixed as part of the cell.

That is the propose-then-polish division the record engines use. The buttons should compose (shake, LP, angle search, LP) and each should state what it guarantees, because they differ sharply: the LP returns the optimum for its cell, the angle search a local improvement, the physics neither.

This also answers the rigid-contact instability in think-r2qd from the other side: a rigid contact is a constraint, and quenching solves constraints rather than integrating stiff forces, so 'rigid' may be better served by an LP button than by a stiffer spring.

Wiring: the solver is Python and the page is a browser document, but the precedent exists in packing/devtools/serve_packing_motion_lab.py and the free-quench lab, where the browser owns the editor and Python owns the quench over a loopback interface with typed, replayable requests and traces. Copy that shape rather than porting the linear program into JavaScript. Owner's design, 2026-09-08.
