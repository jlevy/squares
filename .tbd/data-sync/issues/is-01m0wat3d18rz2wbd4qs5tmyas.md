---
type: is
id: is-01m0wat3d18rz2wbd4qs5tmyas
title: Make the H-042 pilot fail closed on an unresolved cone oracle
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-042-trump-incidence-rigidity-cores.md
delegate: trump_support_algorithm
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0sg2venckvcs3q1cr5v1qzc
created_at: 2026-08-25T11:27:40.448Z
updated_at: 2026-08-25T11:33:50.533Z
closed_at: 2026-08-25T11:33:50.520Z
close_reason: The branch-0 CLI now exits nonzero on unresolved or root-not-zero states, selftest requires the proper exact core, and an injected unresolved oracle remains terminal. The reviewed 14-second replay passes all sixteen checks.
resolution: null
duplicate_of: null
---
Independent phase-3 audit found the first uncommitted incidence_cores CLI always exits zero, while --selftest runs exact replay assertions only when minimization completed. An unresolved or root-not-zero pilot can therefore satisfy the frozen validation command. Return nonzero for every non-completed terminal state, require completed and proper output under --selftest, add an explicit refusal control, and record D-285 before integration.
