---
type: is
id: is-01m0pdhx0dbsk8x90r58ge6pbx
title: Add regression checks for the six fixes that left none
kind: task
status: closed
priority: 1
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pdh5bj67ca8vk7ct53g5qt
created_at: 2026-08-23T04:20:10.892Z
updated_at: 2026-08-23T04:42:04.068Z
closed_at: 2026-08-23T04:42:04.067Z
close_reason: tools/regression_test.py covers D-002/D-015/D-016/D-019; ledger sweep-instance check covers D-010/D-017 with a known_defects declaration for annotated history. D-007 has no practical check and says so.
---
defects.md's 'Fixed, but nothing stops it coming back' list: D-002 inert budget cap, D-007 unsynced beads, D-010/D-017 sweep recorded as one round (already recurred once), D-015 path-dependent objective, D-016 conflated probe and step. Add a check for each where one is cheap, and record honestly where none is practical.
