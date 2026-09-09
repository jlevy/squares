---
title: H-141 — four-owner endpoint footprints improve the matched finite covering objective
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-141
  kind: hypothesis
  claim: >-
    On the declared independent 369-site support and nine reflected directions at
    side 96/25, all four numerical covering arms converge and the four-owner
    owned-point objective exceeds the endpoint-footprint objective by more than
    0.001.
  lane: proof
  derived_from: []
  criterion:
    shape: determination
    metric: M_point minus M_endpoint, with all four arms converged
    direction: greater than 0.001
    threshold: 0.001
  instrument: >-
    packing/devtools/run_owner_footprint_cover.py --owner-count 4, with exact
    vertical decomposition, independent singleton site variables, and exact rational
    event-geometry fallback
  instrument_ready: true
  regime: >-
    Container 96/25 and core side 9977/10000; four physically compatible reflected
    m1, sector-0 corner classes; one 19-by-19 grid with inset 1/2 plus the mark's full
    D4 orbit, giving 369 available independent singleton variables; the nine canonical
    orientations whose folded sources are 0,45,90,135,180 or their reflections. One
    numerical row-generation run per unrestricted, point, triangle, and endpoint arm,
    with 120-second cooperative deadlines, 300 rounds, and twelve rows per direction.
    Every footprint is derived from the full 361-orientation owner manifest.
  instance:
    axis: n
    point: 11
  priority: 1
  cost_estimate: >-
    Four sequential 120-second arms in one process, with a ten-minute external timeout
    and two-second TERM grace. No target retry, alternate support, owner branch, or
    parameter tuning in this round.
  prereqs:
  - exact multi-footprint decomposition, containment, SAT, event-cell, and thin-cell controls
  - prospective exp-143 with the instrument source committed and pushed before launch
  replication: false
  registered: '2026-09-09'
  notes: >-
    This finite-support, finite-direction numerical screen narrows H-111's general
    resource-and-anchor question to one compatible four-owner branch. Endpoint mass
    below seven and M0 minus M_endpoint minus 4 are secondary diagnostics. Acceptance
    is not an exact optimum-gap theorem, an all-direction cover, a universal
    four-owner result, or a conditional packing certificate. A completed gain at most
    0.001 rejects this numerical claim. A timeout, guard refusal, separator failure,
    point-extension guard failure, or incomplete arm leaves it unresolved.
---
# H-141 — Matched Four-Owner Footprint Gain

[H-111](H-111-resource-anchor-case-exclusion.md) asks whether complete owner domains and
resource accounting can exclude Realm 4 at `n = 11`. This hypothesis tests one narrower
mechanism: whether replacing four bare corner marks with the union of their complete
endpoint footprints lowers a matched finite covering objective by more than `0.001`.

The four owners are the reflected `m1`, sector-0 classes at the container corners.
Their axis-aligned unit parents form an exact compatible configuration, so the
four-owner part is realizable.
This does not assert that seven additional squares fit.
The residual centre domain is decomposed outside the union of four closed Minkowski
collision polygons without filling legal gaps.
The unrestricted, owned-point, triangle, and endpoint arms use the same original site
availability and the same nine residual directions.
Each site has its own variable.
Sites in an arm’s closed footprint union are removed once.

All four arms must converge before the primary difference is read.
Endpoint mass below seven and `M0 − M_endpoint − 4` describe conditional-cover scope but
cannot replace the primary criterion.
The numerical result does not cover other owner branches, omitted directions, or exact
coverage.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
