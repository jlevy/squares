---
type: is
id: is-01m0y083cqkdjbbzfjxc5j7wpd
title: Build recurring joined research-loop efficiency report
kind: feature
status: closed
priority: 1
version: 5
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-25-research-loop-efficiency-infrastructure.md
labels:
  - packing
  - focus-efficiency
  - performance
dependencies: []
parent_id: is-01m0r7q50gw0wepeaj1dzb7g3r
created_at: 2026-08-26T03:01:33.715Z
updated_at: 2026-09-16T00:21:14.935Z
closed_at: 2026-09-16T00:21:14.925Z
close_reason: |
  Superseded for the detector half by think-z121: packing/devtools/check_pr_wall.py now measures hosted CI wall on every pull request with a per-job queue/setup/work split, a 180 s budget, a 1.2x regression rule against a recorded median, and an explicit unmeasurable verdict, against declared budgets in packing/devtools/gate-budgets.yaml. The agent-time join this bead specified -- Codex task-tree rollups and Claude session costs in one W5 report -- is not delivered by that and is now tracked separately as think-c3rb under the same parent.
resolution: null
duplicate_of: null
---
Join recursive Codex rollups, local packing validation timings, recent GitHub CI timings, and declared soft budgets into one repeatable W5 report. Acceptance: versioned inputs identify revision, platform, selected surface, worker settings, task roots, samples, medians, dispersion, and prior-median delta; reports distinguish critical-path wall time from recursive agent-time and model stream bounds; compact reviewed summaries exclude raw prompts and private JSONL; the command supports post-session, post-gate-change, and scheduled samples and identifies a regression without turning hosted wall time into a brittle functional assertion.

## Notes

2026-08-26 report contract: join CodexEfficiencyRollup/v2, normalized command keys, recent GitHub queue/job/step timings, local validation JSON, and declared p50/p95 budgets. Run after >1h sessions, after >=10s surface changes, weekly for GitHub history, and before W5 closure. Open/renew W5 work for >=20% regression or hard-budget miss. Commit scrubbed aggregates only; local Codex JSONL cannot run in GitHub Actions.


2026-09-15 (think-z121): closing as superseded for the part that was the detector, and splitting the rest. A repeatable measurement of hosted CI wall with a regression trigger now exists and runs on every pull request: `packing/devtools/check_pr_wall.py` computes the run wall to the aggregator's start with a per-job queue, setup and work split, fails over a declared 180 s budget or 1.2x of a recorded median of at least fifteen runs, and emits GitHub warning annotations plus a step summary when a run cannot be judged rather than passing silently. With `packing/devtools/gate-budgets.yaml` holding the declared budgets and per-tier records, the hosted-CI, local-validation and soft-budget inputs of this bead's report contract are covered. What it does NOT deliver is the join this bead was actually about: Codex task-tree rollups (CodexEfficiencyRollup/v2) and Claude session costs joined with those timings into one W5 report separating critical-path wall from recursive agent-time and model stream bounds. No bead carried that residue, so it is now think-c3rb under the same parent (think-r1yl) at P3.
