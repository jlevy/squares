# Lemma P-TREE: the protected tier as residual zone-trees — A84, 2026-09-03

Target: depgraph node **C.K4TIER** (the 16 K1-protected classes: {k4_03, k4_05, k4_06, k4_08,
k4_11, k4_13 = corners4} and the ten open k ≤ 3 classes), i.e. the last `stratum_kill`
pieces. After A65/A66/A71/A73/A74/A77/A80/A81 every GLOBAL-measure route for these classes is
closed with a named law (K1 sharpness; Lemma W‴/W⁗; Corollary S-08; reserve-plus; hinge wall).
This file proves that the route A83 made sound for trump5 — an s0 residual zone-tree with (K)
kills transferred by Lemma B and (D) discharges transferred by the contraction tube — is
sound for a protected class **with no exact-stratum hypothesis on the lower bound**, says
exactly where the exact hypothesis does enter, records the per-class constants (tube
direction, tube reach, pin-slack reach), and prices the tier from the k4_08 / k3_05 pilot.
Labels: [T] proved, [S] routine given cited items, [M] measured/computed exact, [F] finding,
[C] open. Companion files: `contraction_tube.md` (T1, Lemma SEAM), `closed_disjoint_bridge.md`
(Lemma B, B′, B-NO), `unique_transfer.md` / `theorem_u.md` / `h10_stuck.md` (what this
supersedes), `attempts/A84-protected-trees/` (pilot, tube sweeps, tier table).

## 0. Verdict

> **Lemma P-TREE HOLDS [T].** For a protected class S with pin set P_S, a zone-tree at s0 over
> the MONOTONE hypothesis "P contains axis-aligned unit squares at slots_S" (slack pin cores
> δ_pin), whose leaves are (K) PASS certificates, (C) logic kills, and (D) full localisations of
> the N = 11 − k_S free squares within (r_c, r_θ) of a compatible Trump image, proves — with
> Lemma B for (K) and the contraction tube in the class's own direction for (D) — that **no
> packing at any side m ∈ [ŝ − δ_basin(S), ŝ) contains S's pins**, and that every packing at
> side ŝ containing S's pins is a Trump image g·ẑ, g ∈ G_S. The exact-stratum hypothesis is
> used **nowhere on the lower bound** and enters **only** to read the equality case at m = ŝ as
> "not in class S" (Simp(g·ẑ) = trump5 ≠ S) — and even that reading is optional, because
> P = g·ẑ is the uniqueness conclusion itself. Consequently H10-stuck (U-O2) is a corollary,
> not a hypothesis, for every class whose tree closes, and Theorem U is not consumed at all
> (the (D) leaf localises all eleven squares, so A83 §4.3's Theorem-U pocket cap T′ ≈ 3·10⁻⁴
> is void for this route). **The protected tier is therefore "14 more trump5-like campaigns
> plus 2 shadow trees"** (§5: k4_05 and corners4 have NO compatible Trump image, hence no (D)
> leaves and no discharge obligation — but also no aliveness witness to contract onto).
> Constants [M]: tube reach in the class directions — classes whose Trump-frame pin set keeps
> square 3 (BL(0,1)) inherit trump5's wall E3c2-7e3, T = 0.0457 at A60's landing radii and
> 0.0574 (≥ ŝ − 3.82 = 0.0571, the whole window) at r = 6.5·10⁻⁴; classes that free square 3
> move to the scale-type wall E7c2-9e3, T = 0.130 at the landing radii (the whole window ×2.3).
> Pilot laws and the price: §6–§7.

## 1. Setting

Sides: s0 = 969271/250000, ŝ = Trump's side, s0 − ŝ = 4.0998·10⁻⁷. A *packing at side m* is
eleven closed unit squares with pairwise disjoint interiors in [0, m]². Slots are affine in the
side, k(s) = α + βs, β ∈ {0, 1}, |α| ∈ {1/2, 3/2, 5/2} (A56 P1; Lean `slot_tracking`).

* **Class and pins.** S is a Young class (D4-reduced), k_S pins, N := 11 − k_S. For the
  representative, P_S(m) = slots_S(m). **A_S := max |α| over the pin coordinates**
  (`attempts/A84-protected-trees/results/tier84_classes.json`: 3/2 for the ten classes with a
  BL(0,1)/(1,0)/(0,2)… arm, 1/2 for the corner-only classes k1_00, k2_01, k2_02, k3_05,
  corners4, and 0 for k0_00).
* **Monotone hypothesis M_S(m)**: P is a packing at side m with an axis-aligned unit square
  centred at every point of slots_S(m) (`ContainsPins`). **Exact hypothesis E_S(m)**: the
  skeleton of P is exactly S (`InStratum`). E_S ⇒ M_S after D4 normalisation (A78
  `containsPins_skeleton`, `class_kill`).
* **Compatible images.** G_S := {g ∈ D4 : g·ẑ satisfies M_S(ŝ)} — the Trump images whose
  upright squares realise S's pins. For g ∈ G_S let I_g ⊆ {0, 1, 2, 3, 5} be the Trump-frame
  indices of the squares g maps onto S's pins (A03/A22 indexing: 0 = BL(0,0), 1 = BL(1,0),
  2 = BR(0,0), 3 = BL(0,1), 5 = TR(0,0)). [M] `tier84.py`: k4_08 G_S = {id, transpose}, both
  I_g = {0,1,3,5}; k4_11 {id}, I = {0,2,3,5}; k4_03 {transpose}, I = {0,1,2,3}; k4_06
  {transpose}, I = {0,1,2,5}; k3_05 {xflip, rot90}, I = {0,2,5}; k3_04 two sets {0,1,5},
  {0,3,5}; k2_00 {0,1},{0,3}; k2_01 {0,2},{2,5}; k1_00 {0},{2},{5}; k0_00 all eight images,
  I = ∅; **k4_05 and k4_13 (corners4): G_S = ∅** (agrees with A71's exact G_S for the k4 tier).
* **The free squares of an image.** For g ∈ G_S, F_g := the N squares of g·ẑ not on S's pins
  (for k4_08-id: Trump's six free squares plus the BR corner square, which is a trump5 pin but
  free in k4_08). Their poses at s0 are the λ₀-dilates (λ₀ = s0/ŝ, centres only) — exactly
  the exact rational families of A65 `crowdfam.json` (min SAT gap ~10⁻⁷ > 0), which serve as
  the Lemma A57-3 alive witnesses and as the (D) targets.
* **The tree T_S at s0.** Nodes carry: the k_S slack pin cores K_p (axis-aligned, half-side
  a = 1/2 − δ_pin, centred at slots_S(s0); emitted as the degenerate-θ Box of half-width
  δ_pin/√2 so that A60's `Box.core()` yields hd = δ_pin), conditioned core boxes B₁…B_j
  (each a rational core K(B) ⊆ every unit square with (centre, θ) ∈ B), NO-families, and
  budget b = N − j. Children of a node: over a closed cover {B_i} of a zone Z × [0°, 90°],
  the NO child (no square with centre in Z; budget unchanged) and the YES_i children (some
  square with (c, θ) ∈ B_i; budget − 1), with A57 T5's pinguard: a YES box that contains a
  point of [slot ± δ_pin]² × {0°, 90°} is "parent" (never budget-decremented), a box whose
  core meets a pin core or a conditioned core without a shared witness is "contradictory"
  (a (C) leaf), and refinement of a box by a closed sub-cover keeps the budget (A57 T11).
  Leaves: **(K)** a `case-lp-certificate-v1` PASS at s0 for the node (frozen `verify_case.py`;
  soundness V.CASE Lean-proved), Σw < b; **(C)** contradictory/vacuous; **(D)** j = N with
  pairwise (c, θ)-disjoint boxes (θ mod 90 identified), each B_i within the landing radii
  (r_c on centres, r_θ on tilt in radians) of a distinct member of F_g for one g ∈ G_S —
  the bijection B_i ↔ F_g is the ladder's `hugs` map (A60 ledger §8.2).
* **Landing radii and the tube.** (r_c, r_θ) = A60's measured landings (1.4472·10⁻³ centre,
  2.0102·10⁻³ rad), certified at (1.6·10⁻³, 2.1·10⁻³). Tube_v(T, r) and Theorem T1 as in
  `contraction_tube.md` §1, for a centre-only direction v with v = β on the coordinates of
  the squares in I_g and v = ẑ_i/ŝ on every other centre coordinate — **v_{I}**, the
  "slot(I)" direction of A83's checker (its `direction_spec` accepts any pin list).

## 2. [T] Lemma P-TREE

**Lemma P-TREE.** Let S be a protected class, δ_pin > 0, and let T_S be a finite tree as in §1
all of whose leaves are (K), (C) or (D). Let, for each I ∈ {I_g : g ∈ G_S}, a tube certificate
Tube_{v_I}(T_I, r) with r ≥ (r_c + 3.6·10⁻⁷, r_θ) be verified, and put

    T_K(δ_pin) := ( (δ_pin/A_S)·ŝ − (s0 − ŝ) ) / ( 1 + δ_pin/A_S ),      (A_S = 0: T_K = +∞)
    δ_basin(S) := min( min_I T_I,  T_K(δ_pin) ).

Then:

(a) **[bound]** for every m ∈ [ŝ − δ_basin(S), ŝ) there is NO packing at side m satisfying
    M_S(m); a fortiori none with skeleton in class S;
(b) **[equality]** every packing at side ŝ satisfying M_S(ŝ) equals g·ẑ for some g ∈ G_S
    (if G_S = ∅ there is none); hence no packing at side ŝ has skeleton exactly S;
(c) **[s0 form]** for every m ∈ [ŝ − T_K(δ_pin), s0): every packing P at side m with M_S(m)
    either reaches a (K) leaf (impossible) or a (D) leaf, i.e. the dilated family Δ_λP,
    λ = s0/m, has its N non-pin squares within (r_c, r_θ) of F_g for some g ∈ G_S. (This is
    the tree's own content at s0; (a)–(b) are (c) composed with the tube.)

*Proof.* Fix m and P with M_S(m); λ := s0/m > 1 for every m < s0 (including m = ŝ, since
ŝ < s0). F := Δ_λP.

*Step 1 (F is a strict family carrying the root hypotheses).* By Lemma B.0 (Lean
`dilation_bridge`), F consists of eleven closed unit squares, pairwise disjoint as closed sets,
inside [0, s0]². Each pin square of P at slot α + βm dilates to an axis-aligned square centred
at (α + βs0) + (λ − 1)α (B.0(c), `slot_tracking`), i.e. within (λ − 1)A_S per coordinate of the
s0-slot. If (λ − 1)A_S ≤ δ_pin — which is m ≥ ŝ − T_K(δ_pin) by the definition of T_K (the
same algebra as Lemma SEAM's (K) condition, `contraction_tube.md` §4.1, with 1/A_S in place of
2/3) — then the slack core K_p (half-side 1/2 − δ_pin at the slot) lies inside the dilated pin
square (Corollary B′ / `bprime_containment`), with the pin square's (centre, 0°) inside
[slot ± δ_pin]² × {0°}. So F satisfies the root hypotheses of T_S in the certificate-core
sense, with k_S distinct owners.

*Step 2 (F reaches a leaf; owners stay distinct).* Every branching of T_S is a statement about
the family F and is exhaustive for it: "no square of F has its centre in Z" or "some square of
F has (c, θ) in some B_i" (closed cover; a vacuous box contains no admissible placement —
A57 T1, Lean `Zones.lean`). Descend from the root choosing a true branch. At a YES_i step the
witness square Q_i of F has (c, θ) ∈ B_i; it is distinct from the pin owners because B_i
passed the parent test (no point of [slot ± δ_pin]² × {0°, 90°} lies in B_i, and each dilated
pin's (centre, 0°) does — Step 1), and distinct from earlier witnesses because the conditioned
boxes are (c, θ)-disjoint with the 0°/90° identification (one square has one (c, θ mod 90°)).
Refinement steps keep the witness (the sub-cover is closed and covers the box). So at the leaf,
F has k_S pin owners and j distinct witnesses, and the budget b = N − j counts the remaining
squares exactly (A57 T5′.1 by induction on j).

*Step 3 ((K) leaf ⇒ contradiction).* The leaf certificate C (side s0, cores = the k_S pin cores
+ the j conditioned cores, NO-families of the node, Σw < b) PASSes. Each conditioned core
K(B_i) ⊆ Q_i (the core construction: K(B) ⊆ every unit square with pose in B). The ≥ b
non-owner squares of F are admissible, pairwise disjoint as closed sets, disjoint from every
owner hence from every core, and outside every NO-family of the node (that is the NO-branch
hypothesis for F itself — no B.2″ widening enters, because the hypothesis is about F, not
about P). By Lemma B (Lean `lemma_B` / `hcert_of_priced`, `checkCaseI_kill`) each is priced
(μ ≥ 1) and μ is additive over them: μ(total) ≥ b > Σw. Contradiction. So no P reaches (K).
(A (C) leaf is empty for F by the pinguard logic — Lean `Zones.lean` T5/T11 rules.)

*Step 4 ((D) leaf ⇒ the tube).* At a (D) leaf, F's N non-pin squares are the witnesses
Q₁…Q_N with (c_i, θ_i) ∈ B_i, and B_i lies within (r_c, r_θ) of the pose of the i-th member of
F_g (a bijection, `hugs`), for some g ∈ G_S. Apply g⁻¹ (D4 acts on packings at side m and on
families at side s0, commuting with Δ_λ: Δ_λ ∘ g_m = g_{s0} ∘ Δ_λ, `contraction_tube.md` §4.1;
`d4_packing`, `skeleton_d4`): P′ := g⁻¹P is a packing at side m whose pins sit at Trump's own
slot lines for the squares in I_g, and whose other squares, after dilation, are within
(r_c, r_θ) of the λ₀-dilated ẑ-poses. Per coordinate (Lemma SEAM §4.1 verbatim, with I_g in
place of trump5's pin set): pinned centre coordinate P′_i = α + βm = ẑ_i − t·β_i, w_i = 0;
free centre coordinate P′_i = F_i/λ = ẑ_i − t·ẑ_i/ŝ + w_i with |w_i| ≤ r_c(m/s0) + |ẑ_i|(s0 −
ŝ)/s0 ≤ r_c + 3.6·10⁻⁷; tilts unchanged, |w_θ| ≤ r_θ; side m = ŝ − t exactly, w_s = 0; here
t := ŝ − m. Hence (P′, m) ∈ Tube_{v_{I_g}}(T′, (r_c + 3.6·10⁻⁷, r_θ, 0)) whenever 0 ≤ t ≤ T′.
For m ∈ [ŝ − T_{I_g}, ŝ], t ∈ [0, T_{I_g}] and Theorem T1 for the certified tube gives m ≥ ŝ,
with equality only if P′ = ẑ. So m < ŝ is impossible — (a), with δ_basin the minimum over the
two conditions of Steps 1 and 4 — and at m = ŝ, P = g·ẑ — (b). (c) is Steps 1–3 alone, whose
only side condition is Step 1's. ∎

### 2.1 [T] Lemma PD (pin-drift logic kill) — the slack pocket and its closure

[F, from the pilot] With slack pin cores the residue ladder does NOT contract: the k3_05 scan
at δ_pin = 2·10⁻² stalls at max gap 0.0219 ≈ δ_pin from level 15 on while the residue grows
96 → 3862 boxes by level 28 (`results/a84_k3_05_ladder_j0_scan_pre_PD.json`; example box
(1.2504, 1.4344, 40.13°) = image square g5·sq8 displaced 0.02 INTO the slot square of the
pin at (1/2, 1/2)). Mechanism: a copy of an image square that penetrates a pin's slot square
by e < δ_pin meets no pin core, drops exactly one witness, and is alive-gated unkillable at
budget N − 1 (Lemma A57-3 is exact: the other N − 1 witnesses are a strictly separated family
clear of the slack cores). **The residue floor equals δ_pin**, and it is ≫ any landing radius.
A60's planned re-emission at δ_pin = 10⁻² (A83 §4.4) would hit the same floor on every
interior square (sq7, sq8, sq9 all touch pin corners, A59 §0).

The pocket is an artifact of the CORE: the family F = Δ_λP has, at pin p, the FULL unit square
Σ_p + d(λ), d(λ) = (λ − 1)α_p per coordinate (B.0(c)), and α_p points into the container for
every slot (L-family coordinate |α|: λ|α| = |α| + (λ − 1)|α| grows; R-family s0 − |α|:
λ(m − |α|) = s0 − λ|α| shrinks). So for every m in the range the actual pin covers the slot
square's interior-facing annulus and more.

**Lemma PD.** Let T′ ≥ 0, λ_max − 1 := (s0 − ŝ + T′)/(ŝ − T′), and let B be a YES box with
rational core K = K(B). If K ∩ Σ_p ≠ ∅ AND K ∩ (Σ_p + d(λ_max)) ≠ ∅ for some pin p, then for
every packing P at side m ∈ [ŝ − T′, s0) with M_S(m), no non-pin square of F = Δ_λP has its
pose in B — B is a (C) leaf for the whole side range. *Proof.* {d : K ∩ (Σ_p + d)
≠ ∅} = K − Σ_p is convex (Minkowski sum of convex sets), so it contains the segment
[0, d(λ_max)] ∋ d(λ) for every λ ∈ [1, λ_max]. Any square Q of F with pose in B contains K
hence meets F's pin square Σ_p + d(λ), so Q is that pin square; but a YES witness is distinct
from the pins (Step 2). ∎ (Lean: `Zones.lean`-style logic on the family, plus B.0(c).)
Canary: the box of an image square touching pin p does not fire the rule — its core misses
Σ_p at λ = 1 (the dilated image has gap ≈ λ₀ − 1 > 0 plus 1/2 − a). Pocket placements
(penetrating Σ_p at λ = 1) fire it, since at λ_max they penetrate deeper. The two-endpoint
test is the whole rule, and it is exact rational SAT on full unit squares.

Consequences: (i) the tree's logic kills use the drifted full pin square (stronger than the
slack core; the slack core is needed only inside the certificates, Step 3); (ii) T′ becomes a
tree parameter (the drift endpoint), so a tree is built for a declared reach T′ and its (C)
leaves are valid on [ŝ − T′, s0) — choose T′ = δ_basin(S); (iii) the (K) transfer needs
(λ_max − 1)A_S ≤ δ_pin, i.e. δ_pin ≥ A_S(T′ + 4.1·10⁻⁷)/(ŝ − T′): 1.79·10⁻² at T′ = 0.0457 and
**2.25·10⁻² at T′ = 0.0571 (whole window), A_S = 3/2** — so the whole-window design needs
δ_pin = 2.5·10⁻² rather than 2·10⁻² for the BL(0,1)-pinned classes (A60 measured 2·10⁻²
certifying at η = −0.81, LP ×8 slower; 2.5·10⁻² is unmeasured).

Remarks. (i) The dilation λ > 1 is used in Step 3 exactly as in Lemma B (atom additivity and
owner/non-owner disjointness); at m = ŝ it is λ = s0/ŝ > 1 still, so no S4-type contact
issue arises anywhere. (ii) The parent-test radius must be δ_pin (the full drift budget), not
the emitted Box's half-width δ_pin/√2 — otherwise Step 2's distinctness needs
(λ − 1)A_S ≤ δ_pin/√2 and T_K shrinks by √2. (A84 engine spec §1.3.) (iii) For an upright
image square (θ̂ = 0) the (D) box may sit at θ near 90°; "within r_θ" is the mod-90° distance
and the t ≈ 1 branch of `theorem_u.md` §3 applies. (iv) NO-families in a (D) chain (A60's
confinement route for the outer squares) are handled by Lemma B-NO exactly as in A60: the
confined non-owner has (λc, t) in the family's zone, which is the (D) localisation of that
square — no widening, because the conclusion is about F. (v) Nothing in the proof uses the
class beyond M_S and the constants A_S, G_S: the same lemma with k_S = 5, G_S = {id} is
Lemma SEAM for trump5.

## 3. [T] Where the exact-stratum hypothesis is — and is not — used

* **Not used:** the tree's branching (Step 2), the (K) transfer (Step 3), the (D) pull-back
  and the tube for m < ŝ (Step 4), and hence the whole lower bound (a). The tree never
  PRICES a Trump image — it localises it — so K1-protection (Trump images realise M_S at
  s0, hence no single certificate for the root exists) is not an obstruction but the reason
  the (D) leaves exist. This is the reframe the brief asked to verify: for the bound, the
  quantifier is ∀ packings with M_S, exactly `stratum_kill`'s ∀-packings form (A63's F3
  diagnosis, `unique_transfer.md` §1), and no selection (K*-maximal, teleport-stuck) is
  needed.
* **Used, once, optionally:** in (b), to conclude "no packing with skeleton EXACTLY S at ŝ"
  from "every M_S packing at ŝ is g·ẑ": Simp(g·ẑ) = g·trump5 has five simple squares, S has
  k_S ≤ 4. That is the InStratum-exact semantics of `instratum_bridge.md`, entering exactly
  where Lemma U-ROW's did (`u_ladder.md` §3) — but here it is harmless, because the
  alternative reading "the M_S packings at ŝ are Trump images" is precisely the uniqueness
  clause. Contrast the global-measure routes (P-B, U-ROW, boosted rows), where the exact
  hypothesis was load-bearing to REMOVE g·ẑ from a quantifier that would otherwise bind
  Trump (the monotone trap). The tree has no such trap: nothing it asserts is false of g·ẑ.
* **Consequences for the composition.** With T_S closed for S: (1) `stratum_kill`'s instance
  for S holds at every m ∈ [ŝ − δ_basin(S), ŝ] (at m = ŝ via (b) + the exact reading), and
  at m ∈ [3.82, ŝ − δ_basin(S)] iff plain slack-core kills cover that slab (A82's regime 1 —
  the seam, §5); (2) **H10-stuck (U-O2) for S is a corollary of (b)** — no packing at ŝ is
  in exact-S, stuck or not — so `unique_via_chain`'s `hstuck` is discharged for S by
  P-TREE without any stuckness argument, and `s_eleven_unique` can equally take the direct
  route (`unique_transfer` + `stratum_kill` + `trump_residual` + `basin`), since (b) is
  the ∀-packings statement; (3) **Theorem U (U-O1) is not consumed**: the (D) leaf conditions
  all N free squares (as A60 does for trump5's six), so there is no "10 exact + 1 free"
  pocket, and A83 §4.3's cap T′ ≈ 3·10⁻⁴ for the U-style (D) leaf does not apply — the
  per-class reach is the tube's T in the class direction (§4), 100× larger. A80's U-ladder
  and A65/A66's pair rows are therefore not on the critical path for any class whose tree
  closes. What they still could offer is a cheaper (D) leaf (fewer conditioning levels) —
  priced against the pocket amplification, not needed here.
* **What the lemma does NOT give:** the shadow classes. k4_05 and corners4 have G_S = ∅ (§1):
  no Trump image satisfies M_S, so a tree for them has no (D) leaves and must close by (K)/(C)
  leaves alone — A57's shadow-tree situation (k5_11/k5_16), whose root is LP-alive
  (corners4 τ(0) = 7.2545 > 7, A65; k4_05: A82's alive gate finds ≤ 6 of 7 at every scanned
  side, `alive_gate_grid.json`) but whose sub-strata are killable. P-TREE says nothing about
  whether such a tree closes; A57's measured law (interior-first depth-2 trees, 25+ kills)
  is the reference, and A66's corners4 rigidity exhibit says it is orientation-coupled.

## 4. [M] Per-class constants: tube directions, reach, pin-slack reach

Tube certificates in the class directions (`attempts/A84-protected-trees/code/tube84.py`,
A83's emitter driven with `pins = I_g`; arbiter `certs/verify_tube.py`, untouched; PASSes
written to `certs/tube_<label>_*.json` at 98 % of the measured wall and re-verified from
disk). Landing profile (r_c, r_θ) = (1.6·10⁻³, 2.1·10⁻³ rad); tighter profile 6.5·10⁻⁴ both.

All 19 distinct Trump-frame pin sets of the 14 image-bearing classes were swept (exact
bisection to 0.5 %, 42 certificates written and re-verified; `results/tube84_sweep.jsonl`):

| Trump-frame pin set I | classes (images) | T_max landing | T_max at r = 6.5·10⁻⁴ | wall |
|---|---|---|---|---|
| {0,1,2,3,5} (trump5, A83) | trump5 | 0.0457 | 0.0571+ | E3c2-7e3 |
| {0,1,3,5} | k4_08 (id, transpose) | **0.0457** | **0.0574** | E3c2-7e3 |
| {0,2,3,5} | k4_11 (id) | 0.0457 | 0.0574 | E3c2-7e3 |
| {0,1,2,3} | k4_03 (transpose) | 0.0457 | 0.0574 | E3c2-7e3 |
| {0,1,3} | k3_02 (id, transpose) | 0.0457 | 0.0574 | E3c2-7e3 |
| {0,2,3} | k3_03 (id) | 0.0457 | 0.0574 | E3c2-7e3 |
| {0,3,5} | k3_04 (transpose) | 0.0457 | 0.0574 | E3c2-7e3 |
| {0,3} | k2_00 (transpose) | 0.0457 | 0.0574 | E3c2-7e3 |
| {0,1,2,5} | k4_06 (transpose) | **0.1305** | 0.1680 | E7c2-9e3 |
| {0,1,5} | k3_04 (id) | 0.1305 | 0.1680 | E7c2-9e3 |
| {0,1,2} | k3_01 (transpose) | 0.1305 | 0.1680 | E7c2-9e3 |
| {0,2,5} | k3_05 (xflip, rot90) | **0.1305** | 0.1680 | E7c2-9e3 |
| {0,1} | k2_00 (id) | 0.1305 | 0.1680 | E7c2-9e3 |
| {0,2}, {2,5} | k2_01 | 0.1305 | 0.1680 | E7c2-9e3 |
| {0,5} | k2_02 | 0.1305 | 0.1680 | E7c2-9e3 |
| {0}, {2}, {5} | k1_00 | 0.1305 | 0.1680 | E7c2-9e3 |
| ∅ (pure scale ray) | k0_00 | 0.1305 | 0.1680 | E7c2-9e3 |

**[F] The tube law for the tier: T_max depends on the pin set ONLY through square 3 =
BL(0,1).** With 3 pinned, its corner on free square 7's left edge (A22 row E3c2-7e3) slides
tangentially at 0.39 per unit T (A83 §3) and T_max = 0.0457 / 0.0574 exactly as for trump5;
with 3 freed it contracts together with 7 and the binding row is the 7–9 flush pair
(E7c2-9e3, the scale-ray wall): T_max = 0.1305 / 0.1680, identical for all eleven such sets
(the pinned squares among 0, 1, 2, 5 never bind). Hence: the eight classes whose every image
pins BL(0,1) (k4_08, k4_11, k4_03, k3_02, k3_03; k3_04 and k2_00 through one of their two
images) inherit trump5's reach — the whole window only at r ≲ 6.5·10⁻⁴, i.e. one more ladder
level than A60's — and the corner-only / BL(0,1)-free classes (k4_06, k3_01, k3_05, k2_01,
k2_02, k1_00, k0_00, and k3_04 / k2_00 via their other image) get the whole window with margin
2.3 at A60's landings. For a class with two images of different type (k3_04, k2_00) the (D)
leaves of each image use that image's own tube, so the binding one is the BL(0,1) image.

Anisotropic points in the k4_08 direction (what "one more level" really costs): at
(r_c, r_θ) = (6.5·10⁻⁴, 2.1·10⁻³) T_max = 0.0525; (8·10⁻⁴, 2.1·10⁻³) 0.0516; (10⁻³, 2.1·10⁻³)
0.0500; (6.5·10⁻⁴, 6.5·10⁻⁴) 0.0574; (2·10⁻⁴, 2·10⁻⁴) 0.0621. So the whole window (0.0571)
needs the TILT landing tightened too, from A60's 2.0·10⁻³ rad to ≈ 6.5·10⁻⁴: the ladder halves
each coordinate every third level (measured: containment 2.23·10⁻³ → 1.14·10⁻³ over levels
21 → 24), so the centre needs ≈ 3 more levels and the tilt ≈ 5 — landing at level ≈ 29
instead of 24, i.e. ≈ +20 % on every ladder's queue (the deep levels' kills are the cheap
vacuity-type ones). Alternatively land at (6.5·10⁻⁴, 2.1·10⁻³) (3 levels) and cover
[3.82, ŝ − 0.0525] = [3.82, 3.8246] by plain kills — a 4.6·10⁻³ slab whose η law A82 has not
measured (its lowest k4_08 point is 3.8332 with τ* ≥ 6).

Pin-slack reach at δ_pin = 2·10⁻² (`tier84_classes.json`): T_K = 0.0510 for A_S = 3/2 (the
k4 classes except corners4, k3_01–k3_04, k2_00) and 0.1491 for A_S = 1/2 (k1_00, k2_01,
k2_02, k3_05, corners4); k0_00 has no pins (T_K = ∞, and its tree is pin-free). Hence

    δ_basin(S) = min(T_I, T_K) = 0.0457 (A_S = 3/2 classes, landing radii) / 0.0574 (tighter)
               = 0.130 (corner-only classes, landing radii): the tube binds, never the slack.

A60's finding that δ_pin = 10⁻⁴ caps the route at 2.5·10⁻⁴ holds here too: δ_pin ≥ 1.8·10⁻²
is needed for the tube to be the binding constraint at A_S = 3/2; 2·10⁻² is the operating
point. **A60's slack qualification, reused** (`a60_slackcore.jsonl`, same trump5 cover leaves
re-emitted): δ = 10⁻³ and 10⁻⁴ — 4/4 PASS at η = −1, cost unchanged; δ = 10⁻² — 2/2 PASS
(η = −0.89 unconverged at 961 s, −1.0 at 319 s); **δ = 2·10⁻² — 6 PASS / 2 FAIL of 8**
(PASSes at η = −0.81, −0.75, −1, −2, −2, −1 with LPs 3–1000 s; the two FAILs are leaves whose
LP rises to τ = 5.000 = budget, i.e. the slack made them LP-alive — Y0411, Y0419). So the
certification law relaxes (fractional η now PASSes at 2·10⁻²), but the kill RATE drops by
≈ 25 % on trump5's PASS leaves at δ = 2·10⁻², and those leaves go to the deepen phase. Price
this as ×1.3 on the cover phase at 2·10⁻²; 2.5·10⁻² is unmeasured.

## 5. The seam per class and the composition obligation

For class S the window [3.82, ŝ] splits at ŝ − δ_basin(S):

* regime 2, [ŝ − δ_basin(S), ŝ]: Lemma P-TREE (tree at s0 + tube);
* regime 1, [3.82, ŝ − δ_basin(S)]: plain slack-core kills of M_S at grid sides (A82's scan;
  each fixed-side certificate at δ covers a slab of relative width δ/A_S below its side).

**A82 closed while this attempt ran (2026-09-02; `attempts/A82-side-scan`, LOG entry), and it
settles regime 1 for the k4 tier.** (F0) the aliveness cliff is a step of exactly one at ŝ
(m_fam 7 → 6 the instant Trump stops fitting, s_fit = ŝ to 3·10⁻⁸); (F1) η ≤ −1 is
geometrically impossible on the k4 tier at every side (exact 6-families give τ* ≥ 6 =
budget − 1 everywhere in W) — A60's η ≤ −1 law is a property of its zone-tree route, not of
fixed-side kills; (F2) the FIRST protected-class kills exist: k4_08 and k4_11 cold-verified at
m = 3.833212 with η ≈ −0.38 / −0.33 (`certs/a82/k4_08_958303_250000.json`,
`k4_11_958303_250000.json`, frozen verifier, 4/4 gates); (F3) the operative gate is eps_geo
affordability, budget − τ(m) ≳ 0.21; (F6) dτ/ds ≈ 7.3–8.0 on the k4 tier, so plain kills
reach up to m ≈ ŝ − 0.025 (0.21/8 ≈ 0.026 of slack needed); (F7) A82's certificates use
degenerate pins (shell ~10⁻⁸): each grid side must be re-emitted at δ = 10⁻² (slab
(s″/(1 + δ/2.5), s″] ≈ 0.015 wide), with ≈ 0.17 of headroom left after eps_geo — unmeasured.

Consequently, **for the four image-bearing k4 classes the seam OVERLAPS at A60's landing
radii**: regime 1 = plain slack-core kills on [3.82, ŝ − 0.025] (≈ 3 grid sides at δ = 10⁻²,
if the 0.17 headroom survives the slack), regime 2 = the tree on (ŝ − 0.025, s0] with
δ_basin(S) = 0.0457 ≥ 0.025 — a 0.02 overlap, no extra ladder level, and the tree's (K)
leaves transfer with δ_pin = 2·10⁻² (T_K = 0.051). For k4_06 (I_g ∌ 3, T = 0.130) the tree
alone covers the window. For the corner-only k ≤ 3 classes (k3_05, k2_01, k2_02, k1_00)
T = 0.130 also covers the window at the landing radii; for the BL(0,1)-pinned k ≤ 3 classes
(k3_02, k3_03, k3_04, k2_00) A82 has no crossover data (dτ/ds at budgets 8–9 unmeasured): either
the tighter landing (≈ level 29, whole window) or an A82-style scan per class. **The two
classes A82 flags as genuinely hard are k0_00 (η = 0.000 at 3.833212: the root LP has no
slack — k0_00 IS the unstratified problem) and corners4 (η = +0.011 there, never alive,
ghost-saturated by non-Trump families, orientation-coupled per A66)** — for them regime 1 is
empty and the tube is irrelevant to the (K) side; see §7.1.

**Obligation table (the last `stratum_kill` pieces), per class S:**

| # | obligation | form | status |
|---|---|---|---|
| O1 | tree T_S at s0, δ_pin = 2·10⁻², all leaves (K)/(C)/(D), every image of G_S at a (D) leaf | A60 engine (`tree84.py`), certificates verified by frozen `verify_case.py` | pilot §6; price §7 |
| O2 | tube certificate for each I_g of S at r ≥ landings | `certs/tube_I_*.json`, `verify_tube.py` | §4: done for the sets swept; ~1 min each |
| O3 | (D) landings ≤ (r_c, r_θ) of O2, mod-G bijection = `hugs` | ladder scan (exact) | pilot §6 |
| O4 | seam: either landing ≤ 6.5·10⁻⁴ (regime 2 = window) or plain kills on [3.82, ŝ − δ_basin] | O3 depth, or A82 scan + certificates | recommended: O3 depth |
| O5 | the exact reading at m = ŝ (Simp(g·ẑ) ≠ S) | census fact, Lean `Census.lean` | free |
| O6 | shadow classes k4_05, corners4 (G_S = ∅) | A57-type kill-only trees | OPEN, not covered by P-TREE |

Lean: (O1) is `stratum_kill`'s instance per class through `checkCaseI_kill` + `lemma_B` per
(K) leaf (corpus replay, A78 T5 pricing: 30–170 s per certificate) and the tree's branching
rules (`Zones.lean`); (O2)+(O4) is the tube obligation of `lean/tube_obligation_A83.md`, once
per direction; the pull-back Step 4 is Lemma SEAM's per-coordinate map with I_g. No new
analysis.

## 6. [M] Pilot laws (k4_08 and k3_05 with the A60 engine, δ_pin = 2·10⁻², Lemma PD)

Engine: `attempts/A84-protected-trees/code/{class84,alive84,tree84}.py` = A60's stack with
the class object of §1 (slack pins, both images' exact witness families — crowdfam's
`trump-sym` family and its exact transpose, re-verified: min pairwise gap 1.10·10⁻⁷ (k4_08) /
9.7·10⁻⁸ (k3_05), gap to the slack pin cores ≥ 2.0·10⁻²), the alive gate as max over images,
Lemma PD in the logic gate, containment against the hugged image square under both criteria.

**6.1 Interior census j = 0 (exact; A60's cover: 1152 boxes, w = 0.15, 8 t-cells).**

| class | budget (YES) | contradictory | attemptable | unkillable | images' interior squares |
|---|---|---|---|---|---|
| trump5 (A60, ε-fat pins) | 5 | 344 | 767 | 41 | 3 (sq7, sq8, sq9) |
| k4_08, slack cores only (pre-PD) | 6 | 280 | 772 | 100 | 6 (3 per image) |
| **k4_08, Lemma PD** | 6 | **316** | **752** | **84** | 6, each in an unkillable box, 0 canary violations |
| k3_05, pre-PD | 7 | 54 | 1002 | 96 | 6 |
| **k3_05, Lemma PD** (T′ = 0.130) | 7 | **84** | **984** | **84** | 6, each in an unkillable box, 0 canary violations |
| k3_05, clear corner TR zone (pre-PD) | 7 | 0 | 171 | 2 | 0 |

The unkillable count is ≈ 2× trump5's (one residue per image); Lemma PD recovers the pin
logic kills that the slack cores lost (280 → 316 for k4_08; trump5's 344 has one more pin).
k3_05's interior sees almost no pin (3 corner pins): 87 % of its cover is LP work at budget 7.

**6.2 Residue ladder j = 0 (exact).** k4_08 under Lemma PD
(`results/a84_k4_08_ladder_j0_scan.json`): 24 levels, residue 53–118 boxes (mean 75 —
A60: 21–52, mean 34, i.e. ≈ 2× for two images), contraction ratio gap/radius 2.4–4.5 (median
3.85) from level 6 on — **A59's 4.55 law holds**; cumulative kill queue 1299 (A60: 540);
**lands at level 24 with 59 boxes, all inside both criteria: centre containment
1.1427·10⁻³, θ 2.0102·10⁻³ rad, t 1.2191·10⁻³ — the SAME landing numbers as A60's square-1
ladder (1.1426·10⁻³ / 2.0102·10⁻³)**, so the (D) geometry of a protected class is trump5's
geometry per image, as Lemma P-TREE predicts. Canary: every image square sits in a residue
box at every level (`canary_ok` at all 24 levels, no engine bug).
k3_05 pre-PD (`…_pre_PD.json`): 28 levels, residue 80 → 3862 (diverging, ratio 3 → 99),
queue 11 646, only 293 boxes inside — the δ-floor of §2.1. **k3_05 under Lemma PD
(T′ = 0.130, |d_max| = 1.735·10⁻²): 24 levels, residue 53–117 (mean 75), ratio median 3.57,
queue 1542, lands at level 24 with 59 boxes, containment 1.14·10⁻³ / 2.01·10⁻³ rad — the same
landing as k4_08 and as A60, box for box in the last level.** So the interior (D) geometry is
class-independent per image (the three interior squares and their contacts are Trump's, the
pins only decide which logic kills are free); the class enters through the attemptable count
(752 vs 984) and the LP budget (6 vs 7).

**6.3 The P1 analogue (k4_08) [M, exact certificate].** Node = the four slack pins + the
NO-family "no square centred in the interior zone [1.1, 2.777]²" at budget 7 (alive gate:
4 of 7 witnesses outside the zone per image, attemptable). LP τ = 4.000 (η = −3.0,
converged, 52 s on 2743 warm columns from A55's k4_08 nodes), certificate PASS at depth 56
in 5 s (`results/nodes/k4_08/p1_interior.json`, `certs/k4_08/p1_interior.json`). Hence
**Lemma A84-P1(k4_08)**: every 11-packing at s0 containing k4_08's slack pin cores has a
square centred in the interior zone — the cover is the interior zone alone, as for trump5
(A59-P1 had η = −1 at budget 6; dropping the BR pin makes the NO child EASIER, not harder,
because the freed corner square must itself sit somewhere). **k3_05: the same node at
budget 8 (three corner pins + the interior NO-family): τ = 5.000, η = −3.0, converged in 17 s,
certificate PASS in 2.8 s — Lemma A84-P1(k3_05).** The margin does not shrink with fewer
pins (η = −1 → −3 → −3 for 5 → 4 → 3 pins): squares that cannot use the interior have
nowhere to go, so the interior-zone cover is the whole tree for every class whose images
keep three interior squares (all 14 image-bearing classes) — no whole-free-region cover.

**6.4 Cover kill rate, LP cost, ladder-queue kills (R5–R6; PARTIAL — the LPs sat at the
6 GB commit gate for most of the attempt: free commit 0.8–6 GB with A57 G1, A60 (cover +
slack tests), A61, A82, A78's Lean corpus builds and a 12 GB foreign process resident; 26 +
9 + 12 + 11 gate waits logged; the shards keep running to their 3 h caps and append to
`results/a84_k4_08_{cover,ladder,deepen}_j0*.jsonl`).**

| sample (k4_08, budget 6, lp_time 600, cert_time 300 + eps_geo) | n | PASS | LP-alive | cert-FAIL | η | LP s | cert s |
|---|---|---|---|---|---|---|---|
| cover boxes (nearest-to-image stratum first) | 3 | 2 | 0 | 1 | −0.83, −0.88, −0.78 (all unconverged at the cap) | 744, 679, 691 | 372, 676, 826 |
| ladder-queue boxes, levels 6–9 | 4 | 0 | 3 | 1 | 0.000, 0.000, 0.000 (unconverged at 600–710 s), **0.000 converged (L9)** | 601, 710, 643, 559 | — |

Laws, as far as three + four points allow: (i) cover kills at budget 6 exist and PASS at
fractional η ≈ −0.8 (A82 F1/F3: η ≤ −1 is unreachable on the k4 tier, the gate is eps_geo
affordability), at **≈ 700 s LP + 400–800 s certification per box — ×3 A60's mean LP (214 s)
and ×15 its certification (42 s)**; the one FAIL is the fractional-η certification failure
mode with a 676 s eps_geo repair. (ii) **The ladder queue is NOT a kill queue at this budget:
0/4 at levels 6–9, three at τ = 6.000 = budget after the cap and one CONVERGED at
τ = 6.000000 exactly.** The image gate says k = 5 (two witnesses dropped) but the LP finds
τ* = budget; an exact search for a 6th square (A57 alivewitness on the 5 kept image squares +
grid × tilt, `results/a84_k4_08_ladder_alive.json`) found NO integral witness — so this is
A82's k4-tier wall one level down (τ* ≥ budget − 0 fractionally, no 6-family on the grid),
not the vacated-spot family. These boxes are exactly A57 T11 / A60 G-A60-3 resisters: they
must be bisected at the same budget (deepen) or carried into conditioning depth j = 1 as
chain boxes, and their cost is the unmeasured item of the tier (A60 never ran its ladder
kills either: `progress/ladder_j0_s0.json` done 0 of 540). (iii) The census-level
attemptable/unkillable split (§6.1) is therefore an UPPER bound on what j = 0 kills; the true
j = 0 kill fraction on the queue is the deepen yield, to be measured (R7 did not start).

## 7. Tier price and composition

**Cost model (per class S, from A59 P0–P7 / A60's measured phases, re-scaled by the pilot):**

    cost(S) = Σ_g∈G_S [ cover_j0(S) shared across images
                        + ladder_j0(g) + Σ_{j=1}^{2} (cover_j + ladder_j)(g)   (interior triple)
                        + Σ_{j=3}^{N−1} confinement_j(g) ]                   (outer squares, budget-1 vacuity at the end)
              + deepen rounds on the cover resisters
              + tube certificate per I_g (done, §4)  + (regime-1 kills if landing > 6.5·10⁻⁴).

Measured inputs: A60 trump5 cover j0 — 767 LP attempts, kill rate 0.781 first pass, LP mean
214 s / median 82 s, certification mean 42 s, 41 CPU-h for 717 attempts, resisters
(LP-alive + cert-FAIL) 22 % → deepen; ladder j0 — 540 queue kills at 0.8–90 s; j = 1, 2 —
93–97 % of the level-1 cover free, residues 18 → 7 → 0; confinement O(10) certificates per
square at 1–540 s. Pilot inputs (§6): k4_08 census 752 attempts at budget 6 (A60: 767 at
budget 5), unkillable 84 (2×), ladder queue 1299 (2.4×), landing level 24 (=), residue 75
(2.2×); k3_05: 984 attempts at budget 7, ladder identical to k4_08's (queue 1542); LP-cost
multiplier at budget 6 vs 5: ×3 on the LP and ×15 on certification (§6.4, three boxes); the
ladder queue is a resister queue at j = 0 (0/4 kills), so its cost is the deepen/conditioning
term, unmeasured.

**Provisional price (before §6.3 lands; A60 unit costs, ×(1 + 0.5·(budget − 5)) for the LP
size, two images where G_S has two):**

| class group | classes | per class | tier |
|---|---|---|---|
| k4, image-bearing (I_g ∋ 3: k4_08, k4_11, k4_03; I_g ∌ 3: k4_06) | 4 | cover ≈ 750 LPs × ~330 s + 1300 ladder kills × ~60 s + 2 chains × (j1, j2 covers ≈ 60 LPs, 4 confinement ladders) + deepen ≈ **110–160 CPU-h ≈ 5–7 desktop-days at 1 slot, 2 days at 3** | ≈ 25 desktop-days at 3 slots |
| k3 (k3_01…k3_05) | 5 | cover ≈ 1000 LPs × ~430 s + ladder (residue ≈ 2× k4_08's if PD contracts) + 2 chains, 5 confinement squares ≈ **200–300 CPU-h** | ≈ 40 desktop-days |
| k2, k1, k0 | 5 | budgets 8–10: LP cost grows (A82's budget-7 root LP already 700–850 s unconverged), images 2–8 per class (k1_00: 6, k0_00: 8) — chains per image; residue per image as above | **≥ 100 desktop-days, extrapolated — the size law of §7.1** |
| shadow classes k4_05, corners4 | 2 | no (D) leaves: A57-type kill-only trees; root LP wall (corners4 τ = 7.25 > 7) | not priced by this route (§3) |

Certificates per class: ≈ 750 + 1300 + 2 × (60 + 40) ≈ 2 250 (k4) / ≈ 3 000 (k3) / more
(k ≤ 2), all at s0; plus one tube certificate per direction (19 total, done); the Lean corpus
replay at 30–170 s per certificate (A78 T5) adds ≈ 1–2 days per class.

### 7.1 [F] The size law for k ≤ 3 (what explodes and what does not)

* The (D) side does NOT explode: per image the residue is trump5's (landing level 24, ratio
  ≈ 4, residue ≈ 35 per image) — Lemma P-TREE's "same geometry per image" is measured (§6.2).
  The number of chains is |G_S| × (N − 2) squares to condition after the interior triple: the
  outer confinement ladders multiply (k4: 4 outer squares; k3: 5; k0_00: 8 free squares that
  are trump5 pins in some image — and 8 images).
* What grows is the (K) side: the cover's LP budget (N − 1 = 6, 7, 8, 9, 10) and the number
  of attemptable boxes (k3_05: 1002 of 1152 vs 752 — fewer pins means fewer free logic kills
  and, per Lemma PD, fewer pin-drift kills), and the per-LP cost with the budget (§6.3
  measures the multiplier at 6 and 7).
* **k0_00 (A82 F4: η = 0.000 at 3.833212).** No pins, eight compatible images (I_g = ∅, pure
  scale tube T = 0.130), no logic kills at all (Lemma PD is vacuous; pinguard has nothing to
  meet): its tree is the zone-tree of the WHOLE problem, root budget 11, cover children at
  budget 10 whose LPs are the root LP of the unstratified problem (A82: 11.000 at 3.833, no
  slack; A08's record root certificate 10.72 at 3.82). Alive gate: 8 images × 11 witnesses; a
  cover box is attemptable only if it drops ≥ 2 witnesses of EVERY image — in the interior that
  is the same crowding as for the other classes, but the (K) leaves are budget-10 LPs with no
  pins, i.e. ≥ 10× A60's per-LP cost and no free kills. Estimated ≥ 2 000 LPs × ≥ 10³ s ≈
  ≥ 25 desktop-days at 1 slot for the cover alone, plus 8 image chains of 11 squares each —
  **the class that dominates the tier**, ≥ 100 desktop-days by itself. The A58 clear-corner seed
  (all four corners clear ⇒ ≥ 2 non-simple meeters in every corner box ⇒ ≥ 8 of 11 squares
  in the corner boxes, CC-2′ + A71's stuck rows SR-1/SR-2 as branching) would start the residual
  at budget 3 after eight YES conditionings — but it is STUCK-ONLY (next bullet), so the k0_00
  instance of `stratum_kill` would have to be re-split into the selected form (A78's chain at
  every side): a Lean restructuring, no new mathematics. Priced as a seeded tree: 4 corners ×
  a 2-square conditioning (a cover of the corner box's reach set ≈ 1 100 boxes per square,
  alive-gated against 8 images), then a budget-3 residual — the conditioning covers are ≈ 8 ×
  1 100 LPs at budgets 10…3, dominated by the first two (≥ 10³ s each): ≈ 25–30 desktop-days
  at 1 slot, still the largest single item.
* **corners4 (A82: η = +0.011 at 3.833212, τ(0) = 7.25 at s0; A66: emptiness orientation-
  coupled).** G_S = ∅: no (D) target — every leaf must be (K) or (C), and A58's clear-corner
  bridge is silent (no clear corner). What replaces it (PI + advisor framing, 2026-09-02): with
  four corner pins the free region is a CROSS — the centre block [1, m−1]² of side m − 2
  (1.82–1.877 on W) and four arms (m − 2) × 1. Every dimension is < 2 = s(2), so [T, one
  paragraph]: a square confined to an arm has height 1 available, hence is axis-aligned with
  cy = 1/2 (a tilt gives extent cos θ + sin θ > 1), and each arm holds ≤ 1; the centre holds
  ≤ 1 square of any orientation (two unit squares need side 2); so at most 5 of the 7 free
  squares lie entirely in one part and **≥ 2 are straddlers** (crossing from an arm into the
  centre, necessarily tilted or off-axis). Under the EXACT hypothesis an arm square cannot
  touch its corner pin flush (that puts it at the slot BL(1,0)/BR(1,0)/…, i.e. simple), so
  exact-corners4 arm squares FLOAT with gaps on both sides, and a slide-stuck minimiser needs
  every floating arm square slide-blocked — only a straddler's intrusion into the arm can do
  it (another arm square cannot: the arm is < 2 wide). So a selected exact-corners4 minimiser
  is a FINITE case list: (occupied arms) × (centre occupied?) × (straddler ↦ arm, with a contact
  blocking that arm's square) — A66's orientation coupling made explicit, and the reason
  point-count witnesses (A66's exact 7-point families) cannot see it: they ignore the forced
  θ = 0 and the forced contacts. ∀-packings form (no stuckness): an arm square at its slot puts
  the packing in a k = 5 superclass (corners4 + one arm cell: certified-killed classes, or
  k5_16 via A57 G1) — the K1 climb — so the tree needs only the floating positions, and
  blocking is replaced by the LP seeing the position box. **Route:** a tilt-box zone tree
  seeded by the cross partition (per free square: arm i / centre / straddler of arm i, with
  arm squares as degenerate cores θ = 0, cy = 1/2, cx in ≤ 1-wide cells so the core is
  non-empty) with A71's stuck rows SR-1/SR-2 as case splits; the per-node LP sees the
  orientation coupling that the root LP (η = +0.011) cannot. **Price:** occupancy patterns
  ≤ 2⁴ × 2, straddlers 2–3 each with 4 arms × 8 t-cells × O(4) position cells ≈ 10²
  cells, most pairs geometrically contradictory ⇒ ≈ 10³–10⁴ node LPs at budgets ≤ 5 with
  strong cores (fast, ~10²–10³ s) ≈ **2–10 desktop-days**, plus the written cross lemma;
  if the case list is as small as the framing suggests, a hand proof + per-case exact
  certificates beats the tree. Canary: none needed (no Trump image). This is the corners4 line
  of the tier; it stays [C] until the cross lemma is written and one case is certified.

  **Lemma CC4 (the 8-slot argument; PI + advisor, superseding the sliding seed; CC-2 is
  Lean-proved).** [T at s0; window via C.A57] Each arm of the cross carries the two
  corner-adjacent completable slots of corners4 (bottom arm: BL(1,0) = [1,2]×[0,1] and
  BR(1,0) = [m−2, m−1]×[0,1], overlapping in the middle strip [m−2, 2]×[0,1] since m − 2 < 2):
  8 slot boxes, one D4-orbit. corners4's only k = 5 superclass is **k5_16** = corners4 +
  BL(0,1) (`attempts/A55-k4-sweep/results/k4_lattice.json`: `sup_k5 = ['k5_16']`; all eight
  one-cell completions are D4-images of it), killed at s0 by A57's shadow tree (C.A57,
  `k5_16_interior_NO` + YES children; window form = A57 G1, in flight). Hence, for EVERY
  packing at side m containing corners4's pins (∀-packings, no stuckness — this is A58's CC-3
  mechanism with a killed superclass): if a slot box were met (open interiors) by no square or
  by exactly one non-pin square, teleport a non-pin square into the slot (CC-2 / CC-2′: the
  slot square is inside the container and interior-disjoint from the corner pin) — the result
  is a packing at the same side whose skeleton contains k5_16's pins, contradicting the kill.
  So **every one of the 8 slot boxes is met by ≥ 2 non-pin squares**, empty arms included, and
  this holds at s0 unconditionally.

  Intrusion geometry [M, exact, and a CORRECTION to the framing]: an arm square (axis-aligned,
  cy = 1/2) meets BOTH slot boxes of its arm (its x-range [cx − 1/2, cx + 1/2] with
  cx ∈ (3/2, m − 3/2) always meets [1, 2] and [m−2, m−1]), contributing one meeter to each;
  an axis-aligned non-arm square dipping below y = 1 must have x0 ≥ 1 (the pin) so it meets
  ≤ 2 slots, both of one arm; **a tilted square can meet THREE slot boxes while feasible** —
  exact witness: the unit square with vertices (0.95, 1.25), (1.91, 0.97), (2.19, 1.93),
  (1.23, 2.21) (edge (24/25, −7/25)) is inside [0, s0]², interior-disjoint from all four pins,
  and meets bottom-BL, bottom-BR (through the middle strip) and left-BL (checked in
  Fractions). So the incidence count alone does not close: with a arm squares the 7 free
  squares supply ≤ 2a + 3(7 − a) = 21 − a ≥ 16 = the requirement, whereas "≤ 2 per square"
  would have given 14 < 16 and emptiness outright. The claim "≥ 4 straddlers, one per block
  corner" therefore needs the middle-strip triple excluded by the case analysis (a triple
  intruder dips ≥ 0.03 into the middle strip AND ≥ 0.05 into the adjacent arm; whether two such
  squares plus the rest fit is exactly the per-case LP/Krawczyk question), not by counting.
  Corrected finite structure: exact-corners4 = 4 pins + a ≤ 4 floating arm squares (θ = 0,
  cy = 1/2, cx off both slots) + (7 − a) squares in the centre block or straddling, meeting
  the 8 slot boxes with multiplicity ≥ 2 each, ≤ 3 per square (≤ 2 if axis-aligned). Deliver:
  Lemma CC4 as written (cite k5_16's certificates by id), the intrusion lemma (≤ 3, with the
  middle-strip characterisation), the case list by (a, the slot-incidence pattern), and
  per-case exact certificates (tilt-box case-LPs with SR-1/SR-2 rows at the stuck endpoint,
  or the ∀-form without them) — or the precise surviving case. Price unchanged
  (≈ 10³–10⁴ small LPs, 2–10 desktop-days) with the case list now explicit.
* The A58 clear-corner seed is available ONLY under the teleport-stuck hypothesis (CC-2′ binds
  selected minimisers; CC-3's certificate route is K1-blocked at clear-corner roots) — it would
  turn the k ≤ 3 trees into stuck-only statements, which suffice for the bound through the
  selection chain (`unique_transfer.md` §2, A78 `unique_via_chain` at any side) but NOT for
  the ∀-packings `stratum_kill` form. As a YES–YES branch on the clear corner's root box it
  spends two budget units for free: for k3_05 (clear corner TR, box TR(0,0)) the corner_TR
  zone census has 171 attemptable boxes at budget 7 — the seed would start those at budget 5.
  Recommended only if the plain k ≤ 3 covers prove too expensive at §6.3's multiplier.

### 7.2 Composition (what closes `stratum_kill` for the tier)

For each of the 14 image-bearing classes: obligations O1–O5 of §5 with T′ = δ_basin(S) and
δ_pin = 2.5·10⁻² (BL(0,1)-pinned classes, whole window) / 2·10⁻² (the rest), landing at
r ≤ 6.5·10⁻⁴ for the BL(0,1)-pinned classes (one ladder level beyond A60's 24) so that
regime 1 is empty. For k4_05 and corners4: O6 (kill-only shadow trees) — open, and the only
part of the tier P-TREE does not price. Lean: per class one `stratum_kill` instance from the
tree's certificate corpus + `Zones.lean` rules + Lemma PD + the tube obligation.

## 8. Canary

The lemma asserts nothing that a Trump image falsifies: (a) is vacuous at m = ŝ; (b) SAYS the
M_S packings at ŝ are the images; the tree never certifies a node an image realises (engine
assertion, exit 9); every image must sit in a residue/chain box at every ladder level and end
in a (D) leaf (engine assertion). The tube certificates' own canary (ẑ − Tv violates a
compressed wall row; ẑ the unique equality point) is checked by `verify_tube.py` per file.

## 10. Findings ledger (A84's `notes/findings.md` is blocked by the harness, as for A80/A81/A83)

* [T] **Lemma P-TREE holds**: the protected tier's residual trees need no exact-stratum
  hypothesis on the lower bound; the exact reading enters only at m = ŝ and is optional
  (P = g·ẑ is the uniqueness conclusion). H10-stuck is a corollary; Theorem U is not consumed;
  A83 §4.3's Theorem-U cap (T′ ≈ 3·10⁻⁴) is void for this route.
* [T+M] **Lemma PD** (§2.1): with slack pin cores the residue floor is δ_pin (measured: k3_05
  stalls at 0.0219, residue → 3862); the drifted FULL pin square with the two-endpoint convexity
  test restores A59's contraction law (ratio 3.6–4.5; landing level 24, 59 boxes,
  1.1427·10⁻³ / 2.0102·10⁻³ rad = A60's numbers). A60's own δ_pin = 10⁻² re-emission needs it.
* [M] **Tube law** (§4): T_max is decided by square 3 = BL(0,1) alone — 0.0457 / 0.0574 with it
  pinned (trump5's wall), 0.1305 / 0.1680 without (the scale-ray wall); 19 directions, 42
  certificates. Whole window for the BL(0,1)-pinned classes only at r ≤ 6.5·10⁻⁴ (one ladder
  level beyond A60's); regime-1 plain kills can be dropped for the whole tier if every chain
  lands there.
* [M] **k4_05 and corners4 have no compatible Trump image** (G_S = ∅, exact): no (D) leaves,
  shadow-type trees, outside P-TREE's pricing (§3, §7).
* [M] The (D) geometry is class-independent per image: k4_08 and k3_05 land box-for-box with
  A60's square-1 ladder; the class enters only through the attemptable count and the LP budget.
* [F] Whole-window trees at A_S = 3/2 need δ_pin = 2.5·10⁻² (T_K), above A60's qualified 2·10⁻²
  (η = −0.81 PASS, LP ×8) — the one unmeasured slack point.
* [F] The A58 clear-corner seed is stuck-only (§7.1); usable for the bound through the selection
  chain, not for `stratum_kill`'s ∀-packings form.
* [F] Process: the pilot's LP steps sat at the 6 GB commit gate (free commit 1.0–1.5 GB while
  A78's Lean corpus builds, A57/A60/A61/A82 and an unrelated 12 GB process ran); the exact laws
  (census, ladder, contraction, landing) are complete, the LP laws are §6.3's.

## 9. Files

`attempts/A84-protected-trees/`: `code/tube84.py` (+ `tube84_all.sh`: the 17 remaining pin
sets), `code/tier84.py` → `results/tier84_classes.json` (G_S, I_g, A_S, T_K per class),
`results/tube84_*.json` + `tube84_sweep.jsonl` (every exact evaluation), `notes/pilot_design.md`
(the engine spec), `code/class84.py`, `alive84.py`, `tree84.py`, `launch84.ps1` (the engine),
`results/pilot_summary.json`, `notes/pilot_report.md`; `certs/tube_k4_08_*.json`,
`certs/tube_k3_05_*.json`, `certs/tube_I_*.json` (new files).


## 11. Lean status (A86, 2026-09-03)

Lemma P-TREE (a)+(b) is the Lean theorem `PackingCert.S11.tree_kill` (`ZoneTree.lean`) for an abstract `ClosedTree`
(leaves (K)/(N) = `checkCaseI` PASS at `s0` with node cores + NO-zones, (C), (D) = the SEAM landing, (D') = a folded atlas
box; `cover` = the complete disjunction — the producer's obligation, supported by the rule library `zone_dichotomy`,
`grid_cover` (CI-1), `slot_outside_zone` (CI-3), `pd_convex`/`pd_rule` (Lemma PD, §2.1), `d4_dil_comm` (the mod-G
commutation of Step 4)).  Step 1 is `root_of_containsPins`; §3's "exact hypothesis nowhere on the bound" is literal:
`classKilledAt_of_tree` (`Composition.lean`) normalises by `D4` into `ContainsPins` and reads the equality case as
`IsTrumpImage`.  The composition with TopLevel is `s_eleven_ge_of_classes` / `s_eleven_unique_of_classes`.
See `lean/lean_wave7_A86.md`.

## 12. Depgraph C.K4TIER note — A100's measurement (2026-09-05, chip → A100)

§7's tier price was a model. A100 (`attempts/A100-protected-pilot`) ran **k4_11** and **k3_02** end
to end on the A96 pipeline (this document's engine, copied; A96's emitter, resolver and frozen 4-D
verifier, unmodified) and measured every term. Four things change:

1. **|G_S| = 1 is real.** `class84` asserted two compatible Trump images. **k4_11 has exactly one**
   (sym 0), so the assert is widened to 1 ≤ |G_S| ≤ 2. Nothing else in the engine needs two: the
   alive gate, the canary and the (D) targets are per-image. Its (D) side is correspondingly half:
   28 leaves against k3_02's 59, both landing at level 24, `all_in_tube` true.
2. **The η law of §6.4 is exact, and it is an oracle.** Over **54 cover nodes on two classes,
   η < 0 ⇔ a certificate exists** (25/25 PASS at η < 0; 29/29 resist at η = 0, i.e. τ = budget
   exactly). §6's "η ≈ −0.8 certifies" reading came from three nodes; the sharp statement is that
   the LP decides killability before certification is attempted. Certification and the two ε_geo
   rounds on η = 0 cells are therefore pure loss — measured at 39.5 % of k4_11's cover leg and
   19.9 % of k3_02's, for 0 kills in 14 attempts.
3. **The parametric route reaches the (K) cover side and stops there.** The interior cover is the
   same (P-aff) 12-column grid A57 uses and the pins are slot coordinates, so `to_param96` accepts
   protected-class cover certificates verbatim (28/28 on A84's own corpus). The **resolver closed
   20/20** completed partials (43 exact window rows, 0 residual). But **ladder/residue nodes do not
   emit** — their centres are outside Q_dy — and neither do NO-family nodes. §5's per-class seam
   obligation is unchanged for those; it is discharged for the cover leaves by the window
   certificate instead.
4. **§7's cost model is optimistic by ~2×, and the reason is the resister branch.** Level-2 descent
   at δ_pin = 1e-2 killed **1 of 16 children**; τ stays at the budget on parent and both children
   and no sub-box is logic-killed. §7's "deepen rounds on the cover resisters" therefore has no
   measured closing mechanism; the only one that exists is the ladder, which terminates (24 levels,
   residue bounded 53–118 per level) but sheds 619 / 1 437 LP-bearing (K) boxes that §6.5 already
   measured not to kill at j = 0.

**Revised price.** Per class, the terms that close (level-1 emission at s0 + parametric verify over
W + resolver): **96.0 CPU-h (k4_11), 141.0 CPU-h (k3_02)**, plus one round of the non-closing
level-2 branch at +107.1 / +149.2 CPU-h. Tier, 15 classes excluding k0_00: **3 500–4 200 CPU-h**
central, band 2 900–6 300 on the level-2 child wall (the weakest coefficient, 16 children), against
§7's 1 800 CPU-h. Numbers and the sensitivity are in
`attempts/A100-protected-pilot/results/a100_projection.json`; every measured term is in
`results/a100_report.json`.

C.K4TIER stays open; the chip moves to A100. What would move the price is a theorem that removes
the η = 0 cells (they are the cells where the class LP has no budget slack at all), not more compute.
