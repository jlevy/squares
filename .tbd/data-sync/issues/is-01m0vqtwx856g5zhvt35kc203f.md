---
type: is
id: is-01m0vqtwx856g5zhvt35kc203f
title: Bind autonomous sessions to one wall deadline and preserve renewed slices
kind: bug
status: closed
priority: 0
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - packing
  - process
dependencies: []
parent_id: is-01m0vqkq3x91sg8avet1jgx9rm
created_at: 2026-08-25T05:56:03.623Z
updated_at: 2026-08-25T07:04:34.256Z
closed_at: 2026-08-25T07:04:34.256Z
close_reason: "Published in PR #28 at 1ebc13b: W7 and the frozen mixed portfolio are documented; session, phase, finalization, and delegation clock/receipt guards are executable; D-240 through D-248 are synchronized; ordinary validation passed 31/31 locally in 103.91s with 51 pytest contracts and 62 mutation controls; focused session contracts passed 20/20; Linux validate and macOS portability CI both passed. No research run started, and think-3cbq remains blocked on think-jqkv and the unreconciled launch prerequisites."
resolution: null
duplicate_of: null
---
AgentSession/v2 records per-phase clocks but no mechanically enforced session start/deadline, so repeated phases can reset an eight-hour ceiling. The checker also rejects adjacent phases with unchanged workflow and focus even when the bounded objective changes, contradicting the runbook's 30-minute renewal rule. Add a session clock bounded by wall_minutes/finalization reserve, cap contemporaneous cycles, permit same-workflow/focus renewal only for a changed objective, and add mutation controls. Acceptance: an over-deadline phase, missing active-session clock, excess cycle, and unchanged-objective renewal all fail; historical records remain valid.
