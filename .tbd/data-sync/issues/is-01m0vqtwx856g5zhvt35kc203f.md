---
type: is
id: is-01m0vqtwx856g5zhvt35kc203f
title: Bind autonomous sessions to one wall deadline and preserve renewed slices
kind: bug
status: in_progress
priority: 0
version: 2
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - process
dependencies: []
parent_id: is-01m0vqkq3x91sg8avet1jgx9rm
created_at: 2026-08-25T05:56:03.623Z
updated_at: 2026-08-25T05:56:11.604Z
---
AgentSession/v2 records per-phase clocks but no mechanically enforced session start/deadline, so repeated phases can reset an eight-hour ceiling. The checker also rejects adjacent phases with unchanged workflow and focus even when the bounded objective changes, contradicting the runbook's 30-minute renewal rule. Add a session clock bounded by wall_minutes/finalization reserve, cap contemporaneous cycles, permit same-workflow/focus renewal only for a changed objective, and add mutation controls. Acceptance: an over-deadline phase, missing active-session clock, excess cycle, and unchanged-objective renewal all fail; historical records remain valid.
