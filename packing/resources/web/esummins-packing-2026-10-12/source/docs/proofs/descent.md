# DESCENT — how much a non-simple corner hurts, and how a higher-k kill becomes a lower-k kill — A194, 2026-09-10

Target (A194 BRIEF; the PI's diagnosis of 2026-09-10 00:45): (1) CORNER HURT — a quantitative lemma on what a
packing pays at a corner or Young slot not occupied by a simple square, as a function of the two meeters' poses,
in a form the LP consumes and a form the geometry consumes; (2)–(3) the DESCENT THEOREM: class k+1 (or a grain's
completion) dead on the window ⇒ what is dead in class k; the cleanest true version, the counterexample to the
stronger one, the certificate it emits.  Grains and their precomputation: `descent_grains.md`; the worked examples
(l1_104, c0_Y1033): `descent_examples.md`; picture `docs/residue_map/descent.svg`.  Labels: [T] proved here or by
the cited lemma, [S] supported, [M] measured (`attempts/A194-descent/results/hurt194.json`), [F] false (with the
counterexample), [C] obligation.  Conventions: `sideband.md` (corner frame, meeter, Lemma A1/A2, Theorem B, lonely,
rows R1–R3), `k0_route.md` (K0-FREE, K0-WIDEN w = 0.025509, K0-BLOCKED, teleport), `forced_corners.md` (Theorem FC,
the pad π_i), `slot_crowds.md` (SLOT-CROWD, SLOT-SLIDE, ŝ′), `exchange_lemma.md` (Lemma X, EXPOSE, FLOOD-M),
`local_certificate.md` (Theorem LOCAL, DROP, L ∪ P), `local_certificate_s01.md` (Lemma CHORD-BAND, γ(θ)),
`guardline_clause.md` (LINE-1, MINCHORD).  n-general throughout: n squares, side window W = [s_lo, s_hi], any class.

## 0. Verdict

> **A non-simple corner forces NOTHING individually — no depth, no chord, no area beyond the sealed box — and
> everything jointly: it is a TRADE-OFF, and the trade-off is the descent.**  [T] Lemma CH (§2): at a corner met by
> two squares of depths d₁ ≥ d₂ > 0, (S) the packing converts, at side cost exactly d₂, into a packing whose corner
> is SIMPLE (rigid, ∀-packings, any corner, no cluster); (A) the open box (0, c_b − d₁)² is met by no square, so the
> corner wastes ≥ (c_b − d₁)² of area and the four corners together ≤ m² − n; (C) the meeters sit in distinct cells
> of the 2×2 grid at c_b, ℓ∞-apart ≥ 1/√2, each non-lonely (Theorem B), and the pair's pose set has non-empty
> 6-dimensional interior (K0-PAIR: no finite case list); (L) the BAND meeter carries a unit chord on every
> wall-parallel guard line within γ(θ) ≥ 0.2071 of its centre line, i.e. on a line at distance < c_b + 0.2071 from
> the wall it hugs — the chord a pin gives on every line at distance < 1.  Deep crowd ⇒ large obstacle and a deep
> unit chord; shallow crowd ⇒ waste (c_b − d₁)² and a CHEAP conversion.  Trump's TL crowd sits at (0.168, 0.155):
> a conversion cost of 0.155, exactly the side by which its k6 completion is worse than ŝ can afford [M].
>
> **Theorem D1 (conversion descent) [T].**  If T = S ∪ {p} is dead on [s_lo, s_T] then every S-packing at side m ∈
> [s_lo, s_T] has second-meeter depth d₂(p) ≥ s_T − m at p (k0 corners unconditionally; pinned slots by the cluster
> form of SLOT-SLIDE or, unconditionally, by the dilation form at cost 2 d₂ m and pin drift 2 d₂ A_S).  **This is the
> whole content of "class k+1 dead ⇒ class k"** and its yield is s_T − m: **zero at the top of the window while every
> extension is certified only to s0** (A109's measured zero, now with its reason), and at most s*_T − s0 once T is
> certified up to its own minimum — ≤ 0.0097 for trump5's TL(0,0) (S02 ⊃ k6_23), ≤ 0.0085 for BL(0,2) (S07),
> ≤ 0.052 for the others [M, gallery].  Counterexample to "T dead ⇒ S dead": Trump itself.
>
> **Theorem D2 (basin descent) [T] — the lever.**  A local certificate C = Dead_{L∪P}(N, s0) in T's frame, with p ∈ P,
> descends to S's frame as the SAME selection tree with the body p deleted and, at every leaf, the forced-cell
> requirement of p consumed geometrically: (a) if the tree closes without p (DROP) the node is dead outright;
> (b) a surviving leaf whose witness has a body ℓ ∈ L meeting p's widened box dies if ℓ's pose is LONELY there
> (Theorem B, the A173 clip on ℓ's box); (c) otherwise it dies if no partner square fits — LANE(B_p⁺ | L ∪ P∖p as
> obstacles) + [ℓ meets] ≤ 1 (A141/A161's exact lane cover) — and survives, as a genuine hole of the descended basin,
> when a partner is realised.  What it emits: a certified box set in the p-less frame in the `N_boxes` format with the
> clip and lane records, consumed by lookup (A136's YES leaf).  Counterexample to "basin in T's frame ⇒ basin in
> S's frame": A163's nine trump5 witnesses — of which, at the widened TL box, **[M] see `descent_examples.md` §7.2**.
>
> **Theorem D3 (grain-move descent) [T].**  A grain moves as a unit along its freedoms (common tilt θ, the slides u);
> the basin is a region of (θ, u, positions), and D2 holds fibre by fibre; the exchange completion — remove the crowd,
> place the slot square, re-fit the removed squares by a grain move — is sound by FLOOD-M and costs the chain-formula
> difference s_G(θ′) − s_G(θ) plus the exposure obligation of Lemma EXPOSE; no motion is ever certified, only
> configurations.  The tempting version "the crowd can be slid into the slot along the grain's own freedom at no side
> cost" is [F]: f0's slide is a segment of length 0.298 at FIXED tilt whose ends are stops, not slots.

## 1. Setting

Packing P: n closed unit squares, pairwise interior-disjoint, in [0, m]², m ∈ W.  Corner c; corner frame (u, v) =
distances from c's two walls; the box B_c(c_b) := (0, c_b)², c_b = 1 on P, c_b = 1 + w on F = Δ_λ P at s_hi.  For a
square Q in the quadrant, μ(Q) := min_{q ∈ Q} max(u_q, v_q) and its DEPTH d(Q) := c_b − μ(Q); Q MEETS the box iff
d(Q) > 0.  A CROWD at c is the set of meeters, listed by depth d₁ ≥ d₂ ≥ ….  The corner is SIMPLE when the slot
square (the pressed axis-aligned square [0,1]²) is in P.  Slots p = (c, i, j) of a Young class carry the slot frame
Φ_p of `slot_crowds.md`; all statements below are at a corner unless a slot is named, and the slot versions replace
Theorem B by Lemma A1 only (forced_corners.md §5(f)).  Classes S ⊂ T = S ∪ {p}; "T dead on [s_lo, s_T]" means no
packing at any side of that interval contains the pins of T (the monotone hypothesis, K1).

**Lemma 1.0 (the corner point) [T].**  A square in the quadrant containing the corner point is the pressed square.
*Proof.* The origin is an extreme point of the square, hence a vertex; the two edges at that vertex lie in the
quadrant, so they point along the axes.  ∎  Hence at a non-simple corner d₁ < c_b, and the corner point is uncovered.

## 2. [T] Lemma CH — the corner hurt, in four parts

**CH-S (side: the conversion is rigid and costs d₂).**  Let P be a packing at side m and c a corner with crowd
depths d₁ ≥ d₂ ≥ … (at the unit box).  For t ≥ 0 let P^t be P placed in [0, m + t]² so that its distance to each of
c's two walls grows by t and to the other two walls is unchanged (a translation by t along the inward diagonal of c).
Then P^t is a packing at side m + t whose corner box at c is met exactly by the squares with d(Q) > t, and the pins
of P at the corner OPPOSITE c are at their slots of [0, m + t]².  With t = d₂: at most one meeter, hence (teleport,
`k0_route.md` §3) a packing at side m + d₂ containing the slot square at c.
*Proof.* In c's frame P^t = P + (t, t): max(u + t, v + t) = max(u, v) + t, so μ(Q + (t,t)) = μ(Q) + t and Q + (t,t)
meets (0,1)² iff d(Q) > t; containment P + (t,t) ⊂ [t, m + t]² ⊂ [0, m + t]² (frame coordinates), disjointness is
translation-invariant.  A pin at slot (α + βm) in the frame moves to α + βm + t, and the slot of the new container is
α + β(m + t): equal iff β = 1 in both coordinates, i.e. the pin is anchored to the two far walls.  The teleport is
Lemma K0-FREE's `teleport_packing` at side m + d₂ (the box is met by ≤ 1 square).  ∎
Slots: the same with Φ_p in place of the corner frame, provided the slot's two backing pins are anchored to the far
walls in the two backed coordinates — false in general (a slot backed by a pin near c), which is exactly why
SLOT-SLIDE (A94 §3.4) translates the shallow intruders' retreat clusters instead and needs them non-anchored [T, with
that hypothesis].  Unconditional slot form by DILATION: Δ_λ P with λ − 1 = 2 d₂ has μ(Δ_λ Q) ≥ μ(Q) + (λ − 1)/2 ≥
μ(Q) + d₂ (centres have both coordinates ≥ 1/2), so the second meeter leaves the unit box; the pins of S drift by
(λ − 1)|α| ≤ 2 d₂ A_S; side m(1 + 2 d₂).  [T]

**CH-A (area: the sealed box).**  Every square of P has μ ≥ c_b − d₁ (meeters by the definition of d₁, non-meeters
have μ ≥ c_b), so the open box (0, c_b − d₁)² meets no square: the corner WASTES ≥ (c_b − d₁)², and Σ_c (c_b −
d₁(c))² + |U_wall| ≤ m² − n where U_wall is any other certified-uncovered set (A164's |U|).  [T; Lemma ID's charge
with d₁ in place of the shallowness hypothesis.]  With CEIL (min(d₁, d₂) ≤ 1 − 1/√2 = 0.2929 for the unit box) this
never kills four corners on its own (A89) — the area part of the hurt is a location diagnostic, as A164 measured.
Sharper, per pose pair [S]: the SEALED POCKETS between the meeters and c's walls (FLUSH-JAM's Σ_L-type regions) are
uncovered too; they are certified per pair by the lane test (LANE = 0 on the pocket, A141/A161), not by a formula.

**CH-C (cells, loneliness, obstacle).**  The two meeters' centres lie in distinct cells of the 2×2 grid at c_b and at
ℓ∞-distance ≥ 1/√2 (Lemma A2, A1); each pose is non-lonely (Theorem B; R3); the pair's configuration space has
non-empty 6-dimensional interior (K0-PAIR (b)) — so the obstacle the crowd presents to the rest of the packing is the
UNION over its pose set of Q₁ ∪ Q₂, whose K′ (the intersection over poses) is empty for a whole meeter window and
non-empty only per piece (A171–A173: the per-piece K′ is what clips).  [T]

**CH-L (chord: the band meeter's unit chord).**  By SIDEBAND (a) some meeter has centre (u_z, v_z) with u_z < c_b or
v_z < c_b; say v_z < c_b (it hugs c's floor).  By Lemma CHORD-BAND its chord on the floor-parallel line v = g is
≥ 1 for every g with |g − v_z| ≤ γ(θ) = (cos θ + sin θ)/2 − sin θ cos θ ≥ γ(45°) = 0.20710.  So a non-simple corner
still places a UNIT chord on every floor-parallel line at height in [v_z − γ, v_z + γ] ⊂ (0, c_b + 0.2071), as a pin
does on every line at height < 1; the wall-parallel statement is the mirror.  [T]  What is NOT forced [F]: a unit
chord on a NAMED line — two meeters at depths ε (a NW one up the wall, an SE one along the floor, both poking ε into
the box) leave the line v = 1/2 with total chord < 1 — so the chord deficit of a crowd against a pin is a priced,
not a forced, quantity; the forced form is the band above, whose line is the meeter's own centre line.

**Consumption table.**  LP (case-measure certificate, A57 schema + v4/v5 clauses): CH-S ⇒ the crowd row at depth
δ = s_T − m (Lemma CW / Theorem S(δ): NO-family = the complement of the depth-δ crowd family, weight 1 + e on the
family) — licensed depth s_T − m, today 0; CH-C ⇒ R3's lonely NO-family (free columns in lonely poses dropped) and
R1's pair prune; CH-L ⇒ a `guardlines` row (v5) on the band meeter's centre line with `minchord ≥ 1` certified over
its box when the box's height range lies in one γ-band; CH-A ⇒ no LP form (Leaf WASTE is LP-free).  Geometry
(multibox): CH-C ⇒ the lonely clip per piece + the cell split (A173, R2); CH-S ⇒ nothing to clip — it is a statement
about the side, consumed as D1; CH-A ⇒ the sealed-pocket lane test.

## 3. The descent theorems

### 3.1 [T] Theorem D1 (conversion descent)

Let T = S ∪ {p} be dead on [s_lo, s_T] (monotone hypothesis) and let P be a packing at side m ∈ [s_lo, s_T)
containing the pins of S.  Then at p: (i) p is met by ≥ 2 squares of P (Theorem FC / K0-FREE′); (ii) the second
depth satisfies d₂(p) ≥ s_T − m in each of the three conversion forms of CH-S under its hypothesis — rigid at a k0
corner (no pins to keep; Lean `Slide.slide_crowd` is this statement with s_T = ŝ); cluster form at a slot of a pinned
class with non-anchored shallow clusters (SLOT-SLIDE); dilation form unconditionally, as m(1 + 2d₂) ≥ s_T whenever
2 d₂ A_S ≤ h_T (the slack of T's certificate cores).  *Proof.* CH-S produces a packing at side m + d₂ (resp. m(1 +
2d₂)) containing the pins of T; if that side were ≤ s_T the kill of T is contradicted.  ∎

**The yield, exactly.**  The row D1 licenses is "two squares at depth ≥ s_T − m at p" — A109's crowd row with the
depth it may legally carry.  With every extension certified on [191/50, s0] only (the scoreboard), s_T = s0 and the
depth is s0 − m: 0 at the top of the window, where all the alive pages live.  Certifying T above s0 is bounded by
T's own minimum s*_T; the gallery bounds it from above by the smallest shadow whose skeleton contains T's pins:

| forced cell of trump5 | T | a shadow in T | s*_T ≤ | licensed depth at m = s0 ≤ |
|---|---|---|---|---|
| TL(0,0) | k6_23 | S02 (7 slots ⊇ k6_23) | 3.886746 | 0.00966 |
| BL(0,2) | k6_07 | S07 | 3.885618 | 0.00853 |
| BR(0,1) / TR(0,1) / TR(1,0) / BL(1,1) | k6_21 / 22 / 24 / 19 | S38 ∈ k6_21 (3.928915, A125's basin frame); S08 (3.914214) if its k6_21 match is genuine | ≤ 3.9289 (k6_21) | ≤ 0.052 |

So the conversion descent can never license the depth 0.3 that A109 measured as decisive; its ceiling is ~0.01–0.05.
**Counterexample to the stronger claim "T dead on W ⇒ S dead on W" [F]:** Trump: trump5 ⊂ every k6 extension, all
six extensions dead on [191/50, s0], Trump alive at ŝ; its TL crowd has (d₁, d₂) = (0.168, 0.155) [M], so D1 says
only ŝ + 0.155 > s_T, i.e. s_T < 4.03 — true and harmless.  The non-simple corner is what LETS Trump beat its k6
completions: the crowd's overhang (Lemma X: exactly 1 + E beyond the slot cell) is spent as the wedge of the tilted
strip, the pinwheel's mechanism in reverse.

### 3.2 [T] Theorem D2 (basin descent)

Let C be a local certificate Dead_{L∪P}(N, s0) in T's frame (Theorem LOCAL: pins P with slack h, bodies L in boxes
N; the selection tree over near pairs closes with every leaf's minimum side > s0), and p ∈ P with T = S ∪ {p}
Young-completable and dead on W.  Consider a node of class S whose hypothesis is: pins P ∖ {p} and the bodies L in
boxes N′ ⊆ N.  Then the node is dead if the following descended tree closes, and the tree is sound:
 (a) [DROP] the selection tree of C with the body p deleted (fewer bodies ⇒ weaker hypothesis; a leaf that still
     closes closes for every class not pinning p).  Leaves that close here need nothing more.
 (b) [LONELY] at a surviving leaf, for every body ℓ ∈ L whose box meets p's widened box B_p⁺: clip ℓ's box by the
     lonely set of p (Theorem B's box test, `multibox.lonely_clip`); re-run the leaf on the clipped box.  Sound:
     in any S-packing at side ≤ s0 (dilated to s0) p is met by two distinct non-pin squares (Theorem FC), so a body
     ℓ in a lonely pose at p cannot occur.
 (c) [PARTNER] at a leaf surviving (b): let ℓ be a body meeting B_p⁺ in the leaf's boxes (or none).  The packing has
     a second meeter distinct from every pin and every body outside those meeting B_p⁺; it is a square inside the
     container, interior-disjoint from every body's K′ and every pin core: if LANE(B_p⁺ | obstacles) + #{bodies that
     can meet B_p⁺} ≤ 1 (A141's leaf with A161's exact miss test), the leaf is dead.  Otherwise a realised partner is
     a genuine 10-body partial packing and the leaf SURVIVES — a hole of the descended basin.
*Proof.* Each step is a sound strengthening of the leaf's hypothesis by a fact true of every S-packing at the node:
(a) monotonicity of DROP; (b) Theorem FC + Theorem B's (⇒) direction on F (the pad π₀ is in B_p⁺); (c) Theorem FC's
count with the leaf's obstacles, the lane cover being an upper bound on interior-disjoint meeters.  A closed
descended tree therefore certifies Dead_{L ∪ P∖p}(N′, s0) with the corner requirement, which is the node's hypothesis
at every side of W by dilation (Theorem LOCAL's window clause is unchanged: the tree is at s0, the node's boxes are
stated at s0, the requirement is stated on F).  ∎
**What it emits.**  One `N_boxes` entry per closed descended box set in the p-less frame (A133's generator + its
independent checker as in A160/A163), with two new records per leaf: the lonely-clip trace (tilt sub-bins removed,
slabs removed, A131's certifying bisection) and the lane certificate (A141's cover with A161's exact miss test).  A
node of class S dies by CONTAINMENT in that entry (A187's `cons` column), no LP.
**Counterexample to the stronger claim [F]:** "a basin in T's frame is a basin in S's frame" fails as A163 measured:
the same 54 box sets give 52/54 in k5_16 (BL(1,0) dropped) and 42/54 in trump5 (TL(0,0) dropped), with nine LIVE-LOW
witnesses — real 9-square partial packings at sides 3.8205–3.8771 — so step (a) alone loses a fifth of the pinwheel's
basin in trump5; what (b)/(c) recover is measured in `descent_examples.md` §7.2.

### 3.3 [T] Theorem D3 (grain-move descent) — statement; the dynamics are in `descent_grains.md` §6

Let G be a grain with freedoms (θ, u) (common tilt, slides) and chain formula s_G(θ) on its load path (grain_flood.md
§2: Λ, Y, D, F_T); let its basin in T's frame be certified on a region R of (θ, u, positions).  (i) [fibre form]
D2 applies on every fibre of R; a node whose support matches G at (θ, u) is priced by the descended entry containing
(θ, u).  (ii) [completion form] Let P be an S-packing at side m whose corner p is non-simple with crowd {A, B} and
whose other squares contain G.  If there is a configuration P′ at side m′ consisting of P ∖ {A, B} with G moved to
(θ′, u′) inside its own validity region, the slot square at p, and one re-fit square Q₀, all pairwise
interior-disjoint inside [0, m′]², then P′ is a T-packing at side m′ (FLOOD-M: a packing is a configuration, not a
motion), so m′ > s_T; and m′ − m ≥ s_G(θ′) − s_G(θ) when G's chain is the binding wall-to-wall path in both.  The
re-fit exists iff Lemma EXPOSE's exposure Σ(Q₀) = int Q₀ ∖ (A ∪ B) is met by no untouched square — per fibre a lane
test, never a formula.  (iii) [what is false] "the crowd slides into the slot along G's own freedom at no cost" [F]:
f0's freedom in the pinwheel is a segment of length 0.298 at the fixed tilt 48.4351° whose two ends are the stops
BR(0,1) and f1 (A160), and its tilt window closes like √ε — the freedom never reaches a slot; and Trump's TL crowd is
held at every one of its nine subjects (A130, first-order isolated).  The completion always costs side.

## 4. Obligations [C]

(C1) D1's cluster form at pinned slots: SLOT-SLIDE's non-anchoring hypothesis, stated per slot (A94 §3.4) — the
rigid form needs no hypothesis but keeps only the opposite corner's pins.  (C2) Theorem B's (⇒) direction in Lean
(`SecondMeeterCriterion`, three support clauses), consumed by D2(b).  (C3) The extension certificates above s0
(D1's table): parametric slabs on [s0, s*_T − ε] per extension class, priced in `descent_grains.md` §5.4.
(C4) D2(c)'s lane cover at a leaf with a body ℓ as a possible meeter: A158's obstruction (K′ of a whole window is
empty) applies — run it per piece of ℓ's clipped box, A167's conditional form.
