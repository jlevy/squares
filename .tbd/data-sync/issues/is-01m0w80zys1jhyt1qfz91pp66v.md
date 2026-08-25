---
type: is
id: is-01m0w80zys1jhyt1qfz91pp66v
title: Pair-meter probe used an incompatible basin-event fixture
kind: bug
status: closed
priority: 3
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex-root
labels: []
dependencies: []
parent_id: is-01m0pqg2mnmsmv8250d0rw25kb
created_at: 2026-08-25T10:39:00.568Z
updated_at: 2026-08-25T10:52:13.453Z
closed_at: 2026-08-25T10:52:13.453Z
close_reason: Fixed and regression-checked in pushed checkpoint a9330d6; the 99.08-second normal gate passes all 31 steps and 62 mutation controls.
resolution: null
duplicate_of: null
---
The first basin-entry JSONL meter probe selected exp-019, which has x/y evidence but no t array required by sqsearch read_config. The command failed before work. Re-run against a conforming retained sqsearch configuration and record the exact fixture.
