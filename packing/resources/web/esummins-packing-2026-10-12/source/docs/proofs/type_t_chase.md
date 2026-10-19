# The TYPE-T CHASE — T-CELLS, T-TIP, T-SLOTS, the failure of TWO-TILTED (the type-T ring exists on the window), its pocket, and the count under FAMILY-STUCK — A249, 2026-09-17

A248 closed the PI's corner chase for TYPE-F corners (a flat meeter and its poker) on the window: Lemma TWO-POKERS,
s* = 3.9342 > ŝ.  This note does the same work for the TYPE-T corner — both meeters tilted, 2 763 of the corpus's
3 056 corners and 45 of the 65 locked corners of the genuine FJ points — and says plainly what closes: the type-T
corner's cell structure and its tip supply are exact theorems (§1), but the analogue of TWO-POKERS is FALSE on the
window: two type-T corners share a wall's slots at every side of [3.82, ŝ], and the all-ADJ type-T RING (eight tilted
wall-touching meeters, every border cell doubly met by the eight alone) exists at ŝ with margin 0.037 — an exact
rational witness (§2).  What kills that ring is its POCKET (one square, 8 + 1 = 9 < 11, A237's PIERCE certificate),
i.e. the room statement, not a wall inequality.  The coordinator's FAMILY-STUCK (Lemma CELLS on every family of disjoint
cells) sharpens the demand per corner — every slot needs a non-own meeter and the two are distinct squares — but the
count still does not close (§3; A250 computes the exact minimum below 4, 9 ≤ 11).  Tags: [T] proved, [T-computed] certified /
exactly verified, [S] routine given cited items, [M] measured, [F] false as stated, [C] obligation.  Sources:
`corner_chase.md` (A248), `wedged_seal.md`, `sideband.md` (B0/B0′, A2), `k0_count.md` (PUSH), `construct_towards.md`
(NSS, TYPE-F-OWN), `perimeter_walk.md` (PROJECTION, TWO-FAR), `snap_down.md` (STACK), `ring_swap.md` (CELLS),
`pocket_waste.md` (PIERCE), `wall_torque.md` (TWO-CONTACT).  Code `attempts/A249-type-t-chase/code/` (`geom249`,
`chase249`, `twotilted249`, `pocket249`, `test249`, `summarise249`, `pages249`, `run249.sh`); results
`results/typet249.md` (+ `typet249_summary.json`, `chase249.jsonl`, `twotilted249_{wall,ring2,ring}.json`,
`pocket249.json`); pages `docs/residue_map/campaigns/A249-type-t-chase/{type_t_corner,type_t_ring,tightest_witness}.svg`;
Lean `Statements/Open/TypeTChase.lean`.

## 0. Verdict

> **[T] T-CELLS** (§1.1): in the corner frame a wall-touching tilted meeter B (wall vertex L = (0, δ_B + cos θ_B),
> lowest vertex V = (sin θ_B, δ_B)) meets c00 ⟺ δ_B < 1, meets the wall slot c01 ⟺ δ_B + w(θ_B) > 1 — ALWAYS in a
> doubly-met corner (δ_B > 0 by WEDGED-SEAL) — and meets the floor slot c10 ⟺ δ_B + (1 − sin θ_B) tan θ_B < 1; the
> floor meeter A (leftmost vertex W = (δ_A, cos θ_A)) is the mirror (θ ↦ 90° − θ): c00 ⟺ δ_A < 1, c10 always, c01 ⟺
> u_A(1) := δ_A + (1 − cos θ_A) cot θ_A < 1.  **[T] T-TIP** (§1.3): A's tip enters c01 only with its open chord at
> height 1, (u_A(1), u_A(1) + λ_A), λ_A = (w(θ_A) − 1)/(sin θ_A cos θ_A), disjoint from B's chord (b₁, u_B(1)),
> u_B(1) = sin θ_B + (1 − δ_B) cot θ_B: to the RIGHT of B's cap (then B misses c10 — NSS in closed form) or under B's
> bottom edge.  **[T] T-SLOTS** (§1.4): the second meeter of c01 is A's tip (T-TIP), the adjacent corner's WALL meeter
> B′ (STACK's mutual pair; never its ceiling meeter's tip: a ceiling toucher has no point below s − √2 > 2), or a free
> square — and of c10 the mirror.  [M] 0 violations on 5 526 corpus views and the 90 locked views.
>
> **[F] TWO-TILTED as a window bound** (§2).  The wall problem — B, A at c and B′, A′ at c′ on one wall, all tilted,
> both boxes met, the two wall slots served by the other corner — has sup SAT margin +0.078 at 3.82 and +0.074 at ŝ
> in the mutual sub-case BB′ (the tip sub-cases are dead by −(s − 2 − √2): T-SLOTS).  So **s_T* < 3.82**: no analogue
> of s*.  Stronger, **the all-ADJ type-T ring exists on the window** [T-computed]: eight wall-touching tilted meeters at
> ŝ, every one reaching the far slot of its wall, all twelve border cells doubly met by the eight, pairwise disjoint
> with margin 0.037 (C2-symmetric pinwheel at tilt 14.6°: `twotilted249_ring2.json`, exact rational check
> `test249.test_ring_exact`) — the type-F pattern that TWO-POKERS kills is alive in type T.  Its POCKET: waste 4.30 of
> 7.03, PIERCE(1) residual 0 at the centre ⟹ **capacity ≤ 1** [T-computed]; a direct search places one square (gap
> +0.209) and not two (−0.142): 8 + 1 = 9 < 11.  The FAMILY-STUCK poke (one free square meeting both slots of a wall
> between the mutual pair) fits (margin 0.0017) and is that one square.  On the window the type-T chase reaches NO wall
> inequality; what excludes the ring is the room for the three free squares.
>
> **[T] FAMILY-STUCK per corner and per wall** (§3): every slot has a meeter that is not a meeter of its corner (8
> outside incidences, against NSS's 4), the outside suppliers of a corner's two slots are DISTINCT squares, and a corner
> with no ADJ supply needs two distinct free squares; ADJ supply into a slot is at most ONE square (TWO-FAR), a wall
> meeter of the adjacent corner (T-SLOTS).  **[F] the count alone**: the all-ADJ ring meets every family condition with
> one poking free square ([T-computed] A250: the ILP minimum is 9 squares below 4, and it is this structure), and it exists (§2).  Mixed rings:
> a type-F corner's poker slot still needs a free square through its notch (A248), so ≥ 1 free square per type-F corner
> and, with the family condition, 2 if its floor slot is not ADJ-supplied; ≤ 3 free squares bound the mixed patterns to
> ≤ 3 type-F corners with free supply — no contradiction below ŝ by counting.
>
> **What closes: nothing new on k0_00.**  LOCKED-CROWD-FREE(11) is NOT given by the chase for type T: the honest residue
> is POCKET(11) for 12-stuck (family-stuck) rings with type-T corners — the type-T ring at ŝ is one explicit instance,
> killed by PIERCE(1).  Lean `TypeTChase.lean`: `t_cells`, `t_cells_floor`, `t_tip` [T-prose], `two_tilted_ring_exists`
> [T-computed], `no_two_tilted_bound` (theorem: the analogue of `two_pokers_window` is false), `type_t_chase_closes` [C].

## 1. The type-T corner (task 1)

**1.1 Setting and T-CELLS [T].**  Corner frame (u, v); cells c00 = (0,1)², c01 = (0,1)×(1,2), c10 = (1,2)×(0,1);
meeters A, B tilted, interior-disjoint, both meeting c00.  By Cor. B1 / WEDGED-SEAL neither touches both walls; by
Lemma A2 their centres are in distinct cells of the 2×2 grid.  Name B the one that touches the wall u = 0 or is nearer
it, A the one that touches the floor or is nearer it (`geom249.role_of_pair`).  Wall-touching B: wall vertex
L = (0, ℓ), tilt θ_B ∈ (0°, 90°) = the angle of the edge L→T from the horizontal, V = L + (sin θ_B, −cos θ_B) its
lowest vertex, δ_B := y_V = ℓ − cos θ_B ≥ 0, R = V + (cos θ_B, sin θ_B), T = (cos θ_B, ℓ + sin θ_B).  Floor-touching
A: lowest vertex V_A = (δ_A + sin θ_A, 0), θ_A the angle of V_A→R_A, leftmost vertex W_A = (δ_A, cos θ_A), top
T_A = (δ_A + cos θ_A, w(θ_A)).  The mirror u ↔ v is (θ_B, δ_B) ↔ (90° − θ_A, δ_A) (`test249.test_mirror`).
*Lemma T-CELLS.*  B meets c00 ⟺ δ_B < 1; B meets c01 ⟺ δ_B + w(θ_B) > 1; B meets c10 ⟺ δ_B + (1 − sin θ_B) tan θ_B
< 1.  *Proof.*  V has u = sin θ_B < 1, so V ∈ c00's closure with interior points of B beside it iff δ_B < 1; if
δ_B ≥ 1, B ⊆ {v ≥ 1}.  T has u = cos θ_B < 1 and height δ_B + w; the open diagonal (V, T) is interior to B and has
u < 1 throughout, so B meets c01 iff y_T > 1 (if y_T ≤ 1 then B ⊆ {v ≤ 1}).  B's lower boundary on u ∈ [sin θ_B, u_R]
is the edge V→R, height δ_B + (u − sin θ_B) tan θ_B, and u_R = w(θ_B) > 1; B has interior points with u > 1, v < 1 iff
this edge crosses u = 1 below height 1 (then points just right of the crossing and just above the edge are in c10; if
not, B ∩ {u ≥ 1} ⊆ {v ≥ 1}).  ∎  Mirror for A.  Since δ_B = 0 is the wedged square (alone, Cor. B1), in a doubly-met
corner δ_B > 0 and B meets c01 ALWAYS; likewise A meets c10 always: **SLOT-MET is automatic for touching type-T
meeters**, and the corner's own slot incidences are k_c = 2 + [B meets c10] + [A meets c01] ∈ {2, 3} (NSS forbids 4).
[M] 2 290 + 2 290 corpus predictions vs exact SAT depths, 0 disagreements; 85 + 84 of the locked views, the 3 others
touching-degenerate (a cell met at depth < 10⁻⁶).

**1.2 The reach.**  B occupies [δ_B, δ_B + w(θ_B)] along the wall, A occupies [δ_A, δ_A + w(θ_A)] along the floor; B
reaches the far slot c′01 = (0,1)×(s−2, s−1) iff δ_B + w(θ_B) > s − 2 (its top vertex has u < 1), i.e. iff B is
SHALLOW: d_B ≤ 1 − δ_B < 3 + √2 − s (0.54 at ŝ, 0.59 at 3.82; for a near-flush B, < 4 − s).  [M] corpus: B reaches
far in 1 524 of 5 526 views, A in 1 524, both in 102 (the corners whose two meeters both reach are the ring's).

**1.3 Lemma T-TIP [T].**  *B wall-touching with δ_B < 1, A floor-touching, interior-disjoint, A meeting c01.  Then
u_A(1) < 1 and the open chords of A and B at height 1 are disjoint: either u_A(1) ≥ u_B(1) (A's chord right of B's
cap; then B misses c10) or u_A(1) + λ_A ≤ b₁(B), where b₁ = (ℓ − 1) tan θ_B if ℓ ≥ 1, (1 − ℓ) cot θ_B otherwise (A's
chord under B's bottom edge L→V).*  *Proof.*  A meets c01 iff its left boundary crosses height 1 at u_A(1) < 1
(T-CELLS mirror); A's chord at height 1 is at distance w(θ_A) − 1 ≤ min(sin θ_A, cos θ_A) below its top vertex, so it
is the horizontal cut of the 90° corner at T_A: length (w − 1)(tan θ_A + cot θ_A) = λ_A, starting at u_A(1).  Both
squares have height 1 strictly inside their vertical ranges (A: (0, w(θ_A)); B: (δ_B, δ_B + w(θ_B)) since δ_B < 1 <
δ_B + w), so the open chords are interior to their squares and cannot overlap.  B's chord at height 1 runs from
b₁ (on L→V if ℓ ≥ 1, on L→T otherwise) to u_B(1) on V→R.  Two open intervals at the same height are disjoint iff one
is left of the other.  If A's chord is right of B's: u_A(1) ≥ u_B(1); with u_A(1) < 1 this gives u_B(1) < 1, i.e.
δ_B + (1 − sin θ_B) tan θ_B ≥ 1, B misses c10 (T-CELLS) — NSS's conclusion in closed form.  ∎  [M] 40 000 random
disjoint pairs, 0 violations; both cases occur.  The "under" case needs ℓ > 1 + λ_A cot θ_B — B's wall vertex high
above 1, A flat under it: it is the mirror of the type-F picture with B nearly flush.

**1.4 Lemma T-SLOTS [T] (the second meeter of c01 when B is a tilted wall toucher).**  c01 ∈ N_c ∩ N_c′ only
(PROJECTION), so its meeters are c's own, c′'s, or free.  (a) A: iff T-TIP's inequality holds (then k_c = 3, and B
misses c10).  (b) c′'s WALL meeter B′ (touching u = 0, parameters (θ′, δ′) in c′'s frame): meets c01 iff its lowest
point s − δ′ − w(θ′) < 2, i.e. δ′ + w(θ′) > s − 2 (B′ shallow), and B, B′ are STACK's ordered pair (contact table
`snap_down.md` §1.4; no contact forced, clearance < 4 − s).  (c) c′'s ceiling meeter A′: NEVER when A′ touches the
ceiling — every point of a unit square touching v = s has v ≥ s − √2 > 2 on s > 2 + √2 — and, touching nothing, only
with extent > s − 3 along the wall and a point with u < 1 below height 2 beside B′ (a far-slot reach; ≤ 1 of B′, A′ by
TWO-FAR).  (d) a free square, through B's notch (the wedge between the wall and B's edge L→V above height 1 when ℓ > 1, or the
wedge between the wall and L→T above T) or beside B's cap right of u_B(1) at heights in (1, 2).  Mirror for c10.  So for a corner whose two
meeters touch their walls, **ADJ supply of a slot comes only from the adjacent corner's meeter on the SHARED wall**.
[M] corpus c01 suppliers beyond B: own-A-tip 2 752, free 2 205, c′-meeter off the wall 801 (all at s ≥ 4, where the
ceiling toucher's bound s − √2 > 2.59 leaves only the untouching ones), c′'s wall meeter 687; locked views: A-tip 42,
free 63, B′ 6, off-wall c′-meeter 1.

## 2. TWO-TILTED (task 2): the analogue of TWO-POKERS is false on the window

**2.1 The wall problem [T-computed].**  Wall x = 0, corners c = BL and c′ = TL, both type T with both meeters
touching (B, A; B′, A′), 8 parameters (θ, δ each), side s; constraints: tilts in (0°, 90°), δ > 0, both boxes met,
pairwise interior-disjoint, in the container, c01 met by a square of c′ and c′01 by a square of c (four sub-cases).
Nelder–Mead over the least margin with structured restarts and an SLSQP slack polish (`twotilted249 --mode wall`):
sub-case BB′ (the mutual wall pair) **sup margin +0.0777 at 3.82, +0.0740 at ŝ**; sub-cases with a tip (BA′, AB′,
AA′) −0.4058 at 3.82 = −(s − 2 − √2): exactly T-SLOTS (c).  The mutual pair is A246's pattern (b) with the flats
tilted: B, B′ near-flush at δ ≈ 0.85, the partners steep (θ_A ≈ 60–67°) poking under them (page `type_t_corner.svg`
(c)).  So s_T* < 3.82 and the route "two type-T corners on one wall need s ≥ s_T* > ŝ" does not exist.

**2.2 What the lock adds.**  NO-ROTATE (A248 §2) needs the wall pair's depths to exceed 4 − s; the mutual type-T pair
is shallow by construction (§1.2: d_B < 3 + √2 − s, and for the near-flush witness d ≈ 0.15 each, sum 0.30 > 4 − ŝ =
0.12), so the flush-stack click is Ψ-lowering and NO-ROTATE demands a THIRD square in the window [0,1]×[1,3] minus the
pair — supplied externally by the next corner's meeters exactly as in A248 §2.2 (B′ itself dips below 2 < 3 at
u < 1, and A′, touching the ceiling, has points down to s − √2 ≈ 2.46 < 3 at u < 1 whenever it meets c′00: both block).  TWO-CONTACT (a loaded tilted wall square needs
two further loaded contacts) is met by the partner and the stacked neighbour.  [M] the 45 locked type-T corners: the
along / other holders of the locked meeters are FREE squares (non-meeters) in 96 + 20 + 14 + 2 holder lists, none in
36, meeters of another corner only in 12 — so at the genuine FJ points the pinning of a locked type-T meeter is by an
interior square in the large majority (holder classes in `typet249.md` §2) — [M] evidence for the PI's "pinned by an
internal square", not a theorem (the ring of §2.3 has no force analysis).

**2.3 The all-ADJ type-T ring [T-computed].**  Every corner type T with both meeters touching, every meeter reaching
the far slot of its wall (`twotilted249 --mode ring2`: 8 parameters under the half-turn C2, and `--mode ring`: 16).
At s = ŝ the C2 search finds sup margin **+0.0370**: BL's (θ_B, δ_B, θ_A, δ_A) = (14.56°, 0.891, 14.56°, 0.695),
BR's = (75.44°, 0.695, 75.44°, 0.891) — a pinwheel of eight squares at one tilt, each square's wall vertex the next
one's notch, B_BL from (0, 1.859) down to V = (0.251, 0.891) and up to T = (0.968, 2.110) > s − 2; every one of the
twelve cells is met by exactly two of the eight (table in `typet249.md` §3; the exact rational form with the tilt on
the unit circle verified in `test249.test_ring_exact`: containment, 28 pair gaps ≥ 0, 12 cells doubly met, all
Fractions).  The ladder over sides (results §3; detached at exit, resume block `attempts/A249-type-t-chase/notes/type_t_chase.md`)
finds the C2 ring absent at 3.60 / 3.70 / 3.82 (sup margins −0.047 / −0.033 / −0.009 with 30 restarts) and present at ŝ:
its least side lies in (3.82, ŝ] unless the 16-parameter search (pending) finds it lower; page `type_t_ring.svg` (a).  Compare A248: the type-F ring's pokers need s ≥ s* = 3.934;
tilting the flats by 15° buys the room — the notch under each B's lower-left edge holds the next A's tip.

**2.4 Its pocket [T-computed] (`pocket249`, A237's census).**  Pocket area 7.032, coverable ≤ 2.733 (waste 4.298),
PIERCE(1) at the centre: residual 0 over the 90 tilt bins ⟹ capacity ≤ 1 (Lean `capacity_le_of_pierce`); the direct
search fits one square (least gap +0.209, centre (1.94, 1.94) at 46°) and not two (−0.142) or three (−0.186).  So
8 + 1 = 9 < 11: **this ring is not the skeleton of an eleven-square packing** — by the room, as A237's window family.
FAMILY-STUCK's ring family (§3) asks for a free square meeting both slots of some wall: the search finds one (margin
+0.0017, poking between B_BL and B_TL at height ≈ 1.73), and it is the one square the pocket holds.

## 3. FAMILY-STUCK, the mixed rings and the count (task 3, and the coordinator's addendum)

**3.1 The hypothesis [T, Lemma CELLS].**  A family Π of pairwise disjoint border cells met by ≤ |Π| squares in total
exchanges into the |Π| slot squares (`cells_swap`), so a packing that cannot be raised this way has |M(Π)| ≥ |Π| + 1 for
every such Π.  Below 4 the two slots of one wall overlap ((1,2) ∩ (s−2, s−1) ≠ ∅), so a family holds ≤ 1 slot per wall:
per corner the dominoes {c00, c01}, {c00, c10} (≥ 3 squares) and the triple (≥ 4); along a wall {c00, c01, c′00}
(≥ 4), {c00, c01, c′00, c′10} (≥ 5); the ring family {4 boxes + one slot per wall} (≥ 9).
**3.2 Per corner [T].**  (i) each slot is met by a square that is NOT a meeter of its corner (the domino: M_c ∪ M(c01)
≥ 3 with |M_c| = 2) — 8 outside incidences on the ring, against NSS's ≥ 4; (ii) the triple: the outside suppliers of
c01 and of c10 include two DISTINCT squares; (iii) with |M_c| = 2, the ADJ supply of c01 is ≤ 1 square (TWO-FAR) and is
the adjacent corner's shared-wall meeter (T-SLOTS), so a corner with no ADJ supply needs TWO distinct free squares at
its slots, one with ADJ supply on one wall needs one.  [M] corpus (s ≥ 4): the domino {c00, c01} is met by exactly 2
in 1 926 + 470 of 5 526 views — the coordinator's teleportable dominoes (0 of 764 family-stuck), and the locked FJ
corners: 8 views with both dominoes at 2.  **3.3 Per wall [T].**  A wall's pair (the two meeters touching it) is mutual
iff both reach (§1.2: both shallow); then both slots are ADJ-supplied and no free square is needed there; otherwise each
unsupplied slot takes a free square poking beside the wall meeter.  The ring family forces, on SOME wall, both slots met
by free squares — one square suffices since the slots overlap (§2.4).  **3.4 The count [F as a closure].**  Demand 8
outside incidences with per-corner distinctness; supply: ADJ ≤ 8 (one per slot), free squares ≤ 4 incidences and ≤ 3
corners each.  The all-ADJ ring plus one poking free square satisfies every family; A250's ILP (PROJECTION, NSS,
TWO-FAR, all families) gives the minimum 9 squares below 4 (`count250.json`; 13 at s ≥ 4 where the twelve cells are disjoint), so **the count does not close at any side
below 4, nor on the window**; and the extreme structure it leaves — the all-ADJ type-T ring — exists (§2.3).  Mixed
rings: a type-F corner's poker slot needs a free square (A248, on the window), its flat's floor slot is ADJ-supplied
only by the next corner's flat with δ > s − 3 or a shallow tilted meeter; so f_F ≥ #type-F corners with the domino
condition adding a second distinct free square when the floor slot is not ADJ; with f ≤ 3 that bounds the mixed
patterns (≤ 3 type-F corners needing free supply) but kills none by counting.  The dependence on SEPARATE-NOTCHES
[M] of A248 stays where it was (four type-F corners).

## 4. Tests (task 4; `results/typet249.md`)

The 764 twelve-stuck packings (5 526 type-T views = 2 763 corners): touching classes (A floor, B wall) 1 726 views,
one toucher 1 128, none 2 672 (floating crowds above 4); T-CELLS 0 violations; own incidences k_c = 3 in 5 504 views,
2 in 22; mutual wall pairs 53 views; suppliers as in §1.4.  The genuine FJ points' 45 locked type-T corners (90 views,
sides 3.8948–4.358): (floor, wall) 82 views, one toucher 8; T-CELLS / T-TIP hold on every one; the tightest witness is
`cp85`-type point at **s = 3.894771** (BL/TL, θ_A = θ_B = 37.7°, δ_A = 0.492, δ_B = 0.883, depths 0.377 / 0.117, A's
tip meeting c01 right of B's cap, c10 free-supplied), page `tightest_witness.svg`; every inequality of §1 holds there
with the binding one T-TIP's u_A(1) ≥ u_B(1) (slack 0.03).  The ring witness (§2.3) is verified exactly.

## 5. What is proved, what remains, n-generality (task 5)

* **[T]** T-CELLS, T-TIP, T-SLOTS (for every n and side; the ceiling-toucher clause needs s > 2 + √2); the FAMILY-STUCK
  per-corner / per-wall consequences (any n, s < 4 for the overlapping slots).
* **[T-computed]** the mutual type-T wall pair and the all-ADJ type-T ring exist at ŝ (exact witness); the ring's
  pocket capacity ≤ 1 (PIERCE).  **[F]** TWO-TILTED as a bound above the window; the count as a closure.
* **Plainly:** TWO-TILTED + T-SLOTS + the count do NOT close the type-T and mixed cases below ŝ; LOCKED-CROWD-FREE(11)
  is not proved by the chase; k0_00 unchanged.  The exact remaining case: a 12-stuck (family-stuck) ring with type-T
  corners plus three free squares — drawn: the ring of §2.3 with its single pocket square (`type_t_ring.svg` (b)); what
  is missing is POCKET(11) for every such ring, not one witness.
* n-general: T-CELLS / T-TIP / T-SLOTS are n-free; the ring's existence is a statement at side ŝ (8 squares, any n ≥ 8);
  the count uses f = n − 8 only.  n = 11 corollary: the type-T ring exists at ŝ and holds one square: 9 < 11.
* Lean `Statements/Open/TypeTChase.lean` (build + audit, 0 sorry): axioms `t_cells`, `t_cells_floor`, `t_tip`
  [T-prose], `two_tilted_ring_exists` [T-computed], `type_t_chase_closes` [C]; theorems `no_two_tilted_bound`,
  `optimal_psiMin_not_twelve_stuck_typeT`.  Obligations: O-T-CELLS / O-T-TIP (in Lean over `sqSet`), O-RING-EXACT
  (the rational witness as a Lean term), O-POCKET-TYPE-T (POCKET(11) on family-stuck rings).
* Reproduce: `bash attempts/A249-type-t-chase/code/run249.sh test|chase|wall|ring2|ring|pocket|summary|pages|ladder`
  (chase 2 min; wall 10 min; ring2 40 min; ring 40 min; pocket 5 min; `logs/STOP`, per-side checkpoints).
