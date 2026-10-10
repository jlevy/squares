---
type: is
id: is-01m0w8a4hqt1ktxgcvsbakmszq
title: Phase-count cap ends fast campaigns before their wall-clock goal
kind: bug
status: open
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0rkz14t04yjme92gnfncfv7
created_at: 2026-08-25T10:44:00.182Z
updated_at: 2026-10-10T22:48:54.334Z
---
Session-010 completed fourteen bounded work phases in about three hours and opened its fifteenth, exhausting max_cycles=15 long before the 07:51 finalization reserve. The ledger correctly rejects labelling an early checkpoint as finalization. Preserve the stop, checkpoint session-010, then design the continuation so a wall-clock campaign is not prematurely ended merely because slices finish quickly.

## Notes

Contained in pushed checkpoint a9330d6: session-010 preserves its declared max_cycles=15 instead of mislabelling an early checkpoint as finalization. The reusable policy remains open: successful short slices exhausted the cap around 03:40, more than four hours before the 07:51 reserve. Continue via an explicit successor session rather than weakening session-010.
