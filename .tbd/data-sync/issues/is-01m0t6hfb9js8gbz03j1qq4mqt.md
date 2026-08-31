---
type: is
id: is-01m0t6hfb9js8gbz03j1qq4mqt
title: Run and retain the first n=3 BasinEvent calibration
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
created_at: 2026-08-24T15:34:34.599Z
updated_at: 2026-08-24T15:34:48.248Z
closed_at: 2026-08-24T15:34:48.247Z
close_reason: "exp-018 completed from clean commit ee3acc1 under a 60s process cap: 4/4 full poses independently valid, 3/4 producer-converged, 2 at exact side 2, 3 raw geometric/contact descriptors, 10.0248s total quench wall, and 0/4 scientifically admissible because D-165 is enforced. Replay, schema, ledger, synopsis, and formatting checks pass."
resolution: null
duplicate_of: null
---
Execute exp-018 as a four-seed, hard-capped n=3 positive-control block from a clean instrument commit. Retain starts, full poses, producer termination, independent validity, canonical descriptors, per-event timing, and explicit promotion blockers. Acceptance: replay passes; experiment and ledger agree; no endpoint key is called a component; result is blocked rather than accepted while D-165 is open.
