---
title: H-139 — owner endpoint footprint improves the matched finite covering objective
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-139
  kind: hypothesis
  claim: >-
    On the declared independent 369-site support and nine reflected directions at
    side 96/25, all four numerical covering arms converge and the owned-point
    objective exceeds the endpoint-footprint objective by more than 0.001.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: M_point minus M_endpoint, with all four arms converged
    direction: greater than 0.001
    threshold: 0.001
  instrument: >-
    packing/devtools/run_owner_footprint_cover.py with exact owner geometry,
    independent singleton site variables, and an exact rational event-geometry
    fallback
  instrument_ready: true
  regime: >-
    Container 96/25 and core side 9977/10000; bottom-left class m1, sector 0;
    one 19-by-19 grid with inset 1/2 plus the mark's full D4 orbit, giving 369
    available independent singleton variables; the nine canonical orientations
    whose folded sources are 0,45,90,135,180 or their reflections. One numerical
    row-generation run per unrestricted, point, triangle, and endpoint arm, with
    120-second cooperative deadlines, sixty rounds, and three rows per direction.
    Every footprint is derived from the full 361-orientation owner manifest.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: >-
    Four sequential 120-second arms in one process, with a ten-minute external
    timeout and two-second TERM grace. No target retry, alternate support, or
    parameter tuning in this round.
  prereqs:
  - fourteen focused owner-geometry and generic-runner controls
  - prospective exp-140 with the instrument source committed and pushed before launch
  replication: false
  registered: '2026-09-09'
  notes: >-
    This finite-support, finite-direction numerical screen narrows H-111's general
    resource-and-anchor question to one owner class and one fixed comparison. The
    triangle and endpoint increments and M0 minus M_endpoint minus 1 are secondary
    diagnostics. Acceptance is not an exact optimum-gap theorem, an all-direction
    cover, or a conditional packing certificate. A completed gain at most 0.001
    rejects this numerical claim. A timeout, guard refusal, separator failure, or
    incomplete arm leaves it unresolved.
---
# H-139 — Matched Owner-Footprint Gain

[H-111](H-111-resource-anchor-case-exclusion.md) asks whether complete owner domains and
resource accounting can exclude the open `n = 11` case at side `96/25`. This hypothesis
tests one narrower mechanism: whether replacing bare ownership of the bottom-left `m1`
mark in sector 0 with its full-net endpoint footprint lowers a matched finite covering
objective by more than `0.001`.

The unrestricted, owned-point, triangle, and endpoint arms use the same original site
availability and the same nine residual directions.
Each site has its own variable.
Sites inside an arm’s closed footprint are removed because no strictly disjoint residual
core can contain them.
The point, triangle, and endpoint footprints are built from the full 361-orientation
owner manifest before the nine numerical directions are selected.

All four arms must converge before the primary difference is read.
The triangle increment, endpoint increment, and `M0 − M_endpoint − 1` show where any
change occurs, but they cannot replace the primary criterion.
The numerical result does not cover omitted directions or supply exact coverage.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
