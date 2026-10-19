# H1 by contact structure: the k0 FJ-supporting census and its price — A88, 2026-09-03

Target (A88 BRIEF, PI direction after A87): H1(ŝ) — "no k0 Fritz-John point with σ ≤ ŝ" — is,
by DF-K0 (`drain_flow_k0.md`), the whole k0_00 obligation in MinForm. A87 measured H1 as a
configuration-space cover DEAD (Gordan never fires on a σ-feasible cell). This file prices H1
BY CONTACT STRUCTURE: an FJ point carries a support structure H whose multipliers it must be
able to balance, so H1 is a statement about a FINITE set of FJ-supporting structures, each
excluded by a certificate local to its loaded core. T1 states the contact-count floor and the
k0 structural filters (theorems); T2 measures the census with a rigorous bracket
(`attempts/A88-fj-census/notes/census_report.md`); T3 measures the per-structure cost
distribution — a cheap triage tier on a uniform census sample, then the Krawczyk/Farkas tier on
survivors (`notes/pilot_report.md`). Labels: [T] proved, [S] routine given cited items,
[M] measured, [X] extrapolated, [F] finding, [C] open. Conventions: `structure_lemmas.md`
(Fact 0, L1–L7), A44 `notes/theory.md` (L8–L11, C*, C-rep; ACTIVE vs SUPPORT graph, Fact-0 row
count m = E + F), `drain_lemma.md` v3 (D1, D3′, Gordan form T3(c1)).

## 0. Verdict

> **The k0 FJ-supporting census is ~10³⁶ decorated structures (≥ 10¹² rigorously) and the
> FJ side adds no bulk filter; per-structure exclusion is cheap (0.78 s) and the route loses
> on the count alone — break-even 3·10⁷ structures. Full statement in §7; k0_00 stays on
> A85's tree.**

## 1. Setting and the census object

Configurations z = (c_i, θ_i)_{i≤11}, s; NLP(S) as in `drain_flow_k0.md` §1; FJ certificate
(λ₀, λ) ≥ 0, λ₀ + Σλ = 1, λ₀∇s = Σ λ_k ∇g_k, λ_k g_k = 0. The SUPPORT graph H of a certificate:
squares + 4 wall nodes, one edge per contact carrying a strictly positive multiplier (Fact 0:
a flush contact is ONE edge with TWO rows, a point contact one edge with one row). k_H = number
of LOADED squares (incident to an H-edge), m_H = Fact-0 rows on H, N_H = 3k_H + 1 (core
coordinates plus s), A_H the m_H × N_H Jacobian at z, d_H = dim ker A_H, σ_H = dim ker A_Hᵀ.
The other 11 − k_H squares are UNLOADED: rattlers (no contact) or squares whose contacts all
carry λ = 0. A STRUCTURE is (H, wall masks, contact-type decoration, tilt-class order): exactly
A31's Level-0 + Level-1 object on a loaded core of size k_H (`count_report.json`), which A31
counted per core WITHOUT the rattler completion (its gap G4). §2 shows that is the right unit.

## 2. [T] Theorem T1 — the FJ contact-count floor for k0

**Theorem T1.** Let z ∈ k0_00 be an FJ point of NLP(S) at side σ(z) ≤ ŝ for a consistent S,
with support structure H as above. Then:

(a) *(index identity, A44 L8)* m_H = 3k_H + 1 + σ_H − d_H. Hence the contact-count floor is
    **m_min(d_H) = 3k_H + 1 − d_H**, with equality iff the rows of H are independent; in the
    λ₀ = 0 branch (pure self-stress, A44 L9′) σ_H ≥ 1 and m_H ≥ 3k_H + 2 − d_H.

(b) *(support conditions)* If λ₀ > 0: on a binding axis some component of H joins the two
    opposite walls (L6), with ≥ 3 loaded squares (consecutive centres ≤ √2 apart, end centres
    within √2/2 of the walls, s ≥ 3.82 ⇒ k ≥ ⌈3.82/√2⌉ = 3); every loaded square has
    H-degree ≥ 2 (L1); in the non-thin branch every loaded square has row-degree ≥ 3 (L11),
    so 2E_H ≥ 3k_H + 2 and m_H ≥ 6. If λ₀ = 0: H carries a compression self-stress
    (A_Hᵀλ = 0, λ ≥ 0, λ ≠ 0). Absolute floor: **k_H ≥ 3, m_H ≥ 4** (thin 3-chain with four
    point contacts; L2 collinearity at each degree-2 square), **m_H ≥ 6 non-thin**.

(c) *(flat directions)* If λ₀ > 0 every y ∈ ker A_H has e_s·y = 0 (A44 L10): flexes of the
    support structure are s-neutral, so a positive-dimensional critical manifold through z
    is admissible and cannot be excluded by first-order data. The FJ set with support ⊆ H is
    {g_H = 0} ∩ {e_s ∈ cone(∇g_H)}; on the variety V_H = {g_H = 0} (dimension d_H where the
    rows are independent) the condition e_s ∈ rowspace(A_H) has codimension d_H, so
    GENERICALLY the FJ points of H are isolated in the core (A87 §6.4) and the critical
    manifold is the rattler space, dimension 3(11 − k_H); NON-generically (A37's valleys,
    rank 27–32) it has dimension up to d_H inside the core. Hence
      d_crit(z) ≤ d_H + 3(11 − k_H),  d_H = 3k_H + 1 + σ_H − m_H.
    **d_H is not bounded by any first- or second-order necessary condition** (A44's
    impossibility frame: independent rows, d_H ≥ 1, s|V_H strictly minimal by geometric
    stiffness is a legitimate isolated minimiser with m_H = 3k_H + 1 − d_H ≤ 3k_H). Worst
    case admitted by (a)–(c): k_H = 3, m_H = 4, d_H = 6 + σ_H, eight rattlers:
    d_crit ≤ 30. The brief's "bound d by the chain + L1 + rattlers" therefore yields ONLY the
    rattler term; the chain and L1 bound m_H from below (b), not d_H from above.

(d) *(the census-usable consequence — A44's exact split, unchanged by k0)* A structure with
    m_H < 3k_H + 1 can never be first-order rigid (rank ≤ m_H < N_H): the census splits
    EXACTLY into RIGID-POSSIBLE (χ := m_H − 3k_H − 1 ≥ 0) and FLEX-ONLY (χ ≤ −1, every
    realisation has d_H ≥ −χ). Neither branch is empty of genuine critical points (A44:
    family 31 at χ = −1). No filter of the form m_H ≥ 3k_H + c is a theorem for c > −∞
    beyond (b).

*Proof.* (a) rank–nullity on A_H and A_Hᵀ (A44 L8). (b) L6's proof (sum the x-stationarity
rows over the far-wall component; internal forces cancel) with the span count at s ≥ 3.82;
L1 and L11 as in `structure_lemmas.md` / A44. The λ₀ = 0 case is the definition. (c) L10:
λ₀e_s = A_Hᵀλ ⇒ e_s ∈ rowspace(A_H) = (ker A_H)^⊥. Dimension count: the map ζ ↦
dist(e_s, rowspace A_H(ζ)) has d_H independent components generically; A44 `theory.md`
"Why no unconditional bound below 3k+1 is forced" supplies the second-order-consistent
counterexample frame. (d) is L9 by contraposition. Nothing in (a)–(d) uses skeleton(z) = ∅:
k0 enters only through the structural filters of §3. ∎

**[F] What the PI's premise buys.** "Enough active contacts to support the multipliers" is
exactly L1 + L6 (+ L11 non-thin), i.e. A31's hard filter set; the FJ counting identity adds
the rigid/flex LABEL, not a kill. The FJ-supporting census IS A31's census summed over core
sizes, with the k0 filters below on top. (A31 measured L6 at ×1.5 and L1 at ×1.5 at k = 7;
the strong filters are metric (L5(a), ×50) and planarity (×3.3) — containment filters, as A59
diagnosed.)

## 3. [T] The k0 structural filters (usable by a census)

Throughout, k0_00 ⟺ no square is exactly a corner slot square (`drain_flow_k0.md` §1) and,
for the (S)-flagged filter, the consumer is `stratify`'s k-maximal minimiser (Lemma F-LEAF (S),
`drain_flow_k0.md` §4).

**K0-1 (slot exclusion) [T].** A square in tilt class 0 (axis-aligned) that touches two
adjacent walls touches both flush and has centre (½, ½) (or a D4 image): it is the slot
square. A tilted square touches a wall at exactly one corner (its extreme vertex in the wall
normal is unique). Wall-flush pins class 0. Hence
  k0_00 ⟺ no square has wall-degree 2 and a wall-flush edge ⟺ no square has two wall-flush
  edges ⟺ every wall-degree-2 square is tilted (two corner-on-wall rows, not four).
This is a DECORATION-level filter; at Level 0 it is inert (the all-corner decoration of any
graph satisfies it — A45's law). Consequence for row counts: a k0 corner square carries 2
wall rows where a slot square carries 4 (rank 3), so k0 structures are wall-row-POORER than
Trump-like ones (Trump: 20 wall rows; a k0 structure with N1 has ≤ 4 · 3 · 2 = 24 wall rows
only if every wall square is flush, ≤ 12 if all are tilted).

**K0-2 (clear-corner crowding, contact-graph form) [T, S-flagged].** For the k-maximal
minimiser P* (A58 Theorem A58-1 with k = |Simp| = 0, via CC-2/CC-2′): every corner box
B_c = (0,1)² (D4 images at side s) has its open interior met by ≥ 2 squares, and the four
crowds are disjoint (two corner boxes are ≥ s − 2 ≥ 1.82 > √2 apart, a unit square's
diameter). A square meeting B_c has centre in c + [½, 1 + √2/2)² and can touch only c's two
walls. Census form: ∃ an assignment of ≥ 8 of the 11 squares to the four corner zones, ≥ 2
per zone, consistent with the wall masks and with the pairwise coexistence / touching tables
on the zone-shrunk centre boxes. This is an EXISTENTIAL containment filter (A43's law:
expected near-inert); it is admissible for k0_00 only through the k-maximal selection — the
composition `s_eleven_ge_of_split` feeds `StratumKillMin` the `stratify` representative and
kills the other strata ∀-packings, so a k0 minimiser that is not k-maximal is excluded by
its k-maximal teleport image's stratum. Flag it as (S) exactly as Lemma F-LEAF does.

**K0-3 (flush-ruler cap, A45 Lemma R) [T, EXACT decoration filter, WINDOW-DEPENDENT].** A
series flush chain of k same-class squares has k ≤ s(|cos ψ| + |sin ψ|), i.e. k − 1 links
≤ s(|cos ψ| + |sin ψ|) − 1: at s ≤ s₀ length ≤ 5 (≤ 4 links), and ≤ 3 (≤ 2 links) in class 0
(upright). The cap grows with s (≤ 5 / ≤ 7 at s = 5), so it must be evaluated at the side of
the object it is applied to — the census uses s₀, an out-of-window check must use its own σ
(A88 D6 found 147 spurious kills from applying the s₀ cap at σ = 4). A45 measured its
Level-1 weight at ×1.09 (k = 11 extrapolated); A88 measured ×1.00001 (§5).

**K0-4 (A50 tilt rules) [T, inert at census level].** Near-flush exclusion (no flush-free
spanning P-chain with all tilts in (0, θ*), θ* = 1.7347°) and tilt pinning (an equal-class
P-chain's tilt lies in a finite algebraic set Θ(s)) constrain the CONTINUOUS tilt parameters
of one chain type; tilt classes are symbolic at Level 1, so the census count is unchanged.
They shrink the tilt box of a per-structure solve by ≤ 1.73/90 ≈ 2 % per class (near-flush)
or, for flush-free x-pinning chains only, to a finite menu (pinning). Not a multiplier.

Also inherited unchanged: L6 (in A31's F0), L7, N1 per-wall ≤ 3 (A43, exact).

## 4. [T] Lemma H-LOC — the exclusion unit is the loaded core

**Lemma H-LOC.** Let H be a support structure with loaded core C (k_H squares) and let B_H be
a box in the core coordinates (c_i, θ_i)_{i∈C}, s.
(F) If there is y ∈ R^{3k_H+1} with ∇s·y < 0 and ∇g_r(ζ)·y > 0 for every row r of H and every
    ζ ∈ B_H (interval-verified), then no configuration whose core lies in B_H is an FJ point of
    any consistent selection with support ⊆ H — whatever the unloaded squares do.
(K) If the row system g_H = 0 has at most one solution in B_H (Krawczyk on a square
    subsystem of rank 3k_H + 1), every FJ point with support H and core in B_H is that root,
    whose side s* decides (s* > ŝ_hi ⇒ excluded; s* ≤ ŝ_hi ⇒ a candidate, then the unloaded
    squares' feasibility is a sub-packing question).
*Proof.* An FJ certificate with support ⊆ H reads λ₀∇s = Σ_{r∈H} λ_r∇g_r with (λ₀, λ) ≥ 0
nonzero; rows outside H carry λ = 0 and involve no other coordinates in the equation. Gordan's
alternative (T3(c1), both branches: λ₀ = 0 gives Σλ_r∇g_r = 0 which is also refuted by y)
makes (F) incompatible with such a certificate. (K): a support-H FJ point satisfies g_H = 0. ∎

Consequences. (i) The certificate cost scales with the CORE dimension 3k_H + 1 and with d_H,
never with the 11 − k_H unloaded squares — the rattler term of T1(c) is free. (ii) The a-σ
leaf is weaker on a core than on a full configuration (only cores touching a far wall pin
s), so small cores are killed by (F) or not at all. (iii) For small rigid cores (K) lands on
a sub-packing problem whenever the root is below ŝ (e.g. any rigid wall-to-wall chain that
fits at side ≤ ŝ): the H-certificate is then NOT closed by Krawczyk — the remaining
11 − k_H squares must be shown not to fit, which is the k0 tree for a smaller instance.
(iv) With the rows FIXED by the structure there is no selection menu: A87's menu explosion
(2¹⁶–2³⁴ selections per cell) does not arise; whether (F) fires on fixed-structure boxes is
what the pilot measures.

## 5. [M] The census (T2) — `attempts/A88-fj-census/notes/census_report.md`, `results/census88_summary.json`

Method: A59's, lifted from S₆ to **S₁₁ × D4** (exact Burnside over cycle types with the D4
action along cycles; per-cycle-length multiset reduction; divisibility by 11!·8 asserted;
counter reproduces A31's R0/R2 at k = 3, 4 and a brute-force orbit count on the full
factorable predicate at k = 3, 4 exactly). Window [3.82, s₀]. Every figure labelled.

**5.1 Level 0, k_H = 11 (support graph + wall masks, orbits).**

| quantity | value | class |
|---|---|---|
| upper bound (factorable subset: L5(b) masks, pairwise coexistence, touching window) | **1.2746·10¹⁵** | EXACT |
| point estimate (full F0 = A31 hard set + N1 + Euler) | **9.5·10¹⁰ ± 2.5·10⁹** | MC, 2·10⁷ draws, two estimators agree to 1.8σ |
| lower bound (family P5: Hamiltonian path, masks ⊆ {∅,L,B,R,T}, all 57 232 members F0-verified) | **57 232** | EXACT |

The estimate sits inside A31's EXTRAPOLATED band (6.4·10¹⁰ / 3.4·10¹¹ / 5.0·10¹¹) — A31's
growth model is now measured, not fitted. Dominant filter at k = 11: **L4(b) planarity
(×1 380)**, then N1 (×4.25), Euler (×1.83); L5(a), A31's strongest filter at k ≤ 7, is nearly
inert at k = 11 (×1.13). K0-2 (crowding CSP): **1 493/1 493 pass — inert** (A43's law on
existential filters). Orbit-weight excess of labelled rates: +3.3 % (carried).

**5.2 Level 1 (decorations), 300 uniform Level-0 survivors × 25 000 draws.** E median 23
(Ess 16.7, Esw 6.6); tilt-feasible fraction of the raw 20^Ess·2^Esw menu median 1.5·10⁻³;
**decorations per graph median 1.3·10²¹, mean 2.0·10²⁵** (p05 10¹⁷, p95 1.2·10²⁴, max
5.4·10²⁷) — A31's extrapolated 6.5·10¹⁸ was 2.4 orders LOW. Exact (A44 branch code) vs MC agree
on the six E = 19 graphs where the exact count is affordable. Decoration-weighted pass rates:
**K0-1 0.9895, K0-3 0.99999, K0-2 1.000**. RIGID-POSSIBLE (χ ≥ 0) share: 2.1·10⁻³ of
decorations unweighted, **1.2·10⁻⁵ weighted** (9·10⁻⁶ under K0-1); FLEX-ONLY ≥ 99.79 %
(≥ 99.9988 % weighted); pooled χ mode −10.

**5.3 Composed decorated census, k_H = 11 (orbits).**

| | value | class |
|---|---|---|
| lower bound (ONE explicit F0-verified graph, Ess = 24, Esw = 3: all-corner sub-menu 8²⁴ · AO(G) = 8²⁴ · 165 888, all tilt-feasible and K0-clean by construction, ÷ |Aut| = 2) | **3.9·10²⁶** | EXACT |
| point estimate F0 / F0 + K0-1 + K0-2 + K0-3 | **1.88·10³⁶ / 1.86·10³⁶** (median-fan-out form 1.3·10³²) | MC (±½ order: heavy-tailed mean) |
| upper bound (Level-0 UB × 20²⁷·2⁸) | 4.4·10⁵² | EXACT, crude |

Ablation: F0 → +K0-1 ×0.9895 → +K0-3 ×0.99999 → +K0-2 ×1.000; dropping any one changes the
fourth digit. **The whole k0 hypothesis buys ×1.011.** Sum over k_H = 3..7 (A31 exact) =
886 774 and the k = 8..10 extrapolation ≤ 1.5·10¹⁰: k_H = 11 dominates within ~4 %.
**Dominant multiplier: the contact-type decoration fan-out (10²¹ per graph), ten orders above
the graph count** — the algebraic row set that Krawczyk/Farkas needs, not the graph.

**5.4 Canary (Trump, derived by code at tolerance 10⁻⁶ from `certs/trump11_certificate.json`;
the rounded certificate's contacts sit at residual 1.1–1.3·10⁻⁷).** 14 SS + 11 SW contacts,
per-wall 3/3/3/2, two tilt classes (0; 40.1819°). F0 passes on the active graph G and on the
support graph H; decoration tilt-feasible; K0-3 passes (ruler extent 2); **EXCLUDED by K0-1
with slot squares exactly {0, 2, 5}; INCLUDED with K0-1 dropped** (K0-2 in A58-general form:
TL corner met by squares 3 and 4, the other corners hold slot squares); rows = m = E + F = 40.
PASS 9/9.

**5.5 D6 — the 167 certified k0 FJ points (A87 polish, tol 10⁻⁶) against T1 and the census.**
T1: **0 violations of 167** — k_H ∈ {4 (99), 5 (40), 6 (11), 7 (10), 8 (2), 9 (3), 11 (2)},
m_H 7..32, L1/L3/L6 hold on every NNLS support, identity (a) holds, d_H ∈ [2, 9] never 0,
**χ ∈ [−9, −2]: zero rigid-possible** — every certified k0 critical point in the corpus is
flexible, matching the census's 1.2·10⁻⁵ rigid share. Census membership: tilt-feasible
167/167, K0-1 167/167, L5(a)/N1 0 failures (narrow and widened window), K0-3 167/167 with the
per-σ cap. Two residual alarms (o124, o154, σ = 4): L4(b) planarity fails on the ACTIVE graph
G and resolves when degenerate corner–corner kisses are removed — see G-A88-4.

**[F] G-A88-4 (vocabulary gap, inherited from A31/A43/A44).** A31's gauge-fixed 20-type
menu has no entry for a **corner–corner kiss between two SAME-class squares** (two corners of
one on the other's edge line, contact set a point): a non-flush contact was assumed to order
the two tilt classes strictly. Trump has one — the (1, 3) pair of uprights at (3/2, ½),
(½, 3/2) — and 4 of the 167 certified points carry some. Consequences: (i) the census
undercounts (a kiss-bearing structure is counted by its kiss-free support, which is a valid
support structure, so the verdict direction is unaffected); (ii) **L4 as stated on the active
graph G is FALSE when several squares kiss at one point** (the drawing argument's edges meet
at the shared contact point; o124/o154 are explicit non-planar G's at σ = 4) — L4 holds on the
graph with kisses removed, which is the only object A31/A43/A44 ever enumerated, so their
counts stand; (iii) a per-structure certificate for a kiss-bearing support must carry the
kiss as a tie-alternative row (A35 v2's treatment of Trump's (1,3)). Recorded with two
independent witnesses; not a soundness defect of any existing count.

## 6. [M] The price (T3) — `attempts/A88-fj-census/notes/pilot_report.md`, `results/pilot88_summary.json`

Per-structure certificate as in Lemma H-LOC: core box (wall-tightened centres, ONE tilt
variable per tilt class, pinned classes exact, s ∈ [3.82, s₀]); rows = the structure's
equality rows plus the t3lib dominance rows (rebuilt as g ≥ 0 side conditions — they carry
two thirds of all kills). Float interval arithmetic with outward pad, cross-checked against
t3lib's mpmath.iv rows to 1.2·10⁻¹⁴; a COST measurement, no certificate emitted.

**6.1 Tier 1 — triage (realisability LP), 720 uniform census structures + 19 A87 + Trump.**
Interval-linear outer relaxation of every row over tilt-class bins (sound: cannot kill a
realisable structure), tilt classes bisected ≤ 3 levels, KILL iff every leaf LP is
infeasible; each kill re-run with s ∈ [1, 5] to type it.

| population | n | kill | containment-type | ŝ-type | survivors | ms/structure |
|---|---|---|---|---|---|---|
| census (620 + 100 K0-1-dropped) | 720 | **0.225 [0.210, 0.241]** | **0.222** | **0.003** (2 of 720) | **0.775 [0.759, 0.790]** | 13.6 mean, 26 p95 |
| A87 certified/loose FJ structures | 19 | 0.42 | 0 | 8 (the σ = 4 family: realised only above ŝ) | — | 10 |
| Trump | 2 | 0 | 0 | 0 | survives | 9 |

Farkas dual mass on killing leaves: centre boxes 0.645, separation rows 0.355, the ŝ bound
0.000. **The triage kill is CONTAINMENT-type — A59's diagnosis re-derived; the ŝ bound does
almost nothing at Tier 1.** Sanity: no realised structure was ever containment-killed.

**6.2 Tier 2 — FJ tier (B&B with HC4 propagation, a-structure, a-ineq, a-σ, F = Gordan/Farkas
with the FIXED row set, K = Krawczyk for χ ≥ 0).** 20-structure pilot (cap 20 000 boxes /
10 min): the **7 census structures COMPLETE** (stack empty, no root) in 23–39 boxes,
0.035–0.056 s; the **13 A87/Trump structures never complete** (20 000 boxes, ~30 s) — correctly,
since each CONTAINS a genuine FJ point and the certificate is false there. Calibration on 150
uniform census T1-survivors (20 s cap): **complete 143/150 = 0.953 [0.933, 0.968]**, completing
mean 0.064 s / median 0.050 s / 33 boxes median; mean over all (censored) 0.994 s — a lower
bound. Leaf-kill shares: rebuilt dominance rows 0.667, HC4 0.188, a-structure 0.092,
**F 0.053** (2 050 firings on 4 of 150 structures). Krawczyk was reached 0 times by the search
(boxes never fall below the 0.05 basin on non-closing structures). HC4 ablation: without it the
root box does not contract at all (discharged fraction 0.5–0.9 after 2 000 boxes); with it the
root box collapses onto the realisation variety on the first sweep at no measurable cost.
Extrapolated obstruction on non-closing structures: depth 94–187 at branching 2^0.34–2^0.89
per level, 10⁹–10⁵⁰ boxes — the price of trying to certify a false statement.

**6.3 Canary (Trump's support, A76 Lemma K form).** Descending always into the child
containing ẑ, no leaf test ever excluded it; at depth 100 the ε-inflated Krawczyk contracted
(ratio 0.250, cond 15.5) and certified exactly one root, refined box width 4.4·10⁻¹⁵,
**s-enclosure [3.877083590022812, 3.877083590022816] ∋ ŝ**. Krawczyk IDENTIFIES ẑ, never
excludes it. Control: no certified-FJ structure was excluded by the descent; the only exclusion
was the LOOSE (tol 10⁻⁴, not certified) o018 at its own row-activity slack. PASS.

**6.4 Cost model.** total = N·c_triage + N·f_surv·c_FJ with **c_triage = 0.0136 s,
f_surv = 0.775, c_FJ ≥ 0.994 s (censored)**: **0.78 s per structure** (0.052 median-optimistic).

| N | total CPU-h | vs A85's 7 000 CPU-h |
|---|---|---|
| 10¹¹ (Level-0 graphs, MEASURED 9.5·10¹⁰) | 2.2·10⁷ | **×3 100** |
| 10¹⁸ (one graph's decoration fan-out; MEASURED median 1.3·10²¹) | 2.2·10¹⁴ | ×3·10¹⁰ |
| 10²⁹ (A31's decorated total; MEASURED 1.9·10³⁶) | 2.2·10²⁵ | ×3·10²¹ |

**Break-even N = 3.2·10⁷** (triage-only idealisation: 1.85·10⁹) — 3.5 (1.7) orders below the
smallest census figure and 29 orders below the measured decorated census. A85 baseline
(`attempts/A85-k0-route/notes/pilot_report.md`): ~1 350 s per budget-10 node (6 PASS / 5 FAIL /
1 refused of 12), collapsing to 63 s LP + 4 s cert at 4 corners deep; 3 200–7 000 CPU-h total.
**Per structure this route is cheap (0.78 s, and 95 % of the census closes in ~50 ms); it
loses on N alone.**

## 7. Verdict

> **The k0 FJ-supporting census is 1.9·10³⁶ decorated structures at k_H = 11 (rigorous
> bracket [3.9·10²⁶, 4.4·10⁵²]; graph layer 9.5·10¹⁰ ± 2.5·10⁹ in [5.7·10⁴, 1.3·10¹⁵]),
> ≥ 10¹² rigorously — the brief's "say so" branch. The dominant multiplier is the
> contact-type decoration fan-out (median 1.3·10²¹ per graph, ten orders above the graph
> count), i.e. the algebraic row set a certificate must fix; the FJ side adds no bulk filter
> (T1: the floor is L1 + L6, d_H unbounded, A44's rigid/flex split labels but does not kill,
> rigid share 1.2·10⁻⁵ and 0 of 167 certified points), and the whole k0 hypothesis buys
> ×1.011 (K0-1 ×0.99, K0-2 and K0-3 inert). Per structure the certificate is cheap — 0.78 s
> all-in, 95 % of census structures close in ~50 ms, Gordan fires once the selection menu is
> gone, Krawczyk identifies Trump exactly — so the route loses on the count, not the price:
> break-even N = 3.2·10⁷ against 9.5·10¹⁰ graphs and 10³⁶ structures; at N = 10¹¹ it is
> ×3 100 A85's upper bound. H1-by-structure is NOT k0_00's route; A85's tree stands.**

Two caveats named for the ledger. **Caveat R (K0-3 / Lemma R is window-dependent)**: the
ruler cap is a function of s; applying the s₀ cap to any object outside the window is unsound
(147 spurious kills at σ = 4 before the fix). **Caveat KISS (G-A88-4)**: A31/A43/A44's Level-1
vocabulary omits same-class corner–corner kisses (Trump's (1,3)); L4 planarity is false on the
ACTIVE graph when squares kiss at a point (o124/o154) and must be read on the kiss-free
support, which is the object every existing count enumerates.

What A88 leaves usable: Lemma H-LOC (the H-certificate is core-local — cost independent of
the unloaded squares); the fixed-row Farkas leaf and HC4 propagation as cheap (F)-type leaves
for Lemma F-LEAF's zone-tree (`drain_flow_k0.md` §4), measured at 50 ms per closed structure;
the measured Level-0 growth (A31's extrapolation confirmed at k = 11); and the decoration
fan-out measurement (A31's Level-1 extrapolation was 2.4 orders low).

## 8. Obligations ledger

## 7. Obligations ledger

| # | item | status |
|---|---|---|
| A88-O1 | T1 (a)–(d) | [T] this file (A44 L8–L11 + L1/L6/L11) |
| A88-O2 | K0-1, K0-3 | [T] exact decoration filters |
| A88-O3 | K0-2 | [T] under the k-maximal selection; (S)-flagged like Lemma F-LEAF |
| A88-O4 | K0-4 | inert at census level; box-volume factor only |
| A88-O5 | Lemma H-LOC | [T] |
| A88-O6 | census bracket | [M] §5: [3.9e26, 4.4e52], MC 1.9e36; canary PASS 9/9; D6 167/167 |
| A88-O7 | cost distribution | [M]/[X] §6: 0.78 s/structure, break-even N = 3.2e7; canary PASS |
| A88-G4 | kiss vocabulary gap / L4 on the active graph | [F] recorded; counts unaffected (kiss-free support) |
| Caveat R | K0-3 window dependence | [T] stated §3 |
