# STRIP₂ BY ENCLOSURE — the corner-box entry is closed by one inequality (Lemma WEDGE-FLOAT: no free square of the strip has its centre at or below height 1 — A and WEDGED-SEAL are not needed), the C–X "gap" is a WEDGE that a poke cannot cross, and STRIP₂-IN-RING is [T] on an explicit ring domain (43/43 JAM rings inside it with positive margin) — A267, 2026-09-23

The brief (A267 BRIEF + two addenda): the PI's enclosure route for STRIP₂ — keep A and X, S is walled in, the
entries are (i) the C–X gap, (ii) the A–C gap, (iii) the corner box below; addendum 1: use WEDGED-SEAL for (iii);
addendum 2: the PI's "Lemma WEDGE for a floating C".  Tags [T] proved, [T-prose] proved in prose with the
arithmetic cores in Lean, [T-computed] finite computation with its own check, [M] measured, [C] conjecture, [F]
false.  Code `attempts/A267-strip-enclosure/code/` (`measure267` the ring measurements, `upper267` the C-frame
wedge and the exact bad-centre area, `approach267` the closest free approach to S, `hyp267` the domain
hypotheses with margins, `pages267`); results beside it; page
`docs/residue_map/campaigns/A267-strip-enclosure/enclosure.svg`; Lean `Statements/Open/StripEnclosure.lean`.
Notation as A266: corner frame BL, wall x = 0, floor y = 0, c = cos θ, s = sin θ (C's tilt, θ ∈ [0°, 45°]), C the
floater with lowest vertex B = (u, h_v), u := h_u + s, left vertex L = (h_u, L_h), L_h := h_v + c, top vertex
T = (h_u + c, C_top), C_top := h_v + c + s; ℓ_C(y) = C's left boundary at height y (= u − (y − h_v) tan θ on
the lower-left edge, y ≤ L_h; = h_u + (y − L_h) cot θ on the upper-left edge, y ≥ L_h); g := ℓ_C(1);
T_u = C − h_u e_x, S := T_u ∖ C; X the wall toucher (leftmost vertex (0, y_X), tilt φ ∈ [0°, 45°], bottom
vertex B_X = (s_X, X_low), right vertex R_X), int X ∩ int T_u ≠ ∅, int X ∩ int C = ∅.  Q: a unit square of the
quadrant, tilt ψ ∈ [0°, 90°) (c_ψ, s_ψ), int Q ∩ int C = ∅ = int Q ∩ int X, with a point p ∈ int Q ∩ S.

## 0. Verdict

> **[T] Lemma WEDGE-FLOAT (case (iii), any n, s-free).**  If C meets the open box with h_v < 1 < h_v + cos θ
> (equivalently g < 1 and L above height 1), then every unit square Q of the quadrant interior-disjoint from C
> with an interior point in S has its centre STRICTLY ABOVE HEIGHT 1 — and hence (§2) above L_h.  Proof (§1):
> Q's part above height 1 lies in the slot [0, ℓ_C(y)) of width ≤ g < 1, so by POKE it is one vertex, the top
> vertex T = (t_x, t_y); the wall gives t_x ≥ c_ψ, the floor t_y ≥ c_ψ + s_ψ, the slot at height 1 gives
> t_x + (t_y − 1) tan ψ ≤ g; then c_ψ t_x + (t_y − 1) s_ψ ≥ 1 + c_ψ s_ψ − s_ψ ≥ c_ψ > g c_ψ (Lean
> `wedge_float_core`).  This is the PI's "Lemma WEDGE for a floating C" (addendum 2) with the box condition as
> the only hypothesis; **A is not used, WEDGED-SEAL is not used** (a Q touching both walls is a special case, and
> so is a wall-only toucher and a floater: the inequality does not see which walls Q touches).  So case (iii) does
> not reach the corner-type table.
> **[T-prose, on the ring domain] STRIP₂-IN-RING.**  On the domain (D1)–(D2), (U1)–(U9) of §3 — s-free, m-free,
> corner-local, every hypothesis an explicit inequality in (h_u, h_v, θ; y_X, φ) — no unit square of the quadrant
> interior-disjoint from C and X has an interior point in S.  Route: WEDGE-FLOAT puts Q's centre above L_h (§2,
> and X's too: X is such a square); Q's centre chord is never left of X (room < 1) and, by the room bounds (U4),
> Q's centre is above C's top; in C's own frame (a along the upper-left edge, b outward) the free part of S is the
> WEDGE between X's lower-right edge (the roof, b_X(a)) and C's upper-left edge (the floor, b = 0), Q's chords
> across the wedge are trapped in it (FRAME + NO-STRADDLE + FAR-SIDE, §3.2), and a unit square whose chords on
> (a*, a₂) are ≤ w_max while it reaches past a₂ and starts before a* forces a₂ − a* ≤ w_max s_ψ c_ψ ≤ w_max/2
> (Lean `wedge_extent_core`) — the POKE bound; on the rings a₂ − a* ≥ 0.30 while w_max/2 ≤ 0.11 (U3 margin
> ≥ 0.19).  All 43 JAM rings (A262, t > 0) lie in the domain with positive margin (`hyp267`; the thinnest margins
> are the ring's own sliver and gap: D1 ≥ 0.0009, D2/U2 ≥ 0.0016, U5 ≥ 0.041, the rest ≥ 0.19).
> **[T-computed] the mechanism, exactly (§4).**  With {C, X} alone the closest free square to S on every ring is
> UNDER C, touching C and the floor, at distance 0.054–0.170 from T_u ⊕ Q — the case-(iii) entry, and it OVERLAPS
> A (the ring fills that place with A; the lemma does not need A).  With centres above L_h the closest approach is
> 0.24–0.37 away, above C's top and right of X, touching X and C — the C–X wedge entry.  The exact bad-centre
> area is 0 on all 43 rings at every tilt (`upper267`).
> **What the brief had wrong (§6):** the measurements (h_u 0.25–0.72, h_v ≥ 0.929, θ up to 25.8°, C's box area up
> to 0.010, A's x_min 0.63–0.86), the C–X "gap of width < 0.05" is a wedge of angle φ − θ ∈ [−1.7°, 14°] whose
> roof X's lower-right edge lies ON C's upper-left line (b_B ∈ [−0.09, 0.03]), so "POKE depth ≤ g/2" is the wrong
> slot; case (iii) needs neither WEDGED-SEAL nor the corner-type table; A does not close the strip and is not
> needed to close it.
> **Consequence (§5):** 5b of k0_route.md §13 on the ring domain is [T-prose] + `pair3` (A262 chain3, not landed);
> NO-JAM(11) still lacks 5a/5b `pair3`, 5d, `jam_count`, and STRIP₂ off the ring domain (the general UPPER case,
> §3.5).  k0_00 unchanged.

## 1. Lemma WEDGE-FLOAT (case (iii))  [T]

**Domain.**  C meets the open box (0,1)² and its left vertex is at height L_h = h_v + c > 1: then h_v < 1 and
the lower-left edge covers the heights [h_v, 1], so C meets the box iff g = ℓ_C(1) = u − (1 − h_v) tan θ < 1
(A266's h_u c + h_v s < c + s − sc, multiplied out).  On the rings h_v ≥ 0.929, L_h ≥ 1.89, g ≤ 0.883.
**LEFT [T].**  A horizontal chord of int Q at a height y ∈ (h_v, C_top) that reaches x ≥ ℓ_C(y) contains a point
of C's boundary and hence points of int C; so every such chord is entirely left of C or entirely right of it, and
by convexity (a chord left and a chord right sandwich C) all of them are on the side of p: **Q ∩ {h_v < y <
C_top} ⊂ {x < ℓ_C(y)}** (A265 §1.3 (i), unchanged).
**Statement.**  *Every unit square Q of the quadrant, interior-disjoint from C, with a point p ∈ int Q ∩ S, has
its centre strictly above height 1.*
**Proof.**  Suppose q_y ≤ 1.  (a) Q has points above height 1: otherwise Q ⊂ {y ≤ 1} is the flat square
[a, a+1] × [0, 1], whose chords at heights in (h_v, 1) have length 1 and lie in [0, ℓ_C(y)) ⊂ [0, g + ε) — false.
(b) Q's part above height 1 lies in the slot {0 ≤ x < ℓ_C(y)} ⊂ {x < g} (heights (1, C_top) ⊂ (h_v, C_top), LEFT;
ℓ_C decreases up to L_h and Q's part above L_h, if any, has chords below the chord at L_h < h_u < 1 since q_y ≤ 1
and chords do not grow above the centre).  POKE (peel.md §2.3): two adjacent vertices above 1 give a chord of
length ≥ 1 at height 1 (closure of the slot: ≤ g < 1), three give a vertical extent ≥ 1 above 1 (but Q's top is
≤ q_y + 1/√2 ≤ 1.71 — its part above 1 is < 1 tall): **exactly one vertex, the top vertex T = (t_x, t_y)**, is
above 1, and Q's chord at height 1 is [t_x − (t_y − 1) cot ψ, t_x + (t_y − 1) tan ψ] (ψ ∈ (0°, 90°); ψ = 0 is (a)).
(c) The wall: Q's left vertex T + (−c_ψ, −s_ψ) has x ≥ 0, so t_x ≥ c_ψ.  The floor: the bottom vertex
T + (s_ψ − c_ψ, −s_ψ − c_ψ) has y ≥ 0, so t_y ≥ c_ψ + s_ψ.  The slot: the right end of the chord at height 1 is
≤ g (it is the limit of chords at heights 1 + ε, all in [0, g)).  (d) Multiply the slot inequality by c_ψ:
c_ψ t_x + (t_y − 1) s_ψ ≤ g c_ψ < c_ψ; but c_ψ t_x ≥ c_ψ² and (t_y − 1) s_ψ ≥ (c_ψ + s_ψ − 1) s_ψ, so the left side is
≥ c_ψ² + s_ψ² + c_ψ s_ψ − s_ψ = 1 + c_ψ s_ψ − s_ψ ≥ c_ψ ⟺ (1 − c_ψ)(1 − s_ψ) ≥ 0.  Contradiction.  ∎  (Lean
`wedge_float_core`: the arithmetic of (d) from the three inequalities of (c).)
**Remarks.**  (i) Only the wall, the floor and C's lower-left edge are used: A, X, WEDGED-SEAL, PUSH play no
part; the PI's split (Q touching both walls → WEDGED-SEAL; Q touching the wall only or floating → a third box
meeter, THIRD or FLOAT2) is subsumed — the inequality holds whichever walls Q touches (a wedged Q has equality in
both (c)-bounds and still fails by (1 − c_ψ)(1 − s_ψ) ≥ 0, with h_v < 1 making the slot strictly narrower than 1).
(ii) It is A259's Lemma WEDGE (normal_room.md §2.5: the START gap between the wall and Q₁'s edge line holds no
unit square when a < 1) with C's lower-left edge as the wedge's far side and the apex shifted: there the slot's
width at height 1 is a < 1, here it is g < 1.  (iii) On the general STRIP₂ domain of A266 the hypothesis
L_h > 1 can fail (θ = 45°, h_v < 0.29): then C's left vertex is inside the box and the slot at height 1 is bounded
by the upper-left edge — the lemma is stated for L_h > 1 only.  (iv) The A–C gap (entry (ii)) is inside this
case: a Q entering under C through the A–C gap has its centre below C's bottom < 1.  POKE there would give depth
≤ g_AC/2 ≤ 0.0053 (rings) — not needed.

## 2. Every square of the strip is UPPER; X is one  [T]

Let Q be as in §1 (X and C only).  By WEDGE-FLOAT q_y > 1.  The chord through the centre has length
1/max(c_ψ, s_ψ) ≥ 1 and, if q_y ∈ (1, L_h], lies in [0, ℓ_C(q_y)) ⊂ [0, g) — impossible.  So **q_y > L_h**: the
centre is above C's left vertex.  X is a unit square of the quadrant, interior-disjoint from C, with an interior
point in S (int X ∩ int T_u is open, non-empty and disjoint from int C), so X's centre is above L_h too ([M]
X's centre 2.49–2.62 vs L_h 1.89–1.99).  **NO-LEFT [T].**  The room left of X at any height is ≤ max(s_X, c_X)
< 1 (X's left boundary is within its bottom or top vertex's x of the wall), so Q's centre chord is never left of
X; at a height in X's range it is RIGHT of X: q_x − ½/max(c_ψ, s_ψ) ≥ r_X(q_y).

## 3. The UPPER case in C's frame  [T-prose on the ring domain]

**3.1 C's frame and the wedge.**  Coordinates (a, b) := (e·(P − L), n·(P − L)) with e = (c, s), n = (−s, c):
C = [0, 1] × [−1, 0] (a along the upper-left edge, b outward), T_u = C + (−h_u c, h_u s), S = T_u ∖ C = the top
strip {0 < b ≤ h_u s} ∪ the left strip {a < 0} of T_u; T_u's top edge is a = a* := 1 − h_u c.  X's lower-right
edge from B_X = (a_B, b_B) to R_X = (a_R, b_R) is the graph of the affine b_X(a), slope tan β, β := φ − θ; X lies
above it.  The **wedge** W := {a₁ ≤ a ≤ a₂, 0 ≤ b ≤ b_X(a)}, a₁ := max(a_B, 0), a₂ := min(a_R, 1),
w_max := max(b_X(a₁), b_X(a₂)).  [M] rings: a_B ∈ [−0.44, 0.15], b_B ∈ [−0.09, 0.03], a_R ∈ [0.53, 1.15],
b_R ∈ [0.001, 0.215], β ∈ [−1.7°, 14°], a* ∈ [0.29, 0.75]: X's edge lies ON C's upper-left line and covers the
top strip; the free part of S above L_h is the sliver under X's edge.
**Ring domain.**  (D1) h_v < 1 < L_h, g < 1.  (D2) X as in the notation, X's lowest point ≥ h_v.  (U1) a₁ < a*.
(U2) b_X ≥ 0 on [a₁, a₂].  (U3) a₂ − a* > w_max/2.  (U4) ρ(C_top) < 1, ρ(y₀) < 1 (ρ(y) := ℓ_C(y) − r_X(y), the
room right of X, y₀ := max(X_low, L_h)) and ℓ_C(X_low) < 1 if X_low > L_h.  (U5) a_R − sin β⁺ ≥ a*.  (U6)
h_u + c − cos φ < 1.  (U8) X's top > C_top + 1/√2.  (U9) T_u lies below X's far edge (σ < 1 on T_u, σ the
coordinate across X from its lower-right edge).  Margins on the 43 rings (`hyp267`): D1 ≥ 0.0009, D2 ≥ 0.0016,
U1 ≥ 0.29, U2 ≥ 0.0016, U3 ≥ 0.19, U4 ≥ 0.25, U5 ≥ 0.041, U6 ≥ 0.25, U8 ≥ 0.19, U9 ≥ 0.76.
**3.2 Q's centre is above C's top.**  q_y > L_h (§2).  If q_y ∈ (L_h, C_top]: either q_y < X_low, and the centre
chord (≥ 1) lies in [0, ℓ_C(q_y)) with ℓ_C(q_y) ≤ ℓ_C(X_low) < 1 (U4) — false; or q_y ∈ [X_low, C_top] and the chord
is right of X (NO-LEFT), of length ≤ ρ(q_y) ≤ max(ρ(y₀), ρ(C_top)) < 1 (ρ is convex there: ℓ_C affine, r_X concave)
— false.  So q_y > C_top; and q_y ≤ X's top (else Q's lowest point > X_top − 1/√2 > C_top by (U8) and Q misses
S ⊂ {y ≤ C_top}).  Hence q_y is in X's range, the centre chord is right of X, and its right end E = (x_E, q_y) has
x_E ≥ r_X(q_y) + 1 with r_X(q_y) ≥ min(r_X(C_top), cos φ) > h_u + c − 1 (r_X concave on [C_top, X_top]; (U4), (U6)),
so **a_E = c (x_E − h_u) + s (q_y − L_h) > c (r_X + 1 − h_u) + s² > 1 ≥ a₂** (Lean `e_point_core`): Q reaches
past the wedge's mouth.
**3.3 Q's chords across the wedge are trapped in it.**  *FRAME.*  No point of Q has a ∈ (0, 1) and b < 0: such a
point is in int C (b > −1) or is right of C at a height in (h_v, C_top) (b ∈ (−1 − as/c, −1): against LEFT) or is at
height ≤ h_v — but Q's lowest point is ≥ q_y − 1/√2 > L_h − 1/√2 ≥ h_v for θ < 45°.  *NO-STRADDLE.*  For
a ∈ (a₁, a₂) the chord of Q in the direction n at a is a segment avoiding int C (b ∈ (−1, 0)) and int X (X's chord at
a, non-degenerate for a > a_B): it lies in [0, b_X(a)] (in W) or beyond X's chord.  Two chords of different kinds
sandwich X (the segment between a point of the first and a point of the second crosses X's lower-right line into
X before it can leave through the far one — by the intermediate value theorem on b − b_X, b − top_X), so **all
chords on (a₁, a₂) are in W, or all are beyond X**.  *FAR-SIDE.*  "All beyond X" is impossible: take z ∈ Q with
a_z ∈ (a₁, a₂) beyond X and the segment [p, z) ⊂ int Q.  Write (τ, σ) for the coordinates along and across X's
lower-right edge (X = [0,1]²).  p ∉ X (p ∈ int Q).  If σ_p < 0 (p below the edge line): the segment crosses σ = 0
at a point P₁ before it crosses σ = 1, and [P₁, P₂] ∩ int X = ∅ forces τ ≥ 1 on [P₁, P₂] (τ ≤ 0 puts P₂ at or beyond
X's wall vertex: x ≤ 0, allowed only at the vertex itself, which is then in int Q); then a(P₁) = a_B + τ cos β
≥ a_R ≥ a₂ > a_z, a_p, against the monotonicity of a along a segment.  If τ_p < 0, σ_p ∈ (0, 1) (p under X's
lower-left edge, left of B_X; σ_p < 1 by (U9)): z has τ_z > 0 (a_z > a_B), so the segment crosses τ = 0 at some
σ* ∈ (σ_p, σ_z); σ* < 1 enters int X, σ* ≥ 1 is at or beyond X's wall vertex (x ≤ 0).  If τ_p > 1, σ_p ∈ [0, 1):
a_p > a_R − σ_p sin β ≥ a_R − sin β⁺ ≥ a* (U5), against a_p < a* (p ∈ S ⊂ {a < a*}).  So
**Q ∩ {a₁ < a < a₂} ⊂ W**, and every chord of Q there has length ≤ w_max.
**3.4 The extent.**  Q's chord function along a is a tent: on its support [a_min, a_max] (length c_ψ' + s_ψ' ≥ 1,
ψ' the tilt relative to e) it rises at rate 1/(s_ψ' c_ψ') ≥ 2 from a_min over min(s_ψ', c_ψ'), is ≥ 1 on the
plateau, and falls symmetrically.  a_min ≤ a_p < a* (p ∈ Q) and a_max ≥ a_E > a₂ (3.2).  The plateau (chords ≥ 1
> w_max) avoids (a*, a₂), so it is entirely right of a₂ — then on (a*, a₂) the chord is (a − a_min)/(s c) ≥
(a − a*)/(s c), giving a₂ − a* ≤ w_max s_ψ' c_ψ' — or entirely left of a* — then (a*, a₂) is in the falling part and
the chord at a*⁺ is (a_max − a*)/(s c) > (a₂ − a*)/(s c), giving the same.  With s c ≤ ½ (Lean `sincos_le_half`)
this is a₂ − a* ≤ w_max/2, against (U3) (Lean `wedge_extent_core`).  ∎  **This is the POKE bound for entry (i)**:
a poke into the C–X wedge reaches at most w_max s_ψ' c_ψ' ≤ w_max/2 ≤ 0.108 (rings) past the mouth a₂, while S's
top edge lies a₂ − a* ≥ 0.30 past it.  (Where p ∈ S is — the top strip, the left strip, the sliver under X — is
never used beyond a_p < a*.)
**3.5 What is NOT proved.**  STRIP₂ off the ring domain: the UPPER case when (U1)–(U9) fail — X's right vertex
short of T_u's top edge (a_R − sin β⁺ < a*: S's top corner T′ exposed beyond X), a wide wedge (large φ − θ with
a₂ − a* ≤ w_max/2), the room right of X ≥ 1 below C's top, or L_h ≤ 1 (θ near 45°, C low).  A266's `strip266`
covers that domain [T-computed*]; no ring is within 0.04 of leaving the ring domain (U5), and the exact bad-centre
area is 0 on all 43 rings ([T-computed], `upper267`).

## 4. The mechanism on the rings  [T-computed]

`approach267` (exact centre sets, 1° tilts): the closest unit square free of {C, X} in the quadrant to T_u ⊕ Q is
under C at every ring — centre (1.24–1.84, 0.53–0.76), tilt 3°–16°, touching C and the floor (41/43; 2 touch C
only), distance 0.054–0.170 (the WEDGE-FLOAT margin), and it overlaps A by 0.97–1.00 in SAT gap (page (a), (b)).
Restricted to centres above L_h the closest approach is 0.237–0.367, above C's top and right of X, touching X
(43/43) and C (33/43): the wedge entry, far.  `upper267`: the bad-centre area (free centres in the left shadow of
C ⊕ Q) is 0 at every tilt on every ring.  Per-ring rows in `results/{measure,upper,approach,hyp}267.json`.

## 5. Consequence for NO-JAM(11)

Lean `strip_in_ring_of_enclosure`: on the ring domain the BL sectors of a JAM corner reduce to `pair3` with T_u
as the END square, exactly as `jam_sector_of_strip` (ThreeLemmas) from `strip_lemma`.  So 5b of k0_route.md §13 =
STRIP₂-IN-RING [T-prose, this note] + `pair3` [T-computed*, A262 chain3 — `certs/pair3262_index.jsonl` still
absent at this writing].  **NO-JAM(11) still lacks:** 5a/5b `pair3` (TL and BL), 5d (indirect jams, FLOAT2:
`float262` / `span262` — WEDGE-FLOAT applies to a FLOAT2 corner's floaters verbatim (it uses only C, the wall, the
floor), but their strip statement is a separate obligation), 6's Lean axiom `jam_count`, and STRIP₂ off the ring
domain (§3.5) for rings not yet seen.  General m: everything here is corner-local and s-free — the lemma holds for
every n and every side.

## 6. What the brief had wrong

1. Measurements: h_u ∈ [0.25, 0.72] (not 0.38–0.72), h_v ∈ [0.929, 0.999] (not 0.988–0.999), θ_C up to 25.8°, C's
box area up to 0.010 (not ≤ 3·10⁻⁴), A's x_min 0.63–0.86; the rest as stated (A's band area 0, C touches neither
A nor X: gaps 0.0009–0.0106 / 0.0016–0.042).  2. The C–X "gap of width < 0.05" is not a slot: X's lower-right edge
lies on C's upper-left line and diverges from it at angle φ − θ up to 14°; the narrow neck (≤ 0.043) is at L, the
mouth (≤ 0.215) at X's right vertex, and the POKE that matters is along C's edge, bounded by the mouth width, not
by the SAT gap.  3. Case (iii) needs neither WEDGED-SEAL nor the corner-type table (addenda 1–2): one inequality,
valid for a wedged, a wall-only and a floating Q alike.  4. A neither closes the strip nor is needed to close it —
but it IS what the ring puts where the two-obstacle statement's closest approach sits (§4).  5. "Prove it on the
JAM domain": the JAM conditions alone (C meets the box, X meets T_u, C not pinned) do not give (U1)–(U9); they
are explicit ring-domain inequalities, [M] on 43/43 rings with the margins of §3.1 — said so, not hidden.

## 7. Lean, reproduce

`Statements/Open/StripEnclosure.lean`: theorems `wedge_float_core`, `sincos_le_half`, `wedge_extent_core`,
`e_point_core`, `strip_in_ring_of_enclosure`; opaque `RingDomain`; axiom [T-prose] `strip_two_in_ring`; build +
audit 0 sorry.  Reproduce (each < 1 min, `JAM_COARSE=1`): `python measure267.py`, `python upper267.py`,
`python approach267.py`, `python hyp267.py`, `python pages267.py`.
