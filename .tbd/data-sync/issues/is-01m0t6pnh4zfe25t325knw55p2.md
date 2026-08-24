---
type: is
id: is-01m0t6pnh4zfe25t325knw55p2
title: Run and retain the first n=4 BasinEvent calibration
kind: task
status: closed
priority: 0
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-021-endpoint-identifiability.md
labels:
  - packing
  - focus-correctness
dependencies: []
parent_id: is-01m0t3n7z9fj0p7wwt1kn4nzqk
created_at: 2026-08-24T15:37:24.771Z
updated_at: 2026-08-24T15:37:35.042Z
closed_at: 2026-08-24T15:37:35.041Z
close_reason: "exp-019 completed from clean run commit 16829c9 using instrument ee3acc1: 4/4 poses independently valid, 2/4 producer-converged at exact side 2, 2 explicit cycles, 13.3216s total quench wall, and 0/4 admissible under D-165. Replay, schema, ledger, synopsis, and formatting pass."
resolution: null
duplicate_of: null
---
Execute exp-019 as a four-seed, hard-capped n=4 positive-control block from a clean instrument commit. Retain starts, full poses, producer termination, independent validity, descriptors, timing, and promotion blockers. Acceptance: replay and experiment ledger pass; exact n=4 topology is used only as a control; cycles remain examples rather than components.
