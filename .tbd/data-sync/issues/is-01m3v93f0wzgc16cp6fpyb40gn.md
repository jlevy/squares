---
type: is
id: is-01m3v93f0wzgc16cp6fpyb40gn
title: "Results page: no lineage group headings; the credit column says it"
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T08:25:41.145Z
updated_at: 2026-10-01T10:50:11.718Z
closed_at: 2026-10-01T10:50:11.717Z
close_reason: "e3b64b787, merged into claude/site-polish-3: all-results.html is one flat list, newest first; both tables come from one function, table_of_results; the Source filter stays; the lineage is read from each row's credit."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: on the full results page we don't need the divisions 'This project's results', 'Building on this project', 'Crediting this project second-hand', 'Independent of this project'; we should just make sure the credits clearly reflect these facts. Remove the group rows from all-results.html (and the code that hides or shows them under filters and sorting); the Source filter stays; the lineage is read from each row's credit (think the credit bead).
