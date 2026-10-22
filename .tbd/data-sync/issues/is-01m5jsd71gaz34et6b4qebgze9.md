---
type: is
id: is-01m5jsd71gaz34et6b4qebgze9
title: Normalize empty math style attributes before publication
kind: bug
status: in_progress
priority: 1
version: 2
delegate: navigation-render-stability
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-22T21:48:51.631Z
updated_at: 2026-10-22T21:48:57.069Z
started_at: 2026-10-22T21:48:57.068Z
---
Pages deployment for merged PR735 failed repeated-render comparison solely because an empty style attribute appeared in a different order on a prepared inline math span. Normalize semantically empty styles at publication and retain meaningful output stability checks; include a focused regression test.
