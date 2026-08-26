---
type: is
id: is-01m0y2vvd18pd978cxrnt4h72g
title: "Spike: rank Square Packing CI and research-loop bottlenecks"
kind: task
status: in_progress
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-26T03:47:18.048Z
updated_at: 2026-08-26T04:13:48.129Z
---
Use CodexEfficiencyRollup/v1, recent GitHub Actions receipts, pytest duration profiling, and negative-control worker-count samples to rewrite the active W5 plan with measured cost shares, concrete spike commands, expected seconds saved, equivalence guards, stop/go thresholds, and sub-agent routing experiments. This spike changes documentation and tracking only; production speedups remain in their existing implementation beads.

## Notes

2026-08-26 evidence package: 24 successful workflows have 346s p50 and 430s p95; current PR is 378s Linux and 436s macOS. Current exact tests take 212.53s versus 14.95s for the other 94 tests. Controls take 158.54/98.17/90.19s at 1/2/4 workers. Loop 2 frozen snapshot has 4h33m02s parent active, 9h11m11s recursive agent-time, 65 broad-agent follow-ups, a 41m tail, and 1,743.33 repeated validation command-seconds. The rewritten plan ranks one-minute CI fan-out, exact inventory reuse, deterministic control sharding, validation receipts, and bounded leaf-agent/model experiments.
