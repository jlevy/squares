# The tilt floor for corner blockers at a k0 critical point: what is a theorem, what is a gap, and the intrusion-depth dichotomy — A89, 2026-09-03

Target (A89 BRIEF, PI direction after A88): at a k0 Fritz-John point z at side ≤ ŝ — by DF-K0
(`drain_flow_k0.md`) we may take z a global σ-minimiser — every square Q meeting a corner box
("corner blocker", A58) should have tilt(Q) = 0 exactly or tilt(Q) ≥ θ₀, with θ₀ explicit, so that
the near-flush ghost zone (0, θ₀) can be deleted from every blocker box of A85's tree. Addendum
(PI, mid-attempt): the intrusion-depth dichotomy per corner (Lemma ID) and its consumption.
Labels: [T] proved, [S] routine given cited items, [M] measured, [F] finding, [C] open.
Conventions: `drain_lemma.md` v3 (D1, D3′, Gordan/Farkas), `structure_lemmas.md` (Fact 0, L1–L7),
`k0_route.md` (K0-FREE, K0-WIDEN, K0-PAIR, K0-REUSE, K0-ROT, Lemma P-TREE leaves), A58
`notes/theory.md` (CC-2′, "meets" = open interiors), A46/A47/A48/A50 as cited. Measurements:
`attempts/A89-tilt-floor/notes/t2_report.md` (T2, Opus chore), `results/t2_*.json`.

## 0. Verdict

> **θ₀: NONE for loaded blockers by any local argument; the near-flush jam is first-order
> consistent with criticality (an explicit multiplier solution, §5), exactly the A46/A48-C5b wall.
> What IS a theorem is the other half of the dichotomy, in selected form: Theorem TF-U — there
> is a σ-minimiser (Φ-minimal, Φ = Σ f(tilt_i)) at which EVERY square, corner blocker or not,
> has tilt exactly 0 mod 90° or is FLUSH-LOCKED (Lemma LOCK: its active contacts can exert a
> couple away from flush, or a self-stress). Rattlers and every unloaded-unlocked square have
> tilt exactly 0 there (case (i) of the brief, resolved in the selection form). A flush-locked
> wall-touching blocker needs a FAR-SIDE contact (Lemma MENU: on its far edge, at its two far
> vertices with named normals, or a vertex under its wall edge), so the near-flush zone survives
> only as a jam with ≥ 3 squares, and the two-square corner jam of case (ii) is pinned exactly
> (Lemma JAM-0: an axis-aligned blocker at offset g < 1/√2 forces its partner to
> sin(tilt) ≤ g and intrusion depth ≤ g²/√(1−g²); for g < δ_pin = 0.02 this is the K0-REUSE
> pocket). Case (iii) (tilt exactly 0, offset) is allowed by every statement here, as it must be:
> Trump's TL crowd IS one (an axis-aligned upright 0.8445 above the slot + sq6 at 40.18°), and
> the canary passes (T2: 0 Trump blockers in (10⁻⁷, θ₀) for every θ₀ ≤ 30°).**
>
> **Empirically the floor is far above the target: over A87's 167 certified k0 FJ points (665
> corner blockers) and the 12 atlas families (51), no LOADED corner blocker has tilt in
> (10⁻⁶, 23.89°) — the min loaded tilt is 23.891° (forced, A87 o026) / 33.896° (atlas, = A46's
> WC-loaded min); every positive tilt below 20° is a rattler or an unloaded square (161 of 162
> below 10° carry no loaded corner-wall contact; 127 touch no corner wall). The one near-flush
> two-square jam in the corpus (o170, σ = 4.000, tilts 0.76° / 6.68°) carries λ_max = 0 on every
> incident row — geometrically present, dynamically irrelevant, exactly Theorem TF-U's picture.**
>
> **Deleted fraction and re-price.** Even granting the un-proved loaded floor at θ₀ = 1.7347°
> (A50's θ*), the deletion is 3.4 % of the blocker-box tilt volume, 0 of A85's 33 656 pair
> boxes, and 0 of its 5 FAILed LP nodes (the only failed corner node sits at 41–49°); pair boxes
> start dying only at θ₀ > 7.125° (an end bin dies whole), 31 % at θ₀ = 10°. With the proved
> TF-U the deletion is conditional (SelForm (C) leaves, free at deep nodes, silent at the crowd
> level, same verdict as K0-ROT). **A85's price stands: 3 200–7 000 CPU-h (f₂ ≈ 0.85) / ≥ 3·10⁴
> (f₂ = 1/3). The near-flush ghost zone is not where A85's measured cost is: the FAILs are
> interior depth-1/2 cells failing on certification coverage holes (A85 §7.3), not corner boxes.**
> Lemma ID gives the tree a free exact budget row per SHALLOW corner ((1−δ)² of E(s) = s² − 11
> ≤ 4.0318) and a corner-first branching (§7); it changes the composition, not the frontier.

## 1. Setting and definitions

Packings: eleven closed unit squares Q_i = Q(c_i, θ_i), pairwise interior-disjoint, inside
[0, m]²; M(m) := the set of packings at side m (compact: closed and bounded in the 33 pose
coordinates). σ, D₀, NLP(S), consistent selections S, FJ certificates (λ₀, λ) as in
`drain_flow_k0.md` §1; every packing is S-feasible for some consistent S and S-feasible ⇒
interior-disjoint (soundness). A ROW of Q under S is any S-row involving Q's coordinates: its
four wall rows (near walls q ≥ 0, far walls s − q ≥ 0, s fixed = m) and its pair rows.

* **tilt**(Q) := dist(θ_Q, 90°ℤ) ∈ [0°, 45°]; **flush** = tilt 0. "Toward flush" at tilt ∈ (0, 45)
  is the sense that decreases tilt; at tilt = 45° both senses do.
* **Corner box** B_c := the closed unit box at corner c of [0, m]²; Q **meets** B_c iff
  int Q ∩ int B_c ≠ ∅ (A58); a **corner blocker** is a square meeting some corner box. Two
  corner boxes are ≥ m − 2 ≥ 1.82 > √2 apart (CC-1(ii)), so a square meets at most one, and a
  blocker's far-wall rows have margin ≥ 3.82 − (1 + √2) > 1.4 (never active).
* **Intrusion depth** (BL frame; other corners by D4): for Q meeting the open slot (0,1)²,
  depth(Q) := 1 − inf{max(p_x, p_y) : p ∈ int Q ∩ (0,1)²} ∈ (0, 1]; DEPTH(c) := max over c's
  blockers. An axis-aligned [a, a+1] × [b, b+1] has depth 1 − max(a, b); the slot square has
  depth 1; a 45° diamond with lowest vertex v in the slot has depth 1 − max(v_x, v_y).
* **Flush-locked** (Definition, §2): Q at tilt ∉ 90°ℤ is flush-locked at z if for EVERY
  consistent selection S at z there is no y ∈ ℝ³ (Q's three pose coordinates, everything else
  fixed) with ∇_Q g·y > 0 for all active S-rows g of Q and with tilt decreasing at first order.
* **Selection functional** Φ(z) := Σ_i f(tilt_i), f : [0, 45°] → ℝ continuous, strictly
  increasing, e.g. f = id. Φ is continuous on pose space.

## 2. [T] Lemma LOCK — the first-order characterisation

Fix z, a consistent S, and Q with tilt ∈ (0, 45°) (the 45° and the mirrored senses are
identical with e_θ replaced by −e_θ resp. either sign). Write ∇_Q g_k = (n_k, τ_k) ∈ ℝ² × ℝ for
Q's active rows: n_k is the inward contact normal at contact k (the direction of the contact
force on Q) and τ_k = (x_k − c_Q) × n_k its torque about Q's centre (the gap's rate under unit
ccw rotation). Then exactly one holds:

(a) ∃ y = (v, ω) with n_k·v + τ_k ω > 0 for every active row k of Q and ω < 0 (a rigid motion
    of Q alone that strictly opens all its contacts and rotates it toward flush);
(b) ∃ (μ, ν) ≥ 0, (μ, ν) ≠ 0, with Σ_k μ_k (n_k, τ_k) = (0, ν): either ν > 0 — the contacts can
    exert a pure COUPLE on Q in the away-from-flush sense (zero net force, positive torque) — or
    ν = 0, μ ≠ 0 — Q is WEDGEABLE (a compressive self-stress on its own rows).

*Proof.* Gordan's alternative for the strict system {∇_Q g_k · y > 0 (k active), (−e_θ)·y > 0}. ∎

So "flush-locked for S" = (b) for S. Remarks. (i) (b) is what force balance permits; it is the
exact first-order content of "Q is jammed against rotating flush". (ii) If (a) holds for some
consistent S, then z + εy (Q moved, rest fixed) is S-feasible for small ε > 0 — active rows
increase at a positive rate, inactive rows keep their margin — hence a packing; its far-wall
rows are unchanged unless they are Q's own (then they increase), so σ(z + εy) ≤ σ(z).

## 3. [T] Theorem TF-U — the tilt selection (rattler / unlocked branch)

**Theorem TF-U.** Let m = s(11) (attained, D1). Let z* ∈ M(m) minimise Φ over M(m) (exists:
M(m) compact, Φ continuous). Then every square of z* has tilt exactly 0 mod 90° or is
flush-locked. In particular every rattler (no active row) and every square with an active-row
set admitting a strictly opening flush-ward motion has tilt exactly 0 at z*. The same holds
for z* minimising Φ over any compact subset of M(m) that is stable under small single-square
motions preserving the packing property — in particular (i) over the k-maximal minimisers
(A58/B.SEL: {k ≥ K*} is closed, and a small motion of a square with tilt ≠ 0 changes no slot
occupancy, so k is unchanged), and (ii) at side ŝ, over the non-Trump-image packings (closed,
because each image is isolated by its basin, A36/E.A36: every packing at ŝ within r_B of an
image is the image).

*Proof.* Suppose Q at z* has tilt ∉ 90°ℤ and is not flush-locked: Lemma LOCK (a) holds for some
consistent S. By Remark (ii) z* + εy is a packing with σ ≤ m, hence σ = m (minimality), and
Φ(z* + εy) = Φ(z*) + ε f′(tilt)·ω + o(ε) < Φ(z*) for small ε (at tilt = 45° use either sense;
f is strictly increasing so the one-sided derivative has the sign of ω). For (i) k is unchanged
along the motion; for (ii) the moved packing stays outside every basin for ε < r_B −
dist(z*, images) > 0. Contradiction with Φ-minimality. ∎

What TF-U does and does not say. It resolves case (i) of the brief (a rattler blocker CAN be
rotated to flush, and at the selected minimiser it IS flush; if it lands exactly on a slot the
teleport to k ≥ 1 is CC-2's) and it is exact (no θ₀). It is a statement about a SELECTED
minimiser; its consumers are in §8. It does not exclude any flush-locked square: that is the
loaded branch, §5.

## 4. [T] Lemma MENU — what can lock a wall-touching near-flush blocker

Let Q have tilt δ ∈ (0°, 45°] (ccw from flush; the mirrored sense by reflection) and touch the
bottom wall at its lowest vertex O = (p, 0), so Q has vertices O, R = O + (cos δ, sin δ)
(bottom-right), TR = O + (cos δ − sin δ, cos δ + sin δ), TL = O + (−sin δ, cos δ), in ccw order.
Consider the clockwise rotation of Q about O (toward flush; the wall row at O has rate 0). Under
a clockwise rotation about a pivot P₀ every boundary point x of an edge with ccw tangent t moves
outward at rate (x − P₀)·t. With P₀ = O:

| Q's edge / vertex | outward rate | effect |
|---|---|---|
| bottom edge O→R, t = (cos δ, sin δ) | +dist(x, O) | advances toward the wall (the intended landing; no square fits under it except at R, below) |
| right edge R→TR, t = (−sin δ, cos δ) | +dist(x, R) | ADVANCES: any contact on the right edge above R locks |
| top edge TR→TL, t = (−cos δ, −sin δ) | −(1 − u), x = TR + u t (−1 at TR, 0 at TL) | retreats: top-edge pressers never lock this motion |
| left edge TL→O, t = (sin δ, −cos δ) | −(1 − u), x = TL + u t (−1 at TL, 0 at O) | retreats: the left wall and left neighbours never lock |
| vertex R (moves (sin δ, −cos δ)) | closes against a neighbour edge with outward normal m iff m·(sin δ, −cos δ) < 0 | a support UNDER R (edge facing up) locks |
| vertex TR (moves (cos δ + sin δ, −(cos δ − sin δ))) | closes iff m·(cos δ + sin δ, sin δ − cos δ) < 0 | a neighbour above-right of TR with its edge facing down-left locks |
| vertex TL (moves (cos δ, sin δ)) | closes iff m·(cos δ, sin δ) < 0 | a neighbour whose edge through TL faces −(cos δ, sin δ): e.g. a square above Q with bottom edge through TL at tilt β < δ (m = (sin β, −cos β), m·(cos δ, sin δ) = −sin(δ − β)) |

**Lemma MENU.** A bottom-wall-touching blocker Q at tilt δ ∈ (0, 45°] is flush-locked only if it
has an active contact in its FAR-SIDE SET: on its right edge (above R), a support under R, a
down-left-facing contact at TR, a contact at TL with normal m·(cos δ, sin δ) < 0, or a
neighbour's vertex under its bottom edge (possible only within unit reach of R). The bottom
wall, the left wall (whether Q touches it at TL or not), left neighbours and top-edge pressers
alone never lock it. Symmetrically for a left-wall-touching blocker (rotate about its leftmost
vertex). *Proof.* The table: if no far-side row is active, y = (rotation about O) is Lemma
LOCK (a) for every S (all Q-rows have rate ≥ 0, strictly > 0 except the pivot row, and the
pivot row can be made strict by adding a small translation (0, +ε′) which opens every wall row
and changes the other rates by O(ε′)). ∎

Corollary (corner jam, K0-REUSE pocket). A blocker touching BOTH corner walls at tilt δ (the
"tilted slot square") is locked only by far-side contacts — its two wall contacts do not lock
it; this is why the pocket "square within δ_pin of the slot + its neighbour" is k1_00's tree
(K0-REUSE) and not a critical structure by itself.

Floating blockers (no wall contact) have no canonical pivot; Lemma LOCK (b) is the exact
statement (the contacts must admit an away-from-flush couple or a self-stress), and at least
two contacts on opposite sides of a line through the centre are needed (a couple needs two
non-collinear forces; L1 gives two loaded contacts anyway).

## 5. [T] Lemma JAM-0 and case (ii); [F] why the loaded floor has no local proof (GAP A89-G1)

### 5.1 [T] Lemma JAM-0 — the axis-aligned blocker pins its partner

**Lemma JAM-0.** Let the BL corner box be met by an axis-aligned square Q = [a, a+1] × [b, b+1]
(a, b ≥ 0) with g := max(a, b) < 1/√2, and by a second square N (interior-disjoint from Q,
inside the quadrant). Then N has a vertex v in the L-strip U := ((0, a) × (0, 1)) ∪
((0, 1) × (0, b)) which is N's LOWEST vertex (v in the left strip) or LEFTMOST vertex (v in the
bottom strip), and
  sin(tilt N) ≤ g,   depth(N) ≤ g²/√(1 − g²) (< √2 g²).
In particular N is never axis-aligned (K0-PAIR (a) again) and, for g ≤ 0.1: tilt(N) ≤ 5.74°,
depth(N) ≤ 0.0101; for g ≤ δ_pin = 0.02: tilt(N) ≤ 1.146°.

*Proof.* N meets int B_BL ∖ Q ⊂ U. If no vertex of N lay in U, N ∩ U would be bounded by
N-edges crossing U; a straight edge entering the left strip can exit it only through its top
opening (x = 0 is the container, x = a below y = b + 1 is int Q, y = 0 is the container), so it
enters and exits through the same open side — impossible for a segment. Hence a vertex v ∈ U.
Let v ∈ left strip (the bottom strip is the x↔y mirror). N's two unit edges from v have
perpendicular directions e₁, e₂; both must keep x ≥ 0 over unit length (e·(1,0) ≥ −v_x > −a)
and avoid int Q. Cases on which vertex v is: (lowest: e₁ up-left, e₂ up-right) the up-left
edge gives sin φ ≤ v_x < a for the tilt φ; (rightmost: both edges have negative x-component)
requires cos φ ≤ v_x < a and sin φ ≤ v_x < a, impossible for a < 1/√2; (topmost) the steep
downward edge must clear the wall over unit length, cos φ ≤ v_y, and the other edge, going
down-right, enters int Q at x = a unless v_y ≤ b + (a − v_x)tan φ, forcing v_y ≤ b + o(1) < 1/√2
< cos φ — impossible; (leftmost: e₁ = (cos φ, sin φ) rising, e₂ = (sin φ, −cos φ) descending)
the descending edge gives cos φ ≤ v_y; the rising edge crosses x = a at height v_y +
(a − v_x)tan φ, which must be ≥ b + 1 (then tan φ ≥ (b + 1 − v_y)/(a − v_x), φ > 45°, and the
descending edge crosses x = a below b: cos φ ≤ v_y ≤ (a − v_x)cot φ ≤ a², so sin(tilt) = cos φ
≤ a²) or ≤ b (then the whole of N must pass under Q: its top vertex v + e₁ needs cos φ ≤ a − v_x
or sin φ ≤ b − v_y, and with cos φ ≤ v_y < b < 1/√2 the second is impossible and the first gives
sin(tilt) = cos φ ≤ a). A vertex v UNDER Q (v_x ∈ (a, a+1), v_y < b) is impossible: the edge
that must clear Q's corner (a, b) puts that corner inside N's 90° wedge unless the wedge points
left, and then N's far vertex v + e₁ + e₂ has x ≤ v_x − (cos φ + sin φ) < a + 1 − 1 = a, forcing
sin φ + cos φ ≤ v_x ≤ a + 1 and, for the far vertex to stay in x ≥ 0 and the corner outside the
wedge, a > 1 − (b − sin φ)tan φ ≥ 1 − 0.094 — impossible for g < 1/√2. Depth: in the lowest-
vertex case the part of N below Q's top line y = b + 1 is a right triangle at v of depth d with
legs at angles φ, 90° + φ; it must fit between the wall and Q's left edge, so d ≤ (a − v_x)tan φ
and d ≤ v_x cot φ; with sin φ ≤ v_x this gives d ≤ a tan φ ≤ a²/√(1 − a²), and every point of
N ∩ B_BL has y ≥ b + 1 − d, so depth(N) ≤ d − b ≤ a²/√(1 − a²). In the leftmost-vertex cases
the mirror bound holds with b. ∎

Consequences. (1) Case (ii) of the brief is exactly this lemma with b = 0 and Q flush on the
bottom wall at offset a: the partner dips a vertex into the gap between Q and the left wall,
tilt ≤ arcsin a, dip ≤ a²/√(1−a²), and (K0-PAIR (a)) is never axis-aligned. (2) In the
K0-REUSE pocket (g < δ_pin = 0.02) the partner is within 1.15° of flush: the pocket's whole
crowd is near-flush, as A85 observed ("the k0 landscape lives there": the best k0 optimum at
s₀ + 0.0101 has four axis-aligned squares 1.6·10⁻³–8.6·10⁻³ off their slots). (3) Under a
loaded floor θ₀ (if it were a theorem), an axis-aligned blocker at offset g < sin θ₀ would be
impossible at a critical point (its partner has tilt in (0, θ₀) and, by TF-U applied to the
selected minimiser, would have to be flush-locked — see §5.2 for why that is not excluded).

### 5.2 [T] The near-flush jam is first-order consistent with criticality — GAP A89-G1

Take case (ii): Q = [ε, 1+ε] × [0, 1] flush on the bottom wall; N with tilt α ∈ (0, arcsin ε),
lowest vertex v = (v_x, 1 − d) in the gap, bottom edge through Q's corner c = (ε, 1) at distance
r = d/sin α ≤ ε cos α from v, top-left vertex u = v + (−sin α, cos α) on the left wall
(v_x = sin α). Rows of N: c on N's bottom edge (force on N along (−sin α, cos α)), the wall at u
(force (+1, 0)), and whatever presses from above. Force balance on N with multipliers G (wall),
F (c), H (a presser at distance t_P from u along the top edge, force (sin α, −cos α)) and K (a
right-side contact on N's right edge at height h′ above c's level, force (−cos α, −sin α)):
y: H = F − K tan α; x: G = K/cos α; torque about c: −G(cos α − d) − H(t_P − r) + K h′ = 0, i.e.
H (t_P − r) = K (h′ − 1 + d/cos α) < 0. So with three contacts only (K = 0) the wall is unloaded
(G = 0) and the presser sits exactly at t_P = r (codimension 1) or N is unloaded (H = F = 0 —
then TF-U moves it); with a right-side contact K > 0 the wall carries G = K/cos α and **the
presser must sit within r ≤ ε of N's top-left vertex.** And Q balances with
the reaction (sin α, −cos α)F at c, a right-side contact supplying −F sin α (a neighbour on
Q's right edge or at its corners, Lemma MENU's far-side set for Q's own lock — for Q axis-
aligned there is nothing to lock, but its x-balance needs it), and the wall load on its two
bottom rows, whose moment range [−W/2, W/2] with W = F cos α contains the required
−F cos α/2 + F sin α (1 − h) for every contact height h ≤ 1 on Q's right edge. So every
multiplier is nonnegative and bounded: **the jam admits an FJ certificate locally.** Its lock
(Lemma LOCK (b) for N) is the presser within r of u: the motion "rotate N clockwise about u and
slide it up the wall by q = ωr cos α" opens c, the wall and N's whole right edge (rates
ω(t − 1) < 0) and advances only the top edge on [0, r) from u and the vertex w = N's top-right
corner along N's right-edge direction — exactly the presser's zone, so the jam is locked iff it
is loaded, as Lemma LOCK says it must be.

The presser P sits with its contact point within ε of the left wall; if the contact is P's
vertex, P's up-left edge must stay in x ≥ 0, so sin(tilt P) ≤ ε as well (JAM-0's mechanism one
level up); if it is flush (P's bottom edge on N's top edge, same tilt), P's bottom-left vertex
is at distance t′ ∈ [tan α, r) from u. In the flush case P is locked by ANY presser on its top
edge within 1 − t′ of its top-left vertex (rotation about the far flush row w advances the top
edge at rate ω(1 − t′ − t″)), i.e. by a mid-tilt square from the TL crowd — the recursion
"near-flush needs a more tilted supporter" (A47 I-L19) terminates at the third level without a
contradiction. The same is true of Q's right-side supplier. **Hence no first-order (Gordan/
Farkas) argument on the blocker, the pair, or the pair plus one supporter excludes the near-
flush loaded jam; the jam is a member of the local FJ menu, exactly as A46's bridge (no δ₀ for
loaded WC contacts), A48's C5b (exact press position u = sin² d, bounded multipliers) and A47's
sixth face found one level down.** The candidate global mechanisms are A50 T2.1 (span
quantisation of a near-flush P-chain; conditional on H-P/H-MONO/H-L6CAP, floor θ* = 1.7347°,
applies to a blocker only if it is a member of the binding chain) and A50-G1's second-order
route; neither is a lemma about corner blockers, and the corpus is consistent with the floor
being a global, side-dependent fact (all near-flush jams observed sit at σ ≥ 4.0 and unloaded).

**GAP A89-G1 (loaded floor).** "A flush-locked corner blocker at side ≤ ŝ has tilt ≥ θ₀" is
open for every θ₀ > 0; it is not a local statement (this section), it is not implied by A50
(hypotheses H-P/H-MONO/H-L6CAP and chain membership), and the only evidence is the corpus
(min loaded tilt 23.89° over 167 + 12 critical points, all at σ ≥ 3.897 > ŝ). A counterexample
AT side ≤ ŝ would be a k0 critical point below Trump (H1 false) and is not expected; the
counterexample to the local STRATEGY is explicit above (multipliers) and in vivo (T2 §1.6:
o170 at σ = 4.000, both jam members unloaded).

## 6. [T] Case (iii) and the canary

An axis-aligned square offset from the slot is a corner blocker with tilt exactly 0 and is in
k0_00 (skeleton needs the exact slot pose). Nothing above touches it: TF-U's selection moves
only squares with tilt ≠ 0; Lemma JAM-0 constrains its PARTNER; a loaded floor would delete
(0, θ₀), not {0}. Canary [M, T2 Task C, 300-digit tilts from `A03-upper-reconstruct/
trump11_exact.json`]: Trump's corner blockers are the three slot squares (|tilt| < 2.2·10⁻⁶⁹°),
the TL upright sq4 (tilt 1.1·10⁻¹⁰⁷°, centre 0.8445 above the slot, depth 0.1555) and sq6
(40.18194°); 0 blockers in (10⁻⁷, θ₀) for every θ₀ ≤ 30°. **PASS.** (Correction to the brief's
A58 paraphrase: TL is met by one tilted square and one axis-aligned offset upright, not by two
tilted squares — the exact-0 branch is load-bearing at Trump.)

## 7. [T] Lemma ID — the intrusion-depth dichotomy and its budget row

**Lemma ID.** Fix a corner c of a packing at side m and δ ∈ (0, 1). If DEPTH(c) < δ then the
open box (0, 1 − δ)² (in c's frame) meets the interior of no square; hence the closed box
[0, 1 − δ]² is wasted and the corner strands ≥ (1 − δ)² of the wastage budget E(m) := m² − 11
(the area of [0, m]² not covered by square interiors). At m ≤ ŝ, E ≤ ŝ² − 11 < B₀ =
251986271441/62500000000 = 4.031780343056. The four corner boxes are disjoint (m − 2 > 1), so
with c_sh shallow corners, c_sh (1 − δ)² ≤ m² − 11.

*Proof.* A square meeting (0, 1−δ)² meets (0, 1)², so it is a blocker with
inf max(p_x, p_y) < 1 − δ, i.e. depth > δ. ∎

What the budget row does and does not do. [T] It is exact, position-free and LP-free: a
SHALLOW corner is a NO-family (the poses whose square meets (0, 1−δ)²) for the node's case-LP
certificate, realised as a sound inner union of pose boxes (§8.6′), and it composes across
corners because the corner boxes are disjoint. [F] Area alone does not kill four shallow
corners in the window: 4(1 − δ)² ≤ 4 < 4.0318 for every δ ≥ 0 (at m = 3.82 it needs δ ≥ 0.052;
3-shallow never). **[CERT, A89-O3, §8.6″] The certified bound: no 11-packing at any side
m ∈ [3.82, s₀] has all four corners SHALLOW(0.3) — at least one corner has DEPTH ≥ 0.3 (a
square reaches within 0.7 of the corner point); the same certificate covers δ = 0.1, 0.05.**
Three shallow corners: NOT certified (τ = 10.05 at δ = 0.3 with the feedback rounds climbing to
10.21 — a genuine near-boundary node; at δ = 0.1 η = −1.78 but the C1 certification did not
close at the 900 s LP cap — an LP-time artefact, resumable), so "at most two shallow corners"
is open [C]; the area row gives nothing there (3(1−δ)² ≤ 3 < 3.59). Trump-level waste outside
the corners is not an unconditional bound (Trump's own TL corner has DEPTH = 0.168300 exactly
(sq6; sq4 0.1555) and strands ≈ 0.69 there; his other three corners strand 0; every D4 image has
exactly one shallow corner, which is why 1-SHALLOW is image-realisable and 2-SHALLOW is not).

**Corner-first branching (the addendum's tree).** Per corner: SHALLOW(δ) — free exempt box,
no square localised, DEPTH < δ is a hypothesis on ALL squares (∀-packings, sound as a NO-child:
"no square intrudes ≥ δ" is the complement of the YES-children below); DEEP(δ) — some blocker
Q has a point p ∈ int Q with max(p_x, p_y) < 1 − δ; Q's centre then lies within
(1 − δ) + √2/2 of the corner in each coordinate and Q's box is one of the A85 reach-cover boxes
that can host depth ≥ δ (T2b counts them). In the DEEP branch, by TF-U at the selected
minimiser, Q is tilt-0 (axis-aligned, offset g ≤ 1 − δ, K0-PAIR (a): its partner is tilted,
Lemma JAM-0: partner tilt ≤ arcsin g and depth ≤ g²/√(1−g²) when g < 1/√2 — a (C)-type
coupling row between the two crowd boxes, exact) or flush-locked (needs a far-side contact —
a third square's box must reach Lemma MENU's zone: a SelForm (C) leaf when it cannot). The
reach correction (PI): an axis-aligned deep blocker reaches < 2 from its corner (a + 1 with
a < 1); reach in [2, 1 + √2) needs tilt, the 45° diamond with a vertex in the slot being
extremal at 1 + √2 = 2.414. The crowd hypothesis K0-FREE′ (every corner doubly met,
∀-packings given k1_00's tree) is unchanged and is what makes a NO-branch "≤ 1 meeter" a (T)
leaf; ID's SHALLOW branch is a different, weaker hypothesis (blockers exist but are shallow)
and does not teleport — it only charges. Composition: Lemma P-TREE's Step 3 with the exempt
boxes added to the (K) leaf's certificate hypothesis (Lemma B transports "int Q ∩ (0, 1−δ)² =
∅" to the s₀ family with the box shrunk by the dilation: Q′ = Δ_λ Q meets (0, 1−δ)² only if Q
meets (0, (1−δ)/λ)² ⊇ (0, 1−δ−0.0149)², so the exempt box at s₀ is [0, 1 − δ − (λ_max − 1)]²,
same bookkeeping as K0-WIDEN).

## 8. [M] What T2 measured (`attempts/A89-tilt-floor/notes/t2_report.md`)

**8.1 A87's 167 certified k0 FJ points (tol 10⁻⁶; σ ≥ 3.8972, all above ŝ).** 665 corner
blockers (3.98/point); rattlers 179, rows-but-unloadable 101, loadable 385, forced 118; per-
corner count 0/1/2 blockers at 24/623/21 of the 668 corner slots (all 167 violate K0-2's
≥ 2 — they are FJ points, not k-maximal minimisers). Tilt histogram: 353 exact-0 (the case (iii)
population), 70 in (10⁻⁷, 0.5°), 24 in [0.5, 1), 17 in [1, 1.7347), 5, 20, 26, 53, 42, 21, 34 in
the bins up to 45°. **Loaded(forced) blockers with tilt in (10⁻⁷, θ₀): 0 for every θ₀ ≤ 20°**
(2 at 30°); loadable: 1 (o075 sq4, tilt 3.6·10⁻⁷°, a numerically flush edge-on-wall square —
polish noise), then nothing below **23.891°** (o026 sq5 TL, forced). Unloaded/rattler in
(10⁻⁷, θ₀): 69 / 93 / 110 / 115 / 128 / 135 / 161 / 214 / 254 for θ₀ = 0.5 / 1 / 1.7347 / 2 / 3 /
5 / 10 / 20 / 30. Of the 162 blockers with tilt in (10⁻⁷, 10°): 127 touch no corner wall, 161
have no loadable corner-wall contact. Two-square near-flush jams (case (ii)): exactly one —
o170 BR (σ = 4.0000000000300): sq10 tilt 0.7593° corner-on-wall at x = s, jammed against sq4
(6.685°) and sq0; **λ_max = 0 on all three of sq10's rows** (TF-U's picture: present, unloaded).
Six points admit λ₀ = 0 certificates (o012, o092, o150, o154, o157, o161).

**8.2 The 12 atlas families (A46's set).** 51 blockers, 25 slot squares; min loaded tilt
**33.8963°** (fam13/14 sq5 TR, forced) = A46's WC-loaded minimum; the five positive tilts below
30° (0.025°, 0.169°, 0.519°, 5.47°, 11.77°) are all rattlers touching no corner wall, all at TL.

**8.3 A85's LP rows.** Of the 12 run nodes (26 planned), the 5 FAILs are 4 interior cells
(l1_008/043/053 at 15–90°, l2_p215 at 82.5–90°: the lemma is not about them) and the one
corner node b178 at [41.1°, 48.9°]; the zone-touching blocker boxes ([0, 7.125°] or
[82.875°, 90°]) all belong to PASSed nodes (b595, s2_619, s3_near, s4_near) or to the refused
s3_far (τ = 7.000 at budget 7, TR box [0, 7.125°]). **Fraction of FAILed blocker nodes deleted:
0.0 for every θ₀ ≤ 15°.**

**8.4 The BL blocker-box census (644 sound boxes, 9 tilt bins: t-edges {0, 1/8, 1/4, 3/8,
5/11, 3/5, 7/9, 1} with the end bins bisected in degrees at 7.125°; 33 656 level-2 pairs).**
Zone-touching boxes 128/644 = 19.9 % for every θ₀ ≤ 7.125°; tilt VOLUME deleted 0.99 % / 1.98 %
/ **3.43 %** / 3.96 % / 9.9 % (degrees; 1.16 / 2.31 / 4.00 / 4.60 / 11.3 % in t) at θ₀ = 0.5 / 1
/ 1.7347 / 2 / 5°; pairs with ≥ 1 zone-touching member 10 483 = 31.1 % (both: 1 300 = 3.9 %);
**pairs killed by re-pruning the clipped boxes: 0 at θ₀ ≤ 2°, 146 (0.4 %) at 5°, 10 483 (31 %)
at 10°, 22 630 (67 %) at 15°** (level-0 prune, a lower bound). Nodes die only when an end bin
dies whole (θ₀ > 7.125°).

**8.5 Reach, self-jamming and depth (T2b, `t2_report.md` §A0–A8).** Pair-only model: the
other nine squares absent, the far structure modelled as a rigid L-wall at the pair's own reach
caps (X₀, Y₀) — the only reading under which "no s-nonincreasing motion frees the slot" is
non-vacuous; "self-jammed" = no continuous motion of the pair under the caps ends with the open
slot met by ≤ 1 square, tested by a 190-motion library on an exact witness pose (LIBRARY-JAMMED
is an UPPER bound on self-jammed). Census: 33 656 level-2 pair boxes; witnesses found for 7 800
(grid lower bound; 4 365 slot, 3 435 widened-only), 0 failures on exact re-verification.
* **H0 reach.** Sound box bound max 2.4571 (loose); witness reach max 2.4224 (widened) / 2.3877
  (slot) vs the theoretical single-blocker 1 + √2 = 2.4142 (a 45° diamond on the wall) and
  < 2 for an axis-aligned blocker; **every realisable 2-crowd reaches past 2** (K0-PAIR (a)
  pushes one member out).
* **H1 self-jam.** 151 / 7 800 = **1.94 %** (CI95 [1.63, 2.24] %) library-jammed, all with slot
  witnesses; 98.1 % need a third square or the far structure to be stuck; a plain translation or
  a centre rotation frees 5 of 6. Jam types: near-slot 0, stacked-dipping-vertex (case (ii)) 16,
  side-jam 0, floating 88, diamond-wedge 31, other 16. **Max reach over jammed pairs 2.3860** —
  99.9 % of the realisable maximum: jamming costs nothing in reach, so adjacent-corner reach
  envelopes CAN overlap (2 × max X₀ = 4.77 ≥ ŝ; 144 of 151 jammed pairs have X₀ ≥ ŝ/2 alone;
  necessary for contact, not sufficient). The claim "reach ≥ 2 ⇒ freeable by sliding" is FALSE
  under the caps (151/151 exceptions: the cap blocks the outward slide, the partner the inward
  one; the extremal jams are symmetric 41.1° diamond wedges).
* **H2 (tilt floor applied to the census).** Consistent pairs 33 656 at every θ₀ ≤ 5° (the bins
  are 7.125° wide), 23 173 (69 %) at 7.2–10°, 11 026 (33 %) at 14.3–23.9°, 2 910 at 30°; jammed
  count 151 → 135 → 133 → 107: **the floor kills the case-(ii) jams (all 16) exactly when
  θ₀ > 7.125°, and never touches the floating / diamond-wedge jams**, whose members are not
  near-flush on a wall; max jammed reach 2.386 at every θ₀ (a 41.1° family).
* **Canaries.** K0-PAIR (b)'s exhibit: SAT gap +0.0442 (doc 0.0441), unjammed (floating A).
  The near-slot pocket (A axis-aligned at offset 0.01, B flush on top rotated 0.3° so its vertex
  dips into the gap): **unjammed — rotating B back to flush lifts the vertex out of the slot
  under the caps** (exactly TF-U's motion; consistent with Lemma JAM-0: the dip is ≤ g²/√(1−g²)
  = 1.0·10⁻⁴). Trump's TL crowd in the BL frame: library-JAMMED (stacked-dipping-vertex) — the
  model is not vacuously permissive.
* **Depth.** depth = 1 − f_min_max in the corner frame (exact). Of the 644 sound boxes, 84 cannot
  reach the open slot at all (widened-box artefacts); deep-capable boxes 523 / 449 / 378 / 289 /
  146 (81 / 70 / 59 / 45 / 23 %) at δ = 0.05 / 0.1 / 0.2 / 0.3 / 0.5; pairs with a deep-capable
  member 98 / 91 / 86 / 73 / 51 %; **pairs with BOTH members deep-capable 44 / 18 / 8.8 / 1.2 /
  0 %** — no census pair can have both members intruding ≥ 0.5 (a tilt-independent pair prune).
  A87's 644 met corners: DEPTH < 0.05 / 0.1 / 0.2 / 0.3 at 19 / 40 / 87 / 115 corners (17.9 %
  shallow at δ = 0.3); of the 132 blockers at shallow corners 69 (52 %) are axis-aligned — the
  shallow regime is case (iii), not tilted ghosts. Atlas: no blocker depth in (0.2, 0.5). **Trump:
  DEPTH(TL) = 0.16832098954974430… (sq6; sq4 0.15547), other three corners 1** — a shallow
  2-crowd next to three slot corners.

**8.6 The certification holes of A85's depth-2 FAILs (A89-O3 diagnostic D, exact,
`o3_report.md` §D).** For every witness box of the two FAILed k0_00 depth-2 certificates
(p215_011: 32 boxes, 6 holes + 26 undecided; p210_001: 40 boxes, 8 + 32; and their eps_geo
variants, 184 boxes in all) the corner-frame reach g_c(B) = min over the box of f_c (exact
monotone corner + Lipschitz pad) decides whether the box holds a corner pose and at what
intrusion depth. Base certificates (72 boxes): **48 corner poses (67 %), of which 8 (11 %) in
the ghost zone (tilt < 2°), and 24 interior / mid-tilt (33 %)**; all six variants: 136 / 16 / 48
of 184 (74 / 9 / 26 %). The ghost-zone boxes are exactly two configurations, both WALL-FLUSH
UPRIGHTS pressed against the left wall (c_x ≈ 0.504–0.506) tilted 0.46° (p210, TL, depth
0.0078) and 0.70° (p215 eps_geo 0.004, BL, depth 0.152) — the PI's zone in its purest form,
but a minority of what fails; the bulk is mid-tilt (22–44°) corner poses at depth 0.002–0.25 and
interior boxes. A50's θ* = 1.73° would clip both; a δ = 0.05 SHALLOW branch excludes the TL one
only; δ = 0.3 puts both in the SHALLOW branch. (p210_001 is in fact killed at eps_geo 0.004 —
verifier PASS, 0 holes — so A85's f₂ at the A60 defaults is 2/3 on the three depth-2 cells,
not 1/3; the residual FAIL is p215_011 at every margin.)

**8.6′ The shallow-corner certificates (A89-O3, `code/o3fam.py`, `o3run.py`; engine = A85's
stack copied verbatim).** The NO-family for SHALLOW(δ) at corner c is R_c(a) = {(c_Q, θ): int Q
meets (0, a)²}, realised as a sound INNER union of 108–112 caselp `NoFam` boxes per corner
(exact Fractions: f is monotone in the centre and (√2/2)-Lipschitz in θ; 7 θ-bins with edges at
multiples of 1/4°, widened by 0.5° > EPS_TH so the eroded bins still tile; every family's
rigorous max f < a with margin ≥ 2·10⁻⁴; the union covers 89–92 % of R_c(a) by exact sampling,
the loss being the θ-binning). Window form a_win = (1 − δ)/λ_max, λ_max = 969271/955000
(Lemma B-NO: occupancy transfers with the zone contracted by 1/λ; also sound under K0-WIDEN's
centre-dilation reading since a_win ≤ 1 − δ): δ = 0.3 / 0.1 / 0.05 → a_win = 0.68969 / 0.88675 /
0.93601. **Canary [M, exact]:** every D4 image of Trump has exactly one corner of depth
0.168300 and three of depth 1; hence 1-SHALLOW(BL) at δ ≥ 0.1683 is image-realisable (g2, g6)
and the engine REFUSED it (`R4_1shallow_BL_d0.3 → REFUSED (CANARY: realised by g2, g6)`, no
LP), while every 2-, 3-, 4-SHALLOW pattern contains a depth-1 corner of every image and is
attemptable. Baselines: the plain k0_00 root is unkillable at 3.833212 (A82: τ = 10.99999999982,
hence at s₀) and killed at 3.82 with no exemption (A07/A08 row-only root τ = 10.7159). Results of
R1–R3 (4-, 3-, 2-shallow at δ ∈ {0.3, 0.1, 0.05}, window form, certified with the frozen
verifier): §8.6″.

**8.6″ [CERT] The shallow-corner certificates (`o3_report.md` §A–B; `results/o3_runs.jsonl`,
`certs/k0_00/`).** Root node at s₀, budget 11, no pins/cores, hypotheses = the SHALLOW(δ)
NO-families only; verdict = the frozen `certify.py → verify_case.py` chain (exact rationals,
depth 56, witness feedback, eps_geo 0.002/0.004 repair).

| run | pattern | δ | a_win | exempt boxes | sym | τ | η | LP s | cert s | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| R4 | BL | 0.3 | 0.68969 | 108 | C1 | — | — | 0 | 0 | **REFUSED (canary: g2, g6 realise it)** |
| R1 | all four | 0.3 | 0.68969 | 432 | D4 | 9.5547 | −1.445 | 1 042 | 1 008 | **PASS** — exact total 1372003/125000 = 10.976024 < 11; 220 140 boxes, 2 528 exempt, 0 holes; re-verified independently (85.9 s, rc 0) |
| R2 | BL+BR+TR | 0.3 | 0.68969 | 324 | C1 | 10.0461 | −0.954 | 994 | 2 566 | FAIL (7/16/12, 12/5/19, 18/5/24 holes at eps_geo 0/0.002/0.004; feedback rounds raise τ to 10.209, total 10.975) |
| R2′ | BL+BR+TR | 0.1 | 0.88675 | 336 | C1 | 9.2228 | −1.777 | 936 | 3 202 | FAIL (holes at every margin; minmass 0.58 after 900 s) |
| R2″ | BL+BR+TR | 0.05 | 0.93601 | 336 | C1 | 8.7264 | −2.274 | 910 | — | LP only (wall budget) |
| R3 | 2-shallow (adj / diag) | — | — | — | — | — | — | — | — | not run: τ(2-sh) ≥ τ(3-sh) at each δ, foregone |

**Certified bound (window-valid, every m ∈ [3.82, s₀], via a_win = (1−δ)/λ_max):** no
11-packing has all four corners SHALLOW(0.3) — some corner has DEPTH ≥ 0.3, i.e. a square
reaches within 0.7 of that corner point (min over Q of max(x_c, y_c) ≤ 0.7); by monotonicity
(SHALLOW(δ′) ⇒ SHALLOW(0.3) for δ′ ≤ 0.3) the same certificate discharges δ = 0.1 and 0.05.
**Not certified:** 3-shallow (R2: LP under C1 at the 900 s cap leaves minmass 0.58–0.61, and
τ CLIMBS with feedback at δ = 0.3 — a genuine near-boundary node; at δ = 0.1 η = −1.78 yet
the certificate still has holes, a budget artefact: the fix is lp_time ≥ 5 000 s, resumable
`code/o3_campaign.py`), hence 2-shallow untried. Canary exact: every Trump image has one
corner at DEPTH 0.168300 and three at 1, so 1-SHALLOW(δ ≥ 0.1683) is image-realisable and
was refused; every ≥ 2-corner pattern is not. Baselines: plain root unkillable at 3.833212
(A82 τ = 10.99999999982) and killed at 3.82 with no exemption (A07/A08 τ = 10.7159).

## 9. T3 — consumers, bookkeeping, Lean-readiness, re-price

**9.1 What the tree may use, and in which form.**
* Lemma ID's SHALLOW row: ∀-packings (a hypothesis on all squares), consumed as exempt boxes in
  (K) leaves; the DEEP branch is the crowd box census restricted to depth-capable boxes.
* Lemma JAM-0: an exact (C)-type coupling between the two crowd boxes of a corner when one is
  axis-aligned at offset g < 1/√2 (partner tilt bin must meet [0, arcsin g], partner depth ≤
  g²/√(1−g²)) — ∀-packings, no selection.
* Theorem TF-U: SelForm leaves — "(C-sel): the conditioned square has tilt ∉ 90°ℤ on the whole
  (widened) box and no other square's box can reach its far-side set (Lemma MENU / LOCK)" —
  free at deep nodes (all squares localised), silent at the crowd level (the three free squares
  can always be the supporter), exactly K0-ROT's status. Consumers: the lower bound through the
  Φ-minimal σ-minimiser (TF-U over M(m)); the uniqueness clause at ŝ through the Φ-minimal
  NON-IMAGE packing (TF-U (ii)), which needs the basin isolation of the images (E.A36, already
  in the TCB) — no Theorem-U chain and no k-maximal selection.
* A loaded floor θ₀ (GAP A89-G1) would delete (0, θ₀) ∪ (90 − θ₀, 90) from every blocker box
  — MinForm (an FJ statement about minimisers), consumed as D4-symmetric bin clipping; with
  θ₀ = 1.7347° that is 3.4 % of the tilt volume and no node (8.4).

**9.2 K1 / aliveness bookkeeping.** A box with tilt exactly 0 (t₀ = t₁ = 0) and centre box not
containing the slot centre is a k0_00 box (its poses are axis-aligned offset squares, skeleton
∅); a tilt-0 box whose centre box contains the slot centre contains k ≥ 1 poses and is the
K0-REUSE pocket (k1_00's tree). The alive gate over the eight images is unchanged: images have
tilt-0 corner squares at the slot, so a box with tilt ⊂ [θ₀, 90 − θ₀] is never image-realisable
and the canary (a node realised by an image within 10⁻⁵ is never certified) is not triggered by
clipping; the rotational ghosts R_φ ẑ (|φ| ≤ 1.06·10⁻⁷) have all tilts in (0, θ₀) but side
> ŝ, so they are outside every MinForm/SelForm hypothesis and inside the (D) landing radii.

**9.3 Lean-readiness.** TopLevel axiom fed: `stratum_kill` (C.K4TIER, k0_00 part), in the split
form `StratumKillMin` (A86 `Composition.lean`) for MinForm leaves; TF-U leaves need a third
form, `StratumKillSel`: for z a σ-minimiser that is Φ-minimal among σ-minimisers (lower bound)
resp. Φ-minimal among non-image packings at ŝ (uniqueness), z ∉ k0_00 unless a Trump image.
New Lean obligations: (S1) compactness of M(m) and of the non-image set at ŝ (the latter via
the basin radius, `RigidBasin`/E.A36 interface), (S2) continuity of Φ (tilt is a continuous
function of t = tan(θ/2)), (S3) `IsCompact.exists_isMinOn` to pick z*, (S4) the two consumers
`s_eleven_ge_of_sel`, `s_eleven_unique_of_sel` (one `obtain` each), (S5) the leaf rule
`(C-sel)` as a checker clause: interval evaluation of Lemma MENU's far-side zone against the
other squares' boxes (no derivative; the rotation about O is a rational motion). Lemma ID
needs only the exempt-box clause of `MeasurePy` (present) and the dilation bookkeeping of
K0-WIDEN. Lemma JAM-0 is a closed-form inequality in (a, b, t) — a `native_decide`-free
`nlinarith` target. The DF-K0 hypothesis (criticality) is used only through D3′ at the
selected minimiser, as in Lemma F-LEAF.

**9.4 Re-price (A85's measured per-node constants, `k0_route.md` §7–8).** The priced route is
the interior-first tree: N₂ = 1 728 depth-2 cells at 1 000 s LP + 630–860 s certification,
f₂ = 1/3 first pass (0.85 with repairs), (D)-side 150 CPU-h, ghosts 1 h. What this attempt
changes: (i) the loaded floor is NOT available; had it been, at θ₀ = 1.73° it deletes 0 of the
FAILs and 0 pair boxes (8.3–8.4) — **no price effect**; at θ₀ = 10° (a floor the corpus would
support but nothing proves) 31 % of the crowd pair boxes die, which touches the (T)/(C)-crowd
conditioning below the frontier (≤ the (D)-side 150 CPU-h ⇒ ≤ 50 CPU-h) and not the frontier.
(ii) TF-U's (C-sel) leaves: deep-node rule, no frontier effect (K0-ROT's verdict). (iii) Lemma
ID: the corner-first tree replaces the K0-BLOCKED seed (dead as a cover, A85 §8.4 C3) by a
depth branching: 2⁴ shallow/deep patterns per D4 orbit (≤ 6 representatives); the all-shallow
and 3-shallow nodes are one measure certificate each with exempt boxes (minutes); a DEEP corner
costs its depth-capable box census — T2b counts the depth-capable fraction of the 644 boxes and
of the 33 656 pairs (§8.5); the residual per deep corner is a crowd-pair census of that size
at budget 9, which A85 §7.2 measured at 1.3·10⁴ CPU-h for the FULL pair set at level 1 alone
(2.8·10⁴ attemptable nodes at 1 700 s), i.e. the corner-first tree is affordable only if the
depth-capable fraction at the chosen δ is ≪ 1/10 AND the deep-corner pair nodes decide at
budget 9 (unmeasured: A85's S2–S5 rows never ran). **Verdict: k0_00 stays at 3 200–7 000 CPU-h
(f₂ ≈ 0.85) / ≥ 3·10⁴ (f₂ = 1/3), unchanged; the near-flush ghost zone is not where the measured
cost is, and the tilt floor that would delete it is a global statement without a proof.**

**Caveat on the evidence base [F].** "Not where the cost is" rests on A85's 12 LP rows, and 4 of
its 5 FAILs are A38-comparison INTERIOR cells (level-1 / depth-2 cells of the fundamental
triangle), not corner-crowd nodes of the k0 tree; the single corner FAIL (b178, 41–49°) is an
image-adjacent resister, and the 14 planned crowd nodes (S2–S5) never ran. A proper measurement
needs (a) the crowd-level rows: ≥ 20 S2–S4 pair/multi-corner nodes with certification in the
loop, stratified by the tilt bin of the crowd boxes (end bins [0, 7.125°]/[82.875°, 90°] vs the
rest), so the FAIL rate per tilt bin is measured rather than inferred; (b) the HOLE census: the
witness/hole boxes of every certification FAIL classified by pose (corner box met? tilt in
(0, 2°) ∪ (88°, 90°)?) — A89-O3's diagnostic D does this for the two depth-2 FAILs on file (§8.6);
(c) the same at one lower side (3.82 via A82's side-parametric emitter) since the floor, if
true, is side-dependent. Cost: ≈ 20 × 1 700 s ≈ 10 CPU-h at one slot. Until then the re-price is
"no measured effect", not "no effect".

## 10. Obligations ledger

| # | item | status |
|---|---|---|
| A89-O1 | Theorem TF-U (selection form; rattler/unlocked branch; both consumers) | [T] §3 |
| A89-O2 | Lemma LOCK, Lemma MENU (far-side set), Lemma JAM-0 (partner pinning) | [T] §2, §4, §5.1 |
| A89-G1 | loaded floor θ₀ > 0 for flush-locked blockers at side ≤ ŝ | **OPEN** — no local proof (§5.2); conditional θ* = 1.7347° for binding-P-chain members (A50 T2.1, H-P/H-MONO/H-L6CAP); empirical 23.89° |
| A89-O3 | Lemma ID + budget row; 4-shallow / 3-shallow kills as NO-family case-LP certificates | [T] lemma; [CERT] 4-shallow at δ = 0.3 window-valid (`certs/k0_00/R1_4shallow_d0.3.json`, frozen verifier PASS, re-verified); [C] 3-shallow (LP time, resumable), 2-shallow untried |
| A89-O4 | T2 census (167 + 12 + Trump; A85 rows and boxes) | [M] §8, canary PASS |
| A89-O5 | T2b reach / self-jam / depth-capable census; O3 hole diagnostic | [M] §8.5, §8.6 |
| A89-O6 | Lean: `StratumKillSel` + S1–S5 | [C] readiness note §9.3, no `lean/` edits |
| A89-O7 | re-price | [F] unchanged §9.4 |
