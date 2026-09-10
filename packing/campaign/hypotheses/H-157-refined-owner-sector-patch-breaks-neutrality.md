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
    survivor weight 10, and two improve to 19/2, satisfying the registered upper bound
    79/8 more strongly. The maximum over all thirty-two sixteen-bin classes is exactly
    10. Independent review reproduced the saved table, eight-bin equivalence and
    singleton scan. The six neutral children retain the reported positive distance to
    their fixed targets; m1:J9/16 and m2:J6/16 intersect cores55/50, respectively, so
    those two distances are zero. The delivered distance helper violated its disjointness
    precondition. Its all-children reach identity and the conclusion that the mechanism
    is irrelevant are withdrawn; the survivor-weight rejection is unchanged.
    On the finite retained ray universe, 135 classes per mark read exactly10. A pose
    probe leaves10 at cores59/60. X026's local T1/T2 statements now name the patch-only
    residual domain. T2 gives survivor weight at least10 for any patch inside core59;
    equality also requires a common mark in the patch. A positive-area subpatch omitting
    both marks leaves43/4. The two isolated cores have contained unit parents, but no
    full eleven-parent packing or forced routing has been proved.
    These statements obstruct closing every retained class by patch-only point covers
    on that domain; they do not exclude gains in other classes or stronger domains.
    The sufficient global condition is that for every
    hypothetical physical packing there exists a valid owner selection whose residual
    family is excluded, and a packing carrying an unclosed label may admit another
    selection that is already excluded. Whether the neutral classes are ever forced is
    open. This lane measured deletions, not atoms, so H-155's conditional threshold
    line is untouched. Original target think-dm0f; later source review and corrections
    think-9zc9. A maintained guarded replay is required before reusing the distance
    producer; the delivered script is retained as historical evidence.
---
# H-157 — Sixteen Sectors, a Fatter Patch, and the 0.015 That Would Decide It

**Protocol clarification recorded before the target, September 10, 2026.** The original
criterion required success for every refined subclass; its aggregate metric is therefore
the **maximum** survivor weight.
The earlier “minimum” was an error.
The later outcome and independent source corrections are recorded below.

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
This was one proposed comparison in the corrected
[X-026](../explorations/X-026-what-conditioning-does-and-does-not-buy.md).
The original target is `think-dm0f`; the later source review is `think-9zc9`.

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

**Distance correction from the independent source review.** For the six neutral
children, the squared distance to their selected target core remains

```
d^2 = 75308842465387162009/335694834731568400000000      d = 0.014977891
```

The patches `m1:J9/16` and `m2:J6/16` instead intersect their original target cores55
and50, so their true distances to those cores are zero.
The original helper computed vertex-to-edge distance under a disjointness assumption
without first checking it.
The survivor screen correctly deletes those intersected cores.
Distance to a fixed original target and distance to the nearest remaining survivor are
different metrics.
The guaranteed wedge widens from `pi/4` to `3pi/8` and the patch grows
1.6165x to 1.6175x in area, contained in `Q_phi(m)` for every one of the 87 to 94
retained rays in its bin.
Two subclasses therefore improve; six do not.
The full compound reach assertion is not established by this calculation, and the
all-subclasses survivor criterion is rejected independently.

**Two local obstruction statements** are in
[X-026 §5.1](../explorations/X-026-what-conditioning-does-and-does-not-buy.md), stated
over the retained transported mass-eleven ceiling family and the screened endpoint
patch-only residual domain: **T1**, the intersection patch for any bin containing a
neutral ray in the declared finite retained universe leaves survivor weight ten; **T2**,
any guaranteed patch inside owner core `#59` leaves weight at least ten.
Equality in T2 also requires a common mark inside the patch.
A positive-area corner subpatch of core59 for its singleton class omits both marks and
leaves `43/4`, so containment in the owner alone does not give equality.

For a partition retaining the neutral ray or pose, these statements leave a class
unclosed by point covers on the stated relaxation.
They require new survivor admissibility if the residual domain is strengthened, and do
not decide gains in other classes.
They do not establish that the conditional strategy fails: that strategy needs one
closed owner selection per packing rather than every class closed, and owner labels and
valid selections can overlap.
X-026 escape 1 is therefore narrowed rather than closed, and whether the neutral classes
are ever *forced* stays open beside escape 2.

The conditional **threshold** line,
[`H-155`](H-155-conditional-threshold-cover-on-an-owner-class.md), is untouched: this
measurement read deletions, not atoms.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
