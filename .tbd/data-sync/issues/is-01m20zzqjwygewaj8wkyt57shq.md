---
type: is
id: is-01m20zzqjwygewaj8wkyt57shq
title: sqsearch arms behind flags, and the two sweep instruments
kind: feature
status: open
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m20zyy839t6mbvpqy8ay2hsn
created_at: 2026-09-08T17:10:24.588Z
updated_at: 2026-09-09T00:20:12.012Z
---
Done in this session, recorded so the follow-ups have a parent.

sqsearch gained three flags, all off by default so the control stays reachable and bit-identical:
- --p-perturb / --perturb-scale: Gensane layer 3, a proposal that displaces every square at once (H-135).
- --mu0 / --mu1: an aggregate inward wall-pressure term, geom::spread, ramped like lambda (H-136).
- --budget-pair-tests: a per-chain cap in the campaign's declared budget currency, so arms whose per-move cost differs are comparable.

The selftest pins the control chain to the literal the pre-arm engine printed, exercises both arms for validity, and checks the pair-test cap binds. unsafe_code = "forbid" and the pedantic clippy floor are unchanged; cargo test is green.

Instruments: packing/devtools/run_arm_sweep.py and packing/devtools/run_basin_hopping.py.
