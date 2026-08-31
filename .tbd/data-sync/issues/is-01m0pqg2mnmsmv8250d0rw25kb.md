---
type: is
id: is-01m0pqg2mnmsmv8250d0rw25kb
title: sqsearch does not emit pair_tests, the campaign's declared budget currency
kind: bug
status: closed
priority: 1
version: 8
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0rkz14t04yjme92gnfncfv7
child_order_hints:
  - is-01m0w7pwm6bcbzgntdrxmg2x9t
  - is-01m0w80zys1jhyt1qfz91pp66v
  - is-01m0w81076ba74rjm7tyrxm4h6
  - is-01m0w864pxhkpq48zsvt4akx4g
created_at: 2026-08-23T07:13:56.885Z
updated_at: 2026-08-25T10:52:13.715Z
closed_at: 2026-08-25T10:52:13.714Z
close_reason: Pushed checkpoint a9330d6 adds exact caller-owned pair_tests to both sqsearch Outcomes, every ordinary chain and basin-entry trial, and checked summaries. Cargo integration tests assert 54-per-outcome and exact summary sums; the complete normal gate passes. This closes missing emission only; think-b4jc retains budget migration and campaign adapters.
resolution: null
duplicate_of: null
---

## Notes

2026-08-25 session-010 phase14 bounded vertical slice: define one pair_test as one actual search-side pair_depth evaluation; emit exact per-chain/trial and summary counts while retaining move budgets. Full switch of budgets, saturation thresholds, and cross-proposer comparisons remains think-b4jc. Implementation stop 03:43 PDT; phase deadline 03:53.
