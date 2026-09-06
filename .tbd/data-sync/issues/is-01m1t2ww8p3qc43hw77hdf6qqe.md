---
type: is
id: is-01m1t2ww8p3qc43hw77hdf6qqe
title: Bridge a row-converged cutting-loop primal to a decidable certificate candidate
kind: task
status: closed
priority: 1
version: 2
labels:
  - research
dependencies: []
parent_id: is-01m1t2sgqmantgyx59knjxqheg
created_at: 2026-09-06T00:46:35.796Z
updated_at: 2026-09-06T01:02:19.725Z
closed_at: 2026-09-06T01:02:19.724Z
close_reason: "Implemented on PR 89 in commit c0db25cf: devtools.freeze_cutting_primal (bridge with tests), run_fractional_cutting --seed-certificate/--seed-map with tests, and cases/n12_fractional_certificate/replay_independent.py with the evidence replay repointed and tested; agenda-025 pre-registers the scalar 61/16 probe for the coordinator to allocate or decline at T+0."
resolution: null
duplicate_of: null
---
The cutting-plane driver (devtools.run_fractional_cutting) retains sites and snapped rows in its state file but freezes only the exact packing family; its covering-side LP weights are discarded. BC-232's one lower-bound outcome, a row-converged covering objective below 11 at 3.82, therefore had no path to bytes that devtools.decide_certificate can decide (agenda-025 says 'request a tested rationalize/freeze bridge'). Build devtools.freeze_cutting_primal: load the state, run row generation to convergence, re-solve the covering LP, rationalise the weights as colgen does (bump, round up to 1/scale), write the candidate in the retained shape with least_cell_mass null, refuse an unconverged row set, an LP failure, a total at or above n, or an existing output path. Then declare_least_cell_mass and decide_certificate decide the bytes.
