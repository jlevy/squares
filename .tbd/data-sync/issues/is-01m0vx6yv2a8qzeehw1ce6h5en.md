---
type: is
id: is-01m0vx6yv2a8qzeehw1ce6h5en
title: Reject numeric drift even when frontier lanes share evidence
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-frontier-assurance-and-verification.md
labels:
  - packing
  - soundness
dependencies: []
parent_id: is-01m0typjn7s866m042zsemybj6
created_at: 2026-08-25T07:30:01.679Z
updated_at: 2026-08-25T07:30:06.884Z
closed_at: 2026-08-25T07:30:06.883Z
close_reason: "Fixed in the implementation checkpoint: evidence identity no longer bypasses numeric comparison; exact literal identities are cross-checked; rounded/truncated display tolerance is bounded; the shared-evidence drift regression and the full 100-case schema audit pass."
resolution: null
duplicate_of: null
---
Precommit review found that bounds_agree_at_declared_precision returned true solely because reported and verified lanes shared an evidence id. That could suppress a formal-gap blocker even if their values drifted. Require exact identities and displayed numbers to remain consistent; retain a narrow allowance for rounded or source-truncated renderings; add a regression with shared evidence and inconsistent values.
