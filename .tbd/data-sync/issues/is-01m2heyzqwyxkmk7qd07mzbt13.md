---
type: is
id: is-01m2heyzqwyxkmk7qd07mzbt13
title: "PR #160 review D82: generated beat totals omit correct and use stale timings"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:59.739Z
updated_at: 2026-09-15T02:40:58.788Z
closed_at: 2026-09-15T02:40:58.787Z
close_reason: "Fixed on #160 at 6a316042: the summary sums all four spans at TIMING and the page's static beat; a test compares STATIC_TIMING and TIMING with application.js CONTINUOUS. stats-summary.md is frozen historical output and not regenerated."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Generated beat totals omitted `correct` and used stale static-append timings, so `stats-summary.md` printed 695.3 / 489.0 / 538.5 s against the page's 568.95 s. `AtlasTiming.correct` was fixed at f9099096.

Source: #125 F32 (totals item).

Files: `packages/workbench/tools/workbench_tools/build_candidate.py:1618` (@bb3f7c99); `spikes/v2-transitions/stats-summary.md:85-87`.
