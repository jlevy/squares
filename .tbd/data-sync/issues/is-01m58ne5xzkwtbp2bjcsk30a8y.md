---
type: is
id: is-01m58ne5xzkwtbp2bjcsk30a8y
title: "PR #403 J1: diagnose hosted call-wall refusals"
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-18T23:27:04.638Z
updated_at: 2026-10-18T23:27:33.097Z
started_at: 2026-10-18T23:27:33.094Z
---
PR #403 Review J, J1, at head `3ee60c3e5157a82c0e9b5a48e54fc6c1f57539f5` remains a merge
blocker.
[Full run 38375099262](https://github.com/jlevy/squares/actions/runs/38375099262)
failed: eleven separate prerequisites passed, but four behavioral shards rejected
fifteen completed calls at 12.05–21.55 seconds against the unchanged twelve-second call
wall. Core validation took 2,827.84 of 3,600 allowed seconds.
The pinned validator checks this wall after the command returns; it is not a
twelve-second subprocess timeout.
No source defect or shared-host cause is established.

Recover the per-shard command, JUnit and timing evidence from the retained full-run
artifact and reproduce the affected exact node roster, ordering, guard and four-CPU
allocation with one validator on the host.
Profile repeated custody checks and browser navigation separately if the excess recurs.
Preserve the negative receipts and limits; do not accept a serial or subset pass as the
final gate. After formal stack #447 is integrated with current main under `think-6vrv`,
obtain a terminal full checkpoint at the resulting exact head.
`think-w0if` owns distinct local subprocess timeout evidence.
