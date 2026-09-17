---
type: is
id: is-01m2qm4f1nf7qrv4tqe9m3y7t0
title: "M7 calibration: close the n=6 point bracket at 299/100 and build an n-parameterised threshold producer"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-17T12:05:48.708Z
updated_at: 2026-09-17T12:05:48.708Z
---
From the 2026-09-17 overnight M7 lane (think-4woh; X-037). The n=11 fractional point-certificate producer runs at other n without code changes. n=6, side 299/100, B=9977/10000, 181-net: covering value bracketed in [83/14 = 5.928571 exact, 6.006571 float] -- no site set crossed below 6, no exact depth<=1 family reaches 6; undecided. n=10, side 37/10: closed trivially (0.9977*s(10) = 3.6986 < 3.70, the shrunken known-best packing is a depth-1 mass-10 family); a certificate needs B > 0.998083 and at least 216 net steps; gate-verified crossings s(10) >= 3.685 and s(6) >= 2.97 (weaker than known results, calibration only). Next: close the 299/100 bracket exactly (exact check of the 1128-placement union, which timed out at 20 min twice), then build a threshold (2-of-3) producer that takes n (T-025's producer exists only as agenda-034 .py.txt scratch; estimate 2-3 h) to calibrate the one mechanism past L* on a solved case. Tooling gaps to fix as guarded tools: G1 run_fractional_colgen does not pass support_cap (dual truncated to 32 rows, colgen.py:1079) and never writes the dual family; G2 polish_ceiling_family refuses reflected axis-parallel squares written with t=0; G3 independent_ceiling_reader requires total == n and max depth == 1 rather than >= n and <= 1; G4 no n-parameterised threshold producer; G5 interval-route stalls blocked gate verification at 298/100 and 2985/1000. Owner decision: whether to register the calibration statement 'no point certificate at n=6, 299/100, B=9977/10000, 181-net, for any site set'.
