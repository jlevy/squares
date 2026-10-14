# H10-stuck: the k ≤ 4 tier, re-based — route pricing and the boosted-kill program (A65, 2026-09-01)

Target: depgraph node **C.K4TIER** in its A63 re-based form (`unique_transfer.md` §3): **(H10-stuck)**
no teleport-stuck packing at the attained side has skeleton in a K1-protected class
({k4_03, k4_05, k4_06, k4_08, k4_11, corners4} and the ten open k ≤ 3 classes). The BRIEF's three
routes are priced here; two are closed decisively, and the third is reduced to a single
executable LP form with a per-class decision criterion. Labels: [T] proved, [S] soundness
statement routine given cited items, [M] measured/computed exact, [C] open.

Standing ingredients: A58 CC-1/CC-2′/CC-4 (`attempts/A58-clear-corner/notes/theory.md`), the
A58 occupancy matrix (exact, `results/occupancy_matrix.json`), A55 K1/K2 (protection), Lemma B
family (`closed_disjoint_bridge.md`), the frozen `case-lp-certificate-v1` verifier. Per
unique_transfer §3, CC-2′'s crowd conclusions are derived from teleport-stuckness alone
(K*-maximality is used in A58 only to OBTAIN a stuck packing), so all crowd facts below bind
the chain's stuck endpoint z*.

## 1 [T] The incidence lemma (the quantitative form of stuckness)

Fix a stuck packing P at side m̃ ∈ [3.82, s0] with skeleton exactly S (k pins). Let B_1 … B_m be
the **unclipped completable boxes** of S: the Young-ready cells of S's corner diagrams plus the
clear-corner roots, minus the boxes whose interior meets a pin square (the simple-clip census;
exact per class in the occupancy matrix, s-stable on the window by A53 L2(iv) slot arithmetic).
By CC-2′, each B_i is met (open interiors) by ≥ 2 of the 11 − k non-simple squares — in stratum
S the non-pin squares are exactly the non-simple ones, so R1 can only be realised by a pin,
which the unclipped condition excludes. Counting incidences (q, i) with int Q_q ∩ int B_i ≠ ∅:

> **(H10-I)** the 11 − k non-simple squares of P carry total box-incidence I ≥ 2m.

## 2 [M] The critical-ratio table, and the canary saturates it exactly

N = 11 − k squares must supply R = 2m incidences; the load factor is R/N
(`attempts/A65-low-k-closure/results/h10_boxspec.json`, from the A58 matrix):

| class | k | N | m (unclipped) | R | R/N |
|---|---|---|---|---|---|
| k0_00 | 0 | 11 | 4 | 8 | 0.73 |
| k1_00 | 1 | 10 | 5 | 10 | 1.00 |
| k2_00 | 2 | 9 | 5 | 10 | 1.11 |
| k2_01, k2_02 | 2 | 9 | 6 | 12 | 1.33 |
| k3_01 | 3 | 8 | 4 (2 clipped) | 8 | 1.00 |
| k3_02, k3_03, k3_04 | 3 | 8 | 6 | 12 | 1.50 |
| k3_05 | 3 | 8 | 7 | 14 | 1.75 |
| k4_03, k4_05, k4_06 | 4 | 7 | 5 (2 clipped) | 10 | 1.43 |
| k4_08, k4_11 | 4 | 7 | 7 | 14 | **2.00** |
| k4_13 = corners4 | 4 | 7 | 8 | 16 | **2.29** |
| *(trump5, canary)* | 5 | 6 | 6 (2 clipped) | 12 | **2.00** |

**Canary [M].** Trump's packing (stuck, teleport-extremal, A58 §5) realises H10-I with
EQUALITY on its own class: his 6 non-simple squares carry exactly I = 12 = R on trump5's 6
unclipped boxes — five squares at incidence 2 and the staircase-flanker sq8 at incidence 4
(A58 `trump_canary`, re-tallied). **The packing every argument must spare sits exactly on the
incidence threshold at load factor 2.00.** This is the structural reason the tier is hard:
any pricing scheme strong enough to beat load 2.00 generically would kill Trump. The
K1-protected classes split into strictly-subcritical (k ≤ 2, k3_01: crowding is cheap),
near-critical (k3_02–05, k4_03/05/06), and **at-or-above-critical (k4_08, k4_11 at 2.00;
corners4 at 2.29 — the only class with load strictly above the canary's)**.

## 3 [T] Route (a), decoupled crowd-pricing: DEAD — it ties the threshold exactly

The counting argument A58 left open, done: it cannot close, for a structural reason.
Suppose the pricing is **decoupled**: a covering measure μ₀ (μ₀(Q) ≥ 1 for every admissible
pin-clear placement) plus per-box measures ν_i (ν_i(Q) ≥ 1 for every pin-clear Q meeting B_i).
A stuck packing forces μ₀-total + Σν_i-totals ≥ (11−k) + 2m, so a kill needs the certified
totals STRICTLY below that. But: (i) μ₀-total ≥ τ* ≥ 11 − k (K1 aliveness — 11 − k disjoint
pin-clear squares exist for every protected class); (ii) ν_i-total ≥ 2, because **every
unclipped box admits 2 disjoint pin-clear meeters** [S]: a box has ≥ 2 free sides (predecessor
cells block at most two, walls the rest; the census leaves ≥ 2 free), and two pokers on
adjacent free sides can be made disjoint by tilting one — the axis-aligned pair always overlaps
in the near-corner sliver [1−a,1]×[1−b,1], but rotating the second poker by θ about its centre
lifts its near edge above the first poker's far edge (linear in θ) while its far corner still
penetrates the box; Trump's TL pair (ε-off upright + 40.18°-tilted) is exactly this
configuration in the wild. Hence decoupled total ≥ (11−k) + 2m with equality achievable in the
limit: **the decoupled bound ties the stuck threshold and can never beat it.** The same
conclusion covers all table-composition variants: A58's C6′ screening (max area charge
0.97·B0) already showed the certified zone tables cannot pay, and any position-free "meets-B"
single-square table is a decoupled ν_i. Route (a) in pure counting form is closed.

## 4 [M/pricing] Route (b) as scoped (conditioning on crowd positions): DEAD on cost

Encoding "two squares meet B_i" as case-LP hypotheses requires conditioning each crowd member
into a (c, t)-cell (the Box→core construction) and running the case-LP per cell-pair: the
reach set of a 1×1 box spans ~2.2 × 2.2 × all tilts, i.e. a zone comparable to A60's whole
conditioning zone; a pair-tree is that squared, per box, per class. A60's single zone tree on
ONE class is a multi-week campaign; this is ≥ two orders beyond it. The single-member variant
(one roving core, budget 10−k, disjunction over its cells) is A58's successor route 1
("meets-box primitive, pair version") and is campaign-scale per class as well. Not executable
inside any current budget; and the decisive objection is mathematical, not just cost: with only
per-cell hypotheses the argument decouples again (§3) unless the cell tree is deep enough to
couple the crowd to the global budget — which is what the LP below does directly, without a tree.

## 5 [S + spec] Route (b′): the boosted-kill LP — the sound merged form of (a)+(b)

The coupling the counting argument lacks is exactly an LP with per-placement right-hand side.

**The object.** For class S at certified side s″, atoms/weights μ (Σw = W), boost β > 0, and
the widened boxes B̃_i (the s″-slot box widened by ε_box = (λ_max−1)·(5/2 + 1/2), so that
side-m̃ incidences survive the Δ_λ dilation — same bookkeeping direction as Lemma B-NO's
B.2″ widening):

>   μ(Q) ≥ 1 + β·m(Q) for every pin-core-free placement Q ⊆ [0,s″]²,
>   where m(Q) = #{i : int Q ∩ int B̃_i ≠ ∅}.

**Kill condition.** W < (11 − k) + 2mβ ⟹ no teleport-stuck packing with skeleton-class S at
any side m̃ in the slack shell of s″ (Corollary B′'s shell; the slack-core grid extends to the
window as for every other fixed-side kill). *Proof sketch:* dilate the stuck packing by
λ = s″/m̃ (Lemma B: strictly disjoint, pins contain the slack cores with margin, atoms add over
the 11 − k non-owners); each non-simple square keeps its incidences against the widened boxes
(a witness point p ∈ int Q ∩ int B_i^(m̃) maps to λp ∈ int Δ_λQ ∩ λ·int B_i^(m̃) ⊆ int B̃_i);
H10-I gives Σ_q μ(Δ_λQ_q) ≥ (11−k) + β·I ≥ (11−k) + 2mβ > W. Contradiction. ∎

**Verification uses ONLY the frozen verifier** — no new trusted code. The per-placement RHS is
certified as L+1 cold `verify_case.py` invocations on ONE atom list:
* run 0: cores = slack pin cores, no nofams, strict-margin 0 (μ ≥ 1 everywhere core-free);
* run ℓ (1…L): same atoms and cores, strict-margin ℓβ, nofams Z_ℓ with
  Z_ℓ ⊆ {(c,t) : m(Q) ≤ ℓ−1} (conservative rectangle×t-interval under-approximations of the
  low-incidence region; under-exemption only raises the LP cost, never unsoundness);
* the level cap L: m(Q) ≤ L must hold for every placement — provable by pairwise box-interior
  distances (two boxes with interior distance ≥ √2 = the unit-square diameter cannot both be
  met; e.g. the offset-2 pair BL(2,0)/BL(0,2) is exactly at √2 — the strict-interior form
  excludes it). For corners4's 8-box set the pairwise graph has clique number 4 (bent chains
  such as {BL(0,1), BL(1,0), BR(1,0), TL(0,1)} are pairwise below √2 at s ≤ s0), so L = 4
  suffices; whether any placement actually realises m = 4 is not needed for soundness.
* budget-field bookkeeping: runs are emitted with an n-override so the (P1) gate does not
  fire; only the (P2) clause and the exact recorded total are consumed, per the composition
  lemma above. β = 0 recovers the plain kill; boosted kills do NOT climb (per-class only).

**The decision criterion (both directions).**
* *Death witness [T]:* if 11 − k pairwise-disjoint (as closed sets) pin-clear squares exist at
  s″ with total widened-box incidence I ≥ 2m, then every certifiable W is ≥ (11−k) + 2mβ
  (the family is a dual witness: μ(q) ≥ 1 + βm_q sums against disjointness) — the boosted
  route is dead for that class, decisively, and the residue is contact-level (A58-G2/FJ).
* *Kill hope:* if the maximal incidence I_max of such families is < 2m, the integral
  obstruction vanishes and the (fractional) LP decides; the gap 2m − I_max is the room.
* The load table of §2 says where to look: **corners4 needs I = 16 from 7 squares against a
  pairwise clique cap of 3 (≥ 2 squares must triple), and k4_08/k4_11 need exact saturation
  I = 14 = 2·7** — precisely the regime the canary shows is knife-edge (Trump saturates 2.00
  with zero slack, and A58 found his third-meeter margins to be exact-flush, margin 0).

## 6 [T] Route (c), upward absorption: DEAD at the roots, absorbed elsewhere

A stuck packing cannot be pushed into a killed class: the occupancy matrix (a) shows the open
low-k classes are CLOSED under adjoining clear-corner roots (every root-superset is open — K1
then blocks any certificate for it), so the K1-style climb has no killed target at any root;
and the exchange move to a root is exactly what stuckness forbids (CC-2 extracted its full
content already). At deeper slots the 11 cert-backed CC-3 rows are occupancy statements of the
same shape as H10-I rows and are absorbed into §5's revenue (extra boxes, stuckness-free, at
s0 pending A56/U-O3-style window instantiation). Nothing else climbs. Route closed.

## 7 Execution state (A65) and the exact residue

* Route (a) closed [§3], route (b)-as-scoped closed on cost with the decoupling objection
  [§4], route (c) closed [§6]. Route (b′) is THE surviving executable form.
* Death-witness search (max-I disjoint families, exact-verified) and the corners4/k4_08/k4_11
  verdicts: `attempts/A65-low-k-closure/results/crowdfam.json` — see §8.
* Residue after A65, named exactly: (i) per-class boosted-LP verdicts not yet run at
  certification strength; (ii) classes with a saturating death family are beyond ALL
  measure-pricing on pins + crowd occupancy — their exclusion requires the contact/FJ layer
  (CC-4 persistence made into rows: A58-G2, hard node A50-G1) or the pair-conditioned
  primitive (A58 route 1); (iii) window form: the boosted kills inherit the slack-core
  grid/parametric obligation shared with every fixed-side certificate (B.3/B.4).

## 8 [M] Search + pilot results (A65 runs), and the closing synthesis

**Death-witness search (integral side; Opus chore, exact-verified at denominator 10⁸;
`results/crowdfam.json`, `logs/crowdfam.log`).** NO protected class saturates its revenue
threshold: best exactly-verified incidences I vs required R —
k4_08: 13/14, k4_11: 13/14, k4_03: 9/10 (each short by ONE, with the deficient box a clear
corner root or its analogue); k3_05: 12/14, k3_02: 10/12, k2_01: 11/12, k1_00: 8/10,
k0_00: 5/8; corners4: NO feasible pins+7-family configuration found at s0 at all (its blind
search failed at min-gap −2.5e-2, and a template side-study reached feasibility only near
side 4.0). Structural reading: pins + family = 11 pairwise-disjoint unit squares at s0, i.e.
a near-optimal packing configuration — the searches confirm the only realisable families are
TRUMP-IMAGE PERTURBATIONS, whose incidence profiles on every class's box set fall short.
Caveats, stated honestly: search maxima are evidence, not proofs (A55 K5 calibration: search
machinery undercounts by ~1 even on known-alive nodes), and the corners4 infeasibility signal
is from a weak blind search — but the direction is uniform across 9 classes and two methods.

**Boosted-LP pilots (fractional side; the two A65 LP slots, `code/boostlp.py`,
`results/boost_k4_13.json`, `boost_k4_08.json`; bonus function unit-tested including the
overlapping-box subtlety at s < 4).** Full scans β ∈ {0, 1/4, 1/2, 1} (restricted LP values —
lower bounds on the true τ, so every "no kill" line is a refutation):

| class | τ(0) | τ(1/4) vs thr | τ(1/2) vs thr | τ(1) vs thr | measured law |
|---|---|---|---|---|---|
| corners4 | 7.2545 | 12.58 > 11.0 | 18.00 > 15.0 | 29.00 > 23.0 | τ(β) = τ(0)·(1 + 3.00·β) |
| k4_08 | 7.000000 | 11.14 > 10.5 | 15.58 > 14.0 | 24.68 > 21.0 | τ(β) ≈ τ(0)·(1 + 2.53·β) |

k4_08's τ(0) = 7.000000 exactly is the τ* = k alive pattern (canary-coherent with K2). The
law exposes the mechanism precisely: **τ_boost(β) = τ(0)·(1 + m̄·β)** with m̄ the
dual-average incidence — the entire fractional dual mass rides at the per-square cap
(m̄ = 3.00 exactly on corners4; 2.53 on k4_08), while a kill needs m̄ < 2m/N (2.29, 2.00
respectively). The margins grow LINEARLY in β; both classes are dead at every β. (A grid
scan finds m = 4 placements for corners4's boxes, e.g. an axis square at (1.38, 1.38) — but
every such placement penetrates a pin by ~0.12 and is exempt, so the pin filter caps the
dual at m̄ = 3, consistent with the §5 hand analysis.) The mechanism is visible and universal: fractional
duals put weight ≈ N on placements meeting L_eff ≈ 3 boxes at the box-cluster junctions,
unconstrained by integral disjointness, so the boost costs ≈ N·L_eff·β against revenue 2mβ,
and 2m ≤ N·L_eff with slack ≥ 3 in EVERY protected class (clique table
`results/clique_caps.json`; k0_00: 8 vs 11, corners4: 16 vs 21).

**Verdict (T2).** H10-stuck is very likely TRUE with integral margin ≥ 1 incidence in every
class — but it is UNREACHABLE by single-square measure certificates in every form: plain
(K1), decoupled crowd-priced (§3, ties exactly), or boosted/coupled (§5, fractional slope
gap ≥ 3 units, measured at the two hardest classes). The integral/fractional gap that
K1-protects these classes against pin certificates reappears, quantified, at every boost
level. **The forced 2-crowds pay only 2 per box while fractional duals collect L_eff ≈ 3 —
the crowd's value is PAIRWISE (two DISTINCT disjoint squares), which a single-square measure
cannot monetise.**

**Exact residue (the successor, in order of leverage).**
1. **Pair certificates** (A58-G3's "pair version", now with a quantified necessity proof):
   a measure on DISJOINT PLACEMENT PAIRS with μ₂(Q₁,Q₂) ≥ 1 for pairs both meeting a box,
   priced against the forced per-box 2-crowds. This is the cheapest formalism that sees what
   the single-square LP provably cannot; cost = a new verifier concept (C3-scale trust
   investment) + pair-space LP.
2. **corners4 direct integral infeasibility**: the search signal suggests NO 11-packing at
   s0 has four axis-aligned corner squares (channels of width s−2 = 1.877 < 2 = s(2)-bound
   between adjacent pins); a direct combinatorial proof would delete the only load-2.29
   class outright. Candidate for a short dedicated attempt.
3. **Integral conditioning** (A60-style zone trees branching on crowd cells) — sound but
   campaign-scale per class (§4); and the **contact/FJ cascade** (A58-G2, hard node A50-G1).

**Canary.** Trump survives every statement here: his packing realises H10-I with equality on
trump5 (§2), his class is not in the protected set, the boosted-kill refutations REPRODUCE
his aliveness (τ(0) = 7.000000 at k4_08 is his own witness), and the searches identify the
feasible families as his perturbations. At no point does any argument bind trump5 itself.
