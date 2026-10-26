import Sqpack.SquareArea
import Sqpack.MixedMeasure

/-!
# E′: a lower bound on the Lebesgue area of a tilted square (`QUADRANT_EXACT.md` §4.4)

For `0 < θ < π/2` and a Lebesgue rectangle `U = [a₁, b₁] × [a₂, b₂]`, if `Q = sq c θ 1` lies in
`{x ≤ b₁, y ≤ b₂}` then

  `|Q ∩ U| ≥ 1 − ĝ(a₁ − x_min) − ĝ(a₂ − y_min)`

(`area_ge_ghat`), with `ĝ` of `SquareArea.lean` (`s = sin θ`, `c = cos θ`):  the left cap is
`cap_le_ghat`, the bottom cap is the left cap of the square reflected in `x = y` (`bottom_cap_le_ghat`),
which has angle `π/2 − θ`, so its sine and cosine are exchanged (`cap_le_ghat'`).
-/

open MeasureTheory Set
open scoped ENNReal

namespace SquarePacking

namespace SqArea

lemma preimage_swap_sq (c : ℝ × ℝ) (θ : ℝ) :
    swapXY ⁻¹' sq (swapXY c) (Real.pi / 2 - θ) 1 = sq c θ 1 := by
  ext p
  rw [Set.mem_preimage, show Real.pi / 2 - θ = -θ + Real.pi / 2 by ring, sq_add_pi_div_two,
    mem_sq_swapXY]

/-- The abscissa of the lowest vertex. -/
noncomputable def ymin (c : ℝ × ℝ) (θ : ℝ) : ℝ := c.2 - (Real.cos θ + Real.sin θ) / 2

/-- **The bottom cap**: `|Q ∩ {y < a}| ≤ ĝ(a − y_min)`. -/
theorem bottom_cap_le_ghat {c : ℝ × ℝ} {θ : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ)
    (a : ℝ) :
    volume (sq c θ 1 ∩ {p | p.2 < a}) ≤
      ENNReal.ofReal (ghat (Real.sin θ) (Real.cos θ) (a - ymin c θ)) := by
  set θ' := Real.pi / 2 - θ
  have hs' : Real.sin θ' = Real.cos θ := Real.sin_pi_div_two_sub θ
  have hc' : Real.cos θ' = Real.sin θ := Real.cos_pi_div_two_sub θ
  have e : sq c θ 1 ∩ {p | p.2 < a} = swapXY ⁻¹' (sq (swapXY c) θ' 1 ∩ {p | p.1 < a}) := by
    rw [Set.preimage_inter, preimage_swap_sq]; rfl
  have hm : MeasurableSet (sq (swapXY c) θ' 1 ∩ {p : ℝ × ℝ | p.1 < a}) :=
    (isClosed_sq' _ _ _).measurableSet.inter (measurableSet_lt measurable_fst measurable_const)
  rw [e, measurePreserving_swapXY.measure_preimage hm.nullMeasurableSet]
  have h := cap_le_ghat' (c := swapXY c) (θ := θ') (by rw [hs']; exact hc) (by rw [hc']; exact hs) a
  rw [hs', hc'] at h
  have ex : xmin (swapXY c) θ' = ymin c θ := by
    simp only [xmin, ymin, swapXY, hs', hc']; ring
  rwa [ex] at h

lemma ghat_nonneg {s co d : ℝ} (hs : 0 < s) (hc : 0 < co) : 0 ≤ ghat s co d := by
  unfold ghat
  split_ifs with h1 h2
  · exact le_rfl
  · positivity
  · apply div_nonneg _ hc.le; linarith [not_le.mp h2]

/-- **E′**: the area of `Q` in the Lebesgue rectangle `[a₁, b₁] × [a₂, b₂]`, when `Q` lies left of
`b₁` and below `b₂`. -/
theorem area_ge_ghat {c : ℝ × ℝ} {θ : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ)
    {a1 b1 a2 b2 : ℝ} (hb : ∀ p ∈ sq c θ 1, p.1 ≤ b1 ∧ p.2 ≤ b2) :
    1 - ghat (Real.sin θ) (Real.cos θ) (a1 - xmin c θ) -
        ghat (Real.sin θ) (Real.cos θ) (a2 - ymin c θ)
      ≤ (volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2)).toReal := by
  set g1 := ghat (Real.sin θ) (Real.cos θ) (a1 - xmin c θ)
  set g2 := ghat (Real.sin θ) (Real.cos θ) (a2 - ymin c θ)
  have hsub : sq c θ 1 ⊆ (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2) ∪ (sq c θ 1 ∩ {p | p.1 < a1}) ∪
      (sq c θ 1 ∩ {p | p.2 < a2}) := by
    intro p hp
    obtain ⟨h1, h2⟩ := hb p hp
    by_cases hx : p.1 < a1
    · exact Or.inl (Or.inr ⟨hp, hx⟩)
    by_cases hy : p.2 < a2
    · exact Or.inr ⟨hp, hy⟩
    exact Or.inl (Or.inl ⟨hp, ⟨not_lt.mp hx, h1⟩, ⟨not_lt.mp hy, h2⟩⟩)
  have hle := (measure_mono (μ := (volume : Measure (ℝ × ℝ))) hsub).trans
    ((measure_union_le _ _).trans (add_le_add (measure_union_le _ _) le_rfl))
  rw [volume_sq] at hle
  have hV : volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2) ≠ ⊤ :=
    ne_top_of_le_ne_top ENNReal.one_ne_top ((measure_mono inter_subset_left).trans (volume_sq c θ).le)
  have h3 : (1 : ℝ≥0∞) ≤ volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2) + ENNReal.ofReal g1 +
      ENNReal.ofReal g2 :=
    hle.trans (add_le_add (add_le_add le_rfl (cap_le_ghat hs hc a1)) (bottom_cap_le_ghat hs hc a2))
  have hfin : volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2) + ENNReal.ofReal g1 ≠ ⊤ :=
    ENNReal.add_ne_top.mpr ⟨hV, ENNReal.ofReal_ne_top⟩
  have h4 := ENNReal.toReal_mono (ENNReal.add_ne_top.mpr ⟨hfin, ENNReal.ofReal_ne_top⟩) h3
  rw [ENNReal.toReal_add hfin ENNReal.ofReal_ne_top, ENNReal.toReal_add hV
    ENNReal.ofReal_ne_top, ENNReal.toReal_ofReal (ghat_nonneg hs hc),
    ENNReal.toReal_ofReal (ghat_nonneg hs hc), ENNReal.toReal_one] at h4
  linarith

end SqArea

end SquarePacking
