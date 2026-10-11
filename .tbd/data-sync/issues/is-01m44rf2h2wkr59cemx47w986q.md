---
type: is
id: is-01m44rf2h2wkr59cemx47w986q
title: "A deferred catalogue intake had no owning bead: n = 69, 83, 87 sat five days as pending_catalogue_intake while the frontier called the older sides best known"
kind: bug
status: closed
priority: 1
version: 6
delegate: claude-code@vm
labels:
  - result-import
dependencies: []
parent_id: is-01m44qz0rxvkakmyqaj7qdgagv
hold: null
hold_until: null
created_at: 2026-10-05T00:47:20.098Z
updated_at: 2026-10-05T07:19:48.447Z
started_at: 2026-10-05T00:49:40.017Z
closed_at: 2026-10-05T07:19:48.447Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---
Root cause (2026-10-05): the 2026-09-30 refresh (a897e4031, 1d4020e9f, b8502282d) correctly held the three September 2026 sides as pending intake, and plan-2026-10-01-result-status.md listed 'Register the three catalogue intakes', but no open bead owned the work (only a closed bead's notes mention it). check_requests --backlog reads only GitHub issues and register entries, and check_source_coverage accepts a pending entry indefinitely, so nothing surfaced it. Fix: every pending_catalogue_intake entry names an open bead and a recorded date, the checker refuses one without it, and the sweep reports pending intakes with their age.

## Notes

2026-10-05: b8f94a3ec guard (pending_catalogue_intake bead+recorded; deferred-conflict bead; check_bead_tree liveness incl. open issues' answer_bead), 52c4ddd39 extends it to queued results/asks' own bead; 935a42c2f + 52c4ddd39 postmortem and D-519 (both later instances included: think-e6ss, whose stage 3 sat unresumed after jlevy/squares#305 merged; c56b9b7/1ebd484 unretained). The three live entries name think-s1xt; the Kingbird lane deletes them (merge: take the deletion). Follow-up think-du1e.
