---
type: is
id: is-01m5pdb3nsxtetytme2gpssxak
title: "Record #763's 13 L-border rows at or below 1024 once the D2 construction checker (W7) exists: 365, 444, 487, 632, 733, 734, 737, 788, 789, 845, 910, 966, 970"
kind: task
status: closed
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-24T07:34:57.465Z
updated_at: 2026-11-17T01:34:55.302Z
closed_at: 2026-11-17T01:34:55.302Z
close_reason: "Done on main: #800 (merged 2026-10-25, 4089f9587) recorded all 13 of #763's L-border recipes at 365, 444, 487, 632, 733, 734, 737, 788, 789, 845, 910, 966, 970 as rows of source couzo-issue763-2026-10-23-recipes, decided by devtools.construction_checker (its sibling think-g2qy closed with that merge). Found open by the 2026-11-17 sweep (coord-intake-1117)."
resolution: null
duplicate_of: null
---
Couzo's #763 (franciscouzo/square-packing@964ee2b) claims 14 L-border constructions at 325 to 1024; 909 restates #769's f1ceee4 row (think-fwa9), and the other 13 are recorded by the #763 walk (campaign/issue-intake/upper-bounds-issue763-20261024) and held back from a row (beyond_horizon_replay.WALKS[ISSUE_763].held, RECIPE). The owner's D2 answer (think-f2io, 23 October) makes a recipe-only row a row once a checker this project maintains decides it exactly; no such checker exists yet, so this is a W7 slice. Each recipe is certified_bounds.json's 'square tiling and L-border' construction, tiles_per_side 1, of k layers on a retained certificate of the couzo-issue763-2026-10-23 packet (receipts/index-claims.json names each source count). When the checker lands: decide the 13 from the packet, declare them, write their rows and supersessions, and drop the hold. Created by c-import-763-1024 (PR A, think-ptkk).
