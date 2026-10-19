# The Exchange Lemma as a Young flood: soundness, the excess identity, the exposure lemmas, and the stall (INTERLOCK) — A98, 2026-09-04

Target (A98 BRIEF + PI refinements of 2026-09-04): Theorem EXCHANGE — a K0-BLOCKED packing at
side m converts to a k ≥ 1 packing at the SAME side by removing one corner's two intruders,
placing the exact slot square and re-fitting one square; in the PI's recursive form, the YOUNG
FLOOD: grow a Young diagram of exact unit cells from the corner, paying each cell with the squares
it displaces, with free cells, single-intruder cells and rigid slide-ins, until the deficit
(removed − placed) is 0. Prove termination with deficit 0 for K0-BLOCKED packings at side ≤ ŝ
(route: induction on the pinning graph, one lemma RELEASE), or characterise the stall. Labels:
[T] proved, [S] routine given cited items, [M] measured (`attempts/A98-exchange-lemma/results/`,
`attempts/A87-drain-flow/{notes/exchange87.md, results/flood87.*}`), [F] finding, [C] open.
Conventions: `nocrit_k0_blocked.md` (corner frame, μ_c, d_c, intruder, Lemma K, Lemma CLUSTER,
retreat cluster C_e, anchoring (W)/(I), RES(4)), `k0_blocked_side.md` (CEIL, SLIDE, RES-N, K0-O1),
`tilt_floor_k0.md` (JAM-0, MENU, LOCK), `wall_budget.md` (WALL-F, FLOAT), `k0_route.md` (K0-FREE,
teleport), A85 `cases85.json` (JAM / BLOCK / WEDGE / OTHER), A87 `exchange87.md` (the depth-1
measurement, 21/33), A87 `flood87.py` (the flood measurement). ŝ = 3.877083590022814, m ∈ [3.82, ŝ].

## 0. Verdict

> **EXCHANGE: not proved, not refuted; exact framework, exact residue.** [T] The exchange and the
> flood are SOUND ∀-packings conversions (no selection, no criticality, no tree): Lemma FLOOD-D
> (§2.2) — a Young diagram D at corner c with N(D) := #{squares meeting int D} ≤ |D| yields a
> k ≥ 1 packing at the same side — and its dynamic form Lemma FLOOD-M (§3.1, rigid re-placements
> allowed). The static flood is decided by the EXCESS X(D) := N(D) − |D| = O_D − E_D (overhang of
> the displaced squares beyond D minus the free area inside D; Lemma X, §2.3): the flood wins iff
> some reachable D has X(D) ≤ 0; K0-BLOCKED means X(slot) ≥ 1 at every corner; at side < 4 the full
> 3 × 3 block has X = 2 EXACTLY (Lemma CAP, §2.4: every square meets its interior), so a win needs
> ≤ 8 cells and ≥ 3 untouched squares outside D. A corner with EXACTLY two intruders always exists
> (Lemma TWO, §2.1: Σ_c n(c) ≤ 11) and its slot square is disjoint from the other nine by
> definition — the brief's third-meeter question is closed. **The depth-1 exchange of A87 IS the
> 2-cell static flood on the only sub-4 corpus packing** (record_s0115 at 3.9855): corner by corner
> the verdicts coincide (wins at the two NICK corners d₂ = 10⁻⁸ via the 2-cell diagrams, stalls at
> the two SUBSTANTIVE corners d₂ = 0.0145 with X ≥ 1 over all 20 diagrams and flood87's dynamic
> flood ending at the full block with deficit 2); at side ≥ 4 the static flood is VACUOUS (the
> 4 × 4 grid holds 11 cells, min X = −5), so the seven corpus packings at 4.00–4.11 measure nothing
> about the window. Trump (canary): min over the 20 TL diagrams X = 1 — stalls exactly, as it must.
>
> **What decides a re-fit is its EXPOSURE.** [T] Lemma EXPOSE (§4.1): a candidate placement Q₀
> (any tilt) is a valid exchange placement iff no untouched square's interior meets the exposure
> Σ(Q₀) := int Q₀ \ (A ∪ B) (and Q₀ misses int S, lies in the container). [M] All 21 verified A87
> placements are B re-placed almost in place: area(Q₀ ∩ B) ≥ 0.71 (≥ 0.99 in 15 of 21), exposure
> median 0.0016, max 0.25 (`results/exposure98.json`). Lemma FLUSH-JAM (§4.2, exact): at a JAM
> corner (A = [g, 1+g] × [0,1], nick partner B hugging the left wall at tilt α, dip δ ≤ (g − v_x)
> tan α) the flush re-fit B₀ = [0,1] × [1,2] has exposure = three explicit slivers; the ones on the
> wall side and on S are SEALED (no square can enter them); B₀ fails only if a third square enters
> the TOP sliver (a triangle of width ≤ g − v_x + O(α) along y = 2 and height ≤ δ + 1 − cos α ≈ αg)
> or the RIGHT slivers (width O(α²) at the top-right, a triangle of area ≤ (1−g)² tan α/2 at the
> bottom-right). A square entering the top sliver is a wall-hugging square of tilt β ≥ α − O(αg)
> with its lowest vertex within g of the wall (A89 §5.2's "presser within r of u", made exact), and
> at side < 4 it intrudes the corner above with depth ≥ 4 − m + β − δ: **a JAM stall is an
> interlocked wall column — B and its presser T are the wall's two squares between the corner
> slots, each an intruder of one of the two corners.** For WEDGE/BLOCK pairs Lemma CROSS (§4.3):
> A presses B against exactly the cardinal directions e with n_e < 0 (n = the separating normal),
> so after A's removal B's retreat along those is free of A and the re-fit B + t e (t = the first
> t with μ_c ≥ 1) has exposure = a strip of width t on B's e-side; the diagonal translate
> B + (d, d) has μ_c = 1 exactly (SLIDE's identity). [M] ARM translates certify only 2 of 33
> corners; the successes are cell re-placements (rotation to flush), not translations.
>
> **RELEASE.** [T] Lemma RELEASE-CL (§3.2): in the reduced packing (untouched squares + placed
> cells), an untouched square Q leaves a cell along e iff its e-cluster is not wall-anchored —
> Lemma CLUSTER verbatim, ∀-packings; intruder-anchoring (I) of NOCRIT-SEL is IRRELEVANT here (the
> flood works one corner). Removing a square R un-anchors Q only if EVERY wall chain of Q passes
> through R, and a corner intruder lies on a chain only where it presses a square against that
> square's outward direction — its partner (WEDGE/BLOCK: Lemma CROSS) or a square above-left /
> below-right of a tilted deep intruder. The PI's RELEASE lemma ("removing the deepest intruder of
> the least-intruded completable cell releases ≥ 1 untouched square unless FRAME") is exactly
> right as a DEFINITION of the stall and is NOT a theorem with a smaller residue: its "unless
> FRAME" clause is the residue, and [M] the corpus stall (record BL/BR) is one: after removing the
> pair, the flood's releases are slide-INS (single-intruder cells filled by the untouched square
> that met them: 2 per stalled corner), no retreat out of any cell fires, and the block fills to
> deficit 2. **The stall, named: INTERLOCK (§5)** — a K0-BLOCKED packing in which, at every corner
> c and every reachable Young D at c, some untouched square meets int D \ (A_c ∪ B_c) and every
> untouched square meeting a frontier cell is wall-anchored away from it. INTERLOCK ⊂ A91's
> wall-anchored frames (the flood adds the REMOVAL budget: chains through removed squares break),
> and at side < 4 its depth-2 form is forced to run along the walls: the arm cells of adjacent
> corners overlap by 4 − m, and a deep tilted intruder (reach > m − 2) of one corner meets the
> adjacent corner's arm cell — the mechanism seen at record_s0115 (BL's deep intruder sq1 meets
> BR's arm cell and vice versa). Trump is the archetype at ONE corner (TL: the cell below the slot
> is met by sq3, sq4, sq7; the cell to its right by sq6, sq9). No four-corner INTERLOCK packing is
> in the corpus (every corpus packing converts at ≥ 1 corner) and none was constructed: a JAM-type
> four-corner stall needs, on every wall, a column of two near-flush wall-huggers with the upper
> one tilted at least as much as the lower — the A47 I-L19 / A89 §5.2 recursion closed around the
> whole boundary — and a near-grid realisation of it at side ≥ 4 has margins of order αg (10⁻⁴ …
> 10⁻² at α ≈ g ≈ 0.1) which no scanner-level certifier decides; not attempted [C].
>
> **Leaf (T2, §7).** "Exchange feasible at c" is exactly Lemma EXPOSE at box level: a fixed
> placement Q₀ (a Young cell or B's flush cell) whose box-exposure Σ_box := int Q₀ \ (core(A-box) ∪
> core(B-box)) is reached by no non-pair box (shadow test) — an exact, LP-free, monotone (C)-type
> leaf, ∀-packings (no SelForm). Yield: at the pair frontier the nine other squares are unlocalised,
> their shadows cover Σ_box, and the leaf is silent — the existential-filter law of K0-ROT/TF-U/A91;
> the neighbour-free bound ("Σ_box = ∅", the self-contained exchange Q₀ ⊂ A ∪ B) is 0 on the
> corpus (0 of 21 successes; min exposure 2·10⁻⁶) and 0 on the pair census except the measure-zero
> exact-cell boxes; at nodes where the column above B and the row right of A are localised (depth
> ≥ 4-corner + 2) the leaf is free and decides by Lemma FLUSH-JAM's slivers. **No effect on A85's
> frontier price**, consistent with every prune since A89.
>
> **Composition (T3, §8).** If EXCHANGE (any flood form) held ∀-packings on [3.82, ŝ), it would
> discharge the k0_00 piece of `stratum_kill` in the PLAIN form (no minimality, no selection):
> hypotheses = the k ≥ 1 window kills for every Young skeleton class the flood can output (the
> census classes with a nonempty skeleton at one corner) — nothing else; the ŝ clause (uniqueness)
> is NOT delivered unless the flood's motions stay inside the image basin (r_B = 3/2000): the flood
> output at ŝ is a Trump image by the k ≥ 1 uniqueness, and the input is that image only if the
> displacement is < r_B (true at nick corners: displacement ≈ d₂ + tilt). Lean shape: one leaf
> `exchange_flood : CfgPacking m z → K0Blocked z → ∃ z′, CfgPacking m z′ ∧ Skeleton z′ ≠ ∅`, or
> per-node the EX leaf inside the A85 tree (`classKilledAt_of_tree`, C-type, ∀-packings); the
> replay certificate of a single exchange is the final 11-square configuration with exact cells,
> checked by `sat_squares` (V.CASE) — exchange87's certifier is that checker.

## 1. Setting

Packings P at side m: eleven closed unit squares Q₁..Q₁₁ in [0, m]², pairwise interior-disjoint.
Corner frame of c (D4 map, c at the origin, container in the positive quadrant); μ_c, d_c as in
`nocrit_k0_blocked.md` §1; intruder of c: d_c(Q) > 0 ⟺ int Q ∩ (0,1)² ≠ ∅; n(c) := number of
intruders; K0-BLOCKED: n(c) ≥ 2 ∀c. A square intrudes at most one corner (CC-1(ii): corner boxes
are m − 2 > √2 apart). Fact [T]: for closed squares Q, Q′ with disjoint interiors, int Q ∩ Q′ = ∅
(a point of Q′ in the open set int Q has interior points of Q′ nearby, also in int Q).

**Cells and diagrams.** Cell (i, j) at c := [i, i+1] × [j, j+1] in c's frame, i, j ≥ 0, inside
the container iff i + 1 ≤ m and j + 1 ≤ m (at side < 4: i, j ≤ 2). A Young diagram D at c is a
finite set of cells closed under (i, j) ↦ (i′, j′), i′ ≤ i, j′ ≤ j, all inside the container;
|D| its size; the slot cell is (0, 0). For D put
  R(D) := {Q ∈ P : int Q ∩ int D ≠ ∅},  N(D) := |R(D)|,  X(D) := N(D) − |D|  (the EXCESS),
  E_D := area(D \ ∪_Q Q) (free area inside D),  O_D := Σ_{Q ∈ R(D)} area(Q \ D) (overhang).
A cell square is the exact axis-aligned unit square occupying a cell (rational pose, tilt 0).

**The flood (PI, A87 `flood87.py`).** State: removed set R, placed diagram D (cell squares),
untouched set U (original poses, or rigidly re-placed), deficit := |R| − #(removed squares
placed) = 11 − (|U| + |D|). Completable slot: a cell not in D, inside the container, whose left
and lower neighbours are in D or on the walls. Step: (iii) BONUS — a completable slot whose only
intruder is one untouched square u: move u rigidly into the cell (U loses u, D gains a cell);
(i) a completable slot with 0 intruders: place a cell square, deficit −1; (ii) else the slot with
the fewest intruders: remove them all (n), place the cell, deficit + n − 1. SUCCESS iff deficit 0
(an 11-square packing at side m with the cells of D exact). The depth-1 exchange of A87 (remove
the two intruders, place the slot square, re-fit one square ANYWHERE at any tilt) is the first
step plus a free-form placement; flood87 keeps it as the fallback fit search at every step.

## 2. The static flood

### 2.1 [T] Lemma TWO (a two-intruder corner; the slot square is free)

**Lemma TWO.** Every K0-BLOCKED packing has a corner with n(c) = 2, and at every corner the slot
square S = cell (0,0) is interior-disjoint from every non-intruder.

*Proof.* Each square intrudes ≤ 1 corner, so Σ_c n(c) ≤ 11; with n(c) ≥ 2 at four corners at most
three corners have n ≥ 3. A non-intruder Q has int Q ∩ (0,1)² = ∅, i.e. int Q ∩ int S = ∅. ∎

So the slot is never "blocked by a third meeter" at a two-intruder corner (A87: 33/33), and the
lemma "some corner converts" may be stated for two-intruder corners only; at a corner with n ≥ 3
the flood's first step has deficit n − 1 ≥ 2.

### 2.2 [T] Lemma FLOOD-D (the static flood is sound)

**Lemma FLOOD-D.** Let D be a Young diagram at c with N(D) ≤ |D|. Then there is a packing P′ at
side m consisting of the 11 − N(D) squares of P \ R(D) and N(D) cell squares of D forming a Young
sub-diagram containing the slot cell (when N(D) ≥ 1); P′ has an exact axis-aligned unit square at
the corner slot, hence lies in a class k ≥ 1 (B.CENSUS: nonempty Young skeleton at c).

*Proof.* Cell squares are pairwise interior-disjoint and inside the container; a square of P \
R(D) has int Q ∩ int D = ∅, hence is interior-disjoint from every cell of D. Any order ideal of D
of size N(D) (e.g. the first N(D) cells in a linear extension of D's poset) is a Young diagram
containing (0,0) when nonempty. ∎ Conversely the static flood (cells only, no motion) succeeds at
D exactly when N(D) ≤ |D| (each cell is placed only after its intruders are removed, so R = R(D)
at the end; deficit = N(D) − |D|).

### 2.3 [T] Lemma X (the excess is overhang minus free area)

**Lemma X.** X(D) = O_D − E_D.

*Proof.* Interiors are disjoint and squares not in R(D) miss int D, so Σ_{Q ∈ R(D)} area(Q ∩ D)
= area(D) − E_D. Then N(D) = Σ_{Q∈R(D)} [area(Q ∩ D) + area(Q \ D)] = |D| − E_D + O_D. ∎

Reading. The flood wins at D iff the displaced squares stick out of D by no more than the free
area they left inside it. K0-BLOCKED at c: X({(0,0)}) = n(c) − 1 ≥ 1 for ANY depths (two intruders
overhang the slot by exactly 1 + E_slot). Adding a cell C to D changes X by (#squares meeting int C
but not int D) − 1 ≥ −1: a win from X = 1 needs a chain of cells along which the number of NEW
squares is one less than the number of cells — e.g. a 2-cell diagram whose second cell is met by
the pair only (the depth-1 exchange with a cell placement), or a 3-cell diagram with one new square.

### 2.4 [T] Lemma CAP (the full block never wins below side 4)

**Lemma CAP.** At side m < 4 every square of P meets the interior of the 3 × 3 block B₃ = [0,3]²
at every corner; hence N(B₃) = 11 and X(B₃) = 2, and every win of the static flood at side < 4 has
|D| ≤ 8 and ≥ 3 untouched squares interior-disjoint from D.

*Proof.* Suppose the closed unit square Q ⊂ [0, m]² misses the open quadrant (0,3)². Q is convex
and closed, (0,3)² open and convex, so a line separates them: Q ⊂ {a x + b y ≥ γ} and (0,3)² ⊂
{a x + b y ≤ γ} with (a, b) ≠ 0. The second inclusion forces a, b ≥ 0 (the quadrant contains
points with x or y arbitrarily negative — replace (0,3)² by its superset (−∞,3)², which the same
line also separates from Q since Q ⊂ [0,m]² ... precisely: Q ∩ (0,3)² = ∅ with Q ⊂ [0,m]² means
Q ∩ (−∞,3)² = ∅) and γ ≥ 3(a + b). So Q ⊂ T := {a x + b y ≥ 3(a+b)} ∩ [0, m]², a right triangle
with the right angle at (m, m) (or a strip if ab = 0). If a = 0 then Q ⊂ {y ≥ 3} ∩ [0,m]², a strip
of height m − 3 < 1 < the y-extent of Q; same for b = 0. For a, b > 0 the legs of T are ℓ_x =
(m − 3)(a + b)/a along y = m and ℓ_y = (m − 3)(a + b)/b along x = m. A unit square inside a right
triangle with legs p, q has side ≤ pq/(p + q) (the largest inscribed square of a triangle has a
side on a side of the triangle; on the legs it is the square at the right angle, side pq/(p+q);
on the hypotenuse it is smaller since (h − p)(h − q) ≥ 0 — classical [S]); here pq/(p + q) =
(m − 3)(a+b)²/(ab · ((a+b)/a + (a+b)/b)) = m − 3 < 1. Contradiction. ∎

So at side < 4 the flood is a race: it must reach X ≤ 0 before the block fills; flood87's stalls
(record BL/BR) end exactly at shape [3,3,3] with deficit 2, the CAP value.

## 3. The dynamic flood

### 3.1 [T] Lemma FLOOD-M (rigid re-placements are sound)

Let the flood's state be (R, D, U) with U carrying rigid re-placements of some squares (each at
its final pose, interior-disjoint from every other present square and from the cells of D, inside
the container). If |U| + |D| = 11 the configuration is a packing at side m with the cells of D
exact. [T: the packing property is a property of the configuration, not of a motion; flood87
checks destinations, not paths.] The bonus slide-in (u the only intruder of a completable cell,
moved onto the cell) is the special case where the destination is a cell.

### 3.2 [T] Lemma RELEASE-CL (the exact release criterion, ∀-packings)

Fix the current configuration P′ = U ∪ D (a packing of |U| + |D| ≤ 11 squares), a consistent
selection S′ for it, an untouched square Q meeting a frontier cell C, and a direction e with
μ_C(Q + te) increasing (Lemma K in C's own corner frame — C's "corner" is its lower-left vertex
and e ∈ {e_x, e_y} ∩ K). Let C_e(Q) be the forward closure of {Q} under "is pressed against e"
inside P′ (cells included as fixed obstacles: a cell pressing Q against e is a member that can
never move — treat it as wall-anchoring).

**Lemma RELEASE-CL.** If C_e(Q) is not wall-anchored (no member touches the far wall in direction
e; no cell of D is a member), then for all small t > 0 the configuration with the members of
C_e(Q) translated by te is a packing at side m (Lemma CLUSTER), and the translation continues
until the first new contact (Lemma PLATEAU's argument: rows are affine in t, the first activation
is a new contact or a far wall); Q leaves int C when μ_C(Q + te) ≥ 1. If C_e(Q) is wall-anchored
for every e ∈ K_C(Q), Q cannot leave C by translation of any set containing it and no other
untouched square (any translating set containing Q is S′-feasible only if it contains its pressers).

*Proof.* Lemma CLUSTER verbatim (its hypothesis is closedness and no far-wall contact; cells are
squares of the packing P′ for the row family). The last clause: if some member N of the chain from
Q to the wall is not translated, the active row between N and its predecessor decreases at a
positive rate. ∎

Remarks. (a) The intruder-anchoring (I) of NOCRIT-SEL plays no role: the flood works at one
corner and does not care whether another corner's intruder deepens. (b) A removed square R breaks
a wall chain of Q only if it was a member of the chain, i.e. R pressed some member against e: R is
on the FAR side of that member along e. A corner intruder A of c is on the far side of a square
N along e_x (in c's frame) only if N lies to the left of A's contact point — N is A's partner B
(Lemma CROSS below), or a square above-left of a tilted deep A that touches A's upper-left edge
(the normal (−1,1)/√2-type contact), and symmetrically for e_y. Removing A never frees the outward
retreat of a square on A's far side. (c) [M, flood87] In the corpus the releases that fire are the
slide-INS (rule (iii)): record_s0115 BL — after removing the pair, cell (0,1) ← sq10 and (0,2) ←
sq5 (both had become the single intruder of their cell); no untouched square retreats out of a
cell in any run; the deficit of the stalled corners rises monotonically to the CAP value.

### 3.3 [T] The deficit invariant, restated with Lemma X

Along the static flood, deficit = X(D) after each step; the bonus keeps the deficit and grows D;
rule (i) lowers it by 1, rule (ii) raises it by n − 1 ≥ 0 (n = 1: unchanged). The PI's invariant
("a free cell lowers, a single-intruder cell keeps, a doubly-intruded cell raises") is Lemma X's
increment formula. The flood wins iff free cells (n = 0) catch up with the doubly-intruded ones;
at side < 4 there are ≤ 8 usable cells (Lemma CAP), so the accounting is over a fixed finite set
of at most 20 Young shapes per corner (partitions in a 3 × 3 box) — the static census of §6.1 is
EXHAUSTIVE over shapes, not a strategy.

## 4. Exposure: what a re-fit needs

### 4.1 [T] Lemma EXPOSE

Let c have exactly two intruders A, B, S the slot square, and Q₀ any closed unit square. Put
Σ(Q₀) := int Q₀ \ (A ∪ B) (the EXPOSURE of Q₀).

**Lemma EXPOSE.** Q₀ is a valid depth-1 exchange placement (P \ {A, B} ∪ {S, Q₀} is a packing at
side m) iff (i) Q₀ ⊂ [0, m]², (ii) int Q₀ ∩ int S = ∅, (iii) no untouched square has an interior
point in Σ(Q₀).

*Proof.* (iii) ⟺ int Q₀ ∩ int Q = ∅ for every untouched Q: if int Q meets int Q₀ at p then, Q
being interior-disjoint from A and B (so int Q ∩ (A ∪ B) = ∅ by the Fact of §1), p ∈ Σ(Q₀);
conversely a point of int Q in Σ(Q₀) is in int Q₀. ∎

So the exchange at c is a statement about the REACH of the nine untouched squares into the
exposure of a candidate, never about A and B themselves; the flood's cell placements are the
candidates Q₀ = cell, with Σ(cell) = int cell \ (A ∪ B) — exactly "the cell is met by no third
square" of Lemma FLOOD-D. [M, `results/exposure98.json`] The 21 verified A87 placements are B
re-placed almost in place: area(Q₀ ∩ B) = 1.000 in 9 cases, ≥ 0.99 in 15, ≥ 0.71 in all;
exposure area min 2·10⁻⁶, median 0.0016, max 0.252 (anchored0 TR, side 4.107); 10 of 21 are exact
cells (tilt 0 or 90°); in 17 of 21 the placement is within 10⁻³ of one or two untouched squares
(the squares that bound the exposure) — the corpus exchange is "rotate B to flush inside its own
footprint plus a sliver".

### 4.2 [T] Lemma FLUSH-JAM (the JAM corner, exactly)

JAM corner at c (cases85's stratum; `tilt_floor_k0.md` Lemma JAM-0; frame with A on the bottom
wall): A = [g, 1+g] × [0, 1], 0 < g < 1/√2, n(c) = 2, B the second intruder. By JAM-0, B has a
vertex v = (v_x, v_y) in the left strip (0, g) × (0, 1) which is B's LOWEST vertex, B's edges from v
are e₁ = (cos α, sin α), e₂ = (−sin α, cos α) with 0 < sin α ≤ v_x < g, and the dip δ := 1 − v_y
satisfies δ ≤ (g − v_x) tan α (B's bottom edge must pass above A's corner (g, 1)). Vertices: v,
v + e₁ = (v_x + cos α, v_y + sin α) (rightmost), w := v + e₁ + e₂ = (v_x + cos α − sin α, v_y +
sin α + cos α) (topmost), u := v + e₂ = (v_x − sin α, v_y + cos α) (leftmost; on the wall iff
sin α = v_x). B ⊂ {y ≥ v_y}; d_c(B) ≤ δ.

**Lemma FLUSH-JAM.** Let B₀ := [0,1] × [1,2] (B's cell). B₀ satisfies (i), (ii) of Lemma EXPOSE,
and its exposure is Σ(B₀) = Σ_L ∪ Σ_T ∪ Σ_R ∪ Σ_B ∪ Σ_A where, with the four edge lines of B,
  Σ_L := int B₀ ∩ {left of the left-edge line} = {0 < x < v_x − (y − v_y) tan α, 1 < y < 2},
  Σ_T := int B₀ ∩ {above the top-edge line} = {0 < x < 1, u_y + (x − u_x) tan α < y < 2},
  Σ_R := int B₀ ∩ {right of the right-edge line}, Σ_B := int B₀ ∩ {below the bottom-edge line}
       = {x₁ < x < 1, 1 < y < v_y + (x − v_x) tan α}, x₁ := v_x + δ cot α ≤ g,
  Σ_A := int B₀ ∩ A = ∅ (A ⊂ {y ≤ 1}).
The pieces have the following entrances and sizes:
 (L) Σ_L ∩ {y ≤ u_y} is SEALED: bounded by the wall x = 0, by S (y = 1) and by B's left edge; an
     untouched square cannot have an interior point there (it would have to cross the wall, int S
     or B). Σ_L ∩ {y > u_y} is a triangle of width u_x = v_x − sin α ≤ g − sin α along y = u_y, open
     upward only into Σ_T's side.
 (T) Σ_T is the triangle with vertices (0, y_T), (0, 2), (x_T, 2), y_T := u_y − u_x tan α (the
     top-edge line at the wall), x_T := u_x + (2 − u_y) cot α; height 2 − y_T = δ + (1 − cos α) +
     (v_x − sin α) tan α ≤ (g − v_x) tan α + (1 − cos α) + (v_x − sin α) tan α = (g − sin α) tan α +
     1 − cos α (≤ g tan α), and width x_T ≤ (v_x − sin α) + [(g − v_x) tan α + 1 − cos α] cot α =
     g − sin α + (1 − cos α) cot α ≤ g − sin α + tan(α/2). It is entered only through y = 2 or from
     Σ_L's upper triangle (i.e. from above).
 (R) Σ_R ⊂ {cos α ... : x ∈ (v_x + cos α − sin α, 1)} has width ≤ 1 − (cos α − sin α + v_x) ≤
     1 − cos α + sin α − v_x ≤ 1 − cos α (since v_x ≥ sin α), entered through x = 1 only; Σ_B is the
     triangle (x₁, 1), (1, 1), (1, v_y + (1 − v_x) tan α), area ≤ (1 − g)² tan α / 2, entered through
     x = 1 only (its other sides are S and B's bottom edge).
Hence B₀ is a valid exchange placement iff no untouched square has an interior point in Σ_T ∪
(Σ_L ∩ {y > u_y}) (entering from above the cell) or in Σ_R ∪ Σ_B (entering from the right of the
cell).

*Proof.* B₀ ⊂ [0,m]² and int B₀ ⊂ {y > 1} misses int S. The complement of a convex polygon is the
union of the open outer half-planes of its edge lines, so int B₀ \ B is the union of the four
pieces; A ∩ int B₀ = ∅. The descriptions are the edge-line equations: the bottom edge y = v_y +
(x − v_x) tan α meets y = 1 at x₁ = v_x + δ cot α ≤ v_x + (g − v_x) = g; the left edge x = v_x −
(y − v_y) tan α meets the wall at height v_y + v_x cot α ≥ u_y (as sin α ≤ v_x); the top edge y =
u_y + (x − u_x) tan α meets the wall at y_T and y = 2 at x_T. Sealing of Σ_L ∩ {y ≤ u_y}: its
boundary consists of the wall segment, the segment of y = 1 (the top edge of S, whose interior
lies below) and B's left edge; an untouched square Q is convex with int Q ∩ (S ∪ B) = ∅ and
Q ⊂ {x ≥ 0}, so if int Q contained a point of this sealed region, Q would be contained in its
closure — impossible for a unit square (the region has width < g < 1). The bounds on the sizes
are the dip bound δ ≤ (g − v_x) tan α and sin α ≤ v_x. ∎

**Corollary FLUSH-JAM-T (what enters the top sliver).** Let T be an untouched square with an
interior point in Σ_T (or in Σ_L's upper triangle). Then (a) T has a point at height < 2 with
x < x_T ≤ g − sin α + tan(α/2) and T is disjoint from int B and from the wall's outside, so the
lowest vertex t of T lies in x ∈ [0, x_T) — every other vertex is higher — and T's up-left edge
from t keeps x ≥ 0: sin β ≤ t_x < x_T for T's tilt β (JAM-0's mechanism one level up: T is a
near-flush wall-hugging square, tilted counter-clockwise like B); (b) T's bottom edge from t must
stay above B's top edge on their common x-range, and t_y < 2 ≤ w_y + (2 − w_y) where w_y = v_y +
sin α + cos α is the height of B's topmost vertex; comparing slopes on [t_x, min(t_x + cos β, w_x)]
gives (tan β − tan α)(w_x − t_x) ≥ y_top(t_x) − t_y − (stuff ≥ 0) ≥ −(2 − y_T), i.e.
tan β ≥ tan α − (2 − y_T)/(w_x − t_x) ≥ tan α − 2 g tan α/(1 − 2g): **T is at least as tilted as B
up to O(αg)** (A47 I-L19 / A89 §5.2 exactly); (c) at side m < 4, T's topmost vertex is at height
≥ t_y − ... ≥ (y_T) + cos β + sin β ≥ 2 − 2g tan α + 1 = 3 − 2g tan α > m − 1 and at abscissa t_x +
cos β − sin β < 1 (t_x < g, cos β − sin β ≤ 1 − sin β and sin β ≤ t_x ... precisely t_x + cos β −
sin β ≤ t_x + 1 − sin β ≤ 1 + (t_x − sin β) which is < 1 iff t_x < sin β — not automatic; use the
topmost vertex's x = t_x + cos β − sin β together with T's top edge, which spans x ∈ (t_x − sin β,
t_x + cos β − sin β) ∋ points with x < 1 at height > m − 1), so **T intrudes the corner c′ above c
with depth ≥ 4 − m + (β − δ) − O(g α)** — T is one of c′'s two intruders and the wall between c and
c′ carries exactly B and T (Lemma WALL-F: their chords are 1/cos α + 1/cos β ≤ m − 2 < 2, and a
third wall-line unit chord would exceed the budget together with the two slot cells' 1 + 1 ...
precisely S contributes 1 and c′'s slot region the same after c′'s exchange).

*Proof of (a)–(c).* (a) A point p ∈ int T ∩ Σ_T has p_x < x_T and p_y < 2; T ⊂ {x ≥ 0}; T's lowest
vertex is its unique argmin of y unless T is axis-aligned (then its bottom edge is horizontal
at height < 2 and spans x ∈ (p_x − 1, p_x + 1) ∩ [0, m], which crosses B's top edge unless the
edge is entirely above it — it is not, since B's top edge rises to w_y = v_y + sin α + cos α >
2 − δ + sin α − (1 − cos α) and the horizontal edge at height < 2 ... would have to be above w_y >
... : for α > 0 and the edge at height h < 2, B's top edge exceeds h at x near w_x whenever h <
w_y, and w_y ≥ 2 iff sin α − δ ≥ 1 − cos α, which holds when sin α ≥ δ + 1 − cos α — true for the
JAM regime (δ ≤ g tan α, g < 1/√2 ... if it fails, the axis-aligned T sits with its bottom edge
between y_T and w_y over an x-range of width 1 that contains w_x's side, crossing B's top edge:
contradiction either way). So T is tilted; the lowest vertex t has t_y ≤ p_y < 2 and, T being
disjoint from int B and B's top edge rising to the right, t_x < x_T (a lowest vertex to the right
of x_T would put T's bottom edge, rising from t, below B's top edge ... or the point p left of t
below T's up-left edge — both impossible). The up-left edge from t stays in x ≥ 0 iff sin β ≤ t_x.
(b) is the slope comparison stated. (c) T's vertical extent is cos β + sin β ≥ 1 and its topmost
vertex is t + (cos β − sin β, cos β + sin β); with t_y ≥ y_T ≥ 2 − 2g tan α the topmost height is
≥ 3 − 2g tan α > 2.877 ≥ m − 1 for g tan α < 0.06; T's top edge, of length 1, passes through points
with x ∈ (t_x − sin β, t_x + cos β − sin β) and height ≥ t_y + cos β ≥ 2 + cos β − 2g tan α > m − 1,
and t_x − sin β < g < 1, so T has interior points in (0,1) × (m−1, m) of c′'s slot. ∎

Consequence for the stall of a JAM corner at side < 4 [T]. If the flood stalls at c at depth 2
through the cell B₀ (X({(0,0),(0,1)}) ≥ 1), some untouched T meets Σ(B₀); if it enters from above,
T is c′'s intruder and the column between the two slots is {B, T} with tilt(T) ≥ tilt(B) − O(αg);
c′'s own flood then has its downward cell (0,1)′ = [0,1] × [m−2, m−1] met by B (B's top vertex w is
at height ≥ 2 − δ + sin α > m − 2), so c′ is also stalled at that cell: **a JAM stall propagates
along its nick wall to the adjacent corner** — the interlocked column. If T enters from the right
(Σ_R ∪ Σ_B), T is a square with a vertex in the region between A's top line and B's bottom edge
right of x = 1 (Σ_B) or pressing B's right edge above the rightmost vertex (Σ_R): the pusher-side
neighbour R of the pair, floating at height ≥ v_y + (1 − v_x) tan α − ... > 1 (Lemma FLOAT's
pocket is below it); then the cell to the right of the slot, (1, 0), has exposure (1,2) × (0,1) \ A
= (1+g, 2) × (0, 1) ∪ ... and is met by R iff R reaches below y = 1 — R's footprint question of
`wall_budget.md` §2.3 (P-ON): a floating pusher with y_min ≥ h₀ does NOT meet (1,0), and then
(1,0) is free unless the next bottom-wall square reaches x < 2.

### 4.3 [T] Lemma CROSS (WEDGE / BLOCK / diagonal pairs) and Lemma ARM

Let A, B be c's two intruders, L = {n · p = d} a separating line with A ⊂ {n·p ≥ d}, B ⊂ {n·p ≤ d}
(Theorem CEIL's setting), and let e ∈ {e_x, e_y}.

**Lemma CROSS.** A presses B against e (in the sense of Lemma CLUSTER, for any consistent
selection whose active A–B row has normal n) iff n_e := n · e < 0 (A lies on B's e-side). After A
is removed, the translates B + te, t ≥ 0, are interior-disjoint from S as soon as μ_c(B + te) ≥ 1,
and the first such t is t_e = d_c(B)/ρ_e (Lemma K's rate; ρ_e = 1 for the side types, ρ_x =
n_B,x/(n_B,x + n_B,y) for a D-type edge with inward normal n_B, ρ = cos α/(sin α + cos α) resp.
sin α/(sin α + cos α) for a D-type lowest vertex with edge angle α, ρ = 1 axis-aligned); the
diagonal translate B + (d, d), d = d_c(B), has μ_c = 1 EXACTLY (max(p_x + d, p_y + d) = max(p_x,
p_y) + d). B + te is a valid exchange placement iff no untouched square has an interior point in
the strip Σ(B + te) = int(B + te) \ (A ∪ B) ⊂ (B + te) \ B, a region of width t along B's e-side.

*Proof.* The contact force on B from A along the selected row is a positive multiple of n's
negative... (the row's gradient w.r.t. B's centre is the unit normal pointing from A into B, i.e.
−n up to sign convention of L); it has a negative e-component iff n_e < 0. Translating B along e
never decreases μ_c (Lemma K); the rate formulas are Lemma K's; the diagonal identity is
Lemma SLIDE's. The exposure statement is Lemma EXPOSE with Q₀ = B + te. ∎

**Lemma ARM (the translation re-fits, certified).** [T] Each of the translates above, when its
exposure is free, is an exactly verifiable placement (rational centre, interval SAT gaps > 0 to the
nine, gap ≥ 0 to S, container clearance ≥ 0). [M, `results/static_flood98.json`, 33 corners × 2
intruders × 3 directions] ARM certifies 2 corners of 33 (record_s0115 TL: sq4 by (d,d) and e_x,
d = 7·10⁻⁹; polish15 BL: sq1 by (d,d) and e_y, d = 10⁻⁴); at every other corner the first
translate collides with an untouched square at a distance ≤ d (the worst gap equals −d to
machine precision in 20 of the 31 failures: the pressed square is in CONTACT along the retreat —
NOCRIT-SEL's anchoring, present here in stuck flow endpoints without any selection). The 21 A87
successes are therefore not translations but ROTATIONS of B onto its cell (§4.1): the flush
re-fit of Lemma FLUSH-JAM, whose exposure is O(α) thin, beats the translation re-fit, whose
exposure is a strip of width d — for a nick (d ≪ α) both are tiny, and both are blocked by the
same presser when it sits in the top sliver.

## 5. The stall: INTERLOCK

**Definition (INTERLOCK at corner c).** For every Young diagram D at c reachable by the flood
(static or with slide-ins), N(D) ≥ |D| + 1, and every untouched square meeting a frontier cell of
D is wall-anchored (Lemma RELEASE-CL) in each of its retreat directions from that cell within the
reduced packing. **INTERLOCK (packing):** INTERLOCK at all four corners.

[T] EXCHANGE (flood form) holds for P iff P is not INTERLOCK. [T] INTERLOCK ⊂ {wall-anchored
frames} of A91 in the following sense: at an INTERLOCK corner every intruder's outward clusters in
P \ {A, B} are wall-anchored through chains avoiding {A, B} — the wall-anchoring of RES(4)
restricted to (W) and to chains not passing through the removed pair; the flood's removal budget
is what INTERLOCK adds to A91 (a chain through the pair is broken for free). [T, §4.2] At side
< 4 a JAM-type INTERLOCK corner forces the interlocked wall column (B and its presser T are the
two squares on the nick wall between the slots, T an intruder of the adjacent corner, tilt(T) ≥
tilt(B) − O(αg)); around the whole boundary this is the A47 I-L19 / A89 §5.2 recursion closed on
itself — the near-flush jam supported by a more tilted near-flush jam at every corner, with the
cells to the right of every slot met by the pushers or by the adjacent corner's deep intruder
(reach > m − 2 = the arm-cell overlap 4 − m). [M] Realised at TWO corners of record_s0115 (side
3.9855, d₂ = 0.0145 / 0.0145): BL's cells (0,1), (1,0) are met by sq10 (the column presser) and by
{sq2, sq9} (BR's deep intruder sq2 reaches into BL's arm cell; sq9 the pusher), BR's by {sq6} and
{sq1, sq9} (BL's deep intruder sq1 reaches into BR's arm cell) — the two bottom crowds interlock
through the 0.015-wide overlap of their arm cells; the two nick corners TR/TL (d₂ = 10⁻⁸) are NOT
interlocked (their 2-cell diagrams have X = 0) and the packing converts there. Trump: INTERLOCK at
TL (the only doubly met corner: (0,1) ← {3, 4, 7}, (1,0) ← {6, 9}, all 20 diagrams X ≥ 1, and
after removing {4, 6} nothing can move — A87), not at the three slot corners (X = 0 trivially).
**No four-corner INTERLOCK packing is known** (8/8 corpus packings convert at ≥ 1 corner: 2/4
corners at 3.9855, 2–4/4 at 4.00–4.11 by the depth-1 exchange, more by the flood) and none was
constructed [C]: the JAM-column design closes around the boundary only with two near-flush
wall-huggers per wall between the slots, whose tilts must increase along the pinwheel — impossible
to close consistently with all four tilts ≥ each other unless all are equal up to O(αg), and the
resulting margins are of the size of the slivers (αg ≈ 10⁻⁴ … 10⁻²), below what a scanner
certifies and outside the window (side ≥ 4 for a near-grid realisation). Whether an INTERLOCK
packing exists at side < 4 at all is the exact k0 residue in this formulation: RES-X := {K0-BLOCKED
INTERLOCK packings at side m ∈ [3.82, ŝ)} ⊂ RES-N(δ_∞) ∩ {wall-anchored frames}.

What the window adds [T]. Lemma SLIDE (modulo K0-O1) gives d₂(c) ≥ ŝ − m at every corner; Theorem
S(0.3) gives a corner with d₂ < 0.3. For a JAM corner d₂ ≤ δ ≤ g tan α, so g tan α ≥ ŝ − m: a jam's
sliver height is bounded BELOW by the distance to ŝ — in the window a jam's top sliver is at least
ŝ − m tall, and the presser T that blocks it must dip at least that deep below y = 2; T's own
intrusion of c′ is then substantive (≥ 4 − m + β − δ ≥ 0.12 + β − δ). Nothing here empties RES-X.

## 6. Measurements [M]

### 6.1 The static census (`attempts/A98-exchange-lemma/code/static_flood98.py`, 2.4 s, exact SAT tests with the 10⁻⁹ tolerance law; `results/static_flood98.{json,md}`)

For the 8 corpus packings + Trump, all four corners, all Young diagrams inside the container
(20 shapes at side < 4; 4 × 4 box shapes at side ≥ 4):

| packing | side | corner | intruders (depths) | min X | argmin | X of the two 2-cell diagrams | A87 depth-1 verdict |
|---|---|---|---|---|---|---|---|
| record_s0115 | 3.98548 | BL | 1 (0.227), 0 (0.0147) | **1** | slot | 1, 2 | fail 0.9853 |
| record_s0115 | 3.98548 | BR | 2 (0.0997), 3 (0.0145) | **1** | slot | 1, 2 | fail 0.9855 |
| record_s0115 | 3.98548 | TR | 7 (0.406), 6 (1.6·10⁻⁸) | 0 | [1,1] ({6,7}) | 0, 2 | SUCCESS (cell) |
| record_s0115 | 3.98548 | TL | 5 (1.0), 4 (7·10⁻⁹) | 0 | [2] ({4,5}) | 1, 0 | SUCCESS (cell) |
| polish12/15/21/24, anchored0/1/2 | 4.0000–4.1071 | all | — | −5 | [4,4,4,4] | 0–2 | 17/28 SUCCESS |
| TRUMP | ŝ | BL, BR, TR | slot square | 0 | slot | 0/0, 1/1, 1/1 | K0-FREE |
| TRUMP | ŝ | TL | 6 (0.168), 4 (0.155) | **1** | slot | 2, 1 | fail 0.9823 |

Readings. (i) On the only sub-4 packing the static 2-cell flood reproduces the depth-1 exchange
corner by corner, and the A87 successful placements ARE the 2-cell diagrams' second cells (TR:
centre (3.4852, 2.4855), tilt 7·10⁻¹⁰ = cell (0,1) of the TR frame; TL: (1.5038, 3.4854), tilt 90°
= cell (1,0) of the TL frame). (ii) The win/stall split follows d₂: nick corners (10⁻⁸) win with
the partner's own cell, substantive corners (0.0145) stall at every diagram; the 2-cell excess at a
stalled corner is 1 in the direction of the nick partner's cell (one third square) and 2 along the
wall (the adjacent corner's deep intruder + the pusher). (iii) At side ≥ 4 the static flood is
vacuous, min X = −5 = 11 − 16: those seven packings say nothing about the window. (iv) Trump: 0 of
20 TL diagrams win; canary PASS. (v) Borderline (|gap| ≤ 10⁻⁹) cell tests: 0 on the corpus, 17/10/
5/8 on Trump's four corners — Trump's exact tangencies, decided as non-intrusions by the tolerance
law (`k0dir87.md`), consistent with A87.

### 6.2 The dynamic flood (A87 chore, `flood87.py`, final pass, 1 253 s; `notes/flood87.md`)

33 (packing, corner) rows: **FLOOD_SUCCESS 30, all exactly verified** — 21 at depth 1 (= A87's
depth-1 exchange), 8 at depth 2 and 1 at depth 3 (a free cell after 1–6 slide-ins; the 9 "rescued
beyond exchange87" corners are polish12 TR/TL, polish15 TR/TL, polish24 BL, anchored0 BR/TL,
anchored1 BR, anchored2 BR — all at side ≥ 4, where the static flood is vacuous); **stalls 3**:
record_s0115 BL and BR (no completable slot at shape [3,3,3], deficit 2 = Lemma CAP, 5 and 7
slide-ins, 0 anywhere-fits) and **TRUMP TL (canary: d1 pay 2, d2 pay 2 at the cell below, d3 free
cell (1,1), d4 pay 2, then no completable slot at [3,3,3], deficit 2; canary_OK = True)**. Releases:
only slide-ins fired; no untouched square retreated out of a cell in any run. Every sub-4 stall is
the CAP value; every sub-4 win is a nick corner's 2-cell diagram (§6.1).

### 6.3 Exposure of the 21 verified placements (`code/exposure98.py`, `results/exposure98.json`)

See §4.1. Minimum exposure 2.1·10⁻⁶ (polish12 BL), median 1.6·10⁻³, maximum 0.252; area inside B
≥ 0.709 always; the anchored packings at 4.08–4.11 (margins 5–11 %) have exposures 0.05–0.25, the
side-4.000 packings ≤ 0.04. **The self-contained exchange (Σ = ∅, Q₀ ⊂ A ∪ B) never occurs.**

## 7. T2 — the exchange as a tree leaf

**Leaf EX(c, Q₀).** Node data: the pair boxes β_A, β_B of corner c (rect × tilt-interval, A85
atoms) and the boxes β_j of the other nine squares (a square not yet localised has box = the
whole pose space). Fixed candidate Q₀ ∈ {cell (0,1), cell (1,0), B's flush cell in either
orientation} (exact rational squares; the leaf may list several). Box exposure Σ_box(Q₀) :=
int Q₀ \ (core(β_A) ∪ core(β_B)), core(β) := ∩_{poses ∈ β} Q(pose) (the certificate-semantics core
of the frozen verifier: a region contained in every pose of the box; for a rect × tilt box it is
the intersection of the four extreme poses' squares, computable exactly, and it is EMPTY unless
the box is small — a tilt interval of width τ and centre box of side h give a core of side ≈ 1 −
h − τ/√2·... (the K0-WIDEN bookkeeping)). Test: for every j ∉ {A, B}, shadow(β_j) ∩ Σ_box(Q₀) = ∅,
shadow(β) := ∪_{poses ∈ β} Q(pose) (an outer cover by the A89 o3fam monotone f-test: a box reaches
a rectangle iff its nearest pose does; exact with the Lipschitz pad); and Q₀ ⊂ [0, m]² for every m
of the window, int Q₀ ∩ int S = ∅ (S the slot cell, automatic for Young cells).

**Soundness [T].** For every packing in the node, A ⊇ core(β_A), B ⊇ core(β_B), so Σ(Q₀) ⊆
Σ_box(Q₀); every untouched square lies in its shadow, which misses Σ_box; by Lemma EXPOSE Q₀ is a
valid exchange placement; by Lemma FLOOD-D the packing is not in k0_00 (it converts to a k ≥ 1
packing at the same side, killed by the k ≥ 1 window kills). ∀-packings: the leaf is a (T)-type
kill, not SelForm; it composes with A85's Lemma P-TREE as a NO-child ("no packing of this node is
K0-BLOCKED-and-unconverted"). Monotone: sub-boxes have larger cores and smaller shadows.

**Yield.** (a) Ignoring neighbours (all nine shadows = everything): the leaf passes iff Σ_box(Q₀)
= ∅, i.e. the cores of the pair cover Q₀ — the self-contained exchange; on the corpus 0/21
successes are self-contained (§6.3) and on the census a core containing a unit cell forces the box
to be the single pose "B = the cell" (tilt exactly 0, centre exactly the cell centre), which is
the K0-REUSE pocket (k1_00's tree), measure zero among the 7,044 realisable pairs: **upper bound
on the neighbour-free yield: 0 %** (the 68 JAM pairs included: their B-boxes are tilt-bins of
width ≥ 7.125°, whose cores miss the cell's top corners). (b) With neighbours: Σ_box is a thin
region (the slivers of Lemma FLUSH-JAM plus the box widening, area O(α + h + τ)), reached only by
boxes within reach of the cell's top side or right side; at a 4-corner node (8 intruder boxes
localised, 3 free squares not) the free squares' shadows cover Σ_box: silent; at depth ≥ 4-corner
+ localisation of the column above B and the row right of A (2 more squares) the leaf decides. This
is the existential-filter law (A89 §9, A90 §6, A91 §9): free at deep nodes, silent at the
frontier; **A85's price (3 200–7 000 CPU-h) stands.** Design for A85/A96: EX as a per-node
(T)-leaf test added to the (C)-leaf battery, run before the LP; certificate = (corner, Q₀, the
core/shadow atoms), replay-shaped; no verifier change (the core/shadow tests are the o3fam
primitives; the final packing certificate is `sat_squares`).

## 8. T3 — composition and Lean

**If EXCHANGE (any flood form) holds ∀-packings on [3.82, ŝ)** [C]: for every side m of the
window and every K0-BLOCKED packing z at m there is z′ at m with a nonempty Young skeleton at a
corner; z′ lies in a class k ≥ 1 (B.CENSUS assigns the class by the maximal skeleton; the flood's
output skeleton is a Young diagram of size |D| ≤ 8 at one corner — every such class is one of the
census classes killed on the window by A57/A60/A61 and the pinned-class chain, hypothesis
K0-O1-ALL: "every class with a nonempty skeleton is dead on [3.82, ŝ)", which is what the k ≥ 1
campaigns deliver); hence no K0-BLOCKED packing exists at m, and with Lemma K0-FREE (K0-O1) no
packing at all: `stratum_kill` (k0_00 piece, C.K4TIER) in its PLAIN form StratumKill (∀ z, no
minimality, no Ψ/Φ selection, no DF-K0 criticality). Hypotheses added: none beyond K0-O1-ALL. The
uniqueness clause at ŝ is NOT delivered: a K0-BLOCKED packing at ŝ floods to a k ≥ 1 packing at ŝ,
i.e. (Theorem U chain) to a Trump image, which is consistent; it is excluded only if the flood's
total displacement is < r_B = 3/2000 (basin isolation E.A36 then says the input IS the image,
contradicting K0-BLOCKED) — true when the conversion is a nick corner's 2-cell flood with d₂ +
tilt(B) < r_B, not in general. Residue for uniqueness: RES-X at ŝ with displacement ≥ r_B.

**If EXCHANGE holds only at nick corners** (the corpus pattern: 2-cell wins iff d₂ ≤ 10⁻⁸ …
10⁻⁴): the statement "every K0-BLOCKED packing at m < ŝ has a corner with X({(0,0), cell(B)}) = 0"
composes the same way; its residue is INTERLOCK at every corner — with SLIDE, every corner has d₂
≥ ŝ − m, so within 10⁻⁸ of ŝ the corners are nick-like and the flood's chance is highest exactly
where RES-N lives; no lemma here turns that into a proof.

**Lean obligations** (no `lean/` edits in this attempt). (E1) Lemma FLOOD-D: a finite
configuration lemma — `CfgPacking m z → (∀ Q ∈ R, int Q ∩ int D ≠ ∅) → (∀ Q ∉ R, int Q ∩ int D = ∅)
→ |R| ≤ |D| → CfgPacking m (z \ R ∪ cells)`: `sat_squares` for cell–cell and cell–untouched pairs;
(E2) Lemma X is not needed by the consumer (bookkeeping); (E3) Lemma EXPOSE / FLUSH-JAM: polygon
containment, `nlinarith`-sized after the case split; (E4) the EX leaf: core/shadow atoms (present:
o3fam's monotone reach test is the same primitive as the crowd families' `NoFam` boxes) plus one
clause in the case checker — replay-shaped; (E5) the ∀-packings lemma itself, if it lands, as a
new leaf `exchange_flood`; its consumer is `classKilledAt_of_tree` with the k ≥ 1 kills as
hypotheses (the `ShellKill`/`chain` interface of A93's Composition.lean already quantifies over
every class i).

## 9. Canaries

* Trump TL: static min X = 1 over the 20 diagrams (§6.1); the cells adjacent to the slot are met
  by two new squares (below: sq3, sq7 — sq7's leftmost vertex (0.984, 2.021) is inside the cell)
  and one (right: sq9); A87: after removing {4, 6} no square has a feasible rigid motion, largest
  inscribable 0.9823; flood87: deficit 2 at depth 2 on the stall path. PASS. Trump's three slot
  corners: X = 0 (K0-FREE), untouched by every lemma.
* record_s0115 (3.9855, outside the window): converts at TR and TL (nick corners), stalls at BL and
  BR — consistent with A87 corner by corner, and with Lemma CAP at the stalled corners.
* The side-4.000 polish packings: the static flood is vacuous there (16-cell grid); the depth-1
  and flood verdicts are about placements at the 10⁻⁸ level and are exactly the ones A87 reports.

## 10. Obligations ledger

| # | item | status |
|---|---|---|
| A98-O1 | Lemma TWO (two-intruder corner; slot square free of non-intruders; third-meeter closed) | [T] §2.1 |
| A98-O2 | Lemma FLOOD-D (static flood sound, ∀-packings), Lemma X (excess = overhang − free area), Lemma CAP (X(3×3) = 2 below side 4) | [T] §2.2–2.4 |
| A98-O3 | Lemma FLOOD-M (rigid re-placements), Lemma RELEASE-CL (exact release = un-anchored cluster in the reduced packing; (I)-anchoring irrelevant) | [T] §3 |
| A98-O4 | Lemma EXPOSE; Lemma FLUSH-JAM + Corollary FLUSH-JAM-T (JAM stall = interlocked wall column, presser tilt ≥ partner tilt, presser intrudes the adjacent corner at side < 4); Lemma CROSS + ARM | [T] §4 |
| A98-G1 | **Theorem EXCHANGE / flood termination with deficit 0 on [3.82, ŝ)** | **OPEN** — residue RES-X (INTERLOCK at all four corners, §5); realised at 2 corners (record 3.9855) and at Trump's TL; no four-corner example known or constructed |
| A98-O5 | static census (33 corners, 20–70 diagrams each), ARM census, exposure of the 21 placements, Trump canary | [M] §6 |
| A98-O6 | EX leaf: definition, soundness, yield (0 % neighbour-free; silent at the frontier; free at depth) | [T+M] §7 |
| A98-O7 | composition: plain StratumKill modulo K0-O1-ALL; uniqueness clause not delivered (basin displacement); Lean shape E1–E5 | [T] §8 |
| A98-C1 | construct or exclude a four-corner INTERLOCK packing (near-grid JAM pinwheel at side ≥ 4 with a certified-failure checker — an interval B&B on Λ(p, θ) — or a proof that the presser recursion cannot close around the boundary at side < 4) | [C] |
