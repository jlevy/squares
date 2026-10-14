# Lemma SWAP, the sweep and Lemma RAISE — exchanging a ring at the same side (A222, 2026-09-14)

The PI's proposals (A222 BRIEF 22:10, addenda 0/0b/0c 22:30–23:05): (1) a loaded ring of corner meeters can be
teleport-decomposed AT ONCE — pick up the eight meeters and put down settled corners plus band squares inside their union
and the free space (Lemma SWAP); (2) the proof route is an INDUCTIVE SWEEP around the perimeter: settle a corner, expose the
next cell, it must be met by a second square, pick it up, repeat; the perimeter holds 4⌊√n⌋ − 4 cells and the ring uncovers
that many, so the second meeters must come from the centre and no ring is self-supporting; (3) the target is Lemma RAISE: from
any teleport-stuck packing at side < ⌈√n⌉ at least two cells settle by exchange, so k0 raises to k2 and the compute-bound
k0 cascade is not needed for the VALUE, uniqueness reducing to the swap-rigidity of Trump.  This file makes each exact.
Tags: [T] proved, [M] measured, [F] false as stated, [C] obligation.  Code `attempts/A222-ring-swap/code/`, results
`results/raise222{,_kept}.md` (RAISE / Lemma CELLS on every A217 witness), `results/swap222.md` (the region-constrained
exchanges on the 193 four-crowds), `results/trump222.md` (swap-rigidity of Trump); pages
`docs/residue_map/campaigns/A222-ring-swap/`; Lean `Statements/Open/RingSwap.lean`.

## 0. Verdict

> **[T] Lemma SWAP** (any n, any side): replacing a set X of squares of a packing by |X| unit squares inside
> U(X) = (⋃X) ∪ Free, interior-disjoint from the rest, keeps the packing property at the same side.  Lean `swap_packing`, a
> theorem (28 lines); `teleport_packing` is the case |X| = 1 (`teleport_of_swap`).  **[T] Lemma STEP / Lemma CELLS**: the sweep
> step is valid iff the exposed cell is met by nothing but the squares in hand and the ones being picked up; statically, a packing
> exchanges into one containing a family Π of pairwise disjoint unit cells iff **|M(Π)| ≤ |Π|** (M(Π) = the squares whose
> interiors meet a cell of Π): Lean `cells_swap`.  K0-FREE is |Π| = 1, Theorem FC is Π = pins ∪ {p} in a complete packing.
> **[F] The count does not close.**  An exposed cell needs ONE remaining meeter, not two (one meeter = a teleport; FC's "two
> non-pin meeters" holds only in a COMPLETE packing, and the sweep holds squares in hand from step 1 on).  The sweep leaves nothing
> in hand iff some prefix Π_k has |M(Π_k)| ≤ k; over the whole window perimeter (8 cells at n = 11, S < 4) it needs
> Σ|M_k| ≤ 8 while ≥ 9 squares meet the 8 cells whenever every corner is doubly met — and n = 11 ≥ 9 supplies them.  Counting
> closes only for n ≤ 4⌊√n⌋ − 4, i.e. n ≤ 4.  What the count DOES give: at least one centre square meets an exposed perimeter
> cell (the ring supplies 8 of the ≥ 9 consumptions) — the ring is not self-supporting, but it is supported by one intruder.
> **[T]/[C] Lemma RAISE(0 → k)** is exactly "some admissible family Π with a corner cell has |M(Π)| ≤ |Π| = k"; RAISE(0 → 1)
> with the k1-a kill empties k0_00 (Lean `no_packing_of_raise`); RAISE is NOT a counting consequence — it is the geometric
> obligation, stated as the axiom `raise_zero_one`.  **[M]** On every A217 witness at its own side (4,534 packings, 1,172 four-
> crowds, sides 3.89–5.28) RAISE holds — trivially at S ≥ 4 (12 perimeter cells > 11 squares); every witness below side 4 has a
> corner met by ≤ 1 square (K0-FREE); the window-shaped 8-cell family is over-met on 40 of 1,172 four-crowds (page
> `window8_fail_w047_crowd.svg`).  **[M] The ring swaps at once** at its own side 4.11: X = the eight meeters → four settled
> corners + four band squares (page `ring_swap_rand_0_0569_t20.svg`), although the local CORNER-SWAP at BL fails (rattler 0 in
> the pocket); across the four-crowds see `swap222.md`.  **Loads are never used**: SWAP, STEP, CELLS and RAISE cover rattler
> crowds exactly as loaded ones — the A218/A219 rattler gap is not a separate gap under this route.  **What remains [C]**: RAISE(0
> → 1) for every k0 packing at S ∈ [3.82, ŝ) (no such packing is known; the witnesses live at S ≥ 3.89 and all raise), and, for
> uniqueness, SWAP-RIGIDITY of Trump (§1.7).  k0_00's row is unchanged: the route is sound and load-free, its obligation is
> geometric, not closed by counting.

## 1. The sweep made exact (task 0)

**1.1 Setting.**  A packing P of n unit squares in [0, S]²; a CELL is a closed axis unit box in the container (the census
cells (c, i, j): offsets i, j from corner c); P MEETS a cell iff some square's interior meets the cell's open interior;
M(Π) := {Q ∈ P : Q meets some cell of Π}.  Free(P) := [0,S]² minus the interiors of P's squares (closed).  For X ⊆ P,
U(X) := (⋃X) ∪ Free(P) = the container minus the interiors of P \ X.  A closed unit square lies in U(X) iff it is interior-
disjoint from every square of P \ X (closed convex bodies: Q ∩ int R = ∅ ⟺ int Q ∩ int R = ∅).

**Lemma SWAP [T] (any n, any side).**  Let X ⊆ P and let X′ be |X| unit squares in [0, S]², pairwise interior-disjoint and
interior-disjoint from every square of P \ X.  Then (P \ X) ∪ X′ is a packing at side S.  *Proof.*  The three clauses of the
packing predicate (unit, contained, pairwise interior-disjoint) hold square by square.  ∎  Lean `swap_packing` (hypotheses
`hkeep`, `ht`, `hbox`, `hfree`); `teleport_packing` = X = {i}, X′ = {the slot square} (`teleport_of_swap`).

**1.2 Lemma STEP [T].**  State of the sweep after k steps: settled cells Σ_k (slot squares), untouched squares R_k ⊆ P, and
h_k squares IN HAND; Q_k := Σ_k ∪ R_k is a packing of n − h_k squares (Lemma SWAP, inductively).  Expose a cell p_{k+1}
interior-disjoint from Σ_k and let M_{k+1} := {Q ∈ R_k : Q meets p_{k+1}}.  Then Q_k \ M_{k+1} ∪ {S_{p_{k+1}}} is a packing
(the slot square is in the container and interior-disjoint from everything else — exactly `teleport_packing`'s `hfree`), and
  * |M_{k+1}| = 0: place a square from hand (h ↦ h − 1);   * |M_{k+1}| = 1: teleport it (h unchanged);
  * |M_{k+1}| ≥ 2: pick them all up, place one (h ↦ h + |M_{k+1}| − 1).
So h_k = Σ_{j ≤ k} |M_j| − k.  **The sweep ENDS (nothing in hand) at the first k with h_k = 0**, and then Q_k is a packing of n
squares at side S containing the k settled cells.  The precise hypothesis of a step is therefore only "p_{k+1} is met by no
square outside R_k", automatic since Σ_k's cells are interior-disjoint from p_{k+1}.  On the ring witness at its own side
(page `sweep_rand_0_0569_t20.svg`, window-shaped perimeter from BL counter-clockwise): BL {4,5} → h 1; BL(1,0): rattler 0
teleports; BR {6,7} → h 2; BR(0,1): 8 teleports; TR: 10 teleports; TR(1,0): holder 9 teleports; TL {2,3} → h 3; TL(0,1): free,
place → h 2.  Consumed 10 of 11 (only rattler 1 untouched), h_8 = 2: the sweep does not end.  Its 12-cell perimeter (S = 4.11
≥ 4) ends at step 2 from BR (BR(1,0) = [2.11, 3.11] × [0,1] is met by 6 and 7 only) — the count is trivial at S ≥ 4.

**1.3 Lemma CELLS [T] (the static form).**  Let Π be pairwise interior-disjoint unit cells in the container (any poses; for
the census they are axis slots) with |M(Π)| ≤ |Π|.  Then P exchanges, at the same side, into a packing containing every cell
of Π as a square: X := M(Π) ∪ (any |Π| − |M(Π)| further squares), X′ := Π.  *Proof.*  Lemma SWAP: every cell is interior-
disjoint from every square outside M(Π) by definition, and from the other cells by hypothesis.  ∎  Lean `cells_swap` (the
family `F`, the injection `ι`, `hmiss`).  The sweep is the special case Π = {p_1 … p_k} (a prefix), since a square meeting
several cells is consumed once: Σ_{j≤k}|M_j| = |M(Π_k)|.  K0-FREE (`k0_route.md` §3) is |Π| = 1; Theorem FC (`forced_corners.md`
§0, Step 1) is Π = (pins of S) ∪ {p} in a COMPLETE packing: the pins meet their own cells only, so |M(Π)| ≤ |Π| ⟺ p has ≤ 1
non-pin meeter, and the kill of S ∪ {p} then forbids it — "≥ 2 non-pin meeters".  **Mid-sweep FC does not apply**: the partial
packing Q_k is not a packing of n squares, no class is killed for it, and a cell with one remaining meeter is simply a teleport
(Lemma STEP); the PI's "each exposed cell needs a SECOND meeter" is FC's clause transported to where its hypothesis fails.

**1.4 The count [T]/[F].**  Perimeter cells at side S: per wall a corner, the cells [k, k+1] for k = 1 … ⌊S⌋ − 2 from that
corner, the next corner: 4⌊S⌋ − 4 pairwise disjoint cells ([⌊S⌋−2, ⌊S⌋−1] and [S−1, S] are disjoint since ⌊S⌋ − 1 ≤ S − 1).  At
n = 11 and S ∈ [3.82, 4): ⌊S⌋ = 3 = ⌊√11⌋, **8 cells** (the PI's 4⌊√n⌋ − 4, corners counted once) — with a CHOICE per wall,
[1, 2] from one corner or [S−2, S−1] from the other (they overlap at S < 4).  A full-perimeter sweep ends with nothing in hand iff
Σ_{k≤8}|M_k| ≤ 8.  With every corner doubly met (K0-FREE′: else K0-FREE already raises), |M_1| ≥ 2 and the seven later cells
need |M_k| ≥ 1 each for the sweep to CONTINUE past them with h ≥ 1 — but continuing is not the goal; ENDING is, and it ends at
the first k with Σ_{j≤k}|M_j| = k.  A packing SURVIVES the sweep (never ends) iff Σ_{j≤k}|M_j| ≥ k + 1 for all k ≤ 8, in
particular ≥ 9 squares meet the 8 cells.  The ring supplies at most 8 (each member is consumed once), so **at least one centre
square is consumed** — that is the whole content of the count: the ring is not self-supporting, ONE intruder suffices (the ring
witness: rattler 0 at BL(1,0) or holder 9 at TR(1,0), depending on the start).  It is not a contradiction: 9 ≤ n = 11.  Counting
closes only when the perimeter has ≥ n cells, 4⌊√n⌋ − 4 ≥ n ⟺ n ≤ 4.  Adding the centre cell (9 cells, every square of P meets
one of them since the uncovered strips have width S − 3 < 1) gives |M| = 11 > 9.  So **the PI's conclusion "k0 and k1 trivially
empty if the count holds" does not arise: the count does not hold**; the endgame after 8 settled cells is 3 squares in the cross
region [1,S−1]² ∪ arms, which do not fit at S < 4 (a packing with 8 slot squares would contain a corner pin, killed by k1-a;
directly: s(2) = 2 > S − 2 for the central box), so the only way the sweep ends is a PREFIX with |M(Π_k)| = k, i.e. an under-met
local family — Lemma CELLS with |Π| ≤ 7.

**1.5 Lemma RAISE — the exact statement.**  *RAISE(0 → k) for a packing P at side S*: there is a family Π of k pairwise
interior-disjoint unit cells in the container, one of them a corner slot, with |M(Π)| ≤ k.  [T] RAISE(0 → k) ⟹ P exchanges
at side S into a packing containing k slot squares including a corner (Lemma CELLS).  *Simultaneous vs sequential*: two cells c, p
each met by ≤ 1 square, by DISTINCT squares, are two independent teleports (they commute: neither slot square meets the other
cell); c met by {A} only and p met by {A, D} is sequential (teleport A to c, then p has one meeter D) — both are the single
condition |M({c, p})| ≤ 2; Lemma CELLS needs no order.  [T] RAISE(0 → 1) ⟺ some corner box is met by ≤ 1 square (K0-FREE) OR
a larger family with a corner is under-met.  **What the certified trees give.**  k1-a (the k1_00 tree, `k0_route.md` §3, a
DEPENDENCY priced at 200–300 CPU-h, not yet certified) kills every packing with a corner pin at m ∈ [3.82, ŝ): RAISE(0 → 1) then
empties k0_00 on the window (Lean `no_packing_of_raise`); RAISE(0 → 2) with the corner + adjacent cell lands in ContainsPins
{c, p} ⊆ the monotone k2 classes, whose kills the window trees deliver only where their scoreboard rows are full
(`forced_corners.md` §0: the k5/k6 rows; k2's own tree is not a lab object) — so **the consequence is: if RAISE(0 → 1) holds,
the k0 cascade is replaced by the k1_00 tree; if RAISE(0 → 2) with a Young pair, by the k2 classes' kills, which are not
cheaper today than k1_00's**.  [C] RAISE(0 → 1) for every k0 packing in the window is NOT proved; it is stated from k = 0 only
(above k = 0 the container minus the settled squares is not convex and the cell argument changes, PI 23:05).

**1.6 From a k1 start (0b-a).**  P containing a corner pin S_c (a COMPLETE packing): FC says the adjacent unclipped cell p has
≥ 2 non-pin meeters (else teleport one, or any non-pin square, onto p — a packing with pins {c, p}).  The sweep from there:
pick them up (h = |M(p)| − 1 ≥ 1), continue with Lemma STEP; the accounting is identical, Σ|M_j| ≥ k + 1 to survive.  The general
theorem the sweep gives, for any n and any S < ⌈√n⌉: **every packing exchanges at the same side into a packing containing the
largest family Π (a corner included, or the pins of the start) with |M(Π)| ≤ |Π|** — k* = max{|Π| : |M(Π)| ≤ |Π|}; the count
alone bounds nothing (k* ≥ 1 is RAISE(0 → 1)).  The literal hand placement "fails" exactly when every prefix is over-met; the
corrected bookkeeping is Lemma STEP's three cases, and a cell met only by the next ring member is a K0-FREE teleport on its own.

**1.7 VALUE vs UNIQUENESS (0b-b).**  Exchanges preserve the side.  VALUE: a k0 packing at m < ŝ raising to k ≥ 1 is killed by
k1-a, so s(11) ≥ ŝ needs RAISE(0 → 1) + k1-a, no k0 cascade.  UNIQUENESS: a k0 packing X at side ŝ raises to a packing at ŝ
with a corner pin, which (k1-b) is a Trump image T; X and T agree outside the exchanged set Y ⊆ T (|Y| = |X_swapped|), so X is
T with the squares Y re-packed inside (⋃Y) ∪ Free(T) and no corner settled.  **SWAP-RIGIDITY of Trump [C]**: no re-packing of a
subset Y of Trump's squares inside (⋃Y) ∪ Free(T) yields a packing other than a Trump image (Theorem U, `theorem_u.md`, is
|Y| = 1; the obligation is |Y| ≥ 2).  Test (`trump222.py`, `results/trump222.md`): every |Y| ≤ 3 subset containing a slot
square and every pair, region search for a different re-packing — Trump's free space at s0 is slivers of width ≤ 4·10⁻⁷.

**1.8 Rattler crowds.**  Nothing above mentions a load: SWAP, STEP, CELLS, RAISE are statements about which squares meet
which cells.  A rattler crowd (both meeters unloaded, 61 of 70 doubly-met corners at A217's genuine k0 FJ points) is treated
exactly like a loaded one — the A218/A219 gap ("RING excludes loaded four-crowds only") closes under this route, and the
obligation is the single geometric [C] of §1.5.  Whether RING-SWAP "needs loaded": **no**.

## 2. Lemma SWAP locally: CORNER-SWAP, the band lemma, the ring at once (tasks 2–3)

**2.1 CORNER-SWAP (2-for-2).**  Corner c met by exactly A, B.  [T] S_c ⊆ U({A, B}): int S_c is met by no other square.
[T] The second square needs the free space: a unit square Q′ ⊆ (A ∪ B) \ int S_c cannot lie in A or B alone (a unit square
inside a unit square is that square, and A, B meet int S_c), so it straddles their separating line; on the witnesses the found
squares always use Free (`swap222.jsonl`, the poses).  Criterion [T]: CORNER-SWAP at c ⟺ U({A,B}) \ int S_c contains a unit
square ⟺ the c-space (container shrunk by the tilt's half-width minus the Minkowski sums obstacle ⊕ square) is non-empty for some
tilt — decided exactly per tilt (`region222.cspace`, 1° grid).  [M] The ring: BR, TR, TL swap, BL does not (rattler 0 sits in the
pocket above the 4–6 contact and cuts the remainder); across the 193 four-crowds: `swap222.md`.
**2.2 Band lemma [T].**  Along a wall between two settled corners at side S ≥ 3, the flat square [1, 2] × [0, 1] (any [x, x+1] ×
[0,1], 1 ≤ x ≤ S − 2) lies in U(X) as soon as no square outside X meets the open band (1, S−1) × (0, 1) — trivially, since the
band is interior-disjoint from both corner squares; **its whole content is the hypothesis**, which the ring witness violates on
two walls (rattler 0 at BL(1,0), holder 9 at TR(1,0)).  The pocket UNDER a contact of two adjacent wall meeters (bounded by the
two squares and the wall) is guaranteed free; the pocket ABOVE it is where the intruder sits.
**2.3 The ring at once [M].**  X = the eight meeters, X′ = four settled corners + four squares: FOUND on the ring witness at its
own side (seeded polish, 0.15 s; page `ring_swap_rand_0_0569_t20.svg` (f)): two band squares on the left wall, two on the right,
none on the floor or ceiling bands — the PI's "the four remainders merge into bands" is realised on two walls; the local BL swap
fails and the ring swap succeeds because the 4–6 floor contact is released.  RING1 (one corner, seven re-packed) holds at every
corner of the ring, RING4X (intruders 0, 9 moved too) holds.  Witness counts: `results/swap222.md` (per-row commits, resumable:
`python attempts/A222-ring-swap/code/swap222.py --resume`).  Caveat: at S ≥ 4 there is room; at S < 4 no four-crowd exists among
A217's 4,534 local optima (the lowest is 4.0013), so the exchange tests are structural, not window evidence.

## 3. What is proved, what remains, whether loads are needed

[T] SWAP, STEP, CELLS (n-general; Lean theorems).  [T] the count is not a proof (n ≤ 4).  [T] RAISE ⟹ the k0 cascade is
replaced by the k1_00 tree (value) and by SWAP-RIGIDITY of Trump (uniqueness).  [C] RAISE(0 → 1) at every side of the window —
the geometric obligation, equivalent (given k1-a) to k0_00's emptiness; the witnesses cannot test it below side 3.89.  [C]
SWAP-RIGIDITY of Trump for |Y| ≥ 2.  Loads: not needed anywhere; rattler crowds are covered.  k0_00: unchanged.

## 4. Lean, files

`Statements/Open/RingSwap.lean`: `swap_packing`, `teleport_of_swap`, `cells_swap`, `no_packing_of_raise` (theorems, std axioms
only), `raise_zero_one` (axiom, its own only dependence); `lake build` + `lean/audit.py` exit 0, no sorry (`lean/AUDIT.md`).
Code: `cells222.py` (cells, meeting test, Lemma CELLS by size, the sweep), `raise222.py`, `region222.py` (c-space, greedy,
polish, exact check), `swap222.py`, `trump222.py`, `draw222.py` / `pages222.py`, `summarise222.py`.
