---
type: is
id: is-01m2hpnsaava1xjra0d2antdy5
title: "Pack readout: show the retained best packing, and no side for an invalid state"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-09-15T04:54:46.858Z
updated_at: 2026-09-15T04:54:46.858Z
---
From the PR #160 review (`attic/reviews/pr160/review-body.md`, pinned `72629c03`), non-blocking suggestion 1, "Surface the retained best in Pack": the instantaneous side jitters and is often invalid; the retained best is the one side checked at 1e-9. Showing it, and no side for invalid states, would make the Pack readout safe to read as a claim.

State at `91cf28d6` (#171):

- The D11 fix (c0d9db2b, think-o4pj) words every Pack readout from the validity contract: an invalid state's side is printed as "bounding side" with the failing clause (`packages/workbench/src/app/pack-panel.ts:85-110`). That meets think-o4pj's criterion (label in the same field) but still prints a number for a non-packing.
- The kernel keeps a retained best admitted under `PACKING_VALIDITY` (`src/simulation/pack.ts:410-420`, `run.bestPacking`, `run.best`, `run.bestAt`), independent of frame batching, but the status line and stage facts (`pack-panel.ts:236-250`) never show it.

Work: show the retained best side (and when it was reached) beside the live state, and print no side for an invalid live state; `check_pack_panel` asserts both with an overlapping import. A presentation change to the owner's Pack panel, so confirm the wording with the owner. Related: think-o4pj, think-nals, think-adlf.
