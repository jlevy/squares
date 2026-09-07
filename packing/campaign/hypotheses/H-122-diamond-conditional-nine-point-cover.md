---
title: H-122 — nine points cover squares disjoint from the forced diamond
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-122
  kind: hypothesis
  claim: >-
    At q=1939/500, every contained closed unit square whose orientation modulo
    a quarter turn lies within pi/720 of either0 or pi/4, and which is disjoint
    from the fixed diamond D defined below, contains at least one of the nine
    unchanged Stromquist marks B through J.
  lane: proof
  derived_from: [X-016]
  strategy_refs: ['proof:9', 'proof:10', 'proof:15']
  criterion:
    shape: determination
    metric: complete both-band nine-point coverage conditional on closed disjointness from D
    direction: >-
      Accept only a complete independently checked proof over both full angle
      bands and every admissible center and boundary stratum. Reject only one
      independently verified contained closed unit square in an actual allowed
      band, disjoint from D and strictly avoiding all nine unchanged marks.
      Finite angle samples without an escape, failed sufficient guards, missing
      cases, errors and timeouts leave the continuous claim unresolved.
    threshold: every admissible D-avoiding square contains at least one of B through J
  instrument: >-
    First a bounded exact fixed-frame event-cell falsifier with strict diamond
    separating axes and an independently reconstructed corner/SAT witness reader.
    A complete continuous-angle producer is not yet available.
  instrument_ready: true
  regime: Fixed q, diamond, marks and both full closed angle bands; no obstacle enlargement or mark movement after a result.
  instance: {axis: n, point: 11}
  priority: 1
  cost_estimate: Parallel twenty-minute source-free authors, ten-minute independent reviews, then prospectively capped fixed-frame screen and witness replay.
  prereqs: [source-free controls and independent review, committed prospective screen or proof protocol, actual-angle witness validation]
  replication: false
  registered: '2026-09-07'
---
# H-122 — Cover Outside a Forced Diamond

H-122 is refuted by
[exp-122](../series/series-000-smoke-and-calibration/experiments/exp-122-diamond-conditional-cover-screen.md).
One square at the first prescribed near-axis frame strictly avoids all nine marks and
the closed diamond, independently checked in 0.20 seconds combined process wall time.
This rules out the sufficient diamond cover, not full-square compatibility or H-036. The
unused frames were not run, and no retry is allocated.

The fixed-frame falsifier and source-distinct reader passed 24 source-free controls and
swapped independent reviews by 06:49:01 UTC on September 7, before registration.
That readiness supported counterexample search only, not a complete continuous proof.

Before any target invocation, this claim was temporarily called H-118 locally.
PR 107 landed additional H-118–H-121 records after the last upstream inventory, so it
was renamed H-122 before its first instrument commit or scientific invocation; its
mathematics did not change.

This was the selected BC-255 continuation under `think-jbw5` after H-110 established
that the unchanged unconditional near-axis P12 cover is false.
The separate
[conditional assessment](../series/series-000-smoke-and-calibration/results/agenda-026/bc-255-conditional-compatibility-assessment.md)
proves the fixed-obstacle lemma and counting reduction.
It does not establish this covering hypothesis.

## Fixed Domain and Data

Let `q=1939/500`, `W=q/2-1=939/1000`, `b=q-3=439/500` and `kappa=49/50`. The closed
diamond is

$$
D=\{(1+X,b+Y):0\le X\le W,\quad
|Y|\le\kappa\min(X,W-X)\}.
$$

Its vertices are `(1,b)`, `(1+W/2,b+kappa W/2)`, `(1+W,b)` and `(1+W/2,b-kappa W/2)`.
Boundary contact is intersection, not disjointness.
The nine marked points retain their source coordinates:

$$
\begin{aligned}
B&=(q-1,1),& C_0&=(q-4/5,q/2),& D_0&=(q-1,q-1),\\
E&=(q/2,q-4/5),&F&=(1,q-1),&G&=(4/5,q-2),\\
H&=(17/10,11/5),&I&=(11/5,11/5),&J&=(11/5,17/10).
\end{aligned}
$$

The point called D in the source inventory is written D0 here to distinguish it from the
diamond; the machine inventory retains the original label `D`. No point is scaled or
symmetrized independently of its source formula.

The angle domain is the union of the closed bands `[-pi/720,pi/720]` and
`[pi/4-pi/720,pi/4+pi/720]`, modulo square quarter turns.
The entire closed square must lie in `[0,q]^2`. An independent counterexample check must
establish these actual conditions, not just membership in a numerical enclosure.

## Why the Conditional Statement Is Useful

The reviewed reduction proves that a near-45 square containing A1 and A2 contains D.
Strict-sublevel enlargement gives eleven pairwise-disjoint closed unit cores, so a
distinguished core containing D excludes that whole obstacle from every other core.
Nine marks cannot then cover ten remaining cores.
At registration, this hypothesis together with H-106, H-109 and a localization lemma
would have proved H-036. H-123 has since supplied localization, but exp-122 refuted this
cover. No uniform clearance radius is needed in the reduction, and H-108 is not one of
its premises.

This is only a sufficient cover.
A square may avoid D while overlapping every actual distinguished square allowed by the
stronger premises. A refutation here leaves full-square compatibility, H-036 and the
global packing bound unresolved.

## First Instrument, Not a Complete Proof

The source-free author slice prepares a fixed-frame event-cell screen and independent
witness reader. The proposed first screen examines half-angle offsets `+/-1/500` about
each of 0 and `pi/4`; these are four samples, not a replacement for the full claim.
Their exact order and process caps belong in a committed prospective experiment before
any scientific invocation.

The screen may reject this hypothesis through one valid counterexample.
No-witness output cannot accept it, even if all four sampled center domains were
completely enumerated.
The exact 0-degree and 45-degree special cases already follow from H-104’s accepted P12
cover and A1, A2, A3 lying in D; do not rerun them as new scientific work.

Controls must exercise generic unrelated inputs: both sine signs and exact unit frames,
positive and zero separating gaps, boundary-only and open event strata, a true escape,
malformed or incomplete witness refusal and exact field identity.
Scientific constructors remain forbidden until the prospective target protocol passes
its own launch guards.
Root owns scientific disposition; the producer and witness reader have independent
geometric implementations.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
