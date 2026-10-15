---
type: is
id: is-01m4zvtaxg3pdrgy1e19rea8b5
title: Stabilize direct and fetched case-summary drawing width in browser checks
kind: bug
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: claude-code@spud10.local
labels:
  - pr-620
dependencies: []
parent_id: is-01m4wtv34pphy5w434wk13b85x
hold: null
hold_until: null
created_at: 2026-10-15T13:25:24.527Z
updated_at: 2026-10-15T13:38:43.174Z
started_at: 2026-10-15T13:25:55.918Z
---
PR620 frontend job116443646383 on head82b81649 failed test_case_summaries_keep_math_and_layout_when_fetched[light-1280]: fetched drawing width320 versus direct288, 1 failed/424 passed/6 skipped in299.37s. Investigate the real layout/readiness path and preserve the comparison assertion; fix the actual CSS/measurement race rather than loosen the tolerance or retry blindly. Source baseline includes prior reader delivery; no browser code changed in F1. Group this repair before the next hosted push and keep local work within the external scratch limit.

## Notes

Fixed only existing test setup in cf9003e0: capture desktop drawing width, exercise the 35rem boundary, restore viewport, and assert restoration before measuring direct content. Original fetched/direct equality and tolerance are unchanged. CI red was 288px versus 320px, matching narrow 18rem and desktop 20rem styles. Local exact parameter against the retained v0.7.5 preview passed before (4.18s) and after (3.43s); no local reproduction or new-build claim. Ruff/format passed. Final hosted source and browser confirmation remain required. Evidence: case-layout-nnti-before-configured and case-layout-nnti-after logs/JUnit, plus pr620-frontend-job.log.
