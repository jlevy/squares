---
title: H-138 — where does the point-atom ceiling begin?
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-138
  kind: open_question
  claim: >-
    Two questions about the edge of the exact ceiling at 191/50. First: what is the least
    side L* in (61/16, 191/50] at which a depth-one family of weight at least eleven
    exists at B = 9977/10000 on the retained 181-direction net -- the side below which the
    point-atom method is not yet closed and above which it is? Second: does any such
    family at 191/50 keep maximum depth at most one when its shrink is raised toward
    998/1000, or does the ceiling belong to the retained shrink alone? For the rigid
    family the second answer is already no: clamped at 0.998 its exact maximum depth is
    7/4. The question is whether some other family survives the move, since the ceiling
    transfers downward in B and upward in L but not upward in B.
  lane: proof
  derived_from: [X-023]
  strategy_refs: ['proof:21', 'proof:22']
  instrument: >-
    devtools.independent_ceiling_reader decides any candidate family exactly, from the
    statement rather than from the module, at about 0.8 s per decision, so a bisection in
    L or in B is a matter of minutes once candidates exist;
    devtools.polish_ceiling_family produces the candidates by fixed-support polish with
    an exact dual bound, and devtools.run_fractional_cutting generates the support at a
    new side.
  instrument_ready: true
  regime: >-
    n = 11, sides in (61/16, 191/50], shrink 9977/10000 for the first question and up to
    998/1000 for the second, the retained net t_k = (207107/500000) k/180, k = 0..180;
    D4-symmetric families, weak duality against D4-symmetric measures
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: >-
    one session of two to three hours, dominated by generating candidate families rather
    than by deciding them
  prereqs: []
  replication: true
  registered: '2026-09-09'
  notes: >-
    The bracket at the start is 61/16 = 3.8125, where the best retained family carries
    20843712108/2067791663 = 10.0802 and the row loop stalled at 10.7179 without
    converging, and 191/50 = 3.82, where the exact family carries eleven. Whether 61/16 is
    also under a ceiling is the cheapest discriminating measurement lane E left open: if
    it is, the 5,700 seconds spent on its row completion are answered rather than merely
    unfinished. The second question is the one that decides whether the finer-net route of
    H-137 has room at 3.82 at all: the ceiling transfers to every smaller B and every
    larger L, so a family that holds at B near one would close 3.82 for every net
    containing its directions and every admissible shrink.
---
# H-138 — Where the Ceiling Starts, and What It Is Attached To

The exact depth-one family at `191/50` is a statement about a side, a shrink and a net,
not about a site set, and its edges are not known.
Downward in side it is bracketed by `61/16`, where the heaviest retained family carries
`10.08` and the covering loop stalled at `10.72` without converging; upward in shrink it
is not known to survive at all, since the family that proves it fails at `0.998` with an
exact maximum depth of `7/4`.

Both edges are cheap to probe and neither has been probed.
[X-023](../explorations/X-023-three-losses-and-a-new-atom.md) records the ceiling and
its transfer rules; the
[ceiling reader’s report](../series/series-000-smoke-and-calibration/results/agenda-032/ceiling-reader-191-50.md)
names the two bisections that would settle these questions and times a single decision
at under a second. This is registered as an open question rather than a hypothesis
because neither half has a predicted answer worth writing down: the first asks for a
number in an interval and the second asks whether a family exists at all.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
