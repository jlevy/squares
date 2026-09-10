---
title: H-157 — sixteen owner sectors fatten the patch enough to break neutrality
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-157
  kind: hypothesis
  claim: >-
    Refining the corner-owner angular bins from eight to sixteen makes every guaranteed
    patch reach at least 0.015 further than its eight-sector parent, so that at q = 96/25
    every refined subclass of the four neutral eight-sector classes (m1:j3, m1:j4, m2:j3,
    m2:j4) deletes strictly more than one unit from the transported mass-eleven ceiling
    family: exact survivor weight at most 79/8 = 9.875, strictly below the conditional
    requirement of 10. Neutrality is then a property of the eight-sector patches rather
    than of conditioning, and Step 3 of X-026's ladder no longer holds at sixteen
    sectors.
  lane: proof
  derived_from: [X-026]
  strategy_refs: ['proof:10', 'proof:22']
  criterion:
    shape: determination
    metric: >-
      the exact survivor weight of the mass-eleven ceiling family, transported to 96/25
      and screened against each refined sixteen-sector patch, maximised over the refined
      subclasses of the four neutral eight-sector classes. The reported 0.014978 gap
      motivates the test but is not an equivalent metric for arbitrary patch growth
    direction: >-
      Confirm the screened neutrality-break conclusion when every refined subclass
      has exact survivor weight below 10. Confirming the full compound claim also
      requires a separately defined and verified 0.015 geometric reach assertion.
      Refute when any refined subclass still has survivor weight exactly 10 under
      the declared nested patch construction. This rejects the
      all-subclasses claim for this family only; it does not defeat every global owner
      routing strategy or every changed residual domain. A failed or incomplete patch
      construction is unresolved, not the stated negative.
      A float reading of the separating gap decides neither
      direction, and a gain measured on any family other than the mass-eleven ceiling
      family decides nothing at all (D-489).
    threshold: 10
  instrument: >-
    devtools.owner_footprints builds the patches but hard-codes eight bins
    (owner_branch_manifest iterates range(8); triangle_footprint and endpoint_footprint
    reject sector >= 8), so the one missing piece is a bin-count parameter and the
    certified wedge geometry at the refined boundaries. Exact pi/8 unit directions
    are not rational; an algebraic representation or a sound rational enclosure needs
    its own containment proof and controls. Everything downstream
    exists and runs in seconds: devtools.transport_ceiling_family moves
    ceiling-family-191-50.json to 96/25, screen_footprint from
    devtools.screen_corner_dual_salvage does the deletion with the ownership line's own
    filter, and the lane X1 scripts (lane-x1-ceiling11-screen.py.txt, lane-x1-gap.py.txt)
    are the screen and the gap reader as run.
  instrument_ready: false
  regime: >-
    n = 11, side 96/25, shrink 9977/10000, the 361-direction doubled net; sixteen closed
    angular bins per mark and two marks per corner, so thirty-two classes per corner;
    certified exact arithmetic under the admitted rational-enclosure or algebraic
    representation, screened against the retained depth-one
    mass-eleven ceiling family
  instance: {axis: n, point: 11}
  priority: 2
  cost_estimate: >-
    under an hour: the bin-count parameter and its wedge vectors, then one screen of
    seconds per class over the eight refined subclasses that matter
  prereqs:
  - a bin-count parameter in devtools.owner_footprints, with certified refined wedge vectors and
    the containment argument restated at sixteen bins; specify exact algebraic directions
    or admitted rational enclosures rather than assuming rational pi/8 unit vectors
  replication: true
  registered: '2026-09-09'
  notes: >-
    REVIEW CORRECTION 2026-09-10 before any target run: this is one proposed change of
    endpoint patches, not the only possible exception to X1's measured neutrality.
    The criterion already required every refined subclass below ten, so its aggregate
    metric is the maximum survivor weight, correcting the earlier minimum. Exact
    survivor weights, not a floating separating gap or unspecific patch reach, decide
    that criterion. The claim's phrase reach 0.015 needs a precise geometric definition
    and verification before admission; it is not inferred merely from doubling bins.
    The recorded gap 0.014978 for a nearest weight 1/8 survivor motivates the proposed
    screen. A certified patch that intersects that survivor removes it, but a scalar
    expansion estimate alone does not prove such an intersection for every subclass.
    The refined wedge construction, nesting and exact direction representation need
    proof and controls before instrument_ready can become true. The quoted under-hour
    cost is a prior estimate, not a measured runtime. Confirmation would remove this
    particular source-family obstruction on the declared subclasses, not prove a cover.
    Refutation would retain an obstruction on at least one refined relaxation, not
    close the conditional method: a physical packing may admit another excluded valid
    selection. The unconditional cap near 3.868983 has no verified automatic conditional
    transfer. Stronger wall or unit-parent domains, joint compatibility and richer
    charges remain open independently of this test. No target was run and no outcome
    was changed. Tracked as think-dm0f; allocation requires fresh source admission.

---
# H-157 — Sixteen Sectors, a Fatter Patch, and the 0.015 That Would Decide It

**Unrun protocol clarified September 10, 2026.** The original criterion required success
for every refined subclass; its aggregate metric is therefore the **maximum** survivor
weight. The earlier “minimum” was an error.
No target result exists.

[Lane X1](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md)
measured neutrality for a particular fractional family and endpoint patches.
The proposed sixteen-bin refinement asks whether each refined subclass removes more of
that same family. With the retained weights in multiples of `1/8`, a survivor below ten
has weight at most `79/8`.

The reported gap `0.014978` to a nearest survivor motivates a geometric experiment.
It does not prove that doubling the bins makes every patch reach that core.
Before admission, define the claim’s geometric reach, prove the refined patch
containment and nesting, and specify exact algebraic directions or certified rational
enclosures. Exact unit directions at `pi/8` are not rational.
The under-hour cost remains an estimate pending that work.

A successful screen would remove this family’s point-cover obstruction on the named
subclasses; it would not construct a conditional cover.
An unsuccessful screen would leave a fixed-relaxation obstruction, without showing that
physical packings must route there or excluding stronger domains and charges.
This screen is one open hypothesis among the comparisons in the corrected
[X-026](../explorations/X-026-what-conditioning-does-and-does-not-buy.md).
It is carried as `think-dm0f`; instrument admission is still outstanding.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
