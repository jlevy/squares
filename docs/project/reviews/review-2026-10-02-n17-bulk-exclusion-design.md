---
title: n17 Bulk Exclusion Design
date: 2026-10-02
status: planning-review
---
# n17 Bulk Exclusion Design

**Session:** 167, BC-406, lane F. **Baseline:** main after PR 265 and PR 269.
**Question:** what bulk exclusion engine could take the n17 global half from about 7.7
million occupancy orbits to $10^3$ to $10^4$ geometric leaves, and is any of them
plausible?

Lane B showed an hour earlier that per-cell charge floors cannot be that engine
([X-048 pilots](../../../packing/campaign/explorations/X048-session-167-pilots/README.md),
lines 64–78): R068’s charge collapses at the cap, and any D4-symmetric per-cell floor
vector leaves at least 30,966 orbits.
This review reads how n11 actually did its bulk exclusion, finds that the n17 census is
too large before any engine runs, and prices the engine n11 used on a smaller census.
It changes no bound, verdict or frontier field.
Every n17 number below comes from two exploratory scripts in the session scratchpad and
is planning evidence, not an admitted result.

## Summary

- **n11’s bulk engine was not geometric exclusion and not a global charge.** 1,904 of
  its 2,180 exclusions came from 59 *field* certificates, each an isolated forbidden
  sub-pattern of five to seven occupied cells, transferred by containment to every case
  that contains it. Only 276 cases needed a per-case geometric exclusion.
- **n11’s census was small because its cover was minimal.** Sixteen capacity-one cells
  for eleven squares give $\binom{16}{11}=4{,}368$ masks; a 20-cell cover would have
  given 167,960. The H259 grid is the opposite choice: its 161,100,756 states sit where
  a 30-cell capacity-one cover would, because nine of its cells have capacity two.
- **A 24-cell capacity-one cover exists at the same cap (exploratory).** Deeper wall
  cells, by the wall lemma with the depth and the width decoupled, and an eight-cell
  Voronoi interior give $\binom{24}{17}=346{,}104$ states and 43,593 D4 orbits before
  any exclusion, 177 times fewer than the cut H259 count.
- **Isolated sub-patterns bite on that cover.** A heuristic feasibility search over all
  windowed sub-patterns of up to five cells finds ten D4 classes that look infeasible;
  they leave 94,440 states and 11,939 orbits, and the endpoint survives.
  Arity six, a quarter done, already flags the n17 analogue of n11’s first field, the
  wall row plus one; n11’s fields reached arity seven.
- **The global half looks affordable in order of magnitude, not yet in fact.** If n11’s
  13% non-field residue transfers, the geometric residue is about 5,500 leaves at 24
  cells, 17,000 at 25. The engine is n11’s own, so the producer is the cost.
- **First experiment:** certify the 24-cell cover exactly, then measure the residue of
  isolated sub-pattern exclusion with an admitted instrument, with the endpoint as
  positive control and n11’s mask-0 field as the method control.

## 1. How n11 Made Its Census Tractable

Measured from the record; every number has a source.

**The cover.** Sixteen closed Voronoi cells over the normalised centre box, each of
physical diameter strictly below one
([PROOF.md](../../../packing/resources/web/n11-optimality-2026-09-29/source/PROOF.md),
lines 177–205). The retained cover receipt (`receipts/d4-independent/objects/df7938d9…`)
records physical diameters from $0.939$ to $0.975$, five four-sided and six six-sided
cells, and an average physical area of $0.517$. It also records what the cover replaced:
a 20-cell cover with 167,960 eleven-cell selections, reduced to 4,368 by the factor
$1615/42$. The cover has only the half-turn symmetry $j\mapsto15-j$; D4 enters at the
end through the overlay bridge (PROOF.md, lines 325–392), not through the census.

**The count.** $\binom{16}{11}=4{,}368$ raw masks, 2,184 after the half-turn (lines
207–211). Five empty cells among sixteen is what makes the binomial small.

**The exclusions.** 2,180 cases: 1,904 *field* and 276 *non-field* (census contract
review, lines 161–176 and 2383–2385). A field certificate names required owners $O$,
charged cells $P$ with thresholds $q_i$, and a budget $b$ equal to the sum of its point
and majority-hull feature weights; it excludes a mask $J$ exactly when $O\subseteq J$
and $\sum_{i\in P\cap J}q_i>b$ (lines 133–143). Each feature has capacity one because
two disjoint strict cores cannot both contain the same median projection (lines
754–764). The first field, mask 0, is the whole mechanism in one packet:
$O=\lbrace0,1,2,3,6\rbrace$, the bottom row and one cell above it; one five-site feature
of weight one; cells 1 and 2 each forced to take it, so charge two exceeds budget one;
459 cases excluded (lines 336–347 and 426–439). A field is therefore an **isolated
forbidden sub-pattern**: those five cells cannot all be occupied in any packing at the
cap, whatever the other six do.
Transfer is by containment (PROOF.md, lines 690–696). All 46 field packets replay with
18,855 checked rows and 4,464 ownership checks (lines 180–186).

**The non-field residue.** 273 sequential wall-seed cases, one closed centre partition
(case 1383) and two cases needing earlier D4 centre halfplanes (lines 241–242). The
centre partition is a branch *inside* one geometric exclusion, splitting owner 13 at
centred height $4/3$ into two closed leaves (lines 291–303), not a refinement of the
census. Cost: 32 cases took 20,359 CPU-seconds, about 636 each (lines 2376–2380); case
1383 took 2,111 CPU-seconds over its two branches (lines 2358–2367).

So n11 was tractable for three reasons: a minimal capacity-one cover, a sub-pattern
engine that covered 87% of the cases from 59 local certificates, and geometric exclusion
only for the 13% that are locally consistent everywhere.

## 2. The n17 Census Is the First Problem

The H259 grid has sixteen capacity-one wall cells of side $a=919/1250$ and nine
capacity-two interior cells
([mixed-capacity review](review-2026-10-01-n17-mixed-capacity-cover.md), lines 112–188).
Its 161,100,756 states (line 296) lie between $\binom{30}{17}$ and $\binom{31}{17}$: the
grid behaves like a 30-cell capacity-one cover.
The two free cuts leave 61,563,363 states and 7,703,312 orbits
([route receipts](../../../packing/campaign/explorations/X048-route-review/receipts/route-census.txt)).
No per-case engine recovers from a census that large; n11 would have needed one 37 times
smaller than its own 20-cell cover to be where n17 is now.

### A 24-Cell Capacity-One Cover (Exploratory)

The wall lemma of the mixed-capacity review bounds the separating gap by $at-1-c(t-1)/2$
with the cell’s depth and width both equal to $a$ (lines 129–141). The same derivation
with depth $d$ and tangential width $w$ gives

$$
g\le c\,d+s\,w-1-\tfrac{c}{2}(c+s-1),\qquad c,s\ge0,\ c^2+s^2=1,
$$

so a wall cell has capacity one whenever the maximum of the right-hand side over the
quarter circle is negative.
That maximum is a one-variable trigonometric bound an exact checker can take at rational
angle intervals. Numerically, depth $0.911$ admits width $0.705$; depth $0.735$ admits
$0.835$; a square corner cell is admissible up to side $0.798$ (`cover_design.py`).

Deeper wall cells shrink the interior, which is where diameter-one cells are expensive.
The design that came out of a search over ring shapes and D4-symmetric interior sites:

| Part | Cells | Shape | Capacity argument |
| --- | ---: | --- | --- |
| Corners | 4 | $0.78\times0.78$ squares | wall lemma, $F(0.78,0.78)<1$ |
| Sides | 12 | three per wall, width $0.7053$, depth $0.911$ | wall lemma, $F(0.911,0.7053)<1$ |
| Interior | 8 | Voronoi cells of four axis sites at $0.516$ and four diagonal sites at $0.583$ from the centre, clipped to the $1.854$-square | diameter $0.960<1$, inscribed discs |

The sides overlap the corners on $0.13$-squares, which a cover allows; the deterministic
seam rule of H259 carries over.
Raw states $\binom{24}{17}=346{,}104$; Burnside over the eight symmetries (fixed counts
$346104,660,660,0,660,0,0,660$) gives **43,593 D4 orbits**. Five interior cells failed
(diameter $1.31$), nine failed ($1.02$ to $1.08$), and four side cells per wall need
depth $0.97$ and reach only $N=28$.

Two things did not transfer from H259. The $s(6)$ and $s(10)$ cuts exclude nothing here:
every group of up to six cells has a dilated box larger than the threshold, as in n11,
because the cuts only bit against capacity-two cells.
And the endpoint, embedded at $(U-S)/2$, occupies seventeen distinct cells and survives,
but square 13 sits $0.0023$ below the ring seam at depth $0.911$ and slides along $v$ by
up to $0.07$, so the endpoint family straddles two states, as the route review warned
for H259 (lines 162–170). Square 9 has margin $0.014$, the others at least $0.04$.
BC-410 should either move the seam, at the price of more cells, or let the interior cell
above square 13 overlap the ring down to depth $0.85$ if its diameter allows, which
keeps $N=24$.

| Cover | States | D4 orbits | Source |
| --- | ---: | ---: | --- |
| H259 grid, no cuts | 161,100,756 | 20,155,518 | H260, exact |
| H259 grid, $s(6)$ and $s(10)$ cuts | 61,563,363 | 7,703,312 | lane B, exact |
| 24-cell capacity-one cover | 346,104 | 43,593 | exploratory |
| 25 or 26 cells, if the seam fix costs cells | 1,081,575 or 3,124,550 | about 135,000 or 391,000 | arithmetic |

### Which of n11’s Mechanisms Transfer

| Mechanism | Verdict | Why |
| --- | --- | --- |
| Minimal capacity-one cover | Transfers, and is the largest single factor | $N$ drives $\binom N{17}$; 24 cells is 177 times below the cut H259 count |
| Isolated sub-pattern (field) certificates | Transfers; this is the engine | Local geometry at n11’s cell scale; first proxy below |
| Pair-level floors on adjacent cells | Weak alone | Every adjacent pair is feasible; arity three and four are all feasible on the 24-cell cover |
| Finer or adaptive grids | Wrong direction for bulk | More cells raise the census; n11’s centre partition was a branch inside a leaf, usable there |
| Joint (cell, orientation-class) states | Wrong direction for bulk | Multiplies the census; useful as a branch inside a leaf, as n11’s angle rows are |
| Per-pattern LP or area relaxation | Dead as additive floors | Lane B’s 30,966-orbit ceiling; the pairwise and higher terms are sub-pattern certificates again |
| Wall-layer counting | Refuted as a row cap, absorbed by the cover | Five fit in a wall row at depths $0.178$ and $0.735$ (`route-wallrow.txt`), both inside the $0.911$ ring; the ring’s capacity-one cells carry what the row cap cannot |
| Global charge at the cap (R068 type) | Dead unconditionally | Lane B; the local conditional form is exactly a field |

### Asymmetric and Multi-Charge Floors

The [charge-floor pilot review](review-2026-10-02-n17-charge-floor-pilot.md) narrows
lane B’s ceiling to a single D4-symmetric linear floor vector, and its hill-climb over
free asymmetric vectors in $\mathbb R^{25}$ reaches 6 orbits (28 states) in 33 steps
(`exp-243/audit/asymmetric.log`). That is a combinatorial existence statement: the orbit
test, a maximum over eight images, is D4-invariant and convex, so its universal floor is
$\operatorname{conv}(D4\cdot n^{\ast})$, one orbit.
What a charge would need to realise such a vector is the question, and three facts of
charge accounting answer it in the no-go direction.

- **Tightness.** Excluding everything but the endpoint’s orbit needs
  $\sum_i f_i n^{\ast}_i$ within a hair of the budget $M$, so every endpoint square must
  sit at a minimum-charge pose of its cell and the family must capture every resource:
  no weight may lie in any hole of any family member or translate.
  The route review is right that a piecewise-constant charge can be tight on a family
  (line 213); it must be tight on *every* member, including the $0.07$ slide of square
  13 and the $0.11$ slide of square 6, and on the $0.00027$ translations the cap allows.
- **Empty common cores.** Non-uniformity needs the seven empty cells to carry floors
  above $M/17$ while the seventeen used cells sit at about $M/17$. A cell’s floor is its
  least-capturing pose, and the poses of one cell share only the common core of all unit
  squares with centres in it, which is empty once the cell’s circumradius exceeds $1/2$:
  every cell of this cover ($0.55$ to $0.57$), every H259 cell ($0.52$), and every n11
  cell. So a far pose captures only what it scavenges from neighbours’ footprints, and
  that weight is exactly what fixes the neighbours’ own floors.
  Lane B’s floors of $0.06$ to $0.93$ of $M/17$ are this mechanism measured on one
  charge; a rebuilt charge moves weight between cells but cannot create a core.
- **Families and refinements.** A family of charges is a disjunction of linear tests,
  each separately valid and each subject to the two points above; orientation-refined
  states multiply the census before any of them bites.
  Superadditive pair floors and owner-conditional floors escape, but a conditional floor
  whose power comes from a collision region is a field: in mask 0 the charged cells
  carry threshold one, the whole budget, because the owned points of the required owners
  make the alternative poses impossible, not because of charge bookkeeping.

The decisive instrument is cheap and one-sided: a linear programme over a point measure
on a fine grid, with capture constraints for sampled poses in every cell, maximising the
least empty-cell floor subject to the endpoint family being tight and the used cells
holding $M/17$. Point resources relax majority features, whose capture is decided at a
single median position, so an LP value below the hill-climb’s empty-cell floors would
show that no charge of R068’s kind realises them at $U$. I expect that outcome, for the
core reason above, and I would run it before any charge is rebuilt.
It does not change the engine recommendation: the sub-pattern engine takes its power
from collision, which is where the n11 record says it was.

## 3. The Engine: Isolated Sub-Pattern Exclusion on the Minimal Cover

A sub-pattern of cells $G$ is forbidden when $|G|$ unit squares with centres in the
closed cells of $G$, each inside the cap container, cannot have disjoint interiors.
n11 proved such statements with a majority feature and owned points; the same claim can
also be closed by the ownership induction of its geometric kernel on $|G|$ owners.
Either way the certificate is local, replays in seconds, and transfers to every state
containing $G$.

**Proxy.** `local_feasibility.py` decides feasibility heuristically: 2,048 random pose
tuples per group, then a 192-candidate evolution-strategy descent on a penalty built
from separating-axis penetration, wall containment and cell halfplanes.
A verdict of feasible is witnessed; a verdict of infeasible means the search found no
witness with penalty below $10^{-7}$, so the forbidden family it reports is an
over-estimate, and the survivor count an under-estimate for these arities.
Results on the 24-cell cover, all groups whose centroid box has side at most $3.0$:

| Arity | D4 classes tested | Infeasible classes | Survivors (states) | Survivors (orbits) | Endpoint survives |
| ---: | ---: | ---: | ---: | ---: | --- |
| 3–4 | 137 | 0 | 346,104 | 43,593 | yes |
| 3–5 | 7,089 | 10 | 94,440 | 11,939 | yes |

The ten classes are all crowds of four or five squares among the eight interior cells
and their nearest ring cells; the least cramped has proxy penetration about
$2\times10^{-3}$ and the most about $0.024$. The full wall row of five cells reached
penalty $1.3\times10^{-9}$, a touching configuration, which agrees with the wall-row
receipt and with the endpoint, whose bottom row is exactly that pattern.
Under the strict $10^{-12}$ tolerance that pattern was flagged and the endpoint was
wrongly excluded; the control caught it, and the table uses $10^{-7}$. Dropping the two
weakest classes as well leaves 14,870 orbits.
The arity-six sweep (17,052 classes) was 26% through when this lane closed, with eight
flagged classes, five of them the full wall row plus one cell above or beside it, the
exact analogue of n11’s mask-0 field; it continues in `lf_a6_r3.log`.

**Estimate.** Arity five already removes 73% of the orbits.
n11’s fields ran to arity seven and left 13%; on 43,593 orbits that is about 5,500
geometric leaves, and 1% would be about 440. Both are inside the route review’s $10^3$
to $10^4$ window (lines 186–193). On a 25-cell cover the same fractions give 17,000 and
1,350. These are conjectures on top of an exploratory count; the arity-six run started
at the end of this lane will sharpen the first.

**Cost to build.** The producer is the part n11 does not publish.
Each certificate is a four-to-seven-owner problem at the n11 cell scale, so the owned
point, row cover and feature steps of the v9 kernel apply unchanged; a sub-pattern
closed by ownership induction alone costs a fraction of a 636-CPU-second case.
A few hundred certificates at minutes each is hours of CPU. The engineering is the
adapter from the n17 cover to the kernel’s frame and an exact checker for the
generalised wall lemma, both small.

## 4. The Architectural Question

The H259 occupancy census was the wrong first cut, for a reason that is arithmetic
rather than geometric: a mixed-capacity grid counts like a 30-cell cover, and n11’s own
record shows a cover reduction of 38 times being the step that made its census fit.
The occupancy *idea* is right; the instance is 20 times too coarse.

**Orientation-first census.** Branching on which squares are tilted (the endpoint has
six at $39.8^\circ$ and one at $-36.6^\circ$) does not reduce the census, because every
cell admits every orientation and nothing excludes a tilted square from a cell without a
local argument. It is the right branch *inside* a geometric leaf, where n11 used angle
rows.

**Hybrid with counting certificates below $S^{\ast}$.** An R068-type certificate at a
side below the endpoint proves a strict bound there and cannot reach $S^{\ast}$ (route
review, lines 204–212). Conditioned on an occupancy pattern it becomes a field; lane B’s
pilot tested the unconditional form and found it collapses.
The hybrid route’s rank-one choice is therefore right in shape, with the engine being
local fields rather than per-cell floors.

**Is the global half affordable?** In order of magnitude, yes, on three conditions: the
24-cell cover certifies exactly with the seam fixed; the sub-pattern residue at arity
seven is at most a few times $10^3$ orbits; and the per-leaf cost of geometric exclusion
is near the 1–2 CPU-hour estimate, which BC-411 measures.
Then the geometric residue is of the order of $10^4$ CPU-hours, which is weeks on a
modest cluster, plus the D4 bridge and capture that the capture review prices.
If the residue is $10^4$ to $10^5$ orbits the route is not affordable without a second
engine, and the honest next question becomes whether larger-arity sub-patterns keep
paying, which the arity sweep measures directly.

## 5. First Experiment

Build the cover instrument before the engine, because the engine’s residue is only
meaningful on the cover it will run on.

1. **Exact 24-cell cover (BC-410).** Rational cells, the generalised wall lemma checked
   on closed angle intervals, interior diameters by exact vertex pairs, D4 action and
   Burnside count, and the endpoint family inside one state with margin.
   Falsifier: no D4-symmetric cover with $N\le25$ holds the whole family in one state.
   Cost: a day.
2. **Sub-pattern residue (replaces BC-408’s floor test).** On that cover, run the
   heuristic sweep to arity seven as a *selector*, then prove each selected pattern with
   the n11 kernel adapted to the n17 frame, and count the exact residue.
   Controls: the endpoint state must survive every step; mask 0 of n11, replayed through
   the same adapter at n11’s cap, must reproduce its 459 exclusions.
   Falsifier: the certified residue exceeds $10^4$ orbits at arity seven.
3. **Per-leaf cost (BC-411)** on a uniform sample of that residue, as the route review
   already scoped.

## Hypotheses to Register

**H-F1: a minimal capacity-one cover for n17.** *Claim:* at $U=1169/250$ there is a
D4-symmetric closed cover of the centre box by at most 25 cells of proved capacity one,
with the H256 endpoint family, sliders included, inside one occupancy state with margin
at least $10^{-3}$. *Falsifier:* every such cover needs 26 or more cells, or the family
straddles a seam in all of them.
*Threshold:* $N\le25$ gives at most 135,196 orbits.
*Instrument:* an exact rational checker for the generalised wall lemma, cell diameters,
coverage, the D4 action and the Burnside count, with the endpoint as positive control
and the H259 falsifier pair as a negative control.
*Cost:* one build day, seconds to run.

**H-F2: isolated sub-pattern exclusion leaves at most $10^4$ orbits.** *Claim:* on the
H-F1 cover, the forbidden sub-patterns of arity at most seven, each certified by the n11
kernel or a majority-feature packet, leave at most $10^4$ D4 orbits containing the
endpoint’s. *Falsifier:* the certified residue exceeds $10^4$, or the endpoint state is
excluded by a certified pattern.
*Threshold:* $10^4$, with $3\times10^3$ as the comfortable mark.
*Instrument:* the heuristic selector of this lane as a retained tool, the adapted v9
kernel as prover, an exact set-union consumer; n11 mask 0 as the method control.
*Cost:* a week to adapt the kernel, hours of CPU for the certificates.

## Evidence Status

| Kind | Items |
| --- | --- |
| Measured from the record | n11 cover geometry and the 20-cell comparison; the field rule and the mask-0 packet; the 1,904/276 split; replay costs; H259 and lane B counts; the wall-row receipt |
| Exploratory, this lane | The generalised wall-lemma table; the 24-cell cover and its Burnside count; the endpoint margins; the sub-pattern proxy and its survivor counts |
| Derived here, needing review | The depth–width form of the wall lemma; the reading of a field as an isolated sub-pattern; the leaf estimates from n11’s residue fraction |
| Conjecture | That n11’s 13% non-field fraction transfers; that the ten flagged classes are truly infeasible with certifiable margin |

The scripts and their outputs are in the session scratchpad
(`scratchpad/lanes/f/cover_design.py`, `local_feasibility.py`, `cover.json`,
`lf_a5_r3.log`), outside the record for the same reason as the X-048 scripts: the lint
floor admits no unlinted Python under `packing/`. Every number from them is planning
evidence until an admitted instrument reproduces it.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
