---
type: is
id: is-01m338m3kdks21pzathyt75ksr
title: Decide whether a join between moving runs should blend instead of switching color in one frame
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m32t2yc3xenfb97kxn844rc7
created_at: 2026-09-22T00:35:31.564Z
updated_at: 2026-09-22T00:35:31.564Z
---
While a packing moves, each run of parallel squares that share a whole side carries one moving-palette color, and when two runs touch the smaller takes the larger's color at the next group checkpoint, in a single frame (assignGroups / foldGroups in packages/workbench/src/application.js). At the default drain level of 0 the moving palette is fully grey, so a join shows as a grey level snapping: measured with check_transitions --trace 51 --square 8, L 0.633 -> 0.760 in one frame at t 2.283.

The transition contract's lightness rule exempts the merge window explicitly (transition_contract.merge_window) rather than hiding it, because a join is designed as a discrete event: it is the moment the packing's structure changed, and the palette exists to say so. Whether it should instead cross over a few frames is a design choice for the owner, not a fault to fix quietly. If it should blend, remove the exemption and the contract will hold the new behavior.
