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
    obstruction to point covers on specified residual relaxations. Corrected on
    2026-09-10 after PR139 review: neutrality belongs to the retained fractional family
    and screened endpoint patches; it is not a theorem about every conditional method.
    Global coverage needs an excluded valid selection for every hypothetical physical
    packing, not every overlapping raw label. The unconditional core cap does not
    transfer without separate owner, class, patch and routing premises. Threshold
    covers, changed domains and alternative routing remain open.
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md
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

**Review correction, September 10, 2026.** The earlier version also overstated
neutrality and transferred a core-packing cap without establishing owners.
The account below replaces those deductions following
[R2–R3 of the combined review](https://github.com/jlevy/squares/pull/139#pullrequestreview-5162420994).
The original measurements are retained; the changed conclusions concern their scope.

## 1. Definitions

**`s(11)`.** The side of the smallest square containing eleven unit squares without
overlap, at arbitrary rotations.
To prove a lower bound `L`, exclude every container side strictly below `L`. An endpoint
exclusion proves more at that side; a weak limit need not decide it.

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

**Step 5 (from F5).** Deletions at distinct corners are disjoint, so conditioning on `m`
corners at neutral classes deletes exactly `m` and leaves `11 - m` against a requirement
below `11 - m`. Two corners give nine against nine, four give seven against seven.
This is neutrality for the stated family and patch combinations.
It does not apply automatically to later wall-aware footprints or unit-parent domains.

**Step 6 (additional premises required).** An actual packing of eleven admissible
B-cores obstructs any valid charge certificate of budget below eleven on that core
domain. This includes threshold, floor and valid containment-capacity inequalities.
To transfer such a witness to an owner-conditioned domain, first identify `m` distinct
owners in the witness, verify their marks and classes at the same side, and prove that
their union contains the declared occupied patches.
The remaining cores must also satisfy every further restriction in the residual model.
Only then do their indicators obstruct a budget below `11 - m` on that fixed domain.

The ownership theorem for hypothetical unit-parent packings at `96/25` supplies none of
these missing verifications for an artificial B-core witness at another side.
The unconditional obstruction near `3.868983` therefore retains its original scope; its
proposed transfer to this corner-owner method at every `m` is unestablished.
Even a valid fixed-selection obstruction would leave Step 4’s routing question.

## 4. Where the ladder stops

Step 2 concerns **point covers only**. The survivor family has depth one, but by F7 a
two-of-three atom charges it `5/4` against a budget of one: it *violates* threshold
inequalities, and therefore does **not** block a conditional threshold certificate.
The blocking argument does not reach the richer language.

**Established.**

- The retained depth-one survivor families obstruct point-cover budgets below `11 - m`
  on the specified endpoint-patch relaxations.
- On the measured neutral combinations, deletion and the residual requirement both
  decrease by `m`. “Neutral” names that exact accounting identity for those objects.

**Not established.**

- That all owner-based point proofs fail, or that every physical packing must use an
  unclosed selection.
- That a conditional *threshold* certificate fails.
  F7 is a violation of a threshold inequality, so this survivor is not its obstruction
  witness.
- That matching two cut maxima identifies the conditional and unconditional optima, or
  proves a factor of sixteen in runtime.
  Raw class counts do not account for reuse, routing or pruning; a cost comparison needs
  explicit assumptions and measurements.
- That the unconditional core cap transfers without Step 6’s added premises.

The word **refuted** is therefore wrong for “the conditional route” as a whole.
It can describe the impossibility of a below-threshold point cover of a specified
relaxation with a valid survivor witness.
It does not describe the conditional route as a whole, including its possible choices of
domains and selections.

## 5. Three escapes this argument does not close

1. **Fatter patches.** Neutrality is a property of the *current* eight-sector patches.
   The nearest survivor to a neutral patch lies at a separating gap of `0.014978`, and a
   patch reaching `0.015` further would delete `1/8` more.
   Refining eight sectors to sixteen is one proposed way to seek a larger patch; its
   actual gain has not been measured.
   This is one unrun screen among several domain changes worth distinguishing,
   registered as
   [`H-157`](../hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md).
2. **Empty classes.** If the neutral sectors cannot occur in an actual packing of
   eleven, they need no cover and Step 4 evaporates for them.
   Every sector admits a *pose*, which is weaker than admitting a full eleven-square
   packing.
3. **Routing and compatibility.** One sufficient strategy is to eliminate the unresolved
   combinations by incompatibility.
   Another is to prove that every physical packing admits an excluded selection.
   Neither a complete compatibility census nor that routing theorem is supplied by the
   X1 measurements.

## 6. Reading

The measurements identify fixed residual domains on which ordinary point covers cannot
meet their budget. They also show why the same survivor does not obstruct threshold
charges. They do not measure the comparative productivity of unconditional optimization,
stronger owner geometry, or conditional threshold certificates.
The earlier decision to withdraw the conditional work on grounds of proved equal reach
or sixteenfold cost is therefore withdrawn.
Any next allocation is a revisable strategic choice with declared assumptions.
This is the corrected reading
[`H-155`](../hypotheses/H-155-conditional-threshold-cover-on-an-owner-class.md) now
carries, and the scope correction [X-024](X-024-two-lines-at-eleven.md) §5 and
[lane X1](../series/series-000-smoke-and-calibration/results/agenda-034/lane-x1-corner-conditioning-is-mass-neutral.md)
now carry with it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
