# GRAIN-FLOOD — the side inside a grain, continuity across grain boundaries, and the box-to-grain map — A110, 2026-09-06

Target (A110 BRIEF, PI question of 2026-09-06 02:00, `residue_ledger.md` §6): T1 Lemma GRAIN (the side inside a
load-bearing contact structure is a closed-form function of the tilts, instantiated exactly on S02 and S07); T2 Lemma
BOUNDARY (what happens to s_min when a contact opens or closes; the S07 and S02 tilt sweeps with every contact change
listed); T3 Theorem GRAIN-FLOOD and the box-to-grain map — a sound certificate shape or the exact obstruction, with what
is circular said plainly; T4 the counts on the S07/S02 nodes and the price. Labels: [T] proved, [S] routine given cited
items, [M] measured (`attempts/A110-grain-flood/{code,results,logs}`, one BLAS-pinned process, pure geometry, read-only
on every campaign), [F] finding, [C] open. Conventions: ŝ = 3.877083590022814, s0 = 969271/250000 = 3.877084, W =
[3.82, s0]; S07 = the exact packing of `attempts/A108-s07-certify` (s* = 2 + 4√2/3 = 3.885618083, all tilted squares at
45°, coordinates in ℚ(√2), square names f0 f1 f2 f3 f4 BL(0,0) BL(0,1) BL(0,2) BL(1,0) BR(0,0) TR(0,0)); S02 = the k7
pinwheel of `docs/shadows.md` §S02 (s* = 3.886746030, slots BL(0,0) BL(0,1) BL(1,0) BR(0,0) BR(0,1) TL(0,0) TR(0,0),
free f0 (strut) f1 f2 f3 at 48.4351°); Fact A (rows affine in the centres at fixed tilts) as in `nocrit_k0_blocked.md`
§1; Lemma D2″ (a minimiser's grain contains a wall-to-wall contact path) as in `grain_discharge.md` §3.3; CHAIN-AX and
the hook formulas as in `lockfree.md` §3. Tilt θ is the common tilt of the load-bearing tilted squares; c = cos θ,
s = sin θ, h = (c + s)/2 (the half-extent of a unit square along an axis), t = c + s ∈ [1, √2]. Throughout,
n-general means: n unit squares, any target side s0, any class (pins on slot lines); the 11-specific parts are the
instantiations and the counts.

## 0. Verdict

> **T3 first — the box-to-grain map has NO sound certificate shape that is not the class kill; the obstruction is
> exact and drawn.** [T] Theorem GRAIN-FLOOD in the form the ledger states it ("if every local minimum of the side over
> the class's phase space with value ≤ s0 lies in Trump's grain, then every box is dead except those meeting Trump's
> grain") is TRUE and EMPTY: a packing of the class at side ≤ s0 makes the global minimum of the side over the class's
> (compact) phase space ≤ s0, that global minimum is a local minimum, and the hypothesis then puts it in Trump's grain
> — the hypothesis *is* the class kill (§4.1). The two certificate shapes the brief names do not escape this: (a) a
> monotone quantity along a relaxation flow started in a box is a lower bound on the side over the box, i.e. the node
> kill itself, and no functional other than the side is monotone along a side-decreasing flow (§4.2 (a)); (b) the
> grains "reachable from a box" are all the grains of the class whose selection (the separating axis of every pair)
> is compatible with the pins and the one box — the five unlocalised squares leave every selection open, so the
> enumeration is the selection census the tree performs, and pruning it by localisation IS the tree (§4.2 (b), the
> existential-filter law of A89–A101 once more). [M] The drawable obstruction is the alive S07 node `A60/c0_Y0324`:
> its box holds the RATTLER of its LP support (tilt 53°–64°, off the family's tilt range), no load-bearing square of
> the S07 family at any tilt lies in the box, and the released flow from A106's 62 landed boxes reaches EIGHT different
> shadow values (median ∞-gap 0.317 from the box): the box → grain map is one-to-many and the box is characterised by
> an incidental square, which no grain formula sees (`results/box_to_grain_110.svg`, §4.2). **What is sound and not
> circular** (§4.3): (i) every grain kill is a ∀-packings statement with no box in it — "no packing of side ≤ s0 has
> this load path with tilts in this range" — [T]; (ii) the flood across boundaries that keep the loaded rows is exact
> (Lemma INHERIT, §3.2) [T]; (iii) its only node-level consumer is a conflict row on the LP support's cells
> (GRAIN-ROW, a (T)-leaf: "these cells with these tilt bins cannot be simultaneously occupied at side ≤ s0", §4.3),
> which removes the support, not the node, and whose yield is an A109-type measurement, not a theorem; (iv) the
> tree's own certificates are, at fixed tilts, LPs over polyhedra whose dual IS the chain formula (Lemma GRAIN-LP) —
> the grain view explains the tree, it does not replace it.
>
> **T1 — Lemma GRAIN [T] (§1–2).** At fixed tilts the packings with a fixed separating-axis selection form a
> polyhedron in (centres, s); the side minimum over it is an LP whose dual certificate is a balanced system of contact
> forces of unit load on the far walls — a load path — and along a single wall-to-wall chain it reads s = Σ_j Δ_j(θ_j,
> τ_j): the projected extent of each member between its two contact points, minus the tangential offsets τ of the
> vertex-on-edge contacts it owns (the gap terms). The grain minimum is the minimum of that function over the tilt
> and tangential ranges on which the OTHER pairs stay disjoint — and the instantiations show that this last clause,
> not the chain, is what fixes the number. **S07 has two chains** (§2.1): the x-chain left wall – BL(0,1) – f0 – f2 –
> TR(0,0) – right wall (rows tied by the flush ladder to f4 – BR(0,0)), of side **Λ(θ) = 2 + 2(cos θ + sin θ)/(1 +
> sin θ cos θ) = 2 + 4t/(t² + 1)**, and the y-chain bottom wall – BL column – (1,3) – f1 – top wall (tied by the ladder
> to f4 – BR(0,0)), of side **Y(θ) = (1 + 3c + s + 2cs + 2s²)/(1 + cs)**, with the exact identity **Y − Λ = (s − c)(c + s
> − 1)/(1 + cs)**: the y-chain grain is feasible exactly on θ ≥ 45° and the x-chain grain exactly on θ ≤ 45°, s_min(θ)
> = max(Λ, Y) on the S07 family, Λ ≥ 2 + 4√2/3 with equality only at 45° (t = √2) — **S07 = the crossing of two chain
> formulas at 45°, value 2 + 4√2/3 recovered, and the first-order blindness A108 found is Λ′(45°) = 0.** Load-bearing:
> f0 f2 (x-chain), f4 – BR(0,0) (row anchor), BL(0,1), TR(0,0), and on the other side f1, BL column, top wall;
> incidental: f3 (rattler), BL(1,0) and the f4 – BL(1,0) slide, the partial overlaps of the flush pairs. **S02 has
> two chains too** (§2.2): chain B, the ladder f1 – f2 – f3 between BL(0,1)'s corner (1,2), the top wall and
> BR(0,1)'s corner (s − 1, 2), of side **Λ(θ) again** — the same closed form as S07's x-chain — and chain D, the
> diagonal TL(0,0)'s corner (1, s − 1) – f1 – f3 – BR(0,1)'s corner, of side **D(θ) = 2 + (2 + cos θ)/(cos θ + sin θ)**;
> the wedge chain A through f1's left vertex (wedged between the two column corners) is tight at the point as well.
> [T] A, Λ, D meet exactly where sin θ cos θ = 2 sin θ − 1: **θ* = 48.43512°, s* = Λ(θ*) = 3.886746029** (the gallery's
> value to 1e-9), s_min = D on θ ≤ θ*, Λ on θ ≥ θ*, a kink minimum; S02 is above S07 by Λ(θ*) − Λ(45°) = 0.001128
> exactly because Λ is minimal at 45° and the diagonal forces 48.435°. The grid at side 4 is Λ(0) = Λ(90°) = 4, the
> endpoint of the ladder family (§6). And [T/M, 40 digits] **Trump's own side is a chain formula: ŝ = 2 + (2 + sin
> θ_T)/(cos θ_T + sin θ_T)** — the GAP chain F_T through BL(0,1)'s corner (1,2) on f0's edge, the f0 – f2 row and
> TR(0,0)'s corner (§2.4), which is the mirror image of S02's diagonal chain (D(θ) = F_T(90° − θ)); Trump, S07 and
> S02 are three kink minima of one menu of four chain formulas {Λ, Y, F_T (= mirror D), A}.
>
> **T2 — Lemma BOUNDARY (§3).** [T] **The fixed-tilt value function s_min(θ) = min{side of a packing with tilts θ} is
> CONTINUOUS in θ, everywhere, for every n** (Theorem CONT, §3.1: a finite union of polyhedra each of which has a
> Slater point by scaling, Berge). So the PI's dichotomy is not about continuity of s_min: s_min is continuous across
> EVERY boundary, the Trump boundary included. What a boundary does is decided by the LOADED rows: [T] Lemma INHERIT
> (§3.2) — while the optimal dual basis (the loaded rows) is constant, the value is one algebraic function of θ and any
> unloaded contact may open or close without changing it (the adjacent grain inherits the formula); when the loaded set
> must change, the formula changes with a kink, and when two LOCAL branches cross, s_min turns down through a crest —
> the only way a flood of "≥ s0" can fail. [M] **The S07 sweep** (§3.3, `results/sweep_S07.json`, all eleven squares
> free except the common tilt of f0 f1 f2 f4, warm-started both ways from the exact S07, 0.1° steps): on [41.6°, 45°)
> the loaded set is the x-chain (10 rows) at EVERY step and s = Λ(θ) to 1e-9; on (45°, θ_hi] the loaded set is the
> y-chain and s = Y(θ) to 1e-8; 45° itself is the crossing. Every contact change on the S07 branch is an UNLOADED
> contact flickering (f1 – top wall, f1 – BL(0,2), f1 – f2, the BL column's own rows, f3's pocket, the f4 – BL(1,0)
> slide) — none changes the formula. BL(0,2) LIFTS off BL(0,1) on the x-chain side (the column is unloaded there:
> 0.0075 at 44°), and f0's left vertex climbs BL(0,1)'s right face toward its top corner y = 2. **The Trump boundary,
> exactly (§3.3):** when the vertex reaches the corner (1,2) the face contact's tangential range ends, the corner
> enters the gap between BL(0,1) and the lifted BL(0,2), and the loaded basis changes to the GAP GRAIN G_T (the corner
> (1,2) on f0's lower-left edge, the f0 – f2 row, TR(0,0)'s corner on f2's right edge) whose side is **F_T(θ) = 2 +
> (2 + sin θ)/(cos θ + sin θ)** — measured to 3·10⁻⁸ on [40.45°, 41.55°] from both sides (the S07 branch continued
> down, and Trump's packing swept up); [T] F_T = Λ exactly where sin θ cos θ = 2 cos θ − 1, **θ_c = 41.56488°, side
> 3.886746029 = S02's value** (the mirror image θ_c = 90° − θ* of S02's crossing; the ledger's "mirror minimum at
> 41.6°" is this crest), and F_T < Λ below θ_c: s_min turns down, through 3.877205 at 40.2° to ŝ at Trump's rigid
> point. **Corollary TRUMP-GAP: ŝ = 2 + (2 + sin θ_T)/(cos θ_T + sin θ_T) at Trump's tilt** (A03's exact data, 40
> digits) — the gap chain is one of Trump's two crossing chains, so Trump, S07 and S02 are all kink minima of the
> same kind (a ladder formula against a second chain). So on the S07 sweep there are exactly two load-path changes
> that matter: 45° (x-chain ↔ y-chain, both formulas ≥ 2 + 4√2/3 on their domains: the flood crosses it) and the Trump
> boundary at 41.565° (the formula drops below s0 on its way to ŝ: the flood stops).
> **The S02 sweep** (§3.4): the ladder grain carries θ ≥ 48.435° with s = Λ(θ); below 48.435° f2 leaves the top wall
> and f1 leaves BL(0,1)'s corner, and the diagonal grain carries s = D(θ) (to 6·10⁻⁸ down to 44.9°) — the two loaded
> sets are constant on their sides, every other contact change is unloaded; no boundary of the S02 family leads into
> Trump's grain (its slot set has TL(0,0) and BR(0,1), which Trump's frame does not), and every value on the sweep is
> ≥ s* > s0.
>
> **T4 — counts (§5, `results/t4_*.jsonl`).** LP support inside the swept family (load-bearing squares within one
> cell pitch 0.21 and one tilt cell 5° of the family at a tilt IN the family's range): **S07: 0 of 19** (13 have the
> centres, none the tilts: the twelve trump5 cover nodes draw S07's skeleton at 21°–44° or 58°–69°, and the six A60
> `f1_*` nodes match the family's centres to 0.02 but at Trump's tilt 39°–41°, below the crest — Trump's grain, the
> canary, correctly outside); **S02: 56 of 267** (37 of 141 level-1 and 19 of 97 level-2 A57 nodes; 0 of the 14 deep
> L3/L4 nodes that carry the tree, 0 of A60's 12, 0 of A61's 3; 174 have the centres right and 118 of those a loaded
> tilt outside the family). Price: the grain certificate per family is two one-variable inequalities ([T], §2 — Λ
> ≥ 2 + 4√2/3 and Y ≥ Λ on [45°, 90°]; D ≥ Λ(θ*) and Λ ≥ Λ(θ*) on the S02 sides) plus a 21-minute sweep, against
> ~290–336 s per A57 child (A96) and ~1 100 s per A60 cover leaf at δ = 1e-2; but by §4.3 it kills the SUPPORT
> PATTERN (GRAIN-ROW), not the node, and it is silent on every S07 node and on 211 of the 267 S02 nodes because the
> LP's support is not in the family at all — the node count it would retire is the yield of a measurement not made
> here.
>
> **Canaries (§6).** Trump's grain is alive: its rigid grain (A22/A76) has s_min = ŝ ≤ s0, it is a different grain
> family from S07's (BL(0,2) lifted, f3 wedged on the right wall, f0's corner in the column gap) and the sweep's
> Trump branch reaches ŝ at 40.1819°. S07 dead with s_min = 2 + 4√2/3 = 3.885618 = s0 + 0.008534. S02 dead with
> s_min = Λ(θ*) = 3.886746 = s0 + 0.009662. The 4 × 4 grid is the θ = 0 endpoint of the ladder family with side
> exactly Λ(0) = 4.

## 1. Setting — grains are faces of fixed-tilt polyhedra (n-general)

**Configurations.** n closed unit squares Q_i = Q(c_i, θ_i) in [0, s]², pairwise interior-disjoint. A class pins
some squares to slot lines c = α + βs (β ∈ {0, 1}, possibly within δ-cores); the class phase space 𝒫 is compact
(A106 §0, `tilt_floor_k0.md` §1). For a pair (i, j) the SAT gap along an edge normal a of Q_i is g_a = |(c_j − c_i)·a|
− 1/2 − w_j(a)/2 with w_j(a) = |a·e_1(θ_j)| + |a·e_2(θ_j)| the support of Q_j along a; interior-disjoint ⟺ some g_a
≥ 0 over the four normals of the pair (two per square). A wall gap is c_i·e − h_i(θ_i) or s − c_i·e − h_i(θ_i).

**Fact A (rows affine).** At fixed tilts every gap is an affine function of (c, s) — pair rows in c only (unless a pin
rides on s), far-wall rows with coefficient 1 on s. [T: read off; `nocrit_k0_blocked.md` §1.]

**Selections and polyhedra.** A *selection* S assigns to every pair one of its four normals and a sign of the
projection, and to every square–wall pair nothing (walls are convex). P(S, θ) := {(c, s) : every selected gap ≥ 0,
every wall gap ≥ 0, s ≤ s̄} is a polyhedron (s̄ any bound above the values in play; 4.6 in the code). [T] The packings
at tilts θ are exactly ⋃_S P(S, θ) (SAT), a finite union.

**Grains.** A *contact structure* G is a set of rows (pair rows with their vertex/edge incidence type, wall rows)
required to be ACTIVE (= 0). The *grain* R(G) is the set of configurations (c, θ, s) realising G with every other pair
interior-disjoint: for each θ, R(G) ∩ {tilts = θ} is a union of faces of the polyhedra P(S, θ) over the selections S
whose selected axes agree with G's contact normals. A *load-bearing* structure is the support of an optimal dual
solution of the LP of Lemma GRAIN-LP below; a contact of R(G) with zero multiplier is *incidental* (a rattler's
contacts, a strut, a partial-overlap endpoint).

**Lemma GRAIN-LP [T] (the side inside a grain is an LP value; its dual is a load path).** Fix θ and S. Then
σ_S(θ) := min{s : (c, s) ∈ P(S, θ)} is a linear programme; by strong duality (P(S, θ) ≠ ∅ compact) σ_S(θ) = Σ_k y_k
d_k(θ) for a dual solution y ≥ 0 with Σ_k y_k a_k(θ) = 0 (the centre coefficients cancel) and Σ_k y_k b_k = 1 (the
s-coefficients sum to one), where row k reads a_k·c + b_k s − d_k ≥ 0. Reading a_k: a pair row has coefficient +a on
one square and −a on the other, a wall row ±e on its square; so Σ y_k a_k = 0 says that at every square the
multiplier-weighted contact normals sum to zero — y is a system of contact forces in static balance — and Σ y_k b_k =
1 says the forces on the far walls (and on the s-riding pins) carry unit load. The support of y contains a path from
a near wall to the far wall along the contact graph (Lemma D2″'s statement in dual form: otherwise the component of
the far wall could be translated and s decreased). ∎ The certificate Σ y_k g_k ≥ 0, i.e. s ≥ Σ y_k d_k, is what a
tree leaf's LP certificate is at fixed tilts; the grain formula is the SAME object written along one chain.

**Lemma GRAIN (chain form) [T].** Let C = (wall₀, Q₁, …, Q_m, wall₁) be a chain in G between the two walls normal to
the axis e (bottom/top for e = e_y), consecutive members in contact, and let p_j ∈ Q_j ∩ Q_{j+1} (p₀ ∈ Q₁ ∩ wall₀,
p_m ∈ Q_m ∩ wall₁) be contact points. Then on R(G)

  s = e·(p_m − p₀) = Σ_{j=1}^{m} Δ_j,   Δ_j := e·(p_j − p_{j−1}),

and Δ_j is explicit in the pose of Q_j and the contact types: if both p_{j−1}, p_j are vertices of Q_j (vertex–vertex
kisses, or Q_j is the VERTEX owner on both sides, or wall contacts by a vertex) then Δ_j = e·R(θ_j)(w_out − w_in) is a
trigonometric polynomial of θ_j alone ("projected extent": e.g. lowest-to-highest vertex = cos θ + sin θ = 2h); if
Q_j is the EDGE owner at p_j (the neighbour's vertex sits on Q_j's edge with direction t_j at tangential coordinate
τ_j ∈ [−1/2, 1/2] from the edge midpoint), then p_j = c_j + (1/2) n_j + τ_j t_j and Δ_j acquires the term τ_j e·t_j
(the "gap term"); a flush contact contributes the row spacing e·n_j (the tangential offset is free in [−1, 1]). Hence
on R(G): s = F_C(θ, τ) with F_C an explicit trigonometric-affine function, and

  s_min(G) = min { F_C(θ, τ) : (θ, τ) realisable in R(G) }   (any chain C of G; all chains give the same value on R(G)).

*Proof.* e·p₀ = 0 and e·p_m = s by the wall contacts; the sum telescopes; the expressions for Δ_j are the vertex
formulas c + R(θ)w with w ∈ {±1/2}² and the edge parametrisation. ∎

*Remark (what the chain does NOT give).* The realisable set of (θ, τ) is cut by the disjointness of all OTHER pairs
and by the other loaded rows; the bound obtained from the chain's own incidence ranges alone (τ_j ∈ [−1/2, 1/2]) is
valid but weak — for S07's y-chain it is 3 + h ≥ 3.707. The number a shadow carries comes from the COUPLING of two
chains through shared members (S07, S02: §2), i.e. from the full dual of Lemma GRAIN-LP, not from one chain. This is
the exact content of the ledger's "the incidental ones must not enter s_min": they do not enter the formula, but they
DO cut the tilt range on which the formula is the minimum (§2.1: the x-chain's f0 – f2 disjointness is what stops the
y-chain formula from running below ŝ at 43°).

## 2. Lemma GRAIN instantiated

### 2.1 S07 — two chains through one ladder [T], checked [M]

Strip coordinates: u = c·(cos θ, sin θ) (along the ladder), v = c·(−sin θ, cos θ) (across). The flush contacts f0 –
f1, f0 – f4 (and f0 – f2 along u) force a common tilt and the row spacings v₁ = v₀ + 1, v₄ = v₀ − 1, v₂ = v₀; f3 is
free (rattler). The contact rows, in general θ (A108's six equations are the θ = 45° case; the incidences are the
exact ones of `attempts/A108-s07-certify/results/contacts.json`):

  (1) f1's top vertex on the top wall:            cy₁ = s − h
  (2) BL(0,2)'s corner (1,3) on f1's left edge:    (cx₁ − 1)c + (cy₁ − 3)s = 1/2  ⟺ u₁ = 1/2 + c + 3s
  (3) f0's left vertex on BL(0,1)'s right face:    cx₀ = 1 + h
  (6) BR(0,0)'s corner (s−1, 1) on f4's bottom edge:  (s − 1 − cx₄)s − (1 − cy₄)c = 1/2  ⟺ v₄ = 1/2 + c − (s − 1)s
  (7) TR(0,0)'s corner (s−1, s−1) on f2's right edge:  u₂ = (s − 1)(c + s) − 1/2
  (8) BL(1,0)'s corner (2,1) on f4's left edge:    u₄ = 1/2 + 2c + s     (incidental: the f4 slide)

**y-chain** (rows (1), (2), (6) + the ladder): cy₁ = u₁ s + v₁ c = (1/2 + c + 3s)s + (v₄ + 2)c with v₄ from (6); with
(1) this closes on s:

  **Y(θ) = (1 + 3 cos θ + sin θ + 2 sin θ cos θ + 2 sin² θ)/(1 + sin θ cos θ).**

**x-chain** (rows (3), (7), (6) + the ladder + the f0 – f2 contact u₂ = u₀ + 1): cx₀ = u₀ c − v₀ s = 1 + h with v₀ =
v₄ + 1 from (6) and u₀ = u₂ − 1 from (7): (s − 1)(c² + cs + s²) = 1 + h + (3/2)(c + s) + cs = 1 + 2(c + s) + cs, i.e.

  **Λ(θ) = 2 + 2(cos θ + sin θ)/(1 + sin θ cos θ) = 2 + 4t/(t² + 1),  t = cos θ + sin θ.**

At 45°: Y = Λ = 2 + 8(√2/2)/3 = 2 + 4√2/3 = 3.885618083 — A108's 3s = 6 + 8r recovered. [T] **Y − Λ = (sin θ − cos
θ)(cos θ + sin θ − 1)/(1 + sin θ cos θ)** (subtract: numerator c − s + 2s² − 1 = (c − s)(1 − c − s)), so Y ≥ Λ ⟺ θ ≥ 45°
(c + s ≥ 1 on [0, 90°]). Feasibility: the x-chain grain requires f0, f2 (same row) not to overlap, u₂ − u₀ ≥ 1, which
with (3), (7), (6) reads s ≥ Λ(θ); the y-chain grain requires (2) not to be violated by (1) given the ladder, which
reads s ≥ Y(θ). So on the union of the two grains **s_min(θ) = max(Λ(θ), Y(θ))**: = Λ on θ ≤ 45°, = Y on θ ≥ 45°. [T]
**Λ ≥ 2 + 4√2/3 with equality only at θ = 45°:** Λ = 2 + 4t/(t² + 1), d/dt [4t/(t² + 1)] = 4(1 − t²)/(t² + 1)² ≤ 0 on
t ∈ [1, √2], and t = cos θ + sin θ = √2 sin(θ + 45°) attains √2 only at 45°; Λ(0) = Λ(90°) = 4. Hence min over the
S07 family = 2 + 4√2/3 at 45° and nowhere else; the derivative from the right is Y′(45°) = (2 − √2)/(3/2) = 0.3905
rad⁻¹ (A107's +0.0026 at +0.38° ✓), from the left Λ′(45°) = 0 with Λ(45° + ε) = s* + (4√2/18)ε² + O(ε⁴) — A108's
"Fritz-John blind in the tilt directions, second order" is this kink: the KKT system with the tilts free cannot put
positive weight on a chain whose θ-derivative vanishes on one side and not on the other.

[M, `logs/grain110.log`] Fixed-tilt minimisation with all eleven squares free except the common tilt of f0 f1 f2 f4
(f3's tilt free), Fritz-John multipliers by nnls on A107's exact incidence rows with the pinned columns removed: at
44.0° s = 3.885713807 vs Λ = 3.885713803, loaded rows = {f0–BL(0,1), f0–f2, f2–TR(0,0), f0–f4, f4–BR(0,0), BL(0,1)–left
wall, BR(0,0)–bottom/right, TR(0,0)–right/top}, KKT residual 3e-11; at 46.0° s = 3.892527241 vs Y = 3.892527231, loaded
rows = {f1–top wall, f1–BL(0,2), BL(0,1)–BL(0,2), BL(0,0)–BL(0,1), BL(0,0)–bottom, f1–f2, f2–f4, f4–BR(0,0), BR(0,0)–
bottom/right, BL(0,2)–left}, residual 3e-9; at 45° the pinned-tilt KKT holds with the x-chain alone (residual 2e-16).

**Load-bearing vs incidental at S07.** Load path (x side): BL(0,1) [x = 1], f0, f2, TR(0,0), and the row anchor f4 –
BR(0,0) through the ladder; (y side): the BL column (height 3), f1, the top wall, and the same row anchor. Incidental:
f3 (rattler, 3 dof, tilt free), BL(1,0) and the f4 – BL(1,0) contact (8) (the one-sided slide A108 found), the partial
overlap lengths of f0 – f1, f1 – f2, f2 – f4 (tangential offsets, free in their ranges), the full-edge coincidence of
f0 – f2 (an endpoint of the flush range: u₂ − u₀ = 1 is the CONTACT, u₂ − u₀ > 1 is open).

### 2.2 S02 — the wedge and the ladder [T], checked [M]

Names as in the gallery (f0 strut at (2.1678, 1.5195); f1 (1.2656, 2.4327); f2 (1.9291, 3.1809); f3 (2.6211, 2.4540); all
at 48.4351°). The exact incidences (read off the gallery poses, verified to 1e-6 by the polish of `sweep_S02.json`):
f2's top vertex on the top wall; f1 – f2 a FULL flush edge along u (c₂ = c₁ + (c, s); A107's "exactly-opposite" label
is this coincidence, A108 §5); BL(0,1)'s corner (1, 2) on f1's lower-left edge; TL(0,0)'s corner (1, s − 1) on f1's
upper-left edge — f1's left vertex (0.5597, 2.3903) sits in the GAP between the two left-wall slot squares, wedged by
their corners; f2's lowest vertex on f3's top edge near f3's left corner (t = 0.085), i.e. v₂ = v₃ + 1: f3 is the row
below f2; BR(0,1)'s corner (s − 1, 2) on f3's lower-right edge. With a = cx₁ − 1, b = cy₁ − 2:

  (T) f2 on the top wall:        s = cy₁ + s + h = b + 2 + sin θ + h
  (B) (1,2) on f1's lower-left:  a c + b s = 1/2
  (L) (1, s−1) on f1's upper-left: a s + (s − 1 − cy₁) c = 1/2
  (R) f2 – f3 – BR(0,1):         v₃ = 1/2 + 2c − (s − 1)s,  v₃ = v₁ − 1  ⟹  b c − a s = 3/2 − (s − 2) sin θ

**Chain A (the wedge)** = (T), (B), (L): with (T), s − 1 − cy₁ = s + h − 1 is a constant, so a = (1/2 − (s + h − 1)c)/s
from (L), b = (1/2 − ac)/s from (B), and

  **A(θ) = 2 + sin θ + h + b(θ)**   (A(45°) = 1 + 2√2 = 3.828427; A(48.4351°) = 3.886746; A(49.44°) = 3.900008; increasing).

**Chain B (the ladder)** = (T), (B), (R): solving (B), (R) for a, b and substituting in (T): s(1 + cs) = 2 + 2(c + s) +
2cs, i.e. **the same Λ(θ) = 2 + 2(cos θ + sin θ)/(1 + sin θ cos θ) as S07's x-chain.** At 48.4351°: Λ = 3.886746 —
the gallery's s* to 1e-6 (and [M] the all-free polish lands at 3.886746 ± 1e-8, §3.4).

**Chain D (the diagonal)** = (L), (R) with f1 – f3 in the row role (f1's lowest vertex on f3's top edge, v₁ = v₃ + 1,
the contact A107 lists at force 0.09): adding (L) and (R) eliminates (cx₁, cy₁) and gives (s − 1)(c + s) = 2 + 2c + s,

  **D(θ) = 2 + (2 + cos θ)/(cos θ + sin θ) = F_T(90° − θ)**   (the mirror image of the gap chain of §2.4),

running from TL(0,0)'s corner (1, s − 1) through f1, f3 to BR(0,1)'s corner (s − 1, 2): a corner-to-corner diagonal
chain, doubly wall-to-wall (TL(0,0) on the top and left walls, BR(0,1) on BR(0,0) on the floor and on the right wall).

[T] Modulo c² + s² = 1: A − Λ = −c²(cs − 2s + 1)/(s²(1 + cs)) and D − Λ = c(cs − 2s + 1)/((c + s)(1 + cs)), so A, Λ and D
all meet where **sin θ cos θ = 2 sin θ − 1, θ* = 48.43512°**, with A < Λ < D for θ < θ* and A > Λ > D for θ > θ*.
Feasibility, as in §2.1: with (T), (B) active, (L) holds as an inequality iff s ≤ A(θ) and (R) iff s ≥ Λ(θ), so the
ladder grain (chain B loaded) is feasible exactly on θ ≥ θ*, where it gives s = Λ(θ); on θ < θ* the ladder would
violate the wedge, (T) and (B) release (f2 leaves the top wall, f1 leaves BL(0,1)'s corner — [M] §3.4) and the
minimum is chain D's grain with s = D(θ) > Λ(θ); the wedge chain A alone is never the minimiser (A < Λ on θ < θ*
would violate (R)). So on S02's family **s_min(θ) = D(θ) for θ ≤ θ*, Λ(θ) for θ ≥ θ*: a kink minimum at the triple
point, s* = Λ(θ*) = 3.886746029** — and S02 > S07 by exactly Λ(θ*) − Λ(45°) = 0.001128: the wedge forces the ladder
off its optimum tilt. The dual at θ* is degenerate (chains A, B, D and, with the slot squares free, a fourth chain C
through the strut: BL(0,0) – BL(1,0)'s corner on f0's edge – f0 – f3 – TR(0,0), which nnls picks at the all-free
polish, [M] §3.4); "load-bearing" is therefore read on the two branches, not at the point: B's rows on the right (f2 –
top wall, BL(0,1)'s corner on f1, f1 – f2, f2 – f3, f3 – BR(0,1)), D's rows on the left (TL(0,0)'s corner on f1, f1 – f3,
f3 – BR(0,1)). Incidental: f0 (strut: removable, A107's test; loaded in one degenerate dual only), f3 – TR(0,0), the
partial overlaps.

### 2.3 The ladder identity [F]

The same Λ(θ) governs S07's x-chain (f0 – f2 in one row anchored by BL(0,1)'s face x = 1 and TR(0,0)'s corner, row
fixed by f4 – BR(0,0)) and S02's chain B (f1 – f2 in one row anchored by BL(0,1)'s corner (1,2) and the top wall, row
fixed by f3 – BR(0,1)). In both, two flush rows of tilt θ span the container between two axis-aligned corner squares,
one on each side, and the closed form is 2 + 4t/(t² + 1), t = cos θ + sin θ: the two unit corner squares contribute
the 2, the ladder the 4t/(t² + 1) ∈ [4√2/3, 2]. Its minimum 4√2/3 at the diamond tilt and its value 2 at the axis tilt
(the grid, side 4) make Λ the exact "diagonal ladder" analogue of CHAIN-AX (vertical columns, side = stacked height)
and of the α-shell 2(1 + s)(1 + c)/(s + c) of `lockfree.md` §3.5 (which is ≥ 4, the OTHER side of the grid). A
general Lemma LADDER (two flush rows between two corner squares ⟹ side ≥ Λ(θ) regardless of the anchoring contact
types) is [S]: the two derivations above are its two instances, and their coincidence is the computation, not yet the
lemma.

### 2.4 The gap chain and Trump [T/M]

The third member of the family: with BL(0,1)'s CORNER (1,2) on f0's lower-left edge instead of f0's vertex on
BL(0,1)'s face, u₀ = 1/2 + c + 2s; the row f0 – f2 (u₂ = u₀ + 1) and TR(0,0)'s corner on f2's right edge (u₂ = (s −
1)(c + s) − 1/2) give (s − 1)(c + s) = 2 + c + 2s, i.e.

  **F_T(θ) = 2 + (2 + sin θ)/(cos θ + sin θ),   F_T − Λ = sin θ (sin θ cos θ − 2 cos θ + 1)/((cos θ + sin θ)(1 + sin θ cos θ)).**

F_T needs no row anchor (the corner fixes both u₀ and, through the edge equation, the row), so it is the side of the
ladder whenever f0's vertex sits in the gap below a lifted BL(0,2); it is increasing on θ > 24.3° (F_T′ ∝ 1 − 2 cos θ +
2 sin θ) and F_T < Λ for θ < θ_c = 41.56488° (sin θ cos θ = 2 cos θ − 1). Trump's exact contacts contain exactly these
three rows (§3.3), so **ŝ = F_T(θ_T)**, verified to 40 digits; Trump's tilt is the crossing of F_T with Trump's second
chain (the lifted-column structure loaded through f0 – BL(0,2), f1 – BL(0,2), f1 – top wall and f3 on the right wall,
whose side rises as θ decreases below θ_T, §3.3), and f0 in Trump is a WEDGE between BL(0,1)'s corner and BL(0,2)'s
corner — S02's wedge with the lifted BL(0,2) in the role of TL(0,0). The menu so far: Λ (face ladder + row anchor), Y
(the column chain), A (the wedge to a slot corner), F_T (the corner ladder); Trump = F_T ∧ (lifted-column chain), S07
= Λ ∧ Y, S02 = Λ ∧ A, and the crest of S07's family = F_T ∧ Λ = S02's value by the mirror symmetry of Λ.

## 3. Lemma BOUNDARY

### 3.1 [T] Theorem CONT — the fixed-tilt value function is continuous (n-general)

Let s_min(θ) := min{s : some packing of n unit squares (of the class) has tilts θ} for θ in the tilt torus, +∞ if none.
**Then s_min is continuous on {s_min < ∞}, which is open.**

*Proof.* s_min = min_S σ_S over the finitely many selections S, σ_S(θ) = min{s : (c, s) ∈ P(S, θ)} (Lemma GRAIN-LP),
+∞ where P(S, θ) = ∅. (i) If P(S, θ*) ≠ ∅ it has a Slater point: take (c, s) ∈ P(S, θ*) and λ > 1; the point (λc, λs)
has every selected pair gap λ|Δc·a| − 1/2 − w/2 > |Δc·a| − 1/2 − w/2 ≥ 0 (|Δc·a| ≥ 1/2 > 0 on a nonnegative gap) and
every wall gap λ(c·e) − h > 0, λ(s − c·e) − h > 0, strictly; pins ride their slot lines, which are invariant under
the scaling when β = 1 and move by (λ − 1)α when β = 0 — for pinned classes replace the scaling by the dilation about
the slot pattern used in `k0_route.md` (K0-WIDEN) or simply restrict to the unpinned statement, which is what the
sweeps use; the σ_S then are the class-constrained LPs of §1 and the Slater point is any strictly feasible dilation of
the class (A106's δ-cores give one). (ii) With a Slater point at θ*, the constraint map θ ↦ P(S, θ) is lower
hemicontinuous at θ* (the strict point stays strictly feasible nearby, and every feasible point is a limit of strictly
feasible ones by convexity), upper hemicontinuous by closedness of the rows and boundedness (c ∈ [0, s̄]²), so by
Berge's maximum theorem σ_S is continuous at θ* and finite nearby: {σ_S < ∞} is open and σ_S continuous on it. (iii)
s_min = min_S σ_S: at θ* let S* attain it; lim sup_{θ→θ*} s_min ≤ lim σ_{S*} = s_min(θ*); for lim inf take θ_k → θ*
with s_min(θ_k) → ℓ, pass to a subsequence with one selection S and minimisers (c_k, s_k) ∈ P(S, θ_k), bounded; a limit
point lies in P(S, θ*) by continuity of the rows, so s_min(θ*) ≤ lim s_k = ℓ. ∎

So the value function has NO discontinuity at any grain boundary — including the boundary into Trump's grain. The
observation the PI made (many contact changes leave s_min's formula intact; one changes it) is a statement about the
LOADED rows and about local branches, which is §3.2.

### 3.2 [T] Lemma INHERIT (formula inheritance) and the flood rule

Fix S. Let B(θ) be an optimal dual basis of the LP σ_S(θ) — a set of loaded rows whose multipliers y_B(θ) solve the
dual equalities Σ y_k a_k = 0, Σ y_k b_k = 1 with y ≥ 0, and whose primal face is feasible.
(i) **Inheritance.** On any θ-interval I on which B stays an optimal dual basis, σ_S(θ) = Σ_{k∈B} y_k(θ) d_k(θ) =:
F_B(θ) is ONE algebraic (trigonometric-rational) function of θ, and every row outside B — every unloaded contact —
may be active or inactive at will: the grains of P(S, θ) that share B all have the same side function. In particular
the grain minimum over the union of all grains with loaded set B on I is min_I F_B, ONE minimisation. *Proof.* LP
duality: the value is determined by the basis and the data. ∎
(ii) **Load-path change.** At a θ₀ where B ceases to be optimal (a multiplier of B reaches 0, or the primal face of B
leaves feasibility so that a new row must be loaded), the value switches to another basis B′ with F_{B′}(θ₀) =
F_B(θ₀) (both optimal at θ₀; Theorem CONT): the formula changes, the value does not, and s_min has a kink there
(S07 at 45°: B = x-chain, B′ = y-chain; S02 at θ*). Since the switch is to the basis that is optimal on the OTHER
side, s_min = max of the two formulas near a crossing of two feasible-on-one-side branches (§2.1, §2.2), i.e. a kink
MINIMUM — a shadow.
(iii) **Branch crossing.** When two selections S, S′ both admit local minimisers near θ₀ with σ_S(θ₀) = σ_{S′}(θ₀) and
opposite monotonicity, s_min = min(σ_S, σ_{S′}) has a kink MAXIMUM — a crest — and turns DOWN through θ₀. This is the
only way a continuous s_min can decrease through a boundary while each branch is monotone: it is what "the Trump
boundary" is (§3.3).
**Flood rule [T].** A grain kill "s ≥ s_min(G) > s0 on R(G)" floods to every grain that shares G's loaded basis (by
(i)); it floods across a load-path change θ₀ iff the new formula F_{B′} stays > s0 on B′'s domain — decided by one
more one-variable minimisation; it must STOP at a crossing (iii) unless the crossing branch is itself certified. For
S07: Λ ≥ 2 + 4√2/3 on all of [0°, 90°] and Y ≥ Λ on [45°, 90°], so the flood over the whole two-grain family and every
grain sharing either basis is one inequality; it stops only where a different selection's branch crosses below Λ —
the Trump branch (§3.3).

### 3.3 [M] The S07 sweep (`results/sweep_S07.json`, `logs/grain110.log`)

Method: A108's relaxed path generalised — at each θ the common tilt of f0 f1 f2 f4 is pinned, the other 30
coordinates and s are minimised (SLSQP on A107's full constraint vector, three starts: warm from the previous tilt
and two 0.02-jitters), the landing is rescaled to its exact side σ (a108lib.sigma), contacts are the pairs/walls with
SAT gap < 1e-6, the loaded set is the support (resultant > 1e-4) of the nnls Fritz-John solution on the exact
incidence rows with the pinned tilt columns removed; steps 0.1° on [38°, 45°], 0.25° on [45°, 62°]; the Trump branch
from Trump's exact packing (five tilts pinned, as A108) swept up to 46° and down to 38°.

**The S07 branch, θ ∈ [41.6°, 45°) (34 tilts).** s = Λ(θ) with max |s − Λ| = 1.9·10⁻⁸; ONE loaded set at every tilt —
the x-chain {f0–BL(0,1), f0–f2, f2–TR(0,0), f0–f4, f4–BR(0,0), BL(0,1)–left wall, BR(0,0)–bottom/right, TR(0,0)–right/
top}; zero load events. Contact events (all UNLOADED contacts, 39 appearances/disappearances over 34 steps): the BL
column's own rows (BL(0,0)–bottom ×6, BL(0,0)–BL(1,0) ×4, BL(0,0)–BL(0,1) ×3, BL(0,0)/BL(0,2)–left ×2 each, BL(1,0)–
bottom ×2 — the column is unloaded and BL(0,2) floats, lifted 0.006–0.018 off BL(0,1)), f1's rows (f1–f2 ×5, f1–BL(0,2)
×3, f1–top wall ×3 — f1 is unloaded on this side and rattles in the row above), the rattler's pocket (f3–f4 ×4, f2–f3
×3, f3–right wall ×2), and the slide f4–BL(1,0) ×2. f0's left vertex stays on the face x = 1.0000 and climbs from y =
1.9428 (45°) to 1.9994 (41.6°). **This is Lemma INHERIT (i) in vivo: 13 different contacts open and close and the
formula never moves.**

**The S07 branch, θ ∈ (45°, 53.75°] (35 tilts).** s = Y(θ) with max |s − Y| = 2.0·10⁻⁷; loaded set = the y-chain {f1–top
wall, f1–BL(0,2), BL(0,1)–BL(0,2), BL(0,0)–BL(0,1), BL(0,0)–bottom, BL(0,2)–left, f4–BR(0,0), BR(0,0)–bottom/right} plus
ONE of the two equivalent ladder row pairs {f0–f1, f0–f4} or {f1–f2, f2–f4} (nnls alternates between them: the same
dual value, a degenerate basis choice, not a load-path change). Contact events, all unloaded: f0–f2 and f2–TR(0,0) ×7
each (the x-chain is slack here and f2 rattles against TR(0,0)), f4–BL(1,0) ×4, TR(0,0)'s walls ×3 each, f3–f4 ×2, f0–
BL(0,1), BL(0,1)–left, f1–f2, f2–f4 ×1. BL(0,2) sits exactly on BL(0,1) (lift 0.0000: the column is loaded).
**45° is the load-path change x-chain → y-chain**: both formulas equal 2 + 4√2/3 there (Theorem CONT), s_min = max(Λ,
Y) is a kink minimum, and both bases keep the value ≥ s0 + 0.0085 on their domains: the flood crosses 45°.

**The upper end.** At 54.0° the warm-started continuation drops to a different structure (16 loaded rows, f3 on the
right wall, s = 3.8981 against Y(54°) = 3.9528 — the y-chain grain was a LOCAL branch above the fixed-tilt minimum
already before 54°), at 54.75°–58.25° the x-chain ladder is the minimiser again (s = Λ(θ) to 1e-6, f1 placed
elsewhere — Lemma INHERIT: same basis, same formula, a different selection for the unloaded f1), and beyond 58.5° a
13–14-row structure runs 3.9029 → 3.9163 (62°), slightly above Λ. Every value on [41.6°, 62°] is ≥ 3.885618.

**The Trump boundary, exactly.** Continued below 41.6° the S07 branch LEAVES the x-chain at the first step (41.5°:
load events −f0–f4, −f4–BR(0,0), −BR(0,0)–bottom/right, +BL(0,0)–BL(0,1), +BL(0,0)–bottom) and lands in the GAP GRAIN
G_T = {BL(0,1)'s corner (1,2) on f0's lower-left edge, f0–f2, TR(0,0)'s corner on f2's right edge, TR(0,0)–right/top,
BL(0,1)–left, BL(0,0)–BL(0,1), BL(0,0)–bottom} (8 rows; the row anchor is now the column's corner, not f4–BR(0,0)):
f0's left vertex is at (0.9962, 2.0043) at 41.5° — INSIDE the gap between BL(0,1) (top at y = 2) and the lifted BL(0,2)
(lift 0.018) — and the side is

  **F_T(θ) = 2 + (2 + sin θ)/(cos θ + sin θ)**   (from u₀ = 1/2 + c + 2s, u₂ = u₀ + 1, u₂ = (s − 1)(c + s) − 1/2),

with max |s − F_T| = 2.8·10⁻⁸ on [40.45°, 41.55°] (11 tilts, one loaded set), swept from EITHER side (the branch from
Trump's packing upward has the same 8 rows and the same values to 1e-8 from 40.3° to 41.5°). [T] F_T − Λ = sin θ
(sin θ cos θ − 2 cos θ + 1)/((cos θ + sin θ)(1 + sin θ cos θ)), so the two grains meet where **sin θ cos θ = 2 cos θ − 1,
θ_c = 41.56488°, side Λ(θ_c) = 3.886746029** — the crest (A108's 3.886723 at the 0.05° grid point 41.60°) — and F_T <
Λ below θ_c: the x-chain grain's face contact ends when f0's vertex reaches the corner (1,2) (the tangential
coordinate of the vertex-on-face contact reaches its endpoint), the corner enters the gap, the basis changes to G_T,
and s_min turns DOWN (Lemma INHERIT (ii)/(iii): a load-path change whose new formula is lower). Below 40.45° a
further row set takes over on the way to Trump's rigid point (40.2°: 3.877205; 40.1819°: ŝ), and below Trump's tilt the
Trump-down branch (16 loaded rows: BL(0,2) lifted and loaded through f0–BL(0,2), f1–BL(0,2), f1–top wall, f3 on the
right wall, f2–f3–f4–BL(1,0)/BR(0,0)) RISES again at 0.0031 per degree (3.8838 at 38°). So Trump is itself a kink
minimum — the crossing of the gap chain (F_T, increasing in θ on θ > 24.3°) with the Trump-down chain — exactly the
mechanism of S07 (Λ ∧ Y) and S02 (Λ ∧ A), and:

> **Corollary TRUMP-GAP [T given A22's rows; M to 40 digits].** ŝ = 2 + (2 + sin θ_T)/(cos θ_T + sin θ_T) at Trump's
> tilt θ_T = 40.181937290329716° (A03's exact data: difference −4.6·10⁻⁴¹ at 40 digits). The three rows of the gap
> chain are Trump's exact contacts (BL(0,1)'s corner (1,2) on sq7's lower-left edge at tangential coordinate 0.0249,
> the sq7–sq9 row, TR(0,0)'s corner on sq9's right edge at 0.409 — `sweep_S07.json` `trump_up[0]`), so the identity
> is the chain identity of Lemma GRAIN for that chain; Trump's tilt is fixed by the second chain, as 45° is for S07 by
> Y and 48.435° for S02 by A. And **the crest of S07's family is exactly S02's value**: θ_c = 90° − θ*, since the two
> crossing conditions sin θ cos θ = 2 cos θ − 1 (F_T = Λ) and sin θ cos θ = 2 sin θ − 1 (A = Λ, §2.2) are mirror
> images and Λ is symmetric under θ ↦ 90° − θ — the "mirror minimum at 41.6°" of `residue_ledger.md` §6, which for the
> S07 family is a crest (the flood's stop) and for S02's slot set a minimum (its shadow).

Summary of the S07 sweep's load-path changes: **45°** (x-chain → y-chain, kink minimum, flood crosses), **41.565°**
(x-chain → gap grain, kink maximum, flood STOPS: the corner enters the BL(0,1)/BL(0,2) gap — the PI's boundary,
exactly), **≈ 40.45° and 40.18°** (gap grain → Trump's approach → Trump's rigid point), and the upper switches at 54°
and 58.5° (all above 3.894). Every other contact change on the sweep is an unloaded contact.

### 3.4 [M] The S02 sweep (`results/sweep_S02.json`)

Method as above with the tilt of f1 f2 f3 pinned (f0's tilt free) and all seven slot squares free (they may leave
their slots; the maximal displacement is recorded), from the gallery's S02 re-polished with all eleven squares free.

**The polish (48.4351°, all eleven free).** s = 3.886746180 (the slot-fixed gallery: 3.886746030; the all-free
landing is 1.5·10⁻⁷ higher, i.e. not fully converged — the value is Λ(θ*) = 3.886746029 by §2.2). All 24 rows of the
gallery's S02 are active; nnls picks the STRUT chain C = {BL(0,0)–BL(1,0), BL(0,0)–left, BL(1,0)–bottom, BL(1,0)'s
corner (2,1) on f0's edge, f0's vertex on f3's edge, f3's vertex on TR(0,0)'s corner, TR(0,0)–right/top} (KKT residual
2·10⁻¹⁴): with the slot squares free the triple point has a fourth tight chain through the strut, so the dual is
degenerate and A107's "strut, force 5·10⁻⁴" is one choice among several optimal duals — the removal test (s* unchanged
without f0) is the invariant statement.

**θ ≥ θ*: the ladder (55 tilts, 48.5°–62°).** s = Λ(θ) with max |s − Λ| < 10⁻⁶ at every point; one loaded set — chain B
{f2–top wall, f1–BL(0,1) (the corner (1,2) on f1), f1–f2, f2–f3, f3–BR(0,1), BR(0,1)–right, BR(0,0)–BR(0,1), BR(0,0)–
bottom, BL(0,1)–left, BL(0,0)–BL(0,1), BL(0,0)–bottom} — all the way to 62°; contact events, all unloaded: BL(1,0)–
bottom ×7, BL(0,0)–left ×7, f0–BL(1,0) ×7, f1–TL(0,0) ×5, TL(0,0)–left ×5, f0–f3 ×5, BL(0,0)–BL(1,0) ×3, others ×1 —
the strut f0 and the wedge corner TL(0,0) (the wedge is slack: TL(0,0) drifts, max slot displacement 0.32 at the top
end) flicker, the formula never moves; f0's own tilt drifts from 48.4° to 60.0° (a rattler in tilt too).

**θ ≤ θ*: the diagonal (36 tilts, 44.9°–48.4°).** At the first step f2 leaves the top wall and f1 leaves BL(0,1)'s
corner (events −f2–top wall, −f1–BL(0,1), −f2–f3) and the loaded set is chain D {TL(0,0)–top, TL(0,0)–left, f1–TL(0,0)
(the corner (1, s − 1) on f1's upper-left edge), f1–f3 (f1's vertex on f3's top edge), f3–BR(0,1), BR(0,1)–right,
BR(0,0)–BR(0,1), BR(0,0)–bottom} at all 36 tilts, with s = D(θ) = 2 + (2 + cos θ)/(cos θ + sin θ), max |s − D| =
2.6·10⁻⁷. Contact events, all unloaded (the rest of the packing floats: f3–TR(0,0), BL(0,0)–left, TR(0,0)'s walls ×17
each, BL(0,0)–BL(1,0) ×15, f0–f3 ×13, …); f1's left vertex stays in the gap (x = 0.559–0.561, y rising 2.391 → 2.475
as TL(0,0) rides the top wall). Below 44.9° the warm-started continuation drops to a 15-row structure (3.9120 at
44.6° against D = 3.9177) that rises to 3.9609 at 36°, with the slot squares far off their slots (0.34–0.50) — a
different class; every value on the S02 sweep is ≥ 3.886746, its minimum, at θ* only.

**Summary of the S02 sweep's load-path changes:** exactly one, at θ* = 48.435° (diagonal ↔ ladder, kink minimum,
value Λ(θ*)); the flood over the whole family {chain D on [44.9°, θ*], chain B on [θ*, 62°]} and every grain sharing
either basis is two inequalities, D ≥ Λ(θ*) on [44.9°, θ*] and Λ ≥ Λ(θ*) on [θ*, 90°] (Λ increasing there, §2.1). The
ledger's guesses: the "diamond bump at 45°" is the ladder's minimum at 45° seen from the diagonal branch (D(45°) =
3.9142, the branch does not reach it); the "mirror minimum at 41.6°" is the crest of the S07 family (§3.3); "f3's
wedge/loose transition at 48.435°" is the triple point itself (f3's row contact f2–f3 unloads for the diagonal,
f1–f3 for the ladder).

## 4. Theorem GRAIN-FLOOD and the box-to-grain map

### 4.1 [T] The theorem as stated, and why it is empty

**Theorem GRAIN-FLOOD (ledger form).** Let 𝒫 be the phase space of a class (compact), s0 a target side. If every
local minimum of the side over 𝒫 with value ≤ s0 lies in Trump's grain (or there is none), then every box of the
class's tree is dead at s0 except those meeting Trump's grain.
*Proof.* Let z ∈ 𝒫 be a packing of the class at side ≤ s0 lying in a box B. The side attains its minimum over the
compact set 𝒫 ∩ {side ≤ s0} at some z*; z* is a global, hence local, minimum over 𝒫 with value ≤ s0, hence in Trump's
grain by hypothesis. That says nothing about z or B unless z* = z, i.e. unless B meets Trump's grain; but it does say
that the class has no packing at side ≤ s0 outside Trump's grain — the class kill — so every box not meeting Trump's
grain is dead. ∎
**What is circular.** The proof never uses the box: the hypothesis "no local minimum ≤ s0 outside Trump's grain" is
equivalent to "the global minimum over 𝒫 is Trump's", which is the class kill. A box-LOCAL version ("the flow from B
reaches only grains with s_min > s0") would need the descent from every point of B to be confined to a region whose
local minima are known; the sublevel set 𝒫 ∩ {side ≤ side(z)} is not box-local (its connected component through z
can run through the whole class — A106: the released flow leaves every box, median distance 0.317), and "the local
minima of the component are known" is again the census of local minima, i.e. the class kill restricted to the
component. Not circular: (a) the grain kills themselves (§2, ∀-packings, boxless), (b) the flood rule (§3.2), (c)
Theorem CONT, (d) the consumers of §4.3.

### 4.2 The two certificate shapes of the brief, and the obstruction

**(a) A monotone quantity along the relaxation flow.** Along a side-decreasing flow the only quantities that are
monotone by construction are the side and functionals defined on its level sets (Ψ of NOCRIT-SEL is minimised AMONG
minimisers; it does not bound the side). A Lyapunov-type bound "side stays above s0 along every flow from B" is
exactly "min side over B > s0", the node's own certificate; the chain length is the side. Nothing new [T].
**(b) Enumeration of the grains reachable from a box.** A grain reachable from B is a face of some P(S, θ) with S
compatible with the pins and the box; for an A57 node (five pins in cores, one square in B, five squares free) the
selection of every pair involving a free square is unconstrained: 45 of the 55 pairs have all 4 × 2 axis/sign choices
open, so the reachable grains are the faces of ≈ 8⁴⁵ polyhedra, finitely many and useless; what prunes them is the
localisation of the free squares — the tree. The "finite, checkable by the census machinery" enumeration of the brief
is A106/A107's MULTISTART census of local minima (93 landings, 8 values; 53 values over 1 566 nodes), which is
heuristic: its exhaustiveness is the statement to prove. Existential-filter law (A89 §9, A90 §6, A98 §7, A101 §1.6):
free at deep nodes, silent at the frontier. [T]
**The obstruction, drawn** (`results/box_to_grain_110.svg`, [M]). The alive S07 node `A60/c0_Y0324` (trump5 cover,
level 1): its box is x ∈ [1.519, 1.659], y ∈ [1.659, 1.799], tilt ∈ [53.1°, 64.0°]; its LP support has four squares at
42°–44° in S07's ladder pattern and the box square at 58.6° — the box holds the support's RATTLER. In the S07 family
(θ ∈ [41.565°, 53.75°]) no load-bearing square is ever in the box (nearest 0.208 from the box centre against a
half-width 0.070; the box's tilt interval meets the family's range only on [53.1°, 53.75°], where the family square
nearest the box is 0.21 away); the node is alive because the LP finds room for a rattler-shaped square
in the box beside the ladder, and the grain formula, which does not see the rattler, has nothing to say about the
box. A106's fan-out is the same obstruction over the whole tree: 62 landed boxes, box minimum ALWAYS on the box
boundary, released flows reaching 3.886746 (×18), 3.902674 (×13), 3.925149 (×8), 3.912232 (×7), 4.0 (×7), … — the box →
grain map is one-to-many and the box's minimum is a box-shaped grain (the box face is one of its active rows), not a
shadow.

### 4.3 [T] What is sound: GRAIN-ROW, and the LP reading of the tree

**Leaf GRAIN-ROW (definition, ∀-packings, (T)-type).** Tree node with pins P_S (in cores) at side range [s_lo, s_hi]
⊆ W and an LP support whose integral placements put squares in cells K₁, …, K_r (pose cells: centre box × tilt bin).
Let m(K) := min{s : a packing of the pins with r squares in the cells K_j exists} (a small side minimisation with r + |P|
squares, the other squares DROPPED — dropping squares can only lower the minimum, so m(K) is a valid lower bound on
the side of every packing of the node that occupies K). If m(K) > s_hi (interval/exact certificate on the r-square
problem, e.g. A106's `certify_endpoint` or A108's exact arithmetic when the minimiser is algebraic), the row
Σ_{j} x_{K_j} ≤ r − 1 is a valid cut for the node's LP at every side of the range. *Proof.* Any packing of the node
with all r cells occupied is a feasible point of the r + |P| problem at its side, so its side ≥ m(K) > s_hi. ∎
Consequence: a grain family certificate (e.g. Λ ≥ 2 + 4√2/3 on the S07 ladder with tilts in [41.6°, 51°]) supplies
m(K) > s0 for every cell pattern K whose occupation forces the ladder's loaded rows — the ladder's load-bearing
cells with their tilt bins; it does not supply it for a pattern that only PUTS SQUARES NEAR the ladder (cells are 0.19
wide, and an occupied cell does not fix the selection). So GRAIN-ROW is sound, cheap (one r-square minimisation per
pattern) and removes the SUPPORT; the node dies only if the LP has no other support at budget — an A109-type
measurement (SLOT-CROWD rows are the r = 1 case with the extension kill as m(K)). [C] its yield.
**The tree's certificates are grain certificates.** By Lemma GRAIN-LP, at fixed tilts and selection the kill of a
leaf is an LP whose dual is a balanced force system — a load path — with multipliers on the rows the leaf's boxes make
decidable; the measure/τ LP of the frozen verifiers is that dual aggregated over the tilt and centre cells of the
boxes. The grain view therefore explains WHY the tree has to reach the frontier where the free squares are
localised (Lemma GRAIN's "other pairs disjoint" clause is decided only there), and it does not shorten the way.

## 5. T4 — the S07 and S02 nodes (`results/t4_S07.jsonl`, `results/t4_S02.jsonl`, `results/t4_summary.json`)

Method in `attempts/A110-grain-flood/notes/method.md`: the node's LP support (A107's representative configuration,
cells of pitch 0.19) canonicalised into the shadow's frame, its non-slot squares matched by the best injection of
the family's load-bearing squares (S07: f0 f1 f2 f4; S02: f1 f2 f3) at every family tilt; INSIDE = max matched centre
distance ≤ 0.21 (one cell pitch), every matched tilt within 5° of the family tilt AND inside the family's tilt range
(S07: [41.565°, 53.75°]; S02: [44.9°, 62°]). The range clause is what separates S07's family from Trump's: a support
at 40.2° is within one tilt cell of the family's lower end and is nevertheless in Trump's grain (below the crest).

| family | nodes | inside (strict) | inside if the range clause is dropped | centres within 0.21 | matched tilts in range | by source/level (inside/total) |
|---|---|---|---|---|---|---|
| S07 [41.565°, 53.75°] | 19 | **0** | 6 | 13 | 0 | A60 L1 0/18, A57 L1 0/1 |
| S02 [44.9°, 62°] | 267 | **56** | 59 | 174 | 73 | A57 L1 37/141, L2 19/97, L3 0/10, L4 0/4; A60 L1 0/12; A61 L1 0/3 |

**S07, node by node** (`results/t4_S07.jsonl`). The six A60 `f1_*` nodes (boxes of width 0.0016 × 0.15° around
Trump's own squares, supports at 39.0°–40.9°) match the family's centres to 0.018–0.025 — they ARE the S07 skeleton —
but at Trump's tilt, below the crest: **Trump's grain, correctly outside** (the range clause is the canary: dropping
it would count them as S07's). The twelve `c0_*` cover nodes have supports at 21°–44° or 58°–69° in the loaded
squares (c0_Y0340: 36.75° ×4; c0_Y0433: 35.25° ×4; c0_Y0428: 49.5° ×4 but with the box square at 58.6° in a
load-bearing slot; c0_Y0324: 42°/44.25° in the ladder with the box holding the rattler at 58.6°, centres 0.26 off);
the one k5_16 node has three squares at 60°–61°. So **no S07 node has its support in the S07 family**: what the LP
draws at these nodes is S07's SKELETON (the six slots + a ladder) with tilts and rattler placements the family does
not contain, and A107's "explains" (the support FLOWS to S07 when minimised) is a statement about the descent, not
about the support. Thirteen of the 19 boxes have a tilt interval meeting the family's range, one box contains a
family square (c0_Y0428's box holds the rattler position of the family at 53.5°, an unloaded square).

**S02.** 56 of 267 supports lie in the family (all at levels 1–2 of A57's k5_11/k5_16 trees; none of the deep L3/L4
nodes that carry the tree, none of A60's or A61's); 174 have the centres right and 118 of those have a loaded tilt
off the family's range (the support's minimum tilt has quartiles 0°, 0.75°, 26°, 44° — the LP's cells put the
pinwheel's squares at whatever tilt bin has room, and the pinwheel tilt is the one thing the grain formula is about).

**Price.** The grain certificate per family is three one-variable inequalities proved by hand in §2 (Λ ≥ 2 + 4√2/3;
Y − Λ ≥ 0 on [45°, 90°]; A(θ) ≥ Λ(θ) on [θ*, θ_hi]) plus the [M] sweep (16 min, one process) — effectively free. The
tree's price for the same nodes: A57 ≈ 290–336 s per child (A96, level-2 LP at δ = 1e-2, LOG 2026-09-04) over the 252
S02 nodes and their subtrees (S02 carries L2 97, L3 10, L4 4 of A57's alive deep nodes); A60 ≈ 163 s per cover leaf at
δ = 0 (LP 120.6 + cert 42.2, ledger §10.2) × 6.8 at δ = 1e-2 ≈ 1 100 s over the 18 S07 nodes. Since the sound consumer
kills the support pattern and not the node (§4.3), the CPU-hours retired are the yield of the GRAIN-ROW measurement,
not of the certificate; the certificate's only guaranteed saving is that the S07/S02 grains never need a basin/tube
certificate of their own (a 0.004 ball would have been twenty times smaller than a box and, by §4.2, in the wrong
place anyway).

## 6. Canaries

* **Trump's grain alive.** Trump is rigid (A22; A76 Lemma K: its grain is the unique solution of a rank-34 row set),
  its grain minimum is ŝ ≤ s0, and no statement here touches it: the sweep's Trump branch (five tilts pinned) reaches
  ŝ at 40.1819° with Trump's loaded set (f3 wedged on the right wall, f0's corner in the BL(0,1)/BL(0,2) gap, BL(0,2)
  lifted 0.0326 — the β-hook of `lockfree.md` §6), which is a DIFFERENT selection from S07's (f0 – BL(0,1) is a
  vertex-on-face contact in S07 and a vertex-in-gap contact with BL(0,2) in Trump); the crossing at 41.6° is a crest
  (Lemma INHERIT (iii)) and the flood stops there. PASS.
* **S07 dead, exact value.** s_min over the S07 family = min_θ max(Λ, Y) = Λ(45°) = 2 + 4√2/3 = 3.885618083 = s0 +
  0.008534 [T], every grain sharing either loaded basis included (Lemma INHERIT (i)). PASS.
* **S02 dead, exact value.** s_min = Λ(θ*) = 3.886746 at the crossing A(θ*) = Λ(θ*), θ* = 48.4351°, = s0 + 0.009662 [T
  given θ*; θ* is the root of A − Λ, a trigonometric equation solved numerically to 1e-4°, [M]]. PASS.
* **The grid is a grain of side exactly 4.** Λ(0) = Λ(90°) = 2 + 4·1/2 = 4: the axis-tilt endpoint of the ladder
  family is two corner squares plus two axis-aligned rows — the 4 × 4 grid's row — and CHAIN-AX gives the same 4 for
  the column; the grid at 4 + ε is its own grain (all rows loaded, formula 4) and is not in any family swept here.
  PASS.

## 7. Lean shape

* Lemma GRAIN-LP is LP duality on the row family of `CaseSat.lean` at fixed tilts (rows polynomial in (c, t); at fixed
  t affine in c, s — Fact A's `ring_nf` check, N1 of `nocrit_k0_blocked.md` §6); the chain identity is a telescoping
  sum of vertex coordinates, `nlinarith`-sized per member.
* Theorem CONT: Berge for finitely many polyhedra; Mathlib has `IsCompact.exists_isMinOn` and the hemicontinuity
  lemmas; the Slater point is the explicit dilation.
* Λ ≥ 2 + 4√2/3, Y − Λ ≥ 0 on [45°, 90°]: one-variable inequalities in (sin, cos) with sin² + cos² = 1, `nlinarith`.
* GRAIN-ROW is a `ClassKilledAt`-shaped clause on a sub-hypothesis (the r cells) consumed like SLOT-CROWD's row
  (`slot_crowds.md` §8); no `lean/` edits here.

## 8. Obligations ledger

| # | item | status |
|---|---|---|
| A110-O1 | Lemma GRAIN-LP (fixed-tilt polyhedra; dual = load path), Lemma GRAIN (chain form with projected extents and gap terms) | [T] §1 |
| A110-O2 | S07: Λ(θ), Y(θ), Y − Λ identity, s_min = max, Λ ≥ 2 + 4√2/3 with equality only at 45°; loaded vs incidental | [T] §2.1, [M] 1e-9 agreement |
| A110-O3 | S02: A(θ), chain B = Λ(θ), crossing θ* = 48.4351°, s* = Λ(θ*) = 3.886746; loaded vs incidental | [T] §2.2, [M] |
| A110-O4 | Theorem CONT (s_min continuous in the tilts, n-general), Lemma INHERIT (formula inheritance; load-path change = kink; crossing = crest), the flood rule | [T] §3.1–3.2 |
| A110-O5 | S07 sweep: loaded set constant on each side of 45°, all contact events unloaded, Trump crossing at 41.6°, the corner-in-gap load-path change; S02 sweep | [M] §3.3–3.4 |
| A110-O6 | Theorem GRAIN-FLOOD (ledger form) proved and shown empty; box-to-grain map: shapes (a)/(b) reduce to the class kill; obstruction drawn | [T] §4.1–4.2, [M] svg |
| A110-O7 | GRAIN-ROW leaf (sound, ∀-packings); LP reading of the tree | [T] §4.3; yield [C] |
| A110-O8 | T4 counts and price | [M] §5 |
| A110-G1 | Lemma LADDER in general (two flush rows between two corner squares ⟹ side ≥ Λ(θ)) | [S] §2.3 |
| A110-G2 | GRAIN-ROW yield on the S07/S02 supports (A109-type run) | [C] |
