---
type: is
id: is-01m229b9y5bxr21t7kngnx4esn
title: De-duplicate the collision routine in the workbench simulator
kind: chore
status: closed
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels:
  - packing
dependencies: []
parent_id: is-01m1z68hzazv9yjs9k7cddmf82
created_at: 2026-09-09T05:13:15.460Z
updated_at: 2026-09-13T05:42:45.322Z
closed_at: 2026-09-13T05:42:45.321Z
close_reason: "Superseded by think-nubm: shared browser/Node kernel extraction includes collision de-duplication and preservation of unique regression controls. No implementation completion claimed."
resolution: null
duplicate_of: null
---
collide and optCollide in the v2-transitions template are two copies of the separating-axis test, the most delicate arithmetic on the page. They were kept separate so four checkers' byte-comparisons stayed valid. Merge into one shared collide(ctx, i, j) and prove it by byte-comparing trajectories either side of the change.
