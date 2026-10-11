---
type: is
id: is-01m2ge1hbswk78jv4aa118pan6
title: Make the Search scheduler admission tests independent of wall-clock time
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-14T17:04:40.310Z
updated_at: 2026-10-06T08:30:52.800Z
closed_at: 2026-10-06T08:30:52.779Z
close_reason: "Done: c426eec17 'Freeze the clock in the Search admission test' (2026-09-14) is on origin/main; every Search scheduler test not about the deadline injects now: () => 0."
resolution: null
duplicate_of: null
---
packages/workbench/tests/search-scheduler.test.ts gives every trial in plan() a 5 ms wall-clock deadline (timeout_ms: 5), so under machine load 'fixed physics work and validity are admission conditions' saw a trial report timed-out where it asserts failed (observed 2026-09-14 on a local node --test run; three reruns passed). Tests that are not about the deadline should not race it: inject the scheduler's options.now clock, or give admission tests no deadline, and keep one deterministic timeout test.
