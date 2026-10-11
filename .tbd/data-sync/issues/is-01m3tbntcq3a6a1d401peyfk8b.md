---
type: is
id: is-01m3tbntcq3a6a1d401peyfk8b
title: "Recent Results: the Significance filter defaults to S4 and up"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:51:25.334Z
updated_at: 2026-10-01T04:50:46.722Z
closed_at: 2026-10-01T04:50:46.721Z
close_reason: "Done in 0cb7fabb2 on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. SIGNIFICANCE_DEFAULT = 4 in the shared filter bar: 'S4 and up' is selected on the homepage and on all-results.html (15 of 61 rows show)."
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: the default filter should be S4 or higher. Today overview_sections selects the first option, S3 and up (think-kjd1, sandbox think-u022). Make S4 and up the selected default, keep S3 and up and All as choices, and update the page prose, the design doc and the tests that pin the default.
