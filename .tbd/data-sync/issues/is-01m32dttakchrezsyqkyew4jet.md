---
type: is
id: is-01m32dttakchrezsyqkyew4jet
title: Decide registration of s(17) > 461300/99853 and reconcile it with PR 211
kind: task
status: open
priority: 1
version: 6
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m32dt0p76c4bvp3amxtmyt2p
child_order_hints:
  - is-01m32f1gyvq00kvmh9mab7jph9
  - is-01m32f1hyg3ce025vy02y3m7s4
hold: null
hold_until: null
created_at: 2026-09-21T16:47:19.891Z
updated_at: 2026-10-05T05:40:47.011Z
started_at: 2026-10-05T05:34:33.010Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
Blocked on the replay and the proof review.

If admitted: decide whether PR 211 should still register 461300/99999 at all or be superseded outright, which identifiers the two values take, which register rows move (results.yaml, RESULTS.md, INVENTORY.md, n-017.md, SYNOPSIS.md), and what the session and bead record must say. Precedent for one T-id superseding another at the same n must be cited, not invented.

If not admitted: retain as an unadjudicated external source, move no bound, and record what would reopen it.

## Notes

Reopened: Reopened 2026-10-05: closing it left open children under a closed parent, which devtools.check_bead_tree refuses. The parent's own work is adopted (see the close reason), but its open children need their own disposition before it closes.
