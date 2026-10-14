# The U_k ladder: multi-square rigidity of ẑ as a COUNTING row on the exact strata — A80, 2026-09-02

Target (A80 BRIEF, PI idea): extend Theorem U (`theorem_u.md`: ten squares of ẑ force the
eleventh — 11 certificates, Σw = 0) upward to U_k (11 − k squares near their ẑ-slots force the
other k), and compose with the basin theorem into a counting exclusion on the exact protected
strata: "at most 10 − k squares within (r_c, r_t) of their Trump-slot poses" — a row for the
pair LP of `pair_kill.md`, one level above Lemma P-B (whose row is the k = 0 case: not all 11).
Labels: [T] proved, [S] routine given cited items, [M] measured/computed exact (interval) or
float LP (stated), [C] open. Code `attempts/A80-u-ladder/code/` (the A66 rig COPIED, the A65
emitter re-parametrised, the frozen `verify_case.py` byte-identical: sha256 521cb01f…bef7af).

**Headline (findings first).** (i) [T] The row is sound on the EXACT stratum only and its
soundness has exactly one new ingredient, Lemma U-C (a square within (r_c, r_t) of a slot
contains the slot's slack core once δ ≥ r_t + √2(r_c + ρ_B)); everything else is Lemma P-B's
proof with U_R in place of "all N in-zone". (ii) [T] In the pair LP the level-k row is the single
linear inequality Σ_{in-zone pairs} z ≤ C(6 − k, 2) per image, and by LP duality its multiplier
IS the discount γ of the certificate form (P2″) with rebate C(6 − k, 2)·γ — so the ladder is
measured by ONE constrained LP per rung with no γ sweep, and rung 0 reproduces P-B's optimum
over γ. (iii) [M] T1 — the reach of U_1: the pocket of a removed square at core slack δ is NOT
δ-sized: square 6 (the top tilted square, held by the top wall, the flush contact with 9 and the
point contact with 4) has a pocket of half-widths (5.6 δ, 5.8 δ) in (centre, t) — the hinge
amplification of `grain_discharge.md` §4 seen from inside — so the pocket lands in the basin
only for δ ≤ 5.6·10⁻⁴ (A40 radii) / 2.6·10⁻⁴ (Lean rBasin = 3/2000): **the reach collapses
below 10⁻³**, as the BRIEF's reserve clause anticipated. (iv) [M] T2 — the decisive number: see
§6 (filled from `attempts/A80-u-ladder/results/ladderlp_k4_08*.json`).

## 0 Setting and conventions

As `pair_kill.md` §6/§6.8: class S (k_S pins, N = 11 − k_S free squares; for k4_08 k_S = 4,
N = 7, m = 7 boxes, threshold C(7,2) + 7β = 28 at β = 1), certified side s″ (s0 for the pair
certificate), stuck packing z at side m̃ ∈ [ŝ − ρ_B, ŝ] with skeleton EXACTLY S, compatible
Trump images G_S (k4_08: {id, diag}, A71/A76; both pull back to the Trump-frame pin set
{0, 1, 3, 5}, free slots {2, 4, 6, 7, 8, 9, 10}). Configurations in (c, t)-coordinates, t =
tan(θ/2) (E.COORD); for the six upright slots "within r_t of t̂ = 0" means the equivalent tilt
mod π/2 (`theorem_u.md` §3: t ∈ [1 − h, 1] ⇔ |t′| ≤ h/(2 − h) + (h/(2−h))³). A **basin box**
B = (r_c^B, r_t^B): a theorem σ ≥ ŝ with equality iff ẑ on |c − ĉ|∞ ≤ r_c^B, |t − t̂|∞ ≤ r_t^B,
|s − ŝ| ≤ ρ_B — instantiated by the Lean `basin` axiom (3/2000, 3/2000), by A36 per coordinate
(37/10000, 37/20000) and by A40 per coordinate (5794/884563 ≈ 6.55·10⁻³, half of it in t), all
with the P-B(R) reading (side separately in the shell, no (1+√2) gate).

## 1 The U_R statements

For R ⊆ {0, …, 10} and radii r = (r_c, r_t) define the hypothesis on a packing z at side m̃:

  H_R(r): there is an injective assignment of squares of z to the slots j ∉ R with
          |c_q − ĉ_j|∞ ≤ r_c and |t_q − t̂_j| ≤ r_t (equivalent tilt) for the assigned square q.

**U_R(r; B)** := every packing z at side m̃ ∈ [ŝ − ρ_B, ŝ] with H_R(r) has ALL 33 coordinates in
the basin box B of ẑ, hence (basin equality clause, σ(z) ≤ m̃ ≤ ŝ) z = ẑ. Theorem U of A65 is
U_{{i}}(0; Lean basin) for each i. The ladder's level k is the family {U_R : |R| = k}; the
statement is D4 × S₁₁-covariant (apply g), and the two-images bookkeeping of P-B is inherited.

Two certificate forms deliver U_R, both `case-lp-certificate-v1` PASSes at s″ = 3877083591023/10¹²
(A65's realised side; λ = s″/m̃ ∈ (1, 1 + 2.6·10⁻¹⁰ + ρ_B/ŝ·(1 + …)]) with cores K_j (j ∉ R) =
the tight-certificate poses at half-side a = 1/2 − δ and zones F_i (i ∈ R) = (hw_c, hw_t)-boxes
around the tight poses:

* **C⁰_R** (Σw = 0, budget |R|): PASS ⇔ every admissible placement meeting no core lies in
  some F_i. Bridged (Lemma B-NO, `closed_disjoint_bridge.md` B.2″, applied |R| times — with
  Σw = 0 the pigeonhole prices ANY non-exempt non-owner, so all |R| non-owners are exempt):
  every non-owner square of Δ_λ z has (λc, t) in some F_i, and two disjoint unit squares cannot
  share a zone (zone diameter ≪ 1), so the non-owners occupy the |R| zones bijectively.
* **C¹_R** (0 < Σw < |R|, atoms in the merged pocket): PASS ⇒ at least one non-owner is exempt
  (if all |R| were priced, μ ≥ |R| > Σw). Weaker, needed exactly when the merged pocket of R
  has intermediate placements (a flush pair's 1 × 2 slab: a unit square slides from slot i to
  slot j meeting no core — C⁰ fails at those placements, one atom of weight 1 on the shared
  edge covers them all, Σw = 1 < 2).

**Lemma U-C (containment) [T].** Let q be a square of z with |c_q − ĉ_j|∞ ≤ r_c, |t_q − t̂_j| ≤ r_t
(equivalent tilt), z at side m̃ ≥ ŝ − ρ_B, λ = s″/m̃, and K_j the certificate core of slot j
(centre κ_j with |κ_j − (s″/ŝ)ĉ_j|∞ ≤ ε_κ, tilt t_r with |t_r − t̂_j| ≤ ε_t, half-side 1/2 − δ;
A65 ledger: ε_κ ≤ 2·10⁻¹⁴, ε_t ≤ 10⁻¹³). If

  δ ≥ (r_t + ε_t) + √2·(λ(r_c + ρ_B) + ε_κ)                                             (U-C)

then K_j lies in the open interior of Δ_λ q. *Proof.* In q's body frame the core's corners sit
at o + R(Δθ)·(1/2 − δ)(±1, ±1) with o = R(−θ_q)(λc_q − κ_j) and Δθ = θ_r − θ_q. |λc_q − κ_j|∞ ≤
λ r_c + |λ − s″/ŝ|·|ĉ_j|∞ + ε_κ ≤ λ(r_c + ρ_B) + ε_κ (|λ − s″/ŝ| = s″(ŝ − m̃)/(m̃ŝ) and
|ĉ_j| ≤ ŝ), so |o|∞ ≤ |o|₂ ≤ √2(λ(r_c + ρ_B) + ε_κ); |Δθ| ≤ 2(r_t + ε_t) (X.1 of
`theta_t_transfer.md`, both branches for uprights). A corner's body-frame ∞-norm is ≤
(1/2 − δ)(cos + sin)(Δθ) + |o|∞ ≤ (1/2 − δ)(1 + |Δθ|) + |o|∞ = 1/2 + (1/2)|Δθ| − δ(1 + |Δθ|) +
|o|∞ < 1/2 iff δ(1 + |Δθ|) > |Δθ|/2 + |o|∞, implied by (U-C). ∎

**Lemma U-R (from certificates to U_R) [T].** Fix r, ρ_B and a basin box B with r_c + √2ρ_B +
slop ≤ r_c^B, r_t ≤ r_t^B. (a) If C⁰_R PASSes at slack δ satisfying (U-C) for r, with zones
(hw_c, hw_t) whose pull-back satisfies hw_c + √2ρ_B + slop ≤ r_c^B and hw_t + hw_t³ ≤ r_t^B,
then U_R(r; B). (b) If C¹_R PASSes at slack δ satisfying (U-C) for r, with zones (hw_c, hw_t),
and U_{R∖{i}}(max(r, hw); B) holds for every i ∈ R, then U_R(r; B). *Proof.* (a) H_R(r) and
Lemma U-C give hypothesis (H) of Lemma B-NO for the |11 − R| cores with distinct owners; the
PASS + B-NO (Σw = 0 form) put every non-owner in a distinct zone; pulling back through λ the
zone deviations are ≤ hw_c + √2ρ_B + slop in centres (the P-B drift bookkeeping, dominant
term |ĉ|(ŝ − m̃)/ŝ ≤ √2 ρ_B... per coordinate ≤ ρ_B; the √2 is the conservative constant of
`pair_kill.md` §6) and ≤ hw_t (+ the cubic on the t ≈ 1 branch) in tilt; the assigned squares
deviate by ≤ r; so all 33 coordinates are in B. (b) As (a) up to "some non-owner q* is in some
F_i"; then the squares assigned to slots ∉ R together with q* at slot i satisfy
H_{R∖{i}}(max(r, hw)), and U_{R∖{i}} concludes. The case split over i ∈ R is finite. ∎

The peeling in (b) is where the ladder's reach is spent: each atom-bearing level costs a factor
≈ (√2 + 1)·(pocket amplification) in δ downward, because the zone of level k is the radius of
level k − 1. Since the row's LP value is insensitive to the zone radius (§6, and A76's
saturation law), the reach only has to stay above the B&B resolution — it does not have to be
large; what the ladder buys is the COUNT, not the radius.

## 2 [T] Lemma BR (bridging dichotomy — what the "connected-component shortcut" is)

For R and slack δ let free(R) be the set of admissible placements meeting no core K_j, j ∉ R.
Then free(R) ⊆ ⋃_{i∈R} free({i}) ∪ Bridge(R), where Bridge(R) = placements meeting no core
outside R and meeting ≥ 2 cores of R. *Proof.* A placement in free(R) meets at most the cores
of R; if it meets at most one of them, K_i say, it avoids all cores of {0..10}∖{i}. ∎
Consequently, given the level-1 PASSes (free({i}) ⊆ F_i, each Theorem-U certificate), C⁰_R
PASSes iff Bridge(R) ⊆ ⋃ F_i, and Bridge(R) is non-empty only when a unit square can touch two
cores of R at once while clearing the other nine (7 …): for a flush-contact pair it is the
whole sliding slab; for a point-contact or non-adjacent pair it is decided by the same B&B in
the same sub-second run. So the honest shortcut is not a lemma that saves certificates — every
C⁰_R is cheaper than the lemma it would replace — but the statement of WHICH R need atoms:
exactly those whose removed squares carry a flush contact of ẑ (edges (0,1), (0,3), (6,9),
(7,8), (7,9), (8,10), (9,10) of Trump's contact graph, `grain_discharge.md` §2); the seven
point contacts and the 41 non-adjacent pairs have Bridge(R) ⊆ ⋃F_i by the direct certificate
[M — the census for |R| = 2 is in `attempts/A80-u-ladder/results/`, §6, when T3 ran]. A
disconnected R = R₁ ⊔ R₂ (no contact between the parts) can still have a non-empty Bridge(R)
through Trump's sub-10⁻² gaps (7–4: 0.0126; strip gaps 0.0249), which is why the direct
certificate, not a separation lemma, is the sound route.

## 3 [T] Lemma U-ROW (the counting row, exact stratum only)

**Setting.** Lemma P-B(R)'s: certificate side s″ = s0, class S with pins, compatible images
G_S, zones Ẑ_{g,j} = (r_c, r_t)-boxes in (c, t) at s0 around the s0-dilated poses of the N
non-pin squares of g·ẑ, stuck packing z at m̃ ∈ [ŝ − ρ_B, ŝ] with skeleton EXACTLY S, and the
per-coordinate basin conditions r_c + √2ρ_B + slop ≤ r_c^B, r_t ≤ r_t^B, ρ_B ≤ ρ_B^B.

**Lemma U-ROW.** Suppose U_R(r; B) holds for every R ⊆ (free slots of g) with |R| = k (in
Trump's frame, after the pull-back by g), with r = (r_c + slop, r_t) (slop = the s0 ↔ s″
re-dilation drift ≤ (1 − s″/s0)·ŝ ≤ 4.1·10⁻⁷ and the 10⁻⁸ rounding of the LP's zone centres).
Then for every g ∈ G_S, at most N − 1 − k of the N free squares of Δ_λ z (λ = s0/m̃) lie in
zones of g. Equivalently, since the k_S pins are always in-zone (slot drift (λ − 1)·5/2 ≪ r_c,
B.0(c)): at most 10 − k of the 11 squares are within r of their g·ẑ poses.

*Proof.* Suppose N − k free squares of Δ_λ z lie in zones of g (distinct zones: two disjoint
unit squares cannot share one). Together with the k_S pins that is 11 − k squares; let R be the
k slots of g·ẑ not so occupied — R consists of free slots. Pull g back: the pulled-back
packing satisfies H_R(r) with r as stated (zone membership at s0 pulls back to |c − ĉ_j| ≤
r_c + ρ_B·|ĉ_j|/ŝ + rounding, |t − t̂_j| ≤ r_t; pins to |c − ĉ_j| ≤ (5/2)(ŝ − m̃)/m̃, tilt 0).
U_R(r; B) then gives z = g·ẑ. But g·ẑ has FIVE simple squares (a trump5 image), so its skeleton
is not exactly S (k_S ≤ 4) — contradicting the exact-stratum hypothesis. ∎

**Where the exact-stratum hypothesis enters (and the monotone trap).** Exactly once, in the
last sentence, and it is load-bearing: a MONOTONE hypothesis ("z contains the pins of S") is
satisfied by g·ẑ itself (compatibility of g), so the row would then assert something false of
Trump — the same trap as Lemma P-B's, one level up. Everything before that sentence is a
statement ABOUT Trump-near packings that Trump satisfies (he is the U_R conclusion, never
excluded). The row is a theorem of the InStratum-exact semantics (`instratum_bridge.md`) and
nothing else; it is not a valid row for the ∀-packings quantifier of `stratum_kill`, and it is
consumed only where H10-stuck's rows are (the teleport-stuck endpoint of the selection chain,
`unique_transfer.md` §2–3, side in the ρ_B-shell below ŝ).

**Certificate form and pricing [T].** For rung k and multipliers γ_g ≥ 0 the pair certificate
claims (P2‴) μ₂{Q, Q′} ≥ 1 + β m₂(Q, Q′) − Σ_g γ_g bz_g(Q, Q′) on every admissible interior-
disjoint core-free pair and (P1‴) W₂ < C(N, 2) + βm − Σ_g γ_g·C(N − 1 − k, 2). Kill: Lemma P's
chain with Σ_{a<b} bz_g ≤ C(N − 1 − k, 2) for every g by Lemma U-ROW. Sound for every choice of
γ_g ≥ 0 (a subset of G_S is allowed: fewer discounted pairs). In the restricted packing LP of
the A66 rig (max Σ z_ij(1 + βm₂) s.t. point loads ≤ 1) the rung is the HARD row
Σ_{ij: bz_g = 1} z_ij ≤ C(N − 1 − k, 2) per image — valid for every real family, hence for the
LP; by LP duality (one extra constraint with multiplier γ_g*) the constrained value V_k equals
min over γ of [Lagrangian value + γ·C(N−1−k, 2)], i.e. V_k < threshold ⇔ a restricted
certificate of the (P2‴)/(P1‴) form exists at γ = γ*. So margin_k := V_k/L_max − threshold is
the rung's restricted margin, rung 0 is Lemma P-B optimised over γ (A66 measured γ = 0.1 by
hand: −1.40), and the whole ladder is one LP per rung on a shared row store.

## 4 [S] Composition (what changes in the composed proof: nothing structural)

The row is an additional valid inequality on the death-witness side of Lemma P for the stuck
endpoint; its consumption path is Lemma P-B's verbatim (`pair_kill.md` §6, shell caveat
included: below the ρ_B-shell the pins' slot drift leaves the basin and the row is dropped).
Its own inputs are (i) the U_R certificates (case-LP PASSes at s″, `verify_case.py` frozen,
V.CASE lean-proved soundness) with the exact side-condition ledger (Lemma U-C margins, zone →
basin containment, the peeling slack chain), (ii) `basin` (equality clause only; A36/Lean or
A40 per coordinate — stated per ledger), (iii) InStratum-exact. No new axiom; Trump is never
excluded by any U_R (he is its unique solution) — the exclusion is the skeleton mismatch.

## 5 Canary

Every U_R certificate EXHIBITS ẑ: with all zones deleted (control form) the only holes are
Trump's own pockets, and the PASS says "the free space supports unit squares only there";
the composed conclusion is z = g·ẑ. The counting row asserts nothing that ẑ falsifies: ẑ has
11 squares in-zone and skeleton trump5, so it is outside the row's quantifier (exact k4_08).
The LP measurements are adversary-side. SAFE by construction; per-run ledger in
`attempts/A80-u-ladder/notes/findings.md`.

## 6 [M] Measurements (A80, 2026-09-02)

### 6.1 T1 — U_1 at fat slack: the reach collapses below 10⁻³ (the hinge pocket of square 6)

Per-square MINIMAL passing pocket zones (bisection to 2⁻⁷ of the start, frozen verifier at depth
60, every run sub-second; `attempts/A80-u-ladder/results/u1_zones_d*.json`, 829 verification runs
in `results/u1_runs.jsonl`). The half-widths scale LINEARLY in δ (identical ratios at δ = 10⁻⁴,
3·10⁻⁴, 10⁻³, 3·10⁻³, 10⁻²):

| square | hw_c/δ | hw_t/δ | what holds it |
|---|---|---|---|
| 0 | 1.09 | 0.62 | corner: two walls + 1 + 3 |
| 1, 3 | 2.8, 2.2 | 1.41 | wall + flush 0 + one point contact (8 / 7) |
| 2, 5 | 1.6 | 0.8–0.9 | corner uprights |
| 4 | 1.7–1.9 | 1.7–1.9 | wall + point contacts 6, 7 |
| 7, 9, 10 | 1.9–2.2 | 1.4–2.2 | strip flush pairs |
| 8 | 2.5 | 2.66 | strip + two point contacts |
| **6** | **5.6** | **5.8** | top wall + flush 9 + point contact 4 — the HINGE (`grain_discharge.md` §4) |

Reach = the largest δ whose zones land in the basin (binding: square 6's tilt): **Lean/A36 uniform
rBasin = 3/2000: δ ≤ 2.6·10⁻⁴; A36 per coordinate: 3.2·10⁻⁴; A40 per coordinate: 5.7·10⁻⁴.** At the
BRIEF's δ ∈ {10⁻³, 3·10⁻³, 10⁻²} all 11 certificates PASS (0.4–2.7 s each, 400–6 000 boxes) with
zones up to (5.5·10⁻³, 5.8·10⁻³) / (1.7·10⁻², 1.7·10⁻²) / (5.3·10⁻², 6.1·10⁻²), but square 6's pocket
is outside every basin, so the COMPOSITION does not close there. The premise "rigid to δ ~ 10⁻²
with pins" (A76 Lemma K) does not transfer to U_1: U_1 has no pins — its hypothesis is ten SLACK
cores, and a slack flush contact is exactly the hinge degradation A76 measured (ratio 5.8 here vs
10.7 at (10⁻³, 10⁻³) there — the same nearly-dependent triple top-wall / flush-9 / point-4).
Packaged, verified, gated: `certs/uladder/u1_d1_4000/` (δ = 1/4000, zones = the δ = 10⁻⁴ minima
× 1.03 δ/10⁻⁴; lands in all three basins, headroom 3.4 % in centres, 0.8 % in tilt) and
`certs/uladder/u1_d1_2000/` (δ = 1/2000, A40 only); `certs/verify_uladder.py` PASS on both, all five
corruption gates FAIL as required. Counting-row zone via Lemma U-C: r ≤ 1.04·10⁻⁴ (δ = 1/4000),
2.07·10⁻⁴ (δ = 1/2000) at ρ_B = 0 — irrelevant to the LP (saturation law), relevant to the B&B only.

### 6.2 T2 — the ladder in the pair LP: RESERVE-PLUS, ≈ +0.55 per rung, not a lever

k4_08, β = 1, threshold 28, A66 rig unchanged (catalog 293 placements: the 7 crowdfam zone centres
+ 48 perturbation columns at 0.3 r_z / 3 r_z + the A66 grid, 21 059 disjoint pairs, 285 ghost
pairs), r_z = 10⁻³, one image (A66's convention; `diag` is k4_08's own symmetry). Fresh row store
per rung (45M-nnz / 45k-row caps not hit); every cell CONVERGED (fine Lmax = 1.000000, 0 violators).
`attempts/A80-u-ladder/results/ladderlp_k4_08_rz1e-3_img1_k*.json`, `logs/`.

| rung k | cap C(6−k,2) | V_k | margin V_k − 28 | γ* | gain vs previous rung | LP time |
|---|---|---|---|---|---|---|
| plain pair LP (no row) | — | 27.000000 | −1.000 | — | — | 29 s |
| 0 = Lemma P-B optimised over γ | 15 | 26.588235 | −1.412 | 0.0882 | +0.41 | 148 s |
| **1 (BRIEF's decisive row: ≤ 9 within δ)** | 10 | **26.000000** | **−2.000** | 0.1250 | **+0.59** | 204 s |
| 2 | 6 | 25.435705 | −2.564 | 0.1610 | +0.56 | 5 min |
| 3 | 3 | 24.885193 (long re-run, lp_time 1800: converged) | −3.115 | 0.2398 | +0.55 | 451 s |
| 4 | 1 | 24.277778 | −3.722 | 0.4464 | +0.61 | 461 s |
| 5 | 0 | 23.705394 (long re-run: converged, fine Lmax 1.008, scaled 23.513) | −4.487 (scaled) | 1.0160 | +0.76 | 624 s |

Against the BRIEF's thresholds the k = 1 row gains **+0.59 over P-B's optimum (−1.41; A66's
hand-tuned γ = 0.1 was −1.40) and +1.00 over the plain pair LP** — above "~0.1 = reserve", below
"≥ 1 = lever": a reserve-plus. The ladder is LINEAR in k at ≈ −0.55 to −0.6 per rung (five converged rungs:
−1.41, −2.00, −2.56, −3.11, −3.72, and −4.49 at the last rung whose cap is 0 — the whole ladder to k = 5
buys ≈ 3.5 units of restricted slack over plain Lemma P), not the (k + 1)-unit jump hoped for. (Rungs 3
and 5 first hit the HiGHS 600 s time limit unconverged; the 1800 s re-runs converged.) Rung 1 re-measured at the ladder's real zone r_z = 10⁻⁴ (§6.1, variants at 3·10⁻⁵ / 3·10⁻⁴): **26.000000 again, converged, γ* = 1/8, same class masses (in-in 10.0, in-near 4.67, far-in 4.0)** — the zone radius is irrelevant to the price, exactly as A76's saturation law says.

**The dodge witness (A12's mechanism, quantified).** The rung-1 optimum is 26 = 21 + 5 EXACTLY on a
35-pair support (re-run with the support dump: identical value; `results/ladderlp_k4_08_rz1e-3_img1_k1_dodge.json`).
Pair-mass by class: in-zone/in-zone 10.000 (= the cap, tight), in-zone/near-variant 4.333,
in-zone/far 4.333, far/far 0.667 (Σ z = 19.333). Per placement (an integral 7-family gives every
member degree 6): five ghost members — the trump-sym4 image's squares at zones 0, 3, 4, 5, 6 — keep
degree 4.333 each; zone 2 keeps 3.667 and zone 1 3.333, and their missing degree is carried by the
3·10⁻³-displaced variants (cx = 1.5333 at degree 1.333, cy = 0.503 at 1.000, 2.6208/2.4335/1.5393 at
0.667) plus a few A66 grid placements (degrees 0.33–1.33). Six weight-1 pairs sit entirely inside
the zones; the weight-2/3 and 1/3 pairs mix zone members with the variants. So the row is paid by
thinning TWO ghost members by ≈ 1/3 onto variants that keep every box incidence — mean m₂ 0.345. The displaced variants keep every box incidence (A58's
meeter margins 1.6·10⁻² ≫ 3 r_z) and lose only the discount, so each unit of in-zone-pair budget the
row removes costs the adversary γ* ≈ 0.09–0.16, and the rungs (5, 4, 3, 2, 1 pairs removed) cost
≈ 0.6, 0.55, 0.5, … — the linear law. This is exactly the A12 signature: the row counts SQUARES in
zones, the fractional adversary pays in pair-mass parked just outside them, and (A76's saturation
law) the zone radius does not change the price. The row is sound and bites integrally (no
7-family with ≥ 6 in-zone members exists, by U_1); its fractional price is ≈ 0.55 per rung.
Full support of the dodge: `results/ladderlp_k4_08_rz1e-3_img1_k1_dodge.json` (`support`,
`support_class_mass`).

**A81 addendum (2026-09-02, `pair_kill.md` §6.10).** The table above is at UNIT class boxes
on a ONE-image catalog. In the certificate's own semantics (boxes widened by ε_box, both
compatible images as columns) the plain value is 28 = threshold (Corollary S-08: the image
family has Σm₂ = 7 against any widened box), and with both rung-1 rows the value is again
28.000000: the two image families at weight ½ each halve every per-image counting row (exact
42-pair witness). The widened two-image ladder is 28.000 / 27.667 / 26.962 / ≈ 26.06 / 25.045
at rungs 1–5 (gains 0, 0.33, 0.70, ≈ 0.9, ≈ 1.0 — accelerating once the cap is below the
mixture's reach), and the slack is cashable only at the zone scale (mixed-depth emission at
rung 5 recovers 27.000 = one unit). The row remains sound as stated here; its pricing value
in certificate semantics is rung 5's ≈ 3 sharp units, and rung 1's is zero.

### 6.3 T3 probe — what the climb would cost (census only; the climb was NOT run)

Lemma BR census at rung 2, δ = 10⁻⁴, zones = the per-square minima × 1.1
(`logs/uR_census_k2_d1e-4.log`, `results/uR_census_k2_*`): **41 of 55 pairs PASS in the Σw = 0 form**
(sub-second, 150–6 400 boxes) and **14 FAIL, and stay FAIL with zones ×2, ×4, ×8** — the merged
pockets: the 7 flush pairs (0,1), (0,3), (6,9), (7,8), (7,9), (8,10), (9,10); the 6 point contacts
(1,8), (2,8), (3,7), (4,6), (4,7), (5,9) (removing the point-contact neighbour frees a slide: 1 rises
into 8's vacated space, 4 drops 0.03 toward 3, …); and (3,4) (the two left uprights, gap 0.033, whose
removal opens a 1 × 2.03 channel). The corner–corner pair (1,3) PASSes — the pocket graph is
Trump's contact graph with (3,4) in place of (1,3). Atom form C¹: (0,1) PASSes with ONE atom of
weight 1 at the shared-edge midpoint once the zones are widened ×3 (Σw = 1 < 2; 3 032 boxes, 1.6 s);
(3,4) needs a measure, not a point (a 37°-tilted placement at (0.75, 2.51) sits in 4's freed corner
and misses the channel atom) — the A60-style covering LP (η ≤ −1 law) per merged pocket. Priced:
rung 2 = 41 direct + 14 emitted C¹ certificates + peeling to rung 1 at δ₁ ≥ √2 hw₂c + hw₂t (≈ 2.4×
the rung-2 zone, itself 2–6 δ₂), i.e. δ₂ ≈ 1.8·10⁻⁵ when square 6 ∈ R (B&B depth fine; the hinge
amplification compounds per level); rung 3 = 165 sets, ≈ 40 % with atoms. Cost = emission (hours),
gain ≈ 0.55 of restricted slack per rung. Not run: the lever threshold was not met.

### 6.4 Canary ledger

(1) U_1 sets at δ = 1/4000, 1/2000: the control form (zones deleted) FAILs with holes exactly at
Trump's pockets (`certs/u1_probe_d1e-3_control_00`: (0.500001, 0.500001), θ = 5·10⁻⁵°); the PASSes
assert only "the free space supports unit squares only in the pockets"; composed conclusion
z = g·ẑ. SAFE. (2) Lemma U-ROW reaches z = g·ẑ and contradicts only the exact-k4_08 skeleton
(§3). SAFE by theorem. (3) LP cells are adversary-side; the plain cell reproduces A66's 27.000000
(adequacy) and the crowdfam control (min gap 1.098·10⁻⁷, Σm₂ = 6). SAFE. (4) The rung-2 census
identifies Trump's merged pockets, excludes nothing. SAFE.

### 6.5 Discipline

One LP slot at a time (the first shared-store ladder run was killed by A80 when it hit the 25M-nnz
cap before rung 0 converged; rerun per rung with fresh stores at 45M/45k); BLAS pinned; the 6 GB
headroom gate held at every LP start (one dip at 12:06 waited out); B&B runs are ~50 MB processes.
A57/A60/A61/A77/A78/A79 untouched; frozen verifiers untouched (A66 rig copied, A65 verifier copied
byte-identical); certs/ new files only.
