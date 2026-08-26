---
title: H-044 — are standing records expressible as few aligned chunks plus few rotating chunks?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-044
  kind: hypothesis
  claim: >-
    At least 80 percent of standing-record poses at n <= 30 with public full geometry at
    the preregistered corpus freeze are chunk-expressible at K <= 6: their squares
    partition into at most six groups, each group sharing one fitted angle modulo
    quarter turns within 1e-6 radians and realizing a bar, L, or rectangle lattice
    skeleton whose internal contacts all fall within the declared near-adjacency band,
    with at most two groups off the container frame angle and at most two squares left
    ungrouped.
  lane: search
  derived_from: [X-003]
  strategy_refs: ['search:1', 'search:3', 'search:5', 'search:17']
  criterion:
    shape: conditions
    metric: >-
      fraction of frozen-corpus records admitting a K <= 6 chunk decomposition with at
      most two free squares under the declared exact and near adjacency bands
    direction: at least 0.80
    threshold: 0.8
  instrument: >-
    A chunk-decomposition detector over imported Witness/v1 geometry: fit angle classes,
    test each class for a bar/L/rectangle lattice skeleton under a two-band adjacency
    rule, classify every internal contact as exact (residual <= 1e-9) or near (residual
    <= 1e-3), permit ungrouped free squares, and emit the minimal K, the free-square
    count, the per-contact band, and either a decomposition certificate or a typed
    non-expressible reason.
  instrument_ready: false
  regime: >-
    frozen public-geometry corpus from the archived record catalogue; the criterion is
    scored on n <= 30, and the declared sweep extends through n <= 100 as imported
    geometry becomes available; numerical decomposition under declared tolerances, never
    a formal feasibility claim
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11, 17, 18, 19, 26, 27, 28, 29, 37, 39, 40, 41, 50, 51, 54, 68, 69, 70, 83, 87, 88]}
  priority: 1
  cost_estimate: >-
    tier S; one corpus pass over archived geometry with no search, comparable to the
    exp-012 and exp-037 reconstruction rounds
  prereqs: [imported record geometry corpus, chunk-decomposition detector over imported geometry]
  replication: true
  registered: '2026-08-26'
  notes: >-
    This is the coverage prior for the whole stratified-enumeration design: a grammar
    that cannot express the records it is meant to rediscover has no budget claim. It is
    deliberately measurable from retained geometry with no search, so it can refute the
    ansatz before any enumerator is built. Exp-037 already measures six numerical angle
    classes in the retained n=29 serialization, which is why K is set at six rather than
    three and why n=29 is a declared sweep point rather than an assumed pass. A failure
    is informative in a specific way: the identity of the non-expressible records prices
    exactly which grammar moves are missing. Chunk-expressibility is a statement about
    serialized geometry under a tolerance, never about formal feasibility or optimality.
    Adjacency is deliberately two-band because records mix both kinds: some chunks are
    exactly flush and some are only clumped close, and a single tolerance would either
    merge genuinely separate groups or shatter real ones. Free squares are permitted for
    the same reason, since a record may seat most of its squares in groups and leave one
    or two loose; their count is reported rather than absorbed into trivial one-square
    chunks.
---
# H-044 — the coverage prior for chunk enumeration

The stratified-enumeration design in
[X-003](../explorations/X-003-stratified-chunk-enumeration.md) restricts search to
packings assembled from a small number of chunks: groups of squares sharing one angle
and sitting in a bar, L, or rectangle skeleton.
Every claim that design can make about coverage, saturation, or restricted-class
optimality rests on records actually having that shape.

Two records are known instances.
Trump’s `n = 11` packing is one corner square, one mirrored against the opposite side,
one offset along the top, an L-shaped block of three, and one five-square group tilted
as a rigid unit. Bidwell’s `n = 17` record is an aligned frame plus two tilted groups.

One record is a known stress.
[Exp-037](../series/series-000-smoke-and-calibration/experiments/exp-037-h-042-n29-numerical-angle-classes.md)
measures six numerical angle classes in the retained `n = 29` serialization, with a
minimum class gap of `0.296067` degrees.
Six classes is the reason `K` is set at six and the reason a pass at `n = 29` is not
assumed.

## Exact Chunks, Near Chunks, and Free Squares

The detector uses two adjacency bands rather than one.
A contact is **exact** when its residual is at most `1e-9` and **near** when it is at
most `1e-3`; both count toward a skeleton, and every reported decomposition records
which band each internal contact fell in.
One tolerance cannot serve both cases: set tight, it shatters the loosely clumped groups
records genuinely contain; set loose, it merges groups the geometry keeps apart.

**Free squares are allowed and counted.** A record may seat most of its squares in
groups and leave one or two loose, so the criterion permits at most two ungrouped
singletons and reports the count.
A decomposition needing many free squares is a weak decomposition, and saying so
requires counting them rather than hiding them in trivial one-square chunks.

## What a failure buys

A refutation is not a dead end, because the failing records name the missing grammar
move. Records that fail only on the skeleton test but pass the angle-class test call for
richer intra-chunk shapes; records that fail on class count call for a larger `K` and
price the outer search dimension directly.
Either outcome is a quantitative input to the enumerator’s design, which is why this
round is registered ahead of the instrument it will judge.

## Relation to H-025

[H-025](H-025-record-angle-compressibility.md) asks whether records can be *refitted* to
three angle classes at a bounded side cost, which permits changing the packing.
This hypothesis asks whether records *already are* chunk-structured as they stand, which
permits no reoptimization at all.
A record may satisfy either without the other, and the enumerator’s coverage claim
depends on this one.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
