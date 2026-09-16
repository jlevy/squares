---
type: is
id: is-01m2m59rqzb3m4qjs4h3qca405
title: "PR #183 review R1: always-run Pages jobs escape budget coverage"
kind: bug
status: closed
priority: 1
version: 3
refs:
  - kind: pr
    url: https://github.com/jlevy/squares/pull/183
    at: 2026-09-16T03:50:02.099Z
labels: []
dependencies: []
parent_id: is-01m2kanffw38jyd10dxqqh8831
created_at: 2026-09-16T03:48:50.557Z
updated_at: 2026-09-16T03:50:02.100Z
closed_at: 2026-09-16T03:48:54.568Z
close_reason: "Fixed in 5fc2a0be. Event reachability respects always(), pages-required has a measured budget, and the Pages wall baseline now uses two final-shape observations. Focused contracts: 47 passed."
resolution: null
duplicate_of: null
---
Formal review finding for PR #183. pull_request_jobs propagated dispatch-only exclusion through needs without honoring if: always(), hiding pages-required from the every-PR-job budget contract even though the job ran on hosted PRs.
