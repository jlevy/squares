---
title: H-218 — stock colgen raises a verified floor at n in {12,17,19,20}
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-218
  kind: hypothesis
  claim: >-
    A rows-complete covering of mass strictly below n exists at a container side
    strictly above the current verified floor for at least one n in {12, 17, 19, 20},
    on a named site set built by the stock colgen (auto or four-grid, optional
    certificate seed, optional window lattice), and both routes of decide_certificate
    accept the freeze.
  lane: proof
  derived_from: [X-038]
  strategy_refs: ['proof:22']
  criterion:
    shape: determination
    metric: >-
      decide_certificate on a freeze whose total_mass is strictly below n at a side
      strictly above T-017 (n=12), T-019 (n=17), T-020 (n=19), or T-021 (n=20)
    direction: >-
      Confirm only when decide_certificate prints RETAINABLE. A restricted optimum
      above n, an unconverged loop, a freeze above n, or a stalled interval route
      does not refute the claim; it refutes that site set at that side.
    threshold: 1
  instrument: >-
    devtools.run_fractional_colgen with --freeze; declare_least_cell_mass; then
    both routes of decide_certificate. No packing-campaign runner. No new atom class.
  instrument_ready: true
  regime: >-
    B = 9977/10000, 181-direction net, D4-symmetric nonnegative point-atom weights,
    exact rational freeze; sides strictly above the current verified floor
  instance: {axis: n, point: 20}
  sweep:
    axis: n
    points: [12, 17, 19, 20]
  priority: 1
  cost_estimate: >-
    Four hours of sequential 15-to-40-minute colgen probes on the ranked queue in
    X-038; retain only if the gate prints RETAINABLE
  prereqs: []
  replication: true
  registered: '2026-09-19'
  notes: >-
    X-038 ranks n=20 at 973/200 first because the old certificate-seeded run crossed
    at 20.000223. H-062 walled that side on two named site sets; this claim is about
    a different construction class, not a replay of those two. n=18 is on the survey
    queue but not on this sweep: 117/25 already plateaus at 18. n=11 is excluded;
    T-026 stands. Session-140 landed T-028 at n=18; that retain is off this sweep
    and does not confirm the claim. Session-140 leftover n=20 971/200 stopped at
    19.910044 unconverged below 20, and leftover n=12 3969/1000 stopped at
    12.091168 after crossing 12. Neither freeze was offered. The claim stays open.
    Session-141 reopens it on a new named set: n=20 971/200 with T-021 four-grid
    (34,46,56,64) plus windows 7, as exp-164, after exp-163 accepted T-029. That
    probe stopped at 19.857588 unconverged below 20; remaining rows raise. The
    follow-up exp-165 at 243/50 on the same four-grid stopped at 19.887914
    unconverged below 20; remaining rows raise. Do not replay leftover auto plus
    windows 6 at 971/200 or the Session-141 four-grid at 971/200 or 243/50.
    T-029 does not confirm this claim. After the eight H-220 Nagamochi sides
    finished without RETAINABLE, Session-141 continues on this sweep at n=19
    481/100 T-020 four-grid (34,45,56,64) plus windows 7 as exp-174, which
    stopped at 19.111435 unconverged after crossing 19; remaining rows raise.
    leftover auto plus windows 6 at 481/100 already crossed 19. Follow-up
    exp-175 at n=12 793/200 T-017 auto plus windows 7 stopped at 12.067502
    unconverged after crossing 12; remaining rows raise. Follow-up exp-176 at
    n=12 397/100 T-017 auto plus windows 7 stopped at 12.097146 unconverged
    after crossing 12; remaining rows raise. Follow-up exp-177 at n=19
    241/50 T-020 four-grid plus windows 7 stopped at 19.224565 unconverged
    after crossing 19; remaining rows raise. Follow-up exp-178 at n=12
    793/200 T-017 four-grid plus windows 7 stopped at 12.066995 unconverged
    after crossing 12; remaining rows raise. Follow-up exp-179 / H-221 retained
    T-030 at n=18 4679/1000. Do not replay the Session-141 four-grid at 481/100
    or 241/50 or 793/200 or auto at 793/200 or 397/100. Do not more-wall
    4679/1000.
---
# H-218: Stock Colgen Raises One Small-n Floor

[X-038](../explorations/X-038-n100-lower-bound-survey.md) lists every open floor at
`n <= 100` and ranks the ones the stock covering producer can still touch.

This claim is the first-wave existence statement: at least one of `n = 12, 17, 19, 20`
admits a freeze below `n` at a side above the current verified floor, accepted by both
routes of `decide_certificate`.

A site set that finishes above `n` is a negative about that construction, not about the
side. H-062’s wall at `973/200` binds the two site sets it named. It does not bind a
windows lattice or a four-grid.

Confirm only on `RETAINABLE` at an n on this sweep. n=11 and n=6 are out of scope.
T-028 at n=18 is off-sweep and does not confirm this claim.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
