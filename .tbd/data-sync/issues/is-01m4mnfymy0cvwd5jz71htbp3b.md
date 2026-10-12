---
type: is
id: is-01m4mnfymy0cvwd5jz71htbp3b
title: "PR #496 E6: --since/--changed-paths-file exclusion and NUL-path rejection untested"
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
created_at: 2026-10-11T05:03:14.077Z
updated_at: 2026-10-12T23:39:27.481Z
started_at: 2026-10-11T05:03:51.139Z
closed_at: 2026-10-12T23:39:27.481Z
close_reason: "Fixed in PR #507 (merged 2026-10-12): tests cover the --since/--changed-paths-file mutual exclusion and a NUL-carrying snapshot path."
resolution: null
duplicate_of: null
---
Suggestion. packing/tests/test_reachable_tests.py:648-690; packing/devtools/reachable_tests.py:494-552. Fix: one case each for the argparse mutual exclusion and a snapshot path containing NUL. PR #496, review E: https://github.com/jlevy/squares/pull/496#pullrequestreview-5481683586
