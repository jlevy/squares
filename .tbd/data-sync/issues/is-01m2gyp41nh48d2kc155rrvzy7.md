---
type: is
id: is-01m2gyp41nh48d2kc155rrvzy7
title: Today's approaches written as strategy documents, with guidance declared
kind: feature
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels: []
dependencies:
  - type: blocks
    target: is-01m2gxkvbndg46r6pjy3352cb8
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-14T21:55:32.013Z
updated_at: 2026-09-14T21:55:50.980Z
---
Write today's approaches as PackingStrategy documents, so the evaluation loop has a real first field and every result the campaign has quoted maps to a document:

- `blind-bodies`: previous record, coarse-grid drop, matched blocks welded, shake at a stated level, walls closing onto the record side with overlap tolerance 0.08, then resolve. This is what the 2026-09-12 benchmark measured.
- `blind-physics`: the same with one body per square.
- `free`: target springs toward the record, no snap (guided).
- `snap`: `guide` onto the record (illustration and control only, never ranked).
- `projection-cold`, `assemble-then-tighten` (exists) and `ratchet` from the projection lane.
- The structure-ladder rungs from `sweep_structure_hints.py`, each with its rewired and thinned controls.

Each names its catalogue entry and declares its guidance. Acceptance: every document validates against the extended schema, runs on at least one declared implementation, and refuses cleanly on the others.
