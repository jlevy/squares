import PackingCertMathlib.GuardLine

/-!
# Theorem G — the guard-line (chord-sum) clause, and Lemma LINE-1

**What it says.**  *Lemma LINE-1:* the chords that pairwise-disjoint closed unit squares inside
`[0, s]²` cut on an axis-parallel line sum to at most `s`.  *Theorem G:* the case certificate may
carry guard lines `l` with densities `z_l ≥ 0`, so the pricing measure becomes
`atoms + Σ_l z_l · H¹|_l`; for each line a set `J_l` of unattached cores with pairwise distinct,
non-windowed owners contributes certified chord lower bounds `clo`; if the total
`Σw + Σ_l z_l (s − Σ_{J_l} clo)` is below `b₄ · NEEDR`, no strict family satisfies (H1)–(H3).

**Why it matters.**  A guard line prices the ROOM along a wall or a seam that the atoms cannot
see: the pins' chords are known exactly, so the free squares crossing the line are charged for
the length they must occupy.  It is the clause that kills the "wide H" pages where core-based
tests see nothing.

**Scope correction (A192 finding F1).**  LINE-1 with interior-disjoint squares and CLOSED chords
is FALSE (two rows of squares meeting along the line); it holds for the closed-disjoint families
the chain refutes after dilation — which is how Lean states it.

**How it is proved** (`GuardLine.lean`, A192; prose `docs/proofs/guardline_clause.md`):
one-dimensional Lebesgue additivity for LINE-1; Theorem W's counting with the line mass for G.
The checker half (Lemma MINCHORD, the five-point chord test) is [C] — its obligation is exactly
the hypothesis `hclo` below.

**For any `n`.**  Both are stated for every `N`, `n`.
-/

namespace PackingCert.S11

open Set MeasureTheory MeasureI WindowsW GuardLineW

/-- **Lemma LINE-1** for strict families. -/
theorem line_1 {N : ℕ} {s : ℝ} (hs : 0 ≤ s) {Q : Fin N → Set RP}
    (hQ : IsStrictFamily N s Q) (l : GuardLine) :
    ∑ i, chordLen l (Q i) ≤ s :=
  chord_sum_le_side hs hQ l

/-- **Theorem G**, set level. -/
theorem theorem_G {n m r L : ℕ} {s NEEDR : ℝ} (hs : 0 ≤ s) (hN : 0 ≤ NEEDR)
    (atoms : List IAtom) (hw : ∀ a ∈ atoms, 0 ≤ a.w)
    (lines : Fin L → GuardLine) (z : Fin L → ℝ) (hz : ∀ l, 0 ≤ z l)
    (Exempt : Set RP → Prop)
    {Q : Fin n → Set RP} (hQ : IsStrictFamily n s Q)
    (K : Fin m → Set RP) (own : Fin m → Fin n)
    (W : Fin r → Set RP → Prop) (κ : Fin r → Option (Fin m))
    (att : List ℕ) (hnd : att.Nodup)
    (hatt : ∀ j ∈ att, ∃ jj : Fin m, (jj : ℕ) = j ∧ ∃ i, κ i = some jj)
    (σ : Fin r → Fin n) (hσ : Function.Injective σ)
    (hH1 : ∀ i, W i (Q (σ i)))
    (hH2 : ∀ j, (∀ i, κ i ≠ some j) → K j ⊆ Q (own j))
    (hH3 : ∀ k, ¬ Exempt (Q k))
    (hV1 : 0 < (n : ℝ) - r - ((m : ℝ) - att.length) →
      ∀ S, IsUnitSquare S → S ⊆ container s → (∀ j, Disjoint S (K j)) → ¬ Exempt S →
        NEEDR ≤ lineMass atoms lines z S)
    (hV2 : ∀ i S, IsUnitSquare S → S ⊆ container s → W i S →
      (∀ i' j, i' ≠ i → κ i' = some j → Disjoint S (K j)) → ¬ Exempt S →
        NEEDR ≤ lineMass atoms lines z S)
    (hV3 : ∀ i j, κ i = some j → ∀ S, W i S → K j ⊆ S)
    (J : Fin L → Finset (Fin m)) (clo : Fin L → Fin m → ℝ)
    (hJun : ∀ l, ∀ j ∈ J l, ∀ i, κ i ≠ some j)
    (hinj : ∀ l, ∀ x ∈ J l, ∀ y ∈ J l, own x = own y → x = y)
    (hoff : ∀ l, ∀ j ∈ J l, ∀ i, own j ≠ σ i)
    (hclo : ∀ l, ∀ j ∈ J l, clo l j ≤ chordLen (lines l) (Q (own j)))
    (hV4 : (atoms.map fun a => (a.w : ℝ)).sum + ∑ l, z l * (s - ∑ j ∈ J l, clo l j)
      < ((n : ℝ) - m + att.length) * NEEDR) : False :=
  guarded_dead hs hN atoms hw lines z hz Exempt hQ K own W κ att hnd hatt σ hσ hH1 hH2 hH3
    hV1 hV2 hV3 J clo hJun hinj hoff hclo hV4

#print axioms line_1
#print axioms theorem_G

end PackingCert.S11
