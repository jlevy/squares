---
title: H-111 — resource and anchor exclusions on a complete pose cover
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-111
  kind: open_question
  claim: >-
    At side 96/25, can a complete coarse pose cover, separate certified resource
    budgets, and one or two boundary anchors exclude eleven unit squares, or close
    a nontrivial continuous anchor domain that the same geometric relaxation without
    resource rows leaves unresolved?
  lane: proof
  derived_from: [X-017]
  instrument: >-
    Proposed geometry-bound capacity-one cells, uniform resource minima, exact
    conflicts and residual-ten or residual-nine certificates, composed through a
    complete case DAG. Freeze the pilot domain and comparison before measurement.
  instrument_ready: false
  regime: >-
    n=11, side 96/25, all actual orientations and centers in the declared domain;
    every measure has its own budget; atomic witnesses are strictly interior and
    full-square measures require boundary nullity
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: first price one complete anchor domain in slices of at most 30 minutes
  prereqs: [reviewed resource and anchor implications, geometry-bound case and certificate controls]
  replication: false
  registered: '2026-09-07'
  notes: >-
    This new whole-pose resource model does not inherit BC-248's near-tight-census
    prerequisite. Those guards remain unchanged for that older global-residue tree.
    A narrower prospective claim must freeze the domain, resources, metric and stop
    rule before its first target run.
---
# H-111 — Resource and Anchor Exclusions

[X-017](../explorations/X-017-compatibility-and-complete-case-covers.md#a-resources-and-boundary-anchors-the-principal-global-bound-pilot)
gives the mechanism and its relationship to H-103.
[Agenda 027](../agendas/agenda-027-compatibility-and-restricted-families.md) owns the
proposed pilot; no experiment is registered or executed by this question.

The anchor-box residual domain is a union over all anchors in the box, or a proved
superset. A midpoint anchor does not represent that domain.
Resource minima must hold uniformly, and all angle cells in a capacity-one tile share
its single occupancy budget.
Pair or subsystem conflicts require uniform exclusion.

Mixed-size frame relaxations may be added after angular localization is proved.
Keep frame squares full size; report the residual core loss.
A feasible relaxed configuration does not establish a common full-size completion.

Compare the same frozen geometry with and without resources.
Retain closed domains, exact certificates, open remainder, and measured work.
A partial cover or a timeout leaves the global question open.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
