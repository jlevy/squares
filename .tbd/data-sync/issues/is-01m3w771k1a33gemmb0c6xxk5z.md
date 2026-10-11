---
type: is
id: is-01m3w771k1a33gemmb0c6xxk5z
title: Homepage Recent Results shows the same record links as the full results table; no lateral link to the same table
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T17:11:55.743Z
updated_at: 2026-10-01T19:05:17.859Z
closed_at: 2026-10-01T19:05:17.854Z
close_reason: "c24cbb378 on claude/site-polish-4-columns, merged into jlevy/squares#276 (976c4f8bb): both tables are one table under two filters; the records line shows on both; the two lateral links (the summary's leading formula, the popover's 'Open in the results table' button) are removed; a test asserts every row is identical on the two pages apart from its key and hidden."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'on the new results table it is not showing the detailed links to the github records and pages that appear on the full results table. Let's align these and make them be the same. There's no point in linking from the new results table laterally over to the full results table with no benefit when they're the same table. They're just different filters.' The homepage table hides the records line (.kpress .site-recent-table .site-records) and its rows link across to all-results.html; both tables are one function with different filter defaults, so both show the records line and the same links, and the lateral row links go (one 'See all results' link under the table may stay as navigation).
