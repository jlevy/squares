---
type: is
id: is-01m2ksd6tqpr55mtg89rvzd1jf
title: Join Codex task-tree rollups and Claude session costs into one agent-time report
kind: feature
status: open
priority: 3
version: 1
spec_path: explorations/packing/docs/project/reviews/review-2026-08-23-square-packing-program-and-pr14.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-09-16T00:21:00.373Z
updated_at: 2026-09-16T00:21:00.373Z
---
The residue of think-xuk8, split out when that bead closed on 2026-09-15. Its detector half is built and running: `packing/devtools/check_pr_wall.py` measures hosted CI wall on every pull request, splits each job into queue, setup and work, and fails over a 180 s budget or 1.2x of a recorded median (think-z121). The hosted-CI, local-validation and declared-budget inputs of the original report contract are therefore covered.

What nothing now carries is the agent-time join: recursive Codex task-tree rollups (CodexEfficiencyRollup/v2) and Claude session costs joined to those CI and local timings in one W5 report, so a block can be read as critical-path wall time beside recursive agent-time and model stream bounds rather than wall alone. OR-9 (a pull request leads with what the branch cost) and OR-12 (one block in four to eight is an efficiency block, and the record says which) are what would consume it.

Constraints carried over from think-xuk8's report contract: versioned inputs identifying revision, platform, selected surface, worker settings, task roots, samples, medians, dispersion and prior-median delta; compact reviewed summaries that exclude raw prompts and private JSONL; scrubbed aggregates only in the repository, since local Codex JSONL cannot run in GitHub Actions. P3 because the CI half of the detector already fires on its own.
