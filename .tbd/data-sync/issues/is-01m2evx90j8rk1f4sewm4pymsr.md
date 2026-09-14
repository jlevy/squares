---
type: is
id: is-01m2evx90j8rk1f4sewm4pymsr
title: Build the gate budget re-record tool from hosted readings (OR-1)
kind: feature
status: open
priority: 3
version: 1
labels:
  - validation
  - ci
dependencies: []
created_at: 2026-09-14T02:28:31.889Z
updated_at: 2026-09-14T02:28:31.889Z
---
OR-1 gap: no maintained tool turns hosted gate readings into a recorded budget mean. packing/src/sqpack/gate_budgets.py only prints the `measured_seconds` line to paste (:363, :384) and check_gate_budgets.py validates the register's shape. The 2026-09-14 headroom analysis used one-off scripts (steps.py queue timeline from start/end receipts, sim.py `--jobs N` replay, suite.py per-file test-seconds from junit) now sitting in a worktree attic. Build a devtools tool that downloads hosted job logs/junit for named runs, reconstructs per-step and per-test timing, replays the queue, and emits the geometric-mean record under the register's reference-shape rules, with tests; then use it for the checks and suite re-records.
