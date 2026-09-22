---
type: is
id: is-01m33wqgcd3bea2wh3ygsaxdxx
title: The stage labels 128 upper bounds PROVEN that the register has not certified
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels: []
dependencies: []
parent_id: is-01m33vv4hs6kbe1c349y8wsgsf
created_at: 2026-09-22T06:26:54.477Z
updated_at: 2026-09-22T16:54:20.179Z
---
Found by the citation survey (2026-09-21): in 128 n the stage prints under PROVEN an upper bound that packing/frontier has not certified -- verified_upper_bound is weaker there (122 carry a mathematics blocker; 68, 69, 103, 105, 110, 131 carry source-evidence blockers). Among them 17, 28, 37, 39, 41, 50, 51, 53-55, 68-71, 83, 87, 88, 101-110, 122-132, 145-156, 170-182, 197-210, 226-241, 257-273, 290-307. The case schema says so (square-packing-case.schema.yaml:123-134); the panel's comment at packages/workbench/src/view/facts.ts:200-203 assumes a construction proves its own upper bound. Decide what the panel should say for a reported but uncertified upper bound, and make the stage and the citation line agree with the register.

## Notes

Decided by the owner (2026-09-22): keep these bounds in the stage's bounds line, and mark them reported in the citation line; only certified bounds are presented as proven. Converting reported to verified is the queued epic think-2716.
