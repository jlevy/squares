---
type: is
id: is-01m2evx90j8rk1f4sewm4pymsr
title: Build the gate budget re-record tool from hosted readings (OR-1)
kind: feature
status: open
priority: 1
version: 2
labels:
  - validation
  - ci
dependencies: []
created_at: 2026-09-14T02:28:31.889Z
updated_at: 2026-09-16T00:18:50.606Z
---
OR-1 gap: no maintained tool turns hosted gate readings into a recorded budget mean. packing/src/sqpack/gate_budgets.py only prints the `measured_seconds` line to paste (:363, :384) and check_gate_budgets.py validates the register's shape. The 2026-09-14 headroom analysis used one-off scripts (steps.py queue timeline from start/end receipts, sim.py `--jobs N` replay, suite.py per-file test-seconds from junit) now sitting in a worktree attic. Build a devtools tool that downloads hosted job logs/junit for named runs, reconstructs per-step and per-test timing, replays the queue, and emits the geometric-mean record under the register's reference-shape rules, with tests; then use it for the checks and suite re-records.

## Notes

2026-09-15 (think-z121): half of this is now built, so it is raised to P1 rather than closed. The one-off scripts described above are a tool: `packing/devtools/read_tier_walls.py` reads the tier wall and the eight slowest steps out of each hosted job log, groups readings by the gate's own step count so only comparable shapes pool, and prints both the geometric-mean record and the attribution block a raised record needs. It wrote every record landed on 2026-09-15 in `packing/devtools/gate-budgets.yaml` -- `checks` 145.53 s, `frontend` 76.66 s, `geometry` 102.73 s, `sweeps` 119.72 s -- from runs 34924677097, 34925616821, 34926777301, 34929890466, 34930296150, 35012847055 and 35013703659. The wall half of the original ask is covered separately by `packing/devtools/check_pr_wall.py --sample`. What remains, and what this bead is now only for, is the per-test half: junit per-file costs joined to the record, which is what think-z121's ratchet rule will demand the next time `suite` is raised past 123.40 s.
