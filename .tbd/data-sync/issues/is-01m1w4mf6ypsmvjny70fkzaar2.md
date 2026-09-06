---
type: is
id: is-01m1w4mf6ypsmvjny70fkzaar2
title: "PR #100 review R12: exact separation fallback is silent and 220x slower"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:26.301Z
updated_at: 2026-09-06T19:55:34.242Z
closed_at: 2026-09-06T19:55:34.242Z
close_reason: Fixed in b3176e67 on the PR branch.
resolution: null
duplicate_of: null
---
Crossing the floating envelope (e.g. --side 17) swaps the vectorized screen for exact enumeration with nothing in the log. cutting_plane_loop now writes one line. Fixed in b3176e67.
