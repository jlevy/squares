---
type: is
id: is-01m2ey0c330crgmbpxncejahnx
title: "Route B: test a pairwise SDP bound, starting with an n=6 control"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-14T03:05:10.489Z
updated_at: 2026-09-14T03:05:10.489Z
---
Lasserre level-2 or Schrijver theta-prime bound on a soundly discretized placement graph (de Laat–Vallentin 2015 style). The only route that attacks the fractional-versus-integer gap directly, and the most likely source of a compact proof. Decisive first test: n=6 near side 3, where point certificates reportedly fail (Stromquist recollection, unproved); if theta-prime succeeds there, compare it with the LP at n=11, side 3.84. Obstacles: no symmetry reduction; coarse cells lose conflict edges near the tight side.
