---
type: is
id: is-01m1b29qrvdzvmjb2n22n5826h
title: "Lane A2: certified lower bounds past Nagamochi at the Green Table-2 sizes"
kind: task
status: in_progress
priority: 2
version: 5
spec_path: packing/campaign/explorations/X-010-two-lanes-two-ladders.md
delegate: claude-code@vm
labels:
  - x-010
  - lane-a
dependencies:
  - type: blocks
    target: is-01m1aqj5mt1nn96rvkk06qggwq
hold: null
hold_until: null
created_at: 2026-08-31T04:47:32.123Z
updated_at: 2026-08-31T09:50:27.856Z
started_at: 2026-08-31T09:38:40.199Z
---
DS7 Table 2's non-trivial lower bounds at ~23 open cases rest on 'T. Green, 2000, private communication' -- no primary exists, so think-s1pc's W2 read cannot happen and certifying sets of our own is the only route by which the frontier can adopt values there. First targets n = 17, 18 (Green ~4.4452 vs Nagamochi ~4.1623), where DS7 Figure 34 sketches the set shape. Every certified value above the closed form moves a verified lower lane untouched since 2005. Exit per size: a replayable certificate and a frontier move per the evidence contract, or a typed refusal naming the escaping pose. X-010 Lane A rung 2.

## Notes

2026-08-31 session-057 (block 6): the verified lower lane MOVES — s(17) >= 17/4 = 4.25 and s(18) >= 17/4, certified exactly by a sixteen-point unavoidable set in [0,17/4]^2 (cases/green17), above Nagamochi's ~4.1623, below Green's unadoptable ~4.4452. Design derived first-hand: rationalized Bentz grid (rows 457/500 + k*433/500), x=7/2 column appended to every row, wall strips with wall-vertex ends, three left-wall Lemma 5 quads at (433/500, 1/2), right margin band of exactly 1/2, four near-slabs with worst corner distance^2 = 249989/1000000 (slack 11/1000000 pins the side to exactly 17/4). Falsifier corroborates: 393,216 poses saturate at best margin -1e-4 (caveat intact). Held unresolved+needs_review; frontier adoption is a reviewed evidence-contract change. Typed remainder: the n=19 variant has one spare point (17 allowed) — one gap-anchor at (t-1/2, y) could push t slightly for n>=19; Green's own construction shape (Fig 34, no primary) remains unreconstructed; the m<->paper reconciliation of Green's Theorem 9 formula (2*sqrt2 - 1 prefix = two wall strips) suggests his middle rows use a different cell type — worth one read-through before any further push.
