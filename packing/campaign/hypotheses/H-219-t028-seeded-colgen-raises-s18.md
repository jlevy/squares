---
title: H-219 — T-028-seeded colgen raises s(18) above 187/40
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-219
  kind: hypothesis
  claim: >-
    A rows-complete covering of mass strictly below 18 exists at a container side
    strictly above T-028 187/40 and strictly below the 117/25 plateau, on a named
    site set built by the stock colgen and seeded from the T-028 certificate, and
    both routes of decide_certificate accept the freeze.
  lane: proof
  derived_from: [X-039]
  strategy_refs: ['proof:22']
  criterion:
    shape: determination
    metric: >-
      decide_certificate on a freeze whose total_mass is strictly below 18 at a side
      in (187/40, 117/25)
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
    exact rational freeze; T-028 seed; sides in (187/40, 117/25)
  instance: {axis: n, point: 18}
  sweep:
    axis: n
    points: [18]
  priority: 1
  cost_estimate: >-
    One 1200 s leftover probe at 1871/400, then a four-grid follow-up only if that
    restricted optimum stays below 18
  prereqs: []
  replication: true
  registered: '2026-09-19'
  notes: >-
    Session-141 leftover 1871/400 T-028-seeded auto plus windows 5 converged at
    17.889237 and freeze-then-decide retained T-029. Confirmed. Off the H-218
    sweep. This retain does not confirm H-218.
---
# H-219: T-028-Seeded Colgen Raises s(18)

[X-039](../explorations/X-039-n100-re-rank-after-session-140.md) re-ranks the n<100
floors after Session-140. This claim is the unused leftover side above T-028.

Confirm only on `RETAINABLE` at n=18. `117/25` already plateaus at 18 on every named
seed and is not a target.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
