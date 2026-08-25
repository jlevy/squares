---
type: is
id: is-01m0vj2j85ewtxj3hwxqtqw6sb
title: "PR #23 review R5: Replace gate-running message matching with a typed error"
kind: bug
status: closed
priority: 2
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-24-packing-engineering-maturity.md
delegate: codex@spud10
labels:
  - engineering-maturity
  - pr-review
  - pr-23
dependencies: []
parent_id: is-01m0vj13yefxcxhhew81ewfpvq
hold: null
hold_until: null
created_at: 2026-08-25T04:15:23.396Z
updated_at: 2026-08-25T04:44:36.478Z
started_at: 2026-08-25T04:16:15.469Z
closed_at: 2026-08-25T04:44:36.477Z
close_reason: "Completed in 69e65eb: GateRunningError provides a typed campaign/gate refusal and preflight no longer classifies errors by message substring."
resolution: null
duplicate_of: null
---
PR 23 review R5. File: explorations/packing/src/sqpack/campaign/runner.py around line 975. Replace substring classification of RefusalError text with a GateRunningError subtype and a regression test.
