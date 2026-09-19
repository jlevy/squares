---
title: H-220 — seedless colgen raises a Nagamochi-only floor
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-220
  kind: hypothesis
  claim: >-
    A rows-complete covering of mass strictly below n exists at a container side
    strictly above the Nagamochi floor for at least one n in
    {32, 31, 30, 26, 27, 29, 45, 44}, on a named seedless site set built by the
    stock colgen (auto grids, optional windows), and both routes of
    decide_certificate accept the freeze.
  lane: proof
  derived_from: [X-039]
  strategy_refs: ['proof:22']
  criterion:
    shape: determination
    metric: >-
      decide_certificate on a freeze whose total_mass is strictly below n at a
      queued Nagamochi-only side
    direction: >-
      Confirm only when decide_certificate prints RETAINABLE. A restricted optimum
      above n, an unconverged loop, or a freeze above n refutes that site set only.
    threshold: 1
  instrument: >-
    devtools.run_fractional_colgen with --freeze and no --seed-certificate;
    declare_least_cell_mass; then both routes of decide_certificate. No
    packing-campaign runner.
  instrument_ready: true
  regime: >-
    B = 9977/10000, 181-direction net, D4-symmetric nonnegative point-atom weights,
    exact rational freeze; no first-party certificate seed
  instance: {axis: n, point: 32}
  sweep:
    axis: n
    points: [32, 31, 30, 26, 27, 29, 45, 44]
  priority: 2
  cost_estimate: >-
    Sequential 1200 s probes on the eight queued sides after H-219 and the H-218
    n=20 new-site probe
  prereqs: []
  replication: true
  registered: '2026-09-19'
  notes: >-
    Session-140 second-wave queue never started. n=28, n=61, and n=78 stay
    deferred. Calibration: no seed, larger placement sets. Different n and
    construction class from H-218. Session-141 exp-166 at n=32 29/5 auto plus
    windows 5 stopped at 29.803318 unconverged below 32; remaining rows raise.
    Session-141 exp-167 at n=31 57/10 auto plus windows 5 stopped at 28.331329
    unconverged below 31; remaining rows raise. Session-141 exp-168 at n=30
    559/100 auto plus windows 5 stopped at 27.178193 unconverged below 30;
    remaining rows raise. Session-141 exp-169 at n=26 513/100 auto plus windows 5
    stopped at 25.000000 unconverged below 26; remaining rows raise. Follow-up
    is exp-170 at n=27 525/100, which stopped at 25.000000 unconverged below 27.
    Follow-up is exp-171 at n=29 548/100, which converged at 26.040745 with
    freeze mass 52081879/2000000; declare accepted; decide_certificate refused
    the interval route (272 stalled). T-030 was not offered. Follow-up is
    exp-172 at n=45 684/100, which stopped at 42.137360 unconverged below 45;
    remaining rows raise. Follow-up is exp-173 at n=44 675/100, which stopped at
    41.236782 unconverged below 44; remaining rows raise. The eight queued sides
    are measured. None printed RETAINABLE. Do not replay n=32 29/5, n=31 57/10,
    n=30 559/100, n=26 513/100, n=27 525/100, n=29 548/100, n=45 684/100, or
    n=44 675/100 auto plus windows 5. Confirm only on RETAINABLE.
---
# H-220: Seedless Colgen Raises a Nagamochi-Only Floor

[X-039](../explorations/X-039-n100-re-rank-after-session-140.md) keeps the eight
Nagamochi sides Session-140 queued and did not start.

The first probe is n=32 at `29/5`, auto plus windows 5, no certificate seed.
Later probes are n=31 at `57/10`, n=30 at `559/100`, n=26 at `513/100`,
n=27 at `525/100`, and n=29 at `548/100`. A float LP above `n` refutes that
site set only. n=29 converged and froze below 29; the interval route refused
the freeze. n=45 at `684/100` stopped at `42.137360` unconverged. n=44 at
`675/100` stopped at `41.236782` unconverged. The eight queued sides are
measured. None printed `RETAINABLE`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
