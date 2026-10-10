---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T13:30:14.812Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR462 hosted findings without relaxing existing contracts: declare the reviewed Headroom, rating tooltip and homepage Atlas script families including hashed paper programs; correct two browser-helper type annotations and canonical popover fallback oracle; avoid synchronous Headroom startup layout on the combined Atlas/Frontier page while preserving restored-scroll behavior; remove redundant browser fixture setup so the frontend tier satisfies its existing165s wall limit. Retain unknown-script refusal,300ms longest-task and all browser assertions. Verify focused fixes, Astra review, and final hosted gates before closing; full pre-merge checkpoint remains think-xio5.

## Notes

Draft PR 462 now includes code 0b165d7ec and reconciled plan c812e4ee7. Hosted c812: all behavioral shards and nonfrontend validation jobs passed; frontend passed 403 tests with 6 skips and met the unchanged hard wall (319.83s <330s), with one explicit resize-readiness race remaining. That exact test now passes with a fresh-capacity/stable-frame probe; no column/focus assertions changed. Repeated paper startup failures were causally traced to Headroom’s inherited root offset: same-content control reduced four tasks from 236–245ms to173–183ms and restyle from25,865 elements/59.1ms to24 elements/0.5ms. Direct non-inherited root scroll padding preserves initial0px and measured height+8px; old-write regression fails at9,068 restyled elements on startup and resize, corrected500-MathML-root case passes. Both papers now pass all four unchanged300ms scenarios: optimality180/180/188/184ms, threshold127/127/133/138ms. Astra approved five-file final fix; lint/types/probe provenance clean. Combined frontend rerun active before commit/push and final-head hosted checks. Full pre-merge checkpoint remains think-xio5.
