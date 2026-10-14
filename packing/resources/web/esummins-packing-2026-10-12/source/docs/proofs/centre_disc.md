# CENTRE-DISC(11) — the centre set of a ring's pocket, the corner MOUTH that refutes the disc bound about the container centre, the corrected family-stuck ring structure (ring + POKER) and the poker-anchored obligation — A252, 2026-09-17

A251 reduced RING-POCKET(11) to a RADIUS: Lemma INRADIUS + Lemma THREE-DISC give *if every unit square of the
pocket has its centre within R < 1/√3 of the container centre O, the pocket holds ≤ 2 squares*, and Lemma MID-NOTCH
killed the wall notches.  A252 was to finish the radius bound — the corner wedge and the vertex sectors — over the
all-ADJ ring family on [3.82, 4).  This note (i) sets up the CENTRE SET C = pocket ⊖ D_{1/2} and Lemma
CONTACT-TRIPLES, (ii) gives the corner wedge its closed form, Lemma MOUTH, and shows that it REFUTES the bound: the
brief's premise ("the inscribed disc of the pocket has radius < 1/√3") is false at every ring (inradius 0.77 at ŝ),
and the centre form CENTRE-DISC(O) is false on the whole window by the FLAT LIMIT of one corner, (iii) records the
coordinator's correction of the family-stuck ring structure — RING + POKER — tests it on A249's ring, and states the
criteria that survive (any centre; two pieces; the POKER-ANCHORED residual), (iv) says exactly what remains.
Tags: [T] proved, [T-computed] certified / exactly verified, [S] routine given cited items, [M] measured, [F] false
as stated, [C] obligation.  Sources: `ring_pocket.md` (A251), `type_t_chase.md` (A249), `family250.md` (A250),
`corner_chase.md` (A248 TWO-POKERS), `pocket_waste.md`, `wedged_seal.md`, `ring_capacity.md` (Lemma TWO).  Code
`attempts/A252-centre-disc/code/` (`disc252`, `lemmas252`, `adv252`, `poker252`, `test252`, `summarise252`,
`pages252`, `run252.sh`); results `results/disc252.md` (+ `adv252.jsonl/json`, `poker252_*.json`, `poker252.jsonl`,
`lemmas252.json`); pages `docs/residue_map/campaigns/A252-centre-disc/{mouth_witness,centre_set,notch_disc}.svg`;
Lean `Statements/Open/CentreDisc.lean` (and the removal of the false axiom from `RingPocket.lean`).

## 0. Verdict

> **[F] CENTRE-DISC about the container centre** (the brief's target, A251 §3.5's "one inequality").  Lemma MOUTH
> (§2): the disc of radius ½ separated from a corner's wall meeter B by its edge V→R and from its floor meeter A by
> its inner edge R_A→T_A has a closed-form centre q_mouth(θ_B, δ_B, θ_A, δ_A); over the family's box its distance
> from O is maximised at the FLAT LIMIT θ_B, θ_A → 90°, δ_B, δ_A → 1 (both touchers tending to [0,1]×[1,2] and
> [1,2]×[0,1] of the corner frame), where q_mouth → (3/2, 3/2) and |q_mouth − O| → (s/2 − 3/2)√2, which exceeds
> 1/√3 = 0.57735 iff **s > 3 + 2/√6 = 3.81650** — the whole window.  The limit is approached INSIDE the family:
> the corner box stays doubly met by slivers, the pair interlocks through a channel of width → 0 (δ_A ≥ 1 − δ_B ε_A
> with ε = 90° − θ), the wall neighbours poke their tips into the strips the flat squares leave (Lemma GAP), and at
> most one corner can be flat (two flat corners, adjacent or opposite, are infeasible: §2.3).  [M] `adv252`: on
> FEASIBLE rings (margin +0.003) far_O = **0.628 at s = 3.99** and 0.566 at ŝ after 3 000 Nelder–Mead steps (the
> limit there is 0.620); the far disc touches B and A of one corner at exactly ½ in every case — the mouth.
> The brief's literal premise is also false: the pocket's INSCRIBED disc has radius 0.771 at ŝ (it is the central
> disc; C is small because the centre must stay ½ from the eight squares).
>
> **[F] every INRADIUS-only criterion in the flat-flat limit** (§3, page `notch_disc.svg`): with B flat-ish (θ_B =
> 12°, δ_B = 0.95) and A near flat (θ_A = 89°, δ_A = 0.9916) the corner NOTCH — a trapezoid of width < 1 (δ_A < 1)
> and height 0.91 .. 1.11 — holds the disc of radius ½ at (½, ½) but NO unit square.  So the centre set C acquires
> a component ~2 from O, and far_O, the smallest enclosing circle, the halves and the three-point dispersion all
> fail there while the capacity does not change: **the proof of the pocket bound must use SQUARE room in the
> notches and mouths, or the box-valid pierce on the protected family; a disc radius alone cannot do it.**
>
> **[T] the corrected family-stuck ring structure is RING + POKER** (coordinator / PI, 2026-09-18 00:30; §4): the
> sixteen eight-cell families {four corner boxes + one slot per wall} are admissible below 4 and are met by the eight
> ring squares only, so Lemma CELLS teleports the bare ring; the only protection is a free square meeting both slots
> of one wall — by convexity, its corner in the OVERLAP [0,1]×[s−2, 2] of that wall's slots — the POKER.
> [T-computed] at A249's exact ring at ŝ: poker margin **+0.00166** (A249: +0.0017) on every wall (the C2 pinwheel),
> pose (2.107, 1.574, 14.5°) on y = 0; with the poker in place the residual centre set is **EMPTY**: no second free
> square fits beside it — capacity 1, 8 + 1 = 9 < 11 at ŝ.  The capacity question is now *poker + two more?*, and
> the criteria that survive (any n) are Lemma TWO-PIECES and the **POKER-ANCHORED** form: if the admissible centres
> beside the pinned poker form a set of diameter < 1, capacity ≤ 2 (Lean theorems `capacity_le_two_of_two_pieces`,
> `capacity_le_two_of_anchor`; the chain `ring_pocket_of_poker_residual`).
>
> **[C] what remains: RING-POKER-RESIDUAL(11)** — the residual centre set beside the poker has diameter < 1 for
> every all-ADJ ring of the window and every admissible poker position — measured by the detached PROTECTED ladder
> (ring + poker jointly, §5), NOT proved.  FAMILY-STUCK-EXIST(11) is **not closed**; k0_00 unchanged.

## 1. The centre set and Lemma CONTACT-TRIPLES (task 1)

**1.1 [T] The centre set.**  For a ring x at side s with pocket P = [0, s]² ∖ ⋃ int Q_i, let
C := {q : D(q, ½) ⊆ P} = P ⊖ D_{½}.  By INRADIUS every unit square of the pocket has its centre in C, so any
criterion "C holds no three points pairwise ≥ 1 apart" bounds the capacity by 2, and "diam C < 1" by 1.  Sufficient
forms, each a theorem for every n: (a) C ⊆ D(c, R) for SOME c with R < 1/√3 (THREE-DISC; A251 used c = O);
(b) C = X₁ ∪ X₂ with diam X_i < 1 (pigeonhole; Lean `capacity_le_two_of_two_pieces`); (c) disp₃(C) := max over
triples of the least pairwise distance < 1.  `disc252.metrics` computes far_O, the smallest enclosing circle, the
diameters of the four halves, disp₃, diam, the pocket's inradius and the CONTACTS of the far point.  [M] at ŝ:
far_O 0.417, sec 0.416, diam 0.833, halves 0.691, disp₃ 0.619, inradius 0.771, pocket area 7.032 (A249: 7.032).

**1.2 [T] Lemma CONTACT-TRIPLES (any n).**  The disc D(q, ½) is disjoint from a square iff, in the square's frame
(a, b) (unit coordinates along its edges from a vertex), max(0, −a, a−1)² + max(0, −b, b−1)² ≥ ¼: separated by an
EDGE LINE with margin ½ (one coordinate outside by ≥ ½, the other inside) or by a VERTEX (both outside, Euclidean
distance ≥ ½, q in the vertex's outer normal cone).  C is compact; ∂C is a finite union of straight pieces (edge and
wall contacts) and circular arcs of radius ½ about vertices.  A maximiser of a linear functional or of |q − O| over
C lies on ∂C, hence at a point where TWO constraints are active — edge–edge, edge–vertex, vertex–vertex, wall–edge,
wall–vertex, wall–wall — or at ONE vertex contact with q = P + ½u, u the maximised direction; for |q − O| that needs
u = (P − O)/|P − O| in P's outer cone, impossible at an INNER vertex (its cone points towards O), so a one-contact far
point touches an OUTER vertex, a notch case.  The list is complete because ∂C has no other pieces.  The walls ARE
boundary: a disc within ½ of a wall leaves the container.  ∎  [M] census at the far points of the adversarial
rings: every one is an edge–edge contact (B and A of one corner); `lemmas252.contact_census`.

## 2. Lemma MOUTH — the corner wedge in closed form, and the flat limit (task 2)

**2.1 [T] Lemma MOUTH.**  Corner frame (A249): B with V = (sin θ_B, δ_B), edge V→R of outward normal
n₁ = (sin θ_B, −cos θ_B); A with T_A = (δ_A + cos θ_A, w(θ_A)), inner edge R_A→T_A of outward normal
n₂ = (cos θ_A, sin θ_A).  The disc separated from B by V→R and from A by R_A→T_A has centre on
(q − V)·n₁ = ½, (q − T_A)·n₂ = ½; the lines meet at the wedge angle α = 90° + θ_A − θ_B ∈ (0°, 180°), the disc sits
at distance 1/(2 sin(α/2)) from the apex on the bisector, and q_mouth is the solution of the 2×2 system
(`lemmas252.mouth_centre`; [T-computed] exact on 300 draws).  With its feet on the two SEGMENTS it is the
edge–edge case of §1.2.  *Flat limit.*  As θ_B, θ_A → 90° and δ_B, δ_A → 1, n₁ → (1, 0), V → (1, 1), n₂ → (0, 1),
T_A → (1, 1), so q_mouth → (3/2, 3/2) and |q_mouth − O| → (s/2 − 3/2)√2 = 0.5798 at 3.82, 0.6202 at ŝ, 0.7000 at
3.99; it exceeds 1/√3 iff s > 3 + 2/√6 = 3.81650.  ∎  A251's one-sided bound `corner_wedge_bound` was written for
the OTHER pair of edges (B's V→R and A's left edge W→T_A, the channel between the two squares): that channel has
width 1 − δ_A sin θ − δ_B cos θ ≤ 0.594 in the parallel case and never holds a disc of radius ½; the disc of the
corner sits at the channel's MOUTH, between B's right edge and A's top edge.

**2.2 [F] Lemma CENTRE-DISC about O.**  The flat limit is approached inside the family.  Corner pair: B ≈
[0,1]×[δ_B, δ_B+1] and A ≈ [δ_A, δ_A+1]×[0,1] with tilts ε_B, ε_A > 0 are disjoint iff the channel between B's edge
V→R and A's edge W→T_A has positive width, i.e. δ_A ≥ 1 − δ_B ε_A + O(ε²) and ε_A > (1 − δ_B) ε_B: with δ_B < 1
fixed and ε → 0, δ_A → 1⁻, and both squares still meet the corner box (δ < 1).  Wall pairs: the flat B_c ≈
[0,1]×[1−η, 2−η] (frame) leaves the strip of height η at its top for the adjacent corner's wall meeter, which must
reach past s − 2 (all-ADJ): its tip T′ = (cos θ′, s − δ′ − w′) enters the strip for any θ′ (T-SLOTS' STACK pair);
mirror for A_c's neighbour on the floor.  So the family contains rings with one near-flat corner, and their far
point is the mouth.  [M] `adv252` (Nelder–Mead on far_O − 30·max(0, 0.003 − margin), 16 parameters): far_O =
0.628 at s = 3.99 (margin +0.0030, far point (2.476, 2.399), contacts B_TR, A_TR at ½), 0.566 at ŝ (margin
+0.0030, TR corner at (84.8°, 0.794, 88.1°, 0.987)); the exact witness rows are in `results/adv252.jsonl`.  Page
`mouth_witness.svg`.

**2.3 [T] at most one flat corner.**  Two flat ADJACENT corners put two flat floor touchers on one wall with
overlapping extents [1−η, 2−η] and [s−2+η, s−1+η] (Lemma GAP with s < 4) — impossible for two unit squares
touching the same line.  Two flat OPPOSITE corners (BL, TR) force BOTH squares of TL (and of BR) to their reach
bounds δ = s − 2 − w + O(η); a corner pair with both meeters at the reach bound overlaps (at 45°/45° the edge V→R
of B is a chord of A; at 90°/90° the flats [0,1]×[0.877,1.877] and [0.877,1.877]×[0,1] overlap; the mixed cases put
A's top vertex T_A = (s − 2 − sin θ_A, w_A) inside B).  So the smallest enclosing circle stays near O: [M] sec_r =
0.478 at the far ring of ŝ (centre (2.01, 1.99)), 0.416 at A249's ring, ≤ 0.49 on the C2 rings up to 3.999 — the
criterion (a) with a FREE centre is not refuted by the mouth.  It is refuted by the notch (§3).

## 3. The notch: NOTCH-SEP, TWO-VERTEX, and why disc criteria are lossy (task 3)

**3.1 [T] Lemma NOTCH-SEP.**  A disc of radius ½ in the corner notch separated from B by the line of L→V and from A
by the line of V_A→W, in {u, v ≥ ½}, needs θ_B > 45° with δ_B ≥ φ(θ_B) := ½ − cos θ_B + (1 + cos θ_B)/(2 sin θ_B)
and θ_A < 45° with δ_A ≥ φ(90° − θ_A); min φ = 0.862 at 63.7°.  *Proof.*  (q − L)·(cos θ, sin θ) ≤ −½ with u ≥ ½
gives v ≤ δ_B + cos θ − (1 + cos θ)/(2 sin θ), and v ≥ ½; φ(θ) < 1 iff sin θ + 2 sin θ cos θ > 1 + cos θ iff
θ > 45°.  ∎  [M] 0 violations on 2 000 random corner pairs (`test252.test_notch_sep`).
**3.2 [T] Lemma TWO-VERTEX (the vertex–vertex sector).**  A disc of radius ½ touching two vertices P₁, P₂ at distance
d ≤ 1 has its centre on their bisector at height √(¼ − d²/4) above the midpoint M, so |q − O| ≤ |M − O| + √(¼ − d²/4).
With Lemma GAP the wall vertices T, T′ of one wall's touchers are within 4 − s ≤ 0.18 vertically, so the vertex
sector of a wall's middle notch has |q − O| ≤ |M − O| + 0.498 — a bound, consistent with MID-NOTCH.
**3.3 [F] the other notch case.**  A disc BELOW B's edge V→R and LEFT of A's edge W→T_A (B flat-ish, A near flat):
θ_B = 12°, δ_B = 0.95 (meets c00, reaches: δ + w = 2.14), θ_A = 89°, δ_A = 0.9916: the disc at (½, ½) is 0.510 from B,
0.500 from A, ½ from both walls; the notch component (left of A, below B) has bounding box 0.99 × 1.16 and NO unit
square fits in it (width < 1 since δ_A < 1; Lemma TWO-type room).  Page `notch_disc.svg`.  So C has a far component
while the capacity is unchanged — every criterion of §1.1 (a)–(c) is lossy here, and a proof of the pocket bound
needs square room, not disc room, in the notches.  The parallel-channel disc of A251 §3.5 does not exist
(width ≤ 0.594); the wedge disc exists and is the mouth (§2).

## 4. The corrected structure: RING + POKER (the coordinator's addendum; task 4 and the cross-checks)

**4.1 [T] Why the bare ring is teleportable** (coordinator, verified on A251's ring at 3.85).  Below 4 the sixteen
families Π = {four corner boxes, one slot per wall} are pairwise interior-disjoint (the two slots of a wall overlap,
so only one is taken), |Π| = 8, and each is met by the eight ring squares only: |M(Π)| = 8 = |Π| and Lemma CELLS
(`cells_swap`) exchanges the ring into four corner dominoes.  A free square protects a family only by meeting a cell
of it, and the only cell a free square can add a meeter to without being a corner meeter is a wall slot; to protect
ALL sixteen families it must meet BOTH slots of some wall (each family takes one of the two), hence, by convexity,
their overlap [0,1]×[s−2, 2] (or a D4 image): the POKER, corner in the overlap, body in the centre.  So the
family-stuck ring structure is ring + poker (+ two more free squares for n = 11), and A249's "+0.0017 poking square"
is exactly the poker.  (The free square A251's fit at (2.00, 2.05) meets no border cell and protects nothing.)
**4.2 [T-computed] on A249's exact ring at ŝ** (`poker252 --mode shat`): the poker fits with margin +0.001662 on
each of the four walls (C2 + the D4 relabelling of the pinwheel), e.g. pose (2.1065, 1.5744, 14.54°) with its corner
in [s−2, 2]×[0, 1]; with the poker in place the residual centre set C′ = (pocket ∖ poker) ⊖ D_{½} is EMPTY (area 0):
no further unit square fits — capacity exactly 1 at ŝ (A249's direct search: 2 fail at −0.142), 8 + 1 = 9 < 11.
**4.3 [T] the criteria that survive.**  Lemma TWO-PIECES (§1.1 (b)) and **Lemma POKER-ANCHORED** (any n): if every
unit square of the pocket disjoint from the poker P₀ has its centre in a set X of diameter < 1, the pocket holds ≤ 2
squares (P₀ and one more) — Lean `capacity_le_two_of_anchor`; and the chain `ring_pocket_of_poker_residual`:
RING-POKER-RESIDUAL + `ring_has_poker` [T-prose, 4.1] + `pocket_count_three` [T-prose: two meeters per corner, so
three pocket squares] ⟹ RING-POCKET(11).  The poker's pinned pose (corner in a 1 × (4 − s) cell) is a constraint:
[M] the far rings of §2.2 admit the poker only on the walls away from the flat corner, and the PROTECTED adversary
(ring + poker jointly feasible, 19 parameters) is the honest search — its rows land in `results/poker252.jsonl`.

## 5. The non-ring structures, the obligation, n-generality (tasks 5–6)

* **Non-ring family-stuck structures** (A249 §3.4, A250): (i) mixed rings with 1–3 type-F corners: a type-F corner's
  poker slot needs a free square through its notch (A248 on the window), so ≥ 1 free square per type-F corner and
  a second when its floor slot is not ADJ-supplied; the pocket is bounded by the same eight touchers plus those
  free squares, and the POKER-ANCHORED argument applies verbatim with the corner pokers as further anchors (each
  pinned to a notch) — the residual room shrinks, the obligation is the same shape; four type-F corners are dead
  (TWO-POKERS, s* = 3.934 > ŝ, on [3.82, ŝ] only).  (ii) structures whose corner meeters do not all touch their
  walls: the family box of A251 §1 does not contain them; their pocket is bounded by eight squares in the same
  cyclic order (PROJECTION) with the touching constraint relaxed — CONTACT-TRIPLES and the criteria of §1.1 apply,
  the flat-limit refutation applies a fortiori (a non-touching meeter only enlarges the mouth), and no bound is
  proved.  Neither escapes the argument's SHAPE; both are open.
* **Plainly: FAMILY-STUCK-EXIST(11) is NOT closed on [3.82, 4).**  What A252 proves: CONTACT-TRIPLES, MOUTH (and its
  flat limit), NOTCH-SEP, TWO-VERTEX, TWO-PIECES, POKER-ANCHORED, the chain — all n-free.  What it refutes: the disc
  bound about O (the brief's target) and, in the flat-flat corner limit, every disc-only criterion.  The exact
  remaining obligation: **RING-POKER-RESIDUAL(11)** — for every all-ADJ ring of the window and every admissible
  poker, the residual centre set has diameter < 1 — with the flat-corner rings needing SQUARE room in the notch
  (a Lemma TWO-type bound: the notch's bounding box is narrower than 1 because δ < 1) rather than disc room.  With
  that, k0_00 closes via `FamilyStuck.lean`'s chain (A250 at s ≥ 4, A248's TWO-POKERS for type-F rings on [3.82, ŝ],
  `ring_pocket_of_poker_residual` for the ring family, `family_stuck_non_ring` for the rest) — not before.
* n = 11 corollary: the ring's 8 + the poker + ≤ 1 = 10 < 11 wherever the residual bound holds (at ŝ: 9).
  n-general: every lemma above is about one corner, one wall pair or one region; the count 8 + capacity applies for
  every n with capacity from the anchored residual.
* Lean `Statements/Open/CentreDisc.lean` (build + `lean/audit.py`, 0 sorry): theorems `capacity_le_two_of_two_pieces`,
  `capacity_le_two_of_anchor`, `ring_pocket_of_poker_residual`; axioms `ring_has_poker`, `pocket_count_three`
  [T-prose], `ring_poker_residual` [C]; `RingPocket.lean`: the false axiom `centre_disc_ring` REMOVED (its
  consumer chain was never built on it; `ring_pocket_eleven` [C] unchanged).  Obligations: O-RING-POKER-RESIDUAL,
  O-NOTCH-ROOM (the square-room lemma for flat-limit notches), O-CONTACT (CONTACT-TRIPLES in Lean over `sqSet`).
* Reproduce: `bash attempts/A252-centre-disc/code/run252.sh test|lemmas|adv|poker|protected|summary|pages|ladder`
  (test 2 min; lemmas 1 min; adv ≈ 30 s per start, 12 starts × 6 sides per metric; poker shat 1 min; protected
  ≈ 1 min per start; `logs/STOP`, rows in `results/*.jsonl`, reruns skip what is done).
