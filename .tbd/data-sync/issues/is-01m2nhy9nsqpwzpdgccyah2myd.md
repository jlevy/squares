---
type: is
id: is-01m2nhy9nsqpwzpdgccyah2myd
title: Overlap Pages browser setup with prepared-page production
kind: bug
status: open
priority: 1
version: 2
labels:
  - ci
  - validation
dependencies: []
parent_id: is-01m2m5zjmj7dsycs1x6yxwcwwt
created_at: 2026-09-16T16:49:00.600Z
updated_at: 2026-09-17T02:06:22.888Z
---
PR #188 exact-head Pages run 35123561787 measured 235 seconds against OR-14's 180-second wall. browser-geometry (webkit) was critical: 3 seconds queued, 95 setup, 40 work, after the serialized scope+prepare chain. Start browser setup after scope and overlap it with prepare, then wait through a reusable fail-closed artifact-readiness tool before download; require an exact-head wall at or below 180 seconds.

## Notes

2026-09-16 evidence audit at da2259fb: implementation done (all 7 browser jobs need only scope, install, then wait via wait_for_run_artifact and download by artifact id; pages.yml:429-443, 1013-1100; test_page_check_setup_overlaps_prepare_then_joins_its_exact_artifact; commits c302b330, 89e247a7). The exit criterion, an exact-head Pages wall at or below 180 s, is unmeasured: gate-budgets.yaml still records the PR 180 reading of 189 s. Keep open until the final-head hosted run is recorded.
