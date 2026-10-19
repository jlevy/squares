# Drain lemma and the T3 exclusion specification (advisor draft v3, 2026-08-26)

v2: D3 (KKT under constraint qualification, with a to-be-written degenerate taxonomy) is REPLACED by
D3′ (Fritz John, CQ-free). The taxonomy obligation is DISCHARGED: FJ needs no constraint
qualification, so corner-corner ties, flush contacts and every other CQ failure are covered by the
same statement. T3 updated accordingly. v1's D3 kept below for the record.

v3 (after pilot A30, advisor-verified): three corrections. (C1) FJ stationarity SIGN: with rows
written g ≥ 0 the correct equation is λ₀∇s = Σ λ_k ∇g_k (v2's + sign is unsatisfiable everywhere —
the uniform expansion direction increases s and every row, so v2's T3(c) would exclude every cell).
(C2) D2's bounding-box-clearance hypothesis was VACUOUS (the minimal enclosing square always touches
some square); repaired by shrinking about the container CENTRE — see D2 below, rewritten. (C3) the
separation row selects the NEAREST corner (min along u), (corner_{k*}(j) − c_i)·u ≥ 1/2, dominance
rows (corner_m − corner_{k*})·u ≥ 0. Also added: the Gordan/Farkas form of (c), which is the exact
first-order test and covers the λ₀ = 0 branch for free. Verdict of pilot A30 recorded in Status.

Setting. Configurations z = (c_i, t_i)_{i=1..11}, t_i = tan(θ_i/2) ∈ [0,1]; all constraints polynomial
in (c, t) after clearing (1+t²) denominators. D₀ = {z : squares pairwise interior-disjoint, normalised
min corner at the origin, contained in [0,4]²} — closed, bounded, SEMI-ALGEBRAIC (SAT gives the
polynomial description of interior-disjointness). σ(z) = side of the minimal enclosing axis-aligned
square = max of finitely many polynomial coordinate functions; continuous, piecewise-polynomial.

## Lemma D1 (attainment) — PROVED; LEAN-PROVED (A68, 2026-09-01)
If some z ∈ D₀ has σ(z) ≤ s₀ ≤ 4, then m := min{σ(z) : z ∈ D₀} ≤ s₀ is ATTAINED. Proof: {σ ≤ s₀} ∩ D₀
is closed (σ continuous, D₀ closed) and bounded, hence compact; σ continuous. ∎
Consequently s(11) = m, and "no minimiser of σ with value ≤ s₀ exists" ⟹ s(11) > s₀.

FORMAL (A68): `lean/PackingCertMathlib/PackingCertMathlib/Attain.lean`, theorem `attained_thm` —
the `attained` axiom of `TopLevel.lean` is DISCHARGED (roster 13 → 12; axioms
propext/Choice/Quot.sound only). The Lean statement is the equivalent epigraph form "the set
{s : Fits 11 s} has a least element" (side minimised directly, no σ or normalisation needed).
Two notes the formalisation surfaced, neither a gap in the mathematics:
(i) the one non-obvious ingredient of "D₀ closed" is that pairwise INTERIOR-disjointness is a
closed condition on the coordinates; the formal route is the exact interior formula
interior(square(c,t)) = the OPEN u/v box (`mem_interior_iff_uv` — ⊇ was A64's
`strict_uv_mem_interior`, ⊆ is a push along the edge direction), which makes overlap an open
condition (a witness point with four strict inequalities) and its negation closed;
(ii) no Hausdorff-limit / Blaschke argument is needed anywhere (contrary to the cost estimate
in the old TopLevel docstring): compactness happens in the 33+1 coordinates, with containment
expressed by A64's `set_subset_container_iff` inequalities and boundedness forced by the
containment rows themselves (wT ≥ 1). Nonemptiness: an explicit 11-in-a-row packing at s = 11.

## Lemma D2 (gap-squeeze; slack cells are free) — PROVED (v3 form; v2's was vacuous)
If z ∈ D₀ with σ = σ(z) ≥ 3 has every pairwise SAT-gap ≥ δ > 0, then σ can be strictly decreased, so
z is NOT a minimiser. Proof: shrink about the container centre m = (σ/2, σ/2): c_i ↦ m + (c_i − m)(1 − η)
with η = δ/(2√2 σ), tilts unchanged. (i) Gaps survive: the relative displacement of any centre pair is
η|c_i − c_j| ≤ η·√2σ = δ/2, and a SAT gap along a fixed axis changes by at most that, so all gaps stay
≥ δ/2 > 0. (ii) The bounding box strictly shrinks on all four sides: the owner of the max-x corner has
c_x ≥ σ − √2/2 > σ/2 (corner offset ≤ √2/2), so its centre moves left by η(c_x − σ/2) > 0 and the max-x
corner strictly decreases; the owner of the min-x corner has c_x ≤ √2/2 < σ/2, so its centre moves
right and the min-x corner strictly increases; same in y. Hence σ(new) < σ(z). ∎
Per-cell form: if interval arithmetic certifies min pairwise gap ≥ δ(C) > 0 uniformly on a cell C,
then C contains no minimiser. NOTE the hypothesis is now pairwise gaps ONLY — no bounding-box
clearance condition (which is never satisfiable at the minimal enclosing square).

## Lemma D3′ (per-selection FRITZ JOHN necessity) — PROVED, no CQ needed

Smooth selection NLP. Epigraph variables (z, s). Constraints, all polynomial after clearing (1+t²):
 (i) containment: every corner coordinate of every square lies in [0, s] — already smooth, NO
     selection needed (a conjunction of 88 polynomial inequalities plus the epigraph coupling);
 (ii) pairwise separation, selected: for each pair (i,j) a selection S picks an owner square, one of
     its two edge normals u with a sign (u a rational function of the owner's t, ‖u‖ = 1), and the
     NEAREST corner k* of the other square along u, and imposes  (corner_{k*}(j) − c_i)·u ≥ 1/2
     together with the three DOMINANCE rows  (corner_m(j) − corner_{k*}(j))·u ≥ 0  (k* is minimal).
     Dominance makes the selected row equal to true SAT separation (all of j beyond i's face), so
     S-FEASIBLE ⇒ INTERIOR-DISJOINT (soundness of the smooth surrogate), and
     for convex polygons a separating axis always exists among edge normals, so every z ∈ D₀ is
     S-feasible for AT LEAST ONE selection of the finite menu (completeness). Ties (corner-corner
     contacts, flush = parallel edges) are consistent with SEVERAL selections and are covered by each.

Statement. Let ẑ minimise σ over D₀ with value m (exists by D1). Then for EVERY selection S
consistent with ẑ, the point (ẑ, m) is a global minimiser of s over the S-feasible set (S-feasible ⊆
D₀ and ẑ ∈ S-feasible), a smooth polynomial NLP; hence the FRITZ JOHN conditions hold: there exist
λ₀ ≥ 0 and λ ≥ 0, (λ₀, λ) ≠ 0 (normalise λ₀ + Σλ = 1), with λ₀∇s = Σ λ_k ∇g_k and λ_k g_k = 0
(rows written g_k ≥ 0; this is the v3-corrected sign, cf. A22's A_Sᵀλ = e_s).
Proof: FJ is necessary at any local minimum of a smooth NLP with NO constraint qualification
(F. John 1948; standard). ∎

Remark (cost, not soundness). FJ admits spurious solutions with λ₀ = 0 (positively dependent
constraint gradients with no descent content). A cell whose FJ system is solvable only with λ₀ = 0
is not certified by (c); split it, or exclude the λ₀ = 0 branch by a separate argument. This is the
only trace left of the old degenerate taxonomy, and it is an efficiency question.

## Lemma D3 (v1: per-selection KKT necessity) — superseded by D3′, kept for the record
At any minimiser ẑ, fix ANY "selection" S consistent with ẑ: for each pair, one SAT axis achieving
separation; for the box, the extremal corners; for containment, the touching walls. The region R_S
defined by S's smooth polynomial inequalities satisfies ẑ ∈ D₀ ∩ R_S ⊆ D₀, so ẑ also minimises σ over
D₀ ∩ R_S, a SMOOTH NLP; under the selection's constraint qualification (LICQ/MFCQ), the standard KKT
conditions for that NLP hold at ẑ. This holds for EVERY consistent selection simultaneously.
Care points, quarantined as their own (finitely many) degenerate branches: selections where CQ fails
(corner-corner ties, flush contacts — handled in A22 by centre-distance surrogate rows), and rattler
directions (zero multipliers; excluded by first parking rattlers: a square with a strict free
neighbourhood contributes no active rows and its cell needs only D2).

## T3 specification (sound by D1, D2, D3′)
A cell C (product of centre boxes and t-intervals for the 11 squares, mod symmetry) is EXCLUDED if:
 (a) C ∩ D₀ = ∅ (infeasible; interval SAT), or (b) D2 fires (uniform slack), or
 (c) for EVERY selection S in C's finite consistent menu (only rows whose interval evaluation on C
 straddles activity — small menus for small cells; menu must include tie selections, which are the
 SAME smooth systems), a sound test excludes all solutions of the FJ(S) system with value ≤ s₀ and
 λ₀ ≥ 0, λ ≥ 0, λ₀ + Σλ = 1 in C. PREFERRED TEST (c1), the GORDAN/FARKAS form (pilot A30): exhibit
 one direction y with ∇s·y < 0 and ∇g_k·y > 0 verified in interval arithmetic for every row that can
 be active on C — then dotting stationarity with y forces λ₀ = 0 and all λ_k = 0, contradicting the
 normalisation, so NO FJ point of S lies in C, the λ₀ = 0 branch included. By Gordan's theorem this
 is EXACTLY first-order-complete: the direction exists iff no FJ multipliers exist for any gradient
 tuple in the interval hull. Per-selection cost ≈ 2 ms (measured). The union-over-menu variant (one y
 for all selections at once) is blocked at flush ties (tied dominance rows are exact negatives).
 Fallback (c2), interval-Krawczyk on FJ(S): INOPERATIVE with λ free over the simplex whenever the
 multiplier polytope is positive-dimensional (structurally singular Jacobian); requires active-set
 sub-branching or λ-subdivision — use only inside cells small enough that few subsets survive.
 BONUS TEST (a′): if some straddling pair's whole menu is empty (every selection has a row certified
 < 0 on C), then by menu completeness C ∩ D₀ = ∅ — strictly stronger than naive interval SAT.
If every cell of a cover of D₀/symmetry is excluded, then no minimiser with σ ≤ s₀ exists, so
s(11) > s₀ by D1.

## Status
D1, D2 (v3 form), D3′ complete — T3 is SOUND as specified (with the v3 sign/row corrections), no
outstanding taxonomy obligation. PILOT A30 VERDICT (2026-08-26): the per-branch engine WORKS (FJ
Krawczyk isolates Trump's critical point at cell half-width ≤ 2.4e-4, 0.2 s/branch; Farkas test 2
ms/selection, exactly first-order-complete), and D2's reach at the endgame value s₀ = s* is ZERO
(h_D2 ≈ 0.015(s₀ − s*)); but T3 AS A COORDINATE-CELL COVER IS REJECTED: the discharge-radius ratio
c = δ_kill/h ∈ [1.15, 3.75] (median 1.86) is SCALE-INVARIANT, so a shell of ≈ c³³ ≈ 8e8 cells
survives around EVERY critical point at every refinement depth; floor ≥ 1e5 CPU-h (optimistic) to
5e7 CPU-h (realistic) counting only Trump's shell. The blow-up is dimensional, not algorithmic.
CONSEQUENCE: the exclusion program must branch on STRUCTURE (selection/contact graphs — the PI's
proposal), with per-graph GLOBAL algebraic solving of the FJ system in t = tan(θ/2), coordinate
cells appearing only at the last level inside structure-reduced boxes (h ~ 1e-4), composed with
A22's neighbourhood certificate at Trump. The stress lemma is PROMOTED from optimisation to
load-bearing: it is the natural pruner of the structure-graph menu. Full data:
attempts/A30-t3-pilot/results/pilot_report.json (gap list G1–G16 recorded there).
