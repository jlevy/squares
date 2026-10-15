---
type: is
id: is-01m4z6gf6mwfckwx2z5k0vhy7q
title: "render_announcement: count a held entry's per-count sides as rivals, and decide whether a regularizing entry's line takes the counts its regularization holds"
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-15T07:13:01.140Z
updated_at: 2026-10-15T07:13:01.140Z
---
From PR #614 review A, A6. T-174's claim prints no per-count side, so render_announcement cannot see that it is smaller than T-161 and T-162 at six counts; and T-181's line keeps 211 and 241, where T-182 regularizes it and holds the houses. The #614 announcement block was edited by hand. Waits on a design decision: whether held entries (select_houses.HELD) count as rivals, and whether a regularization's counts leave the regularized entry's line.
