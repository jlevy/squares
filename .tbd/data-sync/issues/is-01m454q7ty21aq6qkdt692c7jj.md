---
type: is
id: is-01m454q7ty21aq6qkdt692c7jj
title: "Stage 4 for T-088 and T-089: exact rational certificates for n = 69, 83, 87, receipts, controls and a separate review"
kind: task
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
created_at: 2026-10-05T04:21:30.590Z
updated_at: 2026-10-05T07:19:53.582Z
started_at: 2026-10-05T04:23:01.170Z
closed_at: 2026-10-05T07:19:53.582Z
close_reason: "Done in jlevy/squares#353 / #359 (merged 2026-10-05)"
resolution: null
duplicate_of: null
---

## Notes

2026-10-05 exit committed on claude/ecstatic-pascal-pothtx-stage4 (NOT pushed): 858597ebc (exit: records, review, renders), a7e7540ce (DATA_REVISION re-pin to 858597eb), c0e20082c (fix: generator adopts catalogue certificates via catalogue_upper_bounds.apply_case; valid7 spot check names V-probe-valid7-fixes). packing-validate --records and --edit pass; --fast failed only on environmental steps (fixed-core-packet reaping fails identically on primary checkout 149a2950b; Chromium 1234 missing; shard D 12 s wall rule; two flakes pass alone). Open follow-ups: KB-3 finer dilation ladder in sqpack.witness.promote_rational (n=83,87 to 2 units; changes reviewed certificates, needs a decision); KB-9 sharper pair-test control; KB-10 promotion carries source.revision; KB-13 n-087 construction_method. Review worktree /home/user/squares-lanes/stage4-review (detached at 0c0559fe1, uncommitted copies of the review) can be removed.
