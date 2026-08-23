---
title: H-019 — the angle objective is non-smooth at the optimum
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-019
  kind: hypothesis
  claim: >-
    s(theta), the LP-in-cell optimum as a function of the angles, has a kink at the
    optimal angles rather than a smooth minimum - distinct one-sided derivatives - so
    any first-order or smooth-model angle search stalls at a distance proportional to
    its step, and only a method that tolerates non-smoothness reaches the optimum.
  lane: search
  derived_from: []
  strategy_refs: ['search:17', 'search:19']
  criterion:
    shape: determination
    metric: ratio of the two one-sided derivatives of s at the optimal tilt
    direction: bounded away from 1
  instrument: >-
    explorations/packing/run_quench.py plus a one-sided difference probe of
    solve_to_fixed_point around the known optimal tilt; measured at n = 11, extend to
    n = 5, 10 and s(17).
  instrument_ready: true
  regime: scipy HiGHS at primal feasibility 1e-10; f64 throughout
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11]}
  priority: 1
  cost_estimate: tier S; seconds per probe
  prereqs: []
  replication: false
  registered: '2026-08-23'
  notes: >-
    Registered by the runner of exp-006 before recording it, because the round measured
    something H-002 did not predict. Kill: the one-sided derivatives agree at every
    tested instance, making the stall numerical rather than geometric.
---
# H-019 — the optimum is a corner, and that decides the method

[exp-006](../series/series-000-smoke-and-calibration/experiments/exp-006-lp-quench-n5-n10-n11.md)
walked the shared tilt of Trump’s five tilted squares off its optimal value and solved
the cell at each step:

| `δ` from the optimal tilt | `s(θ* + δ) − s*` |
| ---: | ---: |
| `−1e-3` | `1.748e-04` |
| `−1e-5` | `1.747e-06` |
| `0` | `1.742e-10` |
| `+1e-5` | `3.840e-06` |
| `+1e-3` | `3.846e-04` |

Both sides are linear in `δ` and their slopes differ — about `0.175` on the left and
`0.384` on the right.
The minimum is a **corner**, not a smooth basin floor.

That is what rigidity looks like from the angle side: the optimum sits exactly where the
active contact set changes, so the one-sided derivatives belong to two different contact
structures and cannot agree.

## Why it matters more than it looks

It decides what the quench spine’s angle half may be built from.
A gradient, a quasi-Newton model, or a simplex-of-points method all assume a locally
smooth objective and none can converge to a corner: measured in the same round,
finite-difference descent stalled five orders short, and Powell and Nelder-Mead did
*worse* than descent.
A method that tolerates non-smoothness — a bisection on the sign of the one-sided
derivative, a subgradient or bundle method, or solving the active contact system
algebraically — is not an optimisation preference here, it is a correctness requirement.

If this generalises across `n`, it is also an argument for
[H-001](H-001-angle-class-reduction.md) that H-001 does not itself make: reducing the
angles to classes shrinks the non-smooth search to one or two dimensions, where
bracketing methods converge to the solver floor.
