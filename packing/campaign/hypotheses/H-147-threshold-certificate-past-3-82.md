---
title: H-147 — a threshold certificate proves a side above 191/50 unconditionally
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-147
  kind: hypothesis
  claim: >-
    The rank-one threshold-atom closure admits a D4-symmetric certificate at a container
    side strictly above 191/50, in one of two ways: the frozen 191/50 threshold
    certificate, placed on a finer net at the larger shrink the net admits and rescaled
    by one rational factor, passes both routes of the gate and dilates by T-022's
    sharpened containment argument to a weak limit above 3.826; or the threshold loop
    started from the accepted 191/50 site and atom set reaches a rows-complete value
    below eleven at 383/100, which freezes to an endpoint certificate there.
  lane: proof
  derived_from: [X-024]
  strategy_refs: ['proof:22', 'proof:23']
  criterion:
    shape: determination
    metric: >-
      the largest side certified unconditionally by a frozen threshold certificate
      accepted by devtools.decide_threshold_certificate with both routes agreeing,
      together with the weak limit its dilation record derives
    direction: >-
      Confirm with a frozen threshold certificate at 383/100 accepted by both routes, or
      with the frozen 191/50 certificate accepted by both routes on a 720- or 1440-step
      net at a shrink whose dilation record exceeds 3.826. Refute the finer-net half by
      the frozen atoms failing every finer net at the sharpened-test shrink, and the
      383/100 half by an exact depth-one family at 383/100 feasible for every rank-one
      threshold atom with weight at least eleven, decided exactly. An LP value with rows
      incomplete decides neither direction.
    threshold: 3.826
  instrument: >-
    devtools.decide_threshold_certificate is the two-route gate; devtools.dilation_corollary
    derives the limit record once it accepts a threshold record's closed-form conditions,
    which it does not yet read; devtools.measure_net_refinement measures crossing shrinks
    for point certificates and needs the threshold sweep to do the same for threshold
    ones; the loop is spike B's rows-only driver and its freeze script, retained beside
    lane B and unpromoted.
  instrument_ready: false
  regime: >-
    n = 11, sides 191/50 and 383/100, shrink 9977/10000 on the 181-direction net and the
    crossing shrinks on the 720- and 1440-step nets; rank-one atoms, D4-symmetric,
    nonnegative weights
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: >-
    the finer-net half is two gate runs and two dilation records, under an hour on one
    core; the 383/100 half is a ninety-minute loop on three cores plus one gate run
  prereqs:
  - the threshold sweep exposed to measure_net_refinement and dilation_corollary
  - the rows-only loop and freeze script promoted or run from their retained copies
  replication: true
  registered: '2026-09-09'
  notes: >-
    The point-atom method is capped at unit side 3.8288 by the exact ceiling family at
    191/50, so no point certificate reaches 383/100 = 3.83 at this shrink, and the LP at
    191/50 read exactly eleven every time its rows completed. The threshold certificate
    at 191/50 sits at 10.967322864 with the rows complete, 0.0327 below eleven; the
    point certificate at 381/100 sat at 10.863675 and the next hundredth of side cost it
    0.136. Whether the threshold LP's slope is gentler is the whole question, and the
    two-of-three atoms are only the first family: three-of-four, two-of-five and
    three-of-five atoms are the next. The finer-net half is the cheap first reading,
    because the dilation argument uses only Conditions 1 to 4 and inverse dilation of
    placements, none of which distinguishes a threshold atom from a point atom.
---
# H-147 — Past 3.82 Without Conditioning

The threshold certificate at `191/50` is the first result past the point-method ceiling,
and [X-024](../explorations/X-024-two-lines-at-eleven.md) makes pushing it up in side
the primary lane, because each success is a global bound in one certificate.
There are two ways up, and both are cheap to read.

The first costs no search.
The finer-net mechanism of
[T-024](../../cases/n11_fractional_certificate/t-024-dilation-limit-proof.md) is a
statement about cores, not about atoms: a finer net admits a larger shrink under
Condition 4, and the frozen weights, multiplied by one rational factor, either cover
every closed core at the new shrink or they do not.
On the point atoms of `T-018` they did, at every net up to 2880 steps, and the 1440-step
rung dilated to `3.816609502788862`. The same sweep on the threshold certificate, with
the threshold atoms entering the same difference array, answers the same question at
`191/50`; if the atoms transfer, the endpoint is about `3.8266`.

The second is the loop.
Spike B’s rows-only driver, warm-started from the accepted site and atom set, costs
about forty seconds a round; the question at `383/100` is whether the value stays below
eleven once the rows are complete, or refills to eleven the way the point LP did at
`191/50`. A refill would be read against its dual, which is the fractional packing
feasible for every two-of-three atom on the site set, and that dual is what the next
atom families would have to cut.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
