---
type: is
id: is-01m20zyy839t6mbvpqy8ay2hsn
title: "[epic] Move-set campaign: which annealing physics recovers non-grid s(n) records"
kind: epic
status: open
priority: 1
version: 4
labels: []
dependencies: []
child_order_hints:
  - is-01m20zzqjwygewaj8wkyt57shq
  - is-01m20zzsft1e4fg2370kjhp26d
  - is-01m20zztsqytk9pzr8cj930m0y
created_at: 2026-09-08T17:09:58.636Z
updated_at: 2026-09-08T17:10:27.892Z
---
Umbrella for the campaign answering the repository owner's question: with the right physics or annealing model, which method recovers best-known non-grid packings for n < 100 to high accuracy?

Design input: docs/project/research/research-2026-09-08-annealing-for-square-packing.md, the 2026-09-08 annealing survey. Its central claims this campaign tests:

- "Solve to n = 100" is 36 non-grid cases, not 100. Re-derived here from the frontier register: 36 non-grid at n <= 100, of which 15 hand-construction, 10 simulated annealing, 6 diagonal-strip, 3 extension, 2 unknown.
- required_side is a max over the two to four extreme squares, so most single-square moves are exact no-ops on the objective. That is the structural reason a plain annealer sticks just above the trivial size.
- The fixes used by engines that get close: simultaneous perturbation (Gensane layer 3), inflation or wall pressure or contract-act-re-expand, and replica exchange over a pressure ladder.
- The currency is refined local optima per record, not moves (Ellsworth: 4 of 3,004 at n = 51).

Round-1 registry: H-125 simultaneous perturbation, H-126 wall pressure, H-127 basin hopping over the LP quench.
Round-1 rounds: exp-129 calibration, exp-130 arm B, exp-131 arm C, exp-132 arm D.
