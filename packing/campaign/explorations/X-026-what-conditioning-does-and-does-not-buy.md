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
    does not reach the richer language. The defensible general claim is neutrality --
    conditioning subtracts exactly m from both the obstruction and the requirement --
    and "refuted" is right only for the point-cover conditional method. Three escapes
    the argument does not close are named, one of them a single unrun screen.
    Revised 2026-09-10 after lane X4 ran that screen and after the PR 139 review.
    Escape 1 is narrowed rather than closed: refining the patch is ruled out as the
    lever at every angular resolution and at pose level (the two theorems now in 5.1),
    but a conditional proof needs one closed owner selection per packing rather than
    every class closed, so whether the neutral classes are ever forced stays open beside
    escape 2. Step 6's transfer of the rank-one cap 3.868983 to the conditional method
    is restated as proposed and unverified, and the cost reading behind H-155 is
    labelled an estimate.
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
  proposes: [H-157]
---
# X-026 — What Conditioning Does and Does Not Buy: Definitions, and a Ladder of Inference

Coordinator analysis, 2026-09-09, written after the measurement lane
([lane X1](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md))
returned.
Its purpose is to state the argument in full, with every term defined before it
is used, and to mark exactly where the chain of inference stops.
It exists because the first summaries of that lane said “conditioning is refuted”, which
is stronger than what was measured.

## 1. Definitions

**`s(11)`.** The side of the smallest square containing eleven unit squares without
overlap, at arbitrary rotations.
Lower bounds are proofs that a container of side `L` is too small.

**Core.** With a shrink factor `B < 1` and a finite net of directions, every unit square
placed in the container contains a closed `B`-square at one of those directions: its
*core*. Disjoint unit squares have disjoint cores.

**Certificate.** A finite family of weighted *atoms*. A *point atom* is a weighted
point; a core’s charge is the total weight of the points it contains.
The certificate is valid when every admissible core is charged at least one.
Eleven disjoint squares then give eleven disjoint cores, each charging at least one, so
the total weight is at least eleven; a certificate of total weight below eleven is
therefore a proof that eleven squares do not fit.

**Threshold atom.** A triple `(S, k, w)` charging `w` to every core containing at least
`k` points of the finite set `S`. Pairwise disjoint cores each consume `k` points, so at
most `floor(|S| / k)` can be charged and the atom costs `w * floor(|S| / k)`. Strictly
stronger than point atoms; it is what carried this branch past `191/50`.

**Fractional packing; ceiling family.** On the dual side, a nonnegative weighting of
cores whose total weight at any point of the plane is at most one (*depth at most one*).
By weak duality, a fractional packing of total weight at least `n` shows no valid
certificate of weight below `n` exists.
Such a family is a *ceiling family*: it certifies that the method fails at that side.
The retained one at `191/50` has 88 cores of weight `1/8`, total exactly eleven, maximum
depth exactly one, decided in exact arithmetic.

**Conditioning.** Case analysis.
Prove that every packing has some structural feature, that the feature falls into
finitely many classes, then refute each class.
The argument succeeds only if *every* class is refuted; one surviving class defeats it.

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
| F3 | The cores containing a given corner mark carry weight **exactly one** in that family | EXACT; independently derived earlier as `y(K_c) = 1` at every corner |
| F4 | For four of the sixteen classes the patch reaches nothing in the family beyond the mark itself | EXACT |
| F5 | No core meets two corner patches, because cross-corner distance `1.8545` exceeds core diameter `B sqrt 2 = 1.4109` | EXACT |
| F6 | Deletion per class ranges from exactly `1` to `11/4`, mean `55/32`; the case split is decided by the minimum | EXACT, over all sixteen |
| F7 | The surviving family at a neutral class carries the *same* cut structure as the full family: two-of-three maximum `5/4`, heaviest rank-one clique `11/8` with piercing number `5/3` | EXACT |

## 3. The ladder

**Step 1 (deductive).** Deleting from a depth-one family those cores that meet the patch
leaves a depth-one family, every member of which is admissible in the residual domain.
So the survivors are a feasible fractional packing of the residual problem.

**Step 2 (deductive, from 1).** By weak duality, every **point cover** of the residual
domain has total weight at least the survivor weight.

**Step 3 (from F3, F4).** At a neutral class the deletion removes exactly one unit, so
the survivor weight is exactly `11 - 1 = 10`, while the requirement is strictly below
ten. Ten is not below ten.

**Step 4.** Hence no point cover closes those classes; and since a case split needs
every class closed, single-corner conditioning by point covers fails.
Four failing classes suffice — that the other twelve are easier is irrelevant.

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
No rung turns.

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
- That the case split fails as a *strategy*. Steps 4 and 5 close every class of one
  particular split; the note on Step 4’s quantifier says why closing every class is more
  than a conditional proof needs.

The word **refuted** is therefore wrong for “the conditional route” as a whole.
It is right only for the point-cover conditional method on this family and this split,
and the general claim that survives is neutrality.

## 5. Three escapes this argument does not close

1. **Fatter patches — narrowed, not closed.** Measured 2026-09-10 by
   [lane X4](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x4-sixteen-sectors-and-the-refinement-limit.md),
   which refutes
   [`H-157`](../hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md).
   Refining the eight sectors to sixteen does widen the guaranteed wedge from `pi/4` to
   `3pi/8` and does grow the patch by about 62 per cent in area, and it buys exactly
   nothing: the reach toward the nearest surviving core is the rational identity
   `d^2 = 75308842465387162009/335694834731568400000000`, bit-identical for the
   eight-sector parent and both sixteen-sector children at both marks, because the
   closest point of the patch to that core is the mark itself.
   Six of the eight refined subclasses of the four neutral classes still read exactly
   10, and the two that break read `19/2`, not the predicted `79/8`.

   Two theorems come out of it, T1 (angular) and T2 (pose), stated in §5.1 below.
   Both are statements about **survivor weight on the retained transported mass-eleven
   ceiling family and the screened endpoint patches**, and both hold unconditionally at
   that scope.

   **What that establishes.** Patch refinement is ruled out as the lever, at every
   angular resolution and at pose level: no refinement can make *every* class closed.
   That closes one route and it is worth having.

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

### 5.1 The two theorems lane X4 proved

Both are about the retained transported mass-eleven ceiling family at `q = 96/25` and
the screened endpoint patches; `w(F)` is the exact survivor weight left when every core
meeting the guaranteed patch `F` is deleted, and F3 is the fact that the cores holding a
given corner mark weigh exactly one.

**T1, angular.** Let `r0` be a retained signed ray whose singleton class has survivor
weight exactly 10. Under any partition of the owner’s pose angle into closed bins, let
`B` be a bin containing `r0` and `F` its guaranteed patch.
`F` is the intersection of `Q_r(m)` over the rays of `B`, so `F` is a subset of
`Q_r0(m)`, so `F` deletes a subset of what `Q_r0` deletes and `w(F) >= 10`. And `m` lies
in `F`, so `F` meets every core containing the mark; the mark clique weighs exactly 1
(F3), so `w(F) <= 11 - 1 = 10`. Hence `w(F) = 10` exactly, against a requirement
strictly below 10.

The statement is unconditional.
It needs only that *some* neutral ray exists, because any partition assigns `r0` to some
bin and that bin is nonempty, `r0` being an admissible pose in it.
There is no fineness threshold and no vacuity escape.
Lane X4 measured 135 such rays per mark, spanning a contiguous arc `34.40698` degrees
wide; that width is robustness, not the load-bearing step.

**T2, pose, which generalises T1.** A guaranteed patch is guaranteed precisely because
it lies inside the owner’s core for every pose in its class.
Mark-clique member `#59` is an admissible net-oriented core inside the container
containing both bottom-left marks, at `(45133461/88696100, 25096071/49318700)`, and
`#60` is its diagonal mirror.
For any conditioning of the owner by pose, at any refinement, let `C` be the class
containing `#59` and `F` its patch.
Then `F` is a subset of `core(#59)`, so `w(F) >= w(core(#59)) = 10`; and `m` lies in `F`
because every pose in `C` owns the corner and so contains the mark, so `w(F) <= 10`.
Hence `w(F) = 10`.

T2 is what makes the narrowing hold at every level of the pose rather than only at the
angular level: refining the patch is the wrong lever throughout.
What would remove such a class is a proof that the pose cannot occur in an eleven-square
packing, which is escape 2 above and not a covering argument at all.

Neither theorem says the conditional strategy fails; see the reading under escape 1.

## 6. Reading

Conditioning has been shown to buy nothing on the objects measured, not to be
impossible. The distinction matters for what gets built next: it removes the reason to
prefer the conditional route over the unconditional one, and it leaves the hybrid
(threshold atoms on a residual domain) exactly as open as it was.
That is the reading
[`H-155`](../hypotheses/H-155-conditional-threshold-cover-on-an-owner-class.md) now
carries, and the scope correction [X-024](X-024-two-lines-at-eleven.md) §5 and
[lane X1](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md)
now carry with it.

Three scope corrections landed on 2026-09-10 from the PR 139 review, and they narrow
this document rather than change any measurement.
**R3**: the two theorems of §5.1 rule out patch refinement as the lever, and no more; a
conditional proof needs one closed owner selection per packing, not every class closed,
so escape 1 is narrowed rather than closed and the forcing question stays open beside
escape 2. **R2**: the transfer of the rank-one cap `3.868983` to the conditional method
is proposed, not established, and needs its own owner, class, patch and routing
verification; the unconditional obstruction is untouched.
**The cost reading**: that the conditional problem is the unconditional one shifted down
by one for sixteen times the work is an estimate on two matching cut maxima with the
class count standing in for a measured cost, and it is labelled as one in §4.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
