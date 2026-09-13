---
type: is
id: is-01m2cx3155gpjrj1gvh6g2g89t
title: The sweep route has no token cap, so a heavy threshold atom hangs the headroom check
kind: bug
status: open
priority: 1
version: 1
labels:
  - n11
dependencies: []
parent_id: is-01m2cv7affzce4qkz704rp2kvv
created_at: 2026-09-13T08:10:40.164Z
updated_at: 2026-09-13T08:10:40.164Z
---
Found while fixing PR157 review MATH-01. Not in the review; the review's own reproduction is the one case where this check happens to be cheap, which is why the overflow was reachable there at all.

THE HAZARD. `_headroom` calls `absolute_expansion_sum(A, k)`, and that is super-linear in the token total: `expansion_terms(A, k)` returns `A - k + 1` terms whose coefficient sums are roughly A-bit integers. Measured on this box:
  A=1000  -> 0.02s
  A=2000  -> 0.15s
  A=4000  -> 0.95s
  A=10000, k=2 -> did not finish in 110s
An atom with A = 5*2**59, k = 4*2**59 had to be killed during probing.

WHY IT IS REACHABLE. Only the INTERVAL route caps tokens (`MAX_TOKENS_PER_ATOM`, 4096, in threshold_interval.py). The SWEEP route has no token cap at all, and `ThresholdAtom` itself does not bound the token total -- `from_record` caps nothing either. So a certificate declaring one heavy atom does not produce a wrong answer or a refusal; it produces a hang inside the headroom check that is supposed to be the cheap guard before the expensive work.

The reviewer's MATH-01 reproduction used k = A, where the absolute coefficient mass is 1 regardless of how heavy the sites are, so `absolute_expansion_sum` returned instantly. That is precisely why the int64 overflow was reachable through that repro: the guard was cheap because the expansion was trivial. Move k away from A and the same atom hangs the guard instead.

So the two failure modes are complementary and neither is covered by the other:
  k = A, heavy tokens -> guard passes cheaply, count grid silently wrapped (MATH-01, now fixed by an exact-integer lane in charge_grid_direct)
  k << A, heavy tokens -> guard does not return

PROPOSED FIX, owner's choice: cap the token total in `ThresholdAtom` itself (so every route inherits it and `from_record` enforces it), or cap it in `_headroom` before calling `absolute_expansion_sum`, or make `absolute_expansion_sum` refuse above a declared bound. Capping on the dataclass is the only option that covers the sweep route, the interval route and record parsing with one constant; the interval route's existing MAX_TOKENS_PER_ATOM would then become a narrower allocation bound rather than the only token guard in the codebase.

NOT CLAIMED: no measurement of where the practical ceiling should sit, and the timings above are single readings on one box (D-472: one reading per configuration is a sample, not a measurement). What is established is the sign -- the cost grows fast enough that an unbounded token total is a hang, and the sweep route currently has no bound.
