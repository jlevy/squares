---
title: H-012 — record basins are rare in quench measure
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-012
  kind: hypothesis
  claim: >-
    Under one versioned raw-coordinate multistart proposal P, deterministic quench Q,
    and terminal-component equivalence E, the proved-optimal component at n = 10 and
    Trump's component at n = 11 each have attraction probability below one tenth of the
    modal component's probability.
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12']
  criterion:
    shape: determination
    metric: per-instance record-to-modal attraction-probability ratio with 95% interval
    direction: accept only if the upper bound is below 0.1 at both n = 10 and 11; reject if the lower bound is at least 0.1; otherwise inconclusive
  instrument: >-
    Not yet built. Extend H-011's event and component pipeline to n = 11, then estimate
    the two ratios from independently replicated samples. Zero hits produce an upper
    bound, not probability zero.
  instrument_ready: false
  regime: >-
    Versioned P/Q/E required: initial-side rule, coordinate parameterization,
    feasibility or repair rule, RNG, quench implementation and terminal equivalence are
    all part of the estimand and artifact.
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [10, 11]}
  priority: 1
  cost_estimate: tier M because H-011 stops at n = 10 and the n = 11 cell needs new identified events
  prereqs: [H-011, H-021, H-023, n = 11 terminal-component identity]
  replication: true
  registered: retroactive
  notes: >-
    The load-bearing premise of the whole cartography program, registered so it can fail
    cheaply. Kill: a 95% interval excludes ratios below 0.1 - then this proposer does not
    show the claimed order-of-magnitude rarity. A result applies only to its named P/Q/E;
    whether rigidity or algebraic degree predicts entry probability is a separate,
    held-out cross-n model under think-3b3s.
---
# H-012 — the premise, made falsifiable first

The strategy layer rests on a testable, regime-specific claim: under one named proposal
and quench, record components are much less likely than the modal component.
Rigidity alone does not imply a small attraction set, and changing the proposal or
quench changes the probability.
If the measured ratio is small for the baseline regime, scaling that same sampler
multiplies effort against a poor hitting probability.

The grounding is real but thin — Ellsworth’s 4-in-3,004 for `s(51)`, the 14 zero-gap
pairs in Trump’s packing, and the double-funnel precedent from energy-landscape science.
None of it is a measurement under this campaign’s declared `P/Q/E`, which is why this is
registered with an explicit kill criterion rather than assumed.

## Why it is placed this early

Because if it is wrong for the baseline, much of the argument against scaling that
baseline falls away.
The verdict is not currently a cheap query over H-011: H-011 stops at `n=10`, while this
hypothesis requires `n=11`, so the instrument must explicitly add and budget that cell.
A strategy that names the observation that would kill it is the kind worth having.

## What this campaign has already seen that bears on it

[exp-001](../series/series-000-smoke-and-calibration/experiments/exp-001-baseline-sweep.md)
is weak evidence for the premise: five independent seeds at `n = 11` all landed in a
narrow band `[3.9144, 3.9361]`, well short of Trump’s `3.8771`, with the band five times
narrower than the remaining gap.
That is consistent with a sampler repeatedly finding one score region, but it is one
budget and one versioned method, and it measures nothing about terminal-component
probabilities directly.
H-012 is the separate `P/Q/E` measurement.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
