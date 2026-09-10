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
  instrument_ready: true
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
  - a bin-count parameter in devtools.owner_footprints, with certified refined wedge
    vectors and the containment argument restated at sixteen bins; exact algebraic
    directions or admitted rational enclosures rather than assumed rational pi/8 unit
    vectors -- satisfied 2026-09-10 in a scratch copy retained as
    agenda-034/lane-x4-nbins.py.txt. Sector boundaries at multiples of pi/8 are exact in
    Q[sqrt 2], so membership is an exact sign decision and no float enters a verdict; an
    eight-bin equivalence control against the tracked module reports zero disagreements
    on the membership predicate, on sector_endpoint_rays and on all sixteen
    endpoint_footprint polygons vertex for vertex. The tracked module still hard-codes
    eight bins; promoting the parameter into it is carried separately under OR-1
  replication: true
  registered: '2026-09-09'
  notes: >-
    REVIEW CORRECTION 2026-09-10, written before the target ran and still governing how
    its outcome reads: this is one proposed change of endpoint patches, not the only
    possible exception to X1's measured neutrality. The criterion already required every
    refined subclass below ten, so its aggregate metric is the maximum survivor weight,
    correcting the earlier minimum. Exact survivor weights, not a floating separating gap
    or unspecific patch reach, decide that criterion. The recorded gap 0.014978 for a
    nearest weight-1/8 survivor motivated the screen, but a scalar expansion estimate
    alone does not prove an intersection for every subclass. The quoted under-hour cost
    was a prior estimate, not a measured runtime. The unconditional cap near 3.868983 has
    no verified automatic conditional transfer. Stronger wall or unit-parent domains,
    joint compatibility and richer charges remain open independently of this test.
    REFUTED 2026-09-10 by exp-154, on exact survivor weights as the corrected criterion
    requires. Six of the eight refined subclasses of the four neutral classes read exact
    survivor weight 10, and the two that break read 19/2 rather than the predicted 79/8;
    the maximum over all thirty-two sixteen-bin classes is exactly 10. The mechanism is
    present and irrelevant: the wedge does widen from pi/4 to 3pi/8 and the patch does
    grow 1.6165x to 1.6175x in area, checked vertex for vertex, but the reach toward the
    critical survivor is the rational identity
    d^2 = 75308842465387162009/335694834731568400000000, bit-identical for the parent and
    both children at both marks, because the closest point of the patch to that core is
    the mark itself. The screen went one resolution further: at the singleton-ray limit
    135 classes per mark read exactly 10, and a pose probe leaves exactly 10 at two
    mark-clique members. Those are theorems T1 and T2 in X-026.
    What the refutation does and does not settle, in the terms this correction set out.
    It retains an obstruction on at least one refined relaxation at every angular
    resolution and at pose level, so patch refinement is closed as a lever. It does not
    close the conditional method: the sufficient global condition is that for every
    hypothetical physical packing there exists a valid owner selection whose residual
    family is excluded, and a packing carrying an unclosed label may admit another
    selection that is already excluded. Whether the neutral classes are ever forced is
    open, and is adjacent to X-026's emptiness escape rather than to any covering
    argument. This lane measured deletions, not atoms, so H-155's conditional threshold
    line is untouched. Tracked as think-dm0f.
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

## Outcome, 2026-09-10: refuted

Measured by
[`exp-154`](../series/series-000-smoke-and-calibration/experiments/exp-154-h157-sixteen-sector-refinement-limit.md),
and retained in full beside
[lane X4](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x4-sixteen-sectors-and-the-refinement-limit.md).

The registered direction refutes on one surviving class, and six survive.

| refined subclass | parent | survivor weight | deletion |
| --- | --- | --- | --- |
| `bottom-left:m1:J6/16` | `m1:j3` | **10** | 1 |
| `bottom-left:m1:J7/16` | `m1:j3` | **10** | 1 |
| `bottom-left:m1:J8/16` | `m1:j4` | **10** | 1 |
| `bottom-left:m1:J9/16` | `m1:j4` | `19/2` | `3/2` |
| `bottom-left:m2:J6/16` | `m2:j3` | `19/2` | `3/2` |
| `bottom-left:m2:J7/16` | `m2:j3` | **10** | 1 |
| `bottom-left:m2:J8/16` | `m2:j4` | **10** | 1 |
| `bottom-left:m2:J9/16` | `m2:j4` | **10** | 1 |

All exact, and the maximum over the full thirty-two-class sixteen-bin split is exactly
10, attained at six classes.

**The `0.015` was a gap to the mark, not to the patch.** The squared distance from the
patch to the nearest surviving core is

```
d^2 = 75308842465387162009/335694834731568400000000      d = 0.014977891
```

and it is bit-identical for the eight-sector parent and for both of its sixteen-sector
children, at both marks, because the minimising vertex is the mark itself.
Every patch at every bin count has the mark as a vertex, so no angular conditioning can
shorten that reach.
The proposed mechanism does happen — the guaranteed wedge widens from
`pi/4` to `3pi/8` and the patch grows 1.6165x to 1.6175x in area, contained in
`Q_phi(m)` for every one of the 87 to 94 retained rays in its bin — and it buys nothing.

**Two theorems came out of it**, and they are the durable result rather than the
refutation. Both are in
[X-026 §5.1](../explorations/X-026-what-conditioning-does-and-does-not-buy.md), stated
over the retained transported mass-eleven ceiling family and the screened endpoint
patches: **T1**, every closed angular bin containing one of the 135 neutral rays has
survivor weight exactly 10, at any bin count; and **T2**, the class containing the pose
of mark-clique member `#59` has survivor weight exactly 10 under any conditioning by
pose, at any refinement.

What they establish is that **patch refinement is ruled out as the lever**, at every
angular resolution and at pose level.
What they do not establish is that the conditional strategy fails: that strategy needs
one closed owner selection per packing rather than every class closed, and owner labels
and valid selections can overlap.
X-026 escape 1 is therefore narrowed rather than closed, and whether the neutral classes
are ever *forced* stays open beside escape 2.

The conditional **threshold** line,
[`H-155`](H-155-conditional-threshold-cover-on-an-owner-class.md), is untouched: this
measurement read deletions, not atoms.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
