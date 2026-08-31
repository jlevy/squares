---
type: is
id: is-01m0t6vhfpqs3pw4dtdjzjf7qg
title: Run and retain the first n=5 BasinEvent calibration
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
created_at: 2026-08-24T15:40:04.469Z
updated_at: 2026-08-24T15:40:17.228Z
closed_at: 2026-08-24T15:40:17.227Z
close_reason: "exp-020 completed from clean run commit 79910a9 using instrument ee3acc1: 4/4 poses valid and producer-converged, two sides observed, no proved optimum found, 14.8211s total quench wall, 3 raw descriptors, and 0/4 admissible under D-165. Replay, schemas, ledger, synopsis, and formatting pass."
resolution: null
duplicate_of: null
---
Execute exp-020 as a four-seed, hard-capped n=5 positive-control block from a clean commit. Retain full evidence and stop scaling if added samples remain promotion-blocked. Acceptance: replay and ledger pass; no descriptor is called a component; the absence of the proved optimum is recorded as an observation, not an algorithmic impossibility.
