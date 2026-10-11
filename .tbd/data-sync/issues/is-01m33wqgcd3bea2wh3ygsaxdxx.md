---
type: is
id: is-01m33wqgcd3bea2wh3ygsaxdxx
title: The stage labels 128 upper bounds PROVEN that the register has not certified
kind: bug
status: closed
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-07-known-best-atlas-video.md
labels: []
dependencies: []
parent_id: is-01m33vv4hs6kbe1c349y8wsgsf
created_at: 2026-09-22T06:26:54.477Z
updated_at: 2026-10-06T08:31:42.956Z
closed_at: 2026-10-06T08:31:42.956Z
close_reason: |
  Done (bead review 2026-10-06, origin/main eb43ffe9a): Owner's 2026-09-22 decision implemented in a4bdfae4c: uncertified upper bounds marked 'reported' in bound-citations.json and the stage (packages/workbench/src/view/facts.ts:300 cites think-n56i); certifying them is think-2716
resolution: null
duplicate_of: null
---
Found by the citation survey (2026-09-21): in 128 n the stage prints under PROVEN an upper bound that packing/frontier has not certified -- verified_upper_bound is weaker there (122 carry a mathematics blocker; 68, 69, 103, 105, 110, 131 carry source-evidence blockers). Among them 17, 28, 37, 39, 41, 50, 51, 53-55, 68-71, 83, 87, 88, 101-110, 122-132, 145-156, 170-182, 197-210, 226-241, 257-273, 290-307. The case schema says so (square-packing-case.schema.yaml:123-134); the panel's comment at packages/workbench/src/view/facts.ts:200-203 assumes a construction proves its own upper bound. Decide what the panel should say for a reported but uncertified upper bound, and make the stage and the citation line agree with the register.

## Notes

Decided by the owner (2026-09-22): keep these bounds in the stage's bounds line, and mark them reported in the citation line; only certified bounds are presented as proven. Converting reported to verified is the queued epic think-2716.
