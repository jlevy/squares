---
type: is
id: is-01m5bxvwndz2nktwat71bq8ces
title: "Census views: byte-compare committed views against fresh render; regenerate stale rectangle census view"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-10-20T05:52:05.805Z
updated_at: 2026-10-20T05:52:05.805Z
---
From Review C of #688 (C3, https://github.com/jlevy/squares/pull/688#issuecomment-6284378953). test_the_committed_census_views_carry_every_census_row checks row names and verified counts only; a rewritten n85 row still passes. packing/.../census/README.md (rectangle family) is stale on main in 9 rows (e.g. rect_n20_L49 reads 'none: first complete check here' where render_report gives 'complete | 3667 (4)'). Mixed view and summary already match render+pinned flowmark byte for byte. Fix: regenerate the rectangle view, then make the test compare each view with the rendered, flowmark-formatted output.
