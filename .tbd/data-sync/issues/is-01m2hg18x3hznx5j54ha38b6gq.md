---
type: is
id: is-01m2hg18x3hznx5j54ha38b6gq
title: "PR #160 review D46: a trial's configuration omits the pair law and timing"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:58:43.234Z
updated_at: 2026-09-15T02:58:53.883Z
closed_at: 2026-09-15T02:58:53.882Z
close_reason: "Fixed on PR #160 in 89250df8 (probe records pair law, wall law, beat and annealed span; AnnealingConfiguration/v2 required by admission, cohorts and replay groups), 4ae3a8ee (the probe gives Animate the page, without which no trial ran on the Pack-first page) and ab10fab8 (foundation fixture re-collected with v2 rows). think-doxp stays open."
resolution: null
duplicate_of: null
---
Canonical defect D46 from the 2026-09-14 stack triage. Source finding: #171 R6 (Medium), code item; the gap exists at #160 `72629c03`.

A trial's recorded configuration was style, mode, seed, inflate and anneal. #171 changes the pair law the benchmark simulates (0.15/2500/0/0 to 0.35/950/80/0.15) and the moving span (0.8 s to 0.9 s), so trials before and after at identical recorded configurations measure different physics and only the source commit separates them.

Files: `packages/workbench/probes/bench-annealing.ts:261-267`, `tools/workbench_tools/trial_records.py:404-405` and admission, `tests/test_benchmark_admission.py`. Coordinator decision (section 5): record the pair law and timing in every trial's configuration; leave think-doxp (whether Pack adopts the new law) open. H-211 and X-034 wording is D70 on #171.
