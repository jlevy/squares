---
type: is
id: is-01m1w4m5my3wy6ax5qkdz3px0b
title: "PR #100 review R7: two new ceiling tests pass unchanged on main"
kind: bug
status: closed
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m1w4krded865yyd393yn5my5
created_at: 2026-09-06T19:55:16.510Z
updated_at: 2026-09-06T19:55:32.508Z
closed_at: 2026-09-06T19:55:32.508Z
close_reason: Fixed in 956cc6d9 on the PR branch.
resolution: null
duplicate_of: null
---
test_a_large_family_uses_exact_sums_even_at_small_coordinates and the decided-count assertion in test_the_maximum_depth_is_taken_at_an_arrangement_vertex were vacuous; now pin the 4096/4097 guard edge and decided == 4. Fixed in 956cc6d9.
