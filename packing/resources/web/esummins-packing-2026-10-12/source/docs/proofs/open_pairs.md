# OPEN PAIRS — the miss-O test FACTORS (corner PAIR of two × wall NOTCH of two, 4 parameters each, tilts independent); WEDGE-NOTCH in closed form; the common-tilt exchange is P2′ again; non-ADJ = a wider shift, ROOM ≤ 1 fails there as a bare-ring statement; the slab: margin law measured, two of three mixed patterns engine-certifiable, the all-near-flat cube of + + + − / + − + − is a first-order (∝ ε) obligation — A263, 2026-09-21/22

The ROOM / certificate leftovers of A259–A261 (`normal_room.md`, `locked_wall.md`, `box_meeters.md`): (O3) LOCK-TILT —
open pairs whose two touchers have different tilts (A260 priced the coupled certificate at ≈ 50 CPU-h per open wall,
> 10³ for two); (O4) hybrid rings that are not all-ADJ; (R2) the tilt slab (0, 0.703°) of the window exclusions.
Tags [T] proved, [T-computed] box-valid certificate with its own verifier, [M] measured, [C] conjecture, [F] false
(witness).  Code `attempts/A263-open-pairs/code/` (`geo263`, `fact263`, `notch263`, `cert263` + `bench263` +
`verify263`, `tilt263`, `slab263`, `slabjobs263`, `pages263`, `run263.sh`; A259 / A260 / A261 code imported, never
edited); results, certs, logs beside it; pages `docs/residue_map/campaigns/A263-open-pairs/`; Lean
`Statements/Open/OpenPairs.lean`.  Notation as A260: corner BR; floor = wall k−1 with START toucher s₁ (a, φ₁) and END
toucher W (b, φ_W), shift e = δ_W − (a + sec φ₁) (any sign when φ_W ≠ φ₁); right wall = wall k with S′ (a′, φ₁′),
W′ (e′, φ_W′); O = (s/2, s/2); Q a free square, centre q, tilt ψ ∈ [−45°, 45°), u, v its edge directions.

## 0. Verdict

> **(a) [T] FACTORISATION.**  A free square missing O violates, at one of the four corners, ONE of three statements
> that each see TWO squares and FOUR parameters (s eliminated as in A259 §2.3):  **P2**(b, φ_W; a′, φ₁′) — the corner
> pair W, S′ with the miss-vertex over W's RIGHT region or S′'s LEFT region;  **WE**(b, φ_W; e, φ₁) — the floor's own
> pair s₁, W with the miss-vertex NOT over W's right region;  **WS**(a′, φ₁′; e′, φ_W′) — the right wall's pair.
> The coupling the brief feared is real but tiny and it is NOT a fifth parameter: it is the PRINCIPAL NORMAL
> (§2.2) — without it P2 is [F] (a 44° square hugging the right wall where the dropped W′ stood misses O "to the floor"
> by +0.03, `fact263_rows_v0.jsonl`); with it, [M] sound on all 82 test rings × 4 corners (36 adversary rings with
> independent tilts, the 46 corpus rings), loss ≤ 0.11 in margin, every factor still < 0 (max −0.0654 / −0.0051).
> **Certificates launched** (`run263.sh chain`, own verifier `verify263`, benchmark 0.025–0.045 s per box, all
> benchmark boxes certify at radius (0.02, 0.57°)): P2 ≈ 10–20 s per 5° × 5° cell (≈ 0.4 CPU-h), WS 3–65 s per cell
> (≈ 1 CPU-h), WE 30–70 s at low tilts, > 20 min at 25°–30° (≈ 5–15 CPU-h) — against A260's 50 CPU-h for ONE open
> wall and > 10³ for two: **LOCK-TILT is a 4-parameter job per factor, three factors in total, for any number of open
> walls.**  **(a′) [T] WEDGE-NOTCH** (§1): the open notch between s₁ (φ₁) and W (φ_W ≠ φ₁) in closed form, both the
> least DEPTH and the least MISS functional, as the minimum of ≤ 12 explicit vertex values of a 2-variable LP; checked
> against exact centre sets on 1 032 (φ₁, φ_W, γ, ψ) to 3·10⁻¹⁴, 0 violations of the principal lower bounds.
> **(b) [T] the common-tilt exchange is P2′ again** (§4): W → T_e at s₁'s tilt raises Φ₂ (a row of two) whenever
> M(T_e) ⊆ {W}, so in the maximiser every unequal-tilt open pair is HELD by a free square in every such cell; [M] on
> all 36 adversary rings the RING never blocks the exchange (143 of 144 unequal-tilt walls have a ring-free
> target interval; the exception has |Δφ| = 0.02°): **unequal tilts survive only as locks, and (a) certifies their
> room without caring about the tilt difference.**  No new potential term is needed: Φ₂ already counts common-tilt rows.
> **(c) NON-ADJ** (§3): [T] a non-served far slot needs a FREE third meeter (the family {slot, adjacent box}); the
> hybrid corner PAIR and (a) do not use ADJ — but ADJ was the certificates' DOMAIN: without it the shift reaches
> e ≤ 1.169 (from the corner forms, `[M]` on a 450² tilt grid; ≤ 0.349 with ADJ), and **ROOM ≤ 1 is [F] as a bare-ring
> statement for e ≳ 1 + w(φ₁) − sec φ₁** (a unit cell touching the wall fits in the gap; drawn).  The non-ADJ
> certificates (P2n, WEn, WSn with e ≤ 1.2) are queued after the ADJ ones and will report OPEN leaves where the
> statement fails; there P1 on the gap cells must take over (§3.3, [C]).  **(d) THE SLAB** (§5): [M] the LP margin of
> A261's engine near a flat wall: for + + − − it is ≥ 0.061 everywhere (a trivial job); for + + + − and + − + − it stays
> ≥ 5·10⁻⁴ as long as ONE wall is ≥ 0.5° and is ∝ ε in the all-near-flat cube (minimiser: b_w = 1, a_w = s − 3 — the
> flat pinwheel of dominoes, feasible in the CLOSED relaxation at every s ∈ [3, 4]; A261 §3.2 right there, wrong as
> a statement about single near-flat walls).  So the slab is 494 A261-engine jobs (§5.2, launched: at least one wall
> ≥ 0.703° — priced 1–10⁵ leaves each, 2·10⁷ for the boxes adjacent to the cube) plus **two cubes (0, 0.703°)⁴ for
> + + + − and + − + − that no box certificate reaches**: the first-order lemma of §5.3 ([T] mechanism: a near-flat
> MIXED corner forces b ≥ 1 + α(1 − a) − O(ε²) — strictly more than 1 unless a ≥ 1 − O(ε); remainder constants
> not certified: [C]).  The brief's "3.9347 − Cφ" is the wrong limit: the near-flat mixed ring tends to the domino
> pinwheel at ANY side, and the exactly-flat type-F ring (3.9347) is a different structure.
> **ROOM now**: §6.  k0_00 unchanged.

## 1. WEDGE-NOTCH  [T] (`notch263.py` [T-computed check])

Notch frame: origin A_W = W's left vertex, x along the wall, y = depth − cos φ_W.  **γ** := the horizontal distance
from A_W to s₁'s right-edge line = e + (cos φ_W − cos φ₁) tan φ₁ ≥ 0 (s₁, W interior-disjoint ⟺ γ ≥ 0 when φ_W ≥ φ₁;
at common tilt γ = e).  s₁'s top vertex T₁ = (−γ − t sin φ₁, t cos φ₁), t = (cos φ₁ + sin φ₁ − cos φ_W)/cos φ₁.  Above
the height of s₁'s right vertex, s₁ = the cone {(x − T₁)·u₁ ≤ 0, (x − T₁)·v₁ ≤ 0} and W = {x·u_W ≥ 0, x·v_W ≤ 0}.
A unit square Q = P + [0,1]u + [0,1]v (P its lowest vertex, ψ ∈ [0°, 45°]) is interior-disjoint from a cone iff one
SAT option per cone holds — for W: (Ra) P·v_W ≥ max(0, sin(φ_W − ψ)) or (Rb, ψ ≥ φ_W) P·v ≥ 0; for s₁: (La)
(P − T₁)·u₁ ≥ max(0, sin(ψ − φ₁)), (Lb, ψ ≥ φ₁) (P − T₁)·u ≥ 0, (Lc) (P − T₁)·v₁ ≥ max(0, sin(φ₁ − ψ)), (Ld, ψ ≤ φ₁)
(P − T₁)·v ≥ 0.  On the NOTCH region {P·u_W ≤ 0, (P − T₁)·u₁ ≥ 0} every option pair is a 2-variable LP, so
**the least depth and the least miss functional (P − A_W)·v are minima of ≤ 12 explicit vertex values** (`closed`).
Principal branch, ψ ≤ φ_W (Ra ∧ La active): with k₁ = max(0, sin(ψ − φ₁)),
  miss ≥ sin(φ_W − ψ) [cos(ψ − φ₁) + k₁ − γ cos φ₁] / cos(φ_W − φ₁),
  depth − cos φ_W ≥ [cos φ₁ sin(φ_W − ψ) + sin φ_W (k₁ − γ cos φ₁)] / cos(φ_W − φ₁);
ψ ≥ φ_W: miss ≥ 0 (the APEX bound, s₁-free) and depth − cos φ_W ≥ sin ψ (k₁ − γ cos φ₁)/cos(ψ − φ₁).  At common tilt
and ψ = φ these give depth = cos φ (1 − e sin φ) — A260's OPEN-TOOTH (Lean `wedge_depth_common`).  [T-computed]
`notch263`: closed = exact centre-set minimum on 7 × 7 tilts × 4 γ × 12 ψ (1 032 admissible cases) to 3.5·10⁻¹⁴
(depth 3.5·10⁻¹⁴); 0 violations of the principal lower bounds.  It is a ONE-WALL lemma (3 parameters γ, φ₁, φ_W + ψ).

## 2. The factorisation  [T]; [M] tests

**2.1 Regions.**  For the wall-nearest vertex P of Q (bottom-left vertex for ψ ≥ 0, bottom-right for ψ < 0; ANY
consistent choice works): RIGHT(W) := {(P − A_W)·u_W ≥ 0} (P beyond W's left-vertex line), LEFT(S′) :=
{(P′ − T₁′)·u₁′ ≤ 0} (P′ before S′'s top vertex along the wall), P′ the right-wall-nearest vertex.
**2.2 PRINCIPAL NORMAL.**  Q misses O ⟹ (q − O)·n ≥ ½ for n ∈ {±u, ±v}; take the n with the LARGEST value.  A259's
rotation puts n at the floor (case (i), n = −v, q_x ≥ s/2) or at the right wall (case (ii), n = u, q_y ≤ s/2), and now
(i) carries (q − O)·(−v − u) ≥ 0, (ii) carries (q − O)·(u + v) ≥ 0 (Lean `principal_normal`).  In the corner frame
(O = (−s/2, s/2)) the (i)-clip equals q·(−v−u) + s sin ψ and the (ii)-clip q·(u+v) − s sin ψ, so **each relaxes as s
grows on the half of the tilt range where it is imposed** (ψ ≥ 0 for (i), ψ ≤ 0 for (ii); Lean `clip_mono`) — the
certificate at s_max implies every s ≤ s_max exactly as `corner_frame_mono`.
**2.3 The cover.**  (i) ∧ P ∈ RIGHT(W) ⟹ P2(i) (drop s₁, W′: the free set only grows); (i) ∧ P ∉ RIGHT(W) ⟹ WE(i)
(drop S′, W′); (ii) ∧ P′ ∈ LEFT(S′) ⟹ P2(ii); (ii) ∧ P′ ∉ LEFT(S′) ⟹ WS(ii).  Hence
**FULL(8 parameters) ⟸ P2 ∧ WE ∧ WS, three statements of 4 parameters each, no parameter shared across a factor.**
The brief's fear ("the miss-O test couples the notch to a corner") materialises only in the principal-normal clip —
one inequality that is intrinsic to Q, not a parameter of the wall.
**2.4 [M] tests** (`fact263 --mode rows`, `results/fact263_rows.jsonl`): 36 A260 adversary rings (independent tilts,
|Δφ| ≤ 7.2°, e ≤ 0.19, ADJ and non-ADJ) + 46 corpus rings, 4 corners each: max(P2, WE, WS) ≥ FULL on 328/328
corners (soundness); adversary: FULL −0.0654, P2 −0.0654, WE −0.0654, WS −0.0666; corpus: −0.0051 (s = 3.99) on all;
loss max(factors) − FULL ≤ 0.114 (adversary), ≤ 0.008 (corpus).  Without the clip: P2 up to +0.030 on 52 corners [F].
**2.5 The certificates** (`cert263.py`, A259's method: CORES over the box, KERNEL per 1° tilt bin, the region and
clip half-planes RELAXED by their variation (0.7072·Δ + r_pos + 2 r_φ + 5.5 r_φ; 1.4143·Δ·5.5), linear forms bounded
by value_mid + Δ|q − O|; PRUNE only off-domain or on core overlap; PLUG for a′ > 0.604 in P2; s_max = 3.8771,
s_min = 3.82; adaptive bisection, tilt radians weighted ×2, depth ≤ 26).  Own verifier `verify263`: independent
0.4° bins with 0 as an edge, exact dyadic tiling per cell, OPEN listed never counted.  **Benchmark** (`bench263`,
36 random feasible boxes per family): 0.045 / 0.025 / 0.026 s per box (P2 / WE / WS), 100 % CERT at radius
(0.02, 0.57°) already, worst certified margins −0.027 / −0.013 / −0.028.  Root cells (5° × 5°): P2 10–18 s,
WS 3 s (2,3), 7 s (0,0), 65 s (5,5), WE 31 s (0,0), 72 s (2,3), cell (5,5) not finished in 21 min at depth 22.
Launched detached: P2 → WS → WE → verifier → the slab jobs → P2n, WSn, WEn → the margin scan → adversaries.

## 3. Non-ADJ  (c)

**3.1 [T] The count.**  ADJ = every toucher reaches its far slot (s₁: a + w(φ₁) > s − 2; W: δ_W < 2).  If s₁ does not
reach the floor's slot R = [s−2, s−1] × [0,1], the family Π = {R, box BR} (interior-disjoint) has ring meeters
{W, S′} only (SAME-WALL / BOX-MEETERS: the box has exactly these two; another wall's toucher cannot reach R), so
FAMILY-STUCK (|M(Π)| > |Π|) forces a FREE square into R: **every non-ADJ wall carries a free square at depth < 1 over its
unserved slot** (Lean `nonadj_free_meeter`).  (The next wall's START square meets R by a sliver whenever
a′ + cos φ′ tan(φ′/2) < 1 — it is already in M(Π) through the box, so the count is unchanged.)
**3.2 What the room certificate needs.**  The hybrid corner PAIR (A260 §3.1) and the factors of §2 use only the box
conditions b, a′ < 1; ADJ entered only as the certificates' domain (`outside_domain`).  Dropping it enlarges the
shift range: from the corner forms with the neighbours' offsets ≤ 1, a ≥ a_min(φ₁, β), b ≥ b_min(α, φ_W), hence
e ≤ s − sec φ₁ − w(φ_W) − a_min − b_min: **sup 1.169 (near-flat tilts) vs 0.349 with ADJ** [M, 450² grid;
a_min → 0 as φ₁ → 0].  But for e ≥ 1 + w(φ₁) − sec φ₁ (1.19 at 14.5°, → 1 as φ₁ → 0) a unit cell touching the wall fits
between s₁ and W (the gap has width e at common tilt), so a free square can sit at the floor and miss O: **ROOM ≤ 1 is
[F] on the wide part of the non-ADJ family as a statement about the eight squares** (page `nonadj_gap.svg`).
**3.3 What kills it there [C].**  Such a square F, or the lowest free square in the gap, has a straight drop to a
wall-touching cell C_F blocked by nothing (the gap's walls are parallel at common tilt; a wedge otherwise) — P1
(TOUCH-CELL) then moves F onto C_F and raises Φ₁.  Two free squares in a gap of width ≤ 1.17 both reaching depth < 1
have tilts ≤ 9.9° and vertical overlap ≤ 0.2, so the lower one is within 0.2 of the floor with a free drop.  Making
this a lemma needs the wedge case (φ_W ≠ φ₁) and the interaction with S′ at the gap's far end; not done.  The
non-ADJ certificates in the chain will mark the region where ROOM fails as OPEN (grey), which is where §3.3 is needed.

## 4. The common-tilt exchange  (b)  [T] + [M] (`tilt263.py`)

**(E6) [T].**  T_e := a unit cell touching wall k at s₁'s tilt (any offset τ).  If M(T_e) ⊆ {W} then W → T_e is a
packing (Lemma CELLS, |Π| = 1) with Φ₁ unchanged and, when T_e = s₁ + sec φ₁ e, a ROW (s₁, T_e): Φ₂ rises — this IS
A258's (E1)/P2 with W the meeter.  If M(T_e) = {W, F}, F free, and F has a cell F′ disjoint from T_e and everything
but W, F: (E3)/P2′.  So **in the maximiser an open pair of unequal tilts is HELD** (A260 §1.2: (P ∖ {W, F}) ∪ {T}
saturated) — no new potential is needed, Φ₂ counts common-tilt rows already.  The other case (|M(T_e)| ≥ 2 for every
ring-free τ, in both directions W → s₁'s tilt and s₁ → W's tilt) forces free squares into every such cell: locks.
**[M]** 36 adversary rings × 4 walls with |Δφ| > 0 (up to 12.4°): the RING alone leaves a ring-free τ-interval on 143
of 144 walls (the exception: |Δφ| = 0.02°); the corpus has no unequal-tilt lock (43/43 corpus locks are common-tilt,
A260) — the two A255 controls (Δφ up to 12.4°, no poker) exchange freely.  **Verdict:** unequal tilts are never forced
by the ring; they exist only when held by a free square, whose room (a) bounds.  LOCK-TILT as an exchange lemma adds
nothing to P2′; LOCK-TILT as a certificate is now 3 × 4 parameters.

## 5. The slab  (d)  [M] + [T-computed launched] + [C]

**5.1 What is certified and what the slab is.**  A261's LP certificates cover per-wall tilts in [0.703°, 45°] (M1–M3,
35 row-of-three jobs) and EXACTLY flat walls (F0, F02).  The slab is the rest: some wall in (0, 0.703°).  The one-sense
family lives there (A261 [F] of its own reading) and its ROOM is bounded by A259 / A260 on all tilts, so the slab
matters only for the MIXED and ROW-OF-THREE patterns.
**5.2 Margin law [M]** (`slab263.py`, `results/slab263.jsonl`; the LP's least τ* over all admissible form choices, the
near-flat wall's ε-forms admissible): + + − −: ≥ 0.061 at every near-flat tilt vector probed; + + + − and + − + −:
0.0007 with one wall at ε ∈ {0.703°, …, 0.003°} and the others optimised (quick scan; ≥ 0.00055 with two walls at
0.01°), independent of ε and equal to the exactly-flat limit; **but ∝ ε in the all-near-flat cube**: τ*(ε, ε, ε, ε) =
0.00079, 0.00039, 0.00011, 0.00003, 0.00001 at ε = 0.7°, 0.35°, 0.1°, 0.03°, 0.01°, minimiser a_w = s − 3, b_w = 1 at
s = 3.8771 — the flat DOMINO PINWHEEL, feasible in the closed relaxation at every side in [3, 4].  So a box certificate
needs h ∝ ε only in that cube (A261 §3.2's law, located).  **Slab jobs** (`slabjobs263.py`, A261's engine imported,
its own certs directory): the 15 boxes [0, 0.703°]^S × [0.703°, 45°]^rest per pattern, 494 jobs after symmetry;
Monte-Carlo price (`price`): SM2_* ≈ 1–10³ leaves, SM3_0 1.6·10³, SM1_0 3.4·10⁴, SM1_3 9·10⁴, SR* 10–300,
SM1_013 (three walls in the slab beside the cube) ≈ 3·10⁷ (heavy tail), SM1_0123 ≈ 1.4·10⁷ (divergent: the cube).
Launched in the chain with a 1.5 h cap per job (PAUSED jobs are resumable); the two cubes SM1_0123, SM3_0123 last.
**5.3 The cube: the first-order lemma [T-mechanism, C-constants].**  A261's closed forms at a MIXED corner (σ_A = +,
σ_B = −), tilts α, β → 0: the START square's form reads b ≥ 1 + α(1 − a) + O(ε²) and the END square's a ≥ 1 + β(1 − b)
+ O(ε²).  With a, b ≤ 1 one of the two offsets must be ≥ 1 − O(ε) at every mixed corner; the one-sense corners give
b ≥ 1 − aα + O(ε²); the ring identity a_w + b_w = s − sec φ_w − w(φ_w) = s − 2 − O(ε) then forces, at the mixed
corner whose offset is the START a ≈ s − 3, the END offset b ≥ 1 + ε(4 − s) − O(ε²) > 1: infeasible with margin
ε(4 − s)/(normalisation) — exactly the measured law.  What is missing for [T]: the O(ε²) remainders of the four forms
on [0, 0.703°]⁴ as explicit constants and the case split over which offset each mixed corner pushes to 1.  It is a
finite algebraic statement (8 offsets, 4 tilts) and the natural next Lean target; a box certificate cannot do it.
**5.4 What the brief had in mind.**  "A row of tilt φ → 0 is a flat row up to O(φ): cost 3.9347 − Cφ" is [F] as the
mechanism: the type-F ring (3.9347) has its flat wall's forms DROPPED (a flat square owns no axis) and is one
structure; the near-flat mixed ring approaches the domino pinwheel at ANY side and is killed by the STRICT box
condition at first order.  No Lipschitz constant on 3.9347 closes the slab.

## 6. Plainly — ROOM and the window exclusions now

| family | ROOM ≤ 1 (every free square ∋ O) | status |
|---|---|---|
| normal D′ | A259 tree + A260 layer | [T-computed] (A259's index complete: check `verify259.json`) |
| hybrid, common tilt per wall, all-ADJ, e ≤ ½ | A260 hybA / hybB / hybAB | [T-computed] hybA 81/81, hybB 81/81; hybAB 8/81 at A260's exit — its chain continues |
| hybrid, INDEPENDENT tilts, all-ADJ, e ≤ ½ | **this note: P2 ∧ WE ∧ WS** | [T] reduction; [T-computed] when `run263.sh chain` ends with 0 OPEN and `verify263_adj.json` bad = 0 (P2 cells 10–18 s each, running at exit) |
| hybrid, not all-ADJ (e ≤ 1.2) | P2n ∧ WEn ∧ WSn, queued | [F] on the wide part (§3.2); [C] §3.3 there |
| window exclusions, tilts ≥ 0.703° or exactly flat | A261 | [T-computed] (M1 running at A261's exit) |
| slab, at least one wall ≥ 0.703° | 492 slab jobs, queued after WE | [T-computed] as they finish + verify |
| slab, all four walls < 0.703°, + + + − and + − + − | §5.3 | [C] (mechanism [T]) |
Chain: packing at s ⟹ normal form ⟹ [C NO-JAM(11), A262] hybrid normal ring ⟹ [this note + A259/A260] every free
square ∋ O ⟹ 8 + 1 < 11 (Lean `openPairs_excludes` from `factor_pierce`).  **Remaining, exactly:** (O1) the three
ADJ factor chains + verifier; (O2) A260's hybAB and A259's tree to completion (their own chains); (O3) non-ADJ: the
OPEN region of P2n/WEn/WSn + the gap lemma §3.3; (O4) the slab jobs to completion + the two cubes (§5.3); (O5)
NO-JAM(11) (A262); (O6) the stretch (ŝ, 4); (O7) Lean: `factor_pierce`, `slab_cube` are axioms.

## 7. What the brief had wrong

1. "3-parameter one-wall lemma (e, φ₁, φ_W, ψ)": right for WEDGE-NOTCH; but the certificate factor that uses it (WE)
   still needs b — where the pair stands relative to O — so the factors are 4 + 4 + 4, not 4 + 3.  2. The coupling is
   the principal normal, not a parameter; without it the two-square corner statement is false.  3. "T_e met by W,
   perhaps the locker F and wall w+1's start square": the ring never meets T_e on the adversary rows; only F does —
   (b) is P2′.  4. "how many wall slots can one square containing O serve": the count is not the issue — ROOM itself
   fails on wide non-ADJ gaps.  5. "3.9347 − Cφ": wrong limit (§5.4); and the slab is a problem only for the mixed
   and row-of-three patterns, and only in the all-near-flat cube for + + + −, + − + −.
