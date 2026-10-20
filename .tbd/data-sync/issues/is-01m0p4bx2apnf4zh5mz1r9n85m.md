---
type: is
id: is-01m0p4bx2apnf4zh5mz1r9n85m
title: "H-018: basin-entry measurement at n=11"
kind: task
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/paused/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bvjsw40qb2e41ycygyqr
created_at: 2026-08-23T01:39:37.161Z
updated_at: 2026-10-12T23:50:53.384Z
closed_at: 2026-10-06T08:46:01.668Z
close_reason: "Done: H-018 basin-entry at n=11 was measured and refuted as stated by exp-005 (ledger on main: H-018 refuted; packing/campaign/ideas.md row 7)."
resolution: null
duplicate_of: null
---
Runnable TODAY against the existing engine, unlike most of the strategy register. Perturb Trump's exact configuration by uniform noise of size eps, measure the fraction of runs returning within 1e-6, sweeping eps over 1e-5..1e-1 with 40 runs each. The eps at which the return rate collapses IS the basin width in the units the search moves in, so a refutation is as quantitative as a confirmation. Re-run after the LP quench lands: 'does the refiner hold the cell' is a sharper question than 'does the annealer wander back'.
