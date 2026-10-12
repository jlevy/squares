---
type: is
id: is-01m4mth1gzbfvd0qzhfbexx891
title: "Give large narrow test selections a measured budget instead of the fixed 900 s cap (PR #496 review F3)"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
labels:
  - packing
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
created_at: 2026-10-11T06:31:12.650Z
updated_at: 2026-10-11T06:31:12.650Z
---
From PR #496 review F (https://github.com/jlevy/squares/pull/496#pullrequestreview-5481911429), finding F3, deferred here by the follow-up PR (think-jjs7).
packing/src/sqpack/cli/validate.py `_push_test_step`: `budget_seconds=FAST_SUITE_BUDGET_SECONDS if everything else None`, so any narrow selection, however large, runs under the shared 900 s behavioural cap, while the whole suite (742 files) gets 1,800 s. At aca9a0784 a change to `.github/workflows/pages.yml` alone selected 554 of 742 test files (every Pages-workflow input), each of the other eleven paths 111-137, and the ten-path snapshot that timed out at 900 s (1,275.28 s wall) selected 155. Pre-existing, not a regression.
Decide with a measurement: a narrow selection above some fraction of the suite takes the whole-suite budget, or the budget scales with the selected fraction. Keep the 900 s guard for small selections.
