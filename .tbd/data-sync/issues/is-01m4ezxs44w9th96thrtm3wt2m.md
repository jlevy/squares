---
type: is
id: is-01m4ezxs44w9th96thrtm3wt2m
title: Assess sampling variance in the Frontier timing-budget regression
kind: task
status: open
priority: 2
version: 1
labels:
  - ci
  - website
dependencies: []
created_at: 2026-10-09T00:10:06.336Z
updated_at: 2026-10-09T00:10:06.336Z
---
A documentation-only PR produced a marginal failure in tests/test_site_rendering.py::test_native_frontier_passes_the_unchanged_http_load_and_nojs_budgets[390-light]: longestTaskMs 311.000 against the 300 ms limit. All structural, glyph and CLS checks passed; the preceding planning commit passed, and rerunning the failed jobs on the same final commit also passed. Evidence: https://github.com/jlevy/squares/actions/runs/37862086989 and PR https://github.com/jlevy/squares/pull/462.

The pytest path calls devtools.check_site_rendering.measure once per configuration, whereas the reusable CLI supports --runs 3 and median timing metrics (development.md documents this). Assess the retained longTasks, animationFrames and readabilitySamples to distinguish page work, checker overlap and runner variance. Choose and declare a repeat-load decision rule for timing metrics while retaining per-sample functional checks and the existing 300 ms budget. Do not raise the budget merely to hide this failure. The existing think-6erz wall-ceiling tracker does not cover this in-page PerformanceObserver metric. This is a separate CI follow-up; the requested website plan remains its eight scoped implementation/verification issues.
