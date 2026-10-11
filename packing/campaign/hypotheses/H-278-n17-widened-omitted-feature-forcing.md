---
title: H-278 — exact omitted-feature forcing in the widened n17 tube
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-278
  kind: hypothesis
  claim: >-
    Across the accepted exp237 root inclusion interval and all eight vertices of
    B_W', the 19 retained pair distances are at most 4/3 and every one of the 125
    omitted options has a fixed witness-corner nominal gap at most -11/200.
    These finite exact checks support the stated hand-derived uniform forcing
    bound -71/21000 for position radius 1/100 and half-angle radius 1/200.
  lane: proof
  derived_from: [X-048]
  criterion:
    shape: determination
    metric: complete_exact_widened_feature_bounds_and_fresh_receipt_replay
    direction: criterion_met
    threshold: All 152 distance and 1000 fixed-corner bounds pass with frozen constants and complete identities; fresh replay agrees.
  instrument: >-
    packing/devtools/check_n17_widened_features.py; independent tuple-interval
    geometry reconstruction and accepted-root certificate recheck. Astra's
    convexity and Lipschitz bridge is recorded separately in
    docs/project/research/research-2026-10-07-n17-proof-interfaces-and-lp-contract.md.
  instrument_ready: true
  regime: >-
    n17 accepted root inclusion_bounds from exp237, not its original search box;
    B_W'=[0,1/4] x [-1/2500,1/12] x [-1/8,1/16]. Position radius1/100;
    |q_i|<=1/200 implies |delta_i|<=1/100. All19 retained pairs,125 omitted
    options,eight closed slider vertices. Exact rational outward arithmetic,
    layout enclosure at2^-256; frozen sqrt2 upper99/70. No target LP solve.
  instance: {axis: n, point: 17}
  priority: 1
  cost_estimate: At most180 seconds for generation and fresh independent receipt replay combined.
  prereqs: [H-255, H-256, H-257]
  replication: false
  registered: '2026-10-07'
  notes: >-
    Conditional feature forcing only. The finite interval checks are machine
    checked; extending the vertex/corner bounds uniformly uses the sole Astra
    hand derivation, with its assurance stated separately. This does not prove
    outer capture, larger slider coverage, or a widened side lower bound.
    Source and criterion are frozen before target evaluation. Any missing
    identity, altered constant, failed bound, root/control failure or replay
    disagreement refuses acceptance. No retuning after seeing results.
---
# H-278: Exact Widened Feature Forcing

Astra selected the fixed constants and mathematical bridge before target evaluation.
The instrument reconstructs the root-dependent nominal geometry and all slider vertices,
then checks a fixed corner that upper-bounds each omitted support gap.
The corner need not remain the minimizing corner after rotation.

The finite receipt and the uniform hand argument have distinct assurance scopes.
A successful check would remove an omitted-feature ambiguity inside the declared tube.
The outer capture and slider-domain obligations remain open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
