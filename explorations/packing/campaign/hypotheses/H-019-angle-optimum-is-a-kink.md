---
title: H-019 — Trump's shared-tilt slice is non-smooth at the published optimum
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-019
  kind: hypothesis
  claim: >-
    On the n=11 Trump contact cell, varying the shared tilt of its five tilted squares
    while re-optimizing centres by LP gives unequal left and right slopes at the
    published tilt. The tested one-dimensional objective therefore has a kink rather
    than a smooth minimum there.
  lane: search
  derived_from: []
  strategy_refs: ['search:17', 'search:19']
  criterion:
    shape: determination
    metric: ratio of the two one-sided derivatives of s at the optimal tilt
    direction: bounded away from 1
  instrument: >-
    cases.campaign_smoke.quench_experiment plus a one-sided difference probe of
    solve_to_fixed_point around the known optimal tilt; measured at n = 11, extend to
    other cells only under separately registered generalizations.
  instrument_ready: true
  regime: scipy HiGHS at primal feasibility 1e-10; f64 throughout
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [11]}
  priority: 1
  cost_estimate: tier S; seconds per probe
  prereqs: []
  replication: false
  registered: '2026-08-23'
  notes: >-
    Registered by the runner of exp-006 before recording it, because the round measured
    something H-002 did not predict. Kill: the one-sided derivatives agree at the
    registered n = 11 slice, making the stall numerical rather than geometric. Corrected under
    D-052 to remove an unsupported claim about all smooth and derivative-free methods;
    the measured one-dimensional kink and criterion are unchanged.
---
# H-019 — the tested shared-tilt slice has a corner

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

That establishes a kink along this angle slice, not rigidity of the full packing.
The optimum sits where the active contact set changes, so the one-sided derivatives
belong to two different contact structures and need not agree.

## Why it matters more than it looks

It informs what the quench spine’s angle half may be built from.
A kink defeats the smooth derivative model used by finite-difference descent.
In the same round, that descent stalled five orders short, and the tested Powell and
Nelder–Mead runs did *worse* than descent.
The latter two are derivative-free and can handle some nonsmooth objectives; these runs
are empirical failures, not a theorem that those method families cannot converge to a
corner. Any convergence claim must therefore account for non-smoothness rather than rely
on a smooth local model at this point.
Bracketing, subgradient or bundle methods, and active-contact algebra are candidates;
the experiment does not prove that one family is necessary or sufficient.

If this generalises across `n`, it is also an argument for
[H-001](H-001-angle-class-reduction.md) that H-001 does not itself make: reducing the
angles to classes shrinks the non-smooth search to one or two dimensions, where the
tested bracketing implementation reached the solver floor on the proved controls.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
