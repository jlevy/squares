---
type: is
id: is-01m4g2z6jk4eycyrwrvqe9vrer
title: "Main red after stack 455: post-merge per-test 12 s wall ceiling"
kind: bug
status: in_progress
priority: 0
version: 4
delegate: claude-code@vm
labels:
  - n-17
dependencies: []
parent_id: is-01m4fhz39j0nmrca9x38tyrnsg
child_order_hints:
  - is-01m4g7nsqn6jdnyg1kbc1nekhm
hold: null
hold_until: null
created_at: 2026-10-09T10:22:33.041Z
updated_at: 2026-10-09T11:44:47.861Z
started_at: 2026-10-09T10:43:09.858Z
---
Post-merge Packing run 37910870148 on main 533dd42c6 failed fast shards A/B on the per-test 12 s wall ceiling (enforced post-merge, relaxed to warning on PRs): test_retained_json_layout::test_the_repository_as_it_stands_passes 32.5 s (was <6 s before the stack), two test_check_n17_two_child_collective_propagation nodes 18-19 s, four test_check_n17_one_round_owned_domain_propagation nodes 14-16 s, test_overview 12.1 s (noise). Fix: speed up or mark slow with measured registry entries; ride PR #473 (designated branch) and land promptly.

## Notes

2026-10-09T10:43Z Fix 54122fed0 pushed on #473 (claude/modest-pascal-z3nisd): 7 nodes marked slow with measured registry entries (retained-JSON sweep 32.5 s hosted — still runs per PR as gate step; six n17 propagation nodes 14-19 s hosted); custody tamper fresh_geometry split out; test_overview uses existing result_bodies fixture (not marked). Deep gate dispatched on #473.
