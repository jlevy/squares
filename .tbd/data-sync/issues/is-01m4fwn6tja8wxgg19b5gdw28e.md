---
type: is
id: is-01m4fwn6tja8wxgg19b5gdw28e
title: "Fold research stack #461 -> #454 -> #404, qualify once, land on main"
kind: task
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - n-17
dependencies: []
parent_id: is-01m4fhz39j0nmrca9x38tyrnsg
hold: null
hold_until: null
created_at: 2026-10-09T08:32:14.162Z
updated_at: 2026-10-09T09:29:45.036Z
started_at: 2026-10-09T08:32:20.183Z
closed_at: 2026-10-09T09:29:45.036Z
close_reason: Stack 455 (#404/#454/#461) merged to main at 533dd42
resolution: null
duplicate_of: null
---
Consolidate formal stack 455 into #404 by merging #461 into #454's branch and #454 into #404's branch, so one Packing run plus one full checkpoint qualifies the whole stack. Measured: folded tree with #404 repair 1af586ef = 200,420,648 bytes (905,944 under the 192 MiB cap); trial merge is conflict-free. Prerequisites: independent review of repair 1af586ef and of the fold delta. Preserve exp315/316 bytes, all proof-scope flags, the cap and all ceilings. Supersedes the propagation plan in think-0m0x.

## Notes

2026-10-09T08:48Z User chose the fold/consolidated landing. #461 is in a formal GitHub stack, so plain gh pr merge is refused; land with gh stack merge 461 --merge (atomic bottom-to-top). Propagated 1af586ef by merge commits: #454 9857dd277, #461 09e9bbaf3 (200,420,648 bytes). Deep gate dispatched on #461 branch: run 37907206428. Review H requested on #404.



2026-10-09T09:01Z Review H https://github.com/jlevy/squares/pull/404#pullrequestreview-5467973247: repair 1af586ef correct, no blocking findings; integrated stack+main e0b02b3ab merges cleanly, 200,442,723 bytes; 129+1+7+18+49 focused tests pass; 174/174 negative controls fire; edit tier 64/64 pass. Non-blocking H1 (0.84 MiB headroom), H2 (untested linked-dir branch), H3 (no dated log entry) routed to the #464 prune commit (think-mg1o). User decision 2026-10-09: keep 192 MiB, traced prunes (resolves A1 resource question).



2026-10-09T09:29Z LANDED: gh stack merge 455 --merge merged #404, #454, #461 into main at 533dd42c6 (09:22 UTC). Gate: Packing/Pages/mergeability green on 9857dd277 and 09e9bbaf3; deep gate 37907206428 12/12 at 09e9bbaf3; Review H no blocking; main e0b02b3ab scheduled run green.
