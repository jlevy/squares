---
type: is
id: is-01m5bhc1y4vxprenpanxz4wnwf
title: "Bound pytest temporary output: failed-only retention, reclaim killed sessions, shrink top writers"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: lane-pytest-tmp
labels:
  - efficiency
dependencies: []
parent_id: is-01m0rrgqj3esjc4jx1fr3qy1ht
hold: null
hold_until: null
created_at: 2026-10-20T02:13:44.003Z
updated_at: 2026-10-20T02:13:48.451Z
started_at: 2026-10-20T02:13:48.451Z
---
Owner request 2026-10-20: 'fix the ongoing issue with filling up file systems with pytest junk? Either outputs should be smaller and/or cleaned up automatically'. On the remote host /tmp/pytest-of-root reached ~11 GB across ~19 basetemp dirs from runs on 15-16 Oct (pytest-N dirs 0.5-1.6 GB; pytest-132 had 1,325 entries and pytest-3 still existed with 450), filling the 39 GB root filesystem twice. pytest keeps 3 numbered sessions by default (policy 'all', whole trees) and treats a session's .lock as stale only after three days, so a session killed by SIGTERM/SIGKILL (validation deadline or cancel, agent command timeout) keeps its whole tree for three days: pytest-3 surviving 129 later sessions shows that. Fix: failed-only retention with an explicit count in packing's pytest config; reclaim numbered/garbage dirs whose lock names a dead process; measure per-test tmp_path bytes with a reusable tool and shrink the top writers where the test does not weaken; tests and a development.md note. Related: think-y3pe (fresh per-run external TMPDIR on the owner's host).
