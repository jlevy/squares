---
title: H-047 — do chunk-regular predecessors recover the solutions they were rounded from?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-047
  kind: hypothesis
  claim: >-
    For at least 70 percent of imported poses at n <= 30, rounding each detected chunk to
    a regularized predecessor - exact intra-chunk lattice contacts and the chunk angle
    snapped to its fitted class value - and then re-running the built class-bracketing
    quench from that predecessor returns a pose whose side is within 1e-6 of the source
    pose's side, and does so for record and non-record source poses alike.
  lane: search
  derived_from: [X-003]
  strategy_refs: ['search:12', 'search:17', 'search:20']
  criterion:
    shape: paired
    metric: >-
      fraction of source poses whose regularized predecessor re-quenches to within 1e-6
      of the source side, reported separately for record and non-record sources
    direction: at least 0.70 overall, with the record and non-record rates reported apart
    threshold: 0.7
  instrument: >-
    The chunk-decomposition detector, a regularizer that snaps intra-chunk contacts to
    exact and chunk angles to their fitted class value, and the built cell-read
    class-bracketing quench, with source and returned sides retained per pose.
  instrument_ready: false
  regime: >-
    numerical f64 LP under the measured 1e-11 solver floor; imported record geometry
    plus retained non-record quench endpoints from series-000; declared rounding
    tolerances
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11, 17, 18, 19, 28, 29]}
  priority: 2
  cost_estimate: tier S; one quench per source pose, seconds of wall time per pose
  prereqs: [imported record geometry corpus, chunk-decomposition detector]
  replication: true
  registered: '2026-08-26'
  notes: >-
    This is the round that tests whether a chunk decomposition is a usable coordinate
    system rather than only a description. If regularizing and re-quenching returns to
    the source, the predecessor is a faithful compressed representation of the pose and
    the enumerator can search over predecessors instead of over configurations. If it
    does not, the decomposition is losing information the packing needs, and the failing
    poses name what. Non-record sources are included deliberately: a representation that
    works only on records would be fitted to twenty or so examples, and the retained
    series-000 endpoints supply the average solutions that test it more honestly. A
    return within tolerance is a numerical statement about one refiner from one start;
    it is not a basin, component, or attraction claim, and D-052 still applies to every
    stopped quench.
---
# H-047 — the predecessor as a coordinate system

A chunk decomposition is only worth building a search on if it is **invertible enough**:
if rounding a pose to its regular predecessor and letting the refiner run returns the
pose, the predecessor carries the information the packing needs, and the combinatorial
geometry of chunks is a legitimate coordinate system for search.
If the round trip fails, the decomposition is a picture rather than a representation.

The round trip is three steps: detect the chunks, **regularize** by snapping intra-chunk
contacts to exact and each chunk’s angle to its fitted class value, then re-run the
built class-bracketing quench from that regularized start and compare the returned side
to the source.

## Why non-record sources are in the sweep

Records are roughly twenty poses at `n <= 30`, which is few enough that a representation
tuned on them would be fitted rather than tested.
The campaign has retained non-record quench endpoints from `series-000`, and those are
the average solutions a search will actually spend its time among.
Reporting the record and non-record rates separately is part of the criterion, because a
representation that works only on the exceptional cases would be exactly the wrong thing
to build a proposer on.

## What it would license

A confirmed round trip makes the predecessor the natural search object: enumerate
predecessors, quench each, and treat the returned pose as the realization.
That is the step that turns [H-045](H-045-chunk-grammar-rediscovery.md)’s enumeration
from a list of hypotheses into a parameterization of the space.
A refutation is equally directional, because the poses that fail to return name the
degrees of freedom the chunk description throws away.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
