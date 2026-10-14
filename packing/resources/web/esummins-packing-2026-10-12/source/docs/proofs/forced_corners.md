# Forced corners and forced cells on a gallery page — A178, 2026-09-09

What a page of `docs/shadows/a57v4/` (classes k5_11, k5_16, trump5) or `docs/shadows/k0v4/`
(k0_00) is REQUIRED to contain beyond its record — the corners and slots that must be met by two
distinct squares — stated on the page's own object at s0, with every hypothesis settled.  Tags:
[T] proved here or by the cited lemma, [S] supported, [M] measured, [F] false, [C] Lean
obligation.  Sources: `slot_crowds.md` §1–2 (Lemma SLOT-CROWD, Lemma CONT, the clip census),
`k0_route.md` §3–4 (K0-FREE, K0-WIDEN), `sideband.md` §2–3 (Lemma A1, Lemma A2, Theorem B),
`protected_trees.md` §1–2 (what a tree node at s0 says about a packing at side m), the A56/A61/
A114/A146 scoreboard (`attempts/A56-sparametric/results/scoreboard.json`, 52/52 FULL), A53's
class table (`attempts/A53-simple-strata/results/name_to_slots.json`).  Code:
`attempts/A178-gallery-geometry/code/classes178.py` (the tables of §6 are computed, not copied).

## 0. Verdict

> **[T] Theorem FC.**  Let S be a Young class with pin set P_S, and let p = (c, i, j) be a cell of
> the census (corner c, offsets i, j ≤ 2) that is Young-completable for S, UNCLIPPED, not a pin,
> and whose extension class T = S ∪ {p} is dead on the closed window [191/50, s0] (a FULL row of
> the scoreboard).  Let P be any packing at side m ∈ [3.82, s0] containing the pins of S, and
> F = Δ_λ P its dilate to s0 (λ = s0/m ∈ [1, λ_max], λ_max = s0/3.82 = 1.0149426).  Then **two
> distinct NON-pin squares of F have interiors meeting the widened open slot box**
>
>     B_p⁺ := (i, i + 1 + π_i) × (j, j + 1 + π_j)   in c's corner frame,   π_i := (λ_max − 1)(i + 1 + 1/√2),
>
> π_0 = 0.025509 (= K0-WIDEN's w), π_1 = 0.040452, π_2 = 0.055395.  Every page of a57v4 is a node
> whose hypothesis is about such an F (protected_trees.md §2, Step 1), so the requirement is a
> hypothesis of the page, free of charge.
>
> **[T] Corollary FC-corner (i = j = 0, an unpinned corner).**  Both meeters lie in c's quadrant,
> so A169's Theorem B applies at c_box = 1 + π_0: each meeter is a NON-LONELY pose (the lonely
> clip is a sound clip of both roles, `multibox.normalise(corners=...)`), and by Lemma A2 their
> centres lie in two DIFFERENT cells of the 2 × 2 grid at threshold 1 + π_0 in c's frame (six
> unordered cell pairs; the pair (NE, NE) is excluded by Lemma A2, the other same-cell pairs by
> the ℓ∞ bound).  For k5_11 that corner is TR(0,0); for trump5 it is TL(0,0); k5_16 has none
> (all four corners pinned); k0_00 has all four, CONDITIONALLY (§5(e)).
>
> **[T] Corollary FC-slot (i + j ≥ 1).**  Only Lemma A1 survives: the two meeters' centres are at
> ℓ∞-distance ≥ 1/√2.  Theorem B does NOT apply (the slot frame is not a quadrant: a meeter may
> extend beside the backing pin, §5(f)), so there is no lonely clip at a slot; the requirement is
> consumed as a partner-existence cut (a first meeter's piece with no admissible partner is dead).
>
> **[T] Corollary FC-count (what the page's roles are).**  The non-pin squares of F are the
> conditioned square(s) H and the free squares.  Hence at every forced cell **at least one FREE
> square (distinct from every pin and from every H) meets B_p⁺**, unconditionally; and **two free
> squares** when every H provably misses B_p⁺ (A161's exact miss test on H's box).  Two forced
> cells p, q whose widened boxes are at Euclidean distance ≥ √2 are met by DISTINCT free squares
> (a unit square's interior has diameter < √2), so their roles may share one multibox node; closer
> cells must be taken in separate rounds (`geo178.groups`).
>
> **What is new against `slot_crowds.md` §1.2 (2026-09-04).**  The scoreboard closed since: k6_21
> (trump5 + BR(0,1)), k6_27 (k5_16 + BR(1,0) / TL(1,0)), k6_23 (k5_11 + TR(0,0), k5_16 + BL(1,0),
> trump5 + TL(0,0)) and k6_07 (trump5 + BL(0,2)) are all FULL [191/50, s0].  So trump5 now has SIX
> usable cells including its only unpinned corner TL(0,0) — the PI's "TL00 corner pair" — and
> k5_16 six, k5_11 four (§6); no usable cell of any of the three classes is window-partial any
> more, so ŝ′ = s0 for all of them.

## 1. Setting

Packings, classes, pins, `ContainsPins`, the corner frame (u, v) = distances from c's two walls,
the slot frame Φ_p (origin at the cell's backed vertex, B_p = [0,1]² in it), completable /
clipped / extension class / W_T exactly as in `slot_crowds.md` §1.  Dilation Δ_λ moves centres
by the factor λ and leaves sizes and tilts alone (`closed_disjoint_bridge.md` Lemma B.0): the
image of a square Q is the translate Q′ = Q + (λ − 1) c_Q, and F = Δ_λ P is a family of eleven
closed unit squares, pairwise disjoint as closed sets, inside [0, s0]² with positive wall margins.
On a page the pins of F are axis-aligned squares with centres within (λ − 1) A_S ≤ δ_pin of the
s0 slots (A57's slack pin boxes, half-width δ_pin = 0.01, core a = 0.49; A60's c0 tree has
δ_pin = 3·10⁻⁸ and is a statement at m = s0 itself), the conditioned squares H are the record's
boxes with their certified cores, and the free squares are the budget.  "Non-pin square of F" =
the dilate of a non-pin square of P (the correspondence is the identity on indices).

## 2. [T] Theorem FC — proof

*Step 1 (at side m).*  P contains the pins of S at side m ∈ W_T = [3.82, s0].  Lemma SLOT-CROWD
(`slot_crowds.md` §2) gives n_p ≥ 2: at least two non-pin squares Q₁, Q₂ of P have interiors
meeting the open slot box int B_p(m) = (i, i + 1) × (j, j + 1) in c's frame at side m.  Its
proof is the teleport: with n_p ≤ 1 replace the meeter (or, if n_p = 0, any non-pin square — N ≥
1) by the slot square B_p(m) itself; the result is a packing at side m containing the pins of
T = S ∪ {p} (the slot square is inside the container, and its interior is disjoint from every
other square because the cell is unclipped and had no other meeter), contradicting T's kill.  The
window matters here only through m ∈ W_T; §5(a) settles the endpoint m = s0.

*Step 2 (transfer to F).*  Let q ∈ int Q₁ ∩ int B_p(m), written in c's frame at side m as
q = (q_u, q_v) with i < q_u < i + 1, j < q_v < j + 1.  A corner frame is x ↦ x or x ↦ m − x per
coordinate, and the same map at s0 applied to F is x ↦ x or x ↦ s0 − x; for a point of Q′ =
Q + (λ − 1) c_Q the frame coordinate transforms as u′ = u + (λ − 1) u_c where u_c is the CENTRE's
frame coordinate (for the reflected coordinate: s0 − (x + (λ−1) c_x) = λ m − x − (λ−1) c_x =
(m − x) + (λ − 1)(m − c_x)).  So q′ := q + (λ − 1) c_Q ∈ int Q₁′ (a translate of an interior
point) has frame coordinates q′_u = q_u + (λ − 1) u_c, and since |q − c_Q| ≤ 1/√2 per coordinate
(`sideband.md` (F1)), u_c ∈ (i − 1/√2, i + 1 + 1/√2).  Hence

    q′_u < i + 1 + (λ − 1)(i + 1 + 1/√2) ≤ i + 1 + π_i,
    q′_u > i + (λ − 1)(i − 1/√2)  — which is > i when i ≥ 1, and for i = 0 is > −(λ−1)/√2;
    but q′ ∈ int Q₁′ ⊆ (0, s0)² gives q′_u > 0 = i in that case.

The same for v.  So int Q₁′ meets B_p⁺, likewise Q₂′, and Q₁′ ≠ Q₂′ are non-pin squares of F.  ∎

*Remark (the pad is the whole window's).*  π_i is computed at λ_max.  A tree that only claims a
slab (A57's G1: (3.861637, s0], λ − 1 ≤ 0.0040) could use π_i(λ) = (λ − 1)(i + 1 + 1/√2), i.e.
0.0068 / 0.0108 / 0.0148, and A60's c0 tree (m = s0, λ = 1) needs no pad at all; the full-window
pad is a SUPERSET hypothesis and therefore sound on every page, which is what A178 uses.  At the
corner the pad is exactly Lemma K0-WIDEN's w (the same computation with i = 0).

## 3. [T] Corollary FC-corner — proof

At a corner cell i = j = 0 the widened box is (0, 1 + π_0)² in c's frame and every square of F is
inside the container, i.e. in c's quadrant.  The two meeters Q₁′, Q₂′ are interior-disjoint unit
squares in the quadrant both meeting the open box (0, c_box)², c_box = 1 + π_0 = 1.025509 <
1/2 + 1/√2 = 1.2071.  Lemma A2 (`sideband.md` §2, Lean `distinct_cells`) puts their centres in
two different cells of the grid {u < c_box, u ≥ c_box} × {v < c_box, v ≥ c_box}.  Theorem B
(`sideband.md` §3, the (⇒) direction) says a pose of Q₁′ admitting no second meeter of the box in
the quadrant is impossible — Q₂′ is one — so every pose of either meeter satisfies one of the
clauses (NE), (W), (S), (P); poses certified LONELY may be removed (A173's `lonely_clip`, row R3
of `sideband.md` §6, soundness grade [S] for the three support clauses as recorded there, (P)
exact).  ∎

*What "the crowd" is here.*  Nothing about the meeters' depth is claimed (SLOT-SLIDE's d₂ ≥
ŝ′ − m is vacuous at ŝ′ = s0 for pages at s0); only "meets the open widened box".

## 4. [T] Corollaries FC-slot and FC-count — proofs

*FC-slot.*  Lemma A1 (`sideband.md` §2, Lean `linf_sep`) needs only interior-disjointness.  For
the non-applicability of Theorem B see §5(f).  ∎

*FC-count.*  The non-pin squares of F are H (one or two on these pages) and the free squares.
Two distinct non-pin meeters exist; at most one of them is a given H; so at least one meeter is
free, and if no H can meet B_p⁺ both are free.  H "provably misses" = A161's exact separating-
axis test (`chordlane.box_misses_cell_exact`, `multibox.Node.misses_cell`) on H's box against
the closed widened box: every pose of the box gives a square whose interior misses the cell.
Distinctness across cells: if one square met B_p⁺ and B_q⁺ it would have two interior points at
distance > dist(B_p⁺, B_q⁺) ≥ √2 (open boxes, so the infimum is not attained), impossible for a
unit square (its closed diameter is √2, attained only at opposite vertices).  ∎

## 5. The hypotheses, settled one by one

(a) **Window vs s0, and the endpoint.**  Theorem FC is stated for m ∈ [3.82, s0] CLOSED at s0
because the scoreboard rows are parametric 4-D certificates over the closed s-window [191/50,
969271/250000] (the s-cells are closed intervals; A146's rule: endpoints checked against the
verifier's integer grid) [S: `attempts/A56-sparametric/results/scoreboard.json` `window`, the
`.report.json` per class].  A60's c0 pages (pins exact, δ_pin = 3·10⁻⁸) are statements at
m = s0 itself and use the endpoint; A57's G1 pages are about the slab (3.861637, s0] and use the
interior.  If a reader wants to avoid the endpoint, the c0 pages' requirement holds for every
m ∈ [3.82, s0) with the same pad, and the endpoint alone is a measure-zero set of sides that
A60's own tube (protected_trees.md §2, T_REACH = 0.0457) covers anyway.

(b) **The pad.**  π_i = (λ_max − 1)(i + 1 + 1/√2) on the two FREE sides of the cell (away from
its backed sides), none on the backed sides (§2, Step 2).  At a corner π_0 = w = 0.025509 =
Lemma K0-WIDEN's pad — the same lemma, and the lonely clip's constant C_WIDEN in multibox.  The
pad only ever widens the box, so it is sound for every page whatever the tree's own reach.

(c) **What "simple" means in the class frame.**  Nothing on the page.  The teleport of Lemma
SLOT-CROWD is performed in P (at side m, where the slot square B_p(m) is an axis-aligned unit
square at an exact slot of [0, m]²), never in F; the page only inherits its CONCLUSION (n_p ≥ 2),
transported by dilation.  "Simple" (= axis-aligned at a census slot, A53) is therefore never
tested on F, and the page's pins are what they are in the record: dilated pins within δ_pin of
the s0 slots, with their certified cores.

(d) **Do the census pins already witness the meeters?**  No — pins never meet a forced cell
(that is what UNCLIPPED means, and the clip census is s-stable on the window, `stuck_rows.md`
§1, re-verified in `classes178.clipped_by_pin`).  A pin ADJACENT to the cell backs it (Lemma
CONT) and is an obstacle, not a meeter.  The conditioned square H may be a meeter (A141's M = 1
on the page: BR(0,1), TR(0,1), TR(1,0) for c0_Y1033), which is why FC-count guarantees one free
meeter, not two, unless H provably misses.

(e) **k0_00.**  The corner requirement of the k0v4 pages is Lemma K0-FREE′ (`k0_route.md` §3):
every corner box of a non-Trump packing is met by ≥ 2 squares, on the widened box at s0 by
K0-WIDEN — but K0-FREE consumes k1_00's tree (K0-O1), which is OPEN.  So on a k0 page the four
corner pairs are the hypothesis K0-BLOCKED, exactly as A168/A173/A176 state it, and every kill
that uses them is CONDITIONAL on K0-O1 (tag it so).  For the pinned classes the extension kills
EXIST (the scoreboard), so Theorem FC is unconditional — `slot_crowds.md` §2 Rem. (ii).

(f) **Why there is no lonely clip at a slot [F for the naive extension].**  Theorem B's (⇒)
direction uses that the SECOND meeter lies in the quadrant of the box's frame (x₂, y₂ ≥ g in
the (W)/(S)/(P) cases).  In the slot frame of BR(0,1) (u = distance from the right wall,
v′ = v − 1, the pin BR(0,0) occupying {u < 1, v′ < 0}) the square of tilt 45° centred at
(1.35, 0.45) is interior-disjoint from the pin (SAT gap 0.0657), inside the container, meets the
open slot box (its left vertex is (0.643, 0.45)), and has its lowest vertex at v′ = −0.257 < 0:
a legitimate meeter outside the quadrant [M, verified].  So a first meeter that is "lonely" by
the quadrant criterion can still have a partner beside the pin; the slot requirement is consumed
only through partner existence with the actual obstacles (pins, H, the container) — A174's
coexistence cut, or A178's node normalisation with the partner as a role.

(g) **The caveat the brief asked about — a corner met by a simple square of ANOTHER crowd.**
None is needed.  If the single meeter Q of the cell happens to be axis-aligned at some other
slot q of P (a latent simple square, not a pin of S), the teleport replaces Q by B_p(m) and P′
still CONTAINS the pins of T = S ∪ {p}; the monotone hypothesis `ContainsPins P_T` is all the
extension kill excludes (K1: kills climb containment, `k0_route.md` §3 remark), so losing Q's
own simpleness at q is irrelevant.  If Q is a pin of S the cell would be clipped — excluded by
hypothesis.  And two forced cells whose boxes are within √2 of each other MAY share a meeter
(e.g. an upright square near (2.44, 2.44) meets four of k5_11's boxes at once, `slot_crowds.md`
§4): that is the distinctness caveat of FC-count, handled by the √2 rule, never by assumption.

(h) **The M = 1 case at a corner.**  If H may meet the forced corner, only ONE free meeter is
guaranteed and it is carried as one role with the lonely clip; the coexistence cut with H as
the possible partner (A174's mixed sub-node) is the sharper consumption and is not part of A178's
first pass.

## 6. [M] The forced cells of the three page classes (computed by `classes178.py` against the
scoreboard of 2026-09-09; `python classes178.py` reprints it)

| class | pins | forced cells (extension, FULL) | forced CORNER |
|---|---|---|---|
| k5_11 | BL(0,0) BL(0,1) BL(1,0) TL(0,0) BR(0,0) | BL(1,1) k6_18; BR(0,1) k6_20; TR(0,0) k6_23; TL(1,0) k6_20 | **TR(0,0)** |
| k5_16 | BL(0,0) BL(0,1) TL(0,0) BR(0,0) TR(0,0) | BL(1,0) k6_23; BR(0,1) k6_29; BR(1,0) k6_27; TR(0,1) k6_30; TR(1,0) k6_28; TL(1,0) k6_27 | none |
| trump5 | BL(0,0) BL(1,0) BL(0,1) BR(0,0) TR(0,0) | BL(0,2) k6_07; BL(1,1) k6_19; BR(0,1) k6_21; TR(0,1) k6_22; TR(1,0) k6_24; TL(0,0) k6_23 | **TL(0,0)** |
| k0_00 | — | BL(0,0) BR(0,0) TR(0,0) TL(0,0), conditional on K0-O1 | all four |

Trump canary [T, `slot_crowds.md` §7]: at ŝ Trump is a trump5 packing whose six cells above are
all doubly met by free squares (TL(0,0) by squares 6 and 4 at depths 0.168 / 0.155) — consistent
with Theorem FC, which says nothing about depth.

## 7. Consumption and Lean shape

A178 (`geo178.cascade`): base node {pins, H}; at each forced corner that H provably misses, the
six Lemma-A2 cases {pins, H, T₁ ∈ cell a, T₂ ∈ cell b} with the lonely clip on T₁, T₂; at every
other forced cell one free role in its meeter window (`classes178.meeter_window`: centres within
1/√2 of the widened box and inside [1/2, s0 − 1/2]²), grouped by the √2 rule and taken in rounds
with H's surviving hull carried between rounds; `EmptyBox` at any role = the pair leaf
(`shared_point_same_square`) for that case; DEAD iff every case dies.  Lean: Theorem FC is
`slot_crowd` (obligation in `slot_crowds.md` §8) composed with `dilation_bridge` and a
coordinate bound; FC-corner adds `distinct_cells` and Theorem B (stated, clause (P) proved,
`Sideband.lean`); FC-count is bookkeeping over `Fin 11`.
