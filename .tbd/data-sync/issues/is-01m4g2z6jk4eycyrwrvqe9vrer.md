---
type: is
id: is-01m4g2z6jk4eycyrwrvqe9vrer
title: "Main red after stack 455: post-merge per-test 12 s wall ceiling"
kind: bug
status: open
priority: 0
version: 1
labels:
  - n-17
dependencies: []
parent_id: is-01m4fhz39j0nmrca9x38tyrnsg
created_at: 2026-10-09T10:22:33.041Z
updated_at: 2026-10-09T10:22:33.041Z
---
Post-merge Packing run 37910870148 on main 533dd42c6 failed fast shards A/B on the per-test 12 s wall ceiling (enforced post-merge, relaxed to warning on PRs): test_retained_json_layout::test_the_repository_as_it_stands_passes 32.5 s (was <6 s before the stack), two test_check_n17_two_child_collective_propagation nodes 18-19 s, four test_check_n17_one_round_owned_domain_propagation nodes 14-16 s, test_overview 12.1 s (noise). Fix: speed up or mark slow with measured registry entries; ride PR #473 (designated branch) and land promptly.
