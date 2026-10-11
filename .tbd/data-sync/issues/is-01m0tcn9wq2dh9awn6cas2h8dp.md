---
type: is
id: is-01m0tcn9wq2dh9awn6cas2h8dp
title: Scope PR20 interval and equality-certification claims
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - review
  - soundness
dependencies: []
parent_id: is-01m0tbtgpb92e81ndvw4xm9be6
created_at: 2026-08-24T17:21:31.542Z
updated_at: 2026-10-10T22:49:39.579Z
closed_at: 2026-08-24T17:36:29.763Z
close_reason: "D-173 fixed: float/interval limitations are scoped to enclosure-only inference of unknown contacts, while structural zero and certified root methods remain valid; normal gate passed."
resolution: null
duplicate_of: null
---
PR #20 claims floating point/interval arithmetic can never certify equality or contact. Narrow this to unrecognised near-contacts inferred from numeric enclosures; acknowledge exact-zero structural evaluation and certified root methods; record D-173.
