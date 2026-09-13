---
title: H-210 — the blind physics never settles to a valid packing
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-210
  kind: hypothesis
  claim: >-
    No blind run of the workbench's physics ends on a valid packing. At every n and every
    parameter setting the squares come to rest overlapping, so every side it reports is a
    bounding box around an invalid arrangement rather than a container a packing needs.
  lane: search
  derived_from: [X-028]
  criterion:
    shape: determination
    metric: the deepest pairwise overlap in the final arrangement, by separating axis
    direction: above tolerance in every trial
    threshold: 0.00001
  instrument: packing/devtools/bench_annealing.py
  instrument_ready: true
  regime: >-
    the workbench's simulation in blind mode; the snapped mode is valid by construction and
    is the control that sets the tolerance
  instance: {axis: n, point: 11}
  sweep: {axis: n, points: [5, 10, 11, 17, 26, 29]}
  priority: 1
  cost_estimate: seconds
  registered: '2026-09-12'
---
# H-210 — the blind physics never settles to a valid packing

**The finding that reframed the epic, registered so the claim can be tested rather than
assumed.**

15,000 of 15,000 blind trials ended with squares overlapping -- at every n from 5 to 29,
at every shake level including zero, by 0.03 to 0.12 of a unit side.
Measured by a separating-axis test over the final poses, written independently of the
simulation, with its tolerance taken from a control rather than chosen: the SNAPPED
trajectory, which ends on the record’s own poses by construction, scores 5.5e-7 to
1.0e-6.

So the workbench’s physics does not settle to a packing on its own.
The animation looks right because its last frame is snapped onto the record; underneath,
contacts stay soft and the squares come to rest inside each other.

**Why the residual survives.** The correction phase pulls every pose onto its target
over the last part of the move -- and in blind mode there is no target, so nothing in
the schedule removes penetration.
The contact law is a spring: at equilibrium a spring balances the wall’s inward pressure
at a non-zero compression, and the run ends at that equilibrium rather than at
separation.

**What would refute this claim.** One blind run, at any n and any parameters, whose
deepest final overlap is under 1e-5. That is the same falsifier as H-209’s and a cheaper
one to check, which is why it is worth having both.

**What follows if it stands.** Every search result from this instrument is about
bounding boxes rather than packings, and the instrument needs a resolution phase -- a
final stage that pushes squares apart until no pair overlaps, and reports the container
that arrangement actually needs -- before any of its numbers are about packing at all.
That is a change to the method, not to its dials.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
