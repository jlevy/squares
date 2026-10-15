---
type: is
id: is-01m4zvtaxg3pdrgy1e19rea8b5
title: Stabilize direct and fetched case-summary drawing width in browser checks
kind: bug
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T13:25:24.527Z
updated_at: 2026-10-15T18:55:27.090Z
started_at: 2026-10-15T13:25:55.918Z
closed_at: 2026-10-15T18:55:27.090Z
close_reason: "Source delivery completed in PR620: reviewed head 32ffac9dd8d8756ec619e808d0d3034b58640e6d merged as 4c9af6902e517bfff7d9f50d7cd6a042a15f60ed. Exact-head ordinary Packing 38787870695 and Pages 38787870830 passed; actual JUnit confirms all 46 targeted policy/selection controls passed without skips. Final reviews O5538212826, P5538213019 and Q5538223370 have no open findings and carry unchanged earlier M/N coverage. The historical full43 aggregate remains failed on CALL timing, while its actual 241 slow-lane nodes including all five moved operations passed. Hosted policy now explicitly reports at12s and enforces45s; strict/local/enforce remain12s, and mathematical/functional/child-deadline guards remain. The bounded retrospective, safety removal, supervision, invocation-local input sharing, measured-node placement, native ownership and selection fixes are delivered; no controlled speedup or three-minute success is claimed. Post-merge publication and complete native main coverage remain OPEN and owned in think-bmix; broader measured CI program remains open in think-kxmq/think-jpto/think-h96x. Evidence retained in primary .codex/regularization-closeout-evidence-2026-10-13/."
resolution: null
duplicate_of: null
---
PR620 frontend job116443646383 on head82b81649 failed test_case_summaries_keep_math_and_layout_when_fetched[light-1280]: fetched drawing width320 versus direct288, 1 failed/424 passed/6 skipped in299.37s. Investigate the real layout/readiness path and preserve the comparison assertion; fix the actual CSS/measurement race rather than loosen the tolerance or retry blindly. Source baseline includes prior reader delivery; no browser code changed in F1. Group this repair before the next hosted push and keep local work within the external scratch limit.

## Notes

Fixed only existing test setup in cf9003e0: capture desktop drawing width, exercise the 35rem boundary, restore viewport, and assert restoration before measuring direct content. Original fetched/direct equality and tolerance are unchanged. CI red was 288px versus 320px, matching narrow 18rem and desktop 20rem styles. Local exact parameter against the retained v0.7.5 preview passed before (4.18s) and after (3.43s); no local reproduction or new-build claim. Ruff/format passed. Final hosted source and browser confirmation remain required. Evidence: case-layout-nnti-before-configured and case-layout-nnti-after logs/JUnit, plus pr620-frontend-job.log.
