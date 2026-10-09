---
type: is
id: is-01m4fwn6tja8wxgg19b5gdw28e
title: "Fold research stack #461 -> #454 -> #404, qualify once, land on main"
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@vm
labels:
  - n-17
dependencies: []
parent_id: is-01m4fhz39j0nmrca9x38tyrnsg
hold: null
hold_until: null
created_at: 2026-10-09T08:32:14.162Z
updated_at: 2026-10-09T08:48:52.689Z
started_at: 2026-10-09T08:32:20.183Z
---
Consolidate formal stack 455 into #404 by merging #461 into #454's branch and #454 into #404's branch, so one Packing run plus one full checkpoint qualifies the whole stack. Measured: folded tree with #404 repair 1af586ef = 200,420,648 bytes (905,944 under the 192 MiB cap); trial merge is conflict-free. Prerequisites: independent review of repair 1af586ef and of the fold delta. Preserve exp315/316 bytes, all proof-scope flags, the cap and all ceilings. Supersedes the propagation plan in think-0m0x.

## Notes

2026-10-09T08:48Z User chose the fold/consolidated landing. #461 is in a formal GitHub stack, so plain gh pr merge is refused; land with gh stack merge 461 --merge (atomic bottom-to-top). Propagated 1af586ef by merge commits: #454 9857dd277, #461 09e9bbaf3 (200,420,648 bytes). Deep gate dispatched on #461 branch: run 37907206428. Review H requested on #404.
