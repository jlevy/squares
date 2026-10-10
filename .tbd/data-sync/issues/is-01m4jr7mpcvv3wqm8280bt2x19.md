---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 10
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T13:46:48.669Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR462 hosted findings without relaxing existing contracts: declare the reviewed Headroom, rating tooltip and homepage Atlas script families including hashed paper programs; correct two browser-helper type annotations and canonical popover fallback oracle; avoid synchronous Headroom startup layout on the combined Atlas/Frontier page while preserving restored-scroll behavior; remove redundant browser fixture setup so the frontend tier satisfies its existing165s wall limit. Retain unknown-script refusal,300ms longest-task and all browser assertions. Verify focused fixes, Astra review, and final hosted gates before closing; full pre-merge checkpoint remains think-xio5.

## Notes

PR 462 at f5effa3 passed every functional hosted check: 405 site tests with six skips, all four unchanged HTTP checks, both strict 300 ms paper reviews, all other Packing leaves, Certificate and branch mergeability. Frontend alone failed its unchanged hard wall: 337.19 seconds versus 330. The site step was delayed by source floor 44.36 seconds plus liveness 24.40 before its 268.42-second run. The existing start_early hint now starts both browser lanes in the same two slots; selected steps, subprocess limits and budgets remain unchanged. Astra approved this two-file adjustment. Full scheduler regressions and combined frontend verification are active. An HTTP fixture alternative showed only 75.07 to 73.59 seconds and was fully reverted as inconclusive. Earlier retained fixes include script inventory, native MathML readiness, half-em web-star clearance, canonical bounded graphics fixtures, stable-frame Atlas resize readiness, and non-inherited Headroom scroll padding. Scientific data and PDFs are unchanged. Final exact-head hosted CI is required before closing this bead; the full pre-merge checkpoint remains think-xio5.
