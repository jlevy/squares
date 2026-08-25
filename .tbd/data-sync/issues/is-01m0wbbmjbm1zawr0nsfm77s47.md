---
type: is
id: is-01m0wbbmjbm1zawr0nsfm77s47
title: Separate an exact H-042 miss from a selftest failure
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/campaign/hypotheses/H-042-trump-incidence-rigidity-cores.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0sg2venckvcs3q1cr5v1qzc
created_at: 2026-08-25T11:37:15.082Z
updated_at: 2026-08-25T11:37:15.082Z
---
The branch-0 golden selftest appropriately expects its now-known proper core, but reusing that mode on a new branch would exit nonzero when a completed exact minimization found no proper core. That is a valid refutation of H-042, not an instrument failure. Before wider execution, split structural selftests from expected scientific outcome and retain criterion_missed with exit zero. D-291 owns the validity distinction.
