---
type: is
id: is-01m0vssrzcz3vxj08sc2bc97r4
title: Close final autonomous-session contract review gaps
kind: bug
status: in_progress
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex@spud10
labels:
  - packing
  - process
dependencies: []
parent_id: is-01m0vqkq3x91sg8avet1jgx9rm
hold: null
hold_until: null
created_at: 2026-08-25T06:30:23.978Z
updated_at: 2026-08-25T06:30:32.738Z
started_at: 2026-08-25T06:30:32.737Z
---
Final read-only checkpoint review found four concrete gaps before publication: the launch plan contradicted its upstream-PR blocker; an active session could remain in_progress after its absolute deadline and ordinary work could consume the finalization reserve; a new terminal delegation could bypass its receipt by omitting optional phase metadata; and an active session had to invent progress.after. Correct the clock/finalization model, contemporaneous delegation provenance and terminal receipt rules, active progress semantics, plan wording, focused regressions, and categorized defect records. Acceptance: historical artifacts remain valid; expired active session, reserve encroachment, receipt omission, placeholder progress, excess max_cycles, and unfrozen delegated uv commands are directly tested; focused and normal gates pass; PR #28 is updated.
