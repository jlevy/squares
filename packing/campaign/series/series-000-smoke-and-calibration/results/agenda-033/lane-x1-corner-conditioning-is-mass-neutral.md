# Agenda 033, lane X1: corner conditioning is exactly mass-neutral

Retained strategy-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by a Fable
sub-agent on 2026-09-09, read-only on the repository at
`claude/n-11-stronger-result-d730ds`. The report is reproduced as delivered, with its
own headings and its own numbers; only its file references were rewritten to say where
each file now is, and two notes were added where they bear on an entry already in the
record: the correction below about the source family, and the scope note that follows
this paragraph. X-024 carries the coordinator’s reading.

**This is the lane that reversed a direction the campaign was leaning toward.** X-024 §3
route C and §4 read conditioning on corner ownership as the architecture for `3.84` and
beyond; the measurement below says it is neutral at every rung, and X-024 §5 now records
that. Nothing here refutes the *validity* of the owner theorem or of a conditional
certificate — what it refutes is the premise that conditioning buys mass.

> **Scope, added 2026-09-09 with
> [X-026](../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md).**
> Read “refutes” in this report as covering **point covers on the residual domain**,
> which is what the survivor weight bounds by weak duality.
> It does not cover threshold atoms there: the survivor family has depth one but charges
> `5/4` against a budget of one on a two-of-three atom (see the plateau-reader reading
> below), so it *violates* the threshold inequalities and cannot block a conditional
> threshold certificate.
> The general result this lane established is **neutrality** — conditioning subtracts
> exactly `m` from both the obstruction and the requirement, so it cannot turn a failing
> method into a succeeding one — and neutrality, not refutation, is what carries to the
> conditional route as a whole.
> X-026 states the six-step ladder and marks the step where it stops.

Retained beside this report: the four screening scripts and the two survivor records,
listed under [Files](#files).
Not retained (scratch only): the transported ceiling family at `96/25`, the sixteen
per-class screen outputs at the four sides, and the three per-class estimate dumps.

Labels: **EXACT** = a rational decision by repository primitives; **CHECKED** = a float;
**RECORD** = read from a file in the repository; **OPEN** = not measured.

## The decision

**Do not build the single-corner rung, the two-corner rung, or the wall-slot
generalization. Conditioning on corner ownership is mass-neutral at the class that
decides the case split, and the ladder is neutral at every rung.** The next measurement
belongs to the unconditional lane: run the plateau reader’s `K4`-`K6` on the
`1/25`-integral dual at `153/40` with the depth gate bypassed, and feed every violated
atom back into the warm LP as a column.

The refuting measurement was cheap and it has already been made.
It cost about 100 seconds of compute.
It has since been taken, and is retained as
[lane A4](lane-a4-separating-the-plateau-dual-at-153-40.md).

## What was measured

The retained ceiling family at `191/50`
([`ceiling-family-191-50.json`](ceiling-family-191-50.json); 88 closed `B`-squares,
weight `1/8` each, total **exactly 11**, exact maximum depth **exactly 1**) was
transported to `96/25` by PR 137’s own transport
([`devtools/transport_ceiling_family.py`](../../../../../devtools/transport_ceiling_family.py),
scale 1, recentring shift `1/100` in each coordinate — the `(+1/100, +1/100)`
translation exp-137 used), and screened against PR 137’s own owner footprints with PR
137’s own filter, `screen_footprint` from
[`devtools/screen_corner_dual_salvage.py`](../../../../../devtools/screen_corner_dual_salvage.py),
imported verbatim: the same canonical orientation test, the same strict positive
separating-axis gap, the same container check.
All 88 placements pass the orientation filter and stay inside the container, so the
transported family is a depth-one fractional packing of mass eleven at `96/25`.

| quantity | value | Label |
| --- | --- | --- |
| weight of the cores containing bottom-left mark `m1` | **exactly 1** (8 placements) | EXACT |
| weight of the cores containing mark `m2` | **exactly 1** (the same 8 placements) | EXACT |
| survivor weight, endpoint footprint, over the 16 classes | `33/4` to **exactly 10** | EXACT |
| classes with survivor exactly 10 | **4 of 16**: `m1:j3`, `m1:j4`, `m2:j3`, `m2:j4` | EXACT |
| mean deletion over the 16 endpoint classes | `55/32 = 1.71875` | EXACT |
| the same, triangle (reviewed) footprint | 6 of 16 at exactly 10 | EXACT |
| the same at sides `191/50`, `153/40`, `383/100` | identical: 4 of 16 at exactly 10 | EXACT |
| deleted sets at the four corners, class `j3` | pairwise **disjoint**, weight 1 each | EXACT |
| four-corner survivor for `(j3, j3, j3, j3)` | **exactly 7** | EXACT |

A survivor is an admissible core strictly disjoint from the guaranteed patch, so the
survivors are a feasible fractional packing of the class’s residual domain.
By weak duality every nonnegative point cover of that domain has mass at least the
survivor weight. The conditional certificate needs budget `< n - m = 10` at one owner.
**At classes `j3` and `j4` the residual point-covering value is at least 10 and the
budget must be below 10: the conditioning is exactly, and only exactly, neutral.**

## Why it is neutral, and why the ladder inherits it

The mechanism is one line.
The ceiling family is *owner-saturated*: the corner-pair proof leaves the duals no room
to avoid the marks ([lane T2](lane-t2-cap-and-next-cuts.md), C.1, `y(K_c) = 1` at every
corner), and this lane confirms it exactly — each mark clique weighs 1, not less.
The patch `F_j` lies inside the owner’s core and contains its mark, so it deletes at
least the mark clique, which is exactly one unit; and for sectors `j3` and `j4` it
reaches nothing else.
So conditioning gives up one unit of threshold and takes back one unit of ceiling.

The gain of a conditioning is therefore not the conditioning but the **patch’s reach
beyond the mark**: `gain_j = y(cores meeting F_j) - m_j`. That is a measurable number,
and for four of the sixteen classes it is exactly zero at every side tested.

Because no core meets two corner patches (cross-corner distance `1.8545 > B sqrt 2 =
1.4109`), the deletion is **exactly additive over corners** — the four deleted sets were
verified pairwise disjoint.
So every rung is the same rung: `m` corners in class `j3` delete exactly `m` against a
threshold of `11 - m`. One corner leaves 10 against 10; two corners (256 classes) leave
**exactly 9 against 9**; four corners leave **exactly 7 against 7**. There is no rung at
which the arithmetic turns.

Additivity is not new evidence; it is already in the record and was checked there too.
exp-137’s minimum one-corner deletion is `1589589099/1644210556` and exp-138’s minimum
four-corner deletion is `1589589099/411052639` — **exactly four times it**, to the last
digit.

> **Correction, and it is why [`D-489`](../../../../../defects.yaml) was filed.** Those
> two figures are additive, and that much stands.
> Their *absolute* level does not: both screens ran on
> `agenda-025/bc-232-leg-01-family.json`, of mass `10.3842`, not on the mass-eleven
> ceiling family, so their reported shortfalls are the source family’s missing mass
> rather than a property of conditioning.
> The paragraph headed “1(c)” below is where that was found, and every citation of
> exp-137 or exp-138 as evidence about conditioning now carries the same note.

## Answers to the four questions

**1(a) Is a single-corner owner theorem available standalone?** Yes, and the proof
separates cleanly.
[`corner-owner-sector-footprints.md`](../agenda-031/proofs/corner-owner-sector-footprints.md)
derives ownership from BC-303’s corner-pair replay, which “verifies that each pair’s
mass exceeds the available uncovered mass, and that cross-corner distances exceed
`B sqrt 2`”. The first clause is a per-pair mass argument against the measure-free
certificate bc-293; it proves *one* corner is owned on its own.
The second clause is used only to make the four owners distinct, and the sector
construction `T_j(m)` inside the owner’s core `P` is per-owner throughout.
So the single-corner statement stands without the four-owner structure, and it holds at
every smaller side because the marks are absolute points.
`owner_branch_manifest()` supplies the 16 bottom-left classes as a standalone,
exhaustive split (a packing belongs to at least one; the bins are closed and may
overlap, which is harmless).
The object exists. It is sufficiency that fails, not validity.
[Lane X2](lane-x2-owner-instrument-survey.md) is the full inventory of what that object
comes with.

**1(b) Is the per-owner reduction an average, and is it far from uniform?** It is an
average, and it is very far from uniform.
`1.5` is `(11 - 5)/4` on one certified class; `1.566` is `(11.262 - 5)/4`, an upper
bound from bc-293 on the same class.
The distribution over the 16 classes at one corner, which nobody had measured, runs from
**exactly 1** to `11/4 = 2.75`, mean `1.71875`. The case split is decided by the
minimum, and the minimum is exactly the neutral value.
This is the answer to the question the lane was asked: one owner buys well under the
`1.0` it must — it buys exactly `1.0`, and `1.0` is not enough, because the requirement
is strict.

**1(c) How would one bound the residual value from below cheaply?** By exactly the
screen above: transport a depth-one family of mass `n`, delete the members meeting
`F_j`, and read the survivor weight.
It is exact, it needs no LP, and it costs seconds.
It is the instrument PR 137 already built.
**The reason their screens read negative is that they were run on the wrong family.**
exp-137 and exp-138 used
[`agenda-025/bc-232-leg-01-family.json`](../agenda-025/bc-232-leg-01-family.json): 768
placements, mass `21342289572/2055263195 = 10.3842`, whose own receipt records
`proved: false, failures: ["K3 total weight at least n"]`. It is
`1265605573/2055263195 = 0.6158` short of eleven.
Their observed shortfalls are `10 - 9.4174 = 0.5826` and `7 - 6.5171 = 0.4829`, both
**smaller than that deficit**: the entire negative result is the source family’s missing
mass. The mass-eleven ceiling family postdates those runs by hours.
X-024’s summary table described the screens as filters of “the retained depth-one family
at `191/50`”, which is the mass-eleven object; the screens did not use it, and X-024 now
carries the correction.
The CLI could not be re-run unmodified because `_source_receipt` requires
`failures == ["K3 total weight at least n"]` — the instrument is hard-wired to accept
only a source that fails the mass threshold — so `screen_footprint` was replayed
directly. That predicate is itself the tell, and it is
[`D-489`](../../../../../../defects.md).

**2. Corner or wall slot?** The generalization is sound in form and dead in substance,
for the same reason.
A slot conditioning needs a proved lemma of the shape “there are finitely many slots,
each is owned, and an owner in class `j` occupies patch `F_j`” — the segment-ownership
line ([X-022](../../../../explorations/X-022-segment-ownership-continuation.md),
agenda-031) has the pieces.
But the neutrality argument does not care what the region is called.
A fractional packing obeys `y(T(p)) <= 1` at every point, so a guaranteed-occupancy mark
can never delete more than one unit by itself, and a saturated family deletes exactly
one; the gain is again only the patch’s reach beyond the mark.
A corner is the *favourable* case, because two walls squeeze the owner’s pose and fatten
the patch.
A mid-wall slot has more angular freedom and a thinner guaranteed patch, so it
will buy less, not more.
The premise also needs correcting: of the three plateau depth witnesses, one is a corner
seam (`383/100`), one is a **mid-wall sliver** (`153/40` after site separation), and one
is **interior** — `(1.71652, 1.71652)` on the diagonal, at the meeting of the tilted
pair and the `8°` squares ([lane A3](lane-a3-threshold-loop-at-383-100.md)). A
boundary-slot conditioning would not reach the interior one at all.

**3. Is there a lift that avoids the tree?** No, and the same measurement proves it
without machinery. A single certificate valid for all 16 classes must charge every core
residual in some class, and `R_{j3}` alone is such a set; the survivor family shows its
point-covering value is at least 10, while a single certificate needs budget below 10.
That is lane T2’s `C.3` at `m = 1`, now with an exact witness rather than the
point-extension lemma.
The disjunction is genuinely essential: it is an integrality statement (“the owner is
one core”) that a fractional packing spreads over the classes, and a valid inequality
for a union of polyhedra must be valid for each piece.
There is no extended formulation to build here.

**4. Does conditioning escape the rank-one bracket?** No, and the bracket transfers
verbatim. At any side where eleven pairwise-disjoint admissible cores exist — Trump’s
packing shrunk to `B` and snapped, `L >= 3.868983` — the packing falls in some class
`j*` at each corner; delete its four owners and the remaining seven cores are pairwise
disjoint, admissible, and disjoint from the patches, because the patches lie inside the
owners’ cores. Their 0/1 indicator is a packing of mass `n - m` feasible for every valid
rank-one cut on the residual domain.
So the conditional rank-one method is capped at the same `3.868983`, for every `m`.
Conditioning changes neither end of `[3.82, 3.868983]`.

Worse, and this is the measurement that settles the hybrid question: the promoted
plateau reader was run on the 80-placement mass-10 survivor family (`m1:j3` at `96/25`),
94 seconds, all keys.
It reports depth exactly 1 over 19,978 vertices, two-of-three maximum **`5/4`**
(complete, 414 maximisers, sparsest witness memberships `[4, 8, 8]`), heaviest rank-one
clique **`11/8` with `tau* = 5/3`**, line chords tight on eight resources, and violated
CG floor atoms at `t = 2, 3, 4` with violations `1/2`, `3/8`, `3/4`. Those are the
*same* values the full ceiling family carries (lane T2 F3, F4;
[lane M0](lane-m0-fixed-support-polish-191-50.md) F7). **Conditioning removed exactly
one unit of mass and exactly none of the cut structure.** The conditional threshold
problem at a class is the unconditional one shifted down by one, with sixteen times the
work and no better reach.

## The next measurement

**Run [`devtools/plateau_reader.py`](../../../../../devtools/plateau_reader.py) on the
`1/25`-integral dual at `153/40`, 280 placements, total exactly 11 — with the `K2` depth
gate bypassed so `K4`, `K5` and `K6` execute, and add every atom it returns to the warm
LP as a column.** This is the object lane A3’s S4 named as unmeasured and the reader
currently refuses by design.

Exact form: one flag on the reader that runs `K4`-`K6` on a family of depth above one,
reporting the readings as separation-oracle readings and not as theorems (a violation is
judged against budget 1 and is sound as separation whatever the depth, because an atom
column that cuts the current dual strictly moves the LP). Then a warm site resume at
`153/40` with the returned atoms as columns.

Cost: the reader took 94 s on 80 placements and 1,418 membership sets; 280 placements
puts `K4`/`K5` in the low minutes and `K6` at up to 60 s per threshold.
One warm re-solve with a handful of atom columns is minutes, not the 825 s that 300 site
columns cost. Call it twenty minutes end to end.

What each outcome means.
**The LP drops below eleven** — freeze, gate, and `s(11) >= 153/40 = 3.825`
unconditionally, which is more than the whole conditional programme could offer.
**The LP stays at eleven and the dual relocates** — the atom language is not what pins
`3.825`, S4’s reading stands, and the sites must be placed by the sliver’s structure
rather than vertex by vertex.
**The reader returns no violated atom at all** — the `1/25` family is rank-one feasible
apart from its `28/25` depth excess, so the sliver is the entire obstruction and the
next object is a repaired depth-one version of it, which would cap the method at `3.825`
as a theorem.

This is preferable to any confirmation on the conditional side because it can only end
in a bound, a named cut, or a theorem about the method, and because the `K6` reading
above is direct evidence that the loop’s single generator is leaving the largest
violations on the table: the CG floor atoms cut three times harder (`3/4`) than
two-of-three (`1/4`) on a family of exactly this shape.

**Outcome, later the same day.** The measurement was taken and is retained as
[lane A4](lane-a4-separating-the-plateau-dual-at-153-40.md): the second outcome, the LP
stays at eleven and the dual relocates, with twenty-four violated atom orbits carrying
primal weight exactly zero.
The prediction about the generator held — the `K6` floor atoms were the largest
violations by an order of magnitude — and it did not matter.

## Uncertainties, and what would decide each

- **The four-corner claim.** `(j3, j3, j3, j3)` leaves survivor exactly 7 against
  threshold 7, so PR 137’s programme is obstructed unless compatibility pruning kills
  all `4^4 = 256` combinations drawn from `{m1:j3, m1:j4, m2:j3, m2:j4}` — and only
  those, since every other combination deletes at least `4.5`. That is the other agent’s
  census; nothing was enumerated here and this lane does not.
- **Class emptiness.** The single-corner refutation has one escape: if sectors `j3` and
  `j4` are empty, they need no cover.
  An emptiness proof is not a covering argument, so it would not rescue the method, only
  these classes; a pose-feasibility check on the two sectors would decide it.
- **A larger guaranteed patch**, registered after this lane as
  [`H-149`](../../../../hypotheses/H-149-refined-owner-sector-patch-breaks-neutrality.md).
  The closest survivor to the `j3` footprint sits at Euclidean separating gap
  **`0.014978`** — a weight-`1/8` wall placement centred at `(1.50658, 0.50885)`. A
  patch reaching `0.015` further picks up `1/8` and opens `0.125` of room, against a
  global ceiling slack (`tau(96/25) <= 11.262`) of `0.262`. Refining the eight sectors
  to sixteen is the way to get it; whether the refined patch clears `0.015` is one
  screen away, and this lane would not spend it.
- **The threshold route on a residual domain** is neither refuted nor supported here.
  It is exactly as open as the unconditional route and costs sixteen times more; that is
  why the decision is the unconditional lane.
  [`H-146`](../../../../hypotheses/H-146-conditional-threshold-cover-on-an-owner-class.md)
  is dispositioned on exactly that reading: the claim is live, not refuted, and it is
  priced at no reach — the survivor family carries the same cut structure as the full
  family, so threshold atoms cut it exactly as they cut the unconditional ceiling.

## Files

Retained beside this report:

- [`lane-x1-ceiling11-screen.py.txt`](lane-x1-ceiling11-screen.py.txt) — the 16-class
  screen, three footprint kinds.
- [`lane-x1-build-survivor.py.txt`](lane-x1-build-survivor.py.txt) — cross-corner
  disjointness and the `m1:j3` survivor family.
- [`lane-x1-sides.py.txt`](lane-x1-sides.py.txt) — the screen at `191/50`, `153/40`,
  `383/100` and `96/25`.
- [`lane-x1-gap.py.txt`](lane-x1-gap.py.txt) — the closest-survivor separating gap.
- [`lane-x1-survivor-m1-j3.json`](lane-x1-survivor-m1-j3.json) — the 80-placement,
  mass-10 residual family.
- [`lane-x1-reader-survivor-m1-j3.json`](lane-x1-reader-survivor-m1-j3.json) — the full
  plateau-reader report on it.

The four scripts are retained with a `.py.txt` extension, as
`agenda-032/unrun-independent-audit/` already does: they are scratch measurement
scripts, not importable project modules, and the repository’s Python surface is held at
zero Ruff and BasedPyright findings over every tracked `.py` file.
Their bytes are as delivered; nothing was reformatted.

Not retained (scratch only): the transported mass-eleven family at `96/25` (rebuildable
in seconds from `ceiling-family-191-50.json` by `transport_ceiling_family` at scale 1
and shift `1/100`), the sixteen per-class screen outputs at each of the four sides, and
the three per-class estimate dumps.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
