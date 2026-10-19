# THE LAST TWO — STRIP₂ for a tilted C is [F] as A265 stated it (the domain "h_u, h_v < 1" is not "C meets the open box" once C tilts; a drawn free square in the strip) and [M] + [T-computed*] on the true domain (a 5-parameter LEFT-SHADOW certificate, launched); CAPACITY-2 reduces to three gap statements (Lean), the brief's "two squares in the notch need width ≥ 2" is [F] as an argument (squares STACK in the gap; what kills the stack is that the upper square contains O), measured on every ring tried — A266, 2026-09-22

The brief (A266 BRIEF): (1) STRIP₂ for a tilted C and the mirrored orientations; (2) CAPACITY-2 on the non-serving
gap; (3) the chain list.  Tags [T] proved, [T-computed] finite computation with its own check, [T-computed*] a
certificate whose detached chain has not finished, [M] measured, [C] conjecture, [F] false (witness).  Code
`attempts/A266-last-two/code/` (`strip266` the box certificate + tree, `verify266` its verifier, `probe266` the
domain probe and the [F] witnesses, `time266` the price, `cap266` CAPACITY-2 measured, `pages266`, `run266.sh`);
results / certs / logs beside it; pages `docs/residue_map/campaigns/A266-last-two/` (`strip_tilted.svg`,
`miss_region.svg`); Lean `Statements/Open/LastTwo.lean`.  Notation as A265: corner frame BL, wall x = 0, floor
y = 0, c = cos θ_C, s = sin θ_C, w = c + s; C the floater (lowest vertex (h_u + s, h_v), tilt θ_C ∈ [0, 45°]; h_u
its wall distance, h_v its floor distance), T_u = C − h_u e_x, S = T_u ∖ C the STRIP; X the wall toucher above C
(leftmost vertex (0, y_X), tilt φ_X), int X ∩ int T_u ≠ ∅, int X ∩ int C = ∅.

## 0. Verdict

> **STRIP₂ (task 1).**  **[F] as stated in strip_plug.md §1.1 for a tilted C.**  "0 < h_u < 1, 0 < h_v < 1 (it meets
> the open box)" is two different conditions once θ_C > 0: C meets (0,1)² iff **h_u c + h_v s < w − sc** (Lean
> `open_box_tilted`; at θ_C = 0 it is h_u < 1).  Between the two — e.g. h_u = 0.963, h_v = 0.848, θ_C = 31.7°, X flat
> at y_X = 2.81 (φ_X = 12.8°) — a FLAT unit square Q at centre (0.599, 0.820) is in the quadrant, interior-disjoint
> from C (gap +0.084) and X (+0.515) and meets int T_u (depth 0.47): a free square in the strip (`probe266`, exact
> SAT; drawn on `strip_tilted.svg`; two more at θ_C = 42° and 33°).  On the true domain no witness exists: 60/60
> in-domain samples CERTIFY under the box test at radius 0.0025 (36/60 already at 0.02), the exact pocket is empty
> on all of them.  **The hand proof does not carry**: its chord step ("a chord of Q through p ∈ S is shorter than
> h_u < 1") fails at every height below C's left vertex once h_u + sin θ_C > 1 (the chord is bounded by C's lower-left
> edge, at x up to h_u + s), and the tilted lemma is TRUE only with the open-box condition — which the flat proof
> never used.  So the tilted case is a different lemma, and its route is the certificate: **`strip266` [T-computed*]**,
> a 5-parameter box tree on (h_u, h_v, θ_C; y_X, φ_X) with the LEFT-SHADOW test (§1.2: the bad centres of a tilt
> bin lie in the left shadow of C ⊕ Q, so the inner polygon's RIGHT-CLOSURE is subtracted, not the polygon — the
> plain annulus test priced at 170 CPU-h per root cell), own verifier `verify266` (0.4° bins, bisect to depth 8,
> exact tiling), lanes `jam` (φ_X ∈ [0, 45°], the JAM ring's X) and `mir` ([45°, 90°), the mirrored X); launched
> detached (`run266.sh chain`), price §1.3.  Consequence when it lands: 5b of k0_route.md §13 is `pair3` at BL with
> T_u — and **`pair3` has NOT started** (A262's chain3 waits for `search262`, still running at exit; no
> `pair3262_index.jsonl`).  NO-JAM(11) then still lacks 5a (pair3 at TL, same job), 5d (indirect jams, FLOAT2:
> `float262` / `span262` not run — chain3 outputs have not landed) and 6's Lean axiom `jam_count`.
> **CAPACITY-2 (task 2).**  **[T] the reduction** (Lean `capacity_two_of_gap`): CAPACITY-2 ⟸ MISS-IN-GAP (every
> miss of the non-ADJ family is a gap square of an unserved wall) ∧ GAP-HOLDS-ONE-MISS (two interior-disjoint gap
> squares of the same wall never both miss O) ∧ ONE-UNSERVED-WALL (misses at two unserved walls do not both occur).
> **[F] the brief's argument** "two unit squares in the notch need width ≥ 2 > e": width bounds nothing ALONG the
> gap — two near-flat squares STACK in a gap of width 1.17 (A263 §3.3 already measured their tilts ≤ 9.9°).  What
> kills the stack is that the UPPER square contains O: [T] its x-range is a unit-or-wider interval inside [1, s − 1]
> and so contains s/2 in its interior (Lean `gap_interval_centre`, margin w − (s/2 − 1) ≥ 0.06), and [C] its y-range
> contains s/2 (it sits above a unit square on the floor and below the ceiling row's teeth) — the vertical half is
> the wedge / lip geometry A264 left open.  ONE-UNSERVED-WALL: [M] `cap266`'s feasible-only search for a ring with
> wide gaps on two walls (opposite or adjacent) is in the chain (its log says what it reached); the corner forms
> make a wide gap cost a + b ≤ s − sec − w − 1 ≈ 0.75 on that wall while every corner wants one offset ≈ ≥ 0.9
> (three_lemmas.md §1.2), so two wide gaps on the window are implausible but not excluded here.  **[M] no two
> interior-disjoint misses on any ring tried** (`cap266`: A260's 32 non-ADJ adversary rings have an EMPTY miss
> region, cap2 = −9; the wide-gap starts and 40 random non-ADJ rings: in the chain).  A265's FULL-corner witness
> is NOT a ring: its box-middle corner pair W / S′ overlaps by 0.007, so no ring carries it (§2.4).
> **Plainly.**  STRIP₂ was mis-stated for tilted C (fixed: the open-box condition), is true on every point tested
> and is being certified; the sector closes only with pair3, which has not started.  CAPACITY-2 is three gap
> statements, one half of one of them proved; the count route (P1 on the lower gap square) is still the way.
> k0_00 unchanged.

## 1. STRIP₂  (task 1)

**1.1 The [F] and the true domain [T].**  C's lower-left edge is B + t(−s, c), t ∈ [0, 1], B = (h_u + s, h_v); C
meets (0,1)² iff some point of that edge has both coordinates < 1 (the edge is C's extreme towards the corner),
i.e. h_u + s − ts < 1 and h_v + tc < 1 for some t ∈ [0,1]; multiplying by c and s and adding: **h_u c + h_v s <
w − sc** (Lean `open_box_tilted`, one direction; the converse is the same computation).  For a flat C this is h_u < 1
and A265's proof is right; for θ_C = 31.7° with h_u = 0.963, h_v = 0.848 the left vertex sits at height 1.70 and the
whole lower-left edge passes x = 1 above y = 1: C is outside the corner box, the strip S reaches down to the floor
along T_u's lower-left edge, and a flat square in the corner under C meets it (`probe266 --nobox`, three witnesses,
each with exact SAT gaps ≥ 0.06 to C and ≥ 0.5 to X, depth ≥ 0.4 in T_u; page `strip_tilted.svg` left panel).
**Domain of STRIP₂, restated:** h_u ∈ (0, 1), h_v ∈ [0, 1), θ_C ∈ [0, 45°], C meets (0,1)²; X's leftmost vertex on
the wall, X ⊂ quadrant, **X above C** (its lowest point not below C's: y_X − cos φ_X ≥ h_v — in the JAM ring X meets
the TL box, so y_X − cos φ_X > 1), int X ∩ int C = ∅, int X ∩ int T_u ≠ ∅.  Every condition is s-free and m-free.
**1.2 The certificate [T-computed*] (`strip266`).**  Per tilt bin [m − D, m + D] of Q (1° bins), with K the kernel
(tilt m, half-side 1/(2w(D))) and Qo the outer square (half-side w(D)/2), cores / outers of C and X over the box
(A259's CORE lemma, ρ = the |·|₁ radius of the centre: C: r_hu + r_hv + r_θ, X: r_yX + r_φ):  a bad centre q (Q
free of C, X, in the quadrant, meeting int T_u) satisfies q ∉ (C ⊕ Q)°, q + h_u e_x ∈ (C ⊕ Q)° = (T_u ⊕ Q)°.
**LEFT SHADOW [T]** (Lean `left_shadow`): C ⊕ Q is convex, so on the horizontal chord through q the point q is
outside and q + h_u e_x inside ⟹ q is at or left of the chord's left end: q_x ≤ ℓ_{C⊕Q}(q_y) < ℓ_{P_in}(q_y), P_in =
core(C) ⊕ K.  Hence TEST(bin) := {q_x, q_y ≥ half-extent of K} ∩ hull(outer(C) ⊕ Qo − [lo, hi]_{h_u} e_x) ∖ (P_in ⊕
[0, 20] e_x) ∖ (core(X) ⊕ K) contains every bad centre of the bin; CERT iff every bin's TEST has area ≤ 10⁻¹⁰.
PRUNE only when the box misses the domain for EVERY parameter (X's lowest point below the floor or below C's
lowest for all of it; cores of X and C overlap; outers of X and T_u disjoint; outer(C) misses the closed unit box).
Without the right-closure (subtracting P_in itself) the annulus of P_out ∖ P_in on C's right, top and bottom — real
free squares that never meet T_u — is kept and the tree refines h_u to 2⁻⁷ over the whole (h_u, h_v) square:
170 CPU-h per root cell (`time266`, the first run).  Root cells: 27 per lane ([0,1]² × 15° × 0.93 × 15° in
(h_u, h_v, θ_C, y_X, φ_X)), adaptive bisection (tilt radians × 2), depth ≤ 30; resumable per cell, `logs/STOP`.
**1.3 Price and benchmark.**  Box test 0.01–0.1 s (early exit on the first failing bin).  In-domain samples
(`probe266`, 60 at seed 1): CERT 36 / 48 / 55 / 60 of 60 at radius 0.02 / 0.01 / 0.005 / 0.0025 (positions and
radians alike) — the statement has a margin at every point tried, but a SMALL one: 0.005–0.02 in parameter
radius.  **Price (`time266`)**: a 1/1200 sub-cell of root cell 1,1,0 (θ_C, y_X, φ_X ranges 1.25°, 0.093, 1.25°;
full (h_u, h_v) square) costs 535 s and 18 133 leaves, 16 004 of them with h_u, h_v refined to 2⁻⁷ over the WHOLE
square — the left-shadow test changed nothing (the annulus was not the driver): the 1° tilt bins of Q cost a
fixed 0.017 (w(0.5°) − 1/w(0.5°)) of the margin, so every box must shrink to radius ≈ 0.005 in the position
parameters before it certifies, and the same will hold in θ_C, y_X, φ_X.  A root cell is ≈ 6·10⁵ s, the 27 cells
of a lane ≈ 5·10³ CPU-h — **A265's "1–3 CPU-h" was wrong** (it priced the pocket's emptiness, not the margin of the
over-approximation; 0.1° bins would cut the fixed loss to 0.0035 at 5× the per-box cost and still leave ~10⁸
boxes).  Launched instead (`run266.sh chain`, after `cap266` and the 3000 / 1500-sample probes): the `jam` lane on
the six ring-relevant root cells (θ_C < 15°, y_X ≥ 1.63 — the ring's X meets the TL box, so y_X > 2.2 — φ_X ≤ 45°)
with a BUDGET of 150 000 boxes each (≈ 40 min; the unvisited subtrees are written OPEN 'budget', tiled, and the
index records the certified volume fraction per cell), then `verify266` on a 10 % sample.  What this buys is a
certified sub-volume and a sampled margin map, not the lemma; the `mir` lane (φ_X ∈ [45°, 90°), the general
s-free lemma, not needed for the JAM ring whose X is wall 3's START square of sense +) is not launched.  The
lemma's cheaper route is the hand proof (§1.4).
**1.4 What a hand proof would need.**  Q and C are separated by a line through one of their eight edges (SAT);
with C's lower-left edge as the separator, Q lies in the wedge between the wall and that edge line (apex on the
wall at height h_v + c + h_u cot θ_C, opening angle θ_C) and meets the parallelogram T_u ∩ {left of the edge} — a
unit square in a wedge of angle ≤ 45° whose lower part must clear the floor; with the upper-left edge as the
separator Q rests on C's upper-left edge within the strip's band of width h_u s along it and collides with X (X
meets T_u, X above C); with C's other two edges Q is below or right of C and cannot reach S; with Q's own edges the
four cases of A265 §1.3 (iv) recur with C's flank in place of the column wall.  Written here as the case list, not
proved; the certificate is the [T-computed] route and the flat case stays [T].
**1.5 Consequence for the sector and NO-JAM(11).**  STRIP₂ on its domain ⟹ (Lean `strip_of_two_obstacles`,
`jam_sector_of_strip`) the BL sectors of a JAM corner are `pair3` at BL with T_u as the END square.  `pair3`'s
index does not exist: A262's `chain3.sh` waits for `search262` (alive at exit) and then runs float2 → pair3 →
verify → jam → held → sector; nothing of it has landed.  So the BL sector is [T-computed*] on TWO chains (strip266 +
pair3), and NO-JAM(11) lacks: 5a (pair3 at TL), 5d (indirect jams / FLOAT2 corners: `float262`, `span262`), 6's
axiom `jam_count`.

## 2. CAPACITY-2 on the non-serving gap  (task 2)

**2.1 The statement and the miss region.**  Non-ADJ hybrid ring (independent tilts, some wall with a toucher missing
its far slot, open_pairs.md §3.1), three free squares, at most one containing O.  CAPACITY-2: no two interior-
disjoint free squares both miss O.  MISS REGION at tilt ψ: M(ψ) := C(ψ) ∖ int(O + Q_ψ), C(ψ) the exact centre set
(room259); two disjoint misses exist iff for some ψ₁, ψ₂ and an edge normal n of the pair, sup_{M(ψ₂)} ⟨q, n⟩ +
sup_{M(ψ₁)} ⟨q, −n⟩ ≥ h_{ψ₁}(n) + h_{ψ₂}(n) (SAT along n; `cap266.cap2`, 1° grid, every witness pair re-checked by
`free_margin` / `contains_O` / `poly_gap`).
**2.2 The reduction [T] and the stack lemma [T half, C half].**  Lean `capacity_two_of_gap`: from `miss_in_gap`
[C] (a miss is a gap square of some unserved wall — what the ADJ certificates P2 ∧ WE ∧ WS say on ADJ corners and
what the non-ADJ ones P2n / WEn / WSn must say on the rest, marking exactly the gap squares OPEN), `gap_holds_one_miss`
[C] and `one_unserved_wall` [C].  *GAP-HOLDS-ONE-MISS.*  Two interior-disjoint free squares F₁, F₂ with a point at
depth < 1 in the same unserved slot: in the gap strip of width ≤ 1.169 both have tilts ≤ 9.9° and x-ranges of
width w ≥ 1 inside the gap; the gap lies in x ∈ [w(φ₁), s − w(φ_W)] ⊂ [1, s − 1] (a ≥ 0, b ≥ 0); they cannot be
side by side, so one (F₂) is above the other; **[T] F₂'s x-range contains s/2 with margin ≥ w − (s/2 − 1) ≥ 0.06**
(`gap_interval_centre`: a unit interval inside [1, s − 1] contains s/2 because s < 4); **[C] F₂'s y-range contains
s/2**: F₂'s lowest point is ≥ cos ψ₁ ≈ 1 above the floor (it clears F₁) and its top is below the ceiling row's
teeth (depth ≥ cos φ_ceiling, TOOTH) — y₀ ∈ (s/2 − w, s/2) needs y₀ < s/2 = 1.94, i.e. F₂ not higher than 1.94:
true when F₂ is a gap square (its depth < 1 in the slot gives y₀ < 1) — so on the depth-< 1 reading BOTH halves hold
and F₂ ∋ O, EXCEPT that "F₂ above F₁" is derived from the strip picture at common tilt: the wedge case (φ_W ≠ φ₁)
and the sub-case 1 + w − sec ≤ e < sec are the [C] of A264 §2.5, unchanged.  The brief's "two unit squares in the
notch need width ≥ 2 > e" is [F] as an argument (stacking), right in its conclusion on the strip picture.
**2.3 ONE-UNSERVED-WALL [M → C].**  A wide gap (e ≥ 1 + w − sec ≈ 1) on a wall costs its offsets a + b = s − sec −
w − e ≤ 0.79 (at 5°), while each of its two corners is a one-sense corner whose form (three_lemmas.md §1.2) wants
the END offset ≥ cos α − a tan α ≈ 0.9 at small tilts; a single wide gap exists (A263's witness at 2°, e = 1.06),
two on the same ring is what `cap266`'s feasible-only widening search (walls {0,2} and {0,1}) probes: the least
shift it reaches on two walls at once is in `logs/cap266.log`.  Not a proof; the count route of strip_plug.md §3.2
(P1 on the lower gap square) does not need it.
**2.4 Measurements [M] (`cap266`, in the chain: `results/cap266.json`).**  At exit: A260's 32 non-ADJ adversary
rings (shifts ≤ 0.12): the miss region is EMPTY at every tilt (cap2 = −9, every free square contains O — A263's
ROOM holds there); the wide-gap starts (one wall; two opposite; two adjacent, each climbed 40 feasible steps on
cap2) and 40 random non-ADJ rings at ŝ follow.  A265's FULL-corner witness (b = 0.994, φ_W = 14.3°, a′ = 0.490,
φ₁′ = 25.5°, e′ = 0.6, φ_W′ = 38°) cannot be completed into a ring: the corner pair W / S′ at the box middle
overlaps by 0.007 (exact SAT), and the best margin reachable with walls 2, 3 free is −0.17 — the miss there was a
box relaxation of the corner pair (still sound as a P2 miss at 3.8771 where P2 is not required).  Page
`miss_region.svg`: the worst ring's miss region and its best-separated pair; grey stipple until the chain writes it.

## 3. The chain list — `k0_route.md` §13, updated links

5b: STRIP₂ [F] as stated for tilted C → restated with the open-box condition; [T] flat C (A265), [M] 60/60 + 323
rings, [T-computed*] `strip266` (jam lane first) — and `pair3` not started.  10d: CAPACITY-2 = three gap statements
[T reduction, Lean]; `gap_interval_centre` [T]; the rest [C]; `cap266` [M].  Still [C] or waiting: 5a/5b pair3
(chain3), 5b strip266, 5d, 6's `jam_count`, 8a–8b chains, 10a–10c chains, 10d's three gap statements, the [T-prose]
axioms, the stretch.

## 4. Lean, reproduce

`Statements/Open/LastTwo.lean`: theorems `left_shadow`, `open_box_tilted`, `gap_interval_centre`,
`capacity_two_of_gap`; axioms [C] `miss_in_gap`, `gap_holds_one_miss`, `one_unserved_wall`; build + audit 0 sorry.
Reproduce: `python probe266.py` (2 min), `python probe266.py --nobox` (the [F] witnesses), `python time266.py`
(the price), `bash run266.sh chain` (cap266 → strip266 jam → verify266 → strip266 mir → verify266 → pages266).
