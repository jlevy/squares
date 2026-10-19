# SNAP-DOWN by directionality — Lemma STACK, the wall click, Lemma REDUCE, and what closes — A245, 2026-09-16

The PI (20:00): *"is there a way to show that ANY ring that doubly meets all edge slots can be snapped down in some
way — something with the DIRECTIONALITY of the meeter tilts, to show a subset can always be reduced to simple."*
This file makes the chain STACK → WALL-CLICK → REDUCE exact for every n, proves what is a theorem, states every
feasibility condition of the click as a hypothesis and tests it on every wall of every testbed the lab has, and
says plainly what closes.  Tags: [T] proved, [S] routine given cited items, [M] measured, [F] false as stated (with
the witness), [C] obligation.  Sources: `attempts/A243-reach-root/notes/wall_slot243.md` (WALL-SLOT, SLOT-MET, the
twelve border cells, the mutual supply), `two_grains.md` (CLICK, EXTENT, LEAN-SLIDE, FLUSH), `realign.md` §1
(WALL-EXCESS, Lemma WALL-F's chord), `ring_swap.md` (SWAP, CELLS, RAISE, CORNER-SWAP), `cross.md` (PARTNER-TORQUE),
`wedged_seal.md`, `pocket_waste.md` §1 (TILT-MIN, DEPTH-BUDGET), A244's 12-stuck candidates.  Code
`attempts/A245-snap-down/code/` (`geom245` n-general geometry + wall frames, `stack245` the sampled lemma,
`lp245` the fixed-tilt LP with a free subset, `click245`, `reduce245`, `testbeds245`, `summarise245`, `pages245`,
`test245`, `run245.sh`); results `results/snapdown245.md` (+ `stack245.jsonl`, `click245.jsonl`); pages
`docs/residue_map/campaigns/A245-snap-down/{stack_cases,wall_click,reduce}.svg`; Lean `Statements/Open/SnapDown.lean`.

## 0. Verdict

> **[T] Lemma STACK, in the form that is true** (§1): a MUTUAL wall pair — B the meeter of corner c and B′ the
> meeter of the adjacent corner c′, both touching their common wall, B meeting c′'s slot and B′ meeting c's — is
> ORDERED on the wall (B below B′), its vertical CLEARANCE is `< 4 − s` (they interleave in height or float with a
> gap below `4 − s`), both squares meet BOTH slots of the wall, and the pair's stack height is at least the sum of
> its WALL-EXCESS chords, `≥ 2`.  The contact, when there is one, is one of four vertex-on-edge types decided by
> `θ + θ′ ≶ 90°` and `θ ≶ θ′` (the table of §1.4), parallel only for EQUAL tilts.  **[F] The PI's dichotomy**:
> contact is NOT forced (two flat squares at `[0,1]×[0.9,1.9]`, `[0,1]×[1.95,2.95]` are a mutual pair at 3.82 with
> a gap 0.05; floating pairs are 2 235 of 4 000 sampled at 3.82, 326 at 3.99), no handedness pairing is forced
> (all nine occur below 4; opposite-handed pairs are 1 187 / 4 000 at 3.82 and fade above 4: 101 / 1 500 at 4.0,
> 6 / 1 500 at 4.1), and a same-handed pair of unequal tilts rests vertex-on-edge exactly like a lean — Lemma W's
> torque senses (same for same-handed, opposite for opposite-handed) are the only directionality difference, and
> A240's PARTNER-TORQUE says the contact torques do not read handedness.
> **[T]/[C] WALL-CLICK** (§2): the along-wall extent is monotone — the chord sum `1/max(cos θ, sin θ) + 1/max(cos θ′,
> sin θ′)` falls to exactly 2 and the flush stack of height 2 fits inside the pair's former wall range [T] — but the
> stack's footprint `[0,1] × [y₀, y₀+2]` is inside `B ∪ B′ ∪ Free` only under a ROOM hypothesis (H-ROOM: the wedge
> under B's lower-left edge, where A's tip sits by SLOT-MET, the wedge above B′'s upper-left edge, where A′'s tip
> sits, and the pocket between the pair are free of other squares); under H-ROOM the click is Lemma SWAP and needs no
> path [T]; without it the LOCAL click (the pair alone, everything else frozen) is feasible on 80 / 115 wall pairs
> of A244's 12-stuck candidates, 177 / 550 of the four-crowds' (blocked or side-raising otherwise; blockers A 156,
> A′ 152, another slot meeter 148, a free square 32) and on the MUTUAL walls on 5 / 20 and 2 / 19; the GLOBAL click
> (all centres re-minimised) is never blocked but the side RISES on 7 / 115 and 102 / 550 (max 0.049): **[F] "the
> packing after the click is at no larger side"** as a lemma.  **[T] REDUCE** (§3): both reductions are Lemma
> CELLS — the lower flush square slides into the corner iff the corner box has no other meeter (`|M({c00})| ≤ 1`),
> and the 3-for-3 is `cells_swap` with `k = 3` (Lean theorem `reduce_three_for_three`: three squares up, the corner
> domino and one leftover down, a packing containing the domino at the same side); the click contributes only by
> lowering `|M(Π)|`, and a flush stack placed at `y₀ ≥ 1` (possible iff the pair's former top is `≥ 3`) leaves
> `M({c00, c01}) = {A, B_flush} ∪ (free squares in the domino)`: [C] as a room count.  **What closes: nothing.**  On
> the only objects the conjecture is about — A244's 12-stuck candidates, all at S ≥ 4.00001 — the mutual wall pair
> with wall contact is the exception, not the rule: 7 of 308 walls (20 mutual by cells, 102 with a wall pair at all);
> their slots are supplied OWN 924 : ADJ 192 : FREE 207 over 616 slots, and only 342 of 616 corner meeters touch a
> wall.  STACK's setting (the PI's ring of wall grains resting on each other) is not the shape of a 12-stuck
> packing; the snap-down would have to handle the own-tip and free-square suppliers, where no wall pair exists, and
> there it is RAISE(0 → 1) again.  STUCK-4(11) on [3.82, ŝ] is unchanged; SNAP-DOWN(11) is stated as the axiom
> `snap_down` [C] with its consequence `no_twelve_stuck_of_snap_down` a theorem.

## 1. Lemma STACK (any n; side 2 + √2 ≤ s < 4)

**1.1 Setting.**  Wall frame: the shared wall is `u = 0`, corner c the origin, c′ at `(0, s)` (`geom245.to_frame`:
every wall of `[0, s]²` is mapped so).  The wall's four cells (`wall_slot243.md`): c00 = (0,1)², c01 = (0,1)×(1,2),
c′01 = (0,1)×(s−2, s−1), c′00 = (0,1)×(s−1, s); below 4 they cover the strip `(0,1)×(0,s)`.  A square MEETS a cell
iff their interiors meet.  H-WALL: B and B′ touch `u = 0` (PUSH / HOLD's setting at a locked corner, Lemma A2; NOT a
consequence of 12-stuck — §4).  A wall toucher of tilt `θ ∈ [0°, 90°]` with wall vertex `L = (0, ℓ)` has vertices
`V = L + (sin θ, −cos θ)`, `R = V + (cos θ, sin θ)`, `T = L + (cos θ, sin θ)`; `θ = 0` is `[0,1]×[ℓ−1, ℓ]`, `θ = 90°`
is `[0,1]×[ℓ, ℓ+1]` (`wall_pose`, `wall_params`).  Cell conditions in these coordinates [T, exact for tilted
squares since V, T have `u < 1`]: B meets c00 ⟺ `ℓ − cos θ < 1`; B meets c′01 ⟺ `ℓ + sin θ > s − 2`; B′ meets c′00
⟺ `ℓ′ + sin θ′ > s − 1`; B′ meets c01 ⟺ `ℓ′ − cos θ′ < 2`.  MUTUAL: all four.

**1.2 Lemma STACK (a) ORDER [T].**  *B, B′ interior-disjoint unit squares touching `u = 0`, B meeting c00 and c′01,
B′ meeting c′00 and c01, `s ≥ 2 + √2`.  Then every wall point of B is below every wall point of B′.*
*Proof.*  Let `p ∈ int B ∩ c00`, `p′ ∈ int B′ ∩ c′00`, `L` a lowest wall point of B, `L′` a highest wall point of
B′; suppose `y_{L′} ≤ y_L`.  A unit square has height `≤ √2`, so `y_{L′} ≥ y_{p′} − √2 > s − 1 − √2 ≥ 1 > y_p` and
`y_L ≤ y_p + √2 < 1 + √2 ≤ s − 1 < y_{p′}`.  Parametrise the segments `σ′ = [L′, p′]` and `σ = [L, p]` by the
abscissa `ξ`: at `ξ = 0`, `σ′ ≤ σ`; at `ξ* = min(x_p, x_{p′})`, `σ′(ξ*) ≥ y_{L′} > 1 > y_p = σ(ξ*)` if `ξ* = x_p`, and
`σ′(ξ*) = y_{p′} > s − 1 > max(y_L, y_p) ≥ σ(ξ*)` if `ξ* = x_{p′}`.  So the segments cross at some `ξ₀ ∈ (0, ξ*]`
when `y_{L′} < y_L`; the crossing lies on the half-open segments `(L′, p′]`, `(L, p]`, which are interior to B′, B
(a segment from a point of a convex body to an interior point is interior except at its start) — contradiction.
If `y_{L′} = y_L =: ℓ`: a tilted square contains the open 90° wedge at its wall vertex, which contains the direction
`(1, 0)`, so two tilted squares sharing the wall vertex overlap; a flat B′ whose HIGHEST wall point is `(0, ℓ)` lies in
`{y ≤ ℓ}` with `ℓ < s − 1 < y_{p′}`, and a flat B whose LOWEST wall point is `(0, ℓ)` lies in `{y ≥ ℓ}` with
`ℓ > 1 > y_p` — contradictions.  ∎  [M] 16 000 / 16 000 sampled mutual pairs (`stack245.jsonl`, four sides).

**1.3 (b) CLEARANCE, (c) INNER SLOTS, (e) CHORDS [T].**  (b) B's top vertex T is at height `ℓ + sin θ > s − 2` and
B′'s bottom vertex V′ at `ℓ′ − cos θ′ < 2`, so `y_{V′} − y_T < 4 − s`: the pair interleaves in height or floats with
a gap `< 4 − s` (`< 0.18` on the window; `≤ 0` at and above 4).  (c) B is convex, has a point with `u < 1, v < 1`
and one with `u < 1, v > s − 2 ≥ 1.41`, so it crosses `(0,1)×(1,2)`: B meets c01; likewise B′ meets c′01.  Hence in
the mutual case BOTH slots of the wall are doubly met by `{B, B′}` alone, and A, A′ (the corners' other meeters)
are needed for the corner boxes only.  (e) Lemma WALL-F (`realign.md` §1.1): the pair's chords on `u = 1/√2` are
disjoint segments of the pair's wall range, so the stack height `H = (ℓ′ + sin θ′) − (ℓ − cos θ) ≥ 1/max(cos θ,
sin θ) + 1/max(cos θ′, sin θ′) ≥ 2`, with equality iff both are flush and stacked.  [M] `H − chords ≥ 0` on
16 000 / 16 000 (min 0.000).  ∎

**1.4 (d) The contact table [T].**  With B below B′ (a), B's upper boundary from L is the edge L→T (rising at
slope `tan θ` up to `x = cos θ`) then T→R (falling at `−cot θ`); B′'s lower boundary from L′ is L′→V′ (falling at
`−cot θ′` up to `x = sin θ′`) then V′→R′ (rising at `tan θ′`).  A rising and a falling edge converge, so
disjointness forces the first vertex to arrive before the crossing; past it the boundaries diverge unless the
trailing edge is steeper — B′ catches B's T→R iff `cot θ′ > cot θ` (`θ′ < θ`), B catches B′'s V′→R′ iff `θ > θ′`.
Hence, when the pair rests: `θ + θ′ > 90°` (T first, `cos θ < sin θ′`): **T ∈ L′V′**, or **V′ ∈ TR** if `θ′ < θ`;
`θ + θ′ < 90°` (V′ first): **V′ ∈ LT**, or **T ∈ V′R′** if `θ > θ′`; `θ + θ′ = 90°`: `T = V′` corner-to-corner;
**equal tilts**: the parallel contact `L′V′ ∥ TR` (`θ ≥ 45°`) or `V′R′ ∥ LT` (`θ ≤ 45°`) — the ring's 2|5.  Contact
heights: V′∈LT `ℓ′ = ℓ + cos θ′ + sin θ′ tan θ`; T∈V′R′ `ℓ′ = ℓ + sin θ + cos θ′ − (cos θ − sin θ′) tan θ′`; T∈L′V′
`ℓ′ = ℓ + sin θ + cos θ cot θ′`; V′∈TR `ℓ′ = ℓ + sin θ + cos θ′ − (sin θ′ − cos θ) cot θ`.  Handedness: `'++'`
⟹ `θ + θ′ < 90°` (the contact is on B's upper-LEFT edge unless `θ > θ′`), `'−−'` ⟹ T first; opposite-handed
pairs fall in either regime.  [M] 15 997 / 16 000 sampled contacts (B′ lowered onto B by bisection, `contact_ell`)
match the table, the 3 exceptions `θ + θ′ = 90°` within 1e-4°; every one of the 20 (handedness, type) classes
occurs at 3.82 (page `stack_cases.svg`: the floating witness and one resting pair per type, all cells checked).
[M] Lowering B′ onto B keeps the four cells on 4 584 / 4 584 grid slices (`test245.test_contact_keeps_cells`), so
a resting configuration exists in every mutual slice — but nothing forces the packing to be in it.

**1.5 What each case forces.**  Only the cell inequalities of 1.1 and the contact heights of 1.4: `ℓ ∈ (max(cos θ,
s − 2 − sin θ), 1 + cos θ)`, `ℓ′ ∈ (max(ℓ′_contact, s − 1 − sin θ′), min(2 + cos θ′, s − sin θ′))`.  No tilt floor
(TILT-MIN binds upward, `pocket_waste.md` §1), no depth constraint beyond DEPTH-BUDGET for the corner pairs (A, B),
(A′, B′), and — the point — no contact: the pair's vertical slack is the whole interval `(ℓ′_contact, 2 + cos θ′)`,
of length up to `4 − s` at the wall.  **n-general form**: STACK (a)–(e) hold for any n at any side `2 + √2 ≤ s < 4`;
at `s ≥ 4` (a), (c), (e) still hold and (b) forces interleaving; the twelve-cell hypothesis itself is A243's and
needs `s < 4` for the cells to cover the border strip.

## 2. WALL-CLICK

**2.1 The move.**  Rotate B and B′ jointly toward flush (`'+'` → 0°, `'−'` → 90°, A223's schedule), all other
tilts fixed, the side re-minimised at every step by the fixed-tilt LP (`lp245.fixed_tilt_min`, Lemma GRAIN-LP's
polyhedron with the separating axes re-chosen until stable) over (i) the pair's centres only — LOCAL: feasible iff
`s_local(t) ≤ s₀`, since every other square is frozen — or (ii) all centres — GLOBAL, A223's variant B.

**2.2 What is a theorem.**  [T] EXTENT: the chord `1/max(cos θ, sin θ)` is strictly decreasing toward flush on each
side of 45°, so the pair's chord sum falls monotonically to 2 and (1.3 e) the flush stack `[0,1] × [y₀, y₀ + 2]`
fits inside the pair's former wall range for every `y₀ ∈ [ℓ − cos θ, ℓ′ + sin θ′ − 2]` (an interval of length
`H − 2 ≥ 0`, the pair's along-wall waste).  [T] Under **H-ROOM** — `[0,1] × [y₀, y₀+2] \ (B ∪ B′)` meets the interior
of no other square — the two flush squares are a Lemma SWAP exchange for `{B, B′}` at the SAME side, no path needed.
**Where H-ROOM fails**, exactly: the footprint minus the pair consists of (α) the wedge between the wall and B's
lower-left edge LV, apex L, angle θ, height `cos θ` at the wall — where A's tip sits whenever A meets c00 from beside
B (SLOT-MET's cap square; TILT-MIN's mode (a)); (β) the wedge between the wall and B′'s upper-left edge L′T′,
apex L′, angle `90° − θ′` — A′'s place; (γ) the pocket between the pair (the wedge between LT and L′V′ at the
wall and the gap beyond T, V′); (δ) the slivers right of the tilted squares inside `x ≤ 1`.  (α) is avoided iff
`y₀ ≥ ℓ`, i.e. `ℓ′ + sin θ′ − ℓ ≥ 2`; (β) iff `y₀ + 2 ≤ ℓ′`, i.e. `ℓ′ − ℓ + cos θ ≥ 2`; both together need `H ≥ 2 +
(ℓ − y_min) + (y_max − ℓ′) = 2 + cos θ + sin θ′` — a large along-wall waste the pair need not have.  So the click's
feasibility is: A out of (α), A′ out of (β), the pocket (γ) empty of free squares — the brief's three conditions,
each a pose fact of the corner crowd, none supplied by 12-stuck or by handedness.

**2.3 [M] On every wall pair of every testbed** (`results/snapdown245.md` §3; 20 steps; 1 164 wall rows):
* A244's 12-stuck candidates (77, S ≥ 4.00001): 115 wall pairs (102 with H-WALL; 20 mutual, 7 of them with
  H-WALL).  LOCAL feasible at `s₀` on 80, blocked on 21 (blockers A 15, A′ 14, another slot meeter 8, free 6),
  side-raising on 14; on the mutual walls 5 / 20.  GLOBAL never blocked, end `≤ s₀` on 108 / 115 (mutual 18 / 20),
  monotone 79 / 115, max rise 0.004.
* The 193 four-crowds (S ≥ 4.0014): 550 pairs (541 H-WALL, 19 mutual).  LOCAL feasible 177, blocked 206, raising
  167 (blockers A 156, A′ 152, slot meeter 148, free 32); mutual 2 / 19.  GLOBAL end `≤ s₀` on 448 / 550 (mutual
  8 / 19), monotone 224 / 550, max rise 0.049 above `s₀`.
* The rings (A239 / A226, 8–9 squares, not 12-stuck): 40 pairs, LOCAL feasible 35 / 40, GLOBAL trivially down (an
  8-square ring re-packs below 3.4).
* In contact before the click: 25 / 115, 177 / 550, 16 / 40 — a floating pair is the common case.
So the joint rotation is feasible about a third of the time with everything else frozen, and even with everything
free the side can rise: the click is not side-non-increasing, and the brief's "packing at no larger side" holds
under H-ROOM only.  Page `wall_click.svg` (a feasible local click on `w043_crowd`, frames t = 0, ½, 1; a blocked one
on `w036_crowd` with its blockers; the global end).

## 3. Lemma REDUCE

**3.1 Both reductions are Lemma CELLS [T].**  After a click the pair is two flush squares on the wall.  (i)
Translating the lower one into the corner slot is a packing iff the swept region `[0,1] × [0, y₀+1]` meets no other
square — i.e. `|M({c00})| ≤ 1` (K0-FREE), "A out of the corner box"; exchanging A for a square in the vacated room
first is the 2-for-2 `|M({c00, c01})| ≤ 2` (Lemma CELLS, `cells_swap`), which needs no click at all.  (ii) The 3-for-3
`{A, B, B′} → {c00, c01, leftover}` is `cells_swap` with `k = 3`: Lean `reduce_three_for_three` (a theorem, std
axioms only) — three squares picked up, the domino and one leftover put down under exactly `cells_swap`'s
hypotheses, the result a packing at the same side containing `ContainsPins {(c,0,0), (c,0,1)}`.  The room the click
frees is the pair's along-wall waste `H − 2` plus the tilt slivers; the leftover must be a unit SQUARE in
`(A ∪ B ∪ B′ ∪ Free) \ domino`, a room statement (H-LEFTOVER), decided per configuration (`reduce245.place_one`,
A222's `cspace` + exact re-check).  [T] What the click changes in the count: a flush stack with `y₀ ≥ 1` meets c01
with its lower square only, so `M({c00, c01}) = {A, B_flush} ∪ {free squares meeting the domino}`; `y₀ ≥ 1` needs
the pair's former top `ℓ′ + sin θ′ ≥ 3` (it is `> s − 1`, so this is `≥ 3` against `> 2.82`: not automatic).
**3.2 [M]** (`snapdown245.md` §4): before any click the wall column is CELLS-reducible on 295 / 308 of A244's walls
(k = 2 direct 136, 3-for-3 placed 116), 739 / 772 of the four-crowds', 84 / 84 of the rings'; after the local click
70 / 94, after the global 86 / 115 (four-crowds 307 / 344, 425 / 550) — the click does not raise the reducible
fraction.  Every testbed sits at S ≥ 3.877 (rings) or ≥ 4 (12-stuck, four-crowds), where a domino plus leftover is
room at 4, not a kill: the tables exercise the choreography, as the brief foresaw.  Page `reduce.svg`.

## 4. Does STACK + WALL-CLICK + REDUCE give STUCK-4(11) below 4?  No — and why

1. **STACK's domain is the mutual case with wall contact.**  12-stuck gives, per wall slot, a second meeter that
   is (a) the adjacent corner's meeter, (b) the corner's own other meeter, or (c) a free square (A243 §3).  On
   A244's 12-stuck candidates the supply is OWN 924 : ADJ 192 : FREE 207 over 616 slots; walls with BOTH slots
   ADJ-supplied: 20 of 308; with a wall-touching pair at all: 102; mutual AND H-WALL: 7.  Only 342 of 616 corner
   meeters touch any wall.  The shape of a 12-stuck packing is not a ring of wall grains resting on each other; it
   is corner crowds whose own tips and free squares fill the slots.  In cases (b), (c) there is no wall pair, no
   stack, no click: the reduction is RAISE(0 → 1) for that wall's column, unchanged.
2. **In the mutual case the click is [C] (H-ROOM) and REDUCE is [C] (H-LEFTOVER / the free squares in the
   domino)** — both room statements about A, A′ and the three free squares, i.e. POCKET(11) on the wall-grain
   family (A243 §4 (ii)) with the pair's along-wall waste `H − 2` as the only new quantity, and `H − 2` is not
   bounded below by anything here (a floating pair has `H = e + e′ + gap`, gap `< 4 − s`).
3. **Directionality adds nothing to the geometry**: the contact type is set by `θ + θ′` and `θ − θ′` (1.4), not by
   handedness; the opposite-handed lean slides (LEAN-SLIDE, A223) and so does the same-handed vertex-on-edge
   contact (the same affine row); torque senses (Lemma W) enter only a force argument, which STUCK-4 in its
   unlocked form does not have and which A240 showed is not an obstruction.
4. **Where the opposite-handed case of STACK occurs**: freely below 4 (1 187 / 4 000 at 3.82), rarely at 4 and
   above (101 / 1 500 at 4.0, 6 / 1 500 at 4.1; all 39 mutual testbed pairs are same-handed) — a frequency effect
   of the interleaving (b) forces at `s ≥ 4`, not a lemma; nothing in §2–3 distinguishes it.
**n-general.**  STACK holds for every n at `2 + √2 ≤ s < 4` (1.5); EXTENT and the SWAP under H-ROOM are n-free;
REDUCE's count is n-free.  For `n ≥ 16` the side is `≥ 4` and the twelve-cell hypothesis is empty; for `n ≤ 15`
below 4 the chain has the same shape and the same two room obligations.  **k0_00 / STUCK-4(11) unchanged.**

## 5. Lean, files, obligations

`Statements/Open/SnapDown.lean`: `wallSlot`, `MeetsSlot`, `TwelveStuck`, `TouchesLeftWall`, `MeetsCell`;
`lemma_STACK` (axiom, [T] in prose: order + clearance, n-general); `snap_down` (axiom [C]: SNAP-DOWN(11), the
existence of an exchange to a corner-pinned packing at no larger side); `reduce_three_for_three` (theorem, std
axioms: the 3-for-3 as `cells_swap`, `ContainsPins {(c,0,0), (c,0,1)}`); `no_twelve_stuck_of_snap_down` (theorem:
SNAP-DOWN + k1-a's kill + the 3.82 bound ⇒ no 12-stuck packing on the window); `twelve_stuck_teleport_stuck`.
`lake build` + `lean/audit.py` exit 0, no sorry.  Obligations: O-STACK-LEAN (1.2 in Lean: the segment-crossing
argument, routine); O-ROOM (H-ROOM / H-LEFTOVER as pose statements of the corner crowd — the residue); the
12-STUCK hypothesis itself rests on SLOT-MET [S] (A243, O-SLOT-MET).  Reproduce: `bash attempts/A245-snap-down/
code/run245.sh stack | click | test | pages` (click resumable, `logs/STOP`).
