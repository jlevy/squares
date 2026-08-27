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
    A deterministic chunk-partition solver over imported Witness/v1 geometry: enumerate
    admissible bar/L/rectangle subsets whose members fit one angle modulo quarter turns,
    classify every internal contact as exact (residual <= 1e-9) or near (residual <=
    1e-3), and solve the resulting exact-cover/set-packing problem. Within the registered
    F <= 2 slice, evaluate every exact F, prefer a certificate within K <= 6, then
    minimize F, K, and maximum residual; zero-residual count ties follow a declared
    deterministic minimum-remaining-values traversal with candidates ordered by size,
    residual, and member key. Emit a replayable decomposition certificate or a typed
    no-partition, outside-budget, or search-limit reason. A later in-budget certificate
    proves existence after an earlier capped F slice, but its F/K minimality remains
    explicitly indeterminate. For an out-of-budget retained certificate, any capped F
    slice leaves both budget selection and F/K minimality indeterminate.
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
  prereqs: [imported record geometry corpus, frozen ChunkPartition/v1 contract, deterministic minimal-partition solver]
  replication: true
  registered: '2026-08-26'
  notes: >-
    This is the coverage prior for the whole stratified-enumeration design: a grammar
    that cannot express the records it is meant to rediscover has no budget claim. It is
    deliberately measurable from retained geometry with no search, so it can refute the
    ansatz before any enumerator is built. Exp-037 measures six numerical angle classes
    in the retained n=29 serialization. That constrains fitted-angle count A, not chunk
    count K; n=29 remains a declared stress point, but the measurement does not justify
    K=6. A failure is informative in a specific way: the identity of the
    non-expressible records prices exactly which grammar moves are missing.
    Chunk-expressibility is a statement about serialized geometry under a tolerance,
    never about formal feasibility or optimality.
    Adjacency is deliberately two-band because records mix both kinds: some chunks are
    exactly flush and some are only clumped close, and a single tolerance would either
    merge genuinely separate groups or shatter real ones. Free squares are permitted for
    the same reason, since a record may seat most of its squares in groups and leave one
    or two loose; their count is reported rather than absorbed into trivial one-square
    chunks. Review amendment 2026-08-26: the n=1..100 corpus was inspected while the
    detector contract was being repaired, so it is calibration-only. This hypothesis
    remains undisposed; a prospective confirmatory successor must freeze an unseen
    corpus after the partition instrument and grammar freeze.
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
That measurement constrains angle-class count `A`, not chunk count `K`. It makes
`n = 29` a necessary stress case but does not justify the six-chunk threshold.

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

## Instrument status after the PR review

The first 1–100 census is descriptive calibration, not this hypothesis’s round.
Its maximal-component view can issue sound certificates for the decompositions it
reports, but a non-certificate cannot establish non-expressibility: a connected
irregular polyomino may split into several allowed chunks.
The bounded exact-cover splitter now handles such lattice splits and certifies every
grid-derived case and 3 of 36 non-grid records within the proposed budget.
Two non-grid records are conclusively outside that budget, 23 have no partition in the
implemented candidate universe, and eight are search-capped and therefore indeterminate.
This argues against rigid lattice chunks as the whole grammar, but it is not a verdict:
angle-class splits and sliding contact assemblies remain outside the instrument.

Because the corpus was inspected while repairing that contract, no W6 verdict will be
issued on H-044 from `n = 1..100`. A later confirmatory successor must freeze an unseen
corpus after the partition contract and grammar are committed.

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
