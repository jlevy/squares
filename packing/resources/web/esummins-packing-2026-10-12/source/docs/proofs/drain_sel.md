# DRAIN-SEL(W) — the restricted target, the menu of coupled moves with exact neighbourhood certificates, and the bounded experiment on the actual residue sample — A128, 2026-09-07

Target (A128 BRIEF, from the external review of the k0_00 residue): make the selected-minimiser restriction central,
target only the side range W and the precisely selected minimiser the existing composition accepts, keep uniqueness
separate, and test whether a small menu of COUPLED moves (cluster screws, exchanges, wall couplings, the supply count)
certifies progress on a representative sample of the actual residue — success meaning EXACT inequalities on
NEIGHBOURHOODS, never a numerical trajectory. Labels: [T] proved, [S] routine given cited items, [M] measured
(`attempts/A128-coupled-moves/{code,results,logs}`), [F] finding, [C] open. Conventions: `nocrit_k0_blocked.md` (A90:
corner frame, μ_c, d_c, Lemma K, CLUSTER, NOCRIT-SEL, Fact A), `frame_census.md` §8.2 (W-GEN, Ψ^(w)), `noroom.md`
(A103: ROT-GRAD, ROT, RES-LOCK, §6 reduction, §8 composition), `lockfree.md` (A105: ROT-W, LOCKED, LINE, PUSH-LINE,
the hook family), `exchange_lemma.md` (A98: Lemma TWO, EXPOSE), `k0_route.md` §3 (K0-FREE, K0-O1),
`attempts/A104-grid-lock/notes/lock104.md` (m_lock, the anatomy of a lock), `attempts/A118-lane-count/notes/method.md`
(the box-level teleport leaf). ŝ = 3.877083590022814, s0 = 969271/250000, W = [3.82, ŝ].

## 0. Verdict

> **T3 first.** The menu was decided EXACTLY, by interval arithmetic on boxes of radius 10⁻³ (and, failing that,
> 3·10⁻⁴ … 10⁻⁶) in every pose coordinate and in the side, on every intruder and every tangent square of every corner
> of the sample — the A107 near-packings of the converged-alive k0 cells (K01 ⊃ l1_071, l2_p65_101; K04 ⊃ l1_104; K06 ⊃
> l1_159; K03 ⊃ l2_p65_111; K05 ⊃ l2_p74_001; K20 ⊃ l2_p114_001; K26 ⊃ s3_far; the fractional cells l1_124, l1_148,
> l1_158 through near-packings built from their A115 supports; l1_153 = Trump), K01–K06, the two fully-held
> boundary packings of A104 (4.000237, 4.001525), Trump as the canary, and the two sub-4 corpus records as extra rows.
> **Result (Table, §3.3): 35 exact certificates on the sample, every one re-sampled 10⁴ → 10⁴ → 0 hits; Trump held
> under every move on every box (canary PASS). On the 10⁻³ box the menu kills 10 of the 15 non-Trump rows, i.e. the
> near-packings of 8 of the 11 non-Trump converged-alive cells — but the coupled moves are not what does it: the
> cluster screw certifies NOTHING at any radius ≥ 10⁻⁵ that the single square does not; the only coupled move that
> works where every single-square move fails is the EXCHANGE, at 4 corners on the 10⁻³ box (the A104 lock 4.000237's BL
> crowd straightened into two cells with margin 3.9·10⁻³; K01 TL; K26 TL; the 3.9907 record's BR) and 5 more on
> 10⁻⁵…10⁻⁴ boxes. Held under the WHOLE menu on every box of radius ≥ 10⁻⁴: the Gordan-certified lock 4.001525 (its BR
> exchange works on a 10⁻⁵ box only), the near-packings of l2_p65_111 (K03), l1_159 (K06) and l1_124 (a K02-type
> packing at 3.9428), and Trump — the residue, drawn in `attempts/A128-coupled-moves/results/residue128.svg`. Below 4,
> the failure is always the same: the best re-fit is FLUSH against an untouched square (margin ≈ 0), the flush
> population of A98/A101/A121 seen from the box side. The bounded experiment's answer to the reviewer is therefore:
> yes for exchanges (∀-packings, on neighbourhoods), no for cluster screws, and the drawn residue names the coupled
> move that is missing — a NON-rigid two-parameter field (column straightening + row slide) at the 4.001525-type frame,
> or a depth-2 exchange with margin at the flush corners.
>
> **T1.** Theorem DRAIN-SEL(W) is stated in §1 exactly against `noroom.md` §6/§8 and `Composition.lean`: for every
> m ∈ W the Ψ^(w)-minimal packing at side m (the selected minimiser) has, at some corner, a member of the MENU that is
> admissible — hence it is not Ψ^(w)-minimal or (exchange) a k ≥ 1 packing at side m exists — hence M(m) = ∅ for m < ŝ
> by K0-O1 and every packing at ŝ is an image, with uniqueness untouched (Trump's basin, Theorem U; the exchange branch
> at ŝ needs the two-square form of Theorem U, [C], or the ROT/CLUSTER branch). It is weaker than LOCK-FREE⁺(< 4) in
> three ways (one packing per side instead of all K0-BLOCKED packings; W instead of (·, 4); a menu instead of one
> square) and that is exactly what the composition consumes.
>
> **T2.** Every move is a NEIGHBOURHOOD statement, [T]: Lemma BOX-MOVE (§2.0) — a rigid screw of a cluster C ∋ Q is
> certified on a box B iff every pair axis that can separate a member from an outsider somewhere on B has separation
> derivative > 0 on B, every possibly active wall row of a member has derivative > 0, Q's μ_c has right-derivative > 0
> over every candidate argmin point of B, and every other (member, corner) depth that can be positive on B is
> nonincreasing; then EVERY packing in B at which Q intrudes c has a packing z′_ε at the same side with smaller Ψ^(w) for
> every positive weight vector — B contains no selected minimiser at which Q intrudes c. Its dual is Lemma BOX-GORDAN
> (Motzkin form with interval rows), which at radius 0 is exactly Lemma ROT's Gordan certificate. (a) CLUSTER-ROT is
> BOX-MOVE for a cluster (NOCRIT-SEL's translation clusters are the ω = 0, e-cardinal case; Lemma ROT the C = {Q}
> case). (b) EXCHANGE-BOX is Lemma EXPOSE on a box: two possible meeters, the slot square placed, a re-fit Q₀ fixed in
> the corner frame and certified disjoint from the nine untouched squares over B — a ∀-packings statement, no
> selection. (c) TWO-WALL: the hook identities and one-wall bounds of A105 evaluated on the box, plus the trivial extent
> bound; [F] on a box around a packing above ŝ it is satisfied trivially and certifies nothing a ruler would not — its
> content is structural, and the structural one-wall version is false (A105). (d) SUPPLY: [T] a pushed intruder needs
> ≥ 3 rows or an exact concurrency (LINE); [F] the four-corner count is vacuous (planarity gives ≤ 54 square rows against
> 24 needed), as A103 §4 found in another guise; on the sample the held intruders carry 3–7 square rows.
>
> **T4.** Not composed: the residue after the menu, RES-MENU(m) (§4.2) — LOCKED intruders, every enumerated cluster
> screw held on the box, every re-fit flush — is strictly smaller than RES-LOCK (the 4.000237 frame leaves it by
> exchange) and is realised at radius 10⁻⁴ by the 4.001525 frame and, below 4, by the flush corners of K03/K06/K02-type
> packings. Cases (R), (Cl), (E) of the case analysis are theorems now; case 4 is the one new obligation, A128-G1. The
> k0 row of `budget.md` (13,500 CPU-h tree / 0 theorem) is unchanged: the menu as box leaves fires on the residue's
> nearest relatives at radius 10⁻³ (10 of 15 boxes, 3 of them by non-trivial exchanges) but the tree's cells are two
> orders of magnitude wider than that — the K0-ROT/TF-U/EX verdict again.

## 1. T1 — the restricted target, exactly

### 1.1 Setting (as in `noroom.md` §1)

Packings z: eleven closed unit squares Q_i = Q(c_i, θ_i) with pairwise disjoint interiors in [0, m]²; M(m) the
compact set of packings at side m (33 pose coordinates). Corner frame of c, μ_c(Q) = min_{p∈Q} max(p_x, p_y), depth
d_c(Q) = max(0, 1 − μ_c(Q)); intruder: d_c > 0; tangent square: μ_c = 1; K0-BLOCKED: ≥ 2 intruders at every corner;
K0-FREE otherwise. Ψ^(w)(z) = Σ_c w_c Σ_i d_c(Q_i) with W-GEN weights (positive, ℚ-independent). **Selected
minimiser** z*(m): a Ψ^(w)-minimal element of M(m) (Lemma SEL-Ψ; for m = ŝ, of the non-image packings at ŝ, compact by
E.A36). Theorems NOCRIT-SEL, ROT, ROT-W hold at z*(m) for every m (their proofs use only that a small feasible motion
stays in M(m)).

### 1.2 The menu and the target

**MENU(z, Q, c)** for an intruder (or tangent square) Q of corner c at a packing z:
 (R) ROT — a screw of Q alone (Lemma ROT's strict system);
 (Cl) CLUSTER-ROT — a rigid screw of a set C ∋ Q of squares (§2.1);
 (E) EXCHANGE — c has exactly two intruders A, Q and a re-fit Q₀ exists (Lemma EXPOSE, §2.2);
 (TW) TWO-WALL — the chain/hook inequality at c is violated by the side (§2.3);
 (S) SUPPLY — the row count at Q cannot hold it (§2.4).
A member of the MENU is **admissible at z** if its exact condition holds at z: for (R)/(Cl) a strict Ψ^(w)-decreasing
feasible direction exists (equivalently, Lemma BOX-MOVE's certificate on some box containing z); for (E) the exchange
is a packing at the same side; (TW)/(S) are exclusion inequalities (they show z is not a packing of the assumed
structure).

**Theorem DRAIN-SEL(W) [statement; status in §4].** For every m ∈ W with M(m) ≠ ∅ (for m = ŝ: with a non-image
packing at ŝ), the selected minimiser z*(m) is K0-FREE, or has an intruder Q at a corner c with a member of
MENU(z*, Q, c) admissible.

**Consequences (composition, [T] given the theorem).** (R)/(Cl) admissible contradicts Ψ^(w)-minimality (Lemmas ROT,
CLUSTER-ROT), so at z*(m) only K0-FREE or (E) can occur; (TW)/(S) are consumed as exclusions inside the proof of the
theorem, not at the composition. Then:
 * m ∈ [3.82, ŝ): K0-FREE gives, by Lemma K0-FREE (teleport), a packing at side m containing a corner slot square;
   (E) gives one directly (Lemma FLOOD-D / EXPOSE). Both contradict K0-O1 (k1-a). Hence **M(m) = ∅**: the k0_00
   piece of `stratum_kill` in the PLAIN form `classKilledAt_of_kill`, i.e. `ClassKilledAt k0_00 m` — and since the
   statement is "no packing at side m at all", it is class-blind (every class at once, as A92's chain).
 * m = ŝ: apply the theorem to the Ψ^(w)-minimiser over the non-image packings at ŝ. K0-FREE gives, by (k1-b) and
   Theorem U (one-square agreement), that z* is an image — contradiction; so **every packing at ŝ is a Trump image**
   [given K0-O1-ALL's uniqueness half and Theorem U]. (E) at ŝ gives an image P′ differing from z* in TWO squares;
   Theorem U as proved covers one square, so this branch needs either the two-square form of Theorem U or the basin
   (displacement < r_B) — **[C], the only place where uniqueness is touched, and it is separate from the lower bound.**
 * Lean: `DrainSelW : ∀ m ∈ wnd, ∀ z, CfgPacking m z → IsMinOn Ψw (packings m) z → K0Blocked m z → ∃ i c, Intrudes z i c ∧
   MenuAdmissible z i c`, with `MenuAdmissible := ¬ heldBox z i c ∨ exchangeOK z i c` (the two consumable branches);
   `heldBox` is the finite Motzkin certificate of Lemma BOX-GORDAN on a box containing z (at radius 0, `held ∧ wheld` of
   `noroom.md`/`lockfree.md`); `exchangeOK` is `teleport_packing` applied to the two-square replacement. Consumers:
   `classKilledAt_of_kill` on [3.82, ŝ) through `k0free_kill` (`Slide.lean` 117) or the exchange's `teleport_packing`;
   at ŝ `StratumKillSel Ψ^(w)` of `nocrit_k0_blocked.md` §6 (`s_eleven_unique_of_sel`). Hypotheses added beyond A90 §6:
   none — the Ψ-minimality hypothesis is the same; the menu only enlarges the set of contradictions available.

### 1.3 What is weaker than LOCK-FREE⁺(< 4), and why it suffices

LOCK-FREE⁺(< 4) (A105 §1.3): every K0-BLOCKED packing at side m < 4 has an intruder that is not LOCKED (held ∧
W-held). DRAIN-SEL(W) differs in three ways, each a strict weakening:
 1. **one packing per side** — only z*(m), the Ψ^(w)-minimiser, not every K0-BLOCKED packing at m. The composition
    never looks at another packing: `s_eleven_ge_of_sel` obtains z* from `IsCompact.exists_isMinOn` and needs the kill
    there only (A90 §6). The empirical residue is consistent: the fully-held packings of A104 exist (58 of them, all
    above 4.0002), and none of them is known to be Ψ^(w)-minimal at its side — Ψ-minimality is a global property
    lock103 does not test.
 2. **m ∈ W only** — [3.82, ŝ], not (·, 4). Below 3.82 `lb_382` applies; above ŝ nothing is needed. This removes
    the whole band [3.9855, 4] in which every known K0-BLOCKED packing lives, and the band [4.0002, ·] in which the
    locked frames live. The theorem must therefore be true VACUOUSLY on W if s(11) = ŝ (M(m) = ∅ there): a proof is a
    proof that no selected minimiser at side ≤ ŝ can be a locked frame — the same statement as ¬RES-LOCK(m) on W
    (`noroom.md` §6), restricted to the menu.
 3. **a menu instead of one square** — (Cl) and (E) are motions of several squares; LOCK-FREE⁺ tests one. The 12
    non-retreatable exits of A90 T3 and the "jams on a near-contact" of A102/A103 were single-square artefacts; A104's
    closing iteration removed most of them by following the manifold, and A104's residue (the held frames at 4.0002+)
    is exactly the population on which (Cl)/(E) are tested here.
Uniqueness is untouched: at ŝ the statement is about non-image packings, and its (R)/(Cl)/K0-FREE branches compose
through Theorem U as before; only (E) raises the two-square question (§1.2).

## 2. T2 — the menu, each move with an exact neighbourhood inequality

### 2.0 [T] Lemma BOX-MOVE (the neighbourhood certificate) and Lemma BOX-GORDAN (its dual)

**Boxes.** For a configuration z = (c_i, θ_i)_{i≤11} at side m and r > 0 put B = B(z, m, r) := {(z′, m′) : |c′_i − c_i|_∞ ≤ r,
|θ′_i − θ_i| ≤ r, |m′ − m| ≤ r}. Every quantity below is evaluated as an INTERVAL over B (outward-rounded).

**Rows.** For two squares A, B′ and an edge k of A with outward unit normal n_k(θ_A) = R(θ_A) n⁰_k, the axis
separation is sep_k(A, B′) := n_k·(c_{B′} − c_A) − 1/2 − h(Δ_k), h(Δ) := (|cos Δ| + |sin Δ|)/2, Δ_k := θ_A − θ_{B′} + (k−1)π/2
(h is the support function of the unit square along n_k). **Lemma SAT [T, standard]**: A, B′ have disjoint interiors iff
max over the 8 axes (4 of each) of sep ≥ 0. Wall rows of A: c_{A,x} − h(θ_A), c_{A,y} − h(θ_A), m − c_{A,x} − h(θ_A),
m − c_{A,y} − h(θ_A) ≥ 0. **Depth candidates** of A at corner c (frame (sx, sy, o)): the four vertices p (value
max(p_{f,x}, p_{f,y})) and, for each edge whose inward frame normal n_f has n_{f,x}, n_{f,y} > 0 on B and whose diagonal
crossing can lie on the edge, the crossing value μ_E = (c_f·n_f − 1/2)/(n_{f,x} + n_{f,y}); μ_c(A) = the minimum over
the candidates (Lemma K's argument: the argmin of a convex piecewise-linear function over a polygon is at a vertex or
at a kink point of an edge, the diagonal crossing). Cand(B) := the candidates whose value can reach min(μ_hi(B), 1).

**The motion.** For C ⊆ {1..11}, Q ∈ C, and a screw y = (v, ω) ∈ ℝ³ about the origin, z′_ε := the configuration with
every member i ∈ C moved by the EXACT rigid motion g_ε = (R(εω), εv) (c_i ↦ R(εω)c_i + εv, θ_i ↦ θ_i + εω) and every
outsider fixed. Member–member relations are exactly preserved. The instantaneous velocity field at ε is the screw
(v − εωJv, ω) (|drift| ≤ ε|ω||v|).

**Derivatives (Fact D).** Along y, with ṅ = ωJn for a rotating normal and ċ = v + ωJc: for the axis of member A against
outsider B′, d sep/dε = (Jn·(c_{B′} − c_A))ω − n·v − (n·Jc_A)ω − h′(Δ)ω; for the axis of outsider A against member
B′, d sep/dε = n·v + (n·Jc_{B′})ω + h′(Δ)ω; walls: ċ_x − h′(θ)ω, ċ_y − h′(θ)ω, −ċ_x − h′(θ)ω, −ċ_y − h′(θ)ω; vertex
candidate p: ṗ_f = (sx ṗ_x, sy ṗ_y) with ṗ = ċ + ωJ(p − c); edge candidate: μ′_E = [ċ_f·n_f + ω_f(c_{f,y}n_{f,x} −
c_{f,x}n_{f,y}) − μ_E ω_f(n_{f,x} − n_{f,y})]/(n_{f,x}+n_{f,y}), ω_f = sx·sy·ω (ROT-GRAD's edge formula in the frame).
h′ is the branch derivative (−sgn(cos Δ) sin Δ + sgn(sin Δ) cos Δ)/2, and on B it is replaced by the HULL over all sign
branches admissible on B (both signs at a zero) — the one-sided derivatives of |cos| + |sin| at a kink are among the
branch values. Each derivative is thus an affine form Σ_j a_j y_j with interval coefficients a_j = [lo_j, hi_j] over B,
and its lower bound at a given y is Σ_j min(lo_j y_j, hi_j y_j). [T: direct differentiation; every formula checked
against finite differences at 300 random poses, `code/test128.py`: max |fd − formula| 4.5·10⁻⁶ at step 10⁻⁶, and the
depth bound never above the finite-difference right-derivative.]

**Lemma BOX-MOVE.** Let a screw y, a cluster C ∋ Q and a corner c satisfy on B (with the padded box B⁺ = B(z, m, r + 10⁻⁶)
and the drift interval for v):
 (P) for every member A ∈ C and outsider B′ ∉ C: either some axis has sep > 0 throughout B⁺ (margin), or every axis
     whose separation can be ≥ 0 somewhere on B⁺ has derivative lower bound > 0 on B⁺;
 (W) every wall row of a member that can be ≤ 10⁻⁷ on B⁺ has derivative lower bound > 0;
 (D) every candidate p ∈ Cand(B⁺) of Q at c has branch-derivative lower bound > 0 (both branches when the vertex can lie
     on the diagonal);
 (N) for every member i and corner c′ with (i, c′) ≠ (Q, c) such that μ_{c′}(Q_i) can be ≤ 1 on B⁺, every candidate of
     Cand(B⁺) has branch-derivative lower bound ≥ 0.
Then for every packing z′ ∈ B (at its side m′) at which Q intrudes c there is ε₀ > 0 such that for all ε ∈ (0, ε₀]: z′_ε
is a packing at side m′, d_c(Q(ε)) < d_c(Q), every other depth is nonincreasing, hence Ψ^(w)(z′_ε) < Ψ^(w)(z′) for EVERY
positive weight vector w. Consequently **B contains no Ψ^(w)-minimiser at which Q intrudes c**; if moreover at most two
squares can meet int(cell c) on B, then every selected minimiser in B is K0-FREE at c.

*Proof.* Fix a packing z′ ∈ B. (Pairs.) For members A, B′ ∈ C nothing changes. For A ∈ C, B′ ∉ C: by Lemma SAT some axis k*
has sep_{k*}(z′) ≥ 0. If the pair has a margin axis, that axis stays > 0 for small ε by continuity, uniformly on B (the
margin is a lower bound over B⁺). Otherwise k* is an axis whose separation can be ≥ 0, so its derivative along the
motion is ≥ δ > 0 at every point of B⁺; the motion stays in B⁺ for ε ≤ ε_pad := 10⁻⁶/(|v| + |ω|(m + 2)); sep_{k*} is
piecewise smooth in ε (a smooth part plus −h(Δ(ε)), a max of four smooth branches) with both one-sided derivatives among
the branch values, all ≥ δ; a continuous function with all one-sided derivatives ≥ δ > 0 is increasing; so sep_{k*}(ε) ≥
sep_{k*}(0) + εδ > 0. (Walls.) Same argument. (Depth of Q.) μ_c(Q(ε)) = min over candidates of their values; candidates
outside Cand(B⁺) exceed μ by a uniform margin on B⁺ and stay irrelevant for small ε; each candidate in Cand(B⁺) is a
max of ≤ 2 smooth branches (vertex) or one smooth function (edge) whose one-sided derivatives are among the branch
derivatives, all ≥ δ_D > 0 on B⁺; so μ_c(Q(ε)) ≥ μ_c(Q) + εδ_D and d_c strictly decreases (d_c(Q) > 0 by hypothesis).
(Other depths.) Identically with ≥ 0 wherever μ ≤ 1; where μ > 1 with margin the depth stays 0. (Ψ.) Outsiders'
depths are unchanged; Q's term strictly decreases; every other term is nonincreasing; positive weights. z′_ε ∈ M(m′).
If z′ were Ψ^(w)-minimal on M(m′), contradiction. The last clause: at a selected minimiser in B, Q does not intrude c,
so c has at most one intruder. ∎

Remarks. (1) The certificate is a statement about the BOX, not about z: nothing in it depends on z being a packing,
and the near-contacts of A102/A103 (gaps 10⁻⁷…10⁻³) are inside a 10⁻³ box, so they are rows of the certificate
automatically — this is where "held on a neighbourhood" is strictly stronger than "held at the point": a parallel-edge
contact whose two tilts differ by 3·10⁻⁹ has, at the exact point, a first-order opening direction (blocked after 5·10⁻⁹
by the kink; `noroom.md` §2.2 remark (2)), while on any box of radius ≥ 3·10⁻⁹ both branches of h′ are admissible and
the rotation is charged in both senses. (2) At r = 0 with the exact contact set the conditions are exactly Lemma ROT's
strict system (C = {Q}) with the diagonal-vertex branches taken conservatively (both rather than the max). (3) The
weak rows (N) are what makes the conclusion weight-free; with a specific w one could trade a member's deepening against
Q's retreat — not used. (4) The certificate says nothing at points of B where Q does not intrude c; the K0-FREE clause
handles them when c has ≤ 2 possible meeters on B. (5) Soundness of the interval evaluation: mpmath `iv` at 64 bits,
outward rounding, every float read of an interval bound moved one ulp outward; the only trigonometric quantities are
cos/sin of pose intervals, supplied by `iv`.

**Lemma BOX-GORDAN [T] (the dual; Motzkin form).** Let the strict rows be a_k (k ∈ K_s) and the weak rows b_l (l ∈ K_w),
each an interval affine form in y ∈ ℝ³ with coefficient boxes [lo, hi]. The robust system {Σ_j min(lo_kj y_j, hi_kj y_j)
> 0 ∀k ∈ K_s, Σ_j min(lo_lj y_j, hi_lj y_j) ≥ 0 ∀l ∈ K_w} has a solution iff the linear system in (y⁺, y⁻) ≥ 0, y = y⁺ − y⁻,
{Σ_j (lo_kj y⁺_j − hi_kj y⁻_j) > 0, Σ_j (lo_lj y⁺_j − hi_lj y⁻_j) ≥ 0} has one (the split with y⁺_j y⁻_j = 0 is exact and
any other split is dominated), and by Motzkin's transposition theorem the latter is infeasible iff there are μ ≥ 0 on
K_s, not all zero, and ν ≥ 0 on K_w with
  Σ_k μ_k lo_kj + Σ_l ν_l lo_lj ≤ 0 ≤ Σ_k μ_k hi_kj + Σ_l ν_l hi_lj  for j = 1, 2, 3:
**Q is HELD ON B with cluster C** iff a non-negative combination of the interval rows has coefficient boxes all
containing 0. At r = 0 (lo = hi) with C = {Q} this is Gordan's certificate of Lemma ROT (contact wrenches + virtual
corner rows in compressive equilibrium); with C = C_e(Q), ω = 0 it is NOCRIT-SEL's anchoring (a wall row (W) or a
deepening member's row (I) enters the combination). ∎

Lean shape: `boxHeld (B : PoseBox) (C : Finset (Fin 11)) (i : Fin 11) (c : Fin 4) : Prop` := the Motzkin certificate over
the finite row list (rows are rational-interval evaluations of `CaseSat.lean`'s polynomial separations and of the
depth candidates — the same T5-style interval leaf machinery as `Local.lean`'s dyadic checker of A119); `box_move :
¬ boxHeld B C i c → ∀ z' ∈ B, CfgPacking m' z' → Intrudes z' i c → ¬ IsMinOn Ψw (packings m') z'`, proved from Fact A/D
(polynomial rows, `ring_nf`-checkable derivatives), Lemma SAT (`sat_selection`, A119's one axiom) and the
one-sided-derivative argument (a finite case split per row).

### 2.1 (a) [T] Lemma CLUSTER-ROT — the joint screw of a retreat cluster

**Lemma CLUSTER-ROT.** Let z* minimise Ψ^(w) over M(m) (or over the non-image packings at ŝ). For every intruder Q of
every corner c, every set C ∋ Q of squares and every consistent selection, the strict system
  ⟨a_k, y⟩ > 0 for every active pair row between a member and an outsider and every active wall row of a member
  (gradients with respect to the cluster's screw (v, ω), Fact D at r = 0),  D_p(y) > 0 for every extreme argmin
  point p of Q at c,  D_p(y) ≥ 0 for every extreme argmin point of every other member at every corner it intrudes or
  touches (a weak row),
has no solution y ∈ ℝ³. Motzkin form: a non-negative combination of the member–outsider wrenches, the member wall
wrenches, Q's virtual corner rows (with a positive total weight together with the pair/wall rows) and the other
members' virtual rows vanishes. In particular (ω = 0, C = C_e(Q), e ∈ {e_x, e_y} ∩ K_c(Q)) this is NOCRIT-SEL's
anchoring, and (C = {Q}) it is Lemma ROT. *Proof.* Lemma BOX-MOVE at r = 0 (the exact contact set: an inactive row has
a positive margin and is not a row), or directly: z* + εy is S-feasible for small ε (member–member rows unchanged,
member–outsider and wall rows strictly increasing, inactive rows keep their margins), a packing at side m, in M(m); Ψ^(w)
strictly decreases (Q's depth strictly, the others nonincreasing by the weak rows, outsiders unchanged). ∎

Which clusters? Unlike the translation case there is no canonical cluster for a screw: a rotating cluster drags each
neighbour through a different motion, so "closed under pressing" is not defined. The experiment (§3) enumerates, for
each subject Q: {Q}; the four cardinal retreat closures C_e(Q) of NOCRIT-SEL (the forward closure of "presses
against e", at the point); Q ∪ (its contact neighbours); the contact component of Q; and every connected subset of the
contact graph (gap < 5·10⁻³, so that every near-contact inside the box counts as an edge) containing Q with ≤ 4
members (≤ 80 clusters). For each cluster the screw is found by the robust LP of Lemma BOX-GORDAN's primal (max t) and
then certified independently on the padded box. The exact inequality on the neighbourhood is Lemma BOX-MOVE's
certificate for (C, y, r); its failure for every enumerated C is the (finite, per-box) statement "held under CLUSTER-ROT
on B", which is not a theorem about all clusters (there are 2¹⁰ subsets) — the enumeration is the bounded experiment's
choice, recorded per row.

### 2.2 (b) [T] Lemma EXCHANGE-BOX — Lemma EXPOSE on a neighbourhood

Lemma TWO (A98 §2.1) says a K0-BLOCKED packing has a corner with exactly two intruders, and the slot square S_c is
interior-disjoint from every non-intruder by definition. Lemma EXPOSE (A98 §4.1): with A, Q the two intruders of c, a
closed unit square Q₀ gives the packing P′ = P \ {A, Q} ∪ {S_c, Q₀} at the same side iff Q₀ ⊂ [0, m]², int Q₀ ∩ int S_c = ∅,
and no untouched square has an interior point in int Q₀. The "swap/slide" of the brief is this with Q₀ chosen in the
footprint of A ∪ Q (A87's placements: Q₀ = B re-placed in its own footprint plus a sliver); Q and its neighbour A "trade
places" in the sense that A's place is taken by the exact slot square and Q's by the re-fit.

**Lemma EXCHANGE-BOX.** Let B = B(z, m, r), c a corner, and suppose exactly two squares A, Q can meet int(cell c) on B
(μ_c < 1 somewhere on B; the others have μ_c ≥ 1 throughout B). Let Q₀ be a unit square given by a FIXED pose (u, v, φ)
in the corner frame, with (i) Q₀ ⊂ [0, m′]² for every m′ ∈ [m − r, m + r] (interval check in the frame, m′-dependent
only through the far walls), (ii) μ_c(Q₀) ≥ 1 exactly (a frame quantity, m′-free), (iii) for every untouched j ∉ {A, Q}
some axis of the pair (Q₀(m′), Q_j(z′)) has separation ≥ 0 for all (z′, m′) ∈ B. Then for EVERY packing z′ ∈ B at side m′
the configuration P′ := z′ \ {A, Q} ∪ {S_c(m′), Q₀(m′)} is a packing at side m′ containing a corner slot square. Hence B
contains no packing at any side m′ ∈ [3.82, ŝ) (K0-O1), and at ŝ every packing in B is an image up to the two replaced
squares. *Proof.* S_c(m′) is the corner cell; its interior meets int Q_j only if Q_j meets int(cell c), so the untouched
squares are interior-disjoint from S_c by the two-meeter hypothesis; Q₀ is interior-disjoint from S_c by (ii) (a
point of int Q₀ has max(p_x, p_y) > μ_c(Q₀) ≥ 1, so it is outside the open cell), from the container by (i) and from every
untouched square by (iii) and Lemma SAT; the untouched squares are pairwise interior-disjoint as parts of z′. ∎

This is a ∀-packings kill of the box (no selection, no Ψ), and it is exactly A118's teleport leaf with the cell's two
possible meeters removed and one of them re-fitted. What it needs, in practice: a re-fit with positive margin against
the nine untouched squares AND their motion inside B — margins of 2.5r and more. The search (§3) maximises the minimum
separation over frame poses (Nelder–Mead from the two removed squares' poses, the cells of the lattice, and random
starts) and then certifies the maximiser. Lean shape: `teleport_packing` twice (the cell and Q₀'s exact frame pose), with
the interval disjointness (iii) as a T5-type leaf; the hypothesis "exactly two possible meeters on B" is A118's
`LANE(C) + M(C)` count with the two meeters named.

### 2.3 (c) TWO-WALL — what an inequality coupling two walls can and cannot certify on a neighbourhood

**Lemma TW-BOX [T, trivial].** Every packing (z′, m′) ∈ B satisfies m′ ≥ max_i x_max(Q′_i) − min_i x_min(Q′_i) and the same
in y; the interval lower bound of the right side over B, m_TW(B), is a lower bound on the side of every packing in B;
if m_TW(B) > ŝ, B contains no packing of W. — On a box of radius 10⁻³ around a sample packing at side s* this reads
s* − 2.5·10⁻³ > ŝ, true for every sample row except Trump (Table 2): the "coupling" of the two walls through the corner
square is already in the poses, and the inequality certifies nothing that reading the side does not.

**Lemma TW-HOOK [T] (the coupling, in the only family where it is exact).** At a hook corner in A105's sense (a
wall-hugging axis-aligned nick N = [0, 1] × [1 − ε, 2 − ε] on the left wall carried by a tilted floor square T of tilt θ
through N's inner corner (1, 1 − ε)), the y-chain's first member (N) fixes the x-chain's start: T's lowest vertex is at
  v_x^α = 1 + tan(θ/2) + (cos θ/ sin θ)·ε  (kind α),   v_x^β = 1 + (1 − sin θ)/cos θ + (sin θ/ cos θ)·ε  (kind β),
so the nick depth ε, a y-quantity, is paid on the floor with gain cot θ (α) or tan θ (β), and the floor's remaining
budget for the rest of the x-chain is m − v_x − cos θ (α) resp. m − v_x − sin θ (β); the wall's remaining budget above
N for the y-chain is m − 2 + ε. Adding the two: (m − v_x − c_T) + (m − 2 + ε) = 2m − 3 − t(θ) − (g(θ) − 1)ε − c_T with
t = tan(θ/2), g = cot θ (α) / t = (1 − s)/c, g = tan θ (β): **a deeper nick buys the wall (m − 2 + ε grows by ε) and
costs the floor (g − 1)ε more** — for α with θ < 45° the floor loses more than the wall gains (cot θ > 1). The
consequences that close are A105's: two same-kind hooks on one wall need m > 4 (HOOK-α: m ≥ 2 + Φ + ε₁ + ε₂, Φ ≥ 2;
HOOK-β: m ≥ 4 + tan θ(ε₁ + ε₂)); the mixed flush pair fits at 2 + f(θ) + (s/c)ε₁ + (c/s)ε₂ with f < 2 on (0°, 30°).
*Proof.* The identities are A105 §3.1 (T's carrying edge passes through (1, 1 − ε) and T's lowest vertex is on the
floor); the budget arithmetic is a sum. ∎ On a box: ε and θ are intervals (the nick's pose and T's tilt within r); the
identity's box form is v_x ∈ [v_x(θ − r, ε − r) − corrections, …], evaluated in Table 2 for the hook corners of the sample
(Trump's TL β-hook, the two sub-4 records, K03's and K05's hook-type corners): [M] the residual v_x(actual) −
v_x(formula) is ≤ 5·10⁻⁷ at every hook found, and the box enclosure contains the actual vertex — an identity, not a
kill.

**[F] Verdict on (c).** A two-wall inequality is a statement about a FAMILY (a contact structure), where it is exact
and where A105 showed the one-wall instance is false for mixed pairs and the two-wall instance is not side-free; on a
NEIGHBOURHOOD of a given packing it collapses to TW-BOX. The reviewer's "inequality coupling several walls" therefore
cannot be a box leaf; it can only enter as a family-level exclusion inside a proof of DRAIN-SEL, and the family it
excludes (same-kind hook pairs) is one the residue avoids (A105 §3.6). Nothing in T3 is decided by (c).

### 2.4 (d) Lemma SUPPLY — the row count of a held intruder, and the four-corner budget

**Lemma SUPPLY [T].** Let Q be HELD at c (Lemma ROT's Gordan certificate) with r_s square rows (one per vertex-on-edge
contact, two per edge-to-edge contact) and r_w wall rows (one per vertex on a wall, two for a flush edge).
 (i) If Q is PUSHED (λ ≠ 0), the contact wrenches positively span the wrench −λ ḡ of the corner-ward push at the
     argmin point (Lemma LINE). A wrench in ℝ³ lies in the cone of r wrenches in general position only if r ≥ 3; so
     r_s + r_w ≥ 3, or r_s + r_w = 2 with the two contact lines of action and the push line CONCURRENT (or all parallel
     — impossible for a push and two contacts on a unit square), or r_s + r_w = 1 with the single contact force exactly
     opposite to the push along the push line.
 (ii) If Q is WEDGED (λ = 0), the contact wrenches admit a non-trivial non-negative vanishing combination: r_s + r_w ≥ 2
     with two exactly opposite wrenches, or ≥ 3 in general.
 (iii) Walls: a flush edge on a wall supplies two parallel wrenches, i.e. a force normal to the wall applied anywhere
     on the contact segment (NO-TIP); a wall never supplies a force with a component toward the corner-ward push of a
     wall-hugging intruder (ROT-W remark (i)), so for a nick on the wall the vertical balance and the torque must come
     from ≥ 2 square rows (HOOK-N's carrier + presser) or 1 square row through the argmin point (PUSH-LINE with G = 0).
 (iv) Four corners: with 8 intruders the demand is ≥ 8·3 = 24 rows minus the concurrency exceptions. The contact graph
     of interior-disjoint convex sets in the plane is planar (join centres through the contact points; two such paths
     never cross), so there are ≤ 3·11 − 6 = 27 square–square contacts, i.e. ≤ 54 square rows (≤ 108 if all are edge-to-
     edge), plus ≤ 16 wall rows on the intruders (two walls each) and more on flush edges. **The count does not close:
     supply ≥ 54 ≥ 24 = demand** [F] — A103 §4's "the count is vacuous" and A104's measured anatomy (3.28 square + 0.97
     wall rows per intruder, 145 of 464 wedged) in one line. What the count DOES say: a held intruder is a square with
     ≥ 3 contacts or with an exact concurrency, so the residue's corners are 2-crowds each of whose members has a
     3-contact star or a concurrent 2-contact star — the objects of Table 2's "rows" column.
*Proof.* (i)–(ii): linear algebra of cones in ℝ³ (a cone generated by r ≤ 2 vectors is contained in a plane through 0,
so it contains −λḡ only if the three wrenches are coplanar: concurrency of the lines by Lemma LINE); (iii) ROT-W remark
(i) and Lemma LINE; (iv) planarity + Euler. ∎

Lean shape: (i)–(ii) are `Finset`-rank statements over the rational wrenches; (iv) is not needed by any consumer.

## 3. T3 — the bounded experiment

### 3.1 Protocol

`attempts/A128-coupled-moves/code/coupled128.py` (one process, BLAS pinned, BelowNormal, pure geometry with
three-variable linprogs for the direction search as in lock103/lockw105; ~2 minutes for the whole sample). For each
sample packing z at side m and each corner c: the SUBJECTS are every square that can meet int(cell c) somewhere on the
largest box (the point intruders and the tangent squares). For each subject Q:
 * ROT / CLUSTER: for r ∈ {10⁻³, 3·10⁻⁴, 10⁻⁴, 10⁻⁵, 10⁻⁶} in that order, the interval rows of Lemma BOX-MOVE are built on
   B(z, m, r) (`BoxGeom`, cached per radius), the robust LP of Lemma BOX-GORDAN's primal is solved for {Q} and for every
   enumerated cluster (§2.1; 20–80 per subject), and every LP solution with t > 0 is re-evaluated by an independent
   interval pass on the padded box B(z, m, r + 10⁻⁶) with the screw's drift; the largest certified radius is reported.
   The point verdicts are the same machinery at r = 10⁻⁸ (lock103's operational semantics: parallel-edge kinks within
   10⁻⁸ count both branches) and at r = 0 (the exact first-order test).
 * EXCHANGE: the possible meeters of c on B(z, m, 10⁻³); if exactly two, a re-fit Q₀ is searched in the corner frame
   (Nelder–Mead on the minimum separation from the nine untouched squares, the slot square and the container; starts:
   the two removed poses, the eight lattice cells, 12 random poses) and Lemma EXCHANGE-BOX is certified on the largest
   radius (same list) for which (i)–(iii) hold with interval margins.
 * TWO-WALL: hook detection at c (A105 §3.1: axis-aligned wall-hugging nick + floor carrier through its inner corner),
   the identity residual and its box enclosure; the extent bound m_TW(B) at r = 10⁻³.
 * SUPPLY: square rows, wall rows, and the certificate mode (pushed / wedged / none) of Q at the point.
 * Sampled confirmation of EVERY certificate: 10⁴ configurations drawn uniformly in the certified box; every certified
   row's derivative (ROT/CLUSTER) or every untouched square's disjointness from the placed squares (EXCHANGE) evaluated
   in floating point against the certified bound — hits = violations.
Canaries: Trump must be held under every move on every box (it is the unique packing at ŝ, so any certificate at Trump
would be a bug); the A104 locks must be held under ROT at the point in lock103's semantics (they are: 8/8 both, and
`test128.py` reproduces lock103's verdicts square by square, with the exact-r0 differences explained by the parallel-edge
kinks of remark (1), §2.0).

### 3.2 The sample

| row | what | side | cells |
|---|---|---|---|
| TRUMP_canary | A03 exact data | 3.877084 | l1_153 (a Trump-image cell; must stay alive) — canary |
| lock_4.000237 | A104 `rnd0173`, fully held at lock103's bar | 4.000237 | boundary packing |
| lock_4.001525 | A104 `rnd0157`, Gordan-certified held at all eight | 4.001525 | boundary packing |
| K01 | A107 k0 shadow, 6 slot + 5 free | 4.000000 | l1_071, l2_p65_101 (and l1_148's A99 twin) |
| K02, K03, K05 | A107 k0 shadows | 3.9428, 3.9251, 3.9122 | K03 ⊃ l2_p65_111, K05 ⊃ l2_p74_001 |
| K04 | A107 k0 shadow | 3.914214 | l1_104 |
| K06 | A107 k0 shadow (the pinwheel family) | 3.886745 | l1_159 |
| K20 | A107 k0 shadow | 3.924402 | l2_p114_001 |
| K26 | A107 k0 shadow | 3.985467 | s3_far_BL389484_TR018470 |
| cell_l1_124, cell_l1_148, cell_l1_158 | near-packings of the FRACTIONAL A115 supports (no A107 shadow), built by `nearpack128.py`: the conditioned square + a maximal set of support atoms, all eleven polished free (worst gaps −1.8·10⁻¹¹, −2.0·10⁻⁹, −1.6·10⁻⁸); they land on known values — 3.942810 (= K02's s*), 4.000000 (K01's), 3.902674 (= S10's) | 3.9428, 4.0000, 3.9027 | l1_124, l1_148, l1_158 |
| extra_floor1e-3 | A87's 3.9907 strictly K0-BLOCKED record (extra row) | 3.990749 | — |
| extra_record_s0115 | A87's 3.98548 record (extra row) | 3.985484 | — |

The shadows are k ≥ 1 packings (slot squares at named cells, free squares from `shadows_k0.json`, tilts taken mod π/2;
worst gap at the point ≥ −1.4·10⁻⁸ except K06, −1.1·10⁻⁶, A107's own landing); the boxes around them contain
K0-BLOCKED configurations (every corner has ≥ 2 possible meeters on B) except where the table says "K0-FREE box".

### 3.3 The table (`results/table128.md`, the full per-subject rows; `results/moves128.jsonl`, everything)

Per packing: subjects tested; ROT / CLUSTER certified at r ≥ 10⁻³ (and at any radius); subjects certified by a cluster
and by no single-square move; EXCHANGE-certified corners; corners K0-FREE on the box (≤ 1 possible meeter); whether the
packing is held under the WHOLE menu on EVERY box; the box verdict "DEAD at radius r" (some corner has ≤ 1 possible
meeter, or an exchange certificate, or exactly two possible meeters one of which is certified retreating — Lemma
BOX-MOVE's last clause); the extent bound; hook corners found.

| packing | side | K0-BLOCKED at z | subjects | ROT ≥ 10⁻³ / any | CLUSTER ≥ 10⁻³ / any | cluster-only | EXCHANGE corners (r) | K0-FREE corners on B | held under the whole menu on every box | BOX DEAD at r | hooks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| TRUMP_canary | 3.877084 | no | 9 | 0 / 0 | 0 / 0 | 0 | 0 | 0 | **YES (canary PASS)** | — | TL (β) |
| lock_4.000237 | 4.000237 | yes | 8 | 0 / 1 | 0 / 2 | 2 (r = 10⁻⁶) | 3: BL (10⁻³, margin 3.9·10⁻³), BR (10⁻⁵), TR (10⁻⁵) | 0 | no | **10⁻³ (BL, by EXCHANGE)** | — |
| lock_4.001525 | 4.001525 | yes | 8 | 0 / 0 | 0 / 0 | 0 | 1: BR (10⁻⁵, margin 1.5·10⁻⁴) | 0 | **YES at r ≥ 10⁻⁴** | 10⁻⁵ (BR, by EXCHANGE) | — |
| K01 | 4.000000 | no | 7 | 2 / 2 | 1 / 1 | 0 | 1: TL (10⁻³, margin 1.4·10⁻²) | 2 (BR, TR) | no | 10⁻³ | — |
| K02 | 3.942809 | no | 8 | 2 / 2 | 1 / 1 | 0 | 0 | 0 | no | 10⁻³ (TL, by ROT) | — |
| K03 | 3.925149 | no | 8 | 0 / 0 | 0 / 0 | 0 | 0 (flush re-fits, margin −1.5·10⁻⁹) | 0 | **YES** | — | BR (2) |
| K04 | 3.914214 | no | 7 | 2 / 2 | 0 / 0 | 0 | 0 | 2 (BR, TL) | no | 10⁻³ | — |
| K05 | 3.912232 | no | 8 | 1 / 1 | 0 / 0 | 0 | 0 | 1 (BR) | no | 10⁻³ | TL (2) |
| K06 | 3.886745 | no | 9 | 0 / 0 | 0 / 0 | 0 | 0 (margins ≤ −2·10⁻⁷) | 0 | **YES** | — | — |
| K20 | 3.924402 | no | 8 | 1 / 1 | 0 / 0 | 0 | 0 | 1 (TL) | no | 10⁻³ | — |
| K26 | 3.985467 | no | 7 | 1 / 1 | 0 / 0 | 0 | 1: TL (10⁻³, margin 1.3·10⁻²) | 1 (TR) | no | 10⁻³ | — |
| cell_l1_124 | 3.942810 | no | 9 | 0 / 1 | 0 / 0 | 0 | 0 (margins 10⁻⁸ … 4·10⁻⁷, flush) | 0 | **YES at r ≥ 10⁻⁵** (TL sq3 by ROT at 10⁻⁶) | 10⁻⁶ | — |
| cell_l1_148 | 4.000000 | no | 8 | 3 / 5 | 1 / 2 | 0 | 1: TL (10⁻³, margin 8.4·10⁻⁴) | 0 | no | 10⁻³ (BR by ROT, TL by ROT and EXCHANGE) | — |
| cell_l1_158 | 3.902674 | no | 8 | 1 / 1 | 0 / 0 | 0 | 0 (flush) | 1 (TL) | no | 10⁻³ (TL) | BL (4) |
| extra_floor1e-3 | 3.990749 | yes | 8 | 1 / 2 | 0 / 0 | 0 | 2: BR (10⁻³, 4.6·10⁻³), TR (10⁻⁴) | 0 | no | 10⁻³ (BR) | BL, BR, TR, TL (1 each) |
| extra_record_s0115 | 3.985484 | yes | 9 | 0 / 1 | 0 / 0 | 0 | 0 (BL/BR margins −7·10⁻³; TL/TR 3 meeters) | 0 | no (TL sq4 by ROT at 10⁻⁵ only) | — | BR (1) |

Sampled confirmations: every certificate in the table was re-sampled, 10 000 → 10 000 → **0 hits** in every case (26
ROT/CLUSTER certificates, 9 EXCHANGE certificates; `moves128.jsonl`, field `sample`). The extent bound m_TW(B) exceeds
ŝ for every row but Trump (3.8741 < ŝ), as §2.3 predicts. The hook identities: every hook found (Trump's TL β-hook;
K03's BR and K05's TL, a stacked nick + carrier; the floor-10⁻³ record at all four corners; the 3.98548 record's BR
α-hook) has |v_x(actual) − v_x(formula)| ≤ 5·10⁻⁷ and the box enclosure contains the actual vertex — the identity of
Lemma TW-HOOK, never a kill.

### 3.4 Reading the table, per move

**ROT on a box (the single-square test made exact on a neighbourhood).** Fifteen subjects are certified at r ≥ 3·10⁻⁴,
and every one of them is either a square with NO contact at all (rows 0/0 — a rattler, Corollary 1 of NOCRIT-SEL:
K01 BR sq7, K04 TL sq8, K20 TL sq5, K26 TR sq9, cell_l1_148 TL sq2/sq7, cell_l1_158 TL sq7), a corner slot square
touching only its two walls (K01 TR, K04 BR, K05 BR), a one-contact free square (cell_l1_148 BR sq5), a floor-depth nick
of the 3.9907 record (BR sq3 at 10⁻³, TR sq6 at 3·10⁻⁴ — the PI's rotation drain and A103's screw, now on a
neighbourhood), or K02's TL pair (sq7 at 24°, sq6 upright; both retreat). At the A104
locks ROT certifies nothing at r ≥ 10⁻⁵ and only BR sq2 of 4.000237 at 10⁻⁶ — the neighbourhood test agrees with A104's
"fully held" and sharpens it: the first-order directions that exist at the exact point (six at 4.001525) are all blocked
within 5·10⁻⁹ by parallel-edge kinks and vanish on any box of radius ≥ 10⁻⁸ (remark (1), §2.0).

**CLUSTER-ROT.** [F] On no subject does a cluster screw certify at a radius where the single square does not, except at
radius 10⁻⁶: lock_4.000237 BR sq3 with cluster {3, 8, 9} and TR sq6 with {6, 7, 10}, and K02 TL sq7 with {6, 7} at the same
radius as ROT. At 4.001525 every enumerated cluster (up to 80 per subject: the four retreat closures, the contact
neighbourhood, the component, every connected ≤ 4-subset) is held on every box down to 10⁻⁶. The retreat clusters of
NOCRIT-SEL are wall-anchored at every subject of both locks (the (W) row is in every Motzkin certificate), which is
exactly RES-LOCK's condition (T). So the coordinated 9–11-square SQP exits of A90 T3 are not rigid cluster screws: they
are the motions A104's closing iteration follows along the manifold, and they are not first-order motions of any
rigid sub-cluster on a neighbourhood.

**EXCHANGE.** This is the move that works, and it works ∀-packings. At lock_4.000237 the BL crowd {sq0 (depth 0.657,
tilt 9°), sq1 (0.022, 9°)} is replaced on the whole 10⁻³ box by the slot square and a re-fit at frame pose (0.508,
1.509, 0.0038 rad) — the two tilted squares of the left column straighten into two cells — with interval margin
3.9·10⁻³ against the nine untouched squares (BR and TR likewise at 10⁻⁵); at lock_4.001525 only BR admits a re-fit
(cell (0,1) exactly, point margin 1.9·10⁻⁴, box 10⁻⁵); at K01 TL, K26 TL and the floor-10⁻³ record's BR the re-fit has
margins 10⁻² … 4.6·10⁻³ and certifies on the 10⁻³ box. [F] Where it fails it fails for one reason: the best re-fit is
FLUSH against an untouched square (margins −10⁻⁹ … +10⁻⁷ at K02, K03, K05, K06, K20; 3.98548's BL/BR at −7·10⁻³; Trump
−10⁻² at TL), and a flush placement has no neighbourhood — A98's "neighbour-free yield 0 %" and A101/A121's flush
population, seen from the box side. The exchange leaf on a box needs the re-fit to clear the untouched squares by
≳ 2.5 r; on the residue's nearest relatives that clearance exists at 4 of 14 blocked-type corners.

**TWO-WALL / SUPPLY.** Nothing is decided by either (§2.3, §2.4). The held intruders of the locks carry 3–7 square rows
and one wall row each, all PUSHED (a certificate with λ > 0: Lemma LINE's concurrent resultant), none wedged; the
record's BL sq1 has 3 square rows and no wall row and is held at the bar only through its near-contact (HOOK-W).

### 3.5 T3 verdict

By the reviewer's criterion (exact inequalities on neighbourhoods of radius ≥ 10⁻³; trajectories count as nothing):
 * **The menu certifies progress on the 10⁻³ box at 8 of the 11 non-Trump converged-alive cells' near-packings** (K01:
   l1_071, l2_p65_101; K04: l1_104; K05: l2_p74_001; K20: l2_p114_001; K26: s3_far; cell_l1_148; cell_l1_158) and at one
   of the two boundary locks (4.000237, by EXCHANGE at BL) and at the 3.9907 record (by ROT at BR and EXCHANGE at BR) —
   but at the shadows the certified move is almost always a trivial one (a corner rattler, a K0-FREE box), because the
   shadows are k ≥ 1 packings: the only NON-trivial certificates at r ≥ 10⁻³ are the five exchanges (4.000237 BL, K01
   TL, K26 TL, cell_l1_148 TL, floor-10⁻³ BR) and the two floor-depth nick retreats (floor-10⁻³ BR/TR).
 * **Four sample packings are held under the whole menu on every box of radius ≥ 10⁻⁴: lock_4.001525 (the
   Gordan-certified frame), K03 (l2_p65_111), K06 (l1_159) and cell_l1_124 (a K02-type packing at 3.9428), plus Trump
   as it must be**; at 4.001525 the exchange works on a 10⁻⁵ box only (BR, margin 1.5·10⁻⁴), at cell_l1_124 one slot
   square retreats on a 10⁻⁶ box only, and at K03/K06/l1_124 every re-fit is flush. The 3.98548 record is held at its
   hook wall (BL/BR) and at TL/TR only by the tangency-scale nick's retreat on a 10⁻⁵ box.
 * **Coupled moves versus single-square moves:** the cluster screw adds nothing at r ≥ 10⁻⁵; the exchange is the only
   coupled move that certifies where every single-square move fails, and it does so at 4 corners on the 10⁻³ box.
 * Trump: held under every member of the menu on every box, at every one of its 9 subjects (the five intruders and the
   four tangent squares); no exchange has a non-negative margin at any corner. **Canary PASS.**

The obstruction, drawn (`attempts/A128-coupled-moves/results/residue128.svg`, every square geometry-checked): the
4.001525 frame — two tilted 2-crowds at BL (sq1 0.103, sq0 0.062, both 83.3°, i.e. 6.7° off the axis, an upright
column leaning on the wall) and TL (sq5 0.044, sq4 0.032, 87.3°/87.9°), two 1 + nick crowds at BR (sq2 0.887 + sq3 at the
floor depth 1.02·10⁻³) and TR (sq6 0.921 + sq7 at the floor), every intruder pushed with 3–5 square rows and 1 wall row,
every retreat cluster wall-anchored, every re-fit flush except BR's (point margin 1.9·10⁻⁴). What a certificate at
r = 10⁻³ would need there: a move of the BL column {sq0, sq1} together with its pressers {sq10, sq5, …} that is not a
rigid screw — the manifold motion A104 follows (straightening the 6.7° column while the floor row slides), i.e. a
TWO-PARAMETER coupled move (column rotation + row slide) whose neighbourhood certificate is Lemma BOX-MOVE with a
non-rigid velocity field. That field is the exact residue of this experiment.

## 4. T4 — composition, and the residue after the menu

### 4.1 What the menu does and does not certify on the sample below 4

The brief's T4 condition — "T2's menu certifies progress on every sample packing below 4" — is NOT met: K03 (side
3.9251) and K06 (3.8867), the near-packings of the converged-alive cells l2_p65_111 and l1_159, are held under every
member of the menu on every box of radius ≥ 10⁻⁶ (their doubly-met corners are slot square + flush tangent square, and
every re-fit is flush), cell_l1_124 (3.9428) on every box ≥ 10⁻⁵, and the 3.98548 record's BL/BR crowds are held on
every box (its TL/TR nicks retreat only on a 10⁻⁵ box). So the composition of §1.2 is not discharged; what follows is the proof shape it would have and the exact
residue.

### 4.2 The proof shape of DRAIN-SEL(W) with the menu as the case analysis

For m ∈ W and z* = z*(m) K0-BLOCKED, by Lemma TWO some corner c has exactly two intruders A, Q; the cases:
 1. **[T now] Q or A not HELD or not W-HELD** (Lemmas ROT, ROT-W): contradiction with Ψ^(w)-minimality — the (R) branch.
    Lean: `rot_lemma`, `rotw_lemma` (`noroom.md` §8, `lockfree.md` §7).
 2. **[T now] some cluster C ∋ Q with a strictly opening, Ψ-decreasing screw** (Lemma CLUSTER-ROT): contradiction — the
    (Cl) branch; NOCRIT-SEL's anchoring is its ω = 0 sub-case. Lean: `box_move` at r = 0 with `C : Finset`.
 3. **[T now] a re-fit Q₀ with Lemma EXPOSE's (i)–(iii)** (EXCHANGE): a k ≥ 1 packing at side m, dead by K0-O1 — the (E)
    branch; ∀-packings, so it may be applied to any packing, not only z*. Lean: `teleport_packing` twice.
 4. **[C, the new obligation] the residue RES-MENU(m)**: K0-BLOCKED packings at side m, every intruder LOCKED, every
    enumerated cluster screw held (Motzkin certificates), every re-fit flush against an untouched square at every
    two-intruder corner. RES-MENU ⊆ RES-LOCK (`noroom.md` §6) strictly (the 4.000237 frame is in RES-LOCK at lock103's
    bar and not in RES-MENU: its BL exchange certifies); the 4.001525 frame is in RES-MENU at radius 10⁻⁴ and not at
    10⁻⁵. Realisations below ŝ: none known (the empirical residue in W is empty, as the brief says); nearest relatives:
    K03/K06-type k ≥ 1 packings with flush tangents at 3.887–3.925 (not K0-BLOCKED themselves), the 3.98548 record's
    hook wall.
 What is a theorem now and what is new: cases 1–3 are theorems (this file adds 2 and the box forms of 1–3); case 4 is
 the open leaf, and it is SMALLER than LOCK-FREE⁺'s residue by exactly cases 2–3. The composition through
 `Composition.lean` is unchanged from `noroom.md` §8 with `lockfree_plus` replaced by
   `drain_sel : ∀ m ∈ wnd, ∀ z, CfgPacking m z → IsMinOn Ψw (packings m) z → K0Blocked m z →
       ∃ i c, Intrudes z i c ∧ (¬ held z i c ∨ ¬ wheld z i c ∨ ¬ clusterHeld z i c ∨ exchangeOK z c)`
 consumed by `k0free_kill` / `teleport_packing` on [3.82, ŝ) and by `s_eleven_unique_of_sel` at ŝ (the `exchangeOK`
 branch at ŝ needs the two-square Theorem U, §1.2).

### 4.3 What it removes from the k0 row of `budget.md` — nothing yet

The k0 row prices the tree at 13,500 CPU-h (7,600–19,900) against "theorem route: 0". The menu as a THEOREM removes
nothing until case 4 closes. As box LEAVES the menu is a different matter: Lemma BOX-MOVE and Lemma EXCHANGE-BOX are
SelForm/∀-packings leaves of exactly the kind A85/A90 §6 priced ("free at deep nodes, silent at the frontier"), and
this experiment measures their fire rate on the residue's nearest relatives at radius 10⁻³: 10 of 15 non-Trump boxes
dead (7 of them by trivial rattler/K0-FREE reasons, 3 by exchanges alone), 0 by cluster screws. On the tree the boxes are far larger
than 10⁻³ at every level that carries cost (level-1 cells are 0.1 wide), so the leaf would fire only near the frontier —
the same verdict as K0-ROT/TF-U/EX (A89, A90, A98). **The k0 row stays at 13,500 / 0.** What would change it: case 4 as a
theorem, whose exact statement is now (§3.5) a certificate for a NON-RIGID two-parameter coupled move (column
straightening + row slide) at the 4.001525-type frame, or the two-square exchange with margin at the flush corners of
K03/K06-type packings — i.e. a depth-2 flood (A98's deficit-2 step) on a box.

### 4.4 The residue, drawn

`attempts/A128-coupled-moves/results/residue128.svg` (three panels, docs/residue_map conventions, every square checked
for containment and pairwise separation ≥ −10⁻⁷): the 4.000237 lock with its certified BL exchange (blue: the slot
square and the re-fit Q₀ = (0.508, 1.509, 0.0038) in BL's frame) and its held intruders (red); the 4.001525 frame, every
intruder red, BR's exchange at 10⁻⁵ only; Trump, all red, nothing fires. The coupled move that the 4.001525 frame needs is
named in §3.5.

## 5. Canaries

* **Trump** (K0-FREE; 9 subjects: BL sq0/sq1/sq3, BR sq2/sq8, TR sq5/sq9, TL sq6/sq4): held under ROT and every
  enumerated cluster at r = 10⁻⁸ and on every box 10⁻⁶ … 10⁻³; no exchange with a non-negative margin at any corner
  (BR/TR: −4·10⁻¹⁶, the strip's tilted square sits exactly on the slot's inner corner — Lemma TRUMP-LOCAL's geometry;
  TL: −10⁻²). The TL β-hook identity reproduces sq6's top-wall vertex to 5·10⁻⁷ on the box. The extent bound is
  3.8741 < ŝ (Trump is not excluded from W by any inequality here). **PASS, at every move.**
* **The A104 locks at the point**: lock103's verdicts reproduced square by square at r = 10⁻⁸ (8/8 held at both);
  `test128.py` shows the exact-r0 directions at 4.001525 are blocked at 5·10⁻⁹ by parallel-edge kinks (a finite motion
  of 10⁻⁸ overlaps pair (1, 10) by 5·10⁻¹⁰), i.e. lock103's two-row reading of a near-parallel flush contact is the
  box semantics at r ≥ 3·10⁻⁹.
* **The two sub-4 records**: A105's held hook wall (3.98548's bottom wall) is held on every box here too; A103's
  rotation/screw drains of the 3.9907 record's BR/TR nicks are the two floor-depth ROT certificates at 10⁻³ / 3·10⁻⁴,
  and its left wall (LOCKED 4/4 in A105) is held on every box. Consistent.
* **Finite differences**: 300 random poses × 8 axes × both movers, walls, and 4 corners' depths: max |fd − formula|
  4.5·10⁻⁶ at step 10⁻⁶; the depth lower bound never exceeded the finite-difference right-derivative.

## 6. Obligations ledger

| # | item | status |
|---|---|---|
| A128-O1 | Theorem DRAIN-SEL(W) stated against `noroom.md` §6/§8 and `Composition.lean`; what is weaker than LOCK-FREE⁺(< 4) and why it suffices; uniqueness separate (the exchange branch at ŝ needs a two-square Theorem U) | [T] statement §1; [C] the theorem |
| A128-O2 | Lemma BOX-MOVE (neighbourhood certificate for a cluster screw, weight-free), Lemma BOX-GORDAN (Motzkin dual with interval rows; = ROT's Gordan at r = 0); Fact D checked by finite differences | [T] §2.0 |
| A128-O3 | Lemma CLUSTER-ROT (joint screw of any cluster at the Ψ^(w)-minimiser; NOCRIT-SEL and ROT as sub-cases) | [T] §2.1 |
| A128-O4 | Lemma EXCHANGE-BOX (Lemma EXPOSE on a box, ∀-packings) | [T] §2.2 |
| A128-O5 | TWO-WALL: TW-BOX (trivial on a box), TW-HOOK (the nick-depth coupling, exact in the hook family); verdict: not a box leaf | [T]+[F] §2.3 |
| A128-O6 | Lemma SUPPLY (row count; four-corner budget vacuous by planarity) | [T]+[F] §2.4 |
| A128-O7 | T3: 15 packings × 5 moves decided exactly on boxes 10⁻³ … 10⁻⁶; 30 certificates, all re-sampled 10⁴ → 10⁴ → 0 hits; Trump held everywhere | [M] §3, `results/{table128.md,moves128.jsonl,summary128.json}` |
| A128-G1 | **RES-MENU(m) = ∅ on W** — the residue after the menu: LOCKED + cluster-held + flush re-fits; realised by the 4.001525 frame (r ≥ 10⁻⁴) and, below 4, by the flush corners of K03/K06-type packings; the coupled move needed is a non-rigid column-straightening + row-slide field, or a depth-2 exchange with margin | **[C]** §3.5, §4.2 |
| A128-O8 | the residue drawn: `results/residue128.svg` | [M] §4.4 |
| A128-O9 | Lean shapes: `boxHeld`/`box_move`, `drain_sel`, `exchangeOK` via `teleport_packing`; no `lean/` edits | note §1.2, §2.0, §4.2 |

Runs (`attempts/A128-coupled-moves/code/`, one process each, BLAS pinned, BelowNormal): `coupled128.py all` (~2 min)
→ `results/moves128.jsonl`, `logs/run128.log`; `summarise128.py` → `results/table128.md`, `results/summary128.json`;
`nearpack128.py` → `results/nearpack128.json`; `gen_residue128.py` → `results/residue128.svg`; `test128.py` (finite
differences + lock103 comparison; `lock103_copy.py` is A103's file copied, not imported). Read-only on every campaign
and attempt; frozen verifiers untouched; no `lean/` edits beyond the depgraph note; git fetch + plain merge + push of
own paths.

## 7. Addendum (A130, 2026-09-07) — the FLUSH case: non-rigid fields, the depth-2 exchange, and what a flush hold is

Files: `attempts/A130-flush-exchange/{notes/lemmas130.md (the lemmas, proofs, Lean shapes), notes/report130.md
(T1–T4), results/table130.md, results/moves130.jsonl, results/flush130.svg, results/shells130_K03_BR.json,
code/flush130.py}`. Labels as above.

### 7.1 [T] The moves (lemmas130.md §1–6)

* **Lemma BOX-FIELD-W** (§1): Lemma BOX-MOVE for a NON-rigid field (one exact screw per member of any set C, every
  pair with a member a row family, the flush kink charged through the exact rotation difference u = ω_{B′} − ω_A)
  with WEAK pair and wall rows (≥ 0 on the padded box; sound for r > 0 by the Dini-derivative argument, not at
  r = 0 where ROT's strict rows are the right statement) and Q's depth rows strict. The column-straighten +
  row-slide field of the brief is a point of its feasible set; the LP over all 33 variables finds the best field.
  Dual BOX-GORDAN-F (Motzkin with the equality rows for u).
* **Lemma MODE** (§2): a pair with ≥ 2 possibly-separating axes is, at every packing of the box, separated by its
  largest axis; on the piece where axis k is largest only row k is needed; a piece whose defining inequality is
  violated on the whole box is vacuous. **[F]** at a flush contact the pieces are the two contact modes (which
  square's corner rests on which edge), their common boundary is the exactly-flush stratum, and the slide that
  preserves the separating contact differs between the modes — a fixed field certified by intervals over a box
  fails by a sign of the order of the tilt uncertainty at EVERY radius: A128's "flush placement has no
  neighbourhood" is a MODE ACCUMULATION, not a lock. **Lemma SHELL-SCALE**: away from the stratum (tilt ∈ [a, 2a])
  a screw with rotation ∝ a certifies every dyadic shell, all coefficients affine in a, so one parametric
  certificate covers (0, r] except the stratum itself, where the slide is exact (Fact A). [M] K03 BR: shells
  a = 5·10⁻⁵ … 1.6·10⁻⁶ certified, failing exactly below the fixed pad 10⁻⁶.
* **Lemma EXCHANGE-2** (§3): A128's exchange whose re-fit Q₀ is flush against untouched squares F, plus a finite
  exact motion of a cluster C ⊇ F (weak rows everywhere, one strict opening axis per U ∈ F with sep ≥ −ρ_U on B
  and rate ≥ δ_U on the padded box, ε* = max ρ_U/δ_U inside the pad): every packing in B yields a k ≥ 1 packing at
  the same side. ∀-packings, no selection.
* **Lemma TWO-INTRUDER** (§4): with exactly two possible meeters A, Q on B, the field certificate for Q need only
  hold where A ALSO intrudes; the K03-type corner (slot-like deep meeter on the floor + flush tangent hugging the
  wall + an interior presser on the tangent's inner corner) is decided by hand on the box: two-intruder packings
  exist only with the tangent leaning toward the wall, and there the deep meeter's slide away from the corner is
  exact — every selected minimiser in the box is K0-FREE at that corner (a theorem; its interval form needs the
  contractor of Lemma MODE).
* **Lemma FLUSH-SLIDE** (§5, the point statement, n-general): at the Ψ^(w)-minimiser a floor (wall) intruder whose
  active contacts are the floor and squares on its top edge only is pressed on its FAR edge — a flush square with a
  free far edge slides (Lemma ROT-W with Fact A). **Lemma ISOLATED**: if the weak cone {rows ≥ 0, depth rate ≥ 0} is
  {0}, z is an isolated point of {packings, d_c(Q) ≤ d_c(Q)(z)} (curve selection). **Lemma KINK** (§6): the exact
  second-order condition at a parallel-edge contact (Δ̇ = 0 ⇒ the kink is second-order, −|w_A − w_{B′}|ε²/4; the
  Farkas/prestress form; the 2 × 2 determinant when dim K = 1) and its box form (only structurally-zero rows admit
  a second-order box certificate).

### 7.2 [M] T3 — the bounded experiment (table130.md; 10⁴ → 10⁴ → 0 hits on every certificate)

| hold | FIELD (all 11 squares, tilt-sign × mode pieces) | ROT-W | EXCHANGE-2 | point |
|---|---|---|---|---|
| K03 (l2_p65_111, 3.925149) | held on 10⁻³…10⁻⁶ (BR sq6 = f2: 10 of 32 pieces certified at 10⁻⁴, rate 1.000 each; every other subject 0 pieces) | held | not certified at any corner (flush blockers f4 / f5 / {f0, f3, f6} / {sq1, f0, f6} wedged in every sub-box and mode) | f2's exact slide toward f1 (rate 1.000): K03 is not Ψ^(w)-minimal; other rates at the residual |
| K06 (l1_159, 3.886745) | held (BR f1: 4 of 8 pieces) | held | not certified (blockers f4 / the 48.4° grain) | void (the landing overlaps by 1.1·10⁻⁶) |
| cell_l1_124 (3.942810) | held (TL sq3: 1 of 4 pieces; TL sq4 0/64) | held | not certified (blockers sq4/sq7, sq4/sq5, {sq0, sq1, sq6, sq8}) | sq3 slides down the wall (rate 1.000); [T] TL has no two-intruder packing at all |
| control 4.001525 | **CERTIFIED at all eight intruders on the 10⁻⁴ box** (min strict 0.052–0.319, every square moves, 0 hits) | held | BR 10⁻⁵ (= A128's depth-1) | weak-cone rates 0.11–0.32 at every intruder |
| 4.000237 / K01 (regression) | all eight at 10⁻⁴ / BR sq7, TR sq5 at 10⁻³ | BR sq2 10⁻⁶ (= A128) | as A128 (F = ∅) | 0.22–1.00 / 1.00 |
| Trump (canary) | held on every box | held | no re-fit at any corner | 0, ISOLATED at all nine subjects — PASS |

Reading. [F] The three window holds survive every move on every box, exactly because (i) at a (slot-like deep
meeter, flush tangent) corner the deep meeter's exact slide (Lemma FLUSH-SLIDE; weak-cone rate 1.000) is
certifiable by a fixed field only on the pieces where every flush partner leans toward the wall — Lemma MODE's
accumulation at the flush stratum, closed by hand (Lemma TWO-INTRUDER + SHELL-SCALE + the stratum) and not by
the plain leaf; and (ii) every re-fit's flush blocker is the interior grain, wedged. [F] The control falls: the
frame that was Gordan-certified locked at all eight intruders under single-square motions, and held under every
rigid cluster screw (A128), has a strictly Ψ-decreasing NON-rigid first-order field at every intruder (rates
0.11–0.32) certified on the 10⁻⁴ box — RES-MENU's only known member above 4 is not in RES-MENU⁺ (the residue with
the field added).

### 7.3 T4 — consequence for DRAIN-SEL(W)

The case analysis of §4.2 with FLUSH inserted (details `report130.md` T4, `lemmas130.md` §7):
 1–3 theorems (unchanged). **F [T] Lemma FLUSH-SLIDE**: at z* every flush floor/wall intruder is pressed on its
 FAR edge (a top-edge presser slides). **F′ [T modulo K0-O1] SLOT-GRAZER**: on W at m ≤ ŝ − δ no packing has a
 corner with an intruder of μ_c ≤ δ/(1 + √2) (Lemma SHELL + Lemma SLIDE) — the K03/K06/l1_124-type corners occur
 only in the slab (ŝ − (1 + √2)ρ, ŝ], where they are Lemma TRUMP-LOCAL's geometry. **FIELD [T at the point]**:
 BOX-FIELD-W at r = 0 with strict rows is CLUSTER-ROT for a non-rigid field (same proof); a strictly feasible
 field decreasing an intruder's depth contradicts Ψ^(w)-minimality. **Case 4 [C]**, the residue RES-MENU⁺(m):
 K0-BLOCKED, LOCKED, cluster-held, flush re-fits, flush intruders pressed on their far edges, NO strictly feasible
 field — realised by NOTHING on disk at any side (the two A104 locks fall to the field). Lean: one more disjunct
 `¬ fieldHeld z i c` (Motzkin over 33 + kink variables) in `drain_sel`'s conclusion, consumed as `¬ clusterHeld`.
 Cost of a menu certificate over the k0 root cells: the field leaf fires at radius 10⁻⁴ (locks) / 10⁻³ (rattlers,
 slots) and the level-1 cells are 0.1 wide — silent at the root, the K0-ROT/TF-U/EX verdict again; at flush stacks
 it is not a box leaf at all (mode contractor + parametric shells + the stratum statement). `budget.md` k0 row
 unchanged (12,000 / 0). A hold at a non-packing support costs DRAIN-SEL(W) nothing (the three holds are k ≥ 1
 packings above ŝ; their boxes' K0-BLOCKED packings are grazer-blocked slot corners, SLIDE-excluded on W outside
 the slab); it costs the TREE leaf, which is blind at every flush stack.
