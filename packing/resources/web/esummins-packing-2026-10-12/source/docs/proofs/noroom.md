# NOROOM — no K0-BLOCKED packing near ŝ, the rotational lock, the chain and the count, and the exact obstruction — A103, 2026-09-06

Target (A103 BRIEF): (A) Theorem NOROOM — no K0-BLOCKED packing at side m ≤ 3.9 (or the largest m* ≥ ŝ
provable); else (B) Theorem DRAIN(W) — K0-BLOCKED at m ∈ W ⇒ a k ≥ 1 packing at m; else (C) the exact
obstruction, drawn, with the one fact that would finish. Three ingredients prescribed: rotational retreat,
chains too long for the box, small corner regions against three free squares. Labels: [T] proved, [S]
routine given cited items, [M] measured (`attempts/A103-noroom/{code,results,logs}`, two second-scale
chores, one process, pure geometry), [F] finding, [C] open. Conventions: `nocrit_k0_blocked.md` (A90:
corner frame, μ_c, d_c, Lemma K, CLUSTER, NOCRIT-SEL, COL, RES(4)), `frame_census.md` (A91: F1–F8, W-GEN),
`k0_blocked_side.md` (A92: CEIL, SLIDE, Theorem N), `tilt_floor_k0.md` (A89: LOCK, MENU, JAM-0, TF-U, ID),
`wall_budget.md` (A97: WALL-F, FLOAT), `flood_lemma.md` (A101: SNAP, SHELL, MULTI, CELL-INTERLOCK),
`attempts/A102-rigidity-drain/notes/rigid102.md` (the drain table). ŝ = 3.877083590022814, W = [3.82, ŝ],
m < 4 throughout unless said otherwise. Trump = the A03 exact data (squares 0–5 upright, 6–10 at 40.18°;
BL staircase {0, 1, 3}, BR slot 2, TR slot 5, TL 2-crowd {4, 6} at depths 0.155 / 0.168).

## 0. Verdict

> **(A) is closed LOCALLY and not globally.** [T] **Lemma TRUMP-LOCAL (§5):** there are η₀, ε₀ > 0 such
> that no packing at side m ≤ ŝ + ε₀ whose poses lie within η₀ of a Trump image is K0-BLOCKED — the
> image's BR and TR cells cannot be doubly met by any admissible perturbation (the only squares within
> reach are the slot square and the 40.18° square resting on its corner, and every admissible pose of the
> slot square covers the corner region through which the tilted square would have to enter, in all three
> tilt cases). With the uniqueness clause of the main theorem (every packing at ŝ is an image) and
> compactness this gives **Theorem NOROOM-LOCAL: no K0-BLOCKED packing exists at any side m ≤ ŝ + ε₀**,
> i.e. the true threshold m* is STRICTLY above ŝ — but the argument is circular for the window (it
> assumes there is no packing below ŝ), so it delivers m* > ŝ as a statement about the geometry, not as a
> composition piece; ε₀ is not quantified (it needs a stability radius at ŝ + ε that the s0-only trees do
> not give). **The largest provable m* is therefore "ŝ + ε₀, ε₀ > 0 unquantified", and (A) at 3.9 is OPEN.**
> [M] `trumplocal103`: 29 000 admissible slot-square poses (side ŝ + {0, 0.01, 0.03, 0.06}, pose radius up
> to 0.1) all cover the corner region; 0 of 11 000 valid (slot, square-8) pairs near Trump's doubly meet
> BR, up to side ŝ + 0.1.
>
> **(B) is not closed.** DRAIN(W) reduces exactly to "¬RES-LOCK on W" (§6): the Ψ^(w)-minimal packing
> at side m is K0-FREE (then teleport gives k ≥ 1 at m) or a LOCKED FRAME; the frame is smaller than A90's
> RES(4) by the new ingredient — [T] **Lemma ROT (§2):** at the Ψ^(w)-minimal packing every intruder is
> HELD: the virtual corner row (the depth gradient, which is the row of a virtual contact at the argmin
> point pushing the square away from the corner, Lemma ROT-GRAD) together with the square's active contact
> rows admits a non-trivial non-negative self-stress; equivalently no single-square rigid motion (v, ω)
> strictly opens every contact and strictly decreases the depth. Gordan, exact, first-order; no second
> order needed for the lemma. The brief's rotation sense is corrected: rotating TOWARD the axis decreases
> the depth of a vertex-argmin intruder (rate |cos θ − sin θ|/2), but for an edge-argmin D-type intruder
> with c_x ≈ c_y the depth-decreasing sense is toward the DIAMOND (dμ/dφ = [(c_y − c_x) + (cos φ − sin φ)/2]
> /(cos φ + sin φ)²). [M] `lock103` on all 12 strictly K0-BLOCKED packings on disk + Trump: **no K0-BLOCKED
> packing is held at all eight intruders** — 37 unheld intruders (17 by translation, 13 by rotation, 7 by a
> screw), every packing has an unheld SECOND meeter (22 in all, 9 of which retract completely out of the
> cell along the single-square direction; the other 13 stop after 1e-7…1e-3 on a near-contact, A102's
> obstruction); **Trump: 5/5 intruders held (canary PASS)**, and the record 3.98548 is held at 7 of 8 (its
> TL nick, 7·10⁻⁹, translates out freely).
>
> **(C) delivered: the exact family is RES-LOCK(m) (§7) — K0-BLOCKED packings at side m at which every
> intruder is held (Lemma ROT) and every cardinal retreat cluster is wall- or strictly anchored (NOCRIT-SEL
> + W-GEN).** No realising configuration exists on disk at any side (12/12 fail ROT at some intruder); the
> candidate realisation is the jammed 4 × 4 grid at 4 + ε with its near-contacts closed (polish12's
> unheld nicks jam after 2·10⁻⁷), which is exactly where a locked frame SHOULD exist and where the theorem
> must fail. The drawing is `attempts/A103-noroom/results/lockmap103.svg` (the two sub-4 packings with
> every intruder labelled HELD / UNHELD and the unheld motion drawn). **The one fact that would finish:
> Conjecture LOCK-FREE(< 4) — a K0-BLOCKED packing at side < 4 always has an intruder that is not held
> (a strictly opening, depth-decreasing single-square motion exists).** With it, (B) follows by Lemma
> SEL-Ψ + ROT + K0-FREE, k0_00 = (window kills of k ≥ 1) + LOCK-FREE, no criticality, no tree (§8). It is
> true on the whole corpus, true at Trump in the only way it can be (Trump is K0-FREE and every one of
> its intruders IS held, so the statement genuinely needs a second blocked corner), and it must fail at
> 4 + ε (the jammed grid). The ingredients the brief expected to force it — the chain (§3) and the count
> (§4) — do not: [T] Lemma CHAIN-AX forces the positions and depths of an axis-aligned edge-to-edge
> column exactly (near end intrudes by 4 − m in its coordinate, far end sits in the far corner's column
> at [m − 1, m]), but [F] a general pressing link makes x-progress > −1 only (F6), Trump's own anchoring
> column sq4 → sq7 → sq8 → sq1 has four members, tilted middles and a far end that is neither a slot
> square nor an intruder (the brief's dichotomy has a third case), so no depth is forced; and [F] the
> four home regions [0, 1 + √2]² pairwise overlap for every m < 2 + 2√2 = 4.83, one free square can brace
> all four crowds (Trump's sq7 touches home squares of all four corners), so the count is vacuous — as
> A91's F5 said. What the frame needs and the count cannot see is the ROOM, and LOCK-FREE is the room
> statement at first order.

## 1. Setting

Packings: eleven closed unit squares Q_i = Q(c_i, θ_i), pairwise interior-disjoint, in [0, m]²; M(m) the
compact set of packings at side m. Corner frame, μ_c(Q) = min_{p ∈ Q} max(p_x, p_y), depth d_c(Q) = max(0,
1 − μ_c(Q)), intruder (d > 0), argmin set S_c(Q) = Q ∩ [0, μ]² (A90 §1); K0-BLOCKED: ≥ 2 intruders at every
corner; K0-FREE otherwise. Ψ^(w) = Σ_c w_c Σ_i d_c(Q_i) with ℚ-independent positive weights (A91 §8.2);
SEL-Ψ: Ψ^(w) attains its minimum on M(m) whenever M(m) ≠ ∅, and Theorem NOCRIT-SEL holds at the
minimiser for EVERY m (its proof uses only that a small feasible motion stays in M(m); minimality of m is
not used — A90 §3.3's "σ ≤ m and m is the minimum" is a remark, not a step). Contacts and rows: for a
square Q and a consistent selection S (A90 §1), the active rows of Q are its near-wall rows at distance 0
and its selected pair rows with gap 0; each active row k has gradient (n_k, τ_k) ∈ ℝ² × ℝ with respect to
Q's pose (v_x, v_y, ω) — n_k the unit contact force on Q (into Q), τ_k = (p_k − c) × n_k its torque about
Q's centre (a × b := a_x b_y − a_y b_x). A rigid motion y = (v, ω) of Q alone is S-feasible to first order
iff ⟨(n_k, τ_k), y⟩ ≥ 0 for every active k, and z + εy is a packing for small ε > 0 whenever all these
are STRICT (inactive rows keep their margin; Q's far-wall rows have margin > 1.4 for an intruder, A89 §1).

## 2. Ingredient 1 — the rotational lock

### 2.1 [T] Lemma ROT-GRAD (the depth gradient is a virtual contact)

Let Q be an intruder at c with μ = μ_c(Q) < 1 and let y = (v, ω) be a rigid motion of Q; the velocity of
a material point p of Q is ṗ = v + ω J(p − c), J = rotation by +90°. Then t ↦ μ_c(Q + ty) has the
right-derivative

  μ′(0⁺) = min_{p ∈ ext S_c(Q)} D_p(y),  D_p(y) = ṗ_x (p_x > p_y), ṗ_y (p_y > p_x), max(ṗ_x, ṗ_y) (p_x = p_y),

the minimum over the extreme points of the (convex) argmin set. In the three cases of Lemma K:

 (Y, vertex) S = {v}, v the lowest vertex with v_x < v_y = μ: μ′ = v̇_y, ∇μ = (0, 1, (v − c)_x) — the row
    of a virtual contact at v with unit force e_y on Q;
 (X, vertex) mirror: ∇μ = (1, 0, −(v − c)_y);
 (D, edge) S = {p*}, p* the crossing of the diagonal with an edge of inward unit normal n = (n_x, n_y),
    n_x, n_y > 0: μ = (c·n − 1/2)/(n_x + n_y) and ∇μ = (n, (p* − c) × n)/(n_x + n_y) — the row of a
    virtual contact at p* with force n on Q, scaled by 1/(n_x + n_y);
 (ties) an axis-aligned Q (S a segment of an edge), a 45° diamond or a vertex on the diagonal: μ′ is the
    min over the segment's endpoints, resp. the max of the two coordinate branches — one-sided, given by
    the formula above.

In every case the depth DECREASES along y iff μ′(0⁺) > 0, i.e. iff D_p(y) > 0 for every extreme point p.

*Proof.* max(p_x, p_y) is convex and piecewise-linear in p, ṗ is affine in p, and the min over the
compact convex set Q of a family of functions whose t-derivatives are continuous in p has, by the
argmin-set (Danskin) rule, the right-derivative min over the argmin set of the pointwise right-derivative;
by convexity the min is attained at an extreme point of S. The vertex cases read off ṗ. The edge case:
the edge is {p : (p − c)·n = −1/2}; the diagonal point on it has μ(n_x + n_y) = c·n − 1/2; differentiate
with ċ = v, ṅ = ωJn: μ′(n_x + n_y) + μ ω(n_x − n_y) = v·n + ω(c_y n_x − c_x n_y), and c_y n_x − c_x n_y −
μ(n_x − n_y) = (c_y − μ)n_x − (c_x − μ)n_y = (p* − c) × n. ∎

**Corollary ROT-SENSE [T] (the rotation sense, correcting the brief).** Under a pure rotation ω about the
centre: (i) a vertex-argmin intruder (types X, Y, or a D-vertex off 45°) has μ′ = ω(v − c)_x resp.
−ω(v − c)_y; for the lowest vertex v of a square of tilt θ ∈ (0°, 45°) this is (cos θ − sin θ)/2 per
radian of CLOCKWISE rotation, i.e. rotating toward the nearest axis decreases the depth at rate
|cos θ − sin θ|/2 — the brief's rule, and the PI's drain of the 3.9907 record (sq3, 1.31° clockwise of the
axis, all three contact torques counter-clockwise, depth 1.02·10⁻³ ≈ 0.5 sin θ − lift). (ii) An edge-argmin
D-type intruder with edge normal at angle φ has dμ/dφ = [(c_y − c_x) + (cos φ − sin φ)/2]/(cos φ + sin φ)²:
for c_x = c_y the depth decreases toward φ = 45° (the diamond) and INCREASES toward the axis — a same-
centre axis-aligned square intrudes deeper (μ = c − 1/2) than the diamond (μ = c − 1/(2√2)). (iii) At
exactly 45° with the vertex on the diagonal, and for an axis-aligned square, the rotation derivative is
one-sided: any rotation of an axis-aligned Y-type intruder DIPS one of its bottom vertices (μ′ = −|ω|/2
when that vertex lies in the box), so rotation never helps it — Trump's upright sq4 is such a square.

### 2.2 [T] Lemma ROT

**Lemma ROT.** Let z* minimise Ψ^(w) over M(m) (or over the non-image packings at ŝ). For every intruder
Q of every corner c and every consistent selection S at z*, the strict system

  ⟨(n_k, τ_k), y⟩ > 0 for every active row k of Q,   D_p(y) > 0 for every extreme point p of S_c(Q)

has NO solution y ∈ ℝ³. Equivalently (Gordan, per branch of the diagonal disjunctions): there are
multipliers μ_k ≥ 0 and λ_p ≥ 0, not all zero, with Σ_k μ_k (n_k, τ_k) + Σ_p λ_p g_p = 0, where g_p is the
chosen branch gradient (∇μ at p) — **Q is HELD: its contacts, together with a virtual push away from the
corner applied at its argmin point(s), are in compressive equilibrium** (λ ≠ 0), or Q is WEDGED by its
contacts alone (λ = 0, Lemma LOCK (b)'s self-stress).

*Proof.* If y solves the strict system for some S, then z* + εy (Q moved, the rest fixed) is S-feasible
for small ε > 0 (all active rows strictly increase, inactive rows keep their margins, Q's far-wall rows are
inactive by A89 §1), hence a packing at side m, hence in M(m) (and, for the ŝ-variant, outside every image
basin for ε < r_B − dist(z*, images)); d_c(Q) strictly decreases at first order by Lemma ROT-GRAD, no
other depth changes (Q intrudes one corner only, CC-1(ii), and no other square moves), so Ψ^(w)(z* + εy) <
Ψ^(w)(z*), contradiction. The alternative is Gordan's theorem for the homogeneous strict system, applied
to each of the ≤ 2^(#diagonal points) branches. ∎

Remarks. (1) Corollary 2 of NOCRIT-SEL (every intruder is pressed from its far side) is the translation
part of this lemma (ω = 0): in the Farkas form, the depth gradient −e (the retreat direction) must lie in
the cone of the contact forces. Lemma ROT adds the torque coordinate, so a square pressed from the far
side but free to turn is excluded too. (2) The lemma is exactly first-order and exact: the second-order
cases are those where the strict system is infeasible but a weakly feasible decreasing direction exists;
they are HELD by definition and not excluded — this is the same status as W-GEN's rate ties, and it is
where A102's "near-contact at gap 10⁻⁶" phenomenon lives (a near-contact is not an active row; the exact
lemma moves the square until it becomes one). (3) The contact set is the EXACT one (gap = 0). A tolerance
contact set (the 10⁻⁷ bar of A102 and of `lock103`) is a sound stand-in only in the direction "unheld at
the bar ⇒ unheld exactly for a small motion" (a gap in (0, 10⁻⁷) is inactive exactly); "held at the bar"
may over-count contacts. (4) Cluster form: if Q's decreasing motion is blocked only by rows to squares
that can move with it (a pressed chain), NOCRIT-SEL's cluster translation is the right tool for
translations; for rotations there is no cluster analogue (a rotating square drags its neighbours through
different motions), so ROT is a single-square lemma — its consumers accept exactly this.

**Corollary ROT-TORQUE [T] (the PI's rule as a special case).** If all active-contact torques τ_k of Q
about its centre have one sign σ (or vanish) and the depth-decreasing rotation sense is σ (ROT-SENSE), Q
is unheld: y = (0, 0, σ) solves the strict system whenever the torques are non-zero; zero torques (a
contact whose force line passes through the centre) leave a weak row and the strict system needs a
small translation to open it, which exists iff the force cone of those contacts is not the whole plane.
So "one-signed torques ⇒ drainable" is right when the free sense is the decreasing one and the forces
through the centre do not pin the square; A102's counterexamples (polish12, floor 10⁻⁴) are of the
second-order kind of remark (2).

### 2.3 [M] The census (`attempts/A103-noroom/code/lock103.py`, 3 s; `results/lock103.{json,jsonl}`)

For every intruder (meet bar 10⁻⁹) of the 12 strictly K0-BLOCKED packings A102 assembled (sides 3.98548 …
4.107) and of Trump: contact rows at the 10⁻⁷ bar with A102's edge-normal convention, the argmin set's
extreme points and branch gradients of Lemma ROT-GRAD, the LP "max t s.t. all rows ≥ t, |y|∞ ≤ 1" per
branch, UNHELD iff t* > 10⁻⁷ and a finite motion of size ε = min(10⁻⁶, g_min/10) (g_min = the smallest
inactive gap) confirms both the packing property (worst gap ≥ −10⁻¹²) and the depth drop; for every
unheld intruder the ROOM along the straight-line motion (travel to the first collision, depth there).

| packing | side | held / 8 | unheld (corner sq depth · mode · room) |
|---|---|---|---|
| floor 1e-2 (s0076) | 4.0004572 | 4 | BL sq0 1.0e-2 trans 0.22; BR sq3 1.6e-2 rot jams 4e-6; TR sq7 0.73 trans jams; **TR sq6 1.0e-2 rot exits** |
| floor 1e-3 (s0050) | 3.9907485 | 6 | **BR sq3 1.0e-3 rot exits (the PI's drain); TR sq6 1.0e-3 screw exits** |
| floor 1e-4 (s0202) | 4.0000044 | 2 | six unheld (both BR meeters, both TL meeters, BL sq1, TR sq7), all jam within 6·10⁻⁵ on near-contacts at 10⁻⁷…10⁻³ |
| floor 1e-6 (s0021) | 4.0000000 | 3 | five unheld; **TL sq4 3.4e-5 rot exits** |
| record_s0115 | 3.9854837 | 7 | **TL sq4 7.0e-9 trans exits** (room 8.5·10⁻⁵) |
| polish12 | 4.0000001 | 6 | TR sq7 6.6e-6 rot retracts 6 %; TL sq4 3.0e-5 trans retracts 0.4 % (near-contacts at 1.2·10⁻⁷) |
| polish15 | 4.0000041 | 4 | **BL sq1 1.0e-4 rot exits**; TR sq7 5.1e-2 trans jams; BL sq0, TL sq4 (first meeters) jam |
| polish21 | 4.0000075 | 4 | **TR sq7 1.0e-4 rot exits**; BR sq2 screw jams; two first meeters jam |
| polish24 | 4.0000119 | 2 | six unheld, all jam (retraction ≤ 8 %) |
| anchored0 | 4.1071074 | 7 | **BL sq1 1.0e-4 screw exits** (room 0.155) |
| anchored1 | 4.0837355 | 7 | **TL sq4 1.0e-4 screw exits** |
| anchored2 | 4.0837359 | 7 | TL sq4 1.0e-4 rot, jams at 1.4·10⁻⁷ on a near-contact (the twin of anchored1's exit) |
| **Trump** | 3.8770836 | **5 / 5** | none — K0-FREE, TL {4, 6} and the three slot squares all HELD; **canary PASS** |

Readings. (i) **Zero packings held at all eight intruders**; 37 unheld intruders (17 translation, 13
rotation, 7 screw); every packing has an unheld second meeter (22), 9 of them with full room (retraction
1.000 — A102's drainers, recovered from the single-square first-order test alone), 13 stopped by a
near-contact after 10⁻⁷…10⁻³ (A102's room dichotomy, now with the gaps that stop them recorded:
`min_inactive_gap`). (ii) The record 3.98548 is held at BL and BR (its two substantive crowds, d₂ =
0.0147 / 0.0145, both PINNED-RIGID in A102) and unheld only at the tangency-scale TL nick — under the
strict convention it is K0-FREE, under the exact one Lemma ROT retreats the nick: either way it is not a
locked frame. (iii) Trump is held everywhere, including its slot squares (whose virtual push at the corner
point is balanced by the two walls and the pressing neighbours) — Lemma ROT excludes nothing at Trump, as
it must. (iv) The obstruction A102 named is visible as the second-order cases of remark (2): the exact
lemma is satisfied by none of the corpus packings, but it moves several of them only by 10⁻⁷ before a new
row becomes active; the moved, re-locked packing is the object the theorem must exclude, and it is
plausibly a locked frame exactly at 4 + ε (the jammed grid), see §7.

## 3. Ingredient 2 — chains too long for the box

### 3.1 [T] Lemma CHAIN-AX (axis-aligned columns are rigidly placed)

Let Q = N₀, N₁, …, N_k be a wall-anchored column for the slot (Q, +x) in BL's frame (each N_{i+1} presses
N_i against +x, N_k touches the wall x = m), and suppose every member is axis-aligned. Then the contacts
are edge-to-edge or corner-to-corner and the x-extents are consecutive: N_i = [x₀ + i, x₀ + i + 1] ×
[y_i, y_i + 1] with x₀ = m − k − 1. For m ∈ [3.82, 4) this forces k = 2: x₀ = m − 3 ∈ [0.82, 1), Q intrudes
BL through the strip (m − 3, 1) × (y₀, 1) — its x-intrusion is exactly 4 − m ≥ 0.123 and its depth is
d_BL(Q) = 1 − max(m − 3, y₀) ≤ 4 − m — and the far end N₂ = [m − 1, m] × [y₂, y₂ + 1] occupies the
right-wall column: it is a BR intruder of depth 1 − y₂ if 0 < y₂ < 1, the BR slot square if y₂ = 0 (k ≥ 1),
and otherwise a wall square above the BR cell. Consecutive members have |y_{i+1} − y_i| ≤ 1, with
equality exactly at a corner kiss.

*Proof.* Two interior-disjoint axis-aligned unit squares in contact have x-extents [a, a+1], [a+1, a+2]
(edge contact, |Δy| < 1) or the same with |Δy| = 1 (corner kiss); "N_{i+1} presses N_i against +x" puts
N_{i+1} on the right. So the union's x-extent is exactly k + 1; it reaches x = m and starts at x₀ < 1
(Q's intruding point), so k + 1 > m − 1 ≥ 2.82, k ≥ 2, and k ≥ 3 would put x₀ = m − 4 < 0. ∎

Canary. Trump's only axis-aligned wall-anchored chains are its staircase and slot squares (sq3 → sq0 →
floor, sq1 → sq0 → left wall), where the far end IS a slot square and the packing is K0-FREE: consistent.

### 3.2 [T] Lemma CHAIN-EXT and Lemma LINK (what a tilted column does not force)

**Lemma CHAIN-EXT.** A wall-anchored column of k + 1 members from an intruder Q of depth d to the far
wall satisfies Σ_{i=0}^{k} (cos θ_i + sin θ_i) ≥ m − 1 + d − (total x-overlap of consecutive members);
with k + 1 = 3 and no overlap, Σ (cos θ_i + sin θ_i − 1) ≥ d − (4 − m): a 3-column whose near end
intrudes deeper than 4 − m contains a tilted member. *Proof.* The union is connected and spans from x <
1 − d to x = m. ∎ **Lemma LINK.** If N presses M against +x through a contact at p with separating unit
normal ν (M ⊂ {(q − p)·ν ≤ 0}, N ⊂ {(q − p)·ν ≥ 0}, ν_x > 0), then c_N − c_M has x-component > −1 and no
better bound holds uniformly: for ν nearly vertical N sits above M with x_max(N) < x_max(M) allowed
(A91 F6, and A97's Lemma WALL-NP overlap of 0.092 for touchers). So a column's x-progress per link is not
bounded below by a positive constant, and a wall-anchored column may have up to ten members.

**[F] The brief's dichotomy has a third case, and Trump is in it.** Trump's TL intruder sq4 (Y-type,
retreat = down) has the wall-anchored column sq4 → sq7 → sq8 → sq1 → floor (sq4's bottom-right corner
on sq7's 40° edge, sq7 on sq8, sq1's corner (2, 1) on sq8's lower-left edge, sq1 on the floor): four
members, two tilted middles, and a far end sq1 = [1, 2] × [0, 1] that is flush on the far wall, is NOT
flush to the adjacent (left) wall, and is NOT an intruder of BL (tangent, μ = 1) — a floor square in the
middle third. Below side 4 three unit footprints fit on a wall (WALL-3), so "flush at the far wall"
never forces "in a corner column"; the forced-depth statement of the brief holds only for the
axis-aligned edge-to-edge column of Lemma CHAIN-AX, and that column is what NINE (≤ 9 axis-aligned
squares) and K0-PAIR (each corner has a tilted meeter) already make rare. **No inequality on the eight
depths follows from the columns alone; the chain ingredient reduces to the frame census (A91), which is
dead.**

## 4. Ingredient 3 — the corner regions and the three free squares, computed

[T] Home squares of corner c (μ_c ≤ 1) lie in R_c := [0, 1 + √2]² ∩ [0, m]² in c's frame (F1), with
centres in [0, 1 + 1/√2]² = [0, 1.707]². (i) Adjacent centre regions are disjoint iff m > 2 + √2 = 3.414 —
true on W, with a gap of m − 3.414 ∈ [0.406, 0.463]; the plus-shaped middle {x or y ∈ (1.707, m − 1.707)}
contains no home-square centre. (ii) The regions R_c themselves pairwise overlap iff m < 2 + 2√2 = 4.83,
so on W every R_c meets every other; a unit square meets ALL FOUR regions (any square centred within
m/2 − 1.707 ≤ 0.23 of the centre of the container does), and the question the brief asks — "a unit square
meets at most how many of the four corner regions?" — has the answer four. (iii) Bracing: a free square
touches a home square of c only if their centres are within √2; a free square centred at the container's
centre is within (m/2 − 1.707)√2 ≤ 0.33 of the nearest admissible home-square centre of every corner, so
ONE free square can touch home squares of all four corners; with the true reach envelopes (A89 §8.5: a
2-crowd reaches ≥ 2.001 and up to 2.386 along a wall) adjacent crowds can even touch each other directly
(2.386 · 2 > ŝ). Canary: Trump's free square sq7 touches sq3 (BL home, tangent), sq4 (TL), sq8 (BR home,
tangent) and sq9 (TR home, tangent) — one square bracing all four corners. **[F] The count is vacuous
(A91's F5 in numbers): the frame needs at most four wall-to-wall chains sharing squares, and 3 free +
8 home squares supply them with room to spare; nothing in the region geometry limits the sharing.** The
only quantity that changes with m here is the 0.406–0.463 gap between adjacent centre regions, which the
crowds' arms cross freely (their reach is ≥ 2.001 > m/2).

## 5. Theorem NOROOM-LOCAL — no K0-BLOCKED packing near Trump

### 5.1 [T] Lemma TRUMP-LOCAL

**Lemma TRUMP-LOCAL.** There are η₀ > 0 and ε₀ > 0 such that: if m ≤ ŝ + ε₀ and z ∈ M(m) has every pose
within η₀ (centre in L∞, tilt in radians) of the corresponding pose of Trump (in its canonical
orientation, the container's origin at the BL corner), then the BR cell C = (m − 1, m) × (0, 1) is met by
at most one square of z. By the D4 symmetry of the statement the same holds for every image and, at TR
(Trump's TR is the BR configuration reflected), for the TR cell; hence z is K0-FREE.

*Proof.* Step 1 (who can reach C). In Trump, the closed box B = [ŝ − 1, ŝ] × [0, 1] is met by sq2 (= B)
and by sq8 at exactly one point, p₀ = (ŝ − 1, 1) = B's top-left corner, which lies in the relative
interior of sq8's lower edge of direction (cos 40.18°, sin 40.18°) (sq8's edge from (2.363, 0.568) to
(3.129, 1.211) passes through p₀; the exact data have the contact); every other square is at distance ≥
0.23 from B (sq10's lowest vertex is at height 1.232; sq1 ends at x = 2; sq9, sq5 are ≥ 1.4 away). A
square within η₀ of its Trump pose moves its points by ≤ η₀(1 + 1/√2) and C moves by ≤ ε₀, so for η₀ +
ε₀ < 0.1 only sq2′ and sq8′ can meet C.

Step 2 (where sq8′ can enter). Near p₀, sq8 is the half-plane H = {q : (q − p₀)·ν ≥ 0} with ν = (−sin
40.18°, cos 40.18°), and B ∩ H = {p₀} (the boundary line of H has slope tan 40.18° ∈ (0, ∞) and touches B
at its top-left corner from outside). After the perturbation, sq8′ ∩ C ⊂ {q ∈ C : (q − p₀′)·ν′ > 0} with
|p₀′ − p₀| ≤ 2η₀ + ε₀ and |ν′ − ν| ≤ η₀: a thin wedge W at C's top-left corner q₀ = (m − 1, 1), bounded by
x = m − 1, y = 1 and a line of slope in (0.7, 1.0) through a point within r := 3η₀ + ε₀ of q₀; every point
of W is within 2r of q₀ and inside C.

Step 3 (sq2′ covers W). Write Q₂ = sq2′, a unit square in [0, m]² with centre within η₀ + ε₀ =: η of
(m − 1/2, 1/2) and tilt α ∈ [0, η] in either sense. Let B₂ = (x_B, y_B) be its lowest vertex (y_B ≥ 0),
R₂ its rightmost (x_R ≤ m). Claim: {q ∈ C : |q − q₀| ≤ 2r} ⊂ int Q₂ for r small. Three cases.
 (a) α = 0: Q₂ = [a, a + 1] × [b, b + 1] with a ≥ m − 1 − η, b ≤ η, a + 1 ≤ m, b ≥ 0: it contains {x ∈ (m − 1,
     a + 1), y ∈ (b, 1)} ⊇ the 2r-neighbourhood of q₀ in C as soon as 2r < 1 − η.
 (b) counter-clockwise tilt α: the edges from B₂ go to R₂ = B₂ + (cos α, sin α) and to L₂ = B₂ + (−sin α,
     cos α) (the leftmost vertex), the top vertex is T₂ = B₂ + (cos α − sin α, cos α + sin α). The top edge
     L₂ → T₂ at abscissa x ≥ m − 1 has height y_L + (x − x_L) tan α ≥ y_B + cos α + (cos α + sin α − 1) tan α
     (using x_L = x_B − sin α ≤ m − cos α − sin α from x_R ≤ m) = y_B + f(α), f(α) := cos α + sin α − sin α
     (1 − sin α)/cos α; f(α) ≥ 1 on [0°, 45°] (f(0) = 1, f ≈ 1 + α²/2, f(30°) = 1.077, f(45°) = 1.121), so the
     top edge passes above y = 1 over the whole of C's x-range. The left edge B₂ → L₂ at height y ∈ (1 − 2r,
     1) has abscissa x_B − (y − y_B) tan α ≤ m − cos α − (1 − 2r − η) tan α ≤ m − 1 (cos α + c tan α ≥ 1 for
     c ≥ 0.9: the derivative −sin α + c sec²α is positive since sin α cos²α ≤ 0.385). The lower-right edge
     B₂ → R₂ at those abscissae has height ≤ y_B + sin α ≤ η + sin η < 1 − 2r. So the neighbourhood is
     right of the left edge, below the top edge, above the bottom edge: inside Q₂.
 (c) clockwise tilt α: from B₂ the edges go to L₂ = B₂ + (−cos α, sin α) (leftmost, LOW) and R₂ = B₂ +
     (sin α, cos α); T₂ = B₂ + (sin α − cos α, sin α + cos α). Near the slot the lowest vertex is the
     bottom-right corner, x_B ≥ m − 1/2, so the neighbourhood of q₀ is left of the edge B₂ → R₂. The left
     edge L₂ → T₂ at height y ≤ 1 has abscissa x_L + (y − y_L) tan α ≤ m − sin α − cos α + (1 − sin α) tan α
     = m − 1 + h(α) with h(α) = 1 − sin α − cos α + tan α − sin α tan α < 0 on (0°, 45°] (h ≈ −α²/2, h(10°) =
     −0.014, h(30°) = −0.078, h(45°) = −0.121): the left edge stays left of x = m − 1. The top edge T₂ → R₂
     at abscissa m − 1 + ξ has height ≥ cos α + (1 − ξ) tan α > 1 for ξ < 1/2. The lower-left edge B₂ → L₂
     has height ≤ η + tan α (1 − sin α) ≤ 0.3. So again the neighbourhood is inside Q₂.
Hence int Q₂ ⊇ W ∩ (2r-ball), and sq8′ ∩ int C ⊂ W has interior points in int Q₂ if sq8′ meets int C at
all — contradicting interior-disjointness. So sq8′ does not meet int C, and C has at most one meeter. ∎

The constants: η₀ + ε₀ < 0.1 (Step 1), 3η₀ + ε₀ small enough for Steps 2–3 (2r < 1 − η and the slope
window); η₀ = ε₀ = 0.01 works with room. [M] `trumplocal103` (seed 103): every one of 29 254 admissible
Q₂ poses (centre within 0.02 / 0.05 / 0.1 of the slot centre, tilt within the same in radians, inside a
container of side ŝ + {0, 0.01, 0.03, 0.06}, meeting the cell) contains all nine test points (m − 1 + ξ,
1 − ξ′), ξ, ξ′ ∈ {0.002, 0.01, 0.03}; and of 11 000 valid (Q₂, Q₈) pairs drawn within 0.02 / 0.05 / 0.1 of
Trump's sq2 / sq8 at sides ŝ + {0, 0.01, 0.03, 0.06, 0.1}, **0 have both squares meeting BR**.

Where the walls enter: Step 3 used y_B ≥ 0 and x_R ≤ m — Q₂ is in the corner of the container. That is
what makes the wedge at the cell's top-left corner unreachable: a slot square that is tilted or shifted
uncovers its cell only along the walls (the strips no square can reach, Step 1) or in slivers of area
O(α³) at its own lower-left edge (§5.3 of `wall_budget.md`'s jam geometry), never at the cell's inner
corner where the tilted neighbour sits. BL is different (its staircase neighbour sq3 can dip a vertex
into the strip that opens when sq0 slides right — the JAM-0 geometry) and TL is already a 2-crowd; the
lemma needs only two corners.

### 5.2 Theorem NOROOM-LOCAL and its status

**Theorem NOROOM-LOCAL.** Assume the uniqueness clause (every packing at side ŝ is a Trump image). Then
there is ε₀ > 0 such that no K0-BLOCKED packing exists at any side m ≤ ŝ + ε₀. *Proof.* Otherwise take
K0-BLOCKED z_k ∈ M(m_k) with m_k ↓ ŝ (below ŝ there is no packing at all, by the assumption's companion
s(11) = ŝ, so m_k ≥ ŝ); poses are bounded, so a subsequence converges to a configuration of closed unit
squares in [0, ŝ]² with pairwise disjoint interiors (SAT separation ≥ 0 is a closed condition) — a
packing at ŝ, hence an image; so z_k is eventually within η₀ of an image at side ≤ ŝ + ε₀ and Lemma
TRUMP-LOCAL says it is K0-FREE. ∎

[T, conditional] So **m* > ŝ strictly**: the PI's "no K0-BLOCKED packing has ever been found below 3.985"
has a rigorous local core — K0-BLOCKED packings cannot accumulate at Trump. What this does NOT give: (i)
anything for the window below ŝ (there the claim to prove is that M(m) = ∅, and the argument assumes it);
(ii) a value of ε₀ — that needs a stability radius at ŝ + ε (every packing at side ≤ ŝ + ε is within η₀ of
an image), which the s0-only certificates (s0 = ŝ + 4·10⁻⁷) supply only inside the (D) leaves of the k ≥ 1
trees and not for k0_00; the empirical value is ≈ 0.108 (the record). So (A) at 3.9 is OPEN and (A)'s
"largest provable m*" is ŝ + ε₀ with ε₀ > 0 unquantified.

## 6. (B) DRAIN(W) — the reduction

**Proposition [T].** Let m ∈ W with M(m) ≠ ∅ and let z* be Ψ^(w)-minimal on M(m). Then z* is K0-FREE
(and `teleport_packing` gives a packing at side m with a slot square — DRAIN(W)'s conclusion for every
K0-BLOCKED packing at m, indeed for every packing at m), or z* ∈ RES-LOCK(m):

  **RES-LOCK(m)** := K0-BLOCKED packings z at side m such that for every intruder Q of every corner c and
  every consistent selection S: (T) for every cardinal retreat e ∈ K_c(Q), C_e(Q) is wall-anchored or
  strictly (I)-anchored (W-GEN's D > 0) or a tilted-D rate tie (NOCRIT-SEL, W-GEN); (R) Q is HELD (Lemma
  ROT); and (S) [modulo K0-O1] d₂(c) ≥ ŝ − m at every corner (SLIDE), min(d₁, d₂) ≤ 1 − 1/√2 (CEIL).

*Proof.* NOCRIT-SEL (for Ψ^(w), A91 §8.2) and Lemma ROT at z*. ∎ So **DRAIN(W) ⟸ RES-LOCK(m) = ∅ for all
m ∈ W**, and this is the form in which (B) is open: it is A90-G1 with (R) added. Nothing else in this
file reduces it further; §3–§4 record that the two other prescribed ingredients do not bite.

## 7. (C) The exact obstruction

**The family.** RES-LOCK(m), m ∈ W, as defined in §6. Its members, if any, are frames in A90/A91's sense
(wall-to-wall or strictly anchored contact columns in both axes through all four crowds), with every
member of every crowd held against the corner by its contacts.

**Realisation [M].** None on disk at any side: every one of the 12 strictly K0-BLOCKED packings has an
intruder that is unheld at first order (§2.3), and the unheld square can always be taken to be a second
meeter. The two sub-4 packings (`results/lockmap103.svg`): the record 3.98548 is held at its two
substantive crowds and unheld at its 7·10⁻⁹ TL nick (translation, full room); the floor-10⁻³ record
3.99075 is unheld at both floor-depth meeters (BR sq3 by the PI's rotation, TR sq6 by a screw), both with
full room. The **candidate realisation is the jammed grid at 4 + ε**: polish12 (4.0000001) and floor 10⁻⁴
(4.0000044) are unheld only through motions of 10⁻⁷…10⁻⁵ that end on near-contacts at gaps 1.2·10⁻⁷ …
1.4·10⁻⁶; closing those gaps (moving each unheld square to its first collision, which Lemma ROT itself
does) produces an exact packing with more active rows at essentially the same side, and the grid's
rigidity (A102: play 10⁻⁷) makes it plausible that this packing is held at all eight intruders — a locked
frame at 4 + ε. This is where the theorem must fail (the brief's "must fail at 4 + ε"), and it says what
the theorem is about: below side 4 the jammed grid does not exist, and no other locked frame has been
found. Producing the closed-gap packing and testing it is a chore (a few polish steps with the contact
rows pinned, then `lock103`); it is not needed for the residue's definition and was not run.

**The one fact.** **Conjecture LOCK-FREE(< 4).** Every K0-BLOCKED packing at side m < 4 has an intruder Q
and a consistent selection S for which the strict system of Lemma ROT is feasible: a single-square rigid
motion strictly opening Q's active rows and strictly decreasing d_c(Q). Consequences: RES-LOCK(m) = ∅ on
W, hence DRAIN(W) (§6), hence k0_00's window kill (§8). Status of the evidence: (i) true on the corpus
(12/12, sides 3.985–4.107, with an unheld SECOND meeter every time); (ii) consistent with Trump exactly
as the brief demands — Trump is K0-FREE and every one of its five intruders is held, so no proof can go
through one blocked corner; a proof must use that TWO corners are blocked, and the natural place is the
shared wall (the two crowds' arms cross the 0.4-wide gap between their centre regions, §4, and a square
pressed between two crowds from opposite sides in the same axis at side < 4 cannot also be pressed from
the wall side of both — the unheld square is the one whose corner-ward virtual push is not in the cone of
its contacts, and along a wall of length < 4 with three unit footprints (WALL-3) one of the eight corner
members has all its far-side contacts on one side of its virtual push); (iii) it must fail at 4 + ε, and
the only place it can fail is the grid, where the wall carries exactly four footprints. What a proof
needs that this file does not have: a statement about the eight intruders' contact cones JOINTLY along
one wall — the wall-length budget WALL-F gives the count of footprints, the corner geometry (CEIL, JAM-0)
gives the shapes, and the missing step is that a held second meeter needs a far-side contact on the
wall-side of its argmin point (Corollary ROT-TORQUE's zero-torque case), which at side < 4 the wall
budget cannot supply at both corners of a wall. The sharper corpus-suggested form — the unheld intruder
is a second meeter with FULL ROOM (9 of 22 on the corpus; A102's dichotomy) — would give the drain
directly, without selection, but 13 of 22 corpus cases jam on near-contacts, so that form is false as
stated at 4 + ε and unmeasured below 4.

**What kills the alternatives.** Area (CEIL: charge ≤ 1 per corner, 4 < E(ŝ)), wall length (WALL-F:
j ≤ 3 jams, no composition kill), the census (A91: 28 orders), the static flood (A101: CELL-INTERLOCK
realised at the record's BL/BR) and the chain (§3) and the count (§4) are all silent on RES-LOCK because
none of them sees the contact CONES; LOCK-FREE is a statement about cones, and the first tool that speaks
about them is Lemma ROT.

## 8. Composition and Lean shape

**If LOCK-FREE(< 4) held on W (or (A) at m* ≥ ŝ, or DRAIN(W) directly):** for m ∈ W with M(m) ≠ ∅, the
Ψ^(w)-minimal z* is K0-FREE (LOCK-FREE + Lemma ROT), so by `teleport_packing` there is a packing at side m
with a corner slot square, excluded on [3.82, ŝ) by K0-O1 (k1_00's tree) and at ŝ equal to a Trump image
by K0-O1-ALL's uniqueness half; so M(m) = ∅ for m < ŝ and every packing at ŝ is an image. This is
`StratumKillSel Ψ^(w)` of A90 §6 with the open leaf ¬RES(4) replaced by LOCK-FREE, and it discharges the
k0_00 piece of `stratum_kill` in `ClassKilledAt` form (`Composition.lean`): no criticality (DF-K0/H1
unused), no selection beyond SEL-Ψ^(w), no tree.

Lean shapes (against `Composition.lean` / `Slide.lean`):
* `K0Blocked (m : ℝ) (z : Cfg) : Prop := ∀ c : Fin 4, ∃ i j, i ≠ j ∧ MeetsCornerBox m c (z i) ∧
  MeetsCornerBox m c (z j)` with `MeetsCornerBox` = interior intersection with `cornerBox m c`
  (`mem_interior_iff_uv`); K0-FREE = its negation.
* (A) `NoRoom (mstar : ℝ) : Prop := ∀ m ≤ mstar, ∀ z, CfgPacking m z → ¬ K0Blocked m z`; consumer
  `classKilledAt_of_noroom (hK1 : K0O1) (h : NoRoom shat) : ∀ m ∈ wnd, ClassKilledAt k0_00 m`, one
  `k0free_kill` (`Slide.lean` 117) per corner. NOROOM-LOCAL is `∀ z, CfgPacking m z → m ≤ shat + ε₀ →
  (∃ image, dist z image < η₀) → ¬ K0Blocked m z` — an off-tree statement (its consumer would need
  uniqueness first), recorded under motivation.
* (B) `DrainW : Prop := ∀ m ∈ wnd, ∀ z, CfgPacking m z → K0Blocked m z → ∃ z' c, CfgPacking m z' ∧
  z' i = slotSq m c` for some `i`; consumer as above through `k0free_kill`.
* Lemma ROT: `held (z : Cfg) (i : Fin 11) (c : Fin 4) : Prop` := the Gordan certificate (finite
  existential over the active rows' gradients — the rows are the polynomial SAT rows of `CaseSat.lean`,
  their pose-gradients rational functions of (c, t)); `rot_lemma : IsMinOn Ψ (packings m) z → Intrudes
  z i c → held z i c`, proved from `teleport`-style feasibility (Fact A + the strict rows) and the
  derivative formula of ROT-GRAD (`nlinarith`-sized per case). LOCK-FREE would be the axiom
  `lockfree : ∀ m < 4, ∀ z, CfgPacking m z → K0Blocked m z → ∃ i c, Intrudes z i c ∧ ¬ held z i c`.
* Lemma TRUMP-LOCAL: a finite geometric statement about two squares near two exact poses; its Lean form
  is the three-case inequality of §5.1 Step 3 (`nlinarith` after the case split on the tilt sense) plus
  Step 1's distance table on the A03 data.

## 9. Canaries

* Lemma ROT: Trump 5/5 held (both TL meeters PINNED-RIGID, the three slot squares held by their walls
  and pressers) — the lemma excludes nothing at Trump [M].
* Lemma TRUMP-LOCAL: about Trump by construction; the numerical pair test finds 0 doubly-met BR in
  11 000 valid neighbours up to ŝ + 0.1 [M].
* Lemma CHAIN-AX: Trump's axis-aligned columns end at slot squares (sq0), Trump K0-FREE [T]; Trump's
  tilted column sq4 → 7 → 8 → 1 is the third case of §3.2 [F].
* The count: Trump's sq7 braces all four corners [T].
* The record 3.98548 (outside W): held at BL/BR, unheld at the TL nick, consistent with A101 (converts
  at TR/TL) and A102 (drains by a tangency-scale move) [M].

## 10. Obligations ledger

| # | item | status |
|---|---|---|
| A103-O1 | Lemma ROT-GRAD (depth gradient = virtual corner contact; explicit rates; the rotation sense, brief corrected) | [T] §2.1 |
| A103-O2 | Lemma ROT (Gordan form, single square, exact first order); Corollary ROT-TORQUE (the PI's rule as the one-signed special case) | [T] §2.2 |
| A103-O3 | lock census on the corpus + Trump: 0/12 locked, 37 unheld, 22 unheld second meeters (9 full room), Trump 5/5 held | [M] §2.3, `results/lock103.{json,jsonl}` |
| A103-O4 | Lemma CHAIN-AX (axis-aligned column exact: 4 − m intrusion, far end in the far column), CHAIN-EXT, LINK; the third case (Trump) | [T]/[F] §3 |
| A103-O5 | the corner-region count: regions overlap for m < 4.83, one free square braces all four — vacuous | [T]/[F] §4 |
| A103-O6 | Lemma TRUMP-LOCAL (no K0-BLOCKED packing near an image at side ≤ ŝ + ε₀); Theorem NOROOM-LOCAL (m* > ŝ, modulo uniqueness) | [T] §5; [M] `results/trumplocal103.json` |
| A103-G1 | **(A) NOROOM at m ≤ 3.9, or any quantified m* ≥ ŝ** | **OPEN** — local only; ε₀ unquantified |
| A103-G2 | **(B) DRAIN(W)** | **OPEN** — reduces to RES-LOCK(m) = ∅ on W (§6) |
| A103-O7 | (C): RES-LOCK defined; no realisation on disk; candidate at 4 + ε named; drawing `results/lockmap103.svg`; the one fact = Conjecture LOCK-FREE(< 4) | [T]+[M]+[C] §7 |
| A103-O8 | composition + Lean shapes | note §8, no `lean/` edits |
| A103-C1 | close the near-contacts of polish12 / floor-10⁻⁴ and re-test: is the jammed grid a locked frame at 4 + ε? | [C] chore, minutes |
| A103-C2 | LOCK-FREE below 4 through the shared-wall cone argument (§7 (ii)) | [C] the theorem |

Runs (`attempts/A103-noroom/code/`, one process each, seconds, BLAS pinned, pure geometry):
`lock103.py all` → `results/lock103.{json,jsonl}`, `logs/lock103.log`; `trumplocal103.py` →
`results/trumplocal103.json`; `gen_lock103.py` → `results/lockmap103.svg` (every square geometry-checked:
containment and pairwise SAT separation ≥ −5·10⁻⁹). No A57/A60/A61/A96 file or process touched; frozen
verifiers untouched; nothing under A102 written (its loader was copied, not imported).
