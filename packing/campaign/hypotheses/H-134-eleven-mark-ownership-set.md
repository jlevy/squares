---
title: H-134 — a robust unavoidable set of at most eleven marks exists at 96/25
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-134
  kind: hypothesis
  claim: >-
    There is a set of at most eleven marks (points or short segments, thickened by the
    transfer tolerance 0.006) in the container of side 96/25 such that every contained
    unit square at any angle meets one of them, with every nonavoidance region proved by
    Stromquist's Lemmas 1–4 as repaired or by an interval reader.
  lane: proof
  derived_from: [X-021]
  strategy_refs: ['proof:9', 'proof:10']
  criterion:
    shape: determination
    metric: a verified cover of the container by nonavoidance regions for a set of at most eleven marks
    direction: exists; any contained unit square avoiding all marks refutes a candidate set
    threshold: 11
  instrument: >-
    T-018's ninety-three heaviest atoms as candidate marks; the exp-121 escape instrument
    as the falsifier engine; sqpack.cover and H-106-style polynomial guards for the mesh
    checks.
  instrument_ready: true
  regime: >-
    n = 11, side 96/25, closed unit squares at all angles, marks thickened by 0.006 so
    the statement transfers robustly from the unknown minimal side
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: one session of four hours; a probe with a prior of about thirty per cent, not a proof plan
  prereqs: [T-018 atom skeleton, exp-121 escape instrument]
  replication: true
  registered: '2026-09-08'
  notes: >-
    X-021's single most valuable lemma: with every square localised to within about one
    of a known mark, route (a)'s tree collapses from about 10^40 feature selections to
    about 2^20 exact fixed-angle LPs. The evidence against getting it cheaply is that the
    weighted certificate at 3.81 needs 1121 atoms of mass 10.86 where an integral set
    would need at most eleven marks of mass one, and that exp-121 found escapes at 3.878.
---
# H-134 — Ownership at the Target Side

Stromquist proved `s(10)` by making ten points unavoidable and then owning them: with as
many points as boxes, every box holds exactly one, and alternative covers force
containments. [X-021](../explorations/X-021-what-can-be-proved-about-eleven-squares.md)
shows the ten-point scheme is rigid at `2 + 4/√5` and that its weighted analogue owns
only atoms heavier than the mass gap; an integral set of at most eleven marks at `96/25`
would restore the whole mechanism at the target side.

The lane is a probe, and its negative form — the catalogue of escapes from every set
built on the atom skeleton — is itself the obstruction the closing route needs to know.
[Agenda 030](../agendas/agenda-030-parallel-structural-lanes-at-n11.md) owns it in
BC-302.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
