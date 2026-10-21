---
type: is
id: is-01m5bqma4efj7297bmf3ryk0vc
title: Hold quick tests to a per-test tmp_path size ceiling, beside the wall ceiling
kind: task
status: open
priority: 3
version: 1
spec_path: docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
labels:
  - efficiency
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
created_at: 2026-10-20T04:03:05.998Z
updated_at: 2026-10-20T04:03:05.998Z
---
Follow-up from think-46yk (bounded pytest temporary output). That branch shrank the largest quick-lane writer (test_replay_bc303_t1_witness: a full shared clone, 663 MiB and 6,538 files per run, now a sparse checkout of the reader and its sources) and gave three module-scoped fixtures back at module end, but nothing stops the next test from writing a 600 MiB tree again. A single per-test budget in pyproject was tried and withdrawn: the slow lane has tests that write about 360 MiB by design (test_negative_controls::test_build_caches_leave_the_counted_surface_and_the_worker_trees, test_fn1_input_bindings::test_actual_worker_carries_every_input_and_refuses_a_receipt_mutant, test_evand_arrangement_adoption::test_production_clone_copies_every_scientific_input_and_admits_exact_links), so one ceiling either misses the regression or fails them. Proposal: enforce the ceiling where the 12 s wall ceiling lives, on the quick lane's own command (sqpack.cli.validate._quick_lane_command and the reachable-test wrapper), and treat a test above it like a test above the wall ceiling: shrink it, or mark it slow with its measurement. Measure first, with devtools.pytest_tmp --tmp-usage over the whole quick lane: the largest quick writers after think-46yk, and the wall cost of walking every tmp_path at teardown. Acceptance: the ceiling, its measured headroom, and a test that an oversized quick test fails.
