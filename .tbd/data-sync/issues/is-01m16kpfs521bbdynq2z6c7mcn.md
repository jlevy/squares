---
type: is
id: is-01m16kpfs521bbdynq2z6c7mcn
title: Phase 1 of the exact simplex, so a cell needs no float starting vertex
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
created_at: 2026-08-29T11:15:23.556Z
updated_at: 2026-08-29T11:15:23.556Z
---
agenda-006 BC-071, following BC-061. The exact LP certifies a vertex but does not find its first feasible one: the float path supplies the starting basis, which is the standard division for exact LP and is why D-021's floor still governs where the search begins. That is exactly the case that matters at n = 29, where no float solver produces a feasible vertex to start from. Build a Big-M or two-phase auxiliary program over the same exact scalars, reusing solve_square_system and the existing pivot loop, with its own negative controls.
