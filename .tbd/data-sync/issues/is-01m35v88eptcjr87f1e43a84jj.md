---
type: is
id: is-01m35v88eptcjr87f1e43a84jj
title: Measure a pull request's cycle cost with a tool, not PR prose
kind: task
status: open
priority: 2
version: 1
spec_path: packing/campaign/agendas/agenda-042-efficiency-block-the-development-cycle.md
labels:
  - focus-efficiency
  - ci
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-23T00:39:35.126Z
updated_at: 2026-09-23T00:39:35.126Z
---
agenda-042 BC-378. Three OR-1 tool gaps found by the 2026-09-23 lanes: (1) no devtool rolls up red versus green runner-minutes and wall across a PR sample (lane B estimated ~443 of ~1,595 runner-minutes red over 20 PRs, inferred from per-job averages); (2) no devtool tracks queue time across runs, though two outlier walls (runs 35777665010 at 227 s, 35780496732 at 282 s) were queue-driven; (3) review-lane minutes are recorded in 1 of 20 PR bodies and in no structured field, so review time cannot be ranked. PR #221's self-reported cycle count also did not reconcile with the Actions API. Extend check_pr_wall / the branch-cost rollup so a PR's cycles, red share, queue time and lane minutes are read, not narrated.
