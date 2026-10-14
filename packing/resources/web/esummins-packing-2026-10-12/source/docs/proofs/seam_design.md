# S1 seam design — hypothesis cells to configuration boxes (A41, Fable, 2026-08-28)

Design note, no campaign compute. Settles Q1 (pinning cascade), Q2 (handoff inventory), Q3
(composed cost formula) for seam S1 of the composed proof
(attempts/A38-root-power/notes/T0_composition.md). Every constant cites its source attempt.
Toy arithmetic: one python run (this note's tables), no solver processes. A29 untouched.

## 0. Objects and target scales

A surviving top-down cell is a hypothesis H = (witness cores B_1..B_k in (cx,cy,t)-boxes,
NO-families), k = 1..3 at A38 depths; level-1 half-width 0.0524, depth-d half-width
0.0524/2^(d-1) (A38). The bottom-up consumers need the full 33-coordinate configuration
(11 x (cx,cy,t)) boxed mod G = D4 x S11:

- K2 atlas discharge: box(z_e, h_e), atlas_final.json (A37, 36 entries). h_e certified:
  Trump e=0: h_T = 3079/819200 = 3.7585e-3; all other entries h_e >= 722261/81920000 =
  8.817e-3 (min, entry 3), up to 6.0e-2 (entry 31). Trump's box carries A36's equality clause.
- K3 FJ/Farkas: full cell, per-selection menus (A30 t3lib language).
- S6: Trump-consistent survivors must end inside the A36 box in ALL coordinates.

Cascade start scale: the A38 seam probe pinned second squares to r_occ = 0.06 neighbourhoods
of the attractor's other placements (A38 seam_trump.json geometry). Depth ledgers
(0.0524/2^(D-1) <= h and 0.06/2^d <= h):

| target h | witness closure D_w | per-square refine d_sq |
|---|---|---|
| h_T = 3.76e-3 (Trump, A37/A36) | 5 | 4 |
| h_e >= 8.82e-3 (non-Trump, A37) | 4 | 3 |
| h = 0.03 (A40 target radius) | 2 | 1 |

A40's h-growth enters ONLY here: every unit of log2 growth in basin radius removes one depth
from BOTH columns.

## 1. Q1 — the pinning cascade

### 1.1 Forcing inventory (what certified statements pin, given 1-2 pinned squares)

| statement | source | pins what | scale where it bites | per-use cost |
|---|---|---|---|---|
| Root occupancy A38.1: some centre in Z = [11/10, 694271/250000]^2, margin 0.9994 | A38 root_s0.json | square 1 into Z | root only | done (banked) |
| Conditional occupancy (K1 with k cores, budget 11-k, NO-zone = complement of candidate zones) | A24 (NO-side-zone kills), A38 probe A (tau = 9.20 vs 10, slack -0.80, UNconverged) | next square into a zone union | any; the workhorse | one case-LP + exact cert = T_D(s0), unmeasured (A38-G7; A39 P2a parameter) |
| Band lemmas: <=1 square avoids the width-w band, any w > (s0-2)/2 = 0.9385; >=7 centres within 1.34711 of a wall | A26.1 + A28.★ (docs/proofs/a28star.md); A26.2 | coarse wall-distance intervals, width ~0.94-1.35 | cascade start only; can never reach h_e | free |
| Tight-sum pair rows (A33.1(i), k=2): cov(x) <= 2 + eta - c_j given certified core coverage c_j | A33 lemma.md; A38 W2 | shrinks partner admissible set | POST-refinement only: at r = 0.06 partner boxes the robust bound collapses (c_2 down to 0.034, pair sums 0.91-1.6 vs thr 2.4254; W2 fired 0/16, A38 seam probe B) | inside the node LP (thr_node lowering); verifier duty S4 |
| Wastage atlas (>=3 mid-tilt cores at half-width <= 0.075: dead area 4.2070 > s'^2-11 = 4.0318 exact; cliff to 0 at 0.10) | A25 (MIN k = 3; threshold ledger point 1.74 / 0.075-box 1.49 / 0.15-box 0.32) | kills mid-tilt >=3-core hypotheses outright | mid-cascade window 0.075 -> below; mid-tilt geography only | 2.9 s/cell lookup (A25) |
| W1 field exemption (m_low > 1 + eta) | A33 T2 + A38 | prunes refinement children; pins nothing to intervals (surviving set = ONE component, 99.9% of surviving volume, A33 T2) | c_core > 1.4254 certified: onset witness-depth 5-7; resealed thr ~1.26-1.30: onset 3-5 (A38 c_core trend 0.658 -> 1.21) | inside node cost |

### 1.2 The cascade: zone-occupancy chain + S11 collapse (the design)

Given a surviving witness leaf (square 1 boxed at h <= r_occ, attractor identified by census):

1. ZONE CERTIFICATES (10 of them): for each remaining attractor placement p_j (mod D4), certify
   K1-kill of "H and no square centre in Z_j = ball_inf(p_j, r_occ)" — a budget-10 case-LP with
   Z_j as NO-zone, exactly A14/A24's proven mechanism (A24: root + NO-all-sides = 8.28 < 11).
   Each certificate forces >= 1 centre into Z_j.
2. S11 COLLAPSE (Lemma N1 below): witness core + 10 pairwise-disjoint zones, each certified to
   contain >= 1 of the 11 centres => each contains EXACTLY one; mod S11 the assignment is
   unique. NO assignment branching. This replaces the naive labeled cascade (b_occ^10 with
   measured b_2 = 16: 16^10 = 1.1e12 leaves, A38 probe B) by 10 ADDITIVE certificates.
   This is the single largest structural saving in the design (12 orders at measured b_2).
3. REFINEMENT: each zone refines from r_occ to its h_e target: d_sq depths of 8-way branching
   in that square's 3 coordinates, killed by W1 / tight-sum / wastage / plain tau; survivors
   at (8(1-f_c))^d.
4. HANDOFF: all 33 coordinates boxed at h_e -> K2 lookup (or K3 where V_e margin thin);
   Trump-consistent leaves must reach h_T and A36's box in all coords (S6), non-Trump h_e.

The theta coordinate rides along: zones are (c,t)-boxes; nothing else forces tilt (A26 ceiling:
10 squares with tilts <= 23.36 deg fit at 3.84 — tilt forcing is structurally weak).

### 1.3 Where it closes and where it stalls

CLOSES at h_e: 3.76e-3 (Trump) / >= 8.82e-3 (others). Unexplained-census cells have NO h_e
until BDBFS mints an attractor (A37 pipeline, 10-30 min/CP measured in A35; the loop is
load-bearing, A37: catalog provably incomplete).

STALL LEDGER (in cascade order):
- S1a — first certificate cost: probe A leaned right (tau 9.20 < 10) but NEVER CONVERGED at
  240 s (A38-G4). Every zone certificate pays T_D(s0), which A38 could not measure (0/60
  decisions; A38-G7). Inherited assassin; A39 P2a is exactly this measurement.
- S1b — the dead window: between r_occ = 0.06 and h_e, measured weapons are silent: W2
  collapses (c_2 = 0.034 at r = 0.06, A38), W1 certified threshold 1.4254 vs c_core median
  1.17-1.21 at half-width 0.0131 (A38 depth-3) — short by ~0.2; resealed threshold ~1.26-1.30
  (A39 P2b target eta <= 0.30) sits AT the measured c_core band: marginal, not established.
  Wastage bites only mid-tilt >=3-core at <= 0.075 (A25). If nothing fires, refinement is pure
  8^d_sq per square — see Q3 for what that costs. THE CASCADE'S FATE = W1's kill fraction f_c
  inside [0.06, h_e], unmeasured at any eta.
- S1c — chain-slack decay: stage-k budget is 11-k; probe A's slack was -0.80 at k = 1. Whether
  slack survives to k = 10 is unmeasured; a mid-chain tau_k -> budget stall would be the A14
  equality mode reappearing. Related: the five alive(LP) cells sit at tau = 10.000000 /
  maxcov = 1.000000 exactly (A38) — provably beyond the coverage LP at their scale (A27's
  refine-only class); their cascade must start from refinement, not occupancy.
- S1d — Trump's two extra depths: h_T = 3.76e-3 needs d_sq = 4 vs 3 (and D_w = 5 vs 4).
  A40 at h = 0.03 removes three of the four refinement depths AND three witness depths for
  the 3 Trump-consistent cells — A40 is worth more to S6 than to anything else.

## 2. Q2 — handoff inventory (A38 census_l1survivors.json: 172 survivors, tol 0.02 / 3 deg)

Per-cell primitive costs (sources): T_visit(s0) >= 500 s measured, T_D(s0) UNMEASURED (A38);
T_D(3.84) = 150-500 s anchor (A27); exact certification is a first-class node cost (A38 lab
rule; A39 measures); K2 lookup = exact-rational containment of 33 intervals against 36 atlas
boxes: < 1 ms, negligible (A37 atlas format); K3 = 1.9 ms/selection Farkas + 37 ms Gordan
direction LP + 30 ms verify (A30) — but menu size at half-width 0.01 is 4.03e8 unfactorized
(A30 P3) = 7.7e5 s/cell; with the A30-recommended per-pair factorization (Lemma N3) ~ sum of
per-pair menus ~ 60 selections = 0.2 s/cell. K3 is unusable without N3.

| class (count; status split) | finisher | per-cell cost (formula, then at measured constants) |
|---|---|---|
| trump_consistent (3; 1 undecided, 2 notrun) | cascade to h_T, then K2-Trump = A36 box + equality clause (S6) | witness 8^(D_w-1) x T_visit to depth 5, then per leaf: 10 T_D + 10 Sum_d (8(1-f_c))^d T_D, d_sq = 4. At f_c = 0: ~4.7e4 T_D per leaf — dead. At f_c = 7/8 (b_eff 1): ~50 T_D ~ 2.5e4 s per leaf. |
| atlas_consistent (34; 22 undecided, 2 alive(LP), 10 notrun) | cascade to h_e >= 8.8e-3, K2 lookup; K3 (factorized) as backstop where V_e - 3.877084 margin thin | same with D_w = 4, d_sq = 3: at b_eff 1, ~40 T_D per leaf + 0.2 s K3. |
| unexplained (135; 62 undecided, 3 alive(LP), 70 notrun) | refine until census resolves (level-1 "unexplained" mostly = boxes too big to pin, A38) -> reclass to atlas_consistent or W1-dead; residue -> BDBFS mint (A37 pipeline 10-30 min/CP) then K2 | reclass cost = the witness-tree share (already in F_w); mint cost = n_new x ~0.5 h, n_new unmeasured (A38: nothing rules new attractors out) |
| alive(LP) subset (5; tau/maxcov = 10.000000/1.000000 exactly) | coverage-LP-immune (1/4-ghost equality manifold, A38/A27): occupancy chain may still fire (different conditioning) — else refinement-only entry, then cascade; if their children re-pin at tau = budget, this is the true wall (needs Lemma N6) | unbounded by current weapons; the honest open corner |
| notrun corner triangle (82 of the 172 overlap this label) | same by census class; corner geography unmeasured at s0 (A38-G6) | adds risk, not a new mechanism |

## 3. Q3 — the composed end-to-end cost formula

Parameters (source; status):
N_1 = 172 level-1 survivors (A38; measured). F_w = witness-tree survivor multiplier to D_w =
Prod_{d=2}^{D_w} 8(1-f_d) (A38 measured f_2 = f_3 = 0 => 8^(D_w-1); A39 re-measures f with
certification-in-the-loop). D_w, d_sq from the ledger in section 0 (A37 h_e; A40 h-growth
moves both). b_eff = 8(1-f_c) in the refinement window (UNMEASURED; the S1b constant).
T_D = per-node decision-plus-certification cost at s0 (A39's (f, b, cost) triple; A38 anchor:
>= 500 s visits with 0 decisions; 3.84 anchor 150-500 s). Endgame terms: T_K2 < 1 ms (A37),
T_K3 ~ 0.2 s factorized (A30 + N3).

  C_total ~= N_1 * F_w(D_w) * T_D                                  [witness closure]
           + N_1 * F_w(D_w) * [ 10 + 10 * Sum_{d=1}^{d_sq} b_eff^d ] * T_D   [S1 cascade]
           + N_full * (T_K2 + T_K3)                                 [handoff, negligible]

The S11 collapse (N1) is what makes the middle term ADDITIVE in squares; without it the
cascade term carries b_2^10 = 16^10 = 1.1e12 (A38 measured b_2) and no lever reaches it.

Scenario table (this note's toy run; desktop-days at 6 workers = 5.184e5 CPU-s/day):

| scenario | nodes | desktop-days |
|---|---|---|
| measured today: D_w=5, d_sq=4, b_eff=8, T_D=500 s proxy | 3.3e10 | 3.2e7 (and T_D is really unbounded: 0 decisions measured) |
| L1 reseal in window only (b_eff=1), witness f still 0 | 3.6e7 | 3.5e4 |
| + witness onset -2 depths (A38's 64x, F_w -> 8^2-ish) | ~5.6e5 | ~540 at T_D 500 / ~160 at T_D 150 |
| A40 h=0.03 everywhere: D_w=2, d_sq=1, b_eff=1 | 2.9e4 | 28 (T_D 500) / 8.4 (T_D 150) |
| A40 but window unkilled (b_eff=8) | 1.25e5 | 121 |

DOMINANT TERM: N_1 * F_w * 10 * b_eff^{d_sq} * T_D — the refinement-window term. Every factor
is a named lever: F_w and b_eff are W1's onset (A33-G5 reseal, A39 P2b), T_D is the decision
rule (A38-L2, A39 P2a), D_w and d_sq are basin radius (A40). No single lever suffices;
the three together land 10-500 desktop-days; break-even demands geometric-mean per-square
multiplier <= ~1.5 (1.5^10 = 58), i.e. the cascade must run in PINNING mode — near-zero
branching — which the S11 collapse provides at the assignment layer and only W1-in-the-window
can provide at the refinement layer.

## 4. NEW lemmas the cascade needs (difficulty: LOW = days, MED = 1-2 weeks, HARD = open)

- N1 (zone-assignment collapse; LOW, high leverage). Witness core + 10 pairwise-disjoint
  zones each certified (K1, NO-zone form) to contain >= 1 of the 11 centres => exactly one
  each, and mod S11 the assignment is unique. Pure pigeonhole on disjoint regions; the K1
  soundness side is T0 verbatim. Needs exact-rational zone disjointness checks.
- N2 (containment/matching; LOW). Cascade boxes at h <= h_e => configuration lies in
  box(z_e, h_e) mod G, with the core-to-atlas-placement matching provably unique because
  atlas placement separations (Trump equal gaps 0.02487, A03) exceed 2(h_e + box radius).
  Exact-rational; extends verify_tree2's D4 bridge (A27) to G = D4 x S11. This is S6's
  containment obligation made precise.
- N3 (menu factorization for K3; MED). A30's recommendation, never proved: per-pair covering
  row sets K_p such that per-pair union-Farkas certificates compose to a full-menu exclusion —
  turns Prod|K_p| (4e8 at h = 0.01, A30 P3) into Sum|K_p| (~60). Blocked-case caveat from A30:
  flush ties make the two dominance rows exact negatives — the factorized form must branch
  those pairs (A36 L1 branch machinery is the template).
- N4 (asymmetric tight-sum kill; LOW-MED). W2 with c_j certified inward on a SMALL pinned
  core applied against every placement row and against whole boxes of an UNREFINED partner;
  the statement is Cor A33.2 + A33.1(i) (done) — the new content is the a-posteriori verifier
  recomputing c_j independently (S4) and the lambda bookkeeping (S2). Mostly verifier work.
- N5 (chain-slack persistence; measurement, not lemma). tau_k < 11-k with usable slack for
  k = 2..10. Probe A gives k=1 slack -0.80 unconverged (A38-G4). Attempting this as a theorem
  is HARD and pointless; it is A39-adjacent measurement. If slack dies mid-chain, S1 falls.
- N6 (equality-manifold discharge; HARD, open). The five tau = maxcov = 10.000000/1.000000
  cells (A38): prove the 1/4-ghost fractional-packing manifold's cells land in atlas basins,
  or supply a non-coverage weapon at their scale. A16 measured theta' kills exactly this node
  type on grids (9.44 vs budget 10) but the continuum certificate died (A17-A20 collapse
  theorem). This is the residual mathematical wall of the whole program.
- N7 (NO-family inheritance; LOW). NO-families and W1/W2 exemption bookkeeping certified at a
  parent remain sound under re-anchoring through cascade stages — mechanical extension of
  verify_tree2 semantics (S2 family).

## 5. Honesty ledger

Grounded-but-unmeasured: b_eff in the window (S1b), T_D(s0) (A38-G7), chain slack at k >= 2
(N5), n_new attractors (A38 census scope), corner geography (A38-G6). The scenario table's
lever rows assume A39/A40 land their targets; nothing here asserts they will. The S11
collapse and the additive cascade form are design theorems (N1/N2) — LOW difficulty but NOT
yet proved; until they are, the only priced cascade is the 1.1e12-leaf labeled one. All etas
used are eta_cert = 0.4254 (A33 sealed); resealed numbers are labelled as targets (A39 P2b).
