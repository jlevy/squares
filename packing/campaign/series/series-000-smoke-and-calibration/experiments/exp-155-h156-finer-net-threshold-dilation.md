---
title: exp-155 — retained finer-net threshold certificate and dilation limit
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-155
  series: series-000
  title: Retained finer-net threshold certificate and dilation limit
  date: '2026-09-09'
  hypotheses: [H-156]
  tier: confirmatory
  subject:
    label: The frozen T-025 atom family on the 1440-step direction net, rescaled at its exact crossing
      shrink, followed by the sharpened rational dilation corollary
    engine: devtools.measure_threshold_net_refinement, devtools.decide_threshold_certificate and
      devtools.dilation_corollary
    assurance: verified
    method: exact-algebraic
    host_system: Project Python 3.14; measurement on two workers of a shared host; exact two-route replay
  instance: {axis: n, point: 11, role: target}
  method:
    control: The retained 720-step certificate with the same atoms, weights, crossing shrink and binding
      physical direction; its exact dilation-limit lower bound is 3.82534784591311198085...
    candidate: The retained 1440-step certificate, differing from the 720-step control only in the finer
      declared direction net; both coverage routes accept it at exact least charge one
    runs_per_condition: 1
    interleaved: false
    operator: Claude Fable measurement lane; retrospectively registered from the retained exact lane and
      T-026 proof packet without a new run
    entry_point: packing/devtools/dilation_corollary.py
    command: >-
      uv run --frozen --all-extras --group dev python -m devtools.dilation_corollary
      cases/n11_threshold_certificate/certificate-191-50-net720.json --source-name
      packing/cases/n11_threshold_certificate/certificate-191-50-net720.json
      --check-limit-record
      cases/n11_threshold_certificate/t-026-net720-dilation-limit-corollary.json && uv run
      --frozen --all-extras --group dev python -m devtools.dilation_corollary
      cases/n11_threshold_certificate/certificate-191-50-net1440.json --source-name
      packing/cases/n11_threshold_certificate/certificate-191-50-net1440.json
      --check-limit-record
      cases/n11_threshold_certificate/t-026-dilation-limit-corollary.json
    record: >-
      packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-a2-threshold-certificate-on-finer-nets.md
    commit: 7ccb679cc0827d10ee80e2cd1988c8a07d65dfdc
    budget: The retained measurement reports about 55 minutes across the multi-net sweep; the separate
      exact gates report their own wall times. This registry repair ran no target.
  results:
  - shape: determination
    role: outcome
    question: Does a frozen T-025 threshold certificate on a finer admitted net yield a proved lower
      bound strictly above 3.826?
    outcome: criterion_met
    checked_by: The 1440-step record has exact crossing shrink 249507/250000 and both complete coverage
      routes return least charge one after rescaling. The exact dilation corollary gives
      955000*sqrt(518400042893309449)/179696714646249 = 3.826447410572939744..., strictly above 3.826.
  - shape: determination
    role: mechanism
    question: Does the finer declared net improve the dilation limit relative to the matched 720-step
      control without relying on a different shrink or atom weighting?
    outcome: criterion_met
    checked_by: The two retained certificates have identical atoms, scaled weights, crossing shrink and
      binding physical direction. Halving the maximum half-gap tangent raises the exact lower bound from
      3.82534784591311198085... to 3.82644741057293974417....
  verdict:
    decision: accepted
    primary_criterion: A two-route verified threshold certificate and exact lower bound strictly above 3.826
    reason: T-026 proves the first disjunct of H-156 at V4. Its two finite decision
      methods supplied C4 at registration; the later mapped review of the complete
      self-contained claim supplies its current C5. Its exact conclusion is s(11) >=
      955000*sqrt(518400042893309449)/179696714646249.
  effort:
    timebox: Retrospective registration of one already completed bounded lane; no new target allowance
    wall_seconds: 6713.2
    stopped_by: criterion
---
# Exp155: Finer-Net Threshold Dilation Confirms H-156’s First Route

This experiment entry repairs the registry around a result already retained and merged
as T-026. It introduces no new calculation.
The source lane records the measurement, the two certificate files retain the exact
finite objects, and the T-026 proof packet proves the ordinary exact lower bound
`s(11) >= 955000*sqrt(518400042893309449)/179696714646249 =
3.826447410572939744...` at V4/C5. The C5 promotion comes from the later mapped review;
it does not change this experiment’s calculation or verdict.

The proof uses strict rational dilations and order completeness.
It does not establish the separate strict inequality `s(11) >
955000*sqrt(518400042893309449)/179696714646249`; this does not qualify the proved lower
bound.

The accepted statement is the disjunction registered by H-156: one of its two proposed
routes produces an unconditional result above `3.826`. The separate rows-complete loop
at `383/100`, re-optimisation at a finer net, and changed atom families remain open.
Those questions do not remain open because H-156 failed; they remain possible successor
routes after its first route succeeded.

The `6713.2` seconds above is the sum of the three reported measurement wall readings
and three reported gate wall readings.
It is an additive reported cost, not elapsed wall for one uninterrupted process and not
a fresh timing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
