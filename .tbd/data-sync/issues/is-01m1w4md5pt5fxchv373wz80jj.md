---
type: is
id: is-01m1w4md5pt5fxchv373wz80jj
title: "PR #100 review R11: logged violating count still uses the strict float comparison"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:24.214Z
updated_at: 2026-09-06T19:55:34.239Z
closed_at: 2026-09-06T19:55:34.239Z
close_reason: Fixed in b3176e67 on the PR branch.
resolution: null
duplicate_of: null
---
cutting.py screened_separation counted depth > floor while the site walk used the loosened screen, so the log could say violating=0 on an iteration that added cuts. Fixed in b3176e67.
