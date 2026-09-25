---
title: H-242 — what a rung-0 cell tree costs on angle boxes away from Trump's tilt
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-242
  kind: open_question
  claim: >-
    Whether the rung-0 fixed-angle cell tree, run unchanged on half-tangent boxes of the
    six-axis plus five-common-angle family that do not contain Trump's tilt, closes at a
    target of U with node counts small enough to tile rung 1 (H-112), and how the count
    grows with box width and with distance from Trump's tilt.
  lane: proof
  derived_from: [X-046]
  criterion:
    shape: record
    metric: >-
      Per box: closed or unresolved at a declared node and wall cap, node count, leaf
      counts and smallest certified margin from the independent reader, for about six
      boxes across the tilt range outside the transfer-closed strips, at two or three
      half-tangent widths each
    direction: >-
      A pricing question: it confirms nothing about s(11). Boxes that close in well
      under the 1.7e8 nodes rung 0 needed make rung 1 a tiling computation; boxes that
      fail to close at their caps, or whose counts grow steeply with width, make a
      stronger per-node relaxation the prerequisite. A box that yields a verified
      non-degenerate leaf below U would be a counterexample candidate to H-112 and is
      reported as such.
    threshold: 170000000
  instrument: >-
    packing/cases/trump11/fixed_angle_tree.py with an additive parameterized box preset
    (h236 unchanged) and the unchanged independent reader fixed_angle_tree_check.py
  instrument_ready: false
  regime: >-
    n=11; six squares at orientation 0, five at one common orientation in each declared
    half-tangent box; exact rational leaf certificates; target U
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: One overnight CPU run on about nine workers, after the preset is reviewed
  prereqs: [think-6b12]
  replication: false
  registered: '2026-09-24'
  notes: >-
    Rung 0 (H-236, exp-232) cost about 1.7e8 nodes on a box of half-tangent width
    2e-6 that contains Trump's pose, where side U is feasible and margins fall to
    6e-10. Boxes away from Trump's tilt have a positive margin, which this question
    measures before any stronger relaxation is built. It supersedes the first part of
    H-239's pricing for the one-parameter family.
---
# H-242: The Cost of Rung 1, Measured Before It Is Built

Rung 0 closed, but at a price: about $1.7\times10^8$ nodes for one angle box of width
$2\times10^{-6}$. That box contains Trump’s packing, where the side $U$ is exactly
feasible, so the tree had to resolve margins down to $6\times10^{-10}$. Every other box
of rung 1 sits away from Trump’s tilt, with a positive margin to $U$, and should be
cheaper by an amount nobody has measured.

This open question is that measurement.
Its answer decides whether H-112 is a compute job or needs a stronger bound per node
first.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
