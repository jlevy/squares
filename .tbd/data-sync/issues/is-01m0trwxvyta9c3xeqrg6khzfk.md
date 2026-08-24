---
type: is
id: is-01m0trwxvyta9c3xeqrg6khzfk
title: Fix stratum-dependent n=5 tangent contact rows before exp-035
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: explorations/packing/campaign/agendas/agenda-001-basin-confidence-ladder.md
labels:
  - packing
  - soundness
  - experiment-tooling
dependencies: []
parent_id: is-01m0tpn9ej3z97jr6nq97fb9gt
created_at: 2026-08-24T20:55:24.284Z
updated_at: 2026-08-24T20:55:28.894Z
---
The committed but unexecuted check_n5_tangent_cones.py reuses one hand-written (0,4) contact differential at endpoint A, the interior, and endpoint B. The owner-axis rotation coefficient depends on the slide position, so the advertised interior/B non-sheet witnesses are not certified by the true first-order constraints. Replace contact rows with exact per-stratum derivation from pose geometry, prove the active inventory separately at every stratum, add a mutation that rejects the stale coefficient, and only then preregister or run exp-035. Log as D-194; no scientific artifact has yet been produced.
