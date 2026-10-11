---
type: is
id: is-01m3tc39nt8ez2vbbaf7cy10ks
title: "Results filters: one set of facet filters, the same on the homepage and on all-results.html"
kind: feature
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-09-30T23:58:46.969Z
updated_at: 2026-10-01T04:50:47.162Z
closed_at: 2026-10-01T04:50:47.161Z
close_reason: "Done in 0cb7fabb2 on claude/overview-page-impl (jlevy/squares#255, pushed at d078a2020); checked in the built site at http://localhost:8000 on 2026-10-01. One filter bar from overview_sections.result_filters on both tables: significance, verification and confirmation floors, standing, source, case n, date from and to; filters compose; a row named by the address always shows."
resolution: null
duplicate_of: null
---
Owner, 2026-09-30: the filtering options should be the same on the main overview page and on the Results page, and it should be possible to filter by every facet: significance, verification, confirmation, standing, source (this project's or others'), and any other facet the rows carry (case, date range if the rows carry dates). One filter component, rendered from one Python helper and driven by overview/table.js, on both tables; defaults as the owner set them (significance S4 and up, think-ogc8); filters compose; the row popover (think-br9e) follows its row through filtering. Documented in paper-design.md.
