# TWO GRAINS and the CLICK — Lemma TWO-GRAIN, Lemma CLICK, Theorem FOUR-WALL, Conjecture SEAM — A223, 2026-09-14

The PI's picture (A223 BRIEF, 21:10): the ring `rand_0_0569|t20` is two half-rings of OPPOSING tilt (2,3,4,5 at 70°;
6,7,8,10 at 20°) balanced against each other at the top middle (3|9|10) and the bottom middle (4|6); the two squares leaning
on each other at the bottom would CLICK DOWN and sit flush unless something above pins them; so a self-supporting k0 structure
needs two opposing GRAINS with grain boundaries on all four walls, and a grain-boundary minimiser collapses every boundary to
flush but a single diagonal SEAM.  This file makes each piece exact.  Tags: [T] proved, [S] routine given cited items, [M]
measured, [F] false as stated (with the witness), [C] conjecture / obligation.  Sources: `grain_flood.md` (Lemma GRAIN-LP,
Lemma GRAIN's chain form, Theorem CONT, Lemma INHERIT, the chain menu Λ, Y, D, F_T), `descent.md` Theorem D3, `descent_grains.md`
§4–6, `wall_torque.md` (Lemma W = A217's wall-torque identity, TWO-CONTACT, ONE-TILTED, CEIL), `k0_count.md` (PUSH, HOLD),
`ring_swap.md` (SWAP, CELLS, RAISE), A217's witnesses.  Code `attempts/A223-two-grains/code/` (`grains223.py`, `click223.py`,
`summarise223.py`, `pages223.py`, `test223.py`), results `results/click223.md`, `click223.jsonl`, `grains223.jsonl`; pages
`docs/residue_map/campaigns/A223-two-grains/`; Lean `Statements/Open/TwoGrains.lean`.  n-general throughout; n = 11 in the
corollaries.  Handedness of a unit square of tilt θ: φ = θ mod 90° and h = '+' for φ ∈ (0°, 45°), '−' for φ ∈ (45°, 90°),
'D' at 45°, 'F' flat.  Rotations of the container preserve h, reflections swap '+' and '−' [T: θ ↦ θ + 90° and θ ↦ −θ].

## 0. Verdict

> **[T] Lemma FLUSH (any n): a packing of n AXIS-ALIGNED unit squares has side ≥ ⌈√n⌉** (§3.1; n = 11: ≥ 4).  **[T] Theorem
> FOUR-WALL, conditional:** if a teleport-stuck packing (every corner box met by ≥ 2 squares) admits a click-down — a flush
> packing at a side no larger than its own — then its side is ≥ ⌈√n⌉; at n = 11 no such packing exists in the window, and
> STUCK-4 ("every teleport-stuck 11-packing has side ≥ 4") implies A222's RAISE(0 → 1) and, with k1-a, empties k0_00 (§3.3).
> **[C] The click-down itself is the whole obligation, and it is EQUIVALENT to STUCK-4** (§3.2: above side 4 the grid is a
> flush packing at 4 ≤ m, so CLICK-DOWN says nothing there, and below 4 it is the kill by FLUSH).  **[M] On the ring the PI's click
> is real**: both grains rotated jointly toward alignment (70° → 90°, 20° → 0°), the side minimised over the centres at every tilt
> step with all 15 contact axes kept, descends MONOTONICALLY 4.1099 → 4.0000 and the lean contact 4|6 slides on 6's edge the
> whole way (page `ring_click_rand_0_0569_t20.svg`).  **On all 193 four-crowds**: never blocked (0 / 193); the free variant
> reaches 4.000 from every one, never above its start, non-increasing at every step on 167 / 193; the contact-kept variant ends
> at 4.000 on 187 and at 5.000 on 6 (the fixed axes force a bad flush arrangement).  Every witness lives at S ≥ 4.0014, so this
> tests the MECHANISM (lean contacts slide, rattlers do not block), not STUCK-4 below 4, where the conjecture asserts emptiness.
> **[F] "The chain formula decreases toward alignment"**: the corner-anchored ladder Λ(θ) = 2 + 4t/(t² + 1) is MINIMAL at 45° and
> rises to 4 at alignment (§2.3); the ring's own two ladders do decrease (§2.4), so monotonicity is a property of the load path's
> TYPE, not of grains.  **[F] Lemma TWO-GRAIN as a geometric statement**: 12 of the 193 four-crowds have ONE grain meeting all
> four corners, 68 have a single handedness class among their loaded tilted squares (`w062_crowd`: all eleven squares '+', one
> contact component, side 4.031) — held by the crowd rows, not Fritz-John points of the free problem; **[C] at a free FJ point**
> (RING's setting) the exclusion is untested, no such point exists among the witnesses.  What IS proved of TWO-GRAIN: the
> handedness calculus, Lemma W's sign (every wall torques a grain toward its own alignment), the torque identity with its
> circulation term, and Lemma CORNER-LOAD (the frame-handedness of a loaded corner decides whether its load runs along the floor
> or up the wall; the ring's bottom corners are floor-loaded, its top corners wall-loaded, and the floor pair 4|6 is therefore a
> LEAN of opposite global handedness) (§1).  **[C] Conjecture SEAM** stated (§4): consistent with n = 5, 10 (Göbel strips: one
> 45° strip between two staircases), 11 (Trump: one 40.18° strip), 19 (one double 45° band, the ladder value 3 + 4√2/3); n = 17
> (Bidwell, several tilts) and 18 (Hämäläinen) unverified here.  **k0_00 is unchanged**: the route is STUCK-4, one geometric
> conjecture stronger than RAISE(0 → 1), with the click as its proposed mechanism and no test object below side 4.

## 1. Lemma TWO-GRAIN

**1.1 Grains [T, definition].**  Packing P of n unit squares in [0, s]², s > 1 + √2, at a Fritz-John point of NLP(S) with
multipliers λ ≥ 0 on the active rows (`k0_count.md` §1: a frictionless force network, every square in force and torque
balance).  A square is LOADED if some wall or pair row of it carries λ > 0; a pair contact is loaded if one of its rows is.  A
GRAIN is a connected component of the contact graph on the loaded squares (edges = geometric contacts, vertex-on-edge or
flush, between loaded squares) restricted to one handedness class; a BOUNDARY is a contact between squares of different grains
— LEAN when the two are tilted of opposite handedness, FLAT when one is flat, DIA when one is a diamond.  A flush contact forces
equal tilts, hence equal handedness [T]; a vertex-on-edge contact does not.  The code takes the loads from A219's bounded FJ
stress (`rows219`); the adjacency by ALL geometric contacts among loaded squares (the PI's picture) or by the loaded rows only
(a basis choice: on the ring it splits the right ladder 6,7,8,10 into {6,7} and {8,10} because 7–8 is unloaded in the chosen
basis, `grains223.py --by-load`).

**1.2 Lemma W (the wall torques a grain toward its own alignment) [T, A217 §2].**  A square of tilt θ touching any wall with
total wall force W receives the torque τ = W (sin θ − cos θ)/2 about its centre, the same formula on all four walls (the wall
normal and the extreme vertex rotate together): τ < 0 (clockwise, toward θ = 0) for '+', τ > 0 (toward 90°) for '−', 0 for 'D'
and 'F'.  So every wall contact of a '+' grain torques it clockwise and every wall contact of a '−' grain counter-clockwise.
*Proof.* Floor: the lowest vertex is c + R(θ)(−½, −½), abscissa offset (sin θ − cos θ)/2, force (0, W); the other walls by
rotation. ∎

**1.3 Lemma TORQUE-ID (the circulation term) [T].**  At an FJ point the wall forces alone are in moment balance about the
container centre O (pair forces cancel pairwise at their common point): Σ_wall (v − O) × F = 0.  Writing (v − O) × F = (v − c) × F
+ (c − O) × F, Σ τ_self + Circ = 0 with Circ = Σ_floor W x̃ + Σ_right W ỹ − Σ_ceil W x̃ − Σ_left W ỹ (x̃, ỹ the centre's
coordinates from O).  If every loaded wall square has handedness '+', Σ τ_self < 0 by Lemma W, hence Circ > 0: the wall forces
circulate counter-clockwise (they act preferentially on the right half of the floor, the top half of the right wall, …).
[F] This is NOT an obstruction by itself: nothing bounds the circulation, and the one-grain witnesses of §1.5 realise it.

**1.4 Lemma CORNER-LOAD (frame handedness decides the load direction) [T].**  Corner c with meeters A (NW cell, touching c's
wall) and B (SE cell, touching c's floor) in loaded contact; by Lemma PUSH (ii) the separating normal has n_u > 0, n_v < 0 in
the corner frame, and n is an edge normal of the OWNER, so its frame angle is φ_o − 90° with φ_o ∈ (0°, 90°) the owner's frame
tilt.  Hence |n_v| > |n_u| iff φ_o < 45°.  So: owner of frame handedness '+' ⇒ B is pushed mostly INTO the floor and A mostly UP
the wall (A needs a strong along-wall holder from above: a WALL-loaded corner); owner '−' ⇒ B is pushed mostly ALONG the floor
away from c and A mostly into the wall (B needs a strong along-floor holder: a FLOOR-loaded corner).  Frame handedness equals
global handedness at BL and TR and is swapped at BR and TL [T, 1.0].  *Corollary [T].* If BL and BR are both floor-loaded corners
whose floor meeters hold each other directly (the contact BL-floor-meeter – BR-floor-meeter loaded along the floor, Lemma HOLD's
holder being the other corner's meeter), the two floor meeters have OPPOSITE global handedness and their contact is a LEAN
boundary.  On the ring: BL, BR at frame tilt 70° (floor-loaded: 4 and 6 hold each other, `k0_count.md` §5), TR, TL at frame
tilt 20° (wall-loaded: 5|2 and 7|8 hold each other up the walls), and 4|6 is the LEAN with 4 at 70°, 6 at 20° (page
`ring_grains_rand_0_0569_t20.svg`).

**1.5 The exclusion clause [F as geometry, C at free FJ points; M].**  Claim (brief): the corner meeters of a teleport-stuck
packing cannot all belong to one grain, so ≥ 2 opposite-handed grains meet at internal boundaries.  Measured on the 193 HELD /
CROWD four-crowds (`results/click223.md` §1): both classes present 121 / 193; a single class 68 / 193; a grain meeting all four
corners 12 / 193 (`w062_crowd`, `w103_crowd`, `w301_held`: every square '+', one component; `w104_crowd`, `w134_crowd`: all '−');
grains' wall contacts covering all four walls 140 / 193; ≥ 1 LEAN boundary 114; ≥ 1 flat-mediated boundary 147.  So as a statement
about packings with four doubly-met corners the clause is FALSE — a one-grain four-crowd is a perfectly good packing.  What the
brief means is a four-crowd that is force- and torque-balanced by walls and contacts alone (RING's setting, `wall_torque.md` §4);
every witness fails that (free FJ LP infeasible 193 / 193, A219), so the clause is untested there and stays [C].  The wall-cover
clause is [T] under the hypothesis that at every corner both meeters touch their walls (Lemma A2's NW/SE cells put one on each
wall of the corner, and the four corners' walls are the four walls) and [M] 140 / 193 otherwise.

## 2. Lemma CLICK

**2.1 The move [T, definition].**  For a packing P with tilts θ_i put φ_i = θ_i mod 90° and the CLICK path θ_i(t), t ∈ [0, 1]:
φ_i (1 − t) for '+', 90° − (90° − φ_i)(1 − t) for '−', flat squares fixed, diamonds assigned a sense (both tried).  A grain of
common tilt rotates as a unit (Theorem D3's common-tilt move); the two handedness classes rotate in opposite senses.  The side
along the move is s_min(θ(t)) = min over centres of the side at the tilts θ(t) — by Theorem CONT (`grain_flood.md` §3.1) a
continuous function of t [T] — and the click is SIDE-NON-INCREASING iff s_min(θ(t)) is non-increasing.  At t = 1 every square is
flat and s_min ≥ ⌈√n⌉ (Lemma FLUSH).  The computed object (`click223.py`): at each of 21 tilt steps the alternating LP over the
polyhedron P(S, θ(t)) of Lemma GRAIN-LP (rows affine in the centres at fixed tilts; the separating axis of each pair re-chosen at
the LP's solution until stable, warm-started from the previous step) — a fixed-tilt LOCAL minimum, in three variants: A the
witness's contact pairs keep their t = 0 axis (the lean contact SLIDES on its edge: the PI's click), B every axis free, C variant
A on the loaded squares with the rattlers removed and re-fitted flat at the end (Lemma SWAP at the end side).

**2.2 Lemma EXTENT [T].**  The projected extent of a unit square along an axis is cos φ + sin φ = √2 sin(φ + 45°), strictly
decreasing toward alignment on each side of 45°.  Hence a chain of Lemma GRAIN all of whose members contribute their full
projected extent (vertex-to-vertex kisses, wall vertex to wall vertex; no gap terms) has s = Σ_j (cos φ_j + sin φ_j), strictly
decreasing along the click until the members are flat, where it equals the number of members.  ∎

**2.3 [F] "The chain formula decreases toward alignment" in general.**  The corner-anchored ladder of `grain_flood.md` §2.1/2.3 —
two flush rows of tilt θ between a slot square's face and a slot square's corner — has Λ(θ) = 2 + 4t/(t² + 1), t = cos θ + sin θ:
Λ(45°) = 2 + 4√2/3 = 3.8856 and Λ(0°) = 4, INCREASING from 45° toward alignment on both sides (d/dt [4t/(t² + 1)] ≤ 0 on
t ∈ [1, √2]).  Likewise Trump's gap chain F_T(θ) = 2 + (2 + sin θ)/(cos θ + sin θ) increases on θ > 24.3°.  The gap terms τ_j e·t_j
of vertex-on-edge contacts and the anchors' constants are what turn a chain formula up.  So Lemma CLICK's "side-non-increasing
because the chain formula decreases" holds for extent-type chains (2.2) and fails for anchored / gap chains; the click's
monotonicity is a property of the LOADED chain's type and is decided per packing by s_min(θ(t)), not by grains.

**2.4 The ring's two chain formulas [T + M].**  Strip coordinates u = c·(cos θ, sin θ), v = c·(−sin θ, cos θ) at the grain's
tilt.  Left grain (θ = 70°): 4–5 flush along v (v_5 = v_4 + 1, u_5 = u_4 + σ₀), 5–2 and 2–3 flush along u (u_2 = u_5 + 1, u_3 = u_2
+ 1, v_2 = v_5 + σ₁, v_3 = v_2 + σ₂), 4's lowest vertex on the floor, 3's highest on the ceiling.  Telescoping (Lemma GRAIN, e =
e_y):  **s_G−(θ; σ) = (cos θ + sin θ) + (2 + σ₀) sin θ + (1 + σ₁ + σ₂) cos θ**, with the measured offsets σ = (0.476, 0.350,
0.116): 1.2817 + 2.3270 + 0.5013 = 4.1099 = the witness's side [M, exact to 1e-6].  Its θ-derivative at 70° with σ held is
−sin θ + cos θ + (2 + σ₀) cos θ − (1 + σ₁ + σ₂) sin θ = −1.13 rad⁻¹: DEcreasing toward 90°.  Right grain (θ = 20°, mirror): 6–7
flush along (cos θ, sin θ), 7–8 and 8–10 flush along (−sin θ, cos θ):  **s_G+(θ; σ′) = (cos θ + sin θ) + (2 + σ′₀) cos θ + (1 +
σ′₁ + σ′₂) sin θ**, decreasing toward 0°.  The offsets are NOT constants of the motion — they are fixed by the other contacts (the
wall contacts of 5, 7, the lean 4|6, the flat holder 9) — which is why the side along the click is the LP value and not either
formula: [M] the LP path 4.1099 → 4.0000 (21 steps, monotone, `click223.md` §3) against the σ-held formulas.

**2.5 Lemma LEAN-SLIDE (feasibility across a lean boundary) [T].**  Let B's vertex v sit on A's edge (normal n_A, tangent t_A),
A and B of opposite handedness rotating in opposite senses along the click, centres free.  The contact row g = n_A(θ_A)·(v(θ_B, c_B)
− c_A) − ½ is affine in (c_A, c_B) at every t with coefficient ±n_A ≠ 0, so for any tilts there are centres with g ≥ 0 and the
vertex at any tangential coordinate τ ∈ [−½, ½] on the edge: a single lean contact NEVER blocks the click; it slides.  The click
along the fixed-axis polyhedron fails at t iff P(S, θ(t)) = ∅, a GLOBAL condition: a closed cycle of contact and wall rows that
cannot all hold at side ≤ s̄ — (i) a pin above: a load path through the boundary whose rows lengthen faster than the far wall can
recede; (ii) a rattler caged in a pocket whose rows are in P(S, θ) though unloaded; (iii) a non-touching pair whose t = 0
separating axis is no longer separating (released in variant B).  ∎  [M] On the 193 witnesses P(S, θ(t)) was NEVER empty (0
blocked in A, B, C): no pin above and no rattler blocked any click; rattlers moved aside by SWAP were not needed (variant C's
core clicks to 4.000 on all 104 witnesses with rattlers; the flat re-fit of the rattlers into the clicked core's free space
succeeded on only 6 / 104 because the core's LP minimiser at side 4 is not grid-aligned — but variant A with the rattlers kept
reaches 4.000 on 187 / 193 and B on 193 / 193, so the re-fit is moot).  What DOES fail is monotonicity: A rises above its
start on 6 / 193 (to 5.000: the fixed axes force a bad flush arrangement), B never rises above its start (0 / 193) but has
small upticks after a descent on 26 / 193 (≤ 0.032; a warm-started local branch turning up, Lemma INHERIT (iii)); page
`click_worst_w156_crowd.svg` (A's largest uptick 0.13; B monotone to 4.000 on that witness).  Time: 297 s for the 193 (1.5 s
per witness, 63 LPs each).

## 3. Theorem FOUR-WALL

**3.1 Lemma FLUSH (any n) [T].**  A packing of n axis-aligned unit squares in [0, s]² has s ≥ ⌈√n⌉.  *Proof.*  Put k = ⌈√n⌉ and
suppose s < k.  The bottom edges b_i ∈ [0, s − 1] ⊂ [0, k − 1) fall into the k − 1 classes b_i ∈ [j, j + 1), j = 0, …, k − 2.  Two
squares of one class have |b_i − b_i′| < 1, so their y-intervals overlap in a set of positive length and their interiors
overlap unless their x-intervals are interior-disjoint: a class is a family of interior-disjoint unit intervals in [0, s],
hence has at most ⌊s⌋ ≤ k − 1 members.  So n ≤ (k − 1)², but (k − 1)² < n since k − 1 < √n. ∎  Corollary (n = 11): ≥ 4.  Lean:
`lemma_FLUSH` (axiom, prose proof above), `flush_eleven_four` (theorem via `ceil_sqrt_eleven`).  Sharp: the grid attains it.

**3.2 Conjecture CLICK-DOWN and its content [C, T].**  *CLICK-DOWN(n)*: every teleport-stuck packing P (every corner's open unit
box met by ≥ 2 squares) at side m admits a flush packing at some side m′ ≤ m.  *STUCK(n)*: every teleport-stuck packing has
side ≥ ⌈√n⌉.  [T] CLICK-DOWN ⟺ STUCK: (⇒) FLUSH; (⇐) at m ≥ ⌈√n⌉ the grid is a flush packing at side ⌈√n⌉ ≤ m, and below there
is nothing to click.  So the conjecture carries no content above ⌈√n⌉ and IS the kill below it; the click PATH is a proposed
proof mechanism — what would have to be proved is that from every stuck packing some tilt path has s_min(θ(t)) ≤ m throughout
(monotonicity is more than needed: ≤ m at t = 1 suffices).  [M] The 193 four-crowds all start at ≥ 4.0014 and all click to
4.000: the mechanism works where the conjecture is vacuous; there is no stuck packing below 4 to test it on (A217: the lowest
four-crowd local optimum of any kind is 4.0014, every k0 local optimum below 3.9 drains to a settled corner).

**3.3 Theorem FOUR-WALL (conditional) [T].**  CLICK-DOWN(n) ⇒ every teleport-stuck packing of n squares has side ≥ ⌈√n⌉.  At
n = 11: ≥ 4 > ŝ, so no teleport-stuck packing exists in the window [3.82, ŝ] (Lean `four_wall`, `no_stuck_in_window`; pure
logic over `click_down` and `lemma_FLUSH`).  Consequences [T]: a packing at m < 4 then has a corner met by ≤ 1 square, which
K0-FREE teleports to a slot square (`teleport_packing`): **STUCK(11) ⇒ RAISE(0 → 1)** on the whole window (`ring_swap.md` §1.5,
axiom `raise_zero_one`) ⇒ with k1-a (the k1_00 tree) k0_00 is empty (`no_packing_of_raise`).  No force argument, no load
hypothesis, rattlers included: the corner box's meeters may be rattlers.  What closes for k0_00: nothing yet — the obligation
RAISE(0 → 1) is replaced by the stronger STUCK(11), whose proposed proof is the click; what the click needs is a monotonicity
theorem for s_min(θ(t)) from a stuck packing, which §2.3 shows cannot come from grains alone (anchored chains rise toward
alignment) and §2.5 shows is the feasibility of one polyhedral path.

## 4. Conjecture SEAM

**Statement [C].**  For every n with s(n) < ⌈√n⌉, every optimal packing consists of flush squares and ONE tilted grain (all
tilted squares contact-connected, one handedness or 45°), whose boundary with the flush part is a single diagonal band — one
seam, or a split of two parallel boundaries centred on a diagonal — and the flush part is two staircases (or corner blocks) on
either side; the grain's tilt is the kink minimum of its chain formula against the seam's anchors (S07 = Λ ∧ Y, S02 = Λ ∧ A,
Trump = F_T ∧ the lifted-column chain, `grain_flood.md` §2).  **Check against the record packings** (Friedman's survey /
Ellsworth's page, read 2026-09-14): n = 5 (Göbel, 2 + √2/2, proved) and n = 10 (Göbel, 3 + √2/2, Stromquist 2003): the GÖBEL
STRIPS — a 1-wide diagonal strip of 45° squares between two flush staircases and two corner squares, n = (a + 1)a + 2 + b, s =
a + 1 + √2/2 (a = 1, 2): ONE seam ✓.  n = 11 (Trump, 3.8771, degree-8 root): five squares at 40.18° in one strip between the six
flush squares: ONE seam of one handedness ✓, the tilt off 45° because the seam's anchors are a corner-in-gap and a lifted
column.  n = 19 (Cottingham / Wainwright, 3 + 4√2/3): the ladder value Λ(45°) + 1 — a two-row 45° band between corner blocks, one
seam with two parallel boundaries ✓.  n = 17 (Bidwell 1998, 4.6756, degree-18 root, several tilts) and n = 18 (Hämäläinen 1980,
7/2 + √7/2; Gustafsson's variant with fewer rotated squares): structure not verified here — the Göbel strip a = 3 (n = 17, side
4.707) is beaten by Bidwell's, so at n = 17 the single 45° seam is NOT optimal and SEAM would need Bidwell's packing to be one
seam at another tilt (open).  **What SEAM would give**: a two-stage proof shape for every n — (i) STUCK(n) kills every
teleport-stuck packing (no seam at all), (ii) among packings with a settled corner the minimiser is a single seam, so the class
census reduces to one-seam families and their chain formulas (the menu of `grain_flood.md`): for n = 11 that is the protected
tier and Trump's tube.  **What it needs**: (i) STUCK(n) (§3) and (ii) a "two seams cost more than one" exchange — moving a second
grain's squares into the flush part at no side cost — which is Lemma SWAP with a chain-formula price, [C] with no candidate proof.

## 5. Lean, files, obligations

`Statements/Open/TwoGrains.lean`: `IsFlatSquare`, `MeetsCorner`, `TeleportStuck`; `lemma_FLUSH` (axiom, [T] in prose),
`flush_eleven_four` (theorem), `click_down` (axiom [C]), `four_wall`, `no_stuck_in_window` (theorems); `lake build` and
`lean/audit.py` exit 0, no sorry.  Lemma TWO-GRAIN (1.2–1.4) and SEAM are prose over the FJ multipliers.  Obligations: O-FLUSH the
interval pigeonhole in Lean (routine); O-STUCK the conjecture; O-LINK `raise_zero_one` from `click_down` (needs the identity
of `cornerBox m 1 c` with the slot box of `⟨c, 0, 0⟩`, routine).  Code and results as in the header; the click run is complete
(193 / 193 rows) and resumable (`click223.md`, resume block).
