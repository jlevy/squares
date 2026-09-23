---
type: is
id: is-01m35v87c8b5sdt54sst3hdqt3
title: Enforce the --push floor with a pre-push hook, at a cost nobody skips
kind: task
status: open
priority: 1
version: 1
spec_path: packing/campaign/agendas/agenda-042-efficiency-block-the-development-cycle.md
labels:
  - focus-efficiency
  - ci
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-23T00:39:34.023Z
updated_at: 2026-09-23T00:39:34.023Z
---
agenda-042 BC-376. AGENTS.md says to run packing-validate --push before any push; nothing enforces it (lefthook has only pre-commit). PR #221's red cycles were validated with --records instead of --push, and generated-record drift, lint/format/type and a real test failure together were 6 of 15 sampled red runs over the last 20 merged PRs (27.8% of 151 cycles red). The --edit tier, which --push contains, measured 181.1 s at 4 cpus on 2026-09-23 with basedpyright as its longest step, so the floor costs about three minutes before any reachable test runs. Question: can a lefthook pre-push run --push with a measured median under a declared ceiling on narrow diffs, and what does the type floor need (incremental cache, scoped selection) to get there?
