import Sqpack.LebE

/-!
# The `tan` regime of a deep cap (`QUADRANT_EXACT.md` §4.4)

For `0 < θ < π/2` (`s = sin θ`, `c = cos θ`) and a depth `d = a − x_min ≥ max(s, c)`, the part of
`Q = sq c θ 1` right of `x = a` is the triangle at the rightmost vertex, of area
`(s + c − d)²/(2sc)` (when `d ≤ s + c`).  This is a convex function of `d`; its tangent at any
`d* ≤ 1`,

  `T(d) = (s + c − d*)²/(2sc) − (s + c − d*)(d − d*)/(sc)`,

is below it, and also below `0` for `d ≥ s + c`.  Hence `|Q ∩ {x < a}| ≤ 1 − T(d)`
(`cap_le_tan`), an affine function of `d`.  The bound is symmetric in `s` and `c`, so the bottom cap
follows through `x ↔ y` (`bottom_cap_le_tan`).
-/

open MeasureTheory Set
open scoped ENNReal

namespace SquarePacking

namespace SqArea

/-- The tangent at `d*` of `d ↦ (s + c − d)²/(2sc)`. -/
noncomputable def tanT (s co ds d : ℝ) : ℝ :=
  (s + co - ds) ^ 2 / (2 * s * co) - (s + co - ds) * (d - ds) / (s * co)

/-- **Fubini** for any measurable set of abscissae. -/
theorem volume_sq_inter_fst {c : ℝ × ℝ} {θ : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ)
    {A : Set ℝ} (hA : MeasurableSet A) :
    volume (sq c θ 1 ∩ {p | p.1 ∈ A}) =
      ∫⁻ x, A.indicator (fun x => ENNReal.ofReal (len c θ x)) x := by
  have hmeas : MeasurableSet (sq c θ 1 ∩ {p : ℝ × ℝ | p.1 ∈ A}) :=
    (isClosed_sq' c θ 1).measurableSet.inter (measurable_fst hA)
  rw [Measure.volume_eq_prod, Measure.prod_apply hmeas]
  refine lintegral_congr fun x => ?_
  by_cases hx : x ∈ A
  · rw [indicator_of_mem hx]
    have e : Prod.mk x ⁻¹' (sq c θ 1 ∩ {p : ℝ × ℝ | p.1 ∈ A}) =
        Icc (max (lowX c θ x) (lowY c θ x)) (min (upX c θ x) (upY c θ x)) := by
      ext y
      simp only [mem_preimage, mem_inter_iff, mem_ofPred_eq, mem_Icc, mem_sq_iff_slice hs hc, hx,
        and_true]
    rw [e, Real.volume_Icc, len]
  · rw [indicator_of_notMem hx]
    have e : Prod.mk x ⁻¹' (sq c θ 1 ∩ {p : ℝ × ℝ | p.1 ∈ A}) = ∅ := by
      ext y
      simp only [mem_preimage, mem_inter_iff, mem_ofPred_eq, hx, and_false, mem_empty_iff_false]
    rw [e, measure_empty]

/-- Right of `x_min + max(s, c)` the slice is cut by the two edges at the rightmost vertex. -/
lemma len_ge_right {c : ℝ × ℝ} {θ : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {x : ℝ}
    (hx : max (Real.sin θ) (Real.cos θ) ≤ x - xmin c θ) :
    (xmin c θ + Real.sin θ + Real.cos θ - x) / (Real.sin θ * Real.cos θ) ≤ len c θ x := by
  have hsc : 0 < Real.sin θ * Real.cos θ := mul_pos hs hc
  have h1 := le_trans (le_max_left _ _) hx
  have h2 := le_trans (le_max_right _ _) hx
  have e : xmin c θ + Real.sin θ + Real.cos θ - x = c.1 + (Real.cos θ + Real.sin θ) / 2 - x := by
    simp only [xmin]; ring
  rw [len, min_sub_max, upX_sub_lowX hs, upY_sub_lowY hc, upY_sub_lowX hs hc, upX_sub_lowY hs hc,
    ← e]
  simp only [le_min_iff]
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;>
    first
    | exact le_rfl
    | (rw [div_le_div_iff_of_pos_right hsc]; linarith)
    | (rw [div_le_div_iff₀ hsc hs]; nlinarith)
    | (rw [div_le_div_iff₀ hsc hc]; nlinarith)

/-- The right part `Q ∩ {x ≥ a}` has area at least `(x_max − a)₊²/(2sc)` once `a` is deep. -/
theorem right_ge {c : ℝ × ℝ} {θ : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {a : ℝ}
    (hd : max (Real.sin θ) (Real.cos θ) ≤ a - xmin c θ) :
    ENNReal.ofReal (max 0 (xmin c θ + Real.sin θ + Real.cos θ - a) ^ 2 /
        (2 * Real.sin θ * Real.cos θ)) ≤ volume (sq c θ 1 ∩ {p | p.1 ∈ Ici a}) := by
  set s := Real.sin θ
  set co := Real.cos θ
  set x1 := xmin c θ + s + co
  have hsc : 0 < s * co := mul_pos hs hc
  rw [volume_sq_inter_fst hs hc measurableSet_Ici]
  rcases le_total x1 a with ha | ha
  · rw [max_eq_left (by linarith)]; simp
  rw [max_eq_right (by linarith)]
  have hcont : Continuous fun x => (x1 - x) / (s * co) := by fun_prop
  calc ENNReal.ofReal ((x1 - a) ^ 2 / (2 * s * co))
      = ENNReal.ofReal (∫ x in a..x1, (x1 - x) / (s * co)) := by
        congr 1
        rw [intervalIntegral.integral_div, intervalIntegral.integral_comp_sub_left (fun x => x)]
        simp only [sub_self, integral_id]
        field_simp
        ring
    _ = ∫⁻ x, (Ioc a x1).indicator (fun x => ENNReal.ofReal ((x1 - x) / (s * co))) x := by
        rw [lintegral_indicator measurableSet_Ioc, intervalIntegral.integral_of_le ha,
          ofReal_integral_eq_lintegral_ofReal]
        · exact (hcont.integrableOn_Icc).mono_set Ioc_subset_Icc_self
        · refine ae_restrict_of_forall_mem measurableSet_Ioc fun x hx => ?_
          exact div_nonneg (by linarith [hx.2]) hsc.le
    _ ≤ ∫⁻ x, (Ici a).indicator (fun x => ENNReal.ofReal (len c θ x)) x := by
        refine lintegral_mono fun x => ?_
        by_cases hx : x ∈ Ioc a x1
        · rw [indicator_of_mem hx, indicator_of_mem (mem_Ici.mpr hx.1.le)]
          exact ENNReal.ofReal_le_ofReal (len_ge_right hs hc (by linarith [hx.1]))
        · rw [indicator_of_notMem hx]; exact zero_le

lemma tanT_le {s co ds d : ℝ} (hs : 0 < s) (hc : 0 < co) (hk : ds ≤ s + co) :
    tanT s co ds d ≤ max 0 (s + co - d) ^ 2 / (2 * s * co) := by
  have hsc : 0 < s * co := mul_pos hs hc
  set k := s + co - ds
  have hk0 : 0 ≤ k := by simp only [k]; linarith
  have e : tanT s co ds d = (2 * k * (s + co - d) - k ^ 2) / (2 * s * co) := by
    simp only [tanT, k]; field_simp; ring
  rw [e]
  apply div_le_div_of_nonneg_right _ (by positivity)
  rcases le_total 0 (s + co - d) with h | h
  · rw [max_eq_right h]; nlinarith [sq_nonneg (s + co - d - k)]
  · rw [max_eq_left h]; nlinarith

lemma one_le_sin_add_cos {θ : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) :
    1 ≤ Real.sin θ + Real.cos θ := by
  nlinarith [Real.sin_sq_add_cos_sq θ, mul_pos hs hc]

/-- **The left cap, `tan` regime**: `|Q ∩ {x < a}| ≤ 1 − T(a − x_min)` when
`a − x_min ≥ max(s, c)` and `d* ≤ 1`. -/
theorem cap_le_tan {c : ℝ × ℝ} {θ : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {a ds : ℝ}
    (hds : ds ≤ 1) (hd : max (Real.sin θ) (Real.cos θ) ≤ a - xmin c θ) :
    volume (sq c θ 1 ∩ {p | p.1 < a}) ≤
      ENNReal.ofReal (1 - tanT (Real.sin θ) (Real.cos θ) ds (a - xmin c θ)) := by
  have hQ : MeasurableSet (sq c θ 1) := (isClosed_sq' c θ 1).measurableSet
  have hS : MeasurableSet {p : ℝ × ℝ | p.1 < a} := measurableSet_lt measurable_fst measurable_const
  have hsplit := measure_inter_add_sdiff (μ := (volume : Measure (ℝ × ℝ))) (sq c θ 1) hS
  rw [volume_sq] at hsplit
  have ed : sq c θ 1 \ {p : ℝ × ℝ | p.1 < a} = sq c θ 1 ∩ {p | p.1 ∈ Ici a} := by
    ext p; simp [not_lt]
  rw [ed] at hsplit
  have hR := right_ge hs hc hd
  have hT := tanT_le (d := a - xmin c θ) hs hc (le_trans hds (one_le_sin_add_cos hs hc))
  have e2 : Real.sin θ + Real.cos θ - (a - xmin c θ) = xmin c θ + Real.sin θ + Real.cos θ - a := by
    ring
  rw [e2] at hT
  set L := volume (sq c θ 1 ∩ {p | p.1 < a})
  set Rt := volume (sq c θ 1 ∩ {p | p.1 ∈ Ici a})
  have hLt : L ≠ ⊤ := ne_top_of_le_ne_top ENNReal.one_ne_top (hsplit ▸ le_self_add)
  have hRt : Rt ≠ ⊤ := ne_top_of_le_ne_top ENNReal.one_ne_top (hsplit ▸ le_add_self)
  have h1 : L.toReal + Rt.toReal = 1 := by
    rw [← ENNReal.toReal_add hLt hRt, hsplit, ENNReal.toReal_one]
  have h2 : tanT (Real.sin θ) (Real.cos θ) ds (a - xmin c θ) ≤ Rt.toReal := by
    refine le_trans hT ?_
    have := ENNReal.toReal_mono hRt hR
    rwa [ENNReal.toReal_ofReal (by positivity)] at this
  rw [← ENNReal.ofReal_toReal hLt]
  exact ENNReal.ofReal_le_ofReal (by linarith)

/-- **The bottom cap, `tan` regime** (through `x ↔ y`; the bound is symmetric in `s`, `c`). -/
theorem bottom_cap_le_tan {c : ℝ × ℝ} {θ : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ)
    {a ds : ℝ} (hds : ds ≤ 1) (hd : max (Real.sin θ) (Real.cos θ) ≤ a - ymin c θ) :
    volume (sq c θ 1 ∩ {p | p.2 < a}) ≤
      ENNReal.ofReal (1 - tanT (Real.sin θ) (Real.cos θ) ds (a - ymin c θ)) := by
  set θ' := Real.pi / 2 - θ
  have hs' : Real.sin θ' = Real.cos θ := Real.sin_pi_div_two_sub θ
  have hc' : Real.cos θ' = Real.sin θ := Real.cos_pi_div_two_sub θ
  have e : sq c θ 1 ∩ {p | p.2 < a} = swapXY ⁻¹' (sq (swapXY c) θ' 1 ∩ {p | p.1 < a}) := by
    rw [Set.preimage_inter, preimage_swap_sq]; rfl
  have hm : MeasurableSet (sq (swapXY c) θ' 1 ∩ {p : ℝ × ℝ | p.1 < a}) :=
    (isClosed_sq' _ _ _).measurableSet.inter (measurableSet_lt measurable_fst measurable_const)
  rw [e, measurePreserving_swapXY.measure_preimage hm.nullMeasurableSet]
  have ex : xmin (swapXY c) θ' = ymin c θ := by
    simp only [xmin, ymin, swapXY, hs', hc']; ring
  have h := cap_le_tan (c := swapXY c) (θ := θ') (a := a) (by rw [hs']; exact hc)
    (by rw [hc']; exact hs) hds (by rw [hs', hc', ex, max_comm]; exact hd)
  rw [hs', hc', ex] at h
  have et : tanT (Real.cos θ) (Real.sin θ) ds (a - ymin c θ) =
      tanT (Real.sin θ) (Real.cos θ) ds (a - ymin c θ) := by
    simp only [tanT]; ring
  rwa [et] at h

/-- `ĝ` lies above its linear branch everywhere. -/
lemma lin_le_ghat {s co : ℝ} (hs : 0 < s) (hc : 0 < co) (x : ℝ) : (x - s / 2) / co ≤ ghat s co x := by
  unfold ghat
  split_ifs with h1 h2
  · exact div_nonpos_of_nonpos_of_nonneg (by linarith) hc.le
  · rw [div_le_div_iff₀ hc (by positivity)]; nlinarith [sq_nonneg (x - s), mul_pos hs hc]
  · exact le_rfl

/-- `1 − T(d)` is the linear branch of `ĝ` at `d' = (k/s) d + c − k²/(2s) − k d*/s + s/2`. -/
lemma one_sub_tanT {s co ds d : ℝ} (hs : 0 < s) (hc : 0 < co) :
    1 - tanT s co ds d = ((s + co - ds) / s * d + (co - (s + co - ds) ^ 2 / (2 * s) -
      (s + co - ds) * ds / s + s / 2) - s / 2) / co := by
  simp only [tanT]; field_simp; ring

/-- **Inclusion–exclusion** for a Lebesgue rectangle reached only from the left and from below. -/
theorem area_ge_caps {c : ℝ × ℝ} {θ : ℝ} {a1 b1 a2 b2 g1 g2 : ℝ} (h1 : 0 ≤ g1) (h2 : 0 ≤ g2)
    (hb : ∀ p ∈ sq c θ 1, p.1 ≤ b1 ∧ p.2 ≤ b2)
    (hx : volume (sq c θ 1 ∩ {p | p.1 < a1}) ≤ ENNReal.ofReal g1)
    (hy : volume (sq c θ 1 ∩ {p | p.2 < a2}) ≤ ENNReal.ofReal g2) :
    1 - g1 - g2 ≤ (volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2)).toReal := by
  have hsub : sq c θ 1 ⊆ (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2) ∪ (sq c θ 1 ∩ {p | p.1 < a1}) ∪
      (sq c θ 1 ∩ {p | p.2 < a2}) := by
    intro p hp
    obtain ⟨k1, k2⟩ := hb p hp
    by_cases hx : p.1 < a1
    · exact Or.inl (Or.inr ⟨hp, hx⟩)
    by_cases hy : p.2 < a2
    · exact Or.inr ⟨hp, hy⟩
    exact Or.inl (Or.inl ⟨hp, ⟨not_lt.mp hx, k1⟩, ⟨not_lt.mp hy, k2⟩⟩)
  have hle := (measure_mono (μ := (volume : Measure (ℝ × ℝ))) hsub).trans
    ((measure_union_le _ _).trans (add_le_add (measure_union_le _ _) le_rfl))
  rw [volume_sq] at hle
  have hV : volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2) ≠ ⊤ :=
    ne_top_of_le_ne_top ENNReal.one_ne_top ((measure_mono inter_subset_left).trans (volume_sq c θ).le)
  have h3 : (1 : ℝ≥0∞) ≤ volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2) + ENNReal.ofReal g1 +
      ENNReal.ofReal g2 := hle.trans (add_le_add (add_le_add le_rfl hx) hy)
  have hfin : volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2) + ENNReal.ofReal g1 ≠ ⊤ :=
    ENNReal.add_ne_top.mpr ⟨hV, ENNReal.ofReal_ne_top⟩
  have h4 := ENNReal.toReal_mono (ENNReal.add_ne_top.mpr ⟨hfin, ENNReal.ofReal_ne_top⟩) h3
  rw [ENNReal.toReal_add hfin ENNReal.ofReal_ne_top, ENNReal.toReal_add hV
    ENNReal.ofReal_ne_top, ENNReal.toReal_ofReal h1, ENNReal.toReal_ofReal h2,
    ENNReal.toReal_one] at h4
  linarith

end SqArea

end SquarePacking
