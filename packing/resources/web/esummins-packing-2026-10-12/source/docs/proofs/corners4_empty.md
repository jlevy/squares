# corners4 (k4_13) emptiness — T1 verdict: the direct counting route is REFUTED (A66, 2026-09-02)

Target (A66 BRIEF T1, successor to A65 residue item 2): prove that **corners4 is EMPTY at every
side s ∈ [3.82, s0]** — no packing of 11 unit squares in [0, s]² contains axis-aligned unit
squares at all four corner slots (the pins P_c = [0,1]², [s−1,s]×[0,1], [0,1]×[s−1,s],
[s−1,s]²) — by the candidate counting argument: the four pins partition the remainder, the
channels between adjacent pins have width s − 2 ≤ s0 − 2 = 1.877084 < 2 = s(2), and the 7 free
squares should not find the occupancy the geometry admits.

**Verdict: the counting route CANNOT close, anywhere in the window.** The natural occupancy
relaxation (centres, unit separation, pin clearance) is FEASIBLE for 7 squares at every
s ∈ [3.82, s0], with exact rational witnesses (§4). corners4 emptiness — very likely TRUE
(A65 search: no pins+7 family found at s0, best min-gap −2.5e-2 to −3.2e-2; feasible only from
side ≈ 4.000) — is an orientation-coupled (pairwise) fact invisible to every single-square
counting or pricing scheme, the same wall `h10_stuck.md` §8 measured fractionally
(τ(0) = 7.2545 > 7 on corners4). C.K4TIER is NOT reduced; the class is not deleted.
Labels: [T] proved, [M] measured/computed exact, [F] float evidence.

## 1 [T] Lemma E1 (the centre relaxation)

Let P be a packing at side s containing the four corner pins, and let Q_1 … Q_7 be its free
squares, c_i their centres. Then the seven points c_i satisfy

  (i) ‖c_i − c_j‖₂ ≥ 1 (i ≠ j);  (ii) dist(c_i, P_c) ≥ 1/2 for each pin square P_c;
  (iii) c_i ∈ [1/2, s−1/2]².

*Proof.* (i) Two closed unit squares with disjoint interiors admit a separating direction u
(SAT for convex polygons): the projections are intervals of half-length ≥ 1/2 with disjoint
interiors, so |（c_j − c_i)·u| ≥ 1, hence ‖c_j − c_i‖ ≥ 1. (ii) The open disk B(c_i, 1/2) lies
in the open square Q_i°, which is disjoint from P_c°; if dist(c_i, P_c) < 1/2 some boundary
point p ∈ P_c has |c_i − p| < 1/2, and points of P_c° near p lie in B(c_i, 1/2)° —
contradiction. (iii) Per axis the centre is at least half the projection width W(θ)/2 ≥ 1/2
from each wall. ∎

## 2 [T] Lemma E2 (the shape of the centre region)

Let C(s) = {c ∈ [1/2, s−1/2]² : dist(c, P_c) ≥ 1/2 for all four pins}. Then

  C(s) = MR ∪ MC ∪ S_BL ∪ S_BR ∪ S_TL ∪ S_TR,

where MC = [3/2, s−3/2] × [1/2, s−1/2] and MR = its transpose are two full-length bands of
width s − 3 ≤ 0.877084, and each sliver S (at inner pin corner κ, e.g. κ = (1,1) for BL) is
the curved triangle {c ∈ [1, 3/2]² : ‖c − κ‖ ≥ 1/2} (diameter √2/2 < 1, so a sliver holds at
most one centre). *Proof.* ⊇ is a direct check. ⊆: if c avoids both bands then (wlog BL)
c_x, c_y < 3/2; c_x ≤ 1 forces dist(c, P_BL) = max(c_y − 1, 0) < 1/2, impossible, so
c_x, c_y ∈ (1, 3/2) and the distance condition is ‖c − (1,1)‖ ≥ 1/2: the sliver. ∎

So the candidate argument's true content at centre level: two centres in the same band at
lateral offset ≤ s−3 differ by ≥ √(1−(s−3)²) ≥ 0.4803 along the band (this is the exact
form of "channel width < s(2)"), slivers hold ≤ 1, the central square Z = MC ∩ MR (side
s−3 < (√6−√2)⁻¹·1 …) holds ≤ 2. None of this caps the count at 6 — see §4.

## 3 [T] Lemma E3 (window embedding)

For 3 ≤ s ≤ s′: C(s) + ((s′−s)/2)·(1,1) ⊆ C(s′). *Proof.* Bands: [3/2 + d, s − 3/2 + d] ⊆
[3/2, s′−3/2] for d = (s′−s)/2, per axis. Slivers: a translated sliver point c has both
coordinates ≥ 1 + d, and c − (1,1) = (c − (1+d, 1+d)) + (d, d) is a sum of two vectors in the
positive quadrant, so ‖c − (1,1)‖ ≥ ‖c − (1+d,1+d)‖ ≥ 1/2; the other pins and walls are
farther. ∎ Hence a 7-point witness at s = 191/50 is a witness at every s ∈ [3.82, s0].

## 4 [M] The refutation witnesses (exact rationals)

**At s = 191/50 = 3.82** the seven points (denominator 1000)

  (1991, 500), (1390, 1337), (2423, 1436), (3313, 2296), (1218, 2353), (2301, 2561),
  (1575, 3320) /1000

satisfy Lemma E1's constraints with margin: min pairwise ‖·‖² = 1.06177, min squared pin
distance 0.265613 > 1/4, all inside [1/2, s−1/2]² (exact `fractions` check, A66 log; the
point (1.390, 1.337) is an S_BL sliver point). By Lemma E3 the relaxation is feasible at
**every** s ∈ [3.82, s0]: the counting argument admits the very configuration it was meant to
exclude, at every side in the window.

**At s = s0** a structured witness shows exactly where the channel admits the occupancy
(BRIEF's question): with mid = s0/2,

  A = (s0−3/2, 1/2), B = (s0−3/2, mid), C = (s0−3/2, s0−1/2)  — three centres in ONE
  channel column (spacing (s0−1)/2 = 1.438542 ≥ 1: the channel is not "2 abreast" but it is
  3-along, and length-wise occupancy was never bounded);
  D = (1/2, mid), E = (s0−1/2, mid)  — the two side-wall midpoints;
  F = (3/2, 1), G = (3/2, s0−1)  — two centres hugging the left pins' inner edges.

All 21 pairwise distances ≥ 1 and all clearances hold exactly (tight pairs: ‖B−E‖ = 1,
‖A−F‖² = 63704771441/62500000000 = 1.019276…). The "2 squares abreast forbidden" fact bounds
only squares CONTAINED in a channel; free squares straddle the channel/centre boundaries and
the pin corners (the sliver positions), and the count the geometry admits at centre level is
≥ 7, not ≤ 6.

## 5 [T/F] Why the truth is pairwise: the rigidity exhibit

The s0 witness does not lift to squares, for a reason no occupancy measure can see:

* **Wall rigidity [T].** c_y = 1/2 forces W(θ) = cosθ + sinθ ≤ 1, i.e. θ ∈ {0, π/2}: A and C
  (and D, E in x) are axis-aligned.
* **Pin-edge rigidity [T].** A unit square centred at (3/2, 1) with interior disjoint from
  [0,1]² is axis-aligned. (SAT over the four candidate axes: e_x needs W ≤ 1; e_y needs
  c_y ≥ 1 + W/2 ≥ 3/2; the square's own normals reduce to (1/2)cosθ ≥ 1/2 resp.
  −(3/2)sinθ ≥ 0 — all force θ = 0.) So F, G are axis-aligned.
* **Axis pair separation [T].** Two axis-aligned interior-disjoint unit squares need
  ‖Δc‖_∞ ≥ 1; but ‖A − F‖_∞ = max(s0 − 3, 1/2) = 0.877084 < 1. **Contradiction** — the
  witness dies at the orientation layer, exactly where every single-square scheme is blind.

Perturbed variants trade wall/pin margins for tilt quadratically and die within ~3e-2 (A65
blind search min-gap −2.5e-2 … −3.2e-2 [F]); classifying all perturbations is a genuine
case analysis over the (few-parameter) near-feasible family — the conditioned mini-tree of
§6(b), not a counting argument.

## 6 Verdict and priced residue

**T1: NO-GO for the direct integral counting proof** — refuted by §4 at every window side.
Combined with the fractional wall (A65: every measure/case-LP certificate needs Σw < 7 while
τ(0) = 7.2545, K1-coherent), corners4 emptiness is beyond ALL single-square machinery,
integral counting included. It remains open, with three constructive routes, in leverage order:

* (a) **Pair certificate at β = 0** (A66 T2 object, `docs/specs/pair_certificate_v1.md`): an
  emptiness certificate for corners4 needs NO stuckness — W₂ < C(7,2) = 21 with pair rows
  μ₂ ≥ 1 on all interior-disjoint core-free pairs kills every pins+7 family outright, and the
  pair LP is not subject to the τ(0) wall. **Measured in the A66 pilot [F]: OPEN.** On an
  adversary-adequate catalog (its single-square fractional packing reaches τ_f = 7.084 after
  13 column-generation rounds, vs A65's 7.2545), the restricted β = 0 pair value brackets
  τ₂(0) ∈ [14.82, 21.32] — the lower end a certified product dual witness (Lmax = 1.000000),
  the upper end the last optimal of an UNCONVERGED cutting-plane run (simplex time on a
  16.8k × 10.5k LP is the binder, not row/nnz caps) with a monotone trend 22.20 → 21.53 →
  21.32 toward 21 and not yet across it. The route is neither refuted nor confirmed; the
  successor needs a first-order/interior-point LP solver, then an emission oracle loop against
  `verify_pair.py`. A first "15" on a coarse catalog was a catalog artifact (that catalog's
  τ_f was 6.0) — the adequacy criterion (reproduce τ_f) is mandatory for every pair-LP
  verdict. (`attempts/A66-corners4-pair/results/pairlp_k4_13_conv.json`, `singlelp_k4_13*.json`.)
* (b) **Conditioned mini-tree**: branch on the cells of the near-feasible centre family of §5
  (wall/pin-forced squares are near-axis; the free interior square carries the tilt), each
  branch a case-LP with crowd-cell cores. Estimated branches: tens, not thousands (the
  feasible centre family is low-dimensional) — cheaper than an A60 zone tree, above A66's
  2-slot budget.
* (c) The contact/FJ cascade (A58-G2/A50-G1), which subsumes it.

Depgraph: C.K4TIER note updated (corners4 counting route refuted; class NOT deleted); no
label change.

## 7 Canary

Trump's configuration has TL clear — its skeleton is trump5, not corners4; nothing here
constrains it. The witnesses of §4 are point sets (no square-packing claim is made for them:
§5 proves the s0 witness does NOT lift), and the only statements about packings are
Lemmas E1–E3, which Trump's packing satisfies vacuously (it has no corners4 pin set). Safe at
every step.
