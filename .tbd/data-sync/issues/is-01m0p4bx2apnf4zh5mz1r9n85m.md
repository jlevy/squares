---
type: is
id: is-01m0p4bx2apnf4zh5mz1r9n85m
title: "H-018: basin-entry measurement at n=11"
kind: task
status: open
priority: 1
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bvjsw40qb2e41ycygyqr
created_at: 2026-08-23T01:39:37.161Z
updated_at: 2026-08-23T01:41:08.664Z
---
Runnable TODAY against the existing engine, unlike most of the strategy register. Perturb Trump's exact configuration by uniform noise of size eps, measure the fraction of runs returning within 1e-6, sweeping eps over 1e-5..1e-1 with 40 runs each. The eps at which the return rate collapses IS the basin width in the units the search moves in, so a refutation is as quantitative as a confirmation. Re-run after the LP quench lands: 'does the refiner hold the cell' is a sharper question than 'does the annealer wander back'.
