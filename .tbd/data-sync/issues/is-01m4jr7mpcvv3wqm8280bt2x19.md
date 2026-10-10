---
type: is
id: is-01m4jr7mpcvv3wqm8280bt2x19
title: Keep website publication and frontend validation within their contracts
kind: bug
status: in_progress
priority: 1
version: 15
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels:
  - website
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T11:12:38.602Z
updated_at: 2026-10-10T16:30:39.844Z
started_at: 2026-10-10T11:13:19.000Z
---
Resolve PR 462 publication and frontend findings without relaxing existing contracts. Preserve script inventory refusal, native MathML readiness, stable Atlas geometry, 300 ms startup assertions, all browser checks and current effective PR hard ceiling. Retained fixes cover non-inherited Headroom clearance, concurrent browser-lane startup, canonical render setup and Atlas host reuse. Final hosted gates must pass before closure; full pre-merge checkpoint remains think-xio5.

## Notes

Published f489084511a56b130e6d86fc46a8260f4fb530bb / draft PR462: all407 functional browser tests pass,6skip; HTTP desktop initial native tasks303/302ms exceed300ms, two mobile scenarios pass; overall413.44s exceeds effective330s PR ceiling. Other29 checks pass including publication and strict papers. Removed Atlas startup flushes and reduced-motion correction remain verified. Native MathML wrapper controls are rejected: baseline desktop medians160/159ms, max-width-only161/160, inline-plus-width167/159 with overlapping ranges. All72 timing contexts pass readability/CLS/budgets; width-only geometry and font controls match exactly. CSS restored byte-for-byte; raw generated ledger retained in task visualization native-wrapper-controls. Test-probe memoization passes exact52-field equality on direct/fetched53, reducing style reads17000 to1174 and93684 to8114; nested clipping/order/boundary regression1PASS1.28s. Matched pair33.63 to32.31s total,4.86 to4.14s calls: modest single-pair evidence, not a hosted guarantee. Astra and scoped Ruff/Biome/types/ESLint/BasedPyright approve three files, not yet committed. Frozen full-frontend allocation control now measures site3 versus4 workers at declared4CPU/outer2/inner1, Workbench2 unchanged, identical408functional nodes plus4HTTP and56floor checks. Require at least15percent wall gain and exact selection equality before considering retention; any eventual change must preserve other local topology behavior. No budgets/assertions/content are relaxed. Full checkpoint remains think-xio5; implementation closeouts held until exact-final-head hosted checks pass.
