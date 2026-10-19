# LOCK-FREE — the wall lemma made exact, its failure on one wall, the hook family, and the LOCKED census — A105, 2026-09-06

Target (A105 BRIEF): prove Conjecture LOCK-FREE(< 4) — every K0-BLOCKED packing of 11 unit squares at side m < 4
has an intruder that is not HELD (Lemma ROT, `noroom.md` §2) — for the largest m range possible (m ≥ ŝ suffices),
by the wall lemma (two blocked corners on one wall, the second meeters' far-side pushers against WALL-3), else via
FLOAT/CLUSTER, else via two adjacent walls; or deliver the exact obstruction as poses. Labels: [T] proved, [S] routine
given cited items, [M] measured (`attempts/A105-lockfree/{code,results,logs}`, two second-scale chores, one process,
BLAS pinned, pure geometry), [F] finding, [C] open. Conventions: `noroom.md` (A103: ROT-GRAD, ROT, ROT-TORQUE,
RES-LOCK, lock103), `nocrit_k0_blocked.md` (A90: corner frame, μ_c, d_c, Lemma K, CLUSTER, NOCRIT-SEL Cor. 2, Fact A),
`k0_blocked_side.md` (A92: CEIL, SLIDE), `tilt_floor_k0.md` (A89: LOCK, MENU, JAM-0), `wall_budget.md` (A97: WALL-F,
WALL-3, WALL-NP, FLOAT), `flood_lemma.md` (A101: SHELL), `attempts/A102-rigidity-drain/notes/rigid102.md`. ŝ =
3.877083590022814, W = [3.82, ŝ], m < 4 throughout. Contacts at SAT gap < 10⁻⁷, meet bar 10⁻⁹, LP strictness 10⁻⁷
(A102/A103 conventions) wherever a number is quoted. Trump = the A03 exact data.

## 0. Verdict

> **Theorem delivered: NONE — LOCK-FREE(m) is not established for any m, and the brief's wall lemma is FALSE on one
> wall.** [M, exact instances] A wall of length < 4 CAN carry two blocked corners with every one of their intruders
> held: the bottom wall of `record_s0115` (side 3.98548: BL {sq1, sq0}, BR {sq2, sq3}, 4/4 held at the 10⁻⁷ bar) and
> the left wall of the floor-10⁻³ record (side 3.99075: BL {sq0, sq1}, TL {sq4, sq5}, 4/4 held with explicit cone
> certificates, and 4/4 LOCKED in the stronger sense of §1). At 4.08–4.11 (anchored0/1/2) two ADJACENT walls
> sharing a blocked corner are LOCKED at all six intruders, so route 3 of the brief (two walls, one shared corner)
> is not a side-free statement either; below 4 the corpus never has two locked walls, so it is not refuted there.
> The m range of LOCK-FREE proved here is therefore EMPTY; what stands is Conjecture LOCK-FREE⁺(< 4) of §1.3 — a
> WEAKER requirement than A103's (it may use the translation lock of Lemma ROT-W as well as Lemma ROT), which is
> exactly what the consumer RES-LOCK(m) = ∅ (`noroom.md` §6) needs.
>
> **What is proved.** [T] **Lemma ROT-W (§1.2):** at the Ψ^(w)-minimiser no TRANSLATION of a single intruder with
> every active row rate ≥ 0 (WEAK rows — exact for translations, Fact A) decreases its depth; Farkas form: the
> corner-ward unit force −e lies in the cone of the square's contact force directions (walls included). It is
> strictly stronger than NOCRIT-SEL's Corollary 2 and independent of Lemma ROT (ROT is strict in all three
> coordinates, ROT-W is weak in two): `record_s0115`'s BL first meeter sq1 is ROT-held (a wedge: its two contacts
> are exactly opposite) and ROT-W-unheld (it slides along the flush edge out of the corner). [T] **Lemma LINE
> (§1.4):** a non-wedged held intruder is one whose contact forces admit a non-negative combination equal to the
> corner-ward force −λe (λ > 0) whose LINE OF ACTION passes through a point of its argmin set — statics, exactly.
> Its corollary PUSH-LINE (§2.1) is the brief's "far-side contact on the wall side of the argmin point" made exact:
> for a wall-hugging Y-type intruder the resultant of its SQUARE contacts must pass through a point (v_x, y_w) with
> v_x the argmin vertex's abscissa (< μ, within 1 − d of the wall) and y_w in its wall-contact range; the floor-10⁻³
> record's BR nick sq3 fails it (its only downward presser acts 0.97 away from the argmin vertex) and is the
> intruder lock103 found unheld by rotation — the PI's one-signed-torque drain, in LINE's language.
> [T] **The hook family (§3).** A wall-hugging axis-aligned nick N = [0, 1] × [1 − ε, 2 − ε] pressed by a tilted
> carrier T on the floor through N's inner corner (1, 1 − ε) comes in exactly two kinds: **α** (the corner on T's
> shallow edge, T ccw): lowest vertex at v_x = 1 + tan(θ/2) + (cos θ/sin θ) ε, and **β** (the corner on T's steep
> edge, T cw): v_x = 1 + (1 − sin θ)/cos θ + (sin θ/cos θ) ε, depth (sin θ/cos θ)(1 − sin θ − ε). **Theorem HOOK-α:
> two α-hooks at the two corners of one wall need m ≥ 4 + ε₁ + ε₂ > 4** — the wall lemma is TRUE for same-kind pairs
> (α–α: equal tilts [T], unequal tilts [M] on a 91 × 91 grid + [S]; β–β: [T], the identity (1 − sin θ)/cos θ + sin θ ≥ 1,
> §3.3); the four-α-hook shell (the tilted 4 × 4 grid) has side exactly 2(1 + sin θ)(1 + cos θ)/(sin θ + cos θ) ≥ 4 with
> equality only at the grid (§3.5). **But a mixed (β, α) pair with the carriers flush edge-to-edge fits at m = 2 +
> f(θ) + (s/c)ε₁ + (c/s)ε₂, f(θ) := (2 − sin θ)/cos θ + tan(θ/2), and f ≥ 1.93424 (minimum at θ = 15.25°) is BELOW 2
> for θ ∈ (0°, 30°) (f(30°) = √3 + (2 − √3) = 2 exactly)** — the record's
> bottom wall is exactly this at θ = 18.93°: the formula reproduces its side to six decimals (3.985484) and sq1's
> depth 0.22666 (§3.4, [M] `hook105`). So the count on ONE wall closes only for same-kind hooks; the flush mixed pair
> is the exact one-wall obstruction, drawn in `attempts/A105-lockfree/results/hookwall105.svg`. [T] **Lemma
> HOOK-W:** the β-carrier of a flush pair is never ROT-W-held by the pair's own contacts (they are ±n) plus the
> floor; it needs a third contact on its upper-right edge — the record has sq9 there at gap 2.1 · 10⁻⁷, A102's
> "near-contact just above the bar" phenomenon in its exact place.
>
> [M] **LOCKED census (`lockw105`, §5):** 0 of 12 corpus packings is LOCKED at all eight intruders (0 held at all
> eight, as A103 found); Trump 5/5 LOCKED, all PUSHED (cone certificates with λ = 1); **Trump's TL crowd is itself
> a β-hook** — the formulas of §3.1 with θ = 40.1819°, ε = 0.155475 (sq4) give sq6's depth 0.168321 and its top-wall
> vertex 1.595678, exact to the digits shown, so the hook is the universal corner motif (Trump TL, the record's BL
> and BR) and Trump, with one hook, is untouched by every two-hook statement. Walls with both corners
> blocked and all four intruders LOCKED: floor-10⁻³'s left wall (3.99075 — the only sub-4 instance), polish12's
> bottom (4.0000001), anchored0's right + top and anchored1/2's bottom + right (4.08–4.11: two adjacent locked walls
> sharing a corner). Canaries: Trump 5/5 (nothing fires); the 4 × 4 grid is the equality case of HOOK-α's shell
> and is not excluded (its nicks are not hooks of this family at all — they are JAM-0 dips); the drained records'
> unlocked intruders are the ones lockmap103 marks (3.98548: TL sq4 by translation; 3.99075: BR sq3 rotation, TR sq6
> screw) plus, under ROT-W, the record's wedged BL sq1 and TR sq7 — on the walls that are NOT hook pairs.

## 1. Setting, the two locks, and the theorem that is actually needed

### 1.1 Setting

Packings, corner frames, μ_c, d_c, intruders, K0-BLOCKED, Ψ^(w) with ℚ-independent weights, active rows (n_k, τ_k)
and the argmin set S_c(Q) with its extreme points p and branch gradients g_p = ∇μ at p (a virtual contact at p with
force e_p on Q: e_p = e_y for a Y-point, e_x for an X-point, n_Q/(n_x + n_y) for the D-edge point, the disjunction
{e_x, e_y} for a diagonal vertex): all as in `noroom.md` §1–2. HELD (Lemma ROT) = the strict system {⟨(n_k, τ_k), y⟩ > 0
∀ active k, D_p(y) > 0 ∀ p} has no solution y ∈ ℝ³; Gordan: Σ μ_k (n_k, τ_k) + Σ λ_p g_p = 0 with (μ, λ) ≥ 0, ≠ 0.

### 1.2 [T] Lemma ROT-W (the weak translation lock)

**Lemma ROT-W.** Let z* minimise Ψ^(w) over M(m) (or over the non-image packings at ŝ). For every intruder Q of every
corner c and every consistent selection S at z*, the system

  ⟨n_k, v⟩ ≥ 0 for every active row k of Q (WEAK),   D_p((v, 0)) > 0 for every extreme point p of S_c(Q)

has no solution v ∈ ℝ². Equivalently, per branch: −e ∈ cone{n_k : k active} where e is the branch's virtual force
(e = e_y for Y, e_x for X, n_Q for the D-edge point; for a diagonal vertex BOTH −e_x and −e_y lie in the cone; for a
tie segment the condition of its endpoints — a translation moves them alike, so it is the condition of the branch
with the smaller cone).

*Proof.* Rows are affine in the centres at fixed tilts (Fact A), so along z* + t(v, 0) (Q translated, everything
else fixed) every active row of Q is g_k(0) + t⟨n_k, v⟩ ≥ 0 exactly, inactive rows keep a margin, Q's far-wall
rows have margin > 1.4, dominance rows do not move: z* + t(v, 0) is S-feasible, a packing at side m, in M(m) (and
outside the image basins for small t in the ŝ-variant). μ_c(Q + tv) has right-derivative min_p D_p(v) > 0 (ROT-GRAD
with ω = 0), so d_c(Q) strictly decreases, no other depth changes: Ψ^(w) decreases, contradiction. The alternative is
Farkas' lemma for {⟨n_k, v⟩ ≥ 0, ⟨e, v⟩ > 0}: infeasible iff −e = Σ μ_k n_k, μ ≥ 0. ∎

Remarks. (i) NOCRIT-SEL's Corollary 2 ("some active row has n_x < 0") is the case of one contact; ROT-W says the
contacts' force directions positively span the corner-ward direction — walls (+e_x, +e_y in the corner frame) never
help, so at least one square contact has a component toward the corner, and if the square contacts' directions lie in
a half-plane not containing −e the wall contacts cannot repair it. (ii) ROT-W is not implied by ROT: `record_s0115`
BL sq1 (X-type, argmin vertex (0.7733, 0.3245)) has exactly two contact directions, ±(0.9459, −0.3245) (sq0's corner
on its steep edge, sq2 flush on its lower-right edge), so it is a WEDGE — ROT's strict system is infeasible to
within 1.3 · 10⁻⁸ (lock103's t*) — while ROT-W's system has the solution v = (0.3245, 0.9459) (slide up along the
flush edge, both rows at rate 0, the floor 2.7 · 10⁻⁵ away): t* = 0.343, and the finite motion confirms the depth
drop. (iii) Nor is ROT implied by ROT-W: the floor-10⁻³ record's BR sq3 is ROT-W-held (pressed from above by sq8,
−e_y in the cone) and ROT-unheld by the rotation A102 and the PI found.

### 1.3 The theorem that is needed: LOCK-FREE⁺

**Definition.** An intruder is **LOCKED** if it is HELD (ROT) and W-HELD (ROT-W). By Lemma ROT + Lemma ROT-W every
intruder of the Ψ^(w)-minimiser is LOCKED, so `noroom.md` §6's residue satisfies RES-LOCK(m) ⊆ {K0-BLOCKED packings
at m with every intruder LOCKED} and the reduction of DRAIN(W) reads:

  **Conjecture LOCK-FREE⁺(< 4).** Every K0-BLOCKED packing at side m < 4 has an intruder that is not LOCKED.

It is implied by LOCK-FREE(< 4) and implies DRAIN(W) (with SEL-Ψ, ROT, ROT-W, K0-FREE exactly as in `noroom.md` §8);
its consumer is the same Lean axiom shape with `held` replaced by `held ∧ wheld`. Everything below is stated for
LOCKED; the records show the two locks fail at different squares (§5), so the weaker conjecture is genuinely easier.

### 1.4 [T] Lemma LINE (held = static equilibrium under the virtual push)

For a wrench w = (F, τ) ∈ ℝ² × ℝ with F ≠ 0 the LINE of w is {p : p × F = τ}: the set of points at which the single
force F has torque τ about the centre (the centre at the origin of the frame). Each active row (n_k, τ_k) is the
wrench of the unit force n_k at the contact point p_k; each virtual row g_p is the wrench of the force e_p at p.

**Lemma LINE.** Q is HELD with a Gordan certificate with λ ≠ 0 (PUSHED) iff there are μ ≥ 0 and a point q in the
convex hull of the argmin points p with λ_p > 0 such that Σ μ_k n_k = −λ ē and Σ μ_k τ_k = −λ (q × ē), where ē =
Σ λ_p e_p / λ, λ = Σ λ_p: **the contacts' resultant is the corner-ward force −λē along a line through q ∈ conv S_c(Q)**
(through the argmin vertex when it is unique; along −n_Q through p* for a D-edge point; through any point of the
argmin segment for an axis-aligned tie). Otherwise Q is HELD only if it is WEDGED (λ = 0: a self-stress of its
contacts, e.g. two exactly opposite contact directions, or a pinch between a wall and a flush neighbour).

*Proof.* Gordan's certificate Σ μ_k (n_k, τ_k) = −Σ λ_p g_p; the right side is the wrench of the forces λ_p e_p at
the points p, which is the wrench of the single force λē at the λ-weighted mean point q of the p's (forces at
points add to a force at the barycentre when they are parallel; for a diagonal vertex the two branch forces e_x,
e_y are at the same point). A wrench with non-zero force is that force along its line. ∎

**Corollary NO-TIP [S].** A wall-touching intruder with wall contact set K (the points of Q on the wall) is HELD
and PUSHED only if the resultant of its SQUARE contacts plus the virtual push passes through the wall's force line
at a point of K's convex hull — the zero-moment-point condition (the square must neither slide nor tip). *Proof.*
Wall forces are parallel (normal to the wall) at the points of K; LINE. ∎

## 2. The wall lemma, exactly

### 2.1 [T] Corollary PUSH-LINE (the far-side pusher's position)

Let B be a held, pushed intruder of BL of Y-type with a vertex argmin v = (v_x, v_y), v_x < v_y = μ (so v_x < μ ≤
1 − d ≤ 1, and v_x < 1 − d: the argmin vertex lies within 1 − d of the LEFT wall in x). Let B touch the left wall at
the heights [y_lo, y_hi] and let R be the resultant (with the certificate's multipliers) of B's square contacts.
Then R = (−G, −λ) with G ≥ 0 the wall load and λ > 0, and **R's line of action passes through (v_x, y_w) for some
y_w ∈ [y_lo, y_hi]** (through v itself if B does not touch the wall, G = 0). Symmetrically for X-type with the floor.

*Proof.* LINE: the total resultant is (0, −λ) along the vertical line x = v_x; the wall contributes (G, 0) at some
point (0, y_w) of the wall contact range (parallel forces at points of a segment add to a force at a point of the
segment); the third force R must close the triangle, so the three lines are concurrent: R passes through the
intersection (v_x, y_w) of x = v_x and y = y_w. ∎

Reading. The downward push that holds a wall-hugging nick must act on the WALL SIDE of the square: its line must
cross the height of the wall contact directly above (or below) the argmin vertex, i.e. within v_x < 1 − d of the
wall. A presser far from the wall (on the inner part of B's top edge) needs a second square contact to bend the
resultant back; the wall itself cannot (it only pushes horizontally). This is the brief's "contact on the wall
side of the argmin point", and it is exactly where the floor-10⁻³ record's BR nick sq3 fails: v = (0.0228, 0.99898)
in BR's frame (0.023 from the right wall), its square contacts are sq2 below (up, at BR-frame x = 0.067) and sq8's
corner above-left (down-right, at x = 0.9997), the wall pushes at x = 0; the down-pushing resultant cannot be moved
to x = 0.023 with non-negative multipliers — lock103: unheld, t* = 0.36, by rotation (all three contact torques are
of one sign, ROT-TORQUE). Its TR twin sq6 fails the mirror statement (X-type, screw).

### 2.2 [F] The one-wall statement is false: two exact instances

**Wall statement (the brief's).** On a wall of length m < 4 whose two corners are both blocked, some intruder of
those two corners is not held.

*Instance 1* — `record_s0115`, side 3.98548, bottom wall. BL: sq1 (tilt 18.93° cw, floats 2.7 · 10⁻⁵ above the
floor, depth 0.2267, X-type) and sq0 = [0, 1] × [0.98527, 1.98527] (Y-type nick 0.01473 from above, on the left
wall); BR: sq2 (same tilt, on the floor, depth 0.0997, D-type) and sq3 = [2.98548, 3.98548] × [0.98548, 1.98548]
(nick 0.01452, on the right wall). lock103 / lockw105: sq0, sq2, sq3 HELD and PUSHED with explicit certificates
(sq0: μ = (1.34, 0.43, 0.27, 0) on (sq1's corner, sq10 above, the wall ×2), λ = 1; sq3: μ = (3.08, 2.92, 0, 0, 0) on
(sq2's edge, sq6 above, …)); sq1 HELD at the 10⁻⁷ bar (t* = 1.3 · 10⁻⁸ — a wedge, §1.2 (ii)). Under the STRICT
convention with the exact contact set, sq1 is not held (t* > 0), but the margin is the size of the LP tolerance,
i.e. the wall is held up to A102's "near-contact" phenomenon: sq9 sits on sq1's upper-right edge at gap 2.1 · 10⁻⁷,
and with that row active sq1 is HELD and LOCKED (Lemma HOOK-W, §3.4).

*Instance 2* — floor-10⁻³ record, side 3.99075, left wall. BL: sq0 (tilt 16.41°, on the left wall, Y-type, depth
0.189) and sq1 = [0.923, 1.923] × [0, 1] (X-type, depth 0.077, on the floor); TL: sq4 (tilt 16.41°, flush on top of
sq0 — a tilted column on the wall — depth 0.090, D-vertex type) and sq5 = [0.990, 1.990] × [2.991, 3.991] (X-type,
depth 0.0099, on the top wall). All four HELD with certificates (sq0: λ = 1, μ on sq1, sq4, sq10, wall; sq1: pressed
by sq9 low on its right edge, λ = (0.82, 0.18) on the two argmin endpoints; sq4, sq5 likewise) and all four W-HELD:
**the left wall is LOCKED at every intruder of its two blocked corners at side 3.99075 < 4.** The packing's unlocked
intruders are on the right wall (BR sq3, TR sq6).

So the count "the two far-side pushers cannot both exist on a wall of length < 4" is refuted as stated. What the
instances have in common is named in §3: each is a WALL COLUMN — a nick hugging the side wall carried by a tilted
square — and the two columns of one wall fit below 4 when their carriers are of different kinds or when one of
them is itself a tilted flush column (instance 2's sq0–sq4).

### 2.3 [F] Route 3 (two adjacent walls) is not side-free

anchored0 (4.1071): right and top walls both blocked at both corners and LOCKED at all six intruders (BR, TR, TL);
anchored1/2 (4.0837): bottom and right, all six LOCKED (BL, BR, TR). So "two adjacent walls with a shared blocked
corner cannot both be locked" holds at no side ≥ 4.08 and can only be a statement about m < 4, where the corpus
has two packings and neither has two locked walls. Nothing here proves it.

## 3. The hook family — the exact one-wall geometry

### 3.1 Definitions

Work in BL's frame; the wall is the left wall x = 0, the floor y = 0. A **hook** is a pair (N, T): N = [0, 1] × [1 − ε,
2 − ε] (an axis-aligned square hugging the left wall and intruding BL from above by ε ∈ (0, 1 − 1/√2], Y-type, argmin
segment [0, 1 − ε] × {1 − ε}) and T a tilted unit square (tilt θ ∈ (0°, 45°]) with its lowest vertex v = (v_x, 0) on
the floor, N's inner bottom corner P = (1, 1 − ε) lying on an edge of T with T on the far side of that edge. N is
then pressed from above (Cor. 2) by whatever sits on its top edge; T is N's carrier. By JAM-0's mechanism (a vertex
of the tilted square in the L-strip is its lowest or leftmost vertex) T's two edges from v are the only candidates
to carry P, and the two cases are:

* **kind α** — T ccw by θ, P on the edge from L = v + (−sin θ, cos θ) in direction (cos θ, sin θ) (T's upper-left,
  SHALLOW edge; the corner-facing lower-left edge is below it). Solving P = L + u (cos θ, sin θ): u = (1 − ε −
  cos θ)/sin θ ∈ [0, 1] (so cos θ ≤ 1 − ε ≤ cos θ + sin θ) and
    v_x^α(θ, ε) = 1 + sin θ − cos θ (1 − ε − cos θ)/sin θ = 1 + tan(θ/2) + (cos θ / sin θ) ε.
  T's right vertex is v + (cos θ, sin θ); T intrudes BL through its lower-left edge's diagonal point (D-edge type,
  inward normal (cos θ, sin θ)) with depth 1 − v_x cos θ/(sin θ + cos θ), positive iff v_x < 1 + tan θ, i.e. iff
  ε < (sin θ/cos θ)(tan θ − tan(θ/2)) (0.0605 at 18.93°; the record's BR has ε = 0.0145 and sq2's depth 0.0997 = the
  formula); for small ε and θ the carrier is a shallow D-intruder.
* **kind β** — T cw by θ, P on the edge from L = v + (−cos θ, sin θ) in direction (sin θ, cos θ) (T's upper-left,
  STEEP edge): u = (1 − ε − sin θ)/cos θ and
    v_x^β(θ, ε) = 1 + (1 − sin θ)/cos θ + (sin θ / cos θ) ε,
  T's left vertex is L = (1 − (sin θ/cos θ)(1 − sin θ − ε), sin θ), T is an X-type intruder (argmin L) of depth
    d^β = (sin θ / cos θ)(1 − sin θ − ε),
  and its right vertex v + (sin θ, cos θ) is HIGH (height cos θ).

[M, `hook105`] On `record_s0115`: θ = 18.9334°, ε_BL = 0.01473, ε_BR = 0.01452; v_x^β = 1.71922 (sq1's lowest vertex:
1.71923), d^β = 0.22667 (sq1: 0.22666), v_x^α from the right wall = 1.20906 (sq2: 1.20906). The identity tan(θ/2) =
sin θ/(1 + cos θ) = (1 − cos θ)/sin θ is used throughout.

### 3.2 [T] Lemma HOOK-N (the nick is held by its carrier and its presser)

In a hook, N is HELD and PUSHED as soon as it is pressed from above by a square M with a contact on N's top edge at
some abscissa x_M ∈ [0, 1] with force −e_y (an axis-aligned M, or a vertex of M), and is W-HELD. *Proof.* Forces on N:
wall (+e_x at (0, y_w), y_w ∈ [1 − ε, 2 − ε]), the carrier at P with force ν = the inward normal of T's carrying edge
(kind α: (sin θ, −cos θ) is the outward normal of the shallow edge, so the force on N is (−sin θ, cos θ)F — up-left;
kind β: (−cos θ, sin θ)F — up-left too), M with −F_M e_y at (x_M, 2 − ε), the virtual push +λ e_y at (x_v, 1 − ε), x_v ∈
[0, 1 − ε]. Balance: G = F ν_x^-, F_M = λ + F ν_y; torque about N's centre with y_w = 1 − ε and x_v = 0: (kind α)
(x_v − x_M)λ + (1 − x_M) F cos θ = 0 has the solution F = λ x_M /((1 − x_M) cos θ) for any x_M ∈ (0, 1); (kind β) the
same with sin θ. W-held: −e_y = (F_M − …) — the cone of {e_x, ν, −e_y} contains −e_y. ∎ (In `record_s0115`: sq0's
certificate μ = (1.34 on sq1's corner, 0.43 on sq10, 0.27 on the wall's lower point), λ = 1.)

So the nicks of a hook are never the unlocked squares; the wall lemma is a statement about the CARRIERS.

### 3.3 [T] Theorem HOOK-α (two α-hooks on one wall need m > 4)

Let the two corners of the floor carry α-hooks with tilts θ₁, θ₂ ∈ (0°, 45°] and nicks ε₁, ε₂ > 0, the carriers on
the floor and interior-disjoint. Then

  m ≥ v_x^α(θ₁, ε₁) + v_x^α(θ₂, ε₂) + D(θ₁, θ₂) ≥ 2 + Φ(θ₁, θ₂) + ε₁ + ε₂,  Φ := tan(θ₁/2) + tan(θ₂/2) + D,

where D(θ₁, θ₂) is the least horizontal distance between the lowest vertices of two floor squares (one ccw θ₁, one
cw θ₂) with disjoint interiors, and

  D(θ₁, θ₂) = max( cos θ₁ + sin θ₁ cos θ₂ / sin θ₂,  cos θ₁ + cos θ₂ − (sin θ₂ − sin θ₁) sin θ₁ / cos θ₁ )  (θ₁ ≤ θ₂).

**Φ ≥ 2 on [0°, 45°]², with equality only at θ₁ = θ₂ = 0; hence m ≥ 4 + ε₁ + ε₂ > 4.** Status: the first inequality
and the formula for D are [T]; Φ ≥ 2 is [T] for θ₁ = θ₂ and at θ₁ = 0, [M] on a 91 × 91 grid (min Φ = 2.000000 at the
origin, D formula against SAT bisection to 7 · 10⁻¹⁰), [S] in general (one-variable calculus in θ₂ at fixed θ₁; not
written out).

*Proof.* Positions: the BL carrier's lowest vertex is at v_x^α(θ₁, ε₁) from the left wall, the BR carrier's at
v_x^α(θ₂, ε₂) from the right wall, and the two are D apart at least; v_x^α = 1 + tan(θ/2) + (cos θ/sin θ)ε ≥ 1 +
tan(θ/2) + ε since cos θ ≥ sin θ. D: the right boundary of the ccw square (relative to its lowest vertex) is the
concave piecewise-linear function h ↦ x_R(h) rising along (cos θ₁, sin θ₁) to height sin θ₁ then falling along
(−sin θ₁, cos θ₁); the left boundary of the cw square is the mirror with θ₂; the squares are disjoint iff x_R(h) −
x_L(h) ≤ D for all common heights, and the concave sum is maximal at a breakpoint, h = sin θ₁ (value cos θ₁ + sin θ₁
cot θ₂) or h = sin θ₂ (value cos θ₁ − (sin θ₂ − sin θ₁) tan θ₁ + cos θ₂). Φ ≥ 2: at θ₁ = θ₂ = θ, Φ = 2 tan(θ/2) + 2 cos θ
and cos θ + tan(θ/2) − 1 = tan(θ/2)(1 − sin θ) ≥ 0 (exact identity, equality only at θ = 0); at θ₁ = 0, D ≥ 1 + cos θ₂
and Φ ≥ 1 + cos θ₂ + tan(θ₂/2) ≥ 2 by the same identity. ∎

Reading. Two hooks of the SAME kind α at the two ends of a wall push their carriers' inner vertices past the
midline of a wall of length 4 — the wall lemma holds for them, and their nicks are exactly what the wall lacks:
m − 4 ≥ ε₁ + ε₂ > 0, so at m ≤ 4 the nicks vanish and the corners are singly met.

**Theorem HOOK-β [T] (β–β pairs).** Two β-hooks with a common tilt θ at the two corners of one wall have their
carriers' HIGH inner vertices (height cos θ) at horizontal distance ≥ 2 sin θ (the steep lower edges converge
upward, the upper edges diverge), so m ≥ 2 v_x^β + 2 sin θ = 2 + 2[(1 − sin θ)/cos θ + sin θ] + (sin θ/cos θ)(ε₁ + ε₂),
and (1 − sin θ)/cos θ + sin θ − 1 = (1 − sin θ)(1 − cos θ)/cos θ ≥ 0 with equality only at θ = 0: **m ≥ 4 + tan θ (ε₁ +
ε₂) > 4.** (Unequal tilts: the same breakpoint argument with the roles of the shallow and steep edges exchanged [S].)
So same-kind pairs never fit below 4; the exception is the MIXED pair, where one carrier's steep edge lies flush
against the other's shallow edge.

### 3.4 [T] Proposition HOOK-βα (the mixed flush pair fits below 4) and Lemma HOOK-W

Let the floor carry a β-hook at BL and an α-hook at BR with the same tilt θ, the carriers flush edge-to-edge
(the β carrier's lower-right edge, direction (sin θ, cos θ) from v₁, against the α carrier's upper-left… in the
container both are cw by θ and the α carrier's left edge is parallel to the β carrier's right edge). The flush
contact puts the lowest vertices 1/cos θ apart, so

  m = v_x^β(θ, ε₁) + 1/cos θ + v_x^α(θ, ε₂) = 2 + f(θ) + (sin θ/cos θ) ε₁ + (cos θ/sin θ) ε₂,  f(θ) := (2 − sin θ)/cos θ + tan(θ/2),

and f(θ) < 2 exactly for θ ∈ (0°, 30°) (f(0) = 2, f(30°) = √3 + tan 15° = √3 + 2 − √3 = 2, f > 2 beyond) with min f =
1.934237 at θ = 15.25° [M]: **a flush (β, α) hook pair occupies less than 4 of the wall; at ε₁ = ε₂ → 0 it fits at
3.934.** `record_s0115` is the instance θ = 18.93°: f = 1.9385, ε-terms 0.0051
+ 0.0423, m = 3.985484 = its side [M, six decimals].

**Lemma HOOK-W.** In a flush (β, α) pair the β carrier T₁ has contact directions ν = (cos θ, −sin θ) (N's corner on
its steep edge; on T₁ this force points down-right) and −ν (the flush neighbour) and, if it touches the floor, e_y.
The cone {ν, −ν, e_y} is a half-plane that does not contain −e_x: **T₁ is ROT-W-unheld unless it has a further
contact with a component toward the corner** — a presser on its upper-right edge (force (−sin θ, −cos θ)) or on its
top vertex. With such a presser, −e_x = (1/sin θ)(−sin θ, −cos θ) + (cos θ/sin θ) e_y ∈ cone, and T₁ is LOCKED
whenever its LINE condition is met. *Proof.* Farkas; the arithmetic is displayed. ∎ (Record: sq9's vertex sits on
sq1's upper-right edge at gap 2.1 · 10⁻⁷; at the 10⁻⁷ bar it is inactive and sq1 is a wedge; closing that gap by
Lemma ROT-W's own motion makes the whole bottom wall LOCKED. The α carrier sq2 needs nothing extra: the floor, sq3's
corner (down-left) and the flush contact already give a certificate, λ = 1.)

### 3.5 [T] The four-α-hook shell (the tilted grid)

Four α-hooks, one per corner, with the two nicks of each side wall STACKED (N₁ = [0, 1] × [1 − ε, 2 − ε] and N₂ = [0, 1]
× [2 − ε, 3 − ε], nicking BL and TL by ε each, so 2ε = 4 − m — CHAIN-AX vertically), equal tilts, neighbouring
carriers touching vertex-to-vertex along each wall: m = 2 v_x^α(θ, (4 − m)/2) + 2 cos θ, which solves to

  m(θ) = 2 (1 + sin θ)(1 + cos θ)/(sin θ + cos θ) = 4 + θ² + O(θ⁴) ≥ 4, equality iff θ = 0 (the 4 × 4 grid).

So the shell's nicks are ε = (4 − m)/2 ≤ 0: **the tilted grid is never K0-BLOCKED; at θ = 0 it is the grid at side 4
with tangent corners.** [M, `hook105`] Built as poses at θ = 18.93° (m = 4.057526), 5°, 40°, 45°: containment 0,
pairwise SAT ≥ −7 · 10⁻¹⁶, every corner box met by exactly one square. This is the family the brief's picture
("the grid escapes because its wall carries four footprints") describes, and it is excluded at every side — the
blocked grid at 4 + ε of A102/A103 (polish12, floor-10⁻⁴) is NOT in it: its second meeters are JAM-0 dips of
neighbours tilted by 10⁻⁴…3°, not wall-hugging nicks carried by tilted floor squares.

### 3.6 [F] Where the one-wall count stands

| wall pair | count | m < 4 possible? | realised |
|---|---|---|---|
| α–α (carriers on the floor) | m ≥ 4 + ε₁ + ε₂ | no [T] | — |
| β–α flush | m = 2 + f(θ) + … , f ≥ 1.934 | yes for θ < 33.5° [T] | `record_s0115` bottom (3.98548), held at the 10⁻⁷ bar |
| β–β | m ≥ 4 + tan θ (ε₁ + ε₂) | no [T] | — (Trump's single TL hook is a β-hook) |
| tilted flush column on the wall + floor upright (instance 2) | not a hook of §3.1; sq0's carrier is the floor upright's neighbour sq10 | yes | floor-10⁻³ left wall (3.99075), LOCKED 4/4 |

The count on one wall therefore closes for the two same-kind pairs and fails for the mixed pair and for the
tilted-column wall. A proof of LOCK-FREE⁺(< 4) must couple
the walls: in instance 1 the unlocked squares are TL sq4 (an X-type upright beside the slot square, pressed by
nobody from the right), TR sq7 (wedged between sq6 and the top wall, W-unheld), and — exactly — BL sq1; in
instance 2 they are the right wall's two nicks, whose pressers act at the wrong end (PUSH-LINE). In both, the
locked wall is paid for on the opposite wall, where a second flush column or a corner-column upright cannot be
pressed toward its corner. The statement that would finish, in this language [C]: *at side < 4 the eight
carriers/pressers cannot all satisfy PUSH-LINE — some corner's presser is forced to the far end of its square by
the columns of the adjacent walls.* The four-corner count that expresses it is not in this file.

## 4. The routes of the brief, disposed

1. **Wall lemma (route 1):** exact form = LINE + PUSH-LINE (§1.4, §2.1) for the position of the far-side pusher, and
   the hook formulas of §3 for the count. It closes for α–α (Theorem HOOK-α) and fails for the mixed and the β–β
   pairs; two exact instances (§2.2). WALL-3's footprint budget is not what decides: the record's bottom wall
   carries only 2.11 of footprint (two carriers at 1/cos 18.93°; the nicks have y_min ≥ 0.985 > 1/√2 and footprint
   0), and the constraint that bites is the carriers' vertex geometry (D and 1/cos θ), not the chord sum. The tilted
   width cos θ + sin θ is not used anywhere (WALL-NP).
2. **FLOAT / CLUSTER (route 2):** the pushers of the nicks are not floating in either instance (sq10 sits on sq0,
   sq6 on sq3; sq4 on sq0), and the carriers' own pushers are the carriers of the other hook (flush) — no pocket
   to price. FLOAT is silent.
3. **Two adjacent walls (route 3):** not side-free (§2.3); not closed below 4.

## 5. [M] The LOCKED census (`attempts/A105-lockfree/code/lockw105.py`, 3 s; `results/lockw105.{json,jsonl}`)

For every intruder of the 12 strictly K0-BLOCKED packings and Trump (A103's loader): (R) lock103's strict LP; (W)
the weak-row translation LP of Lemma ROT-W with finite-motion confirmation and the room along the direction; (C) the
cone certificate (PUSHED with Σλ = 1, else WEDGED with Σμ = 1).

| packing | side | held R / 8 | W-held / 8 | LOCKED / 8 | walls both blocked & LOCKED | unlocked (corner sq: R / W) |
|---|---|---|---|---|---|---|
| floor 1e-2 | 4.0004572 | 4 | 5 | 4 | — | BL sq0 RW, BR sq3 RW, TR sq7 RW, TR sq6 R |
| floor 1e-3 | 3.9907485 | 6 | 8 | 6 | **left** | BR sq3 R (rot), TR sq6 R (screw) |
| floor 1e-4 | 4.0000044 | 2 | 2 | 2 | — | six, all RW |
| floor 1e-6 | 4.0000000 | 3 | 3 | 3 | — | five, all RW |
| record_s0115 | 3.9854837 | 7 | 5 | 5 | — (bottom, right held-R only) | BL sq1 W (wedge), TR sq7 W (wedge), TL sq4 RW |
| polish12 | 4.0000001 | 6 | 5 | 5 | bottom | TR sq6 W, TR sq7 RW, TL sq4 RW |
| polish15 | 4.0000041 | 4 | 4 | 4 | — | BL sq0, sq1, TR sq7, TL sq4: RW |
| polish21 | 4.0000075 | 4 | 5 | 4 | — | BL sq0 RW, BR sq2 R, TR sq6 RW, TR sq7 RW |
| polish24 | 4.0000119 | 2 | 4 | 2 | — | six |
| anchored0 | 4.1071074 | 7 | 8 | 7 | **right, top** | BL sq1 R |
| anchored1 | 4.0837355 | 7 | 8 | 7 | **bottom, right** | TL sq4 R |
| anchored2 | 4.0837359 | 7 | 7 | 7 | **bottom, right** | TL sq4 RW |
| **Trump** | 3.8770836 | **5 / 5** | **5 / 5** | **5 / 5** | — (K0-FREE) | none; all PUSHED |

Readings. (i) No packing is LOCKED at all eight; every packing has an unlocked SECOND meeter (as A103 found for
held). (ii) ROT-W adds 9 unlocked squares beyond ROT (the wedges: record sq1/sq7, polish12 TR sq6, floor-1e-2 BL sq0
…), and ROT adds squares ROT-W misses (the rotation drains: floor-1e-3 sq3/sq6, polish21 BR sq2, anchored0/1) —
the two locks are independent in vivo. (iii) Fully locked walls exist at every side on disk: one below 4 (instance
2), and pairs of adjacent ones at 4.08–4.11. (iv) Trump: five PUSHED certificates (e.g. TL sq4: μ = 0.129 on sq6's
corner, 0.699 on sq7, λ = (0.45, 0.55) on its two argmin endpoints; TL sq6: μ on sq4, sq9 ×2, top wall) — nothing
in this file fires at Trump.

## 6. Canaries

* **Trump** (K0-FREE, only TL blocked): LOCKED 5/5, all PUSHED [M]. Its TL crowd is a β-hook of §3.1 in TL's frame
  (N = sq4 = [0, 1] × [2.0326, 3.0326] hugging the left wall, nick ε = 0.155475; carrier sq6 at tilt 40.1819° touching
  the top wall, N's corner (1, 3.0326) on sq6's steep edge; presser sq7 at N's far corner (1, 2.0326)): the
  formulas give d^β = 0.168321 = sq6's depth and v_x^β = 1.595678 = sq6's top-wall vertex, exact to the digits
  shown [M]. Lemma HOOK-N: sq4 held and pushed (μ = 0.129, 0.699 on sq6, sq7; λ = (0.45, 0.55)) ✓. Theorems HOOK-α/β
  and Proposition HOOK-βα need TWO hooks on one wall; Trump has one, on a wall (left / top) whose other corner is a
  slot square: nothing fires, as the brief demands (the wall statement of §2.2 is about two blocked corners). PASS.
* **The 4 × 4 grid at 4 + ε:** Theorem HOOK-α excludes only walls with two α-hooks, i.e. m ≤ 4 with positive nicks;
  the shell's equality case IS the grid at m = 4 (tangent corners, §3.5) and the blocked grids of A102/A103 (nicks by
  JAM-0 dips, tilts 10⁻⁴–3°) are outside the hook family; lockw105 confirms polish12's bottom wall LOCKED 4/4 at
  4.0000001. Not excluded. PASS.
* **The drained records:** 3.98548 — lockmap103 marks TL sq4 (translation, exits); here TL sq4 fails R and W, and
  ROT-W additionally names BL sq1 and TR sq7 (wedges, W-unheld with the finite slide confirmed, retraction < 1:
  sq1 stops on sq9 after 2.1 · 10⁻⁷ — A102's obstruction); the fully held wall is the hook wall (bottom), as §3
  predicts, and the unlocked squares are on the other three walls. 3.99075 — lockmap103 marks BR sq3 (rotation) and
  TR sq6 (screw); here exactly those two, both W-held, both failing PUSH-LINE / its mirror (§2.1); the locked wall
  is the left wall (tilted flush column). Both agree with lockmap103, and the extra ROT-W failures are consistent
  with A102's drain of the record (it drains to k = 7). PASS.

## 7. Lean shape (against `noroom.md` §8)

* `wheld (z : Cfg) (i : Fin 11) (c : Fin 4) : Prop` := the Farkas certificate over the FORCE parts of the active
  rows: `∃ μ ≥ 0, Σ μ_k n_k = −e` per branch; `rotw_lemma : IsMinOn Ψ (packings m) z → Intrudes z i c → wheld z i c`,
  proved from Fact A (rows affine in centres — `ring_nf`-checkable on the polynomial rows of `CaseSat.lean`), the
  weak feasibility of z + t(v, 0), and ROT-GRAD's ω = 0 rate; no second-order term.
* `locked z i c := held z i c ∧ wheld z i c`; the axiom that would finish: `lockfree_plus : ∀ m < 4, ∀ z, CfgPacking m
  z → K0Blocked m z → ∃ i c, Intrudes z i c ∧ ¬ locked z i c`, consumed exactly as `lockfree` in `noroom.md` §8.
* Lemma LINE is bookkeeping on wrenches (a wrench with F ≠ 0 is F along the line {p × F = τ}); Theorem HOOK-α's
  closed-form inequalities are `nlinarith` targets in (sin θ, cos θ, ε) after the case split on the D breakpoint;
  Φ ≥ 2 in general needs the [S] calculus first.

## 8. Obligations ledger

| # | item | status |
|---|---|---|
| A105-O1 | Lemma ROT-W (weak translation lock at the Ψ^(w)-minimiser; Farkas force-cone form); LOCKED; Conjecture LOCK-FREE⁺(< 4) as the exact consumer statement | [T] §1.2–1.3 |
| A105-O2 | Lemma LINE (held & pushed = corner-ward resultant along a line through the argmin set); NO-TIP; PUSH-LINE (the far-side pusher's position, the brief's clause made exact) | [T] §1.4, §2.1 |
| A105-O3 | the one-wall statement is FALSE: `record_s0115` bottom wall (held 4/4 at the 10⁻⁷ bar), floor-10⁻³ left wall (LOCKED 4/4, side 3.99075) | [M] §2.2, `results/lockw105.jsonl`, drawing `results/hookwall105.svg` |
| A105-O4 | the hook family: kinds α/β with exact positions and depths (Trump's TL = a β-hook to 6 digits); Lemma HOOK-N; Theorem HOOK-α (m ≥ 4 + ε₁ + ε₂ for two α-hooks on a wall; Φ ≥ 2) and HOOK-β (m ≥ 4 + tan θ (ε₁ + ε₂)); Proposition HOOK-βα (mixed flush pair at 2 + f(θ) + …, f ≥ 1.934 — fits below 4, record = the instance to 6 decimals); Lemma HOOK-W (the β carrier needs a third contact); the α-shell m(θ) = 2(1+s)(1+c)/(s+c) ≥ 4 | [T] §3 (Φ ≥ 2 general: [M] grid + [S]) |
| A105-O5 | LOCKED census: 0/12 fully locked, locked walls listed, Trump 5/5 PUSHED | [M] §5 |
| A105-G1 | **LOCK-FREE⁺(< 4) (hence LOCK-FREE(< 4), DRAIN(W))** | **OPEN** — m range proved: none; one-wall route refuted, two-wall route not side-free and not closed; the four-corner PUSH-LINE count named [C] §3.6 |
| A105-O6 | canaries (Trump, grid, both records) | [M] §6 PASS |
| A105-O7 | Lean shapes | note §7, no `lean/` edits |

Runs (`attempts/A105-lockfree/code/`, one process each, BLAS pinned, seconds): `lockw105.py` → `results/lockw105.{json,
jsonl}`, `logs/lockw105.log`; `hook105.py` → `results/hook105.json`, `results/hookwall105.svg` (three panels: the two
one-wall instances with contacts, the α-shell at 18.93°; every drawn packing geometry-checked: containment and
pairwise SAT ≥ −7 · 10⁻¹⁶ for the shell, the records from A87's exact poses). A104 has no report on disk (BRIEF
only). No A57/A60/A61/A96/A104 file or process touched; A103's loader copied, not imported; frozen verifiers untouched.
