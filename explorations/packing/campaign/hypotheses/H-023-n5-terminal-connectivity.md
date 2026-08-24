---
title: H-023 — are the observed n = 5 endpoints in one terminal family?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-023
  kind: open_question
  claim: >-
    Which of the observed n = 5 polished endpoints are connected by feasible paths at
    the same optimum side, and which represent distinct terminal components?
  lane: search
  derived_from: [X-001]
  strategy_refs: ['search:12', 'search:18']
  instrument: >-
    Retained poses, full active-system rank and feasible tangent analysis, followed by
    bidirectional continuation at fixed objective and independent validity checks.
  instrument_ready: false
  regime: proved n = 5 optimum; no identity conclusion from side/contact summaries alone
  instance: {axis: n, point: 5}
  priority: 1
  cost_estimate: focused local geometry experiment before the n <= 10 census
  prereqs: []
  replication: true
  registered: '2026-08-24'
  notes: >-
    Six endpoints from six converged proposals show non-saturation, not its cause. This
    question discriminates true component diversity, positive-dimensional families,
    classification instability, and incomplete local termination.
---
# H-023 — resolve the first ambiguous census cell

The `n = 5` sample is the earliest place where endpoint keys, matching side/contact
summaries, and geometric interpretation disagree.
Calling it either a rich landscape or one flat family before continuation would repeat
the same soundness error in opposite directions.

This is the focused control for H-021 and the practical precursor to H-011.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
