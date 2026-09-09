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
  author: Claude coordinator (Fable), written after the agenda-033 lane X1 measurement returned
  campaign: packing.squares
  brief: >-
    The first summaries of agenda-033 lane X1 said "conditioning is refuted", which is
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
  sources:
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-x1-corner-conditioning-is-mass-neutral.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-t2-cap-and-next-cuts.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-x2-owner-instrument-survey.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/ceiling-family-191-50.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-x1-survivor-m1-j3.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-x1-reader-survivor-m1-j3.json
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md
  - packing/campaign/explorations/X-024-two-lines-at-eleven.md
  - packing/campaign/hypotheses/H-146-conditional-threshold-cover-on-an-owner-class.md
  proposes: [H-149]
---
# X-026 — What Conditioning Does and Does Not Buy: Definitions, and a Ladder of Inference

Coordinator analysis, 2026-09-09, written after the measurement lane
([lane X1](../series/series-000-smoke-and-calibration/results/agenda-033/lane-x1-corner-conditioning-is-mass-neutral.md))
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

**Step 5 (from F5).** Deletions at distinct corners are disjoint, so conditioning on `m`
corners at neutral classes deletes exactly `m` and leaves `11 - m` against a requirement
below `11 - m`. Two corners give nine against nine, four give seven against seven.
No rung turns.

**Step 6 (deductive, independent of the above).** At any side where eleven pairwise
disjoint admissible cores exist, delete the owners’ cores; the remaining `11 - m` are
disjoint, admissible, and avoid the patches, because the patches lie inside the owners’
cores. Their 0/1 indicator is feasible for every rank-one inequality on the residual
domain. So the proved rank-one cap of `3.868983` transfers to the conditional method at
every `m`.

## 4. Where the ladder stops

Step 2 concerns **point covers only**. The survivor family has depth one, but by F7 a
two-of-three atom charges it `5/4` against a budget of one: it *violates* threshold
inequalities, and therefore does **not** block a conditional threshold certificate.
The blocking argument does not reach the richer language.

**Established.**

- Conditioning by point covers cannot close the neutral classes, at one, two or four
  corners.
- Conditioning subtracts exactly `m` from both the obstruction and the requirement, so
  it cannot convert a failing method into a succeeding one.
  This is the substantive result, and “**neutral**” is its correct name.
- The rank-one cap `3.868983` applies unchanged to the conditional method.

**Not established.**

- That a conditional certificate using *threshold* atoms fails.
  What F7 shows is that the conditional problem at a class is the unconditional problem
  shifted down by one on both sides, for sixteen times the work — an argument that
  conditioning buys no reach, not a proof that it cannot work.

The word **refuted** is therefore wrong for “the conditional route” as a whole.
It is right only for the point-cover conditional method, and the general claim that
survives is neutrality.

## 5. Three escapes this argument does not close

1. **Fatter patches.** Neutrality is a property of the *current* eight-sector patches.
   The nearest survivor to a neutral patch lies at a separating gap of `0.014978`, and a
   patch reaching `0.015` further would delete `1/8` more.
   Refining eight sectors to sixteen is how one would get it.
   This is one cheap screen and it was not run; it is the only measurement that could
   overturn Step 3, and it should be run before the conditional line is closed in the
   record. Registered as
   [`H-149`](../hypotheses/H-149-refined-owner-sector-patch-breaks-neutrality.md).
2. **Empty classes.** If the neutral sectors cannot occur in an actual packing of
   eleven, they need no cover and Step 4 evaporates for them.
   Every sector admits a *pose*, which is weaker than admitting a full eleven-square
   packing.
3. **Pruning.** The four-corner programme survives if compatibility rules kill every
   combination drawn from the four neutral sectors.
   Nobody has enumerated them.

## 6. Reading

Conditioning has been shown to buy nothing, not to be impossible.
The distinction matters for what gets built next: it removes the reason to prefer the
conditional route over the unconditional one, and it leaves the hybrid (threshold atoms
on a residual domain) exactly as open as it was, and exactly as expensive.
That is the reading
[`H-146`](../hypotheses/H-146-conditional-threshold-cover-on-an-owner-class.md) now
carries, and the scope correction [X-024](X-024-two-lines-at-eleven.md) §5 and
[lane X1](../series/series-000-smoke-and-calibration/results/agenda-033/lane-x1-corner-conditioning-is-mass-neutral.md)
now carry with it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
