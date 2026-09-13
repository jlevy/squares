---
type: is
id: is-01m2e4b5m0xrgxkzqcrxmbb5q0
title: Wire BC329 run sheet to the maintained run-set verifier
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m2b884n0ms50xp93q6aaps1g
child_order_hints:
  - is-01m2e52mry1qw2v6vkskf1yha7
hold: null
hold_until: null
created_at: 2026-09-13T19:36:41.343Z
updated_at: 2026-09-13T19:58:58.678Z
started_at: 2026-09-13T19:43:01.453Z
closed_at: 2026-09-13T19:58:58.678Z
close_reason: PR156 commit 9c56e901 retains the maintained five-step verifier run sheet, direct evidence-commit parent checks, refusal and acceptance reports, and the exact formatted sheet blob 29517a3f accepted by independent Sol high rereview. Records and edit tiers pass. Operational integrated-head review, remote equality, positive profiles, and evidence admission remain under think-pp3j.
resolution: null
duplicate_of: null
---
Independent integrated-head review at PR156 source fbd915fc found the draft run sheet still invokes the reader directly and hand-copies evidence; it never calls the maintained verifier snapshot/read/join/retain/source-closure entry points. Wire the frozen target-free sheet to the accepted verifier blobs, preserve exact argv/status/proof copies, 22-file coordinator root and status inventory, source and candidate-index checks, and later evidence-commit OID check. Run Bash parse and synthetic operational controls, then independent rereview on one clean head. Do not execute positive calibration or BC329 until every gate accepts.

## Notes

Run-sheet wiring now calls all five maintained verifier steps with 22-file coordinator and 19-file review inventories. Independent rereview refused missing execution-parent check; child think-i0sv repaired it. Final exact-diff review ACCEPTED the formatted run-sheet blob 29517a3f with Bash parse and target-free direct-parent/refusal controls. The report and sheet await PR156 document commit and records/push/hosted gates. This closes only draft command wiring; operational execution admission and positive profiles remain under parent think-pp3j.
