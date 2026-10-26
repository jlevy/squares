import Sqpack.LebTan

/-!
# The corner of the Lebesgue square: inclusion–exclusion (`QUADRANT_EXACT.md` §4.4, E″)

Near the corner `(a₁, a₂)` of the Lebesgue rectangle `U`, the bound `1 − ĝ(d_x) − ĝ(d_y)` drops the area
`A_LL = |Q ∩ {x < a₁, y < a₂}|`, which is not small.  Here:

* `area_ge_incl_excl`: `|Q ∩ U| ≥ 1 − cap_x − cap_y + A_LL` (exact inclusion–exclusion, when `Q`
  lies left of and below the far sides of `U`);
* `corner3_ge`: in the frame at the lowest vertex, with `α = a₁ − x_BL`, `β = a₂ − y_BL`,
  `z = cβ − sα ≥ 0` and `0 ≤ α ≤ c`, `β ≤ c`, `cα + sβ ≤ 1`, `A_LL ≥ (2cαβ + s(β² − α²))/(2c)`;
* `corner3_incl`: if instead `z ≤ 0` (and `α ≤ c`), `Q ∩ {y < a₂} ⊆ {x < a₁}`;
* `xcut_ge`: in the frame at the leftmost vertex, with `α = a₁ − x_TL ≤ s`, `β = a₂ − y_TL ≤ 0`,
  `z′ = cα + sβ ≥ 0`, `A_LL ≥ z′²/(2sc)`.

Each lower bound is the area of a region between two graphs inside the square
(`vol_ge_between`, Mathlib's `volume_regionBetween_eq_integral`).
-/

open MeasureTheory Set
open scoped ENNReal

namespace SquarePacking

namespace SqArea

/-- **A region between two graphs inside the square**, in the centred coordinates `v` of `Q`. -/
theorem vol_ge_between {c : ℝ × ℝ} {θ : ℝ} {S : Set (ℝ × ℝ)} {l h : ℝ} (hlh : l ≤ h)
    {f g : ℝ → ℝ} (hf : Continuous f) (hg : Continuous g) (hfg : ∀ x ∈ Ioo l h, f x ≤ g x)
    (hsub : ∀ v : ℝ × ℝ, v.1 ∈ Ioo l h → v.2 ∈ Ioo (f v.1) (g v.1) → v ∈ ub ∧ pos c θ v ∈ S) :
    ENNReal.ofReal (∫ x in l..h, (g x - f x)) ≤ volume (sq c θ 1 ∩ S) := by
  rw [volume_sq_inter]
  have hR : regionBetween f g (Ioo l h) ⊆ ub ∩ pos c θ ⁻¹' S := fun v hv =>
    ⟨(hsub v hv.1 hv.2).1, (hsub v hv.1 hv.2).2⟩
  calc ENNReal.ofReal (∫ x in l..h, (g x - f x))
      = ENNReal.ofReal (∫ x in Ioo l h, (g - f) x) := by
        rw [intervalIntegral.integral_of_le hlh, integral_Ioc_eq_integral_Ioo]; rfl
    _ = volume (regionBetween f g (Ioo l h)) := by
        rw [Measure.volume_eq_prod, volume_regionBetween_eq_integral
          ((hf.integrableOn_Icc).mono_set Ioo_subset_Icc_self)
          ((hg.integrableOn_Icc).mono_set Ioo_subset_Icc_self) measurableSet_Ioo hfg]
    _ ≤ volume (ub ∩ pos c θ ⁻¹' S) := measure_mono hR

lemma integral_affine (p q l h : ℝ) :
    ∫ x in l..h, (p * x + q) = p * (h ^ 2 - l ^ 2) / 2 + q * (h - l) := by
  have h1 : IntervalIntegrable (fun x : ℝ => p * x) volume l h :=
    (continuous_const.mul continuous_id).intervalIntegrable _ _
  rw [intervalIntegral.integral_add h1 intervalIntegrable_const, intervalIntegral.integral_const_mul,
    integral_id, intervalIntegral.integral_const, smul_eq_mul]
  ring

lemma pos_apply (c : ℝ × ℝ) (θ : ℝ) (v : ℝ × ℝ) :
    pos c θ v = (c.1 + Real.cos θ * v.1 - Real.sin θ * v.2, c.2 + Real.sin θ * v.1 + Real.cos θ * v.2) := by
  simp only [pos, rotL_apply]; ext <;> simp <;> ring

lemma mem_ub {v : ℝ × ℝ} (h1 : -(1 / 2) < v.1) (h2 : v.1 < 1 / 2) (h3 : -(1 / 2) < v.2)
    (h4 : v.2 < 1 / 2) : v ∈ ub := by
  simp only [ub, mem_ofPred_eq, abs_le]; exact ⟨⟨h1.le, h2.le⟩, h3.le, h4.le⟩

/-- **xcut**: frame at the leftmost vertex `TL`; `α = a₁ − x_TL ≤ s`, `β = a₂ − y_TL ≤ 0`,
`z′ = cα + sβ ≥ 0`.  The part of the `x`-cap below `y = a₂` is a triangle of area `z′²/(2sc)`. -/
theorem xcut_ge {c : ℝ × ℝ} {θ a1 a2 : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ)
    (hα : a1 - c.1 + (Real.cos θ + Real.sin θ) / 2 ≤ Real.sin θ)
    (hβ : a2 - c.2 - (Real.cos θ - Real.sin θ) / 2 ≤ 0)
    (hz : 0 ≤ Real.cos θ * (a1 - c.1 + (Real.cos θ + Real.sin θ) / 2) +
      Real.sin θ * (a2 - c.2 - (Real.cos θ - Real.sin θ) / 2)) :
    ENNReal.ofReal ((Real.cos θ * (a1 - c.1 + (Real.cos θ + Real.sin θ) / 2) +
        Real.sin θ * (a2 - c.2 - (Real.cos θ - Real.sin θ) / 2)) ^ 2 /
        (2 * Real.sin θ * Real.cos θ)) ≤
      volume (sq c θ 1 ∩ ({p | p.1 < a1} ∩ {p | p.2 < a2})) := by
  set s := Real.sin θ with hsdef
  set co := Real.cos θ with hcdef
  have hsc : s ^ 2 + co ^ 2 = 1 := Real.sin_sq_add_cos_sq θ
  set α := a1 - c.1 + (co + s) / 2 with hαdef
  set β := a2 - c.2 - (co - s) / 2 with hβdef
  set z := co * α + s * β with hzdef
  have hscp : 0 < s * co := mul_pos hs hc
  have hz1 : z ≤ 1 := by nlinarith [sq_nonneg (s - co)]
  -- `η` between `(sξ − β)/c` and `(α − cξ)/s`, `ξ = v₁ + ½`, `v₂ = ½ − η`
  have key := vol_ge_between (c := c) (θ := θ) (S := {p | p.1 < a1} ∩ {p | p.2 < a2})
    (l := -(1 / 2)) (h := z - 1 / 2) (by linarith)
    (f := fun x => 1 / 2 - (α - co * (x + 1 / 2)) / s)
    (g := fun x => 1 / 2 - (s * (x + 1 / 2) - β) / co) (by fun_prop) (by fun_prop)
    (fun x hx => by
      have e : (α - co * (x + 1 / 2)) / s - (s * (x + 1 / 2) - β) / co = (z - (x + 1 / 2)) / (s * co) := by
        field_simp; linear_combination (-2 * (x + 1 / 2)) * hsc
      have : 0 ≤ (z - (x + 1 / 2)) / (s * co) := div_nonneg (by linarith [hx.2]) hscp.le
      linarith)
    (fun v h1 h2 => by
      obtain ⟨hl, hh⟩ := h1
      obtain ⟨hf, hg⟩ := h2
      have gη : (α - co * (v.1 + 1 / 2)) / s ≤ 1 := by
        rw [div_le_one hs]; nlinarith
      have fη : 0 ≤ (s * (v.1 + 1 / 2) - β) / co := div_nonneg (by nlinarith) hc.le
      refine ⟨mem_ub hl (by linarith) (by linarith) (by linarith), ?_, ?_⟩
      · show (pos c θ v).1 < a1
        simp only [pos_apply]
        have : v.2 * s > (1 / 2 - (α - co * (v.1 + 1 / 2)) / s) * s := mul_lt_mul_of_pos_right hf hs
        rw [sub_mul, div_mul_cancel₀ _ hs.ne'] at this
        linarith
      · show (pos c θ v).2 < a2
        simp only [pos_apply]
        have : v.2 * co < (1 / 2 - (s * (v.1 + 1 / 2) - β) / co) * co := mul_lt_mul_of_pos_right hg hc
        rw [sub_mul, div_mul_cancel₀ _ hc.ne'] at this
        linarith)
  refine le_trans (le_of_eq ?_) key
  congr 1
  rw [intervalIntegral.integral_congr (g := fun x => (-(1 / (s * co))) * x + (z - 1 / 2) / (s * co))
    (fun x _ => by simp only; field_simp; linear_combination (-2 * (x + 1 / 2)) * hsc), integral_affine]
  field_simp
  ring

/-- **corner3**: frame at the lowest vertex `BL`; `α = a₁ − x_BL ∈ [0, c]`, `β = a₂ − y_BL ≤ c`,
`z = cβ − sα ≥ 0`, `cα + sβ ≤ 1`.  Then `A_LL ≥ (2cαβ + s(β² − α²))/(2c)` (in fact equal). -/
theorem corner3_ge {c : ℝ × ℝ} {θ a1 a2 : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ)
    (hα0 : 0 ≤ a1 - c.1 + (Real.cos θ - Real.sin θ) / 2)
    (hα1 : a1 - c.1 + (Real.cos θ - Real.sin θ) / 2 ≤ Real.cos θ)
    (hβ1 : a2 - c.2 + (Real.sin θ + Real.cos θ) / 2 ≤ Real.cos θ)
    (hz : 0 ≤ Real.cos θ * (a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) -
      Real.sin θ * (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2))
    (hx : Real.cos θ * (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2) +
      Real.sin θ * (a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) ≤ 1) :
    ENNReal.ofReal ((2 * Real.cos θ * (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2) *
        (a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) + Real.sin θ *
        ((a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) ^ 2 - (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2) ^ 2)) /
        (2 * Real.cos θ)) ≤
      volume (sq c θ 1 ∩ ({p | p.1 < a1} ∩ {p | p.2 < a2})) := by
  set s := Real.sin θ with hsdef
  set co := Real.cos θ with hcdef
  have hsc : s ^ 2 + co ^ 2 = 1 := Real.sin_sq_add_cos_sq θ
  set α := a1 - c.1 + (co - s) / 2 with hαdef
  set β := a2 - c.2 + (s + co) / 2 with hβdef
  set xs := co * α + s * β with hxsdef
  have hscp : 0 < s * co := mul_pos hs hc
  have hm0 : 0 ≤ α / co := div_nonneg hα0 hc.le
  have hm1 : α / co ≤ xs := by
    rw [div_le_iff₀ hc]; nlinarith
  have hsb : s * xs ≤ β := by nlinarith
  set f : ℝ → ℝ := fun x => max (-(1 / 2)) ((co * (x + 1 / 2) - α) / s - 1 / 2) with hfdef
  set g : ℝ → ℝ := fun x => (β - s * (x + 1 / 2)) / co - 1 / 2 with hgdef
  have key := vol_ge_between (c := c) (θ := θ) (S := {p | p.1 < a1} ∩ {p | p.2 < a2})
    (l := -(1 / 2)) (h := xs - 1 / 2) (by linarith) (f := f) (g := g) (by fun_prop) (by fun_prop)
    (fun x hx => by
      obtain ⟨h1, h2⟩ := hx
      simp only [hfdef, hgdef]
      refine max_le ?_ ?_
      · have : 0 ≤ (β - s * (x + 1 / 2)) / co := div_nonneg (by nlinarith) hc.le
        linarith
      · have e : (β - s * (x + 1 / 2)) / co - (co * (x + 1 / 2) - α) / s = (xs - (x + 1 / 2)) / (s * co) := by
          field_simp; linear_combination (-2 * (x + 1 / 2)) * hsc
        have : 0 ≤ (xs - (x + 1 / 2)) / (s * co) := div_nonneg (by linarith) hscp.le
        linarith)
    (fun v h1 h2 => by
      obtain ⟨hl, hh⟩ := h1
      obtain ⟨hf, hg⟩ := h2
      simp only [hfdef, hgdef, max_lt_iff] at hf hg
      obtain ⟨hf1, hf2⟩ := hf
      have gη : (β - s * (v.1 + 1 / 2)) / co ≤ 1 := by
        rw [div_le_one hc]; nlinarith
      refine ⟨mem_ub hl (by linarith) hf1 (by linarith), ?_, ?_⟩
      · show (pos c θ v).1 < a1
        simp only [pos_apply]
        have : (co * (v.1 + 1 / 2) - α) / s < v.2 + 1 / 2 := by linarith
        rw [div_lt_iff₀ hs] at this
        linarith
      · show (pos c θ v).2 < a2
        simp only [pos_apply]
        have : v.2 + 1 / 2 < (β - s * (v.1 + 1 / 2)) / co := by linarith
        rw [lt_div_iff₀ hc] at this
        linarith)
  refine le_trans (le_of_eq ?_) key
  congr 1
  have hcont : Continuous fun x => g x - f x := by fun_prop
  rw [← intervalIntegral.integral_add_adjacent_intervals (b := α / co - 1 / 2)
    (hcont.intervalIntegrable _ _) (hcont.intervalIntegrable _ _)]
  rw [intervalIntegral.integral_congr (g := fun x => (-(s / co)) * x + (β - s / 2) / co)
    (fun x hx => by
      rw [uIcc_of_le (by linarith)] at hx
      simp only [hfdef, hgdef]
      rw [max_eq_left (by
        have : (co * (x + 1 / 2) - α) / s ≤ 0 := by
          apply div_nonpos_of_nonpos_of_nonneg _ hs.le
          have h3 := (le_div_iff₀ hc).mp (show x + 1 / 2 ≤ α / co by linarith [hx.2])
          linarith
        linarith)]
      field_simp; ring), integral_affine]
  rw [intervalIntegral.integral_congr (g := fun x => (-(s / co + co / s)) * x +
      ((β - s / 2) / co - (co / 2 - α) / s))
    (fun x hx => by
      rw [uIcc_of_le (by linarith)] at hx
      simp only [hfdef, hgdef]
      rw [max_eq_right (by
        have : 0 ≤ (co * (x + 1 / 2) - α) / s := by
          apply div_nonneg _ hs.le
          have h2 := hx.1
          have : α ≤ co * (x + 1 / 2) := by
            have := (div_le_iff₀ hc).mp (show α / co ≤ x + 1 / 2 by linarith); linarith
          linarith
        linarith)]
      field_simp; ring), integral_affine]
  clear_value α β xs f g
  subst hxsdef
  have e : ∀ K : ℝ, s ^ 2 + co ^ 2 - 1 = 0 → (s ^ 2 + co ^ 2 - 1) * K = 0 := fun K h => by rw [h, zero_mul]
  have key2 := e ((α * co - α + β * s) * (α * co + α + β * s) / (2 * co * s)) (by linarith)
  rw [← sub_eq_zero, ← key2]
  field_simp
  ring

/-- **corner3, `z ≤ 0`**: the bottom cap lies left of `x = a`. -/
theorem corner3_incl {c : ℝ × ℝ} {θ a1 a2 : ℝ} (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ)
    (hα1 : a1 - c.1 + (Real.cos θ - Real.sin θ) / 2 ≤ Real.cos θ)
    (hz : Real.cos θ * (a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) -
      Real.sin θ * (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2) ≤ 0) :
    sq c θ 1 ∩ {p | p.2 < a2} ⊆ {p | p.1 < a1} := by
  set s := Real.sin θ with hsdef
  set co := Real.cos θ with hcdef
  intro p ⟨hp, hy⟩
  rw [← pos_coord c θ p] at hy ⊢
  set v := coord c θ p
  have hv : |v.1| ≤ 1 / 2 ∧ |v.2| ≤ 1 / 2 := hp
  rw [abs_le, abs_le] at hv
  simp only [mem_ofPred_eq, pos_apply] at hy ⊢
  -- `ξ = v₁ + ½ < β/s`, so `cξ − sη ≤ cξ < cβ/s ≤ α`
  have h1 : s * (v.1 + 1 / 2) < a2 - c.2 + (s + co) / 2 := by nlinarith
  have h2 : co * (v.1 + 1 / 2) * s < co * (a2 - c.2 + (s + co) / 2) := by nlinarith
  have h3 : co * (v.1 + 1 / 2) < a1 - c.1 + (co - s) / 2 := by nlinarith
  nlinarith

/-- **Inclusion–exclusion**: `|Q ∩ U| ≥ 1 − cap_x − cap_y + A_LL` when `Q` lies left of and below
the far sides of `U`. -/
theorem area_ge_incl_excl {c : ℝ × ℝ} {θ a1 b1 a2 b2 : ℝ}
    (hb : ∀ p ∈ sq c θ 1, p.1 ≤ b1 ∧ p.2 ≤ b2) :
    1 - (volume (sq c θ 1 ∩ {p | p.1 < a1})).toReal - (volume (sq c θ 1 ∩ {p | p.2 < a2})).toReal +
        (volume (sq c θ 1 ∩ ({p | p.1 < a1} ∩ {p | p.2 < a2}))).toReal ≤
      (volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2)).toReal := by
  set Q := sq c θ 1
  set A := Q ∩ {p : ℝ × ℝ | p.1 < a1}
  set B := Q ∩ {p : ℝ × ℝ | p.2 < a2}
  set V := Q ∩ Icc a1 b1 ×ˢ Icc a2 b2
  have hQ : MeasurableSet Q := (isClosed_sq' c θ 1).measurableSet
  have hB : MeasurableSet B := hQ.inter (measurableSet_lt measurable_snd measurable_const)
  have hsub : Q ⊆ V ∪ (A ∪ B) := by
    intro p hp
    obtain ⟨k1, k2⟩ := hb p hp
    by_cases hx : p.1 < a1
    · exact Or.inr (Or.inl ⟨hp, hx⟩)
    by_cases hy : p.2 < a2
    · exact Or.inr (Or.inr ⟨hp, hy⟩)
    exact Or.inl ⟨hp, ⟨not_lt.mp hx, k1⟩, ⟨not_lt.mp hy, k2⟩⟩
  have fin : ∀ T ⊆ Q, volume T ≠ ⊤ := fun T hT =>
    ne_top_of_le_ne_top ENNReal.one_ne_top ((measure_mono hT).trans (volume_sq c θ).le)
  have hAB : A ∩ B = Q ∩ ({p | p.1 < a1} ∩ {p | p.2 < a2}) := by
    ext p; simp only [A, B, mem_inter_iff]; tauto
  have hui := measure_union_add_inter (μ := (volume : Measure (ℝ × ℝ))) A hB
  rw [hAB] at hui
  have h1 : (1 : ℝ≥0∞) ≤ volume V + volume (A ∪ B) := by
    rw [← volume_sq c θ]; exact (measure_mono hsub).trans (measure_union_le _ _)
  have hV := fin V inter_subset_left
  have hA := fin A inter_subset_left
  have hBt := fin B inter_subset_left
  have hU : volume (A ∪ B) ≠ ⊤ := fin _ (union_subset inter_subset_left inter_subset_left)
  have hI := fin (Q ∩ ({p : ℝ × ℝ | p.1 < a1} ∩ {p | p.2 < a2})) inter_subset_left
  have r1 := ENNReal.toReal_mono (ENNReal.add_ne_top.mpr ⟨hV, hU⟩) h1
  rw [ENNReal.toReal_add hV hU, ENNReal.toReal_one] at r1
  have r2 := congrArg ENNReal.toReal hui
  rw [ENNReal.toReal_add hU hI, ENNReal.toReal_add hA hBt] at r2
  linarith

/-- **E″, corner3**: `min(1 − g_x − g_y + M, 1 − g_x) ≤ |Q ∩ U|` for cap bounds `g_x`, `g_y` and any
`M ≤ quad(α, β)` (BL frame). -/
theorem area_ge_corner3 {c : ℝ × ℝ} {θ a1 a2 b1 b2 gx gy M : ℝ} (hs : 0 < Real.sin θ)
    (hc : 0 < Real.cos θ) (hb : ∀ p ∈ sq c θ 1, p.1 ≤ b1 ∧ p.2 ≤ b2)
    (hgx : volume (sq c θ 1 ∩ {p | p.1 < a1}) ≤ ENNReal.ofReal gx)
    (hgy : volume (sq c θ 1 ∩ {p | p.2 < a2}) ≤ ENNReal.ofReal gy) (hgx0 : 0 ≤ gx) (hgy0 : 0 ≤ gy)
    (hα0 : 0 ≤ a1 - c.1 + (Real.cos θ - Real.sin θ) / 2)
    (hα1 : a1 - c.1 + (Real.cos θ - Real.sin θ) / 2 ≤ Real.cos θ)
    (hβ1 : a2 - c.2 + (Real.sin θ + Real.cos θ) / 2 ≤ Real.cos θ)
    (hx : Real.cos θ * (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2) +
      Real.sin θ * (a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) ≤ 1)
    (hM : M ≤ (2 * Real.cos θ * (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2) *
        (a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) + Real.sin θ *
        ((a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) ^ 2 - (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2) ^ 2)) /
        (2 * Real.cos θ)) :
    min (1 - gx - gy + M) (1 - gx) ≤ (volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2)).toReal := by
  have hie := area_ge_incl_excl (a1 := a1) (a2 := a2) hb
  have fin : ∀ T ⊆ sq c θ 1, volume T ≠ ⊤ := fun T hT =>
    ne_top_of_le_ne_top ENNReal.one_ne_top ((measure_mono hT).trans (volume_sq c θ).le)
  have tx := ENNReal.toReal_mono ENNReal.ofReal_ne_top hgx
  have ty := ENNReal.toReal_mono ENNReal.ofReal_ne_top hgy
  rw [ENNReal.toReal_ofReal hgx0] at tx
  rw [ENNReal.toReal_ofReal hgy0] at ty
  rcases le_total 0 (Real.cos θ * (a2 - c.2 + (Real.sin θ + Real.cos θ) / 2) -
      Real.sin θ * (a1 - c.1 + (Real.cos θ - Real.sin θ) / 2)) with hz | hz
  · have h := corner3_ge hs hc hα0 hα1 hβ1 hz hx
    have tq := ENNReal.toReal_mono (fin _ inter_subset_left) h
    rw [ENNReal.toReal_ofReal' ] at tq
    refine min_le_of_left_le ?_
    have : M ≤ max _ 0 := le_trans hM (le_max_left _ _)
    linarith
  · have hsub := corner3_incl hs hc hα1 hz
    have e : sq c θ 1 ∩ ({p : ℝ × ℝ | p.1 < a1} ∩ {p | p.2 < a2}) = sq c θ 1 ∩ {p | p.2 < a2} := by
      ext p; constructor
      · rintro ⟨h1, -, h3⟩; exact ⟨h1, h3⟩
      · rintro ⟨h1, h3⟩; exact ⟨h1, hsub ⟨h1, h3⟩, h3⟩
    rw [e] at hie
    refine min_le_of_right_le ?_
    linarith

/-- **E″, xcut**: `min(1 − g_y + M, 1 − g_x − g_y) ≤ |Q ∩ U|` for any `M ≤ quad(α, β)` (TL frame,
`α = a₁ − x_TL ≤ s`, `β = a₂ − y_TL ≤ 0`). -/
theorem area_ge_xcut {c : ℝ × ℝ} {θ a1 a2 b1 b2 gx gy M : ℝ} (hs : 0 < Real.sin θ)
    (hc : 0 < Real.cos θ) (hb : ∀ p ∈ sq c θ 1, p.1 ≤ b1 ∧ p.2 ≤ b2)
    (hgx : volume (sq c θ 1 ∩ {p | p.1 < a1}) ≤ ENNReal.ofReal gx)
    (hgy : volume (sq c θ 1 ∩ {p | p.2 < a2}) ≤ ENNReal.ofReal gy) (hgx0 : 0 ≤ gx) (hgy0 : 0 ≤ gy)
    (hα : a1 - c.1 + (Real.cos θ + Real.sin θ) / 2 ≤ Real.sin θ)
    (hβ : a2 - c.2 - (Real.cos θ - Real.sin θ) / 2 ≤ 0)
    (hM : M ≤ (2 * Real.cos θ * (a1 - c.1 + (Real.cos θ + Real.sin θ) / 2) *
        (a2 - c.2 - (Real.cos θ - Real.sin θ) / 2) + Real.sin θ *
        ((a2 - c.2 - (Real.cos θ - Real.sin θ) / 2) ^ 2 - (a1 - c.1 + (Real.cos θ + Real.sin θ) / 2) ^ 2)) /
        (2 * Real.cos θ)) :
    min (1 - gy + M) (1 - gx - gy) ≤ (volume (sq c θ 1 ∩ Icc a1 b1 ×ˢ Icc a2 b2)).toReal := by
  have hie := area_ge_incl_excl (a1 := a1) (a2 := a2) hb
  have fin : ∀ T ⊆ sq c θ 1, volume T ≠ ⊤ := fun T hT =>
    ne_top_of_le_ne_top ENNReal.one_ne_top ((measure_mono hT).trans (volume_sq c θ).le)
  have ty := ENNReal.toReal_mono ENNReal.ofReal_ne_top hgy
  rw [ENNReal.toReal_ofReal hgy0] at ty
  have hI0 : 0 ≤ (volume (sq c θ 1 ∩ ({p : ℝ × ℝ | p.1 < a1} ∩ {p | p.2 < a2}))).toReal :=
    ENNReal.toReal_nonneg
  set s := Real.sin θ with hsdef
  set co := Real.cos θ with hcdef
  have hsc : s ^ 2 + co ^ 2 = 1 := Real.sin_sq_add_cos_sq θ
  rcases le_total 0 (co * (a1 - c.1 + (co + s) / 2) + s * (a2 - c.2 - (co - s) / 2)) with hz | hz
  · refine min_le_of_left_le ?_
    have h := xcut_ge hs hc hα hβ hz
    have tq := ENNReal.toReal_mono (fin _ inter_subset_left) h
    rw [ENNReal.toReal_ofReal (by positivity)] at tq
    -- the `x`-cap is the triangle: `cap_x ≤ α²/(2sc)`
    have hα0 : 0 ≤ a1 - c.1 + (co + s) / 2 := by nlinarith
    have hcx := cap_le_ghat (c := c) hs hc a1
    have ex : a1 - xmin c θ = a1 - c.1 + (co + s) / 2 := by simp only [xmin, hsdef, hcdef]; ring
    rw [ex] at hcx
    have gpar : ghat s co (a1 - c.1 + (co + s) / 2) ≤ (a1 - c.1 + (co + s) / 2) ^ 2 / (2 * s * co) := by
      unfold ghat; split_ifs <;> first | positivity | exact le_rfl | linarith
    have tx := ENNReal.toReal_mono ENNReal.ofReal_ne_top hcx
    rw [ENNReal.toReal_ofReal (ghat_nonneg hs hc)] at tx
    have iden : -(a1 - c.1 + (co + s) / 2) ^ 2 / (2 * s * co) +
        (co * (a1 - c.1 + (co + s) / 2) + s * (a2 - c.2 - (co - s) / 2)) ^ 2 / (2 * s * co) =
        (2 * co * (a1 - c.1 + (co + s) / 2) * (a2 - c.2 - (co - s) / 2) + s *
          ((a2 - c.2 - (co - s) / 2) ^ 2 - (a1 - c.1 + (co + s) / 2) ^ 2)) / (2 * co) := by
      rw [← sub_eq_zero]
      have k : ∀ A B : ℝ, -A ^ 2 / (2 * s * co) + (co * A + s * B) ^ 2 / (2 * s * co) -
          (2 * co * A * B + s * (B ^ 2 - A ^ 2)) / (2 * co) = (s ^ 2 + co ^ 2 - 1) * (A ^ 2 / (2 * co * s)) := by
        intro A B; field_simp; ring
      rw [k, show s ^ 2 + co ^ 2 - 1 = 0 by linarith, zero_mul]
    try rw [← hsdef, ← hcdef] at tq
    try rw [← hsdef, ← hcdef] at tx
    rw [neg_div] at iden
    linarith [tx.trans gpar]
  · refine min_le_of_right_le ?_
    have tx := ENNReal.toReal_mono ENNReal.ofReal_ne_top hgx
    rw [ENNReal.toReal_ofReal hgx0] at tx
    linarith

end SqArea

end SquarePacking
