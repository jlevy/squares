---
type: is
id: is-01m1b29rfxaxq8g3nbt23wwgre
title: "Lane A4: machine-readable Bentz m=7, then the m=8 substitution at n=61 (H-033)"
kind: task
status: open
priority: 2
version: 8
spec_path: packing/campaign/explorations/X-010-two-lanes-two-ladders.md
delegate: claude-code@vm
labels:
  - x-010
  - lane-a
dependencies:
  - type: blocks
    target: is-01m0qxpfkjybnxbyx67zy0vyta
hold: paused
hold_until: null
created_at: 2026-08-31T04:47:32.861Z
updated_at: 2026-08-31T10:06:16.641Z
started_at: 2026-08-31T10:06:00.774Z
closed_at: null
close_reason: null
resolution: null
duplicate_of: null
---
s(m^2-3)=m is proved for m = 3..7 and conjectured for all m >= 3 in Bentz 2016; n = 61 is the next member, third-narrowest gap in the corpus (0.0718). H-033's registered route: encode the m = 7 proof as checked moving resources in the A0 instrument, substitute m = 8, falsify each failed forcing step before inventing a new resource. Peak of Lane A together with s(12) = 4; ambition bounded by rungs A0-A1 landing first. Sharpens think-9m9x to the Bentz-line route. X-010 Lane A rung 4.

## Notes

2026-08-31 session-058 (BC-103 sizing slice, PARKED): the m=7 encoding cost one block (92 cells, 3 lemma kinds, no corner-restriction machinery, 3.2s wall, certified first run). The m=8 substitution breaks BEFORE any lemma encoding: the pattern's ceiling is 7*sqrt(3)/2 + 2*sqrt(2) - 1 ~ 7.8906 — exactly below 8 (4*sqrt2+7*sqrt3 < 18 since 18816 < 21025) AND below the standing verified lower 7.928203 at n=61 (Nagamochi, per gap_ranking), so it proves nothing. First breaking premise: the wall strip's b <= sqrt(2)-1/2 (equivalently Lemma 2 capping row pitch at sqrt(3)/2: 8 rows at side 8 need pitch ~0.8817). Lattice dilemma exact: 8 rows fit the 60-point budget but not the geometry (+0.0157 pitch over cap); 9 rows fit the geometry (pitch ~0.77) but need 67 points (+7 over budget). A real attempt needs: deeper wall cells (Lemma-5-family strips reach ~0.95 depth -> ceiling ~7.96, still short), non-uniform/sheared lattices, or m=4-style corner-restriction analysis spending fewer points. Full attempt stays a later agenda's, now with its first obstruction named exactly.
