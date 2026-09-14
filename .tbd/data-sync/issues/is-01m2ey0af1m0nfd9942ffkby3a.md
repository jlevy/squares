---
type: is
id: is-01m2ey0af1m0nfd9942ffkby3a
title: "Route A: test a systematic case split (helper argument) at side 3.85"
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
created_at: 2026-09-14T03:05:08.832Z
updated_at: 2026-09-14T03:05:08.832Z
---
Split packings by region occupancy or wall-contact pattern, then run a conditional certificate per case; this goes past the point-certificate ceiling L* ≈ 3.8288 by construction. Precedent: T-023 closed one four-owner branch at 3.84. First test (≤1 day): at side 3.85, enumerate occupancy patterns under proved per-cell capacity caps, run the existing threshold generator on each, report the share closed and the worst residual case. Obstacle: balanced patterns may still admit 10–11 fractional squares.
