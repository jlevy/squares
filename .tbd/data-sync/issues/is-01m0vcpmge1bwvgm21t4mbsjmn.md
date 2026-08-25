---
type: is
id: is-01m0vcpmge1bwvgm21t4mbsjmn
title: Correct stale normal-gate metrics in the synopsis
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
delegate: codex@spud10
labels:
  - packing
  - bookkeeping
dependencies: []
parent_id: is-01m0vbg75b3j30f9eq2j678b9j
hold: null
hold_until: null
created_at: 2026-08-25T02:41:29.609Z
updated_at: 2026-08-25T02:44:51.487Z
started_at: 2026-08-25T02:41:40.486Z
closed_at: 2026-08-25T02:44:51.486Z
close_reason: Corrected the mutable synopsis checkpoint from 37s/37 controls to the two current 69s and 91s receipts with 55 controls; logged D-223; regenerated defects.md; schema, synopsis, README, ledger, bead, and 55/55 negative-control checks pass.
resolution: null
duplicate_of: null
---
The current PR-22 checkpoint paragraph still reports 37 negative controls and a 37-second normal gate after the live review measured 55 controls and independent 69/91-second receipts. Correct the mutable current-status paragraph, retain historical measurements elsewhere, mention contained D-222 as required for every open defect, regenerate aggregates, and validate the synopsis.
