---
type: is
id: is-01m5jsd71gaz34et6b4qebgze9
title: Normalize empty math style attributes before publication
kind: bug
status: closed
priority: 1
version: 3
delegate: navigation-render-stability
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-22T21:48:51.631Z
updated_at: 2026-10-22T21:55:33.870Z
started_at: 2026-10-22T21:48:57.068Z
closed_at: 2026-10-22T21:55:33.865Z
close_reason: "Fixed in a65366fba: remove semantically empty styles from cloned prepared math hosts. Regression failed before and passes after; 19 tests passed and two concurrent complete renders agree under recursive diff."
resolution: null
duplicate_of: null
---
Pages deployment for merged PR735 failed repeated-render comparison solely because an empty style attribute appeared in a different order on a prepared inline math span. Normalize semantically empty styles at publication and retain meaningful output stability checks; include a focused regression test.
