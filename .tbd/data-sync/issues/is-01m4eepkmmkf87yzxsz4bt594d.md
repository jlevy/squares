---
type: is
id: is-01m4eepkmmkf87yzxsz4bt594d
title: Keep mutation-control snapshots below the existing cap
kind: bug
status: in_progress
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4e2gm6ya1mxg40qmv53ysbn
hold: null
hold_until: null
created_at: 2026-10-08T19:09:05.555Z
updated_at: 2026-10-08T19:09:38.275Z
started_at: 2026-10-08T19:09:38.274Z
---
Merged parent and child negative-control snapshots exceed the fixed 192 MiB cap. Audit retained snapshot inputs and dependency closure with existing tools/fdu, exclude only unused generated research payloads with evidence, retain all required controls, and verify custody without raising the cap.
