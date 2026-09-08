---
type: is
id: is-01m1v4dna6sja0srcttmpwb5hp
title: Correct weighted-overlap controls for BC-243
kind: bug
status: closed
priority: 0
version: 4
spec_path: packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md
labels:
  - release-blocker
  - mathematics
dependencies:
  - type: blocks
    target: is-01m1v2yhy02qmka8ez4d2f5bde
parent_id: is-01m1tvqp2v2js8437xek2xk2gz
created_at: 2026-09-06T10:32:28.741Z
updated_at: 2026-09-06T17:57:54.053Z
closed_at: 2026-09-06T10:43:40.508Z
close_reason: Integrated commit 7e5604cb narrows BC-243's Trump mutation to an exact unit-weight depth-greater-than-one refusal and adds the required positive two-placement weight-1/2 overlap control with summed a.e. depth at most one, consistently in the continuation and Agenda 026.
resolution: null
duplicate_of: null
---
The continuation addendum says an interior perturbation creating positive-area overlap must be rejected, but that is sound only for unit-weight Trump atoms: a weighted dual family may overlap while full-dimensional summed depth stays at most one. Before BC-243 opens, either pin the Trump overlap control to unit weights or require an exact mutated arrangement cell with a.e. depth above one, and add a positive fractional-overlap control whose summed depth remains at most one.
