# Eleven squares in a square: the result, the method, and who did what

> **Start here — 2026-09-10, commit `7d21d1df`.**
> The one canonical table of what is proved, checked and open is **[`05_status_sheet.md`](05_status_sheet.md)**.
> The capped compute plan, with its rates, its pilot and its stop conditions, is
> **[`06_compute_plan.md`](06_compute_plan.md)**.
> This page is the two-page brief. It does **not** claim a complete optimality-and-uniqueness proof is ready
> except for purchasable compute; three Lean obligations are open, two classes are theory-limited with no priced
> route, and no k0 cell is closed.

*Living document, edited in place. Status as of 2026-09-10 (night).*

**Tag legend — identical in every writeup document, and in `05_status_sheet.md`.**

| tag | meaning |
|---|---|
| **[T]** | proved in prose, in a named `docs/proofs/*.md` note; not formalised |
| **[L]** | Lean-checked, no `sorry`; where `native_decide` is used the axiom roster says so |
| **[C]** | certificate-backed **under a named verifier and its sha** — a `[C]` that does not name its verifier is not a `[C]` |
| **[P]** | pending computation; a **priced** route exists, and the price is in `docs/budget.md` |
| **[O]** | **open proof obligation** — specified, not proved; no priced route until it lands |
| **[M]** | measured (a number from a run, with the run cited) |
| **[S]** | supported by evidence, not proved |

*The verifiers `[C]` can name: **frozen v1** `attempts/A57-shadow-trees/code/verify_case.py` sha `521cb01fe656`;
**measure** `certs/verify_measure.py` sha `2a735939d67f`; **v3** (polygon cores) `f578a8c9346c`; **v4** (windows
clause) `b36acb012f42`; **v5** (guard-line clause, post-fix) `f93958cca421`. Attempt notes older than 2026-09-09
sometimes use [C] for "open"; here it never does.*

## The question

Take eleven unit squares. What is the smallest square box they all fit in, with no overlaps and any rotation
allowed? The best known arrangement, found in 1979 and never beaten, uses a box of side about 3.8771. Nobody
had proved that nothing smaller works, and the gap between what was known and what was believed had stood
for roughly fifty years. This lab's goal is that proof: the minimal side is exactly the known value, and the
known arrangement is the only way to achieve it, with every step of the argument either a checked proof or a
certificate a computer can verify independently.

## What is established now

- **Bounds.** The side is at least 3.82 and at most 3.877084. The lower bound is certified [C]; the upper bound
  is the exhibited packing. The remaining question is the window between them.
- **The window scoreboard is full; the classes are not all closed.** The problem splits into classes by how
  many squares sit "simply" in a corner slot of the box. The designated window scoreboard stands at 52 of 52
  rows certified by the frozen verifier [C] (`521cb01fe656`), and the neighbourhoods of three exact local minima —
  S07, S02 and now S33 — have Lean-checked closures [L]. What remains open, by family: the two A57 window trees
  (k5_11, k5_16) [P, ≈ 1,800 CPU-h]; the trump5 residual [P]; **fourteen** protected classes [P, ≈ 3,800 CPU-h];
  **corners4 and k4_05, theory-limited with no priced route** [O]; and k0, the family with no simple corner-slot
  square at all. For k0 the reduction to "every corner met by two squares" rests on the K0-O1 transfer, not on
  the definition. Its diagnostic residue is eleven converged-alive cells; the exhaustive frontier behind them
  also carries unresolved certificate candidates (A115's pool of 128 in 166 open records), and the gallery is a
  **review interface** — 71 pages, 56 alive, a 3.8 % sample of 1,693 alive records — **not the covering manifest**.
- **The complete theorem is conditional.** The top-level Lean statement still names three obligations:
  `stratum_kill` (the stratum kills per class), `trump_residual` (the Trump residual), and `a22_exact_structure`
  (the exact structure of the minimiser). The composition route refines them; it does not discharge them.
  Twelve other named axioms have been discharged; `sat_selection` is a theorem since A126.

### Last night's numbers (2026-09-09/10)

- **The first k0 node kills under the frozen chain [M].** A191 ran the combined cascade leaf on `l1_104`:
  **17 of its 64 alive S2 nodes** die by the exact-core LP at budget 8 (τ = 7.000 < 8) and **23 S3 nodes**
  (10 fine, 13 coarse) die the same way — all 40 **PASS the frozen v1 `521cb01fe656`**, conditional on K0-O1 as
  every cascade kill is. 19 further S2 nodes are unconverged **kill candidates**, and candidates are not
  certificates. **No cell is closed**, and no whole k0 gallery cell has ever been closed by this cascade. Earlier
  attempts record root-cell kills (A115: 22) and conditional lane kills (A141). A closed cell would be a pilot
  with a measured price, **not** a theorem that the rest is compute.
- **The S3 price [M].** `l1_104`'s S2 layer costs 305 s per node (5.4 CPU-h for the layer); its S3 layer is
  **5,432 nodes at 239 s = 360.5 CPU-h = 23 instance-hours at 16 vCPU**. Below S3 nothing is measured, and the
  whole per-cell price turns on that: **1,375 CPU-h** if the S3 layer closes the cell, **4,245** at a deep kill
  rate of 0.99, **359,647** at the 0.95 the S3 sample itself measured. Eleven cells is an *upper* envelope — the
  canary `l1_153` has one alive S2 node against `l1_104`'s 64. Measuring the S4 rate is the single highest-value
  experiment in the project, and it is lane 3 of the pilot in [`06_compute_plan.md`](06_compute_plan.md).
- **corners4 and k4_05 are theory-limited, with named fixes [M/O].** A193 ran the full k0 toolkit on both.
  *corners4* (k4_13): at s0 every one of six complete assignments returns the same answer — the geometry
  localises the meeters (hulls of area 0.1–0.7, cores on three of five), the no-room leaf cannot pocket the
  centre block (residue 5.90), no guard line is ever active, and the LP sits at **τ = 11.000000 exactly with a
  half-integral support** (14 placements at weight ½; the largest near-disjoint sub-family is 5 of 14, so it is
  not two near-packings averaged). **The missing object is a pair row**: two distinct meeters of one slot box
  cannot both be half-present. *k4_05*: two open k5 extensions put Lemma-K1 witness images inside every LP — the
  root's τ = 6.965 < 7 is not a kill, its certificate fails with 58 holes **at the k5_11 slot pose**, and the
  re-solve lands at **7.189 > 7**; 0 of 3 s0 leaves certify, all three re-solves reaching or crossing 11. **The
  missing clause is NoFam semantics for window rows**, which the δ-resister split needs and v4/v5 cannot state.
  This refutes the working conjecture that the tools which closed the k0 cell would carry to the other classes,
  and it refutes it for identifiable reasons rather than by running out of time.
- **The Lean roster grew [L].** A192 closed, with no `sorry` and no new axiom: the **windows clause end to end**
  (`windowed_dead`, `checkWindowsI_kill_of_check` — no geometric hypothesis left), **Lemma LINE-1 and Theorem G**
  at set level (the checker half remains [C]), **Theorem FC Steps 1 and 2**, the **no-room lemma**, and the
  **S33 `LocalDead` kernel** at (0.05, 10°) (`localDead_s33_t`, a 3,800 s `native_decide` build).
- **A verifier soundness bug was found by external review, reproduced, and fixed.** v5 accepted a declared
  right-hand side *smaller* than the one it re-derived, which the proved inequality does not license; a
  four-line certificate then "proved" that one unit square does not fit in a box of side 3.877084. Fix:
  `f590c4db`, `12f8b9c6` — the declared RHS must equal the derived one exactly. **All six v5 kills replay PASS**,
  and four certificates (`Y0027`, `Y0230`, `Y0241`, `Y0249`) turned out to carry no guard-line term at all and
  **PASS the frozen v1**, so they were relabelled into the frozen chain. The adversarial case is committed as
  `attempts/A190-guardline-clause/tests/repro_v5_false_kill.json`. Related, and found the same way: LINE-1 as
  written for *interior*-disjoint squares is false (the 2×2 tiling of `[0,2]²` on `y = 1`); Lean states it for
  strict closed-disjoint families, which is what the certificate bridge supplies.

## How the proof works, in plain terms

Every candidate arrangement is described by where each square's centre is and how it is turned. The proof
never searches for arrangements. It does the opposite: it assumes a region of possibilities and shows the
region is empty, by one of two kinds of argument.

1. **Counting arguments turned into linear programs.** If some squares are pinned to a region, the area they
   must cover and the walls they must touch leave less room than the other squares need. A linear program
   finds the contradiction, and a small certificate lets anyone re-check it exactly. This is the workhorse,
   and it is expensive: tens of minutes per case, thousands of cases.
2. **Geometry.** Before any linear program runs, the region is shrunk by facts that need no computation at
   all: a square that must sit here cannot also sit there; two squares that must share a point are the same
   square; a corner met by two squares forces one of them into a narrow band along a wall; a square pulled
   diagonally away from a corner leaves no room for the partner the corner requires. Each such cut also grows
   the "core" every pose of a square must contain, which cuts the neighbouring squares in turn. Done to a fixed
   point, the geometry removes most of the tree before the linear programs see it.

The order of these two, geometry first and to a fixed point, then linear programs only where geometry runs
out, is the central lesson of the lab. Whether the remaining search is compute-bound is an empirical forecast
from measured kill rates and per-node costs on representative branches, and it is stated that way below.

## What each party did, from the record

The AI built the pipeline: the certificate format, the frozen verifiers, the Lean formalisations and checkers
(using Lean and Mathlib; the trusted kernel is Lean's own, and the axiom audits record where `native_decide`
is used), the case trees, the linear programs, the galleries of thousands of drawings, and the process that ran
them across weeks of compute. This is not a controlled comparison with either party working alone; it is what
happened in this collaboration and which suggestions preceded which results. Concretely:

- The idea that makes the whole proof tractable, stratifying by how many squares sit simply against the box,
  came from the PI, not the AI.
- Twice the AI built multi-square case trees on boxes it had not clipped against each other, producing
  pictures of squares overlapping and leaving the container. The PI saw it in the drawings; the AI had not.
- The AI's clipping code rebuilt cores from a bounding hull, throwing away the growth that makes cuts
  propagate. The PI asked whether the polygon grew on the far side of a clip; it did not; the fix followed.
- The AI's cascade clipped against small inscribed squares rather than the true polygon cores. On the page
  that showed it, one square's outline crossed two neighbours' cores while the printed numbers said nothing
  had been cut. The PI read the picture; the corrected clip kills that node outright.
- Several of the PI's readings were wrong too, and the drawings said so: a hairline grazer the eye cannot
  see, a lane the PI thought open that a certified polygon closed. The loop corrects in both directions.

## Where the levers came from

Most of the proof's geometric leaves began as a spatial reading by the PI on a drawing, which the AI then turned
into a lemma, a test against the certified geometry, and a script that applies it everywhere. The record
(`03_lab_timeline.md`, section 3) has each episode with dates and attempt numbers; the short list, PI's reading
first and the AI's formalisation second:

| the PI's reading | what it became |
|---|---|
| stratify by how many squares sit simply against the box | the class frames the whole proof is organised by (A53) |
| search bidirectionally: a breadth-first sweep from the outside (the case tree) meeting an inside-out set of targets (the basins around the known minima and the drains toward them), so the tree never has to reach the bottom on its own and its asymptotic blow-up is cut | the basin-and-drain route the case trees run on: local certificates around the exact minima, drains, and the tree only down to where a basin or a drain takes over (A29, A30, the drain and basin notes) |
| grow basins anisotropically, along the directions the packing can actually move, not as balls | the asymmetric-width certificates and the slide and common-tilt chains (A151, A160, A163) |
| "chords along a line add up": the Y0147 page carries a pin, H and two free columns for more than the side | the guard-line row and its verifier clause (A144, A190), six pages dead the night it landed |
| a corner not holding a simple square must be met by two distinct squares, or the packing climbs to a dead class | Theorem FC on forced cells, the slot-lane kill, the assignment construction (A141, A178, A180) |
| one meeter of a doubly-met corner sits in a band along a wall; the deepest second meeter is a csc(theta) construction | the sideband lemma in its sharp cell form and the requirement theorem, Lean-checked in part (A169) |
| a first meeter must leave room for its partner; place the forced meeters before branching on the two-meeter ones | the coexistence cut and unit propagation before branching (A168, A180) |
| the pinwheel's basin should grow along f0's slide and the common-tilt grain | the S02 basin as a union of certified boxes across three class frames (A160, A163) |
| a clipped box's polygon must grow on the far side of the clip, and the growth must propagate | the per-piece core rebuild and the parent-seeded fixed point (A172, A181) |
| "H is still allowing solutions that intersect S's core" on a page | the axis-core clip defect found and replaced by the polygon clip (A175) |
| "I only see ten squares; how does this admit an eleventh?" | the no-room leaf, five nodes dead the same night (A189) |
| union all the pins and pick five squares that satisfy all of them at once | the simultaneous assignment cover (A180) |
| confine the LP's adversary to the designated boxes | the window clause, seven budget-zero assignments dead (A185) |
| force geometry to a fixed point before any LP; drop the fine pass; test B before S; short-circuit by wastage | the standing order of the cascade and the knob experiments (A184) |
| "can the whole solution set be a basin?" | the basin map, which showed the residue clustering on a side-4 plateau, and the line certificate (A187, A188) |
| how much does a non-simple corner hurt, and can grain coverage carry high-k kills down to low k? | the descent programme (A194) |
| two millisecond pair exclusions: meeters' centres a unit apart (inscribed discs), and a chord row that leaves budget for one unit chord, not two | the first tests of the fast propagation engine (A198), which kill in milliseconds what the fine pair test took 1,310 seconds to say |
| a meeter reaching around a pin's corner is forced into one rotation and seals the neighbouring slot's top edge, so that slot cannot be met from above | the corner-sealing lemma and its window slabs (A199); on Y0491 the pad was the only thing keeping the page alive |
| "something about torque being an invariant that prevents all four corners from being pinned like that" | the torque probe (A217: no sign-rule invariant, but no Fritz-John point with four doubly-met corners) and its counting form (A218): Lemma PUSH, two meeters of an open corner push each other out along their walls, and Lemma HOLD, proved for every n; the count itself refuted by a nine-square force-balanced ring and by rattler crowds, so the k0 obligation stays with the drain |

Not every reading survived: several were refuted by the drawings, hairline grazers the eye cannot see or a lane a
certified polygon closed, and those are listed in the timeline too. The point is the direction of the traffic.
The PI supplies lateral, spatial reasoning that the AI does not generate on its own; the AI supplies the
formalisation, the certificate, the test, and the application to every case at once. In this record the leaves
came from the two halves together, and the leaves are where the kills came from.

## Three episodes, in pictures

*Each figure below is the actual page the loop ran on. For each: what the PI read, what changed or was refuted,
the exact measured effect, and what is still not closed.*

### 1. "Chords along a line add up" — the guard-line row

![The guard line on k5_11_interior_Y0147 and its four chords](figures/A144_k5_11_interior_Y0147_guardline.svg)

**The original reading.** On the `k5_11_interior_Y0147` page the PI saw a pin, the hypothesis square H and two
free columns all crossing one horizontal line about 0.99 below the top of the box, and read off that their
chords along that line already added to more than the box's own side could allow. The node's LP had recorded
τ = 5.000000 against a budget of 5 — dead level, no kill.

**What it became, and what was refuted.** The reading became **Lemma LINE-1** (the chords of a family of
squares on any axis-parallel line sum to at most the side) and **Theorem G**, a new row in the certificate
language, with a verifier clause (A144 → A190 v5). Two things about it were then refuted, both by exact
argument rather than by opinion: (i) LINE-1 as first written, for *interior*-disjoint squares with closed
chords, is **false** — the ordinary 2×2 tiling of `[0,2]²` puts four unit chords on the line `y = 1`; the true
statement is for **strict, closed-disjoint** families, which is what the certificate bridge supplies after
dilation, and that is the form Lean proves (`chord_sum_le_side`). (ii) The v5 checker accepted a declared
right-hand side smaller than the one it derived, which lets a certificate claim more than the lemma gives.

**Measured effect [M].** The line at `h = 2.887084` gives four chords; the family line `grid h 6/8` at 2.907813
gives the identical four. **Six gallery pages died the night the clause landed**, at τ = 4.0000, 4.7500, 4.8773,
4.8775 and 4.8896 against budget 5. After the soundness fix (`f590c4db`, `12f8b9c6`) **all six replay PASS**,
and four further certificates turned out to carry no guard-line term at all and PASS the **frozen v1**.

**Remaining limitation.** Theorem G is [L] only at set level. The checker half — `minchord_of_box`,
`checkBoxesDisjoint`, `checkCornersFar`, `checkCoreOffPiece` — is **[C]**, and the residual Lean obligation is
exactly `clo l j ≤ chordLen (lines l) (Q (own j))` plus three distinctness facts. The T3 test still enshrines
the old inequality direction and needs rewriting.

### 2. "Does the polygon grow on the far side of the clip?" — hull versus per-piece cores

![K′ rebuilt from the union hull (before) versus the exact intersection of the per-piece K′ (after)](figures/kprime_pieces_S2.svg)

**The original reading.** The cascade's clipping step reported that the invariant held and that boxes had been
cut, yet on the drawn page the *core* — the region every pose of a square must contain — was not growing where
it visibly should have. The PI asked whether the polygon grew on the far side of the clip.

**What it became.** It had not. `multibox.normalise` rebuilt each core from the **union hull** of the surviving
centre pieces, which throws away exactly the growth that makes a cut propagate to the neighbours. The fix (A172)
rebuilds the core as the **exact intersection of the per-piece cores**. In the figure the band between the
dashed outline (the core the clip actually used) and the solid one (the true per-piece intersection) *is* the
discarded growth; after the fix the dashed line lies on the solid one.

**Measured effect [M].** On the A168 S2 node `BR139/TRH-25`, same settings (nsub 4, refine 3): role **H** kept
fraction 0.4408 → **0.3584**, core used 0.6580 → **0.7308**, pieces 26 → 22; role **D** kept 0.0882 → **0.0722**,
core used 0.7401 → **0.7937**, pieces 14 → 12. Role B1, already tight, did not move. Crucially, **kills computed
on the old fixed point still stand** — the hull core is a subset of the true one — so only ALIVE verdicts were
ever weakened. The same defect, in a second form (clipping against small inscribed squares instead of the true
polygon cores), was caught later on another page and fixed in A175; the parent-seeded re-normalisation of A181
follows from the same principle.

**Remaining limitation.** The fixed point is now per-piece and parent-seeded, but computing it is expensive: the
per-piece core build was four-fifths of a 570-second wall on one node until the intersection was restricted to
the host piece. Geometry cost is the reason the cascade runs a coarse pass first, and A184 measured that choice
(mean S3 cost 41.7 s coarse against 263.9 s fine, for one verdict change in 64 cases) — which supports
coarse-first but does **not** establish the price of the whole search.

### 3. "I only see ten squares; how does this admit an eleventh?" — the no-room leaf

![The no-room leaf killing c0_Y1033's STEP 34 node by geometry alone](figures/noroom_c0_Y1033.svg)

**The original reading.** On the STEP 34 page of `c0_Y1033` the PI counted the drawn squares, got ten, and asked
where the eleventh was supposed to go. The search had recorded that node **UNDECIDED**.

**What it became.** A new leaf (A189 Lemma 1) that needs no linear program at all: with ten roles boxed, the
eleventh unit square must lie in the container with its interior clear of every core; certify that the residue
is a small pocket, then run an exact lane cover on the pocket. If the lanes sum to less than one square, there
is nowhere for it to be.

**Measured effect [M].** Ten cores of total area 6.7320; an exact bisection of the eleventh square's
centre × tilt domain (13 levels, 8 tilt sub-bins) certifies **99.9615 %** of the root volume dead, leaving 2,594
open pieces — one connected pocket `[3.179, 3.440] × [1.522, 1.903]`. The exact lane cover on that pocket
returns **LANE = 0** (depth 21, 249 leaves, **2.5 s**). Verdict **DEAD**, with no LP and **no certificate file
to verify at all**. Five nodes died the same night.

**Remaining limitation.** The bisection alone does not finish: the pocket exists because of a **graze** — the
core of `F1` reaches y = 1.873 and the core of `H` starts at y = 1.870, three thousandths of a unit that no
piece representation can pin. That is why the lane cover is needed as a second certificate. And in Lean,
`noroom_dead` is [L] but the lane cover's own soundness and the residue cover enter as **hypotheses**, i.e. as
certificate data — closing that is an open obligation, not a proved one.

## The systems that closed the gap

The PI cannot read certificates or linear programs, and does not write proofs in the usual sense. What the
PI can do is look at a drawing of squares and see what is possible. So the lab was built around drawings:
every open case is rendered as a page with the hypothesis square at the centre of its region and at its
middle tilt, the extremes drawn faintly, the cores every pose must contain drawn solid, the pinned squares
drawn only as pins, the undecided region stippled grey and never a hopeful colour, and a note on every panel
saying what it is. A status script moves pages to a `killed/` folder as certificates land so the PI only
reads what is alive. The PI reads pages and writes readings; the AI turns readings into lemmas, tests them
against the certified geometry, and either kills the case or shows the PI why the reading fails. A reading
that survives becomes a reusable leaf that applies to every case, not just the one it came from.

That loop, drawing, reading, refutation or lemma, re-drawing, ran dozens of times a day. It is where the
proof's geometric leaves came from, and it is the part of this work that is not about squares.

## What remains, and what "compute-bound" would mean

- **Close `l1_104` [P].** The cascade with the polygon clip, the lonely clip and the partner cuts, then linear
  programs only at the geometric fixed point. Forty of its nodes are now dead under the frozen verifier; the
  cell is not. Closing it would be the first evidence the method finishes on k0 — **a pilot with a measured
  price, not a proof that everything after it is compute.**
- **Measure the S4 kill rate [P].** The eleven-cell price ranges over three orders of magnitude on this one
  unmeasured number (15,125 CPU-h if the S3 layer closes a cell; 3.96 × 10⁶ if the deep layers kill at the rate
  S3 itself did). No other experiment in the project has that leverage.
- **Land two clauses [O].** A pair row for two meeters of one slot box (corners4) and NoFam semantics for
  window rows (k4_05). Until they exist those two classes have **no priced route at all** — they are not slow,
  they are blocked, and running more compute at them buys nothing.
- **Finish the Lean composition [P/O].** The remaining local minima, the sideband requirement theorem, the
  guard-line checker-half bridge, a concrete tree-file → cover check on one complete example, and the top-level
  assembly that discharges `stratum_kill`, `trump_residual` and `a22_exact_structure`.

**What "compute-bound" would require, and does not yet hold.** A sound fixed certificate chain; every
non-computational proof and transfer obligation discharged or separately committed; an *exhaustive* manifest of
outstanding work keyed by tree and node identity rather than by page name; independently checked tree
composition; and a workload estimate calibrated on representative **complete** branches. Those five conditions
are written out with their current status as E1–E5 of [`06_compute_plan.md`](06_compute_plan.md), and none of
them is satisfied today. Until they are, the accurate description of this project is: **unconditional certified
results, a substantial formal-verification infrastructure, and a priced but only partially calibrated campaign
for the rest** — not a finished proof waiting on a purchase order.

*See [`02_mathematics.md`](02_mathematics.md) for the lemmas and their composition, [`03_lab_timeline.md`](03_lab_timeline.md)
for the full record of the interaction, [`04_related_work.md`](04_related_work.md) for where this sits among other
AI-assisted results, [`05_status_sheet.md`](05_status_sheet.md) for the canonical status table, and
[`06_compute_plan.md`](06_compute_plan.md) for the capped compute plan.*
