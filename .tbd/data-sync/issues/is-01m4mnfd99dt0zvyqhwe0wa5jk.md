---
type: is
id: is-01m4mnfd99dt0zvyqhwe0wa5jk
title: "PR #496 E1: --push and --since banners print to stdout under --format json"
kind: bug
status: closed
priority: 3
version: 3
delegate: claude-code@spud10
labels: []
dependencies: []
parent_id: is-01m4mneswbxt0m4w1caxy0x320
hold: null
hold_until: null
created_at: 2026-10-11T05:02:56.296Z
updated_at: 2026-10-12T23:39:23.491Z
started_at: 2026-10-11T05:03:48.695Z
closed_at: 2026-10-12T23:39:23.491Z
close_reason: "Completed: --push/--since banners go to stderr under --format json; fixed in PR #507 (merged 2026-10-12, e96e9ea95) with tests in tests/test_validation_cli.py."
resolution: null
duplicate_of: null
---
Low. packing/src/sqpack/cli/validate.py:7442-7449 (--push banners), :7468 (pre-push floor line), :7473-7484 (--since block). packing-validate --push --since origin/main --list --format json writes banner lines before the JSON array. Fix: route the block's banners to stderr under --format json, as _unless_verified does (:6156-6161); add a test that --push --list --format json stdout parses as one JSON document. PR #496, review E: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481683586
