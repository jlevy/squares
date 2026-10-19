# POCKET WASTE — TILT-MIN, the JAGGED census of a ring's centre pocket, and POCKET-CAP: what closes, what does not — A237, 2026-09-16

The PI (00:00): *"given the tilt requirements of the loaded ring, and that they have to have a fairly high angle to all
fit, the pocket is almost necessarily quite jagged — use the wastage census on grain boundaries to assert a minimum
wastage in the centre pocket, then show there isn't room for n − (ring)."*  This file (i) proves the exact two-meeter
tilt lemma of a doubly-met corner and says in which DIRECTION it binds, (ii) defines the pocket of a ring and proves a
rigorous, computable wastage census (the coverable-set sandwich, the sealed regions, the wedge bound, the piercing
certificate), (iii) states Theorem POCKET-CAP, computes it at n = 11 on the window and tabulates n = 5..60, and (iv) says
plainly what closes: specific pockets close by certificate (A226's ring family at S = 3.90; the window family ring(S, θ)
at every S ∈ [3.82, ŝ] and θ ≤ 30°: each holds ONE square, 8 + 1 = 9 < 11), the analytic bound does not (the waste is
O(tilt), no tilt floor exists).  Tags: [T] proved, [S] routine given cited items, [M] measured, [F] false (with the
witness), [C] obligation.  Sources: `ring_capacity.md` (A236: STABLE RING, NO-CLOSURE, POCKET(n)), `one_flush.md` (A226:
CROWD-ABOVE, ring11), `realign.md` (WALL-EXCESS, sealed pockets), `sideband.md` (Theorem B, B0/B0′, Cor. B1–B4),
`corner_seal.md` (SEAL, WEDGE), `wall_torque.md` (ONE-TILTED, TWO-CONTACT), `tilt_floor_k0.md` (A89: no loaded tilt floor,
Lemma JAM-0), `local_lock.md` (A233: CHAIN, the loaded component), `two_grains.md` (FLUSH, TILT-BAND depth).  Code
`attempts/A237-pocket-waste/code/` (`geom237.py`, `tiltmin237.py`, `pocket237.py`, `family237.py`, `summarise237.py`,
`pages237.py`, `test237.py`, `run237.sh`), results `results/pocket237.md` (+ `tiltmin237`, `pocket237`, `family237`,
`table237` `.jsonl`), pages `docs/residue_map/campaigns/A237-pocket-waste/{ring_pocket,n11_window}.svg`, Lean
`Statements/Open/PocketWaste.lean`.

## 0. Verdict

> **[T] Lemma TILT-MIN binds UPWARD, not downward** (§1).  A flat meeter touching its wall at offset δ ∈ (0, 1) and a
> tilted partner of tilt θ (frame: the flat meeter's wall is the floor; θ ∈ (0°, 90°) the angle of the edge leaving the
> partner's lowest vertex to the right) satisfy **sin θ ≤ δ**, and the partner's lowest point is at height
> ≥ 1 − (δ − sin θ) tan θ; both are sharp (mode (a) of Theorem B: the partner's leftmost vertex on the wall, its edge
> through the flat meeter's corner — clause (W) at ζ = θ).  So the deeper the flat meeter reaches (δ → 0) the SMALLER the
> partner's tilt must be; two nearly flush squares CAN both meet the box (CROWD-ABOVE: tilt ε/2 at offset ε).  **[T]
> DEPTH-BUDGET**: d_A + d_B ≤ 1 for a flat wall meeter and any partner (∞-depths, A233's d_c); [M] 774/774 doubly-met
> corners, max 0.90.  **[F] TILT-MIN as a LOWER bound θ ≥ θ_min for locked corners**: A89 (no loaded tilt floor by any
> local argument; its Lemma JAM-0 is this upper bound), and the 193 witnesses' tilts sit AT the tilt floor their generator
> imposed (30 of 32 HELD corners at t_min = 10°).  θ_min is a PARAMETER of the census, not a theorem.
>
> **[T] Lemma JAGGED** (§2): the pocket P of a member set U is the container minus the members' interiors; its coverable
> set is ∪_θ (C(θ) ⊕ Q_θ) (C(θ) the free centres at tilt θ); over a tilt bin of width Δ the kernel K = Q_mid / w(Δ/2)
> lies inside and the hull H = w(Δ/2) Q_mid outside every square of the bin, so coverable ⊆ ∪_bins (P ⊖ K) ⊕ H and
> **WASTE(P) := area(P) − area(that union) is a rigorous lower bound on the uncoverable area** (J1); a sealed region
> (no unit square fits) is waste (J2, `realign.md` §1.2); a convex pocket vertex of angle α ≤ 90° has an uncoverable
> sector of radius r(α) ≥ (1 + cos α + sin α)/(4 sin(α/2)) − 1/√2 (J3, Lemma WEDGE); and **PIERCE** (J4, Lean
> `capacity_le_of_pierce`): k points, one in the interior of every unit square inside P, bound the capacity by k —
> certified per bin by (P ⊖ K) ⊆ ∪_i (p_i + K).  **[F] "a unit square cannot approach a tilted edge closer than a
> tilt-dependent margin"**: a square parallel to the edge approaches at distance 0 along its whole length; the waste of a
> near-flush ring is O(ε) (its vertices are 90° ± ε, its slivers have area O(ε)) — the jaggedness is not where the
> closure lives.
>
> **[T]+[M] Theorem POCKET-CAP** (§3): a stable ring at side s < ⌈√n⌉ with loaded component U (p = |U|) is impossible if
> the capacity of its pocket is < n − p, in particular if area(coverable) < n − p or PIERCE(n − p − 1) holds.  **At n = 11
> by certificate**: A226's ring family at S = 3.90 (ε = 0.02, 0.05, 0.10) and at S = 3.95 / 3.99 with ε = 0.10 hold ONE
> square (PIERCE(1), residual 0 over 90 bins; 8 + 1 = 9 < 11), and the window family ring(S, θ) — flat meeters at the
> least offset sin θ + 0.02, partners at tilt θ, S ∈ {3.82, 3.85, ŝ}, θ = 1°..30° — holds ONE square at every member
> (PIERCE(1) at the centre, residual 0; the members with θ ≥ 35° are not packings).  **Analytically it does NOT close at
> n = 11**: the area form 4 w_c(θ_min) > ŝ² − 11 = 4.03 needs θ_min ≥ 32° (w_c(20°) = 0.689, w_c(45°) = 1.271) and no
> tilt floor exists; the n-general table (§3.3) closes at n = 5, 10, 11, 17, 19 only under tilt floors 17°–42° that
> nothing supplies, and at no n ≥ 18 otherwise (the slack s(n)² − n grows like 2√n·slack while the waste is 4 w_c ≤ 5.1).
> The closure of the n = 11 rings is the CENTRE (side s − 2 − δ < 2: one square by Lemma TWO) plus the stubs' width
> < 1 — a shape statement PIERCE certifies pocket by pocket, not a jaggedness count.  The ring `rand_0_0569|t20` at 4.11
> holds its two rattlers (waste 4.31 of 7.89, PIERCE(2) fails by 0.12: the rattlers slide); the records are sound (the area
> bound fires on none of 22, the interior squares sit in the coverable set).  **k0_00 unchanged**: LOCKED-CROWD-FREE(11) =
> POCKET(11) on [3.82, ŝ]; what A237 adds is a 0.1-second sound leaf test for any explicit ring's pocket (the PIERCE
> certificate) and the exact reason the analytic route stops (O(ε) waste, no floor).

## 1. Lemma TILT-MIN (any n) [T]

**Setting.**  Corner frame (u, v); the open box (0, 1)²; A, B interior-disjoint unit squares in the quadrant both meeting
the box (int ∩ (0, 1)² ≠ ∅).  ONE-TILTED (`wall_torque.md` §3): not both flat.  Suppose A is flat and touches a wall;
rotate the frame so that wall is the floor: A = [δ, 1 + δ] × [0, 1] with 0 < δ < 1 (δ = 0 is the pressed square, lonely by
Cor. B1; A meeting the box forces δ < 1).  B has tilt θ ∈ (0°, 90°), the angle of the edge leaving its lowest vertex
v = (x_v, y_v) to the right; its leftmost vertex is v + (−sin θ, cos θ), rightmost v + (cos θ, sin θ).  (θ and 90° − θ are
different squares here: the tilt is NOT folded to [0°, 45°].)

**1.1 Lemma TILT-MIN.**  (a) sin θ ≤ x_v ≤ δ; (b) y_v ≥ 1 − (δ − x_v) tan θ ≥ 1 − (δ − sin θ) tan θ; hence B's ∞-depth
d_B = 1 − min_B max(u, v) ≤ 1 − y_v ≤ (δ − sin θ) tan θ, and (c) DEPTH-BUDGET d_A + d_B ≤ 1 with d_A = 1 − δ.  Sharp:
for every θ with sin θ < δ the square with x_v = sin θ, y_v = 1 − (δ − sin θ) tan θ is in the quadrant, interior-disjoint
from A and meets the box (its vertex v has x_v < 1, y_v < 1).
*Proof.*  B ∩ int A = ∅ (a point of the closed square B inside the open set int A is a limit of interior points of B).
The slab part B ∩ {0 < y < 1} is convex, avoids int A = (δ, 1+δ) × (0, 1), and is not contained in {x ≥ 1 + δ} (B meets
the open box: a point with 0 < x, y < 1); so it lies in {x ≤ δ}.  B's lowest vertex has y_v < 1 (B meets the box) and
y_v ≥ 0, so v or the points just above it lie in that slab part: x_v ≤ δ.  The leftmost vertex has x = x_v − sin θ ≥ 0:
(a).  The edge from v in direction (cos θ, sin θ) stays in the slab until height 1; it cannot end below height 1 (then its
end x_v + cos θ ≤ δ and sin θ + cos θ ≤ δ < 1, absurd), so it reaches height 1 at x = x_v + (1 − y_v) cot θ ≤ δ: (b).
(c): d_B ≤ (δ − sin θ) tan θ ≤ δ ⟺ δ (tan θ − 1) ≤ sin θ tan θ, true for θ ≤ 45° (left side ≤ 0) and for θ > 45° since
δ < 1 ≤ sin²θ/(sin θ − cos θ) (⟺ sin θ (1 − sin θ) ≤ cos θ, true on (45°, 90°)).  Sharpness: direct.  ∎
The exact curve is Theorem B's clause (W) at ζ = θ: h_A(n_W(θ)) = cos θ − δ sin θ < cos θ − sin²θ ⟺ δ > sin θ
(`sideband.md` §3); mode (a) is its witness, and A89's Lemma JAM-0 (sin(tilt) ≤ g for an axis-aligned blocker at offset
g) is the same inequality.  Lean: prose ([T] here); obligation O-TILTMIN.

**1.2 What it says about locked corners.**  TILT-MIN bounds the tilt ABOVE by arcsin δ = arcsin(1 − d_A): the deeper the
flat meeter, the flatter its partner.  [F] as a lower bound: CROWD-ABOVE's crowds (`one_flush.md` §3.1) have δ = ε and
tilt ε/2 (sin(ε/2) < ε ✓), both meet the box, and they exist at every side above s(n) for eight n; on the window family of
§3 the ring at θ = 1° is a packing at S = 3.82 (its partners' depth 0.02 tan 1° = 3·10⁻⁴ is below `meets` tolerance,
so it is not counted as a four-crowd; at θ = 5° it is).  For LOCKED corners (both meeters loaded, PUSH/HOLD) no sharpening
exists by a local argument: `tilt_floor_k0.md` §0 (A89) — the near-flush jam is first-order consistent with criticality,
the two-square jam is exactly Lemma JAM-0 = TILT-MIN.  What stability adds is TWO-CONTACT (a loaded tilted wall meeter has
two more loaded contacts) — a holder count, not a tilt.  [M] The 193 four-crowds (`tiltmin237.md` §1): 774/774 corners
ONE-TILTED, 258/258 flat–tilted pairs satisfy (a) and (b) (slack arcsin δ − θ: min 1.26°, median 40.5°; every flat meeter
touches a wall), DEPTH-BUDGET 774/774 (max 0.9018, median 0.465); Trump's TL/TR crowd: δ = 0.8445, θ = 40.18° ≤
arcsin δ = 57.6°, depths 0.156 + 0.168 = 0.32.  The HELD witnesses' least meeter tilt is AT the generator's floor
t_min = 10° on 30 of 32 corners: their "fairly high angle" is an artefact of A217's tilt bound, not a consequence of the
lock.  [M] Random search (`test237.py`): no violation of (a), (b), (c) on 91 random flat–tilted pairs and 28 random
two-tilted pairs (DEPTH-BUDGET for two TILTED meeters is [M] only; obligation O-DEPTH2).

## 2. Lemma JAGGED (any n): the pocket and its census [T]

**2.1 The pocket.**  P a packing at side s, U ⊆ P a member set (A233's loaded component of the crowd: meeters, wall chains,
holders; every meeter in U).  POCKET(U) := [0, s]² ∖ ∪_{Q∈U} int Q — a closed polygon (with holes if U is not connected to
the walls), whose boundary consists of wall segments and members' edges; its VERTICES are container corners, member
vertices, member–wall and member–member contact points, with interior angle α; CONVEX (α < 180°: at a member vertex
pointing into the pocket the angle is 270° − reflex... concretely: between two edges of the same member 270° — reflex;
between a member edge and a wall at a wall contact 90° ± tilt; between two members in contact a convex angle equal to the
angle between their edges), REFLEX otherwise.  The other n − p squares of P are unit squares inside POCKET(U), pairwise
interior-disjoint: **capacity(POCKET(U)) ≥ n − p** [T, trivial: Lean `packsBeside_compl`].  A ring at s < ⌈√n⌉ is
therefore impossible iff its pocket's capacity is < n − p (POCKET(n) of `ring_capacity.md` §5, now `pocket_cap`).

**2.2 (J1) The coverable set and the sandwich [T].**  COV(P) := ∪ {Q unit square : Q ⊆ P} = ∪_θ (C(θ) ⊕ Q_θ), C(θ) :=
{c : c + Q_θ ⊆ P} (Lemma GRAIN-LP's fixed-tilt free space).  For θ within Δ of θ_m the ∞-norm of a point in the two
frames differs by a factor ≤ w(Δ) = cos Δ + sin Δ (|x cos Δ ± y sin Δ| ≤ w(Δ) max(|x|, |y|)), so K := Q_{θ_m}/w(Δ/2) ⊆
Q_θ ⊆ w(Δ/2) Q_{θ_m} =: H for every θ in the bin [θ_m − Δ/2, θ_m + Δ/2]; hence C(θ) ⊆ P ⊖ K := {c : c + K ⊆ P} and
C(θ) ⊕ Q_θ ⊆ (P ⊖ K) ⊕ H.  Therefore **COV(P) ⊆ COV̄(P) := ∪_bins (P ⊖ K_bin) ⊕ H_bin and WASTE(P) := area(P) −
area(COV̄) ≤ area(P) − area(COV) = the true uncoverable area**; and capacity(P) ≤ area(COV(P)) ≤ area(COV̄): the AREA
BOUND.  Computation (`geom237.py`): P ⊖ K = the container shrunk by K's half-width minus ∪ (member ⊕ K) (hulls of vertex
sums), G ⊕ H = G ∪ ∪_{edges e of ∂G} hull(e + H) (H convex ∋ 0), 90 bins of 1°; [M] the sandwich on 3 000 random tilts,
waste 0 on a box of side 1.9 and 2.5.  ∎  (The lab's earlier census, `contact_census.md` / `grain_flood.md`, counts
contacts; this one counts area.)

**2.3 (J2) Sealed regions [T]** (`realign.md` §1.2, restated in the pocket): a region R ⊆ P bounded by members' edges and
walls in which no unit square fits (e.g. of width < 1 in some direction) is waste: a unit square meeting int R and not
inside R crosses ∂R, i.e. contains a boundary point of a member in its interior, hence meets that member's interior.
Instances: the strip between a wall and a flat meeter at offset δ < 1 (width δ); the wedge above a flat meeter's corner
under its tilted partner's edge (angle θ at the apex (δ, 1)); the STUBS of the n = 11 rings (width s − 3 − 1.5ε < 1 at
S < 4).  Common-tilt sealed wall pockets have area tan(min(φ, 90° − φ))/2, the corner triangle sin φ cos φ/2 (A231).

**2.4 (J3) Lemma WEDGE [T].**  Let W be a wedge of angle α ∈ (0°, 90°] with apex O and Q ⊆ W a unit square of tilt ψ
(relative to one ray).  Then dist(O, Q) ≥ r(α) := (1 + cos α + sin α)/(4 sin(α/2)) − 1/√2; so the sector W ∩ B(O, r(α))
is uncoverable (area r(α)² α/2), and r(90°) = 0 (a square nests in a right angle), r(60°) ≥ 0.476, r(45°) ≥ 0.870,
r(30°) ≥ 1.578.  *Proof.*  Rays at angles 0 and α; Q ⊆ {y ≥ 0} gives c_y ≥ w(ψ)/2 for the centre c, and Q ⊆
{x sin α − y cos α ≥ 0} gives c_x sin α − c_y cos α ≥ w(α − ψ)/2 (half-widths of Q in the two normal directions,
w(φ) = |cos φ| + |sin φ|).  With u the unit bisector, dist(O, Q) ≥ min_Q u·p = u·c − w(α/2 − ψ)/2 and u·c =
c_x cos(α/2) + c_y sin(α/2) ≥ [c_y + w(α−ψ)/2] cos(α/2)/sin α ≥ [w(ψ) + w(α−ψ)]/(4 sin(α/2)).  On [0, α] and [α, 90°]
ψ ↦ w(ψ) + w(α − ψ) is concave (a sum of shifted sinusoids on pieces where both are cos + sin), so it is ≥ its endpoint
value 1 + w(α); and w(α/2 − ψ) ≤ √2.  ∎  [M] r(α) ≤ the numerical minimum over ψ at every α = 5°..90° (`test237.py`; the
true minimum is NOT the edge-aligned cot α: at α = 50° a 60°-square reaches 0.817 < cot 50° = 0.839).  At a pocket
vertex of a near-flush ring the angles are 90° ± ε: r = 0 on the obtuse side and O(ε) on the acute side — the census of
vertices is O(ε), which is §0's [F].

**2.5 (J4) Lemma PIERCE [T, Lean `capacity_le_of_pierce`].**  If p₁..p_k are points such that every unit square Q ⊆ R
has some p_i ∈ int Q, then any family of interior-disjoint unit squares in R has ≤ k members (two squares sharing p_i in
their interiors are not interior-disjoint; the assignment is injective).  Certificate: with K_bin ⊂ int Q_θ for every θ
of the bin (the kernel is strictly inside), (P ⊖ K_bin) ⊆ ∪_i (p_i + K_bin) for every bin implies the hypothesis
(a centre c ∈ C(θ) ⊆ P ⊖ K has c ∈ p_i + K, i.e. p_i ∈ c + K ⊂ int(c + Q_θ)).  [M] verified as a residual area ≤ 10⁻⁹
over the 90 bins (floating-point shapely; the exact-rational replay is obligation O-PIERCE-EXACT).  The natural k = 1
point of an n = 11 ring is the container centre: every FLAT square inside the central box (1, s−1)² of side < 2 contains
it (Lemma TWO), and a tilted square can avoid it only by poking two stubs at once (a 47.6° square at S = 3.99, ε = 0.02
does, residual 0.020: `pocket237.md` §2), which the narrower pockets at S = 3.90 forbid.

## 3. Theorem POCKET-CAP

**3.1 Statement [T].**  P a stable ring (A236: a four-crowd none of whose meeters retreats) of n squares at s < ⌈√n⌉ =: m,
U ⊇ its meeters, p = |U|.  If capacity(POCKET(U)) < n − p — in particular if area(COV̄) < n − p (area form) or
PIERCE(n − p − 1) holds — then P does not exist.  Lean: `PacksBeside`, `PocketCapacityLT`, axiom `pocket_cap` (POCKET-
CAP(n) as the residue [C]: every stable ring below m has capacity < n − p), theorems `ring_capacity_of_pocket_cap`
(⇒ RING-CAPACITY(n)), `locked_crowd_free_of_pocket_cap`, `one_flush_value_of_pocket_cap` (ONE-FLUSH(n) value form),
`optimal_psiMin_not_stuck_of_pocket_cap` (n = 11).  The n-general shape: area(P) = s² − p exactly (members are unit
squares), so the area form reads WASTE(P) > s² − n, INDEPENDENT of p — the count of members never enters (NO-CLOSURE
again): only the pocket's shape does.

**3.2 n = 11 on the window [T computed, M].**  Ring p = 8 (the window's rings have two meeters per corner and, below 4, no
room for a ninth member with a pocket of capacity 3: A226), s ∈ [3.82, ŝ], area(P) = s² − 8 ∈ [6.59, 7.03], needed:
capacity ≤ 2.  (i) The A226 family (`pocket237.md` §2): waste ≥ 3.08–3.64 (the four stubs of width 0.87–0.96 and the
corner slivers), coverable ≤ 3.77–4.71 — the area form gives capacity ≤ 3 or 4, not 2; PIERCE(1) at the best of 225 grid
points certifies capacity 1 at S = 3.90 (ε = 0.02, 0.05, 0.10) and at S = 3.95, 3.99 with ε = 0.10 (residual 0), fails
by 3·10⁻⁴–2·10⁻² at the other four (two-stub diamonds).  (ii) The window family ring(S, θ) (`family237.py`: at each
corner a flat meeter at offset δ = sin θ + 0.02, the least admitting a partner of tilt θ by TILT-MIN, and the mode-(a)
partner at tilt θ resting 10⁻³ above its corner; alternating floor / wall variants; verified packings for θ ≤ 25° at
S = 3.82, 3.85 and θ ≤ 30° at ŝ, four-crowds for θ ≥ 5°): PIERCE(1) at the centre holds with residual 0 at EVERY (S, θ),
θ = 1°..30° — the pocket holds ONE square, 9 < 11; A222's greedy placer agrees (capacity 1); the area form alone gives
capacity ≤ 2 only for θ ≥ 15° (S = 3.82, 3.85) or θ ≥ 20° (ŝ).  So on these families POCKET-CAP closes — by the shape
(centre side s − 2 − δ ≤ 1.86 < 2, stubs of width s − 2 − (1 + δ) − (cos θ + sin θ − 1)... < 1), not by jaggedness.
(iii) **Analytically**: the only n-general handle is the area form with a tilt floor: 4 w_c(θ_min) > ŝ² − 11 = 4.032
needs θ_min ≥ 32° (`table237`: w_c(30°) = 0.973, w_c(32°) ≈ 1.03); the loaded rings that exist (the 193, at 4.00–4.42)
have meeter tilts down to 10° = their generator's floor and, by A89, no floor is forced; Trump's own crowd has a FLAT
meeter.  **POCKET-CAP does not close LOCKED-CROWD-FREE(11) analytically.**  What remains is exactly A236's: the extremal
route (A233) + TILT-MIN + JAGGED reduce the four-crowd case to "every stable 8-ring's pocket at s ∈ [3.82, ŝ] has
capacity ≤ 2" — a statement about a family of pockets parametrised by 8 poses, which PIERCE decides pocket by pocket
(0.1 s each) and which no tilt floor turns into arithmetic.

**3.3 The n-general table [T computed].**  w_c(θ) := the uncoverable area attached to one crowd (flat meeter at the least
offset, partner at tilt θ) in a large box — the sealed strip beside the flat meeter, the triangle under the partner
against the wall, the wedge above the flat meeter's corner: w_c = 0.194 / 0.364 / 0.530 / 0.689 / 0.973 / 1.271 at
θ = 5° / 10° / 15° / 20° / 30° / 45°.  A four-crowd wastes ≥ 4 w_c(θ_min) at tilt floor θ_min.  Area form: closes iff
4 w_c(θ_min) > s(n)² − n.

| n | m | s(n) | s² − n | 4 w_c(10°) | 4 w_c(20°) | 4 w_c(45°) | least θ_min that closes |
|---|---|---|---|---|---|---|---|
| 5 | 3 | 2.7071 | 2.33 | 1.46 | 2.76 | 5.08 | 17° |
| 10 | 4 | 3.7071 | 3.74 | 1.46 | 2.76 | 5.08 | 29° |
| 11 | 4 | 3.8771 | 4.03 | 1.46 | 2.76 | 5.08 | 32° |
| 17 / 19 | 5 | 4.68 / 4.89 | 4.86 / 4.87 | 1.46 | 2.76 | 5.08 | 42° |
| 18 | 5 | 4.8229 | 5.26 | 1.46 | 2.76 | 5.08 | none |
| 26–29 | 6 | 5.62–5.93 | 5.57–6.21 | 1.46 | 2.76 | 5.08 | none |
| 37–41 | 7 | 6.60–6.93 | 6.54–7.39 | 1.46 | 2.76 | 5.08 | none |
| 50–55 | 8 | 7.57–7.95 | 7.33–8.30 | 1.46 | 2.76 | 5.08 | none |

Reading: the four corners' waste is bounded (≤ 5.08 even at 45°) while the slack s(n)² − n grows with n (the records
leave ≈ 2 m · (m − s) + (m² − n) of area), so the corner census alone closes nothing from n = 18 on and closes n ≤ 17
only under tilt floors no theorem supplies.  Adding the wall chains' sealed pockets (A231: tan φ/2 per sealed pair) gives
`realign.md` §4's area horn — 2⌊s/√2⌋ − 1 at best — which beats the slack only for all-diamond walls at n ≥ 17 and never
under available hypotheses.  **The residue, n-general: POCKET(n) is a SHAPE statement** (the pocket of a stable ring
below m is a centre of side < m − 2 − 2ι with stubs of width < 1, and such a region holds ≤ N(m − 2 − 2ι) + (stub
pokes) squares), not a waste count; its proof must control the members' POSES (the loaded component's geometry), which is
the k0_00 obligation at n = 11 and has no local form (A233 §4).

## 4. Tests [M] (`pocket237.md`)

The ring + 189 four-crowds with a loaded component (sides 4.00–4.42, above m: the lemma must not fire): soundness
(coverable ≥ n − p) 189/189, the area form fires on 0; waste min 3.10, median 5.46, max 8.58 of pocket areas ≈ 6.1;
PIERCE(n − p) with the rattlers' own centres certifies 13 of 67 (rattlers slide; the rest are not tight).  The ring
`rand_0_0569|t20`: p = 9, rattlers 2, area 7.89, coverable 3.58, waste 4.31 in 6 components (the largest, 2.06, is the
sealed left region beside member 4's 20° lean), PIERCE(2) residual 0.12.  Features: convex vertices median 22 (185 rows
have an acute one), reflex 29, tilted edges 37 — the held crowds' pockets ARE jagged, at tilts the generator imposed.
A226's rings and the window family: §3.2.  The 22 records (U = wall touchers, 4–24 members; interior squares 1–32): sound
22/22, the area form fires on none (coverable ≥ n − p with slack ≥ 0.03), waste 1.46 (n = 26) to 3.39 (Trump: its 45°
grain's sealed corners) — the records' "pockets" are the interior of a cross-braced frame and hold exactly their
interior squares.  Pages: `ring_pocket.svg` (the ring, A226's S = 3.90 ring with its piercing point, Trump; the uncoverable
sets hatched), `n11_window.svg` (ring(ŝ, 20°), ring(ŝ, 2°), one crowd's w_c(20°)); every panel geometry-checked, note per
panel.  Unit tests `test237.py`: sandwich, TILT-MIN random search, DEPTH-BUDGET, WEDGE, box sanity — all pass.

## 5. Lean, files, obligations

`Statements/Open/PocketWaste.lean`: `PacksBeside`, `PocketCapacityLT`; axiom `pocket_cap` ([C], n-general, = POCKET(n));
theorems `packsBeside_compl`, `ring_capacity_of_pocket_cap`, `locked_crowd_free_of_pocket_cap`,
`one_flush_value_of_pocket_cap`, `optimal_psiMin_not_stuck_of_pocket_cap` (n = 11), `capacity_le_of_pierce` (std axioms
only); `lake build` + `lean/audit.py` exit 0, no sorry (`lean/AUDIT.md`).  Obligations: O-TILTMIN (§1.1 in Lean over
`IsUnitSquare`, routine), O-DEPTH2 (DEPTH-BUDGET for two tilted meeters: [M] only), O-WEDGE (§2.4, routine), O-PIERCE-
EXACT (the certificate in exact rationals), POCKET-CAP(n) [C].  Resume: `bash attempts/A237-pocket-waste/code/run237.sh`
(python ≈ 4 min; `--lean-only` for the build + audit ≈ 5 min).
