---
type: is
id: is-01m2agbxyzknj4s538jxexx8dz
title: Test whether new atoms remove the whole old optimal dual face
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m24r3sgyw8hj7k7cfd8spmxg
created_at: 2026-09-12T09:49:51.454Z
updated_at: 2026-10-06T08:38:20.000Z
closed_at: 2026-10-06T08:38:20.000Z
close_reason: "Superseded by T-060: s(11) equals Trump's side, registered 2026-09-29 at V3/C3 and on main since PR #246 (merged 2026-09-30). This n = 11 lower-bound certificate work has no target left; the owner's 2026-09-14 strategy reset had already paused it, and the post-optimality plan (plan-2026-10-01) uses n = 11 only as a control."
resolution: canceled
duplicate_of: null
---
For one prospectively frozen common placement support and admitted new-atom bundle, test the full optimal face of the old finite LP rather than only the solver's returned optimum. Establish exactly whether every old optimum violates at least one admitted new capacity row, or retain an old optimum that survives. Use the same rows and source bytes in both arms, exact primal/dual certificates, and independent replay. A cut to one selected optimum or a strict finite-program improvement does not imply a continuum certificate or a new packing bound.
