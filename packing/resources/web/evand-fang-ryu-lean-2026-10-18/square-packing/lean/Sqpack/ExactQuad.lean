import Sqpack.ExactCheck

/-!
# Closed forms for quadratic sides

`packs_exact` (`ExactCheck`) proves `∃ s, pS(s) = 0 ∧ Sa ≤ s ≤ Sb ∧ Packs n s`: the side is named only as the root of
`pS` in a rational interval.  When `pS = c₀ + c₁ X + c₂ X²` is quadratic, `quadOK` checks, in rational arithmetic, that
this root is `P + Q √D`:

* `r = P + Q √D` is a root: `c₂ (P² + Q² D) + c₁ P + c₀ = 0` and `Q (2 c₂ P + c₁) = 0`;
* the other root `r' = -c₁/c₂ - r` is outside `[Sa, Sb]`, using rational bounds `lo ≤ √D ≤ hi`
  (`0 ≤ lo`, `lo² ≤ D ≤ hi²`, `0 ≤ hi`): `r'` lies between `P' - Q lo` and `P' - Q hi` (`P' = -c₁/c₂ - P`), and both
  are below `Sa` or both above `Sb`.

`eq_of_quadOK` turns this into `s = P + Q √D`; `packs_quad` and `minSide_le_quad` restate the packing theorem with the
closed form.  Everything is decided by `decide +kernel`.
-/

namespace UnitSquarePacking.EC

/-- The root of `pS` in `[Sa, Sb]` is `P + Q √D` (see the module docstring). -/
def quadOK (pS : Poly) (P Q : ℚ) (D : ℕ) (lo hi Sa Sb : ℚ) : Bool :=
  match pS with
  | [c0, c1, c2] =>
    decide (c2 ≠ 0) && decide (c2 * (P ^ 2 + Q ^ 2 * D) + c1 * P + c0 = 0) && decide (Q * (2 * c2 * P + c1) = 0) &&
      decide (0 ≤ lo) && decide (lo ^ 2 ≤ D) && decide ((D : ℚ) ≤ hi ^ 2) && decide (0 ≤ hi) &&
      ((decide (-c1 / c2 - P - Q * lo < Sa) && decide (-c1 / c2 - P - Q * hi < Sa)) ||
        (decide (Sb < -c1 / c2 - P - Q * lo) && decide (Sb < -c1 / c2 - P - Q * hi)))
  | _ => false

theorem eq_of_quadOK {pS : Poly} {P Q lo hi Sa Sb : ℚ} {D : ℕ} (h : quadOK pS P Q D lo hi Sa Sb = true)
    {s : ℝ} (hs : peval pS s = 0) (ha : (Sa : ℝ) ≤ s) (hb : s ≤ Sb) : s = P + Q * √(D : ℝ) := by
  match pS, h, hs with
  | [c0, c1, c2], h, hs =>
    simp only [quadOK, Bool.and_eq_true, Bool.or_eq_true, decide_eq_true_eq] at h
    obtain ⟨⟨⟨⟨⟨⟨⟨h2, hr1⟩, hr2⟩, hlo0⟩, hlo⟩, hhi⟩, hhi0⟩, hex⟩ := h
    simp only [peval] at hs
    set x := √(D : ℝ) with hx
    have hD : (0 : ℝ) ≤ D := Nat.cast_nonneg D
    have hxx : x ^ 2 = D := Real.sq_sqrt hD
    have hlox : (lo : ℝ) ≤ x := Real.le_sqrt_of_sq_le (by exact_mod_cast hlo)
    have hxhi : x ≤ (hi : ℝ) := Real.sqrt_le_iff.2 ⟨by exact_mod_cast hhi0, by exact_mod_cast hhi⟩
    have h2' : (c2 : ℝ) ≠ 0 := by exact_mod_cast h2
    have hr1' : (c2 : ℝ) * (P ^ 2 + Q ^ 2 * D) + c1 * P + c0 = 0 := by exact_mod_cast hr1
    have hr2' : (Q : ℝ) * (2 * c2 * P + c1) = 0 := by exact_mod_cast hr2
    have hr : (c2 : ℝ) * (P + Q * x) ^ 2 + c1 * (P + Q * x) + c0 = 0 := by
      linear_combination hr1' + x * hr2' + (c2 : ℝ) * Q ^ 2 * hxx
    have key : (c2 : ℝ) * ((s - (P + Q * x)) * (c2 * s + c2 * (P + Q * x) + c1)) = 0 := by
      linear_combination (c2 : ℝ) * hs - (c2 : ℝ) * hr
    rcases mul_eq_zero.1 ((mul_eq_zero.1 key).resolve_left h2') with h0 | h0
    · linarith
    · exfalso
      have hs' : s = -c1 / c2 - P - Q * x := by field_simp; linear_combination h0
      have hq1 : ((-c1 / c2 - P - Q * lo : ℚ) : ℝ) = -c1 / c2 - P - Q * lo := by push_cast; ring
      have hq2 : ((-c1 / c2 - P - Q * hi : ℚ) : ℝ) = -c1 / c2 - P - Q * hi := by push_cast; ring
      have hQ : ((Q : ℝ) * lo ≤ Q * x ∧ (Q : ℝ) * x ≤ Q * hi) ∨ ((Q : ℝ) * hi ≤ Q * x ∧ (Q : ℝ) * x ≤ Q * lo) := by
        rcases le_total 0 (Q : ℝ) with hq | hq
        · exact Or.inl ⟨mul_le_mul_of_nonneg_left hlox hq, mul_le_mul_of_nonneg_left hxhi hq⟩
        · exact Or.inr ⟨mul_le_mul_of_nonpos_left hxhi hq, mul_le_mul_of_nonpos_left hlox hq⟩
      rcases hex with ⟨e1, e2⟩ | ⟨e1, e2⟩
      · have e1' : ((-c1 / c2 - P - Q * lo : ℚ) : ℝ) < Sa := by exact_mod_cast e1
        have e2' : ((-c1 / c2 - P - Q * hi : ℚ) : ℝ) < Sa := by exact_mod_cast e2
        rw [hq1] at e1'; rw [hq2] at e2'
        rcases hQ with ⟨q1, q2⟩ | ⟨q1, q2⟩ <;> linarith
      · have e1' : (Sb : ℝ) < ((-c1 / c2 - P - Q * lo : ℚ) : ℝ) := by exact_mod_cast e1
        have e2' : (Sb : ℝ) < ((-c1 / c2 - P - Q * hi : ℚ) : ℝ) := by exact_mod_cast e2
        rw [hq1] at e1'; rw [hq2] at e2'
        rcases hQ with ⟨q1, q2⟩ | ⟨q1, q2⟩ <;> linarith

/-- The packing theorem of `packs_exact` with the side in closed form. -/
theorem packs_quad {n : ℕ} {pS : Poly} {P Q lo hi Sa Sb : ℚ} {D : ℕ}
    (h : ∃ s : ℝ, peval pS s = 0 ∧ (Sa : ℝ) ≤ s ∧ s ≤ Sb ∧ Packs n s)
    (hq : quadOK pS P Q D lo hi Sa Sb = true) : Packs n (P + Q * √(D : ℝ)) := by
  obtain ⟨s, hs, ha, hb, hp⟩ := h
  rwa [← eq_of_quadOK hq hs ha hb]

/-- A container holding a unit square has side `≥ 0` (as `SpecBridge.nonneg_of_packs`, which imports heavy data). -/
lemma nonneg_of_packs_q {n : ℕ} {s : ℝ} (hn : 1 ≤ n) (h : Packs n s) : 0 ≤ s := by
  obtain ⟨c, θ, hin, -⟩ := h
  have hc : c ⟨0, hn⟩ ∈ unitSq (c ⟨0, hn⟩) (θ ⟨0, hn⟩) :=
    ⟨0, ⟨⟨by norm_num, by norm_num⟩, by norm_num, by norm_num⟩, by simp [rot]⟩
  obtain ⟨⟨h1, h2⟩, -⟩ := hin _ hc
  linarith

/-- `s(n) ≤ P + Q √D`. -/
theorem minSide_le_quad {n : ℕ} (hn : 1 ≤ n) {pS : Poly} {P Q lo hi Sa Sb : ℚ} {D : ℕ}
    (h : ∃ s : ℝ, peval pS s = 0 ∧ (Sa : ℝ) ≤ s ∧ s ≤ Sb ∧ Packs n s)
    (hq : quadOK pS P Q D lo hi Sa Sb = true) : minSide n ≤ P + Q * √(D : ℝ) :=
  csInf_le ⟨0, fun _ hs => nonneg_of_packs_q hn hs⟩ (packs_quad h hq)

end UnitSquarePacking.EC
