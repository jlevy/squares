# The k0_00 route: D4 quotient, teleport reduction, corner seed, re-price — A85, 2026-09-02

Target: the k0_00 instance of `stratum_kill` (depgraph **C.K4TIER**, the unstratified root
problem: no pins, no cores, no logic kills, 11 free squares, all eight D4 images of Trump
compatible). A84 priced it at ≥ 100 desktop-days plain / 25–30 with the A58 corner seed
(`protected_trees.md` §7.1); A38 had already measured the same object as "the far-field tree at
s0" and found a per-node LP DECISION wall (70–700 desktop-days as an open-ended floor,
`attempts/A38-root-power/results/rootpower_report.md`). This file proves the lemmas behind the
three cuts the brief names (C1 D4 quotient, C2 teleport reduction to k1_00, C3 the doubly-blocked
corner seed), adds the two the PI/advisor added mid-attempt (Lemma K0-ROT, atlas discharge
leaves (D′)), quantifies each cut from the A85 pilot, and re-prices. Labels: [T] proved,
[S] routine given cited items, [M] measured/computed exact, [F] finding, [C] open.
Companions: `protected_trees.md` (Lemma P-TREE, whose leaf semantics this file extends),
`contraction_tube.md` (T1, Lemma SEAM), `closed_disjoint_bridge.md` (B.0, Lemma B),
`d4_reduction_s0.md` (D4 at s0, `d4_wlog`), `attempts/A58-clear-corner/notes/theory.md`
(CC-1, CC-2, CC-3), `attempts/A85-k0-route/` (pilot, CP search, atlas tool).

## 0. Verdict

> **Start here instead (A275, 2026-09-23): [`k0_knowledge.md`](k0_knowledge.md)** — everything the lab knows about k0
> (true, false, certified, measured, conjectured, dead routes), with this file's §13 re-tagged as of 2026-09-23.  The
> verdict below is A85's (2026-09-02) and describes the volume-tree route, now dead (`k0_knowledge.md` §7).

> **Re-price (§8, stacked): k0_00 ≈ 3 200–7 000 CPU-h (45–100 desktop-days at three slots)
> if depth-2 certifications repair at ≈ 85 % — a 3–30× cut on A38's floor but NOT below A84's
> plain "≥ 100 desktop-days at one slot"; ≥ 3·10⁴ CPU-h if only first-pass certifications
> count (f₂ = 1/3). The deciding constant is certification reliability at η ≈ −1, an
> engineering constant, not a geometric one; the order-of-magnitude cut the brief asked for
> does not exist along C1–C3.**
> The cuts, separately: **C1** is sound and worth exactly ×1/8 on every node count of the
> tree (Lemma K0-D4, two instances — the interior-first tree through Theorem A38.1 + `d4_wlog`,
> and the corner seed through orbit representatives) — but on the residue term only, and the
> residue is not what dominates (§8). **C2** is sound in the ∀-packings form (Lemma K0-FREE:
> a free OR singly-met corner box teleports into the MONOTONE hypothesis of k1_00, which Lemma
> P-TREE kills at every side of the window — no minimiser selection, no stuckness), so A84's
> "stuck-only" caveat on the corner seed is VOID: k0_00 owes only K0-BLOCKED, ∀-packings,
> given k1_00's tree. **C3**: K0-BLOCKED has NO finite case list — the corner 2-crowd
> configuration space contains 6-dimensional open sets (Lemma K0-PAIR (b): an explicit
> floating same-sense pair), so the residual is a tree; and as a COVER the seed is dead at
> shallow depth (pair-box count N_pair per corner «pilot» ⇒ N_pair⁴/8 «pilot» four-corner
> nodes before any LP has slack) — its sound value is the free NO-branches (teleport leaves)
> and (C) prunes on fine boxes. The price is governed by the interior-first tree's per-node
> decision cost at budget 10 — A38-G7 — which the pilot measures with the A60 engine (§7).

## 1. Setting

Sides: s0 = 969271/250000, ŝ = Trump's side, s0 − ŝ = 4.0998·10⁻⁷, window W = [3.82, ŝ].
A packing at side m: eleven closed unit squares, pairwise interior-disjoint, in [0, m]².
For P at side m < s0 put λ := s0/m and F := Δ_λ P (centres scaled by λ about the origin,
tilts and sizes unchanged; Lemma B.0: F is a strictly disjoint closed 11-family inside
[0, s0]² with positive margins at all four walls). λ_max := s0/3.82 = 1.0149426…

* **k0_00** := the packings whose skeleton is empty: no square is axis-aligned at a census
  slot (Lean `skeleton s z = ∅`). Its monotone hypothesis M_{k0_00} is TRUE of every packing
  (no pins), so the class's tree is the zone-tree of the whole problem.
* **[F] k0_00 is NOT empty.** A rigid rotation R_φ ẑ of Trump about the container centre by
  any φ ≠ 0 has no axis-aligned square, hence skeleton ∅; its side is σ(R_φ ẑ) = ŝ + 3.877|φ|
  + O(φ²) (§5.2, both senses), so for |φ| ≤ 1.057·10⁻⁷ it is a k0_00 packing at side ≤ s0.
  The target is therefore strictly **"no k0_00 packing at any side m ∈ [3.82, ŝ]"** (at ŝ:
  every packing is a Trump image, which is not in k0_00); the rotational ghost family near
  each image must land in a (D) leaf (§5.2 checks the radius: centres move ≤ 2.2·10⁻⁷, tilts
  ≤ 1.06·10⁻⁷ — three orders of magnitude inside A60's landing radii (1.6·10⁻³, 2.1·10⁻³)).
* **Images.** G_{k0_00} = D4, eight images g·ẑ, Trump-frame pin set I_g = ∅ for all g; the
  tube direction is the pure scale ray v = ẑ/ŝ; T_max = 0.1305 at the landing radii
  (`certs/tube_I_none_landing_T1279o10000_rc1o625_rt21o10000.json`, A84 §4; also A83's
  `certs/tube_scale_T5.71e-2_window.json`) ≥ ŝ − 3.82 = 0.0571: **the whole window is regime 2
  at A60's landing radii, and there is no pin-slack condition (A_S = 0, T_K = ∞).** Regime-1
  plain kills do not exist for k0_00 anyway (A82: τ = 11.000 at 3.833212; A08's root
  certificate 10.72 binds only at 3.82).
* **The corner boxes.** B_c := the closed unit box at corner c ∈ {BL, BR, TR, TL} of
  [0, m]²; "Q meets B_c" means int Q ∩ int B_c ≠ ∅ (A58's convention). The widened box at s0:
  B_c^w := B_c(s0) grown by w INTO the container ([0, 1 + w]² at BL, [s0 − 1 − w, s0]² at TR,
  etc.), w := (λ_max − 1)(1 + √2/2) = 0.025509 (Lemma K0-WIDEN).
* **Leaves.** As in `protected_trees.md` §1: (K) a `case-lp-certificate-v1` PASS at s0
  (frozen `verify_case.py`), (C) contradictory/vacuous, (D) all N = 11 squares localised within
  (r_c, r_θ) of a distinct member of g·ẑ; plus two new leaf types proved here: **(T) teleport
  leaves** (§3) and **(D′) atlas leaves** (§4.3).

## 2. [T] Lemma K0-D4 — the quotient, with the mod-G bookkeeping

D4 acts on packings at side m by the container symmetries about (m/2, m/2) (Lean `d4Apply`,
`d4_packing`: the image of a packing is a packing at the same side; on poses g(Q(c, θ)) =
Q(g c, θ′) with θ′ = θ for rotations and θ′ = 90° − θ for reflections, `d4Sq_set`;
`d4_reduction_s0.md` R5). Dilation commutes with the action at the respective sides,
Δ_λ ∘ g_m = g_{s0} ∘ Δ_λ (`contraction_tube.md` §4.1). The k0_00 hypothesis is D4-invariant
(there is nothing to preserve), and so is the K0-BLOCKED hypothesis of §4 (the set of corner
boxes is a D4-orbit).

**Lemma K0-D4 (equivariant quotient).** Let T be a zone-tree at s0 for a D4-invariant root
hypothesis H, in which the children of every node n are indexed by a finite D4-set X_n (a
closed cover of a D4-invariant region by boxes permuted by D4, the induced action on a
YES-box being g·B := {(g c, θ′)}; the NO child is fixed) and whose leaf verdicts are (K), (C),
(D), (D′), (T). Suppose subtrees are built only below one representative child per D4-orbit
of X_n at every node, and the representative subtrees close. Then T closes: every family F
satisfying H reaches a closed leaf up to D4.

*Proof.* Induction on depth. At node n with F reaching child x ∈ X_n, let g map x to its
orbit representative x̄ = g·x. g·F is a family at side s0 (`d4_packing` at s0), satisfies H
(invariance), and reaches x̄ (the square witnessing x for F witnesses g·x for g·F, by the pose
transport; core containment is preserved because g maps the core K(B) onto K(g·B), a rational
isometry). By induction g·F reaches a closed leaf of the representative subtree. Verdict
transport: (K)/(C): "no family" is D4-invariant, so F is excluded; (T): "some corner box of
g·F is free/singly met" ⇒ the corresponding corner box of F is (g⁻¹ of a corner box is a
corner box); (D): g·F within (r_c, r_θ) of g′·ẑ ⇒ F within the same radii of g⁻¹g′·ẑ
(g is a Euclidean isometry on centres and θ ↦ ±θ mod 90° on tilts, so both landing metrics
are invariant); (D′): g·F inside an atlas box ⇒ F inside the D4-image of that box, and A37's
atlas is stated mod D4 × S₁₁ (the containment test ranges over the eight images, §4.3). ∎

**Instance (i) — interior-first, /8 at the root.** Theorem A38.1 (certified, verify_case
PASS, `attempts/A38-root-power/results/root_s0.json`): every 11-packing in [0, s0]² has a
square centred in Z(s0) = [11/10, 694271/250000]²; F is such a packing. `d4_wlog`
(`D4Wlog.lean`, D4.5) then gives a D4-image of F with a square centred in the fundamental
triangle T(s0) = {s0/2 ≤ y ≤ x ≤ s0 − 1/2 − 3/5} and tilt in [0°, 90°]: the level-1 cover is
A27's 216 cells of T(s0) × [0, 90°] (A38 used exactly this at s0), i.e. **the root branching
factor is already divided by 8** — the only D4 saving the interior-first tree admits (deeper
nodes carry no residual symmetry). The eight images are one image seen eight times: exactly
the (D) leaves in T(s0)'s subtree for the images whose witness square lies in T(s0) (A38's
census: 3 level-1 cells contain image placements), and the other seven are their D4 transports.

**Instance (ii) — the corner seed, /8 on the product.** The K0-BLOCKED tree branches, per
corner, over pairs of reach-cover boxes (§4). With the cover D4-closed (same centre grid at
each corner by the corner symmetries; a σ-closed tilt partition, e.g. t-edges {0, 1/8, 1/4,
3/8, 5/11, 3/5, 7/9, 1}, closed under t ↦ (1 − t)/(1 + t)) the four-corner tuples form a
D4-set on which D4 acts freely off the symmetric tuples, so the representative count is
N_pair⁴/8 + O(N_pair²). [M] «pilot: canonical fraction».

**The mod-G tube clause (D.S6).** At a (D) leaf F is within (r_c, r_θ) of g′·ẑ; apply g′⁻¹
(commuting with Δ_λ) and run Lemma P-TREE's Step 4 with I = ∅: (g′⁻¹P, m) ∈ Tube_scale(T′,
(r_c + 3.6·10⁻⁷, r_θ, 0)), T′ = ŝ − m ≤ 0.0571 < T_max = 0.1305, so m ≥ ŝ with equality only
at P = g′·ẑ. One tube certificate serves all eight images.

## 3. [T] Lemma K0-FREE — the teleport reduction to k1_00 (∀-packings)

**The k1_00 kill, as consumed.** Lemma P-TREE for S = k1_00 (pins {BL(0,0)}, N = 10, A_S =
1/2, G_S = six images, I_g ∈ {{0}, {2}, {5}}, tube wall E7c2-9e3, T = 0.1305, T_K(2·10⁻²) =
0.1491, so δ_basin(k1_00) = 0.1305 ≥ 0.0571 — the whole window) gives:
(k1-a) no packing at any side m ∈ [3.82, ŝ) contains an axis-aligned unit square at a corner
slot (`ContainsPins {corner} m z`, any corner after D4 normalisation, `class_kill`);
(k1-b) every packing at side ŝ containing a corner slot square is a Trump image.
This is a DEPENDENCY: k1_00's own tree (O1–O5 of `protected_trees.md` §5, priced there as a
k3-scale campaign, ~200–300 CPU-h) must close first. Nothing below uses more than (k1-a)/(k1-b).

**Lemma K0-FREE.** Let P be a packing at side m ∈ [3.82, ŝ] and c a corner such that at most
ONE square of P meets int B_c(m). Then: if m < ŝ, P does not exist — contradiction; if m = ŝ,
P is a Trump image.

*Proof.* Let Q be the meeter if there is one, otherwise any square of P (11 ≥ 1). Define
P′ := P with Q replaced by the slot square B_c(m) itself (axis-aligned at the corner slot).
B_c(m) ⊆ [0, m]², and int B_c(m) is disjoint from the interior of every square of P other than
Q (hypothesis), so P′ is a packing at side m (Lean `teleport_packing`, hypotheses `hbox`,
`hfree`) — no corridor, no slide, no minimality. P′ contains a corner slot square, so
`ContainsPins {c} m P′` (the occupier map is the teleported index). For m < ŝ this contradicts
(k1-a). For m = ŝ, (k1-b) gives P′ = g·ẑ; P and P′ agree except at the one index of Q, so
Theorem U (A65, `theorem_u.md`; the `hU` interface of `unique_via_chain`: a packing at ŝ
agreeing with a Trump image except at one square IS a Trump image) gives that P is a Trump
image. ∎

**On the brief's question ("is the result necessarily in k1_00 and not a higher class?").**
Not necessarily: if P has latent axis-aligned squares at slots adjacent to c (e.g. at BL(1,0),
not simple in P because the corner was empty), the skeleton of P′ is a strict superset of
{c} — k2_00, k3_02, … . This is IRRELEVANT: the k1_00 tree kills the MONOTONE hypothesis
`ContainsPins {c}` (Lemma P-TREE (a)/(b) are stated for M_S, not E_S), which every superset
class satisfies (K1: kills climb containment, Lean `Skeleton.lean` K1(i)). No exactness
bridge is consumed. The same lemma with "at most one meeter" replaced by "no meeter" is the
CC-3 mechanism of A58 §3 with the k1_00 tree in place of a (non-existent) root certificate:
A58 (a) proved that no single certificate for k0_00 + root can exist (K1-protection); a TREE
kill of the monotone hypothesis is exactly what K1-protection does not forbid.

**Remark (why this is not stuck-only).** A84 §7.1 read the corner seed through CC-2′ (a
K*-maximal minimiser) and concluded "stuck-only". Here the exchange is used as in CC-3: the
teleported packing is a genuine packing at the same side and (k1-a) is a ∀-packings
statement, so the conclusion binds every packing. The selection chain, H10-stuck and T4's
re-split (§9) are not needed for K0-FREE.

**Corollary K0-FREE′ (the residual root).** For every packing P at side m ∈ [3.82, ŝ] that is
not a Trump image, **every corner box B_c(m) is met by at least two squares of P.** (Apply the
lemma at each corner.) At k0_00 this is A58 Theorem A58-1(i) with the quantifier upgraded from
"a selected minimiser" to "every packing" and the price of the upgrade = k1_00's tree.

## 4. K0-BLOCKED: the doubly-crowded corners as a tree

### 4.1 [T] Lemma K0-WIDEN (the crowd transfers to the s0 family)

Let P be a packing at side m ∈ [3.82, s0), F = Δ_λ P, and Q ∈ P meeting int B_c(m). Then
Q′ := Δ_λ Q meets int B_c^w(s0) with w = (λ − 1)(1 + √2/2) ≤ (λ_max − 1)(1 + √2/2) = 0.025509.
Conversely, if Q′ meets int B_c(s0) then Q meets int B_c(m).

*Proof (BL; the other corners by Δ_λ ∘ g_m = g_{s0} ∘ Δ_λ).* Q′ = Q + (λ − 1)c_Q. Take
p ∈ int Q ∩ int[0, 1]²; p′ = p + (λ − 1)c_Q ∈ int Q′, and p′_x ∈ (0, 1 + (λ − 1)c_{Q,x})
with c_{Q,x} < 1 + h(θ_Q) ≤ 1 + √2/2 (Q meets the box), so p′ ∈ int[0, 1 + w]². Converse:
p′ ∈ int Q′ ∩ int[0, 1]² gives p = p′ − (λ − 1)c_Q ∈ int Q with p_x < 1 and p_x > −(λ−1)c_{Q,x};
but Q ⊆ [0, m]² and p ∈ int Q give p_x > 0. ∎

Hence the tree at s0 states the crowd hypothesis on F with the WIDENED boxes (sound: every
crowd of P is a crowd of F for B_c^w), and the teleport leaves with the UNWIDENED ones:
"no non-owner square of F meets int B_c(s0)" ⇒ (converse) no non-owner square of P meets
int B_c(m) ⇒ Lemma K0-FREE at P. For a tree built for a declared reach T′ < 0.0571 the
widening shrinks to (λ_max(T′) − 1)(1 + √2/2), as Lemma PD's drift does.

### 4.2 [T] The residual hypothesis and its tree

**Lemma K0-BLOCKED (structure).** Let P be a packing at side m ∈ [3.82, ŝ), F = Δ_λ P. Either
some corner box of P is met by ≤ 1 square (Lemma K0-FREE: P does not exist), or F has, at
each of the four corners, two distinct squares meeting int B_c^w(s0); the four pairs are
pairwise disjoint sets of squares, so **eight distinct squares of F are localised to the four
corner reach sets R_c^w := {(c, θ) : Q(c, θ) ⊆ [0, s0]², Q(c, θ) meets int B_c^w}, and at most
three are free.** *Disjointness*: a unit square has diameter √2 < s0 − 2 − 2w = 1.826 = the
distance between two distinct widened corner boxes (CC-1(ii) with the widening). ∎

**The tree T_B.** Root hypothesis H_B on F: the eight crowd squares as above. Branching, per
corner c, over a closed cover {B_i} of R_c^w (A60 boxes: centre width 0.15, σ-closed tilt
cells, cores of half-side ≥ 0.34): YES_i for the first crowd square, then YES_j (j ≠ i, and
j = i is contradictory: two unit squares with centres < 1 apart overlap, box diameter
0.15√2 < 1) for the second; the pair (B_i, B_j) is a (C) leaf when `cores_meet(K(B_i), K(B_j))`
(distinct squares of a packing have interior-disjoint cores). NO children do not exist at the
crowd levels: the covers are of the reach sets, and "no square in R_c^w" or "no second square"
is a (T) leaf by Lemma K0-WIDEN + K0-FREE. After the eight conditionings the budget is 3;
kills may be attempted at any intermediate level (budgets 9, 7, 5, 3) with the alive gate over
the eight images (Lemma A57-3: an image whose ≥ budget witnesses survive the cores makes the
node LP-unkillable). Below the seed the tree is A60's: ladders on the crowd boxes, then the
three free squares, until (K)/(C)/(D)/(D′). Soundness is Lemma P-TREE's proof with k_S = 0
(Step 1 vacuous; Step 2 unchanged — the pair witnesses are distinct by the (C) rule; Steps
3–4 verbatim; the (T) leaves by §3; the (D′) leaves by §4.3), and Lemma K0-D4 (ii) for the
orbit quotient.

### 4.3 [T] Lemma K0-ATLAS — atlas discharge leaves (D′)

A37's atlas (`attempts/A37-cp-atlas/results/atlas_final.json`, 37 entries incl. A51-NEW-0;
per entry a box centre z_c ∈ ℝ³³ and a rational radius h with the certified claim: every
feasible 11-square configuration z (pairwise interior-disjoint, no container) with
‖z − z_c‖_∞ ≤ h has σ(z) ≥ V, and every entry's V ≥ s0 (`V_at_h_max ≥ 3.877084`); tilts in
radians, A38 §3) gives a leaf type for ANY s0 tree:

**Lemma K0-ATLAS.** If at a node all eleven squares of F are localised in boxes whose union,
after some relabelling of the squares and some g ∈ D4, lies inside an atlas box (centres:
rational interval containment; tilts: the θ-interval [2 arctan t₀, 2 arctan t₁] of the
t-box inside [θ_c − h, θ_c + h], checked with E.COORD's X.1 |dθ| ≤ 2|dt| or by interval
arctan), then no packing P at side m < s0 reaches the node.

*Proof.* F is feasible, so σ(F) ≥ V ≥ s0. But F = Δ_λ P has strictly positive wall margins:
its leftmost coordinate is λx_min − h ≥ (λ − 1)h > 0 and its rightmost λx_max + h ≤ s0 −
(λ − 1)h < s0 (x_min ≥ h, x_max ≤ m − h), same in y; so σ(F) < s0. Contradiction. ∎

No dilation bookkeeping, no window obligation (m = ŝ included, since ŝ < s0), no equality
clause: the atlas boxes are already stratum-blind value certificates. Incompleteness of the
atlas is irrelevant (unmatched residues need LP kills; matched ones are free). Their reach: h
between 3.8·10⁻³ and 6.0·10⁻² (37 entries), i.e. at the scale of A60's landing radii, so a
residue chain that contracts onto an atlas CP lands in (D′) at about the same depth (L24) as
one contracting onto Trump lands in (D). [M] A38's level-1 census at s0: 172 survivors = 3
Trump-consistent, 34 atlas-consistent, 135 unexplained at box scale. Tool:
`attempts/A85-k0-route/code/atlas85.py` (`in_atlas`, convention note
`results/atlas85_convention.md`, self-test `results/atlas85_selftest.json`).

### 4.4 [T] Lemma K0-PAIR — what a corner 2-crowd is, and is not

Fix the corner BL, quadrant {x ≥ 0, y ≥ 0}, and let A, B be unit squares in the quadrant with
disjoint interiors both meeting int[0, 1]² (w = 0; the widened statements are weaker).

(a) **At most one of A, B is axis-aligned.** Two axis-aligned squares [x_i, x_i + 1] ×
[y_i, y_i + 1] meeting int[0, 1]² have x_i, y_i ∈ [0, 1), so |x₁ − x₂| < 1 and |y₁ − y₂| < 1:
they overlap. (With the widening w > 0 the statement fails exactly in the pocket x₁ ≤ w:
one square within w of the slot and its flush neighbour — the near-k1_00 pocket, which the
ladder handles as an image-adjacent residue.)

(b) **The 2-crowd configuration space has nonempty interior in the 6-dimensional pose space,
and contains SAME-SENSE tilted pairs.** Exhibit [M, `attempts/A85-k0-route/code/`-checked in
floats, SAT gap 0.0441]: A with lowest vertex (0.643, 0.7), tilt 40° (vertices (0.643, 0.7),
(1.409, 1.343), (0.766, 2.109), (0.0002, 1.466)); B with vertex (0.95, 0.9) and edges at −60°
and 30°, i.e. tilt 30° mod 90 (vertices (0.95, 0.9), (1.45, 0.034), (2.316, 0.534),
(1.816, 1.4)). Both lie in the quadrant, both meet int[0, 1]² (A at its apex, B at its
vertex), the separating-axis gap is 0.044, and neither touches the other or the walls with
zero margin except A's left vertex at x = 0.0002 (shift A right by 0.01: still a 2-crowd).
Every small perturbation of (A, B) is again a 2-crowd — an open set. Consequences: **there is
no finite exact case list for K0-BLOCKED** (unlike corners4's straddlers, whose rigidity came
from the arms being < 2 wide between PINS; k0_00 has no pins), and the PI/advisor's
proposed prune "a 2-crowd is a mixed-sign V or contains an axis-aligned blocker" is FALSE as
a local geometric statement (both tilts here are in (0°, 45°)). What survives is the
box-level census: which pairs of cover boxes admit a 2-crowd (a sound over-approximation by
core disjointness, refinable by subdivision), and the count is the branching factor
N_pair(c) of §4.2. [M, `attempts/A85-k0-route/results/a85_reach_BL.json`, `a85_pairs_BL.json`]:
the BL reach set [1/2, 7/4]² × [0°, 90°) at A60's box width 0.15 with the σ-closed 7-bin tilt
partition has 678 cover boxes, **644 in the reach set by the sound test, 586 witnessed** (a
sampled pose meets the widened box); of the 207 046 unordered pairs, **44 516 survive the
core-disjointness prune, 37 788 after one subdivision, 33 656 after two** — N_pair ≈ 3.4·10⁴
per corner. Sense table at level 2: PP 5402, MM 5507 (same-sense tilted pairs, 32 %), PM
7835, with an axis-touching member (A·) 10 483, straddling 45° (S·) 3243, SS 388. Same-sense
pairs are a third of the census — the local prune the advisor proposed would have been
unsound, and (b) is not an isolated exhibit.

(c) **[S] The rigidity that does exist is box-level, not a theorem here.** A square A whose
lowest vertex sits on the bottom wall at tilt θ_A ∈ (0°, 45°) leaves, inside the box, only the
two wall wedges (angles θ_A and 90° − θ_A) and the cap beyond its right/top vertex; a partner
B must enter one of these vertex-first (the extreme point of B ∩ {x < 1} in the −x direction
is a vertex of B), and near the wedge apex B's two unit edge rays (spanning 90°) cannot both
avoid the wall and A's edge (the admissible directions span ≤ 2θ_A < 90° for a vertex within
unit distance of the apex). So a 2-crowd partner of a wall-apex square at small tilt must
intrude far from the apex — exactly the pocket where cores of coarse boxes collide. The
exhibit in (b) evades every such lock-out because A floats (apex at height 0.7). The
quantitative content is the pilot's pair census under `cores_meet` + subdivision (sound
over-approximations of the crowd space); no sharper theorem is claimed or needed.

### 4.5 [S] Lemma K0-REUSE — the near-slot pocket is k1_00's tree

Lemma K0-PAIR (a) leaves, under the widening, the pocket "an axis-aligned (or nearly so) square
within δ of a corner slot plus its flush neighbour". [M] The targeted k0 critical-point search
(`attempts/A85-k0-route/results/cp85_k0_search.json`: A04's optimiser from V-crowder, rotated-
Trump, catalogue and atlas seeds, 516 runs, 262 k0 optima by the operational test "no square
axis-aligned within 10⁻⁶ at a corner slot", none below ŝ) shows this pocket is where the k0
landscape lives: the best k0 optimum has side 3.887213 (+0.0101 over ŝ) with FOUR axis-aligned
squares, corner squares displaced 1.6·10⁻³–8.6·10⁻³ from the slots; the smallest optimum with
NO axis-aligned square at all is at 3.905653 (+0.0286). The pocket is discharged by REUSE:

**Lemma K0-REUSE.** Let B be a node box of the k0_00 tree for a square at corner c whose
core satisfies K(B) ⊇ K_p := [δ_pin, 1 − δ_pin]² (at c; e.g. centre box within δ_pin of the
slot and tilt small enough that the inscribed axis box still contains K_p). Then every family
F reaching the node satisfies the root hypothesis of k1_00's tree T_{k1_00} at s0 (slack pin
cores, `protected_trees.md` §1) with that square as the pin owner, so T_{k1_00}'s subtree
applies verbatim below the node: its (K)/(C) leaves are (K)/(C) leaves here (Lemma P-TREE
Step 3 uses only the core hypothesis), and its (D) leaves localise the other TEN squares
within the landing radii of an image g·ẑ, g ∈ G_{k1_00} ⊂ D4, leaving the pin owner known
only to contain K_p (within δ_pin of the slot at tilt ≤ ~2°). A single-square ladder on the
owner (budget 0 for the other ten — vacuity certificates and Lemma-PD-type logic, A60's
confinement phase for ONE square) then lands the eleventh square, and the node is a (D)
leaf of the k0_00 tree. *Proof.* Immediate from the definitions: T_{k1_00}'s branching and
leaf rules are statements about F given a square containing K_p; nothing in them uses the
exactness of the pin (Lemma P-TREE §3). ∎ Consequently the eight corner pockets (4 corners ×
2 tilt senses, D4-equivalent) cost one k1_00 subtree (already owed, K0-O1) plus eight
one-square ladders (~10 certificates each at 1–500 s, A60's confinement law).

The k0 CP at 3.887213 is NOT in A37's atlas (nearest entry distance 0.78 to Trump; no atlas
hit) — the atlas is incomplete at k0 (as A37 warned) and this CP sits 0.0101 above ŝ, i.e. at
LP slack η ≈ −0.08 for its neighbourhood (dτ/ds ≈ 8), below A82's affordability gate: nodes
near it will not certify by LP and need a (D′) box. **Recommendation:** run A37's pipeline
(3S soft certificate, < 1 desktop-hour per entry) on the distinct k0 attractor structures of
`cp85_k0_search.json` before the campaign; each certified box turns a resister pocket into a
free (D′) leaf. Nothing in the soundness of the tree depends on this.

### 4.6 [T+M] Drain boxes at the k0 ghosts (PI/advisor directive, 2026-09-02) — the list and the price

Directive: a k0 residue that does not die by LP at depth 2 and sits near a k ≥ 1 family gets a
NEW discharge box baked around that family's critical point, consumed as a (D′) leaf.
**The list [M, `cp85_k0_search.json`, nearest-family assignment by `atlas85.in_atlas`]:** of
the 262 k0 optima, **12 lie within 0.02 in side of s0** (offsets 0.0101–0.0116), all
classified NEW_below_3.9, all OUTSIDE every atlas box; by nearest atlas family: **#9 (s_min
3.887416; 5 ghosts at L∞ distance 0.070–0.090, box h = 0.0103, miss 0.059+), #8 (3.887045;
5 ghosts at 0.015–0.089, h = 0.0100, best miss 0.0047), #7 (3.886832; 1 ghost at 0.146), #11
(3.888014; 1 ghost at 0.025, h = 0.0109, miss 0.014).** No other family has a k0 ghost within
0.02 of s0 (the next k0 optima start at +0.020 and the first with no axis-aligned square at
all is at +0.0286).

**Where to centre the box [T].** A box around the FAMILY's CP that reaches its k0 ghost must
have radius ≥ 0.07–0.09 in L∞ (family 9) — 20× the radius A36 certified around Trump
(3.7·10⁻³, 17 IV certificates, days of work) and 1.5–9× every A37 box; a second-order (FJ +
interval-Hessian) basin of that size around a NOT-CP saddle-type point is not something the
A35/A36 machinery has ever produced, and its cost would be open-ended. It is also
unnecessary: the (D′) leaf needs the tree's RESIDUE box (landing scale ~1.6·10⁻³, §1) inside
the discharge box, and the residue contracts onto the k0 ghost itself, not onto the family's
CP. So the drain is centred at the **ghost** z_g (a jammed k0 optimum at side s_g ≥ s0 +
0.0101), where A37's stratum-blind soft certificate (mode 3S: σ ≥ V_soft(h) on ‖z − z_g‖_∞ ≤ h,
no criticality needed — atlas meta: "value certificates are sound regardless of class") gives
V_soft(h) = s_g − h to 10⁻⁶ on every NOT-CP/soft entry of the atlas (the measured slope is
exactly 1: e.g. entry 3, 3.885403 / 3.884903 / 3.883903 at h = 1/2000, 1/1000, 1/500). Hence
**h_max = s_g − s0 = 0.0101–0.0116 ≥ 6× the landing radius**, and the certificate's window
coverage is free (σ ≥ s0 on the box, Lemma K0-ATLAS, no dilation). A36-type hard basins are
needed only for ghosts with s_g − s0 < 1.6·10⁻³ — there are none in the census (and none can
exist below +0.0101 unless the search missed a structure; a residue chain that lands on an
unknown point at side < s0 + 1.6·10⁻³ is the BDBFS discovery loop of A37, and would be the
most interesting object in the campaign).

**Price per drain.** A37's pipeline: 3S certificate 4–31 s of checker wall per box
(`atlas_final.json` `wall_secs`), the full audit → ladder → refine → certify → gates chain
< 2 desktop-hours for all 37 boxes ≈ 3 min per box; A36 hard basin (only if ever needed):
≈ 1 desktop-day per family (A35+A36). So **12 ghost boxes ≈ 1 desktop-hour**, before the
structural dedupe (the 12 sides 3.887213–3.888698 are ≤ 12 structures; A37's collapse rate
32 → 10 suggests 4–6). Consumed by `atlas85.in_atlas` if written in A37's box format (34
rationals, A22 order, θ in radians, `results/atlas85_convention.md`).

**Decision rule for the k0_00 tree (as directed):** at every node of depth ≥ 2 — (i) LP kill if
η ≤ −0.21 (A82's eps_geo affordability gate; the pilot's depth-2 rows in §7 say how often);
(ii) else, if the node's alive/ghost structure is within the drain radius of a certified
ghost box → (D′) leaf, or of a Trump image → ladder to (D); (iii) deepen only where neither
applies, and every deepened residue that lands on a new point at side ≥ s0 + 1.6·10⁻³ is
drained by a fresh 3S box (3 min) rather than bisected. The price consequence is in §8.

## 5. [T] Lemma K0-ROT — rotation stationarity (selected form) and the ghost radius

### 5.1 Statement, at drain-v3 rigour

Let P be a packing at side m that is a **σ-minimiser** (D1: σ(P) = m = s(11) = min over all
configurations of the axis-parallel extent). For φ ∈ ℝ let R_φ P be the rigid rotation of the
whole configuration by φ about any point (translations do not change extents, so the point is
immaterial); it is feasible (interiors stay disjoint), so σ(R_φ P) ≥ σ(P) for all φ. Write
h(θ) = (|cos θ| + |sin θ|)/2 for the half-extent of a unit square at tilt θ, x_i, y_i for
centres, X(φ), Y(φ) for the two extents of R_φ P, σ = max(X, Y). X(φ) = max_i (x_i(φ) +
h_i(φ)) − min_i (x_i(φ) − h_i(φ)) is a max/min of finitely many functions that are smooth in
φ except at the kinks of h (axis-aligned squares, where h has one-sided derivatives ±1/2), so
the one-sided derivatives D^±σ := lim_{φ→0±} (σ(R_φ P) − σ(P))/|φ| exist. Let L, R, B, T be the
extremal contact sets (the squares attaining the left/right/bottom/top extents), and for a
square i let D⁺h_i := d/dθ h(θ_i + ·) at 0⁺ and D⁻h_i := d/dθ h(θ_i − ·) at 0⁺ (so D⁺h_i =
(cos θ_i − sin θ_i)/2 = −D⁻h_i for θ_i ∈ (0°, 90°), and D⁺h_i = D⁻h_i = +1/2 at θ_i ∈ 90°ℤ).
Then, with x_i′ = −y_i, y_i′ = x_i under +φ about the origin (the origin cancels):

    D⁺X = max_{i∈R}(−y_i + D⁺h_i) + max_{i∈L}(y_i + D⁺h_i),   D⁻X = max_{i∈R}(y_i + D⁻h_i) + max_{i∈L}(−y_i + D⁻h_i),
    D⁺Y = max_{i∈T}(x_i + D⁺h_i) + max_{i∈B}(−x_i + D⁺h_i),   D⁻Y = max_{i∈T}(−x_i + D⁻h_i) + max_{i∈B}(x_i + D⁻h_i),
    D^±σ = max over the TIGHT axes (X = σ, and/or Y = σ) of D^±(extent).

**Lemma K0-ROT.** At a σ-minimiser, D⁺σ ≥ 0 and D⁻σ ≥ 0. Equivalently: for each rotation sense
there is a tight axis and a pair of extremal contacts on its two walls (r ∈ R, l ∈ L, resp.
t ∈ T, b ∈ B) whose centre-height difference plus tilt-derivative terms is ≥ 0, e.g. for the
sense −φ on the X axis: y_r − y_l + D⁻h_r + D⁻h_l ≥ 0. ∎ (Proof: the one-sided derivative of a
max of finitely many one-sided-differentiable functions is the max of the derivatives over
the active ones; minimality gives both signs.)

**Exact bookkeeping / what the lemma does and does not say.** (i) The centre-height term
(y_r − y_l, up to ±(m − 1)) is NOT small against the tilt terms (|D^±h| ≤ 1/2): the advisor's
one-line form "the extremal wall contacts cannot all be tilted in the same rotational sense"
holds ONLY when both walls' contact sets are single squares at the same height (then
y_r − y_l = 0 and same-sense tilts give D⁻X < 0 or D⁺X < 0), or more generally when the
contact heights cannot compensate. With contacts spread along the walls the condition is
trivially met (Trump: D⁺σ = D⁻σ = 3.877, §5.2). (ii) A single tilted pair (r, l) on a uniquely
tight axis is a codimension-1 condition (y_r − y_l = D⁺h_r + D⁺h_l exactly): the generic
degree-2 thin branch of `structure_lemmas.md` L2 in rotational form. (iii) Axis-aligned
contacts resist rotation in BOTH senses (D^±h = +1/2), which is why the advisor's "or
axis-aligned" clause is right. (iv) The lemma binds MINIMISERS only: as a (C) leaf it lives
in the selected form of `stratum_kill` (§9), and the tree's boxes localise F = Δ_λ P, so the
test must be run over the P-boxes for all λ ∈ [1, λ_max] (centres scaled by 1/λ — a
(λ_max − 1)·coord widening, as in Lemma B-NO). (v) Certificate form without calculus: a
**rotation-descent leaf** = a rational rotation (cos φ, sin φ) = ((1 − u²)/(1 + u²), 2u/(1 +
u²)) and an interval proof that σ(R_φ P) < σ(P) for every P in the node's (widened) box; this
is the drain lemma's improving direction restricted to rigid rotations and needs no
derivative in Lean — only "σ(R_φ P) ≥ σ(P) at a minimiser", which is the definition.

### 5.2 [M] Trump is rotation-stationary with a V-shaped profile; the ghost radius

`attempts/A85-k0-route/code/rot85.py` → `results/rot85.json` (floats, A03 data): both axes
tight; contacts L = {0, 3, 4}, R = {2, 5, 10}, B = {0, 1, 2}, T = {5, 6}; D⁺X = 3.033, D⁻X =
3.877, D⁺Y = 3.877, D⁻Y = 2.281, hence D⁺σ = D⁻σ = 3.877172 (finite differences of σ(R_φ ẑ):
3.877083 at φ = 10⁻⁷, agreeing to 3·10⁻⁵). The value ≈ ŝ is the diagonal corner pair (BL and
TR corner squares, axis-aligned, D^±h = 1/2): rotating a full-diagonal pair grows the extent
at rate ≈ ŝ. So σ(R_φ ẑ) = ŝ + 3.877|φ| + O(φ²), and the **rotational ghosts at side ≤ s0 are
exactly |φ| ≤ 1.0574·10⁻⁷** (bisection, both senses); their centres move by ≤ 2.034 · φ =
2.15·10⁻⁷ (max centre radius 2.034 about the container centre) and their tilts by 1.06·10⁻⁷ —
inside the (D) landing radii (1.6·10⁻³, 2.1·10⁻³) by factors 7·10³ / 2·10⁴, and inside the
tube. **Canary.** The ghost is a legitimate k0_00 packing; the engine's canary (a node
realised by an image within tolerance 10⁻⁵ is never certified) covers it, since every ghost
pose is within 2.2·10⁻⁷ of an image pose. The V-shape (not a flat direction) is also why the
ghosts are not a "rotational family" of critical points: ẑ is the unique minimum on its
rotation orbit, consistent with A22's rigidity.

**Use in the tree.** (1) A free (C) rule at DEEP nodes where the extremal contacts are
determined by the boxes (all wall-touching squares localised): a node is a (C) leaf under the
selected form if, for one sense, every admissible contact pair over the box violates the
inequality (interval arithmetic on the four formulas). At shallow nodes (the seed's 8 cores
with 3 free squares) the free squares can be any wall's contact, so the rule is silent — it is
not a lever on the price. (2) In the pair enumeration (C3) it prunes NOTHING by itself (Lemma
K0-PAIR (b): crowd members need not be wall contacts, and same-sense crowds exist).

## 6. Composition (what closes the k0_00 instance)

For every m ∈ [3.82, ŝ] and every packing P at side m:
1. some corner box of P is met by ≤ 1 square ⇒ Lemma K0-FREE (needs k1_00's tree at every
   side of W, i.e. O1–O5 of `protected_trees.md` §5 for k1_00 with δ_basin = 0.1305 ≥ 0.0571):
   P does not exist (m < ŝ) or is a Trump image (m = ŝ); or
2. every corner box is doubly met ⇒ F = Δ_λ P satisfies H_B (Lemma K0-WIDEN) ⇒ the tree T_B
   (or the interior-first tree of §2(i), whichever is built — both are sound; H_B is a
   strengthening usable inside the interior-first tree as free (T) leaves wherever a corner
   NO-family appears) sends F, up to D4 (Lemma K0-D4), to a leaf: (K) Lemma B ⇒ no P; (C) ⇒
   no P; (T) ⇒ case 1; (D′) ⇒ no P (Lemma K0-ATLAS, m ≤ ŝ < s0); (D) ⇒ the scale tube ⇒ m ≥ ŝ
   with equality only at P = g·ẑ.
Hence no packing at m < ŝ (the lower bound, ∀-packings), and every packing at ŝ is a Trump
image (uniqueness; no k0_00 packing at ŝ). The exact-stratum hypothesis is used nowhere; the
selected form (§9) is needed only if K0-ROT leaves are used.

| # | obligation | form | status |
|---|---|---|---|
| K0-O1 | k1_00's tree closed on W (regime 2 = whole window) | Lemma P-TREE, A84 O1–O5 | OPEN — the dependency |
| K0-O2 | root occupancy at s0 | Theorem A38.1 | DONE (certified) |
| K0-O3 | scale-ray tube at landing radii | `certs/tube_I_none_landing_…json`, `verify_tube.py` | DONE (T = 0.1279 ≥ 0.0571) |
| K0-O4 | the tree at s0 (§2(i) or §4.2) with (K)/(C)/(T)/(D)/(D′) leaves | A60 engine + `atlas85.py` | priced §8 |
| K0-O5 | Theorem U at ŝ (K0-FREE equality case) | `theorem_u.md`, certified | DONE |
| K0-O6 | (optional) K0-ROT leaves ⇒ selected form of `stratum_kill` | §9 | Lean-readiness note only |

## 7. [M] Pilot laws (`attempts/A85-k0-route/notes/pilot_report.md`)

Engine: A84's copy of the A60 stack re-parametrised for k0_00 (`code/class85.py`, `tree85.py`:
no pins, all eight images with exact witness families, `results/witnesses_k0_00.json`,
re-verified: pairwise gaps > 0, contained; alive gate = max over eight images; canary =
`images_realizing` over eight images). Exact phases: minutes. LP phase: ≤ 3 slots, lp_time
900 s, cert_time 300 s + eps_geo repair, commit gate 6 GB.

**7.1 Corner reach set and pair census (exact; §4.4).** BL reach set: 678 cover boxes (w =
0.15, σ-closed 7-bin tilt partition, a_min 0.34), 644 sound / 586 witnessed; pairs: 207 046
unordered → 44 516 / 37 788 / 33 656 after core-disjointness at subdivision 0 / 1 / 2; the
BL box set is σ-closed and maps exactly onto the other corners' covers (`corner_map_check`
0 bad at every corner; the surviving PAIR set is σ-closed to 98.9 % — the rational core's
t-grid dependence, harmless: the prune is sound either way).

**7.2 Alive gate (exact; `a85_gate_samples.json`).** Pair nodes at BL, budget 9: 27 702
attemptable (82.3 %), 5 954 unkillable; image-compatible pairs per image: 12 (g0, g4 — the
images whose BL corner is Trump's own) and 2 for each of the six others; every image has a
compatible BL pair (canary set intact). Sampled multi-corner nodes: BL+TR (budget 7) 97.3 %
attemptable / 1.0 % unkillable / 1.7 % contradictory (n = 300); BL+BR+TR (budget 5) 43.3 /
1.0 / 55.7 % (n = 300); all four corners (budget 3) 17.9 / 0.2 / 81.9 % (n = 1000), with
the D4-canonical fraction 0.120 (orbit size 8 for all 1000: **the /8 of Lemma K0-D4 (ii) is
exact on the seed**). Effective four-corner node count: 33 656⁴ × 0.179 / 8 ≈ 2.9·10¹⁶.
**The seed as a cover is dead at every level:** even level 1 alone is 2.8·10⁴ attemptable
LP nodes at budget 9 (≈ 1.3·10⁴ CPU-h at the measured 1 700 s per attempt, §7.3) before any
expected kill; the seed's sound value is the (T) leaves (§3) and (C) prunes at fine boxes.

**7.3 LP decision rows at s0 (`a85_lp_samples.jsonl`; A38-G7).** All nodes single-core,
budget 10, no pins, warm pool 697 columns from A38's nodes.

| node | source | τ (A38) | τ (A60 engine, 900 s) | η | LP s | cert s | verdict |
|---|---|---|---|---|---|---|---|
| l1_008 | A38 level-1 cell | 9.633 | 9.876 unconv. | −0.12 | 949 | 661 | FAIL; eps_geo 0.002/0.004 FAIL (801 / 1168 s) |
| l1_053 | A38 level-1 cell | 9.583 | 9.664 unconv. | −0.34 | 1014 | 644 | FAIL; eps_geo FAIL (1052 / 832 s) |
| l1_043 | A38 level-1 cell | 9.581 | 9.778 unconv. | −0.22 | 1010 | 692 | FAIL; eps_geo FAIL (416 / 568 s) |
| l2_p114_010 | A38 depth-2 cell | 8.569 | **9.000** unconv. | **−1.00** | 1066 | 632 | **PASS** (first certified k0_00 interior kill at s0) |
| l2_p215_011 | A38 depth-2 cell | 8.622 | 8.806 unconv. | −1.19 | 995 | 709 | FAIL: 32 witness boxes at depth 56, 8 exact HOLES + 24 undecided; eps_geo 0.002 re-solve τ = 8.955, certificate total 9.977 < 10 but the holes persist (FAIL); 0.004 round in flight at close |
| l2_p210_001 | A38 depth-2 cell | 8.600 | 8.727 unconv. | −1.27 | 1043 | 860 | FAIL: 16 witness boxes, 2 exact HOLES + 14 undecided at depth 56; eps_geo 0.002 τ = 8.871, total 9.977 < 10, holes persist (FAIL); 0.004 round in flight |
| cor_near_b178 | BL reach box, near an image | — | 9.548 unconv. | −0.45 | 953 | 685 | FAIL; the eps_geo re-solve converges to τ = 10.000 (LP-alive: an image-adjacent resister, correctly not certifiable) |

Laws. (i) **Level 1 does not decide** with the A60 engine either: η ∈ [−0.34, −0.12] after
900 s, unconverged, and every certification and eps_geo repair fails (A38's finding
reproduced with the modern oracle; the fractional η band that A82 certified on the k4 tier
at 3.833 does not certify here at budget 10 — the coverage holes of an unconverged oracle at
τ ≈ 9.7 are the failure mode). (ii) **Depth 2 decides:** τ = 8.7–9.0 = budget − 1 (A60's law
η ≤ −1 reappears at the second bisection level), and the first cell PASSes cold; the other
two FAIL on coverage HOLES (2 and 8 exact holes plus 14–24 undecided witness boxes at certification depth 56) although their repaired certificate totals are 9.977 < 10 — A38's failure mode (oracle coverage gaps), now measured with certification-in-the-loop: the LP has the slack, the certificate does not close at the default depth / witness caps. (iii) Cost per decided node:
≈ 1 000 s LP + 630–860 s certification (+ 800–1 200 s per eps_geo round) ≈ 0.5–0.9 CPU-h,
×1.5 A84's budget-6 nodes. (iv) A38-G7 is closed: T_decide(s0) ≈ 1 700 s at depth 2 with
certification-in-the-loop; at depth 1 it does not exist (undecidable at any cap tried).
(v) S2–S5 (pair and multi-corner nodes) not run: the 3 h LP cap was consumed by S1 (free commit 1–3 GB under the other campaigns until the end).

## 8. Re-price

Units: CPU-h; a desktop-day = 24 CPU-h at one slot (A84's unit) or 72 CPU-h at the three
slots the memory gate allows. Reference prices: A84 §7.1 — k0_00 ≥ 100 desktop-days plain
(≥ 2 400 CPU-h), 25–30 with the A58 corner seed; A38 §9 — 1·10⁴–1·10⁵ CPU-h floor,
open-ended (no decision constant).

**8.1 The tree that is priced** (§6 route 2 built as the interior-first tree, §2(i)): root =
Theorem A38.1 + `d4_wlog` → 216 level-1 cells of T(s0) × [0°, 90°] (the /8 is here), bisection
b = 8 per level (A27 shape), single conditioned square until the LP decides, then A60's
conditioning depths j = 1, 2 on the interior triple and confinement of the outer squares, with
(T) leaves at corner NO-families, (D) leaves onto the images whose witness lies in T(s0), (D′)
leaves onto atlas + ghost boxes, and the §4.6 decision rule at every node of depth ≥ 2.

**8.2 The measured constants (§7.3).** Level 1 (box half-width 0.052): undecided, 0/3 — no
LP is spent there (A38's 44 float kills were uncertifiable; treat level 1 as pure branching).
Depth 2 (half-width 0.026): τ = budget − 1.0…1.27 on 3/3, cost 1 000 s LP + 630–860 s
certification per node, first-pass PASS 1/3, eps_geo repair 800–1 200 s per round; the
certified-kill fraction is f₂ = 1/3 at the A60 defaults (depth 56, eps_geo 0.002/0.004, cert_time 300 s): the two FAILs have certificate totals 9.977 < 10 and fail only on 2–8 exact coverage holes + 14–24 undecided witness boxes; the lever is certification depth / witness feedback at solve time (A38-L2), unmeasured, and f₂ ≈ 0.85 is the scenario in which that engineering closes them. Depth 3 (A38: τ 8.56–9.25,
η −0.75…−1.44) unmeasured here; A38's τ trend (−0.5 per level) says f₃ ≥ f₂.

**8.3 The count.** Nodes: N₂ = 1 728; N₃ = 8·N₂(1 − f₂); N₄ = 8·N₃(1 − f₃); … until the
residue is image/ghost-bound (A38's five τ = 10.000 cells + 3 Trump cells + 34 atlas cells at
level 1 seed the (D)/(D′) chains). Per-node cost c = 0.47 CPU-h (PASS first pass) to 1.1 CPU-h
(two repairs). (D) side in the quotient: the images with a witness in T(s0) only — A84's
per-image laws (ladder queue ≈ 1 300 kills at ≈ 60 s, landing L24, then j = 1, 2 covers ≈ 60
LPs each and eight outer-square confinement ladders at O(10) certificates each) ≈ 30–60 CPU-h
per image chain, ≤ 3 chains ≈ 100–200 CPU-h; (D′)/drains ≈ 1 desktop-hour for the 12 ghost
boxes (§4.6) + the atlas lookups (free).

| scenario | f₂ = f₃ | N₂ + N₃ + N₄ | LP/cert CPU-h | (D)+(D′) | total CPU-h | desktop-days (3 slots / 1 slot) |
|---|---|---|---|---|---|---|
| repairs succeed | 0.85 | 1 728 + 2 074 + 2 488 | 3 000–6 900 | 150 | **≈ 3 200–7 000** | 45–100 / 130–290 |
| first-pass only | 0.33 | 1 728 + 9 216 + 49 152 → deeper | 2.8·10⁴–6.6·10⁴ before depth 5 | 150 | ≥ 3·10⁴ (A38's picture with decided nodes) | ≥ 400 / ≥ 1 200 |

**8.4 The three cuts, separately and stacked.**
* **C1 (D4):** ×1/8 on every level — realised in the 216-cell root (1 728 depth-2 nodes
  instead of 13 824) and on the (D) side (≤ 3 image chains instead of 8). Sound (Lemma K0-D4).
  Worth ≈ 8× on the LP frontier: without it the "repairs succeed" row reads ≈ 25 000–55 000
  CPU-h.
* **C2 (teleport):** sound ∀-packings (Lemma K0-FREE); removes A84's stuck-only caveat and
  makes the corner-crowd hypothesis available to every node for free; on the priced tree it
  contributes (T) leaves only where a corner NO-family occurs (the confinement phase of the
  eight outer squares — ≤ 10 % of the (D)-side cost, not of the frontier). Dependency: the
  k1_00 campaign (200–300 CPU-h, A84). **Price effect on k0_00: ≈ 0 on the frontier, ≈ −10 %
  on the (D) side.**
* **C3 (corner seed as cover):** DEAD. N_pair = 3.4·10⁴ per corner; four-corner tuples
  2.9·10¹⁶ after the exact prunes and the /8; level 1 alone (2.8·10⁴ attemptable pair nodes at
  budget 9, where the LP has η ≈ −0.3 at best by the S1 rows) costs more than the whole
  interior-first tree. No finite exact case list (Lemma K0-PAIR (b)). Its sound residue is
  Lemma K0-REUSE (the near-slot pocket = k1_00's tree) and the (C) prunes at fine boxes.
* **Added mid-attempt:** (D′) atlas leaves + ghost drains (§4.3, §4.6): remove the ghost
  resisters (the nodes at η ≈ −0.08 near the k0 CPs at s0 + 0.0101 that no LP can certify) for
  ≈ 1 desktop-hour — without them those pockets would be deepened indefinitely (A38's "five
  τ = 10.000 cells" are exactly this geography). Lemma K0-ROT: no price effect (deep-node (C)
  rule, selected form).
* **Stacked:** the priced route is C1 × (A60 engine decides at depth 2) × (D′)/drains, with
  C2 as the soundness upgrade; **k0_00 ≈ 3 200–7 000 CPU-h if f₂ ≈ 0.85, i.e. 45–100
  desktop-days at three slots** — a 3–30× cut on A38's floor, in line with (not below) A84's
  "≥ 100 desktop-days at one slot" plain figure, and A84's 25–30-day seeded figure was
  unfounded (the seed is a 10¹⁶-node cover). **The order-of-magnitude cut the brief asked for
  does not exist along C1–C3; the constant that decides between the two rows of the table is
  certification reliability at η ≈ −1 (f₂), i.e. eps_geo/oracle engineering, not geometry.**
  A single further measurement (deeper certification of the two hole-FAILs, then ~20 depth-3 nodes) pins it.

## 9. T4 — the `stratum_kill` re-split (Lean-readiness note; no `lean/` edits)

**Where a selection enters, and where it does not.** The k0_00 instance built from §3–§4 with
(K)/(C)/(T)/(D)/(D′) leaves is a ∀-packings statement and instantiates `stratum_kill` AS
STATED (`TopLevel.lean`: `∀ i ≠ trumpStratum, ∀ s ∈ wnd, ∀ z, CfgPacking s z → ¬InStratum i
s z`) for i = k0_00 — A84's "the corner seed forces the selected form" is void (§3 Remark).
A selection is needed only for leaves that use minimality: K0-ROT rotation-descent leaves, and
any A71 stuck-row / CC-2′ crowd rule used as a (C) leaf.

**The statement change, if such leaves are used.** Replace the single axiom by two:

    axiom stratum_kill_all : ∀ i ∈ AllForm, ∀ s ∈ wnd, ∀ z, CfgPacking s z → ¬InStratum i s z
    axiom stratum_kill_min : ∀ i ∈ MinForm, ∀ s ∈ wnd, ∀ z, CfgPacking s z →
        (∀ s' z', CfgPacking s' z' → s ≤ s') → ¬InStratum i s z

with `AllForm ∪ MinForm = {i ≠ trumpStratum}` (a decidable partition by class name; today
MinForm = ∅). The added hypothesis is global σ-minimality of z ("z attains s(11)"), the
weakest form under which rigid rotations are improving directions; local minimality would
also do but is not what B.SEL supplies. **Who supplies it.** (1) The lower bound: the top-level
proof takes the attained minimiser z* at side s* (D1 attainment, node B.SEL / `attained_thm`
in `Attain.lean`), places s* ∈ wnd (`lb_382` and s* ≤ ŝ from `trump_packs_at_shat`), and picks
its stratum by census exhaustiveness (`exists_stratum`, node B.CENSUS); at that point
`∀ s' z', CfgPacking s' z' → s* ≤ s'` is exactly the attainment property of z*, so
`stratum_kill_min` applies to z* verbatim. (2) The uniqueness clause at ŝ: once s(11) = ŝ is
proved, every packing at side ŝ is a σ-minimiser, so both `s_eleven_unique` (direct route) and
`unique_via_chain`'s `hstuck` (every stuck packing at ŝ is a packing at ŝ) supply the
hypothesis for free. No other consumer of `stratum_kill` exists (`#print axioms` on
`s_eleven_ge`/`s_eleven_unique`). **Cost:** one axiom split, one `have hmin :=` at each of the
two consumers; the K0-ROT leaf rule itself is a new checker clause (`rotation-descent`:
rational (cos φ, sin φ), interval evaluation of σ over the box) whose Lean statement needs no
derivative — only `σ (R_φ z) ≥ σ z` from minimality and the interval bound. Readiness: the
tree's Lean replay (`Zones.lean` rules + `checkCaseI_kill` per (K) leaf + Lemma K0-ATLAS as a
value-certificate consumer of A37's boxes, which are NOT yet in the Lean corpus — a new
obligation "atlas box ⇒ σ ≥ V" per used entry, A37's re-checker `a37_check.py` being the
current arbiter) is the same corpus-replay shape as trump5's.

## 10. Findings ledger (A85's `notes/findings.md` is the proof doc, as for A80–A84)

* [T] **Lemma K0-FREE**: a corner box met by ≤ 1 square teleports the packing into k1_00's
  MONOTONE hypothesis at the same side; with k1_00's P-TREE this excludes the packing at every
  m < ŝ and makes it a Trump image at ŝ (Theorem U). ∀-packings; A84's "stuck-only" caveat on
  the corner seed is void. The exact-class question is irrelevant (K1 climbs).
* [T] **Lemma K0-D4**: equivariant quotient, /8, with the mod-G transport of (K)/(C)/(T)/(D)/
  (D′) verdicts; instance (i) via Theorem A38.1 + `d4_wlog`, instance (ii) on the seed (the
  D4-canonical fraction measured 0.120).
* [T+M] **Lemma K0-PAIR**: no finite case list — the corner 2-crowd space has interior and
  contains same-sense pairs (explicit exhibit; 32 % of the 33 656 surviving pair boxes are
  same-sense); at most one axis-aligned member (w = 0). The advisor's "mixed-sign V" prune is
  unsound as a local statement.
* [T] **Lemma K0-WIDEN** (w = 0.0255 whole-window), **K0-ATLAS** ((D′) leaves, no dilation,
  no window obligation), **K0-REUSE** (near-slot pocket = k1_00's tree + one-square ladder).
* [T+M] **Lemma K0-ROT**: rotation stationarity with the exact centre-height term; the
  advisor's one-line form holds only for single same-height contacts; Trump has D⁺σ = D⁻σ =
  3.877 (V-profile), ghosts at side ≤ s0 within 2.2·10⁻⁷ / 1.06·10⁻⁷ of an image; a deep-node
  (C) rule in the selected form only, no price effect.
* [M] **The seed as a cover is dead**: 644 reach boxes, 33 656 pairs per corner, 2.9·10¹⁶
  four-corner nodes; level 1 alone costs more than the interior-first tree.
* [M] **A38-G7 closed**: with the A60 engine the k0_00 interior-first tree does not decide at
  level 1 (0/3, η −0.12…−0.34, all repairs fail) and decides at depth 2 (τ = budget − 1.0…1.27
  on 3/3, first cold PASS `certs/k0_00/s1int_l2_l2_p114_010`), at ≈ 1 000 s LP + 630–860 s
  certification per node; f₂ = 1/3 at the A60 defaults, the two FAILs being coverage-hole failures with certificate totals 9.977 < 10 (lever: certification depth / witness feedback, A38-L2).
* [M] **k0 landscape**: 262 k0 optima from 516 targeted runs, none below ŝ; the best at
  s0 + 0.0101 (four axis-aligned squares 1.6·10⁻³–8.6·10⁻³ off their slots), the first with no
  axis-aligned square at s0 + 0.0286; 12 ghosts within 0.02 of s0 near atlas families 9/8/7/11,
  all outside the atlas — drained by 3S boxes centred at the ghosts (h = s_g − s0 ≥ 6× the
  landing radius), ≈ 1 desktop-hour; family-centred basins would need radius 0.07–0.09 and are
  not the route.
* [F] **Price**: 3 200–7 000 CPU-h (f₂ ≈ 0.85) or ≥ 3·10⁴ (f₂ = 1/3); no order-of-magnitude cut
  along C1–C3; the lever is certification reliability at η ≈ −1.
* [F] Process: exact phases 7 min; LP phase 7 nodes in the 3 h cap at three slots (LP 7 029 s +
  cert 4 882 s + repairs); S2–S5 not run; free commit sat at 1–3 GB throughout under the other
  campaigns — no gate reading was logged at launch (the waits file stayed empty); free commit read 1.0 GB during the LP phase with the three shards resident and 11.9 GB at close, so the shards launched into a dip or the gate was not consulted — a process finding against the chore, recorded here.

## 11. Files

`docs/proofs/k0_route.md` (this file); `attempts/A85-k0-route/`: `code/` (A84 engine copied:
`class85.py`, `tree85.py`, `rot85.py`, `cp85.py`, `atlas85.py`), `results/` (`rot85.json`,
`a85_reach_BL.json`, `a85_pairs_BL.json`, `a85_gate_samples.json`, `a85_lp_samples.jsonl`,
`cp85_k0_search.json`, `atlas85_*.json`, `pilot_summary85.json`), `notes/` (`pilot_design.md`,
`cp_design.md`, `pilot_report.md`), `certs/k0_00/` (new files only); `lean/depgraph.json`
C.K4TIER note (chip A85 → released) + svg; REGISTRY row; LOG entry.


## 12. Lean status (A86, 2026-09-03)

Lemma K0-ATLAS (§4.3) is `PackingCert.Atlas.atlas_dilated_kill_fold` (`AtlasBridge.lean`; checker `AtlasKernel.lean`,
the trivial-reach / extent form in `(cx, cy, t)`, boxes tilt-folded into `[0, pi/4]`): with `L >= s0` every side `m < s0`
is discharged at once — the extent of the dilate is `<= s0 - (lambda - 1)` exactly.  The 12 ghost drains of §4.6 and
A37's 37 boxes are emitted and replayed (`AtlasData.lean`, `AtlasCheck.lean`, 48/49 with `L >= s0`, `h_max` about half of
A37's radius, ghosts at 5.1e-3..5.8e-3 = 3.2-3.6x the landing radius; `attempts/A86-lean-wave7/notes/t2_atlas.md`).
The `stratum_kill` re-split of §9 is stated (`StratumKillAll` / `StratumKillMin`, `Composition.lean`) with both consumers
proved (`s_eleven_ge_of_split`, `s_eleven_unique_of_split`); the (T) teleport leaves are consumed as (C)/(D) leaves of the
k1_00 tree through `teleport_packing` (unchanged).  See `lean/lean_wave7_A86.md`.
## 13. The FULL CHAIN for k0 at n = 11 on [3.82, ŝ] (A264, 2026-09-22) — every link tagged

Read top-down; a link tagged [T-computed*] is a certificate whose detached chain has not finished (its index says
how much is done); [C] links are the obligations.  Files in `docs/proofs/` unless noted.

1. **A packing of 11 at side s ∈ [3.82, ŝ] is family-stuck or reduces to the k ≥ 1 classes** [T] — `normal_ring.md`
   §1.2 (Lean `normal_ring_value`); the k ≥ 1 classes are the k1_00 / k5 trees (their own ledgers, not this list).
2. **NORMAL FORM** [T]: among the packings at side s a lexicographic maximiser of (Φ₁, Φ₂, Φ₄, Φ₃) exists with P1
   (touch-normal), P2 (row-normal modulo longer rows), P2′, P3, P4 (RETREAT) — `normal_ring.md` §1 (Lean
   `exists_normalForm`; the compactness step is [T-prose]); P1⁺, the family form — `box_meeters.md` §1.1.
3. **BAND-COUNT / HOLE-ONE** [T]: ≤ 1 square contains O, every other square meets the unit band — `peel.md` §2.1,
   `normal_room.md` §2.1 (Lean `hole_one_tilt`, `band_count` [T-prose]).
4. **MEETERS SPLIT** [T]: a doubly-met corner box has ≤ 1 toucher per wall, none touching both, every further
   meeter floats (SAME-WALL, WEDGED-SEAL, TWO-CORNERS) — `box_meeters.md` §0, §2 (Lean `same_wall_core`,
   `meeters_split` [T-prose]).  Corner types PAIR / THIRD / JAM / FLOAT2 — `no_jam.md` §1.
5. **COUNT + ROOM ⟹ n ≤ 9 for every corner type** [T]: if every unit square disjoint from the minimal box-serving
   structure S_min contains O then n ≤ 9 — `no_jam.md` §2.3 (Lean `jam_count_core`, `no_jam_of_count`); the
   third-meeter type is free by monotonicity.  So NO-JAM(11) = ROOM(JAM ring) ≤ 1, per JAM corner (sectors):
   5a. TL sectors of a JAM corner = **pair3** (row of two + one wall square, 4 parameters) [T-computed*, A262 chain3,
       verifier `verify262`; not started at exit — chain3 waits for search262].
   5b. BL sectors = **pair3 at the BL corner with C's wall drop T_u** [T given STRIP] + **STRIP** — A265: a TWO-square,
       s-free, sector-free statement (C, X and the wall seal the strip; `strip_plug.md` §1): [T] for a flat C in
       standard orientation, [T-computed] on 323 rings (no square free of {C, X} enters the strip).  A266
       (`last_two.md` §1): **[F] as A265 stated it for a tilted C** — "h_u, h_v < 1" is not "C meets the open box"
       once θ_C > 0 (C meets (0,1)² iff h_u cos + h_v sin < cos + sin − sin cos, Lean `open_box_tilted`), and between
       the two a flat square under C is a free square in the strip (drawn); the flat-C chord proof does not carry
       (chords are bounded by C's lower-left edge, up to h_u + sin θ_C).  On the true domain (C meets the box, X
       above C): [M] 60/60 in-domain points certify at radius 0.0025, exact pocket empty; [T-computed*] `strip266`,
       a 5-parameter LEFT-SHADOW box tree (Lean `left_shadow`, own verifier `verify266`) — priced at ~5·10³ CPU-h
       for the 27 root cells (535 s per 1/1200 sub-cell; A265's 1–3 CPU-h was wrong: the 1° tilt bins cost 0.017
       of a 0.005–0.02 margin), so launched BUDGETED on the six ring-relevant cells (150 000 boxes each, the rest
       OPEN 'budget', the index records the certified volume).  **And `pair3` has not started** (A262's chain3
       waits for search262, alive at exit): the BL sector is [T-computed*] on two chains.
       **A267 (`strip_enclosure.md`): STRIP₂-IN-RING [T-prose]** — the corner-box entry is closed by Lemma
       WEDGE-FLOAT [T] (no free square of the strip has its centre at or below height 1; needs neither A nor
       WEDGED-SEAL; Lean `wedge_float_core`), the C–X entry is a WEDGE along C's upper-left edge that a poke
       cannot cross (depth ≤ w_max/2 ≤ 0.11 vs ≥ 0.30 to T_u's top edge; Lean `wedge_extent_core`), on an explicit
       ring domain (D1)–(D2), (U1)–(U9) holding on 43/43 JAM rings with positive margin (`hyp267`); off that
       domain STRIP₂ stays [T-computed*] (`strip266`).  So 5b = STRIP₂-IN-RING [T-prose] + `pair3` (not landed).
       **A271 (`ring_domain.md`)**: of the ten domain conditions, (D1), (D2), (U1), (U2), (U9) are THEOREMS from the
       JAM hypotheses H1–H3 (Lemma SLOPE + Lemma LOW: a floater sharing its box with a floor toucher has L_h ≥ 1.121;
       BLOCKER-SIDE's mirror puts X above C's upper-left line; X_low > 1.406 from the window), (U8) is [M] positive
       (margin 0.094) and **(U3)–(U6) are FALSE as consequences of H1–H5** (drawn: |φ − θ| ≥ 13°, X meeting T_u by a
       sliver) — they are RING-level facts; STRIP₂ itself is [M] true on every violator (`probe271`, sup t → 0 only as
       h_v → 1).  So 5b = STRIP₂-IN-JAM [T-prose: H1–H3 + (U3)–(U6) + (U8)] + the five ring inequalities on the JAM-ring
       family [M; ~10³ CPU-h as a corner-local residual, not launched] + `pair3` (not landed).
       **A272 (`strip_jam.md`)**: on every violator the square's best attempt is stopped by X's RIGHT BOUNDARY
       shadowing T_u's top (C never active; sup t = −0.017 over H1–H3, at X FLAT, `left272`); the problem reduces [T]
       to the DISC LEMMA (a point q above L_h at distance ≥ ½ from the convex sets Ξ = left of X's right boundary and
       Γ = right of C's left boundary, within 1/√2 of the strip: impossible), tilt-free, five parameters — [M] on all
       of H1–H3 (sup slack −0.005, only as h_v → 1), NOT proved; the case q_y > X_top with Q left of X is dead by
       Lemma CL [T] (so (U8) is folded, never assumed).  So 5b = STRIP₂-IN-JAM [T-prose under (U3)–(U6)+(U8) OR under
       the DISC LEMMA; Lean `strip_two_in_jam_of_disc`] + the disc lemma's certificate [~20 CPU-h on R, ~10² on H1–H3,
       not launched] or a proof + `pair3` (not landed).
       **A273 (2026-09-23):** the DISC LEMMA as stated is [F] (exact witness `witness273`); the corrected DROP LEMMA
       (the whole cone conv(D(q, ½) ∪ {p}) misses int Ξ, int Γ) is 4-parameter (h_v-invariant) and certified by a
       box-valid penumbra tree + independent verifier over (θ, φ) cells (`attempts/A273-disc-lemma`, running, hours
       not 10² CPU-h) EXCEPT the corner θ ≤ 5° ∧ φ ≤ 5°, where STRIP₂'s own slack → 0 (≈ 0.15 θ² at φ = 0): that
       layer needs a hand proof (or A271's ring inequalities).  So 5b = STRIP₂-IN-JAM [T-prose, the DROP form] + the
       drop tree [T-computed when verify273 passes, outside the corner] + the corner [C] + `pair3`.
       **A276 (2026-09-23):** the corner is CLOSED by hand: `docs/proofs/flat_x.md` -- Theorem FLAT-X [T] (φ = 0, θ ≤ 30°: the
       intruder is the flat square resting on C's top line against X's right edge, corner (1, C_top) at distance (1 − c) c from
       T_u, the 0.25 θ² halved by the probe) and Theorem CORNER [T] (0 ≤ θ, φ ≤ 5°: case split on Q's left vertex with the
       three pins R_X / T / L; at φ > 0 the flat square is dead outright, slack first order).  Lean `Statements/Open/FlatX.lean`
       (cores [T], `strip_two_in_jam_corner` [T-prose]).  So 5b = STRIP₂-IN-JAM [T on the corner (A276) + T-computed outside it
       (A273's drop tree; c5_4 / c5_5 at θ 25–30° capped, still open)] + `pair3` (not landed).
       **A280 (2026-09-24):** A273's steep-C OPEN layer (θ ≥ 25°, 24 capped / open cells) was a MISSING PRUNE: the open
       leaves have X wholly above T_u (H2 fails; (D-low)) and the h_u → 1 corner is excluded by Lemma LOW; drop slack
       negative at every open leaf [M].  tree280 (A273's test + DLOW / SEP / LOWF) closes the bench cells in ≤ 327 boxes,
       verify280 PASS; the 29 steep cells run gated on A273's chain (`attempts/A280-drop-steep/code/run280.sh`).  So 5b =
       STRIP₂-IN-JAM [T on the corner + T-computed outside it once run280 lands (LOWF leans on (F4)(c) prose)] + `pair3`.
   5c. j = 2 opposite: room 0 [M]; j = 2 adjacent: rings exist, capacity 1 [M] — the same per-corner sectors apply
       (`three_lemmas.md` §4.4); j ≥ 3: none on the window [M].
   5d. Indirect jams (a non-toucher blocker), FLOAT2 corners, a middle toucher above X: **[C] = two CAP-2 statements** (A277, 2026-09-23,
       `float2_room.md`): n ≤ 8 + cap(S_8) with every blocker a pocket square, so what n = 11 needs at a non-PAIR corner is CAP-2 of its two
       box meeters — BL-CAP-2(C, D) for FLOAT2, BL-CAP-2(A, C) for the indirect JAM and the middle toucher above X (no two disjoint BL-sector
       misses; diameter test, Lean `cap2_of_diam`); ROOM is one more than needed and FALSE for FLOAT2 whenever a blocker outside S_8 misses O.
       [T] ONE-DROP, MUTUAL; LOW with a floating D; STRIP-C / STRIP-D = 5b's strip lemma iff the blocker serves its far box.  **The FLOAT2
       witness float262.json is [F] as a normal-form object**: D's floor drop is free (A blocks nothing), the corner is a JAM corner after one
       drop; with Y blocking it, P1 still lands D (J_D = +0.024); [M] `float277` sup ≤ 0 in the 4-square P1-sense model.  Certificate `cert277`
       (6 / 5 parameters, diameter) benched 12/12, priced 30–1000 / 3–100 CPU-h, not launched.  Lean axiom `bl_cap2_float2` [C].
       **A278 (2026-09-24, `no_float2.md`):** [T] FLOAT-SLOPE (case (N) of MUTUAL is empty; X, Y outside {C, D}); [T] SHADOW-CELL reduces
       NO-FLOAT2 to the 4-square statement L (a wall cell whose part outside D is unreachable by any admissible square); [T-computed] A277's
       witness is landed by the flat floor cell with shadow margin 0.032 and by SWEEP; [C] NO-FLOAT2 (residual (NEST): Y under a high D),
       certificate > 10^3 CPU-h naive, not launched -- so `bl_cap2_float2` stays; [C] BL-CAP-2(A, C) with S1-S4, cert277 jam 3-100 CPU-h not
       launched.  Lean `Statements/Open/NoFloat2.lean` (axioms `no_float2_of_local` [T-prose], `float2_local` [C]).
       **A279 (2026-09-24, `nest_residual.md`):** the NEST sub-residual: [T] NOT-BOTH, D HIGH, (Sigma) (shallow nests impossible: tan alpha > 0.95
       at eta -> 0), (WEDGE), FLAT-C; cells N_Y / N_X named and tested; count chase: third meeters of c01, c10 forced, "Y meets B" not; [M] nest279
       running at exit (no NEST quadruple in hand); [C] NEST-emptiness.  Erratum: (NEST) is the P1-sense residual, L's shadow residual is larger.
       Lean `Statements/Open/NestResidual.lean` (4 cores [T], no new axiom).  `float2_local`, `bl_cap2_float2` unchanged.
   5e. Adversary / search: 399 structured starts, capacity ≤ 1 always, no 11-witness [M].
6. **BOX-MEETERS(11)** [T from 5]: every box has exactly two meeters, wall touchers, eight distinct — `box_meeters.md`
   §5 (Lean `box_meeters_262` from the axiom `jam_count` [C = 5a–5d]).
7. **ROW CLASSIFICATION** [T-prose]: each wall carries a row of two, a row of three or an open pair — `normal_ring.md` §3.1 (prose [T]; Lean `rows_classified` a documented axiom).
8. **WINDOW EXCLUSIONS** (which pinwheels of rows exist below ŝ):
   8a. Rows of three, exactly flat walls, mixed senses at tilts ≥ 0.703° on every wall: A261's LP certificates
       [T-computed*: 11/50 verified at A261's exit; `cert261.jsonl` says which; M1 last].
   8b. The slab (some wall in (0, 0.703°), not all): A263's 492 engine jobs [T-computed*, queued after WE].
   8c. **The all-near-flat cube of every mixed pattern: [T]** — `three_lemmas.md` §3 (Lean `slab_cube_264`).
   8d. Exactly one sense, common tilt, rows of two: this is the normal family D′ / the hybrid ring — not excluded,
       it exists; its room is 10.
   8e. Mixed senses with per-wall tilts exist from s = 3.9298 > ŝ [M, A258] — outside the window.
9. **LOCKS AND OPEN PAIRS** [T]: an open pair survives only HELD by a free square (UNLOCK = P2′; LIFT) —
   `locked_wall.md` §1; unequal tilts survive only as locks — `open_pairs.md` §4.  Non-ADJ walls carry a free square
   in the unserved slot [T, Lean `nonadj_free_meeter`].
10. **ROOM: every free square of the hybrid normal ring contains O**:
    10a. Normal D′ (four rows): A259's PAIR tree [T-computed*: index filling, all ok] + A260's LAYER (PLUG) [T +
         T-computed, verified 0 bad] — `normal_room.md`, `locked_wall.md` §4.
    10b. Hybrid, common tilt, all-ADJ, e ≤ ½: A260's hybA / hybB (81/81) / hybAB [T-computed*: 8/81 at A260's exit].
    10c. Hybrid, independent tilts, all-ADJ: A263's P2 ∧ WE ∧ WS [T] reduction + [T-computed*: P2 41/81 cells in
         A263's chain, five OPEN (2,4 / 2,5 / 3,4 / 3,5 / 3,6) — A265 [T]: the OPEN leaves are a SIDE mismatch (P2
         tested at 3.8771 on boxes all-ADJ only near 3.82; the failing square is at the centre line, not the corner,
         and is a real P2 miss at 3.8771 where P2 is not required) — re-run at the ADJ-consistent side s_eff (Lean
         `adj_side_bound`, `p2_of_adj_side`) + graded plug: 2,4 / 2,5 / 3,4 certified (`verify265`), 3,5 / 3,6 in
         A265's second lane (`certs/P2265_index.jsonl`) — `strip_plug.md` §2; WS 3 cells, WE 1 cell, no OPEN].
    10d. Non-ADJ (wide gap, e up to 1.169): ROOM is [F] as a bare-ring statement; STRUCTURE closes the strip:
         GAP-CELL, BLOCKER-SIDE, STRIP-CHAIN [T] for e ≥ sec φ₁ at common tilt; the case 1 + w − sec ≤ e < sec and
         the wedge case [C] — `three_lemmas.md` §2.  A265 [T]: the derived count is TWO free squares in the gap
         (the brief's "> 3" is not a consequence), and the statement the chain needs is CAPACITY-2 — no two
         interior-disjoint free squares both missing O (Lean `gap_needs_two_misses`) — weaker than ROOM ≤ 1;
         CAPACITY-2 on the wide gap [C] via P1 on the lower gap meeter (`strip_plug.md` §3).  The non-ADJ
         certificates P2n / WEn / WSn are queued and will mark exactly this region OPEN.  A266 (`last_two.md` §2):
         **[T] CAPACITY-2 = three gap statements** (Lean `capacity_two_of_gap`): MISS-IN-GAP (every miss is a gap
         square of an unserved wall) ∧ GAP-HOLDS-ONE-MISS (two disjoint gap squares of one wall never both miss O)
         ∧ ONE-UNSERVED-WALL — all [C]; the brief's "two squares in the notch need width ≥ 2 > e" is [F] as an
         argument (they STACK); the stack's upper square contains O: [T] horizontally (`gap_interval_centre`: a
         unit interval inside [1, s − 1] contains s/2), [C] vertically (the wedge / lip cases of A264).  [M]
         `cap266`: no two interior-disjoint misses on any ring tried (A260's 32 non-ADJ rings have empty miss
         regions; wide-gap starts and 40 random non-ADJ rings in the chain); A265's FULL-corner witness is not a
         ring (its corner pair overlaps by 0.007).
11. **8 + 1 < 11** [T]: eight ring squares + one square containing O — Lean `openPairs_excludes`,
    `normalRoom_count`.  Hence no normal-form family-stuck packing of 11 on the window ⟹ **FAMILY-STUCK-EXIST(11)**
    fails in value form ⟹ with 1: **k0_00 is empty** (Lean `k0_value_of_factors`, `lockedWall_excludes`).
12. **k0_00 via CELLS / K0-FREE** [T]: Lemma CELLS (`ring_swap.md` §1.3, Lean `cells_swap`), K0-FREE = |Π| = 1;
    RAISE(0 → 1) is exactly 11 (`ring_swap.md` §0).
13. **The stretch (ŝ, 4)** [M only] and **uniqueness at ŝ** (the iterated form of VALUE-WLOG, `common_sense.md`
    §2.1 (i): SWAP-RIGIDITY k ≤ 3 [M], k ≥ 4 [C]) are outside this list.

**Still [C] or waiting, exactly (A266, 2026-09-22):** 5a/5b `pair3` (A262's chain3: NOT STARTED — search262
alive); 5b STRIP₂ off the ring domain ([T-prose] on it, A267 `strip_enclosure.md` §3; [T-computed*] `strip266`
elsewhere, budgeted: the full tree is ~5·10³ CPU-h); 5d (float262 / indirect jams,
in chain3); 6's Lean axiom `jam_count`; 8a–8b chains (A261 `cert261.jsonl`, A263's 492 slab jobs); 10a A259's
tree (verify259 rerun alive), 10b A260's hybAB; 10c A263's P2 (cell 4,4 open at 10 947 s, index 36/42 ok) / WE (1
cell) / WS (3 cells) chains and A265's lane (cells 3,5 / 3,6: `P2265_index.jsonl` has 3 rows at exit); 10d the
three gap statements of CAPACITY-2 (MISS-IN-GAP, GAP-HOLDS-ONE-MISS's vertical half + wedge + 1 + w − sec ≤ e <
sec, ONE-UNSERVED-WALL); the [T-prose] Lean axioms (`meeters_split`, `band_count`, `normal_form_step`, the three
corner lemmas of A264); the stretch.  **Running chains that must land for the chain to be all [T] /
[T-computed] on [3.82, ŝ]:** A259 verify rerun (10a), A262 chain3 (5a, 5b pair3, 5d), A263 WE / WS / P2 4,4 + the
slab jobs (8b, 10c), A265's lane (10c), A266's chain (5b strip266 — budgeted, so a hand proof or ~5·10³ CPU-h is
still owed).

