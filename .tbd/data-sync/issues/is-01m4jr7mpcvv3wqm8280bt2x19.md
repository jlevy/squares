---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T12:48:08.801Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR462 hosted findings without relaxing existing contracts: declare the reviewed Headroom, rating tooltip and homepage Atlas script families including hashed paper programs; correct two browser-helper type annotations and canonical popover fallback oracle; avoid synchronous Headroom startup layout on the combined Atlas/Frontier page while preserving restored-scroll behavior; remove redundant browser fixture setup so the frontend tier satisfies its existing165s wall limit. Retain unknown-script refusal,300ms longest-task and all browser assertions. Verify focused fixes, Astra review, and final hosted gates before closing; full pre-merge checkpoint remains think-xio5.

## Notes

Commit eb9d1271c is pushed to draft PR 462; local frontend passed four steps in 195.54s. Hosted first run: five stale expectations across shards A/C; focused fixes passed 5 tests in 59.60s and Astra approved. Certificate paper initially exceeded the unchanged 300ms startup limit; isolated attempt 2 passed the entire publication workflow on identical code, so no CSS or budget edit was made. Frontend passed 403 tests with 6 skips and failed one desktop star-clearance check, plus its 431.29s wall exceeded the inherited 330s hard cutoff. Web-only star placement now reserves half an em before its actual left edge; all-324 source geometry passed and Astra approved, focused browser verification pending. Header worker is reducing repeated Atlas fixture preparation and unnecessary waits, retaining all assertions; baseline pair passed in 81.48s. Final frontend, commit/push and exact-head hosted checks remain. Full pre-merge checkpoint remains think-xio5.
