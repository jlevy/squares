---
type: is
id: is-01m3yrqjwzmyheqrc7wecfhrxq
title: "Results tables: columns run Date, Result, N, Credit, Rungs, ID on the Overview's Recent Results and the Results page"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T16:56:32.407Z
updated_at: 2026-10-02T22:41:19.582Z
closed_at: 2026-10-02T22:41:19.576Z
close_reason: "Merged in jlevy/squares#310 (1e2e16fbb): the tables of results run Date, Result, n, Credit, Rungs, Status, Details, ID."
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'Another change in the main results table, both on the overview page and in the results page: let's make the result the first column. let's reorder columsn to be date, result, n, credit, rungs, id'. Both result tables (the Overview's Recent Results and all-results.html) take the column order Date, Result, N, Credit, Rungs, ID, from today's ID, N, Result, Credit, Rungs, Date. The explicit list puts Date before Result; it is followed as written. Sorting, filters, the row popover's trigger, narrow-screen layout and column widths follow the columns; tests and paper-design.md that pin the order are updated.

## Notes

2026-10-02: committed 1e2e16fbb on claude/amazing-bohr-ytjim9 (restarted from main cf1810034 after jlevy/squares#306 merged). Header and cells reordered to Date, Result, n, Credit, Rungs, ID; the phone card unchanged (date ordered after the credit). Tests (overview, column geometry) and paper-design.md updated; test_overview + test_site_result_columns + test_site_math_faces 332 passed. Rides one PR with think-ybt5 and think-tgjv. PR jlevy/squares#310 opened 2026-10-02 (head 38346bf4a); close when it merges.
