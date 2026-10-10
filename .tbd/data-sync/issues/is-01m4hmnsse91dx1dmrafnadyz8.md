---
type: is
id: is-01m4hmnsse91dx1dmrafnadyz8
title: Make nested endpoint refusal test independent of worker state
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h9s465x7mphy1xxkmdyqc9
hold: null
hold_until: null
created_at: 2026-10-10T00:51:13.830Z
updated_at: 2026-10-10T00:51:36.070Z
started_at: 2026-10-10T00:51:36.069Z
---
Final candidate whole-branch push passed all65edit checks and16419normal tests, including15hover cases; one n17 shared-centre CLI test failed because the nested submitted payload was correctly refused with fresh endpoint mathematical payload differs instead of expected packet nesting exceeds encoder depth. Reproduce and establish whether recursion state, order, input validation or refusal precedence causes the mismatch. Correct the established defect narrowly without accepting malformed input, weakening refusal assertions or hiding failures. Focused checks during repair; one final full qualification after changes are complete. Retain failed candidate receipt1394.71s and original metadata, then refresh exact candidate tree and hosted head. No GitHub merge authorized.
