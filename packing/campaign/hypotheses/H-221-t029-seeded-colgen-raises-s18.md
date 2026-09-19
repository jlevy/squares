---
title: H-221 — T-029-seeded colgen raises s(18) above 1871/400
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-221
  kind: hypothesis
  claim: >-
    A rows-complete covering of mass strictly below 18 exists at a container side
    strictly above T-029 1871/400 and strictly below the 117/25 plateau, on a named
    site set built by the stock colgen and seeded from the T-029 certificate, and
    both routes of decide_certificate accept the freeze.
  lane: proof
  derived_from: [X-039]
  strategy_refs: ['proof:22']
  criterion:
    shape: determination
    metric: >-
      decide_certificate on a freeze whose total_mass is strictly below 18 at a side
      in (1871/400, 117/25)
    direction: >-
      Confirm only when decide_certificate prints RETAINABLE. A restricted optimum
      above 18, an unconverged loop, a freeze above 18, or a stalled interval route
      does not refute the claim; it refutes that site set at that side. 117/25 is
      not in the interval.
    threshold: 1
  instrument: >-
    devtools.run_fractional_colgen with --freeze; declare_least_cell_mass; then
    both routes of decide_certificate. No packing-campaign runner. No new atom class.
  instrument_ready: true
  regime: >-
    B = 9977/10000, 181-direction net, D4-symmetric nonnegative point-atom weights,
    exact rational freeze; T-029 seed; sides in (1871/400, 117/25)
  instance: {axis: n, point: 18}
  sweep:
    axis: n
    points: [18]
  priority: 2
  cost_estimate: >-
    One 1200 s probe at 4679/1000 after the Session-141 ranked queue reaches it
  prereqs: []
  replication: true
  registered: '2026-09-19'
  notes: >-
    Session-141 T-029-seeded auto plus windows 5 at 4679/1000 converged at
    17.893285 and freeze-then-decide retained T-030. Confirmed. Off the H-218
    sweep. This retain does not confirm H-218. Do not more-wall 4679/1000.
---
# H-221: T-029-Seeded Colgen Raises s(18)

[X-039](../explorations/X-039-n100-re-rank-after-session-140.md) left a 0.0025-wide
interval between T-029 `1871/400` and the `117/25` plateau. This claim is that
interval.

Confirm only on `RETAINABLE` at n=18. `117/25` is not a target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
