import Sqpack.ExactCheck

/-!
# Sweep-line pair pruning for `ExactCheck`

`ExactCheck.rowOK` visits every `j > i`.  Most pairs are far apart; the shadow disc test then passes, but evaluating
it still costs a lookup of `encl j`, which in a generated certificate (a `![…]` vector) is linear in `j`.  So the
kernel's work grows like `n³`.

Here the squares are listed with nondecreasing `encl.x` lower bounds (`sortedOK`, checked on adjacent pairs only), and
each row `i` carries a cut `cut i`: the first index whose `x` lower bound is at least `3/2` beyond `i`'s `x` upper
bound (`cutOK`).  For `j ≥ cut i` the `x` gap alone is `≥ 3/2`, so `gap² ≥ 9/4 ≥ 2`: the disc test `farOK` holds
(`farOK_of_xgap`), and the row check skips those `j` with a `Nat` comparison (`rowOKc`).

`packs_exact_cut` is `packs_exact` with `rowOK` replaced by `sortedOK`, `cutOK` and `rowOKc`.  The `Cert` structure
and the old entry point are unchanged.
-/

namespace UnitSquarePacking.EC

open Shadow

variable {n : ℕ} (C : Cert n)

/-- The `x` lower bound of square `j`'s enclosure. -/
def xlo (j : Fin n) : ℚ := (C.encl j).x.1

/-- Nondecreasing `x` lower bounds, checked on adjacent pairs. -/
def sortedOK : Bool :=
  (List.range n).all fun k => if h : k + 1 < n then decide (xlo C ⟨k, by omega⟩ ≤ xlo C ⟨k + 1, h⟩) else true

/-- Row `i`'s cut is at least `3/2` to the right of square `i`. -/
def cutOK (cut : Fin n → ℕ) (i : Fin n) : Bool :=
  if h : cut i < n then decide ((C.encl i).x.2 + 3 / 2 ≤ xlo C ⟨cut i, h⟩) else true

/-- The pairs `(i, j)`, `i < j < cut i`. -/
def rowOKc (cut : Fin n → ℕ) (i : Fin n) : Bool :=
  (List.finRange n).all fun j => !decide (i < j) || decide (cut i ≤ j.val) || pairOK C i j

lemma xlo_mono (hs : sortedOK C = true) : ∀ k (a b : Fin n), b.val = a.val + k → xlo C a ≤ xlo C b
  | 0, a, b, h => by rw [Fin.ext (by omega : b.val = a.val)]
  | k + 1, a, b, h => by
    have hb1 : a.val + k < n := by omega
    have h1 := xlo_mono hs k a ⟨a.val + k, hb1⟩ rfl
    simp only [sortedOK, List.all_eq_true, List.mem_range] at hs
    have h2 := hs (a.val + k) (by omega)
    have hlt : a.val + k + 1 < n := by omega
    rw [dif_pos hlt, decide_eq_true_eq] at h2
    have hb : b = ⟨a.val + k + 1, hlt⟩ := Fin.ext (by simp; omega)
    rw [hb]; exact h1.trans h2

lemma farOK_of_xgap {Ei Ej : Encl} (h : Ei.x.2 + 3 / 2 ≤ Ej.x.1) : farOK Ei Ej = true := by
  simp only [farOK, decide_eq_true_eq]
  have g1 : Ej.x.1 - Ei.x.2 ≤ gap Ei.x Ej.x :=
    (le_max_left _ _).trans (le_max_right _ _)
  have g0 : (0 : ℚ) ≤ gap Ei.y Ej.y := le_max_left _ _
  have : (3 / 2 : ℚ) ≤ gap Ei.x Ej.x := by linarith
  nlinarith

lemma rowOK_of_rowOKc {cut : Fin n → ℕ} (hs : sortedOK C = true) {i : Fin n} (hc : cutOK C cut i = true)
    (hr : rowOKc C cut i = true) : rowOK C i = true := by
  simp only [rowOK, rowOKc, List.all_eq_true, List.mem_finRange, true_implies] at hr ⊢
  intro j
  have hj := hr j
  by_cases hij : i < j
  · by_cases hcj : cut i ≤ j.val
    · have hcn : cut i < n := lt_of_le_of_lt hcj j.isLt
      simp only [cutOK, dif_pos hcn, decide_eq_true_eq] at hc
      have hm := xlo_mono C hs (j.val - cut i) ⟨cut i, hcn⟩ j (by simp; omega)
      have hx : (C.encl i).x.2 + 3 / 2 ≤ (C.encl j).x.1 := hc.trans hm
      simp [pairOK, Shadow.pairOK, farOK_of_xgap hx]
    · simpa [hij, hcj] using hj
  · simp [hij]

/-- **The packing theorem from a certificate, with sweep-line pruning.** -/
theorem packs_exact_cut (pS : Poly) (Sa Sb : ℚ) (cut : Fin n → ℕ) (hab : C.a ≤ C.b)
    (hsign : qeval C.f C.a * qeval C.f C.b ≤ 0) (hSl : SlOK C = true) (hbox : ∀ i, boxOK C i = true)
    (hs : sortedOK C = true) (hc : ∀ i, cutOK C cut i = true) (hrow : ∀ i, rowOKc C cut i = true)
    (hp : zeroOK C.f (pcomp pS C.S) = true)
    (hlo : nonnegOK C.f C.a C.b (psub C.S [Sa]) = true) (hhi : nonnegOK C.f C.a C.b (psub [Sb] C.S) = true) :
    ∃ s : ℝ, peval pS s = 0 ∧ (Sa : ℝ) ≤ s ∧ s ≤ Sb ∧ Packs n s :=
  packs_exact C pS Sa Sb hab hsign hSl hbox (fun i => rowOK_of_rowOKc C hs (hc i) (hrow i)) hp hlo hhi

end UnitSquarePacking.EC
