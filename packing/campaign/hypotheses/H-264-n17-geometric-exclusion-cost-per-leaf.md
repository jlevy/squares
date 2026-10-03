---
title: H-264 — the cost of exact geometric exclusion per n17 occupancy leaf
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-264
  kind: open_question
  claim: >-
    On 10 to 20 closed-assignment D4 orbits drawn uniformly from the residue H-262
    leaves, at a cap U >= S*, what fraction does an exact geometric exclusion engine
    adapted from the n11 v9 pipeline exclude, at what producer and checker cost per
    leaf, and what total does that extrapolate to?
  lane: proof
  derived_from: [X-048]
  instrument: >-
    An adaptation of the n11 exclusion engine with an independent certificate checker,
    run on a uniform sample of the H-262 residue; built under BC-411
  instrument_ready: false
  regime: >-
    n=17; the cover selected by H-263 (or the H259 grid); cap U >= S*, so exclusions
    apply to every smaller side by the centred embedding; unresolved leaves retained as
    explicit outcomes
  instance: {axis: n, point: 17}
  priority: 2
  cost_estimate: At most 2 CPU-hours per sampled leaf, 20 to 40 CPU-hours in all
  prereqs: [H-262, H-263, think-j1uw, think-x4a6]
  replication: false
  registered: '2026-10-01'
  notes: >-
    Re-scopes think-11ma after the PR 265 route review. The earlier pilot "below the
    certified endpoint" at a candidate cap of 4.67 would cover only sides up to 4.67 and
    leave (4.67, S*) open; the n11 proof excludes every non-captured case at a cap above
    its endpoint. The n11 replay cost about 640 CPU-seconds per nonfield exclusion; n17
    has 136 pairs and 52 variables against 55 and 33. Affordability falsifier: fewer
    than half of the sampled leaves excluded within 2 CPU-hours each.
---
# H-264: What One Geometric Exclusion Costs

A census that cannot be priced cannot be planned.
This samples the residue uniformly, so the measured cost extrapolates, and works at a
cap above the endpoint, so every exclusion it makes is reusable in a final proof.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
