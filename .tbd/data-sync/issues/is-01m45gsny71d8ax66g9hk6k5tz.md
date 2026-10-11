---
type: is
id: is-01m45gsny71d8ax66g9hk6k5tz
title: "Frontend tier: cut the site-table settle cost under the 150 s ceiling and re-take its record"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-05T07:52:33.478Z
updated_at: 2026-10-05T07:52:33.478Z
---
The frontend tier misses its 150 s ceiling on slow hosted runners (151-163 s on PR #359 and #362, every test green). Since Oct 4 the wall is the lane running browser floor + liveness + site table layout serially; the table step grew from 24 s (Oct 2) to 44-67 s (Oct 5, 98 tests) through main's site-table commits be33790fe, 577ccf2cd, 9897ae38c, 0788c67c8, ec7cb6fa4. Locally test_site_result_columns.py's module fixture spends ~98 s in setup, ~76 s of it in four settle_math calls (~19 s each, ~1,100 formulas typeset progressively). Options: (A) settle each page once and reach the as-opened and short-lists states without reloading (drops two settles); (B) a test-mode hook that typesets all math at once; (C) a third lane, which needs hosted measurements first. Do not raise the ceiling (OR-17). Re-take the tier record (104.74 s) with an attribution block. Also: suite-a reads 132 s against a 131 s ceiling on slow runners because site_renders.pages() (~25 s) is memoized per xdist worker and paid twice when test_repo_links and test_site_documents land on different workers under --dist=loadfile; a shared on-disk render or co-locating those modules would remove the duplicate.
