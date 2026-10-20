---
type: is
id: is-01m59f4zkye3agw7a31k3a885t
title: "check_requests draft: distinguish unintegrated replay, inventoried claims, and actual posting agent"
kind: bug
status: open
priority: 2
version: 1
assignee: codex-stage7-20261018
delegate: codex-stage7-20261018
labels: []
dependencies: []
parent_id: is-01m4kraefdygkg3wkdwegf6vfw
created_at: 2026-10-19T06:56:26.238Z
updated_at: 2026-10-19T06:56:26.238Z
---
Deduplicated extension of existing think-ri84, found by Stage7 draft audit at main d167d4b86. --draft 668,669,674 says nothing has been read or replayed here yet for V0/C0, then correctly says separate complete source replay/controls await integration. --draft 666,670,672,675,678 says claims not yet mapped although their individual Stage1 inventories are retained. Every draft hardcodes Claude Code footer even when actual posting agent is Codex. Preserve actual register rungs, distinguish receipt integration from execution, describe inventory vs triage faithfully, and make attribution reflect actual poster. No tool edits in this posting task. Existing think-ri84 already owns general RECORDED wording; this child records new regression examples and two additional cases without altering its owner.
