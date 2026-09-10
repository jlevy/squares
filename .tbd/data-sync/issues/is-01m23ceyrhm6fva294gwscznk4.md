---
type: is
id: is-01m23ceyrhm6fva294gwscznk4
title: Sweep the projection search's start policy properly
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-09-09T15:26:55.239Z
updated_at: 2026-09-09T15:26:55.239Z
---
exp-139 found the start policy is the dial that decides whether a run finds anything, and that it trades against quality: at n=5 every mixed or fully cold run left the grid (6 of 6) against 1 of 4 for pure continuation, but that single continuation escape reached 2.7082 where the best cold-mixed run reached 2.7691. Half cold gave the best n=11 side measured anywhere in the round (3.9234375, +1.201 per cent).

Three runs per condition is too few to call the ordering. Sweep cold in {0, 0.17, 0.33, 0.5, 0.67, 1.0} with enough repeats to separate the escape rate from the conditional quality, and report both statistics rather than the mean side, which blends a search result with a starting condition.

Entry point: devtools/run_projection_ratchet.py --cold.
