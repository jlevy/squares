---
type: is
id: is-01m84k5bya0m37kxbc0wgbgp7k
title: "Intake: verify Özden's 264-square packing (#1099)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: codex-intake-1099
labels:
  - intake
  - validation
dependencies: []
hold: null
hold_until: null
created_at: 2026-11-23T16:17:26.473Z
updated_at: 2026-11-23T16:21:50.196Z
started_at: 2026-11-23T16:17:39.786Z
---
Review https://github.com/jlevy/squares/issues/1099 and pinned rational-corners witness kenaznia-doga/s264-upper-bound-1677216830@72c4d195c85b6099002ad6c675b27df40fdaceac. Replay exact and independent verifiers, review provenance and compare with the T-308 house and GeiserX #1037 before disposition and potential adoption. Reviewed alongside the 23 November intake.

## Notes

23 November intake. Retained the pinned 721,390-byte rational-corners Witness/v2, issue JSON and published digest under external evidence drawing-audit-20261122/n264-1099-triage. Both maintained exact rational GMP paths verified all 264 unit squares and 34,716 pairs at side 16.77216830504054639626340160… and rejected duplicate-square and outside-wall controls. Each exact output and the memory-guard receipt are retained alongside it. Side is 0.00163929296145 smaller than published T-308 and 0.000674847636987 smaller than the retained but not yet adopted GeiserX #1037 report. The disclosed Kaggle leaderboard number with no coordinates is 0.00187977729055 smaller. Scope is finite feasible upper bound. Pending stage-3 source packet, report-order disposition, and house adoption with regularization.
