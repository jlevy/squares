# Lemma N1 — the zone-assignment collapse (A42, Fable, 2026-08-28)

Named N1 in docs/proofs/seam_design.md §4; load-bearing for the S1 cascade (it replaces the
labeled occupancy branching b₂¹⁰ = 16¹⁰ ≈ 1.1e12, A38 probe B, by 10 additive certificates).
Setting and soundness of the individual certificates are Theorem 1 / K1 (docs/results.md;
NO-zone form as in A24/A38): this note supplies only the counting/assignment layer on top.

## 0. Setting and the quotient framing

Fix s > 0 (here s₀ = 969271/250000). A *packing* P is a set of 11 closed unit squares with
pairwise disjoint interiors contained in [0,s]². For a square Q write c(Q) ∈ [0,s]² for its
centre and θ(Q) ∈ ℝ/90° for its tilt — θ is well defined only in the quotient ℝ/90°, because a
square is invariant under its own quarter-turn; a "θ-window" is a closed arc of this circle,
possibly wrapping 0/90 (e.g. [84°,90°] ∪ [0°,6°] is ONE arc, the arc [−6°,6°]).

A packing carries no labels: it is the 11-element multiset {(c(Q), θ(Q), Q)}. A *labeling* is a
bijection {1..11} → P; the symmetric group S₁₁ acts freely and transitively on labelings. Every
statement certified by a Theorem-1/K1 case-LP is label-free ("SOME square of P satisfies …");
the cascade, however, is priced on labeled hypotheses ("square j lies in zone j"). Lemma N1 is
exactly the statement that this lift is unique mod S₁₁ — the labeled and unlabeled hypothesis
spaces are in bijection, so pricing one fixed labeling is exhaustive and no sum over
assignments is ever paid.

Everything below is stated in a fixed D4 frame (the A37 e-frame); the D4 quotient is handled
upstream by census canonicalization (A27 bridge; extended to G = D4 × S₁₁ by Lemma N2, not this
note).

## 1. Separation and the at-most-one lemma

**Lemma N1.0 (centre separation).** Distinct squares of a packing have ‖c(Q) − c(Q′)‖₂ ≥ 1.

*Proof.* A closed unit square contains the closed disk of radius 1/2 about its centre (the
inradius of a unit square is 1/2, any tilt). If ‖c − c′‖₂ < 1 the OPEN disks of radius 1/2
about c and c′ intersect (their centres are closer than the sum of radii); each open disk lies
in the interior of its square, so the interiors intersect — contradicting disjointness. ∎

The bound is sharp (two axis-aligned squares flush side-by-side), and the Trump configuration
attains it: the minimum pairwise centre distance of the 11 A37 e-frame placements is EXACTLY 1
(min ‖pᵢ − pⱼ‖² = 1 in exact rational arithmetic over the float placement values; A42
verification, §4).

**Corollary N1.0.1 (at-most-one).** A set Z ⊆ [0,s]² of Euclidean diameter < 1 contains the
centre of at most one square of any packing. In particular an ∞-ball of radius r < 1/(2√2)
≈ 0.35355 (diameter 2r√2), and any wall-clipped sub-rectangle of it. At r_occ = 0.06 the
diameter is 0.12·√2 ≈ 0.16971, margin ≈ 5.9×. ∎

Note what this buys: "exactly one per small zone" needs NO pigeonhole and NO disjointness — it
is pure geometry. Disjointness enters only in the counting across zones, next.

## 2. Lemma N1 (zone-assignment collapse)

**Hypotheses.**
(H1) Z₁, …, Z_m ⊆ [0,s]² × (ℝ/90°), m ≤ 11, are "zones": Zⱼ = Rⱼ × Θⱼ with Rⱼ ⊆ [0,s]² closed,
     Θⱼ a closed θ-arc; the FOOTPRINTS Rⱼ are pairwise disjoint and each has Euclidean
     diameter < 1. (Both conditions checked per instance in exact rational arithmetic; §4.)
(H2) For each j ≤ m there is a certified statement Oⱼ, valid for every packing P in some class
     𝒞 (the cascade's current hypothesis class): "at least one square Q of P has
     (c(Q), θ(Q)) ∈ Zⱼ." (In the cascade each Oⱼ is a K1 kill of the NO-zone hypothesis
     "no square in Zⱼ", Theorem 1 with budget 11 − #cores; soundness is T0/K1 verbatim and is
     NOT re-proved here. Oⱼ may itself be conditional on O₁…O_{j−1}: see Remark 2.)

**Conclusion.** For every P ∈ 𝒞:
(i)  each footprint Rⱼ contains the centre of EXACTLY one square, call it Q_{σ(j)}, and
     θ(Q_{σ(j)}) ∈ Θⱼ;
(ii) σ is injective; consequently the labeling "square j := the square in zone j" exists and
     any two labelings of P compatible with {label j ∈ Zⱼ} agree on labels 1..m — the
     assignment zones → squares is UNIQUE, and mod S₁₁ the labeled hypothesis
     "∀j: square j ∈ Zⱼ" has exactly one orbit of representatives. No assignment branching:
     the cascade prices ONE labeled node, not b_occ^m of them.
(iii) if m = 11: σ is a bijection, every centre of P lies in ⋃ⱼ Rⱼ, and no square has
     (c, θ) ∈ Rⱼ × Θⱼᶜ for any j (Θⱼᶜ = complement arc). The complement
     [0,s]² ∖ ⋃Rⱼ is certifiably centre-free.

*Proof.* (i) At least one centre in Rⱼ by Oⱼ; at most one by Corollary N1.0.1 since
diam Rⱼ < 1; and the unique square with centre in Rⱼ must be the Oⱼ-witness, so its θ lies in
Θⱼ. (ii) If σ(j) = σ(j′) for j ≠ j′ then the single square Q_{σ(j)} has its centre in
Rⱼ ∩ Rⱼ′ = ∅ — contradiction. Uniqueness of the labeling on 1..m: any compatible labeling must
send j to a square with centre in Rⱼ, and there is exactly one such square. (iii) An injection
of {1..11} into 11 squares is a bijection; every square is Q_{σ(j)} for some j, its centre lies
in R_{σ⁻¹(·)}; and the unique square with centre in Rⱼ has θ ∈ Θⱼ, while every other square has
centre outside Rⱼ — so no square at all has (c, θ) ∈ Rⱼ × Θⱼᶜ. ∎

**Corollary N1.1 (branch-free window-complement conditioning; used by the A42 drivers).**
Given Oⱼ certified with zone Rⱼ × Θⱼ, diam Rⱼ < 1, the hypothesis "some square in Zⱼ" may be
imposed on a subsequent case-LP as

    core  Rⱼ × [0°, 90°]   (full θ)   +   NO-family  Rⱼ × Θⱼᶜ,

with no case split, EVEN when Θⱼ wraps 0/90. Indeed by (i) the unique square with centre in Rⱼ
has θ ∈ Θⱼ and no other square has centre in Rⱼ, so Rⱼ × Θⱼᶜ is genuinely square-free — the
NO-family is a certified statement, not a guess. This removes the 2-way wrap split per
wall-flush zone (6 of the 11 Trump zones have θ-window [84°,90°] ∪ [0°,6°]; naive window-cores
would pay up to 2⁶ labeled cases per node). ∎

**Remark 1 (what fails if two zones overlap — the explicit failure mode).** If Rⱼ ∩ Rⱼ′ ≠ ∅, a
single square with centre in the intersection can witness BOTH Oⱼ and Oⱼ′: injectivity of σ
fails, the count of distinct occupied zones drops to ≥ m − 1, and with m = 11 conclusion (iii)
collapses — one square double-witnesses and some other square's centre may sit OUTSIDE ⋃Rⱼ, so
the complement is no longer centre-free and the sweep encoding (T3) becomes unsound. Similarly
if some diam Rⱼ ≥ 1, "exactly one" fails and Corollary N1.1 becomes unsound (a second square in
Rⱼ could carry θ ∈ Θⱼᶜ). Both hypotheses are therefore CHECKED, exactly, per instance.

**Remark 2 (chain composition).** In the A42 chain, O_{k+1} is certified for the class
𝒞_k = {P : conclusions of O₁…O_k hold}. By induction on k, all conclusions hold on the base
class 𝒞₀ (the surviving witness leaf): the conditional certificates compose. The bookkeeping
that conditioning survives re-anchoring across cascade stages is Lemma N7 (seam_design §4),
mechanical and out of scope here.

**Remark 3 (multiset reading).** Equivalently: the map {labeled packings with label j ∈ Zⱼ ∀j}
→ {unlabeled packings with all zones occupied}, forgetting labels, is a bijection; S₁₁ acts
freely on the fibers of the labeled space and each fiber meets the constraint set exactly once.
This is the precise sense of "assignment unique mod S₁₁" from seam_design §1.2 step 2.

## 3. Instance verification (exact, A42)

Zones: Rⱼ = clip([pⱼ.x ± 0.06] × [pⱼ.y ± 0.06], [1/2, s₀ − 1/2]²), Θⱼ = θⱼ ± 6°, over the 11
A37 Trump e-frame placements (seam38.trump_placements('e')). Checked in exact rational
arithmetic (Fraction over the exact float values; A42 code dir, one-shot script, 2026-08-28):

- min pairwise centre distance² = 1 exactly (attained; consistent with N1.0's sharpness);
- pairwise footprint disjointness: min inter-rectangle sup-gap = 34675803100911181/56294995342131200
  ≈ 0.615966 > 0 — disjoint with ~0.6 of margin;
- max footprint diameter = 0.12√2 ≈ 0.16971 < 1 (margin 5.9×); wall clipping only shrinks.

Hypothesis (H1) therefore holds for the A42 instance at r_occ = 0.06, and remains true a
fortiori for every shrunken radius r′ < 0.06 used by the T3 tightening sweep.

Status: proved (short, elementary); hypotheses machine-checked per instance; no Lean target
yet (candidate for the A28-style batch — the proof is two inequalities and a pigeonhole-free
count).
