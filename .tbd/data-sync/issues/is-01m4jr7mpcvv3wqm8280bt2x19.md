---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 7
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T12:24:21.551Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR462 hosted findings without relaxing existing contracts: declare the reviewed Headroom, rating tooltip and homepage Atlas script families including hashed paper programs; correct two browser-helper type annotations and canonical popover fallback oracle; avoid synchronous Headroom startup layout on the combined Atlas/Frontier page while preserving restored-scroll behavior; remove redundant browser fixture setup so the frontend tier satisfies its existing165s wall limit. Retain unknown-script refusal,300ms longest-task and all browser assertions. Verify focused fixes, Astra review, and final hosted gates before closing; full pre-merge checkpoint remains think-xio5.

## Notes

Upstream main af17208c0 is integrated with scientific inputs and exports unchanged. Astra approved the merge, probe declaration, and final Atlas test repairs. The edit floor passed 64 checks, then the repaired probe-loader check passed separately. The first frontend run exposed 111 nested Playwright setup errors; one shared browser owner resolved them. A serial Atlas run passed 112 checks and exposed five stale fixture/contracts: missing initial SVG assets, strict 100-case motion bounds, and Global normalization across a complete 102-case Grid preview. All five regressions now pass across focused reruns; final two passed in 60.66s. Source lint, types and 500-probe inventory are clean. No production geometry changes or budget relaxation were needed. Final combined frontend gate is running; commit, push and exact-head hosted gates remain. Full pre-merge checkpoint stays in think-xio5.
