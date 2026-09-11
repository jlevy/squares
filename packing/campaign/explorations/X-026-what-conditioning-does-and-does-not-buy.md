---
title: "X-026 — what conditioning does and does not buy: definitions, and a ladder of inference"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-026
  title: "What Conditioning Does and Does Not Buy: Definitions, and a Ladder of Inference"
  date: '2026-09-09'
  author: Claude coordinator (Fable), written after the agenda-034 lane X1 measurement returned
  campaign: packing.squares
  brief: >-
    The first summaries of agenda-034 lane X1 said "conditioning is refuted", which is
    stronger than what was measured. The owner asked for the argument stated in full,
    with every term defined before it is used, and for the exact point where the chain
    of inference stops to be marked. This report defines s(11), cores, certificates,
    threshold atoms, fractional packings and ceiling families, corner ownership and the
    conditional requirement; lists the seven facts the lane established with the status
    of each; sets out the six-step ladder from the mass-eleven ceiling family to the
    failure of point covers on a residual domain; and then says where the ladder stops.
    It stops at point covers: the survivor family violates the two-of-three inequalities
    it would have to satisfy to block a threshold certificate, so the blocking argument
    does not reach the richer language. Neutrality is an identity for the named
    fractional family and endpoint-patch relaxations, not a method-wide result.
    Revised after lane X4 and the independent PR139 source review: six refined
    subclasses retain ten, two improve to19/2, and the maximum remains ten. Two
    claimed positive distances were invalid because the polygons intersected. The
    local angular and pose statements in section5.1 retain their finite-universe and
    patch-only domain premises. An arbitrary guaranteed subpatch inside core59 gives survivor
    weight at least ten; equality also needs a common mark in the patch. A conditional
    proof needs an excluded valid selection per physical packing rather than every
    raw class closed. Stronger domains and routing remain open. Step6's transfer of
    the rank-one cap3.868983 is unverified, and unmatched cut maxima and an unmeasured
    class-cost estimate do not establish comparative productivity.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x4-sixteen-sectors-and-the-refinement-limit.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-t2-cap-and-next-cuts.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x2-owner-instrument-survey.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/ceiling-family-191-50.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-survivor-m1-j3.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-reader-survivor-m1-j3.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md
  - packing/campaign/explorations/X-024-two-lines-at-eleven.md
  - packing/campaign/hypotheses/H-155-conditional-threshold-cover-on-an-owner-class.md
  proposes: [H-157, H-158]
---
# X-026 — What Conditioning Does and Does Not Buy: Definitions, and a Ladder of Inference

Coordinator analysis, 2026-09-09, written after the measurement lane
([lane X1](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md))
returned.
Its purpose is to state the argument in full, with every term defined before it
is used, and to mark exactly where the chain of inference stops.
It exists because the first summaries of that lane said “conditioning is refuted”, which
is stronger than what was measured.

**Review correction, September 10, 2026.** The earlier version also overstated
neutrality and transferred a core-packing cap without establishing owners.
The account below replaces those deductions following
[R2–R3 of the combined review](https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994).
The original measurements are retained; the changed conclusions concern their scope.

## 1. Definitions

**`s(11)`.** The side of the smallest square containing eleven unit squares without
overlap, at arbitrary rotations.
To prove a lower bound `L`, exclude every container side strictly below `L`. The
conclusion is `s(11) >= L`; it does not by itself decide whether a packing exists at
side exactly `L`. A direct exclusion at `L` settles that additional question.

**Core.** With a shrink factor `B < 1` and an admitted finite direction net satisfying
the proved strict-containment condition, every unit square placed in the container
contains a closed `B`-square at one of those directions: its *core*. Disjoint unit
squares have disjoint cores.

**Point certificate.** A finite family of nonnegative weighted *point atoms*. A point
atom is a weighted point; a core’s charge is the total weight of the points it contains.
The certificate is valid when every admissible core is charged at least one.
Eleven disjoint squares then give eleven disjoint cores, each charging at least one, so
the total weight is at least eleven; a certificate of total weight below eleven is
therefore a proof that eleven squares do not fit.

**Threshold atom.** A triple `(S, k, w)`, with finite `S`, integer `1 <= k <= |S|` and
`w >= 0`, charging `w` to every core containing at least `k` points of the finite set
`S`. Pairwise disjoint cores each consume `k` points, so at most `floor(|S| / k)` can be
charged and the atom costs `w * floor(|S| / k)`. Strictly stronger than point atoms; it
is what carried this branch past `191/50`.

**Fractional packing; ceiling family.** On the dual side, a nonnegative weighting of
cores whose total weight at any point of the plane is at most one (*depth at most one*).
By weak duality, a fractional packing of total weight at least `n` shows that no **point
cover** of its admissible core family has mass below `n`. Such a family is a *ceiling
family* for that specified point-cover problem.
For threshold charges it must also satisfy the threshold inequalities; depth one alone
is insufficient. The symmetry, shrink, net and residual domain are part of the claim.
The retained one at `191/50` has 88 cores of weight `1/8`, total exactly eleven, maximum
depth exactly one, decided in exact arithmetic.

**Conditioning.** Case analysis.
Prove that every hypothetical physical packing has a valid selection of structural
features whose residual family is excluded.
Excluding every raw class is a sufficient plan, but overlapping classes can give one
packing several valid selections.
One unclosed label does not defeat every such plan.

**Corner ownership, the conditioning at issue.** At side `96/25`, every packing of
eleven has, at each corner, an *owner*: a square whose core contains one of two
designated marks near that corner.
Owners fall into sixteen classes per corner (two marks by eight angular sectors).
Fixing a class pins the owner’s pose enough to name a *patch* that is guaranteed
occupied; the other squares’ cores must avoid it, and those cores constitute the class’s
*residual domain*.

**The conditional requirement.** Conditioning on `m` corners accounts for `m` owners, so
the remaining `11 - m` squares hold pairwise disjoint cores in the residual domain.
A cover of that domain of total weight strictly below `11 - m` is a contradiction.
The requirement per class is therefore: **strictly below `11 - m`**.

## 2. The facts, with the status of each

| # | Fact | Status |
| --- | --- | --- |
| F1 | The single-corner ownership theorem stands alone; the four-owner structure is needed only to make the owners distinct from one another | read from the proof documents |
| F2 | The mass-eleven ceiling family transports to `96/25` and is there a depth-one family of mass eleven | computed with the ownership line’s own transport and screen, imported unmodified |
| F3 | The cores containing a given corner mark carry weight **exactly one** in that family | EXACT for this family; not a consequence for all fractional families of the physical ownership theorem |
| F4 | For four of the sixteen classes the patch reaches nothing in the family beyond the mark itself | EXACT |
| F5 | No core meets two corner patches, because cross-corner distance `1.8545` exceeds core diameter `B sqrt 2 = 1.4109` | EXACT |
| F6 | Deletion per class ranges from exactly `1` to `11/4`, mean `55/32` | EXACT over the sixteen screened endpoint classes; not a physical routing census |
| F7 | The surviving family at a neutral class has two-of-three maximum `5/4` and heaviest rank-one clique `11/8` with piercing number `5/3`, matching these readings for the full family | EXACT readings; not equality of the whole cut structure or optimization problems |

## 3. The ladder

**Step 1 (deductive).** Deleting from a depth-one family those cores that meet the patch
leaves a depth-one family, every member of which is admissible in the residual domain.
So the survivors are a feasible fractional packing of the residual problem.

**Step 2 (deductive, from 1).** By weak duality, every **point cover** of the residual
domain has total weight at least the survivor weight.

**Step 3 (from F3, F4).** At a neutral class the deletion removes exactly one unit, so
the survivor weight is exactly `11 - 1 = 10`, while the requirement is strictly below
ten. Ten is not below ten.

**Step 4 (scope of the obstruction).** Hence no point cover with budget below ten closes
those fixed endpoint-patch relaxations.
This is an obstruction supplied by the retained survivor family, not by the mere fact
that a raw label is unclosed.
Let `Gamma(P)` be the valid owner selections of a hypothetical physical packing `P`, and
`G` the selections whose residual families have been excluded.
A sufficient global condition is

`for every hypothetical physical packing P, Gamma(P) intersects G`.

An unclosed label may be physically empty, or a packing admitting it may also have an
excluded selection. A feasible isolated owner pose or a fractional residual family
establishes neither a physical eleven-square packing nor an unavoidable label.

**Note on Step 4’s quantifier** (2026-09-10, PR 139 finding R3). “A case split needs
every class closed” is stronger than what a conditional proof requires.
The sufficient global condition is that for **every** hypothetical packing there
**exists** a valid owner selection whose residual family is excluded, and owner labels
and valid selections can overlap — one packing may admit several valid (corner, owner)
selections. A class that is never closed defeats the strategy only if some physical
packing admits **no other** valid selection, which has not been shown.
Steps 4 and 5 therefore establish that *this* case split, as posed, does not close; they
do not establish that conditioning by point covers is impossible.

**Step 5 (from F5).** Deletions at distinct corners are disjoint, so conditioning on `m`
corners at neutral classes deletes exactly `m` and leaves `11 - m` against a requirement
below `11 - m`. Two corners give nine against nine, four give seven against seven.
This is neutrality for the stated family and patch combinations.
It does not apply automatically to later wall-aware footprints or unit-parent domains.

**Step 6 (proposed, and not established).** The argument runs: at any side where eleven
pairwise disjoint admissible cores exist, delete the owners’ cores; the remaining
`11 - m` are disjoint, admissible, and avoid the patches, because the patches lie inside
the owners’ cores; their 0/1 indicator is then feasible for every rank-one inequality on
the residual domain, so the proved rank-one cap of `3.868983` would transfer to the
conditional method at every `m`.

**It does not go through as stated** (2026-09-10, PR 139 finding R2). The deduction
starts from an artificial packing of eleven `B`-cores at `3.868983`, and that packing
has never been shown to carry distinct marked owners, class memberships or occupied
patches; the ownership theorem the step leans on concerns unit-parent packings at
`96/25`. “Delete the owners’ cores” presupposes exactly what is unproved there.
Any conditional transfer of the cap therefore **requires a separate owner, class, patch
and routing verification**, and none has been done.
Spelled out, that verification is: identify `m` distinct owners in the witness, verify
their marks and classes at the same side, and prove that their union contains the
declared occupied patches; the remaining cores must then satisfy every further
restriction in the residual model.
Only then do their indicators obstruct a budget below `11 - m` on that fixed domain.
Even a valid fixed-selection obstruction would still leave Step 4’s routing question.
The unconditional obstruction is untouched by this and stands at its own stated scope.

## 4. Where the ladder stops

Step 2 concerns **point covers only**. The survivor family has depth one, but by F7 a
two-of-three atom charges it `5/4` against a budget of one: it *violates* threshold
inequalities, and therefore does **not** block a conditional threshold certificate.
The blocking argument does not reach the richer language.

**Established**, each at the scope of the objects it was measured on: the retained
transported mass-eleven ceiling family, and the screened endpoint patches.

- Conditioning by point covers cannot close the neutral classes, at one, two or four
  corners.
- Conditioning subtracts exactly `m` from both the obstruction and the requirement on
  that family, so it cannot convert a failing method into a succeeding one there.
  This is the substantive result, and “**neutral**” is its correct name.

**Not established.**

- That a conditional certificate using *threshold* atoms fails.
  F7 reads two cut maxima on the survivor family and finds them equal to the full
  family’s; that is a match on one family at one class, not a proof that the conditional
  optimisation *is* the unconditional one shifted down by one on both sides.
  Read as an **estimate**, with its assumptions named — that those two matching maxima
  are representative of the whole cut structure, and that the cost multiplier is the
  **class count per corner** (sixteen classes at eight sectors) rather than a measured
  running cost. The estimate says conditioning buys no reach for more work; it is not a
  proof that it cannot work.
- That the rank-one cap `3.868983` applies to the conditional method.
  Step 6 is the proposed transfer and it does not go through as stated; it requires a
  separate owner, class, patch and routing verification that has not been done.
  This entry moved here from **Established** on 2026-09-10 (PR 139 finding R2).
- That the case split fails as a *strategy*. Steps 4 and 5 retain obstructions on the
  named neutral relaxations; they do not supply the proposed all-class closure.
  Step 4’s quantifier explains why closing every raw class is more than a conditional
  proof needs.

The word **refuted** is therefore wrong for “the conditional route” as a whole.
It is right only for the point-cover conditional method on this family and this split,
and the general claim that survives is neutrality.

## 5. Three escapes this argument does not close

1. **Fatter patches — narrowed, not closed.** Measured 2026-09-10 by
   [lane X4](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x4-sixteen-sectors-and-the-refinement-limit.md),
   which refutes
   [`H-157`](../hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md).
   Refining the eight sectors to sixteen does widen the guaranteed wedge from `pi/4` to
   `3pi/8` and grows the patch by about 62 per cent in area.
   Six of the eight refined subclasses retain survivor weight ten; two improve to
   `19/2`, exceeding the registered improvement to at most `79/8`. Thus the maximum
   remains ten, but local improvement is real.

   **Distance correction, September 10.** The reported unchanged positive distance holds
   for the six neutral children.
   The patches `m1:J9/16` and `m2:J6/16` intersect their fixed target cores 55 and 50,
   so their distances to those cores are zero.
   The delivered distance helper assumed disjoint polygons and failed to check that
   premise. A mark being a vertex does not prevent an enlarged patch from approaching
   another core. The independent review reproduces the survivor table and corrects this
   explanatory geometry; the count-based H157 rejection stands.

   Two theorems come out of it, T1 (angular) and T2 (pose), stated in §5.1 below.
   Both concern **the retained transported mass-eleven family on the specified
   patch-only residual domain**. Their patch, mark and pose-universe premises are stated
   beside them; additional residual restrictions require fresh admissibility.

   **What that establishes.** Within those premises, every partition retaining the named
   neutral ray or pose has a class with survivor weight at least ten.
   Refining its patch alone cannot close every class by a point cover on that same
   domain. Other classes can improve, as two of the measured subclasses do.

   **What it does not establish.** That the conditional strategy fails.
   The sufficient global condition is not that every class is closed — it is that for
   every hypothetical packing there **exists** a valid owner selection whose residual
   family is excluded. Owner labels and valid selections can overlap, so a packing may
   admit several valid (corner, owner) selections.
   A permanently neutral class is therefore fatal only if some physical packing admits
   **no other** valid selection, and that has not been shown; a packing carrying one
   unclosed label may still admit a selection that is already excluded.

   So escape 1 is **narrowed, not closed**. What remains open is whether the neutral
   classes are ever *forced* — whether some physical packing admits only neutral
   selections. That question is adjacent to escape 2 (emptiness) and is not settled here.
   Routing, stronger residual domains, wall-aware footprints and richer conditional
   charges are untouched and remain exactly as open as they were.

2. **Empty classes.** If the neutral sectors cannot occur in an actual packing of
   eleven, they need no cover and Step 4 evaporates for them.
   Every sector admits a *pose*, which is weaker than admitting a full eleven-square
   packing.

3. **Pruning.** The four-corner programme survives if compatibility rules kill every
   combination drawn from the four neutral sectors.
   Nobody has enumerated them.

### 5.1 The Angular and Pose Obstructions, with Their Premises

Both are about the retained transported mass-eleven ceiling family at `q = 96/25` and
the screened endpoint patches; `w(F)` is the exact survivor weight left when every core
meeting the guaranteed patch `F` is deleted, and F3 is the fact that the cores holding a
given corner mark weigh exactly one.
The residual domain here imposes patch avoidance and the retained core admissibility
rules. Adding parent, wall or joint-compatibility restrictions requires verifying that
the surviving family satisfies them.
T1 and T2 below are local proposition labels, not frontier claim identifiers.

**T1, angular.** Let `r0` be a retained signed ray whose singleton class has survivor
weight exactly 10. Partition the declared finite retained signed-ray universe into
closed angular bins, and let `B` contain `r0`. Define its patch `F` to be the
intersection of `Q_r(m)` over the retained rays of `B`, all at the same mark `m`. Then
`F` is a subset of `Q_r0(m)`, so `F` deletes a subset of what `Q_r0` deletes and
`w(F) >= 10`. And `m` lies in `F`, so `F` meets every core containing the mark; the mark
clique weighs exactly 1 (F3), so `w(F) <= 11 - 1 = 10`. Hence `w(F) = 10` exactly,
against a requirement strictly below 10.

The argument needs only one neutral retained ray: every partition of that universe
places it in a bin. This is a statement about the declared angular construction, not
about a class remaining possible after additional physical or joint restrictions.
Lane X4 measured 135 such rays per mark, spanning a contiguous arc `34.40698` degrees
wide; that width is robustness, not the load-bearing step.

**T2, pose.** In this patch-only model, a guaranteed patch lies inside the selected
owner core for every pose in its class.
This definition does not cover every possible occupied-region argument, such as one
using more of the unit parent.
Mark-clique member `#59` is an admissible net-oriented core inside the container
containing both bottom-left marks, at `(45133461/88696100, 25096071/49318700)`, and
`#60` is its diagonal mirror.
For a partition of a pose universe retaining `#59`, let `C` contain it and let `F` be
any patch contained in every selected owner core of `C`. Then `F` is a subset of
`core(#59)`, so `w(F) >= w(core(#59)) = 10`. That inequality already obstructs a point
cover of budget below ten on the stated residual domain.

Equality additionally requires a common mark `m` to lie in `F`, for example when `F` is
the full intersection for a class whose every core contains that same mark.
Owning the mark does not force every chosen subpatch to contain it.
As an exact counterexample, scale `core(#59)` by `1/10000` about its bottom-left corner
and use that positive-area patch for the singleton class.
It contains neither mark and leaves survivor weight `43/4`, confirmed by SAT and
clipping.

Cores `#59` and `#60` each have a contained concentric same-angle unit parent, with
positive wall margin `785411/88696100`. No completion to eleven disjoint parents or
forced owner selection is proved.
The subset argument does not settle the survivor family’s admissibility after stronger
residual restrictions, or the value of refining other classes and routing physical
packings to them.

Neither theorem says the conditional strategy fails; see the reading under escape 1.

## 6. Reading

The measurements retain neutral classes on the named patch-only relaxations and show
improvement in two refined subclasses.
They do not supply a measured comparison of conditional and unconditional runtime,
reachable bound, or value of routing and pruning.
Conditional threshold charges remain a separate open comparison.
This is consistent with
[`H-155`](../hypotheses/H-155-conditional-threshold-cover-on-an-owner-class.md) now
carries, and the scope correction [X-024](X-024-two-lines-at-eleven.md) §5 and
[lane X1](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md)
now carry with it.

The PR139 reviews on September 10 separate the supported counts from their
interpretations.
**R3**: §5.1 obstructs all-class point closure within its stated domain,
while a global conditional proof needs an excluded valid selection per packing.
**R2**: the transfer of the rank-one cap `3.868983` to the conditional method is
proposed, not established, and needs its own owner, class, patch and routing
verification; the unconditional obstruction is untouched.
**The cost reading**: that the conditional problem is the unconditional one shifted down
by one for sixteen times the work is an estimate on two matching cut maxima with the
class count standing in for a measured cost, and it is labelled as one in §4. It does
not establish comparative productivity.
The later independent source review also corrects the two distance cases, exp154’s
aggregate and T2’s missing mark premise; the retained survivor counts are unchanged.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
