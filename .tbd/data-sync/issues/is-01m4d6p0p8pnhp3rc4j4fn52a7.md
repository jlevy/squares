---
type: is
id: is-01m4d6p0p8pnhp3rc4j4fn52a7
title: Restore measured import validation lanes without relaxing gates
kind: task
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4cxvcjvqn3knceewfmcwtqb
hold: null
hold_until: null
created_at: 2026-10-08T07:29:43.097Z
updated_at: 2026-10-08T10:20:40.609Z
started_at: 2026-10-08T07:30:01.120Z
---
Fix hosted full-checkpoint call-wall failures at imported stack heads while preserving all functional assertions, complete source custody, invalid-input refusals, and existing 12-second/byte/time limits. Optimize repeated catalogue/fragment/admission work, declare only measured complete-worker or geometry integrations in slow lane, independently review, merge through stack, and require fresh exact-head CI.

## Notes

MAIN INTEGRATION CHECKPOINT 2026-10-08 UTC: Fetched origin/main e74a82190302a576e312a9daf2780626971454a2 repeatedly; all six owned intake branches434/439/440/441/442/443 contain it through clean normal merges, no force or hook bypass. Fresh434 source-cap failure201343816 was resolved by backporting independently accepted440 exact-destination deduplication: all selected source paths retained,576453 repeated-write bytes avoided, final11e78e029 cap200771087/201326592. Nine tiny meaningful copy/sparse controls and Ruff pass; strong review accepted. Final44094de/4417591 are full-tree-identical to prior reviewed heads; final442e098/4437194 are similarly history-only joins. Required43437760456404 and44237760346465 completedSUCCESS; final Pages/full/deferred gates remain pending, so all PRs remain draft. Previous local --push900-second failures and isolated clone180-second timeout remain failures; no cap/time limit raised and no alternate-ODB implementation adopted. External scratch low, disk-heavy local clones/builds paused. Final heads/caps/ancestry durable in review-notes/latest-main-intake-cascade.json; complete checkpoints dispatched once per final head. Performance work stays open until final hosted outcomes and review-ready status.
