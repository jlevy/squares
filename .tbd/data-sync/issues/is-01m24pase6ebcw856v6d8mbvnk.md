---
type: is
id: is-01m24pase6ebcw856v6d8mbvnk
title: Play a strategy plan in the workbench
kind: task
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-09-packing-strategies-as-a-shared-language.md
labels: []
dependencies: []
created_at: 2026-09-10T03:38:38.915Z
updated_at: 2026-09-10T03:53:04.650Z
---
Phase 2. The workbench loads a plan document and its recorded trace, plays the stages in sequence with per-stage labels, and shows the container side against both the known record and the proved lower bound. A stage can be edited and re-run, and the edited plan exports back out as the same document the headless tools read.

This is what turns the workbench from a menu of fixed animation styles into a place a strategy is watched and edited. The hand-hunting argument in X-025 is the reason it matters: of the 36 non-grid cases below n=100, hand construction found 21 and annealing 10.

Depends on the schema and executor bead.
