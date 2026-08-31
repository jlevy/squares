---
type: is
id: is-01m0s80pzvvz9r62g2cz63wwkf
title: "PR #17 review E10: make gate worker semantics truthful and serial at jobs one"
kind: bug
status: closed
priority: 1
version: 2
labels:
  - packing
  - focus-infrastructure
dependencies: []
parent_id: is-01m0rwwt8912eq5f3507d581e1
created_at: 2026-08-24T06:41:08.090Z
updated_at: 2026-08-24T07:13:45.309Z
closed_at: 2026-08-24T07:13:45.308Z
close_reason: "Merged in PR #18 at b3545d0: PACK_JOBS is documented as a per-step cap and --jobs 1 is serial at both layers; D-123 records the correction."
resolution: null
duplicate_of: null
---
The stacked implementation calls PACK_JOBS a shared global budget, but it is a per-step cap and concurrent pools can oversubscribe. Narrow the claim or implement global coordination; --jobs 1 must also force one inner worker. Add focused verification.
