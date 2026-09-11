---
title: H-156 — a threshold certificate proves a side above 191/50 unconditionally
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-156
  kind: hypothesis
  claim: >-
    The rank-one threshold-atom closure admits a D4-symmetric certificate at a container
    side strictly above 191/50, in one of two ways: the frozen 191/50 threshold
    certificate, placed on a finer net at the larger shrink the net admits and rescaled
    by one rational factor, passes both routes of the gate and dilates by T-022's
    sharpened containment argument to a lower bound above 3.826; or the threshold loop
    started from the accepted 191/50 site and atom set reaches a rows-complete value
    below eleven at 383/100, which freezes to an individual-side certificate there.
  lane: proof
  derived_from: [X-024]
  strategy_refs: ['proof:22', 'proof:23']
  criterion:
    shape: determination
    metric: >-
      the largest side certified unconditionally by a frozen threshold certificate
      accepted by devtools.decide_threshold_certificate with both routes agreeing,
      together with the lower bound its dilation record derives
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
    devtools.decide_threshold_certificate is the two-route gate;
    devtools.measure_threshold_net_refinement measures the finer-net crossing shrink;
    and devtools.dilation_corollary replays the threshold record's closed-form
    conditions and derives the retained limit record. The separate 383/100 loop remains
    in its retained unpromoted state.
  instrument_ready: true
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
    T-026 subsequently confirms the first disjunct. The retained 1440-step certificate
    and exact dilation corollary prove
    s(11) >=
    955000*sqrt(518400042893309449)/179696714646249 = 3.826447410572939744...
    at V4/C5 after the mapped source-distinct review of the self-contained claim. The
    separate rows-complete loop at 383/100 remains open, as do re-optimised finer-net
    atoms and changed atom families. The point-atom obstruction and earlier LP slopes
    retain their original finite scopes.
---
# H-156 — Past 3.82 Without Conditioning

**Status update, September 10, 2026.** T-026 confirms the finer-net and dilation
disjunct by proving the ordinary exact lower bound
`s(11) >= 955000*sqrt(518400042893309449)/179696714646249 =
3.826447410572939744...` at V4/C5. The separate rows-complete loop at `383/100`,
re-optimisation on a finer net, and changed atom families remain open.

The
[source-distinct review](../../../docs/project/reviews/review-2026-09-10-t025-t026-verifiable-claims.md)
checks the complete claim from the finite threshold certificate through the endpoint
inference. The promotion from C4 to C5 changes the retained assurance record, not the
theorem or this hypothesis’s measured outcome.

**Separate strictness question.** The dilation-limit method does not establish
`s(11) > 955000*sqrt(518400042893309449)/179696714646249`. This does not qualify the
proved lower bound.

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
the threshold atoms entering the same difference array, gives the verified covering
premise for the dilation-limit lower bound `3.826447410572939744...` from the 1440-step
rung.

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
