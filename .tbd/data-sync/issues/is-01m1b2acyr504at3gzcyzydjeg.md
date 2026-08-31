---
type: is
id: is-01m1b2acyr504at3gzcyzydjeg
title: "Queue hygiene: reconcile the 25 in_progress beads left by closed sessions"
kind: chore
status: open
priority: 3
version: 2
labels:
  - x-010
dependencies: []
created_at: 2026-08-31T04:47:53.815Z
updated_at: 2026-08-31T05:14:46.342Z
---
tbd list --status in_progress carries 25 beads including epics for sessions closed weeks ago (session-010 era, PR-41/44/45 integration, CI tiering already landed). Each: close with a reason, return to open, or re-own. Stale in_progress hides real capacity and distorts ready-queue trust; OR-4 takes the next slice from the handoff, and the handoff should not point at ghosts.

## Notes

agenda-010 BC-097, gate filler only, alongside think-6z95.
