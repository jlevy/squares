import Sqpack.Basic

/-!
# Areas of pieces of a closed unit square (the Lebesgue part of a mixed cover)

A mixed cover may carry mass uniformly by area on a polygon (`MixedMeasure.lean`, `areaMeasure`); a
checker then needs the area of `Q ∩ P` for the closed unit square `Q = sq c θ 1`, or bounds on it.
This file proves the facts the Lebesgue leaves of `search/QUADRANT_EXACT.md` §4 use, once, for any
pose.

* `volume_sq_inter`, **`volume_sq`** — `Q` is the image of the axis-parallel unit square under a
  rotation and a translation, both area-preserving: `|Q ∩ S| = |U ∩ pos⁻¹ S|`, `|Q| = 1`.
* `mem_sq_iff_slice` — for `0 < θ < π/2` the vertical slice of `Q` at abscissa `x` is the interval
  `[max(lowX, lowY), min(upX, upY)]` cut out by the four edges.
* `volume_sq_inter_Iio` — Fubini: `|Q ∩ {x < a}| = ∫_{x < a} len(x)`, `len` the slice length.
* `len_le_lin`, `len_le_inv_cos`, `len_mono` — the slice length is at most `(x − x_min)/(sc)`
  (the two edges at the leftmost vertex) and at most `1/c` (`s = sin θ`, `c = cos θ`), and is
  non-decreasing on `x ≤ a ≤ c_x`.
* **`cap_le_ghat`** — the left cap: `|Q ∩ {x < a}| ≤ ĝ(d)`, `d = a − x_min`, with `ĝ(d) = d²/(2sc)`
  for `d ≤ s` and `(d − s/2)/c` beyond (`QUADRANT_EXACT.md` §4.4, E′: `ĝ ≥ g`).
* **`cap_le_chord`** — the width lemma of Lemma K: for `a ≤ c_x`, `|Q ∩ {x < a}| ≤ d · len(a)`.

The other three caps follow by the symmetries `x ↦ m − x`, `x ↔ y` (`D4.lean`).
-/

open MeasureTheory Set
open scoped ENNReal

namespace SquarePacking
namespace SqArea

/-! ## 1.  Rotations preserve area -/

/-- The rotation by `θ`. -/
noncomputable def rotL (θ : ℝ) : (ℝ × ℝ) →ₗ[ℝ] (ℝ × ℝ) :=
  Matrix.toLin (Module.Basis.finTwoProd ℝ) (Module.Basis.finTwoProd ℝ)
    !![Real.cos θ, -Real.sin θ; Real.sin θ, Real.cos θ]

lemma rotL_apply (θ : ℝ) (v : ℝ × ℝ) :
    rotL θ v = (Real.cos θ * v.1 + -Real.sin θ * v.2, Real.sin θ * v.1 + Real.cos θ * v.2) := by
  rw [rotL, Matrix.toLin_finTwoProd_apply]

lemma det_rotL (θ : ℝ) : LinearMap.det (rotL θ) = 1 := by
  rw [rotL, LinearMap.det_toLin, Matrix.det_fin_two_of]
  nlinarith [Real.sin_sq_add_cos_sq θ]

lemma volume_image_rotL (θ : ℝ) (A : Set (ℝ × ℝ)) : volume (rotL θ '' A) = volume A := by
  rw [MeasureTheory.Measure.addHaar_image_linearMap, det_rotL]
  simp

/-- The point of rotated offset `v` from the centre `c`: the inverse of `coord c θ`. -/
noncomputable def pos (c : ℝ × ℝ) (θ : ℝ) (v : ℝ × ℝ) : ℝ × ℝ := c + rotL θ v

lemma coord_pos (c : ℝ × ℝ) (θ : ℝ) (v : ℝ × ℝ) : coord c θ (pos c θ v) = v := by
  have h := Real.sin_sq_add_cos_sq θ
  simp only [coord, pos, rotL_apply, Prod.fst_add, Prod.snd_add]
  ext
  · simp only; linear_combination v.1 * h
  · simp only; linear_combination v.2 * h

lemma pos_coord (c : ℝ × ℝ) (θ : ℝ) (p : ℝ × ℝ) : pos c θ (coord c θ p) = p := by
  have h := Real.sin_sq_add_cos_sq θ
  simp only [coord, pos, rotL_apply]
  ext
  · simp only [Prod.fst_add]; linear_combination (p.1 - c.1) * h
  · simp only [Prod.snd_add]; linear_combination (p.2 - c.2) * h

lemma volume_image_pos (c : ℝ × ℝ) (θ : ℝ) (A : Set (ℝ × ℝ)) :
    volume (pos c θ '' A) = volume A := by
  have e : pos c θ '' A = (fun x => c + x) '' (rotL θ '' A) := by
    rw [Set.image_image]; rfl
  rw [e, Set.image_add_left, measure_preimage_add, volume_image_rotL]

/-- The axis-parallel closed unit square centred at the origin. -/
def ub : Set (ℝ × ℝ) := {v | |v.1| ≤ 1 / 2 ∧ |v.2| ≤ 1 / 2}

lemma ub_eq : ub = Icc (-(1 / 2 : ℝ)) (1 / 2) ×ˢ Icc (-(1 / 2 : ℝ)) (1 / 2) := by
  ext v; simp only [ub, mem_ofPred_eq, mem_prod, mem_Icc, abs_le]

lemma volume_ub : volume ub = 1 := by
  rw [ub_eq, Measure.volume_eq_prod, Measure.prod_prod, Real.volume_Icc]
  norm_num

lemma sq_inter_eq_image (c : ℝ × ℝ) (θ : ℝ) (S : Set (ℝ × ℝ)) :
    sq c θ 1 ∩ S = pos c θ '' (ub ∩ pos c θ ⁻¹' S) := by
  ext p
  constructor
  · rintro ⟨hq, hS⟩
    refine ⟨coord c θ p, ⟨?_, ?_⟩, pos_coord c θ p⟩
    · simpa [ub, sq] using hq
    · simpa [pos_coord] using hS
  · rintro ⟨v, ⟨hv, hS⟩, rfl⟩
    refine ⟨?_, hS⟩
    simpa [sq, ub, coord_pos] using hv

/-- **The area of a piece of `Q`** is the area of the corresponding piece of the axis-parallel
unit square. -/
theorem volume_sq_inter (c : ℝ × ℝ) (θ : ℝ) (S : Set (ℝ × ℝ)) :
    volume (sq c θ 1 ∩ S) = volume (ub ∩ pos c θ ⁻¹' S) := by
  rw [sq_inter_eq_image, volume_image_pos]

/-- **A closed unit square has area `1`**, at every position and angle. -/
theorem volume_sq (c : ℝ × ℝ) (θ : ℝ) : volume (sq c θ 1) = 1 := by
  have h := volume_sq_inter c θ univ
  rw [inter_univ, preimage_univ, inter_univ, volume_ub] at h
  exact h

/-- A closed unit square inside a region has all of its area there. -/
lemma volume_sq_inter_of_subset {c : ℝ × ℝ} {θ : ℝ} {P : Set (ℝ × ℝ)} (h : sq c θ 1 ⊆ P) :
    volume (sq c θ 1 ∩ P) = 1 := by
  rw [inter_eq_left.mpr h, volume_sq]

lemma isClosed_sq' (c : ℝ × ℝ) (θ L : ℝ) : IsClosed (sq c θ L) := by
  have hc : Continuous (coord c θ) := by unfold coord; fun_prop
  have e : sq c θ L = {p | |(coord c θ p).1| ≤ L / 2} ∩ {p | |(coord c θ p).2| ≤ L / 2} := rfl
  rw [e]
  exact (isClosed_le hc.fst.abs continuous_const).inter (isClosed_le hc.snd.abs continuous_const)

/-! ## 2.  Vertical slices, for `0 < θ < π/2` -/

section slices

variable (c : ℝ × ℝ) (θ : ℝ)

/-- The four edges of `Q` as functions of the abscissa `x` (`s = sin θ > 0`, `c = cos θ > 0`):
`|X| ≤ ½` gives `lowX ≤ y ≤ upX`, `|Y| ≤ ½` gives `lowY ≤ y ≤ upY`. -/
noncomputable def lowX (x : ℝ) : ℝ := c.2 + (-(1 / 2) - (x - c.1) * Real.cos θ) / Real.sin θ
noncomputable def upX (x : ℝ) : ℝ := c.2 + (1 / 2 - (x - c.1) * Real.cos θ) / Real.sin θ
noncomputable def lowY (x : ℝ) : ℝ := c.2 + ((x - c.1) * Real.sin θ - 1 / 2) / Real.cos θ
noncomputable def upY (x : ℝ) : ℝ := c.2 + ((x - c.1) * Real.sin θ + 1 / 2) / Real.cos θ

/-- The length of the vertical slice of `Q` at `x` (possibly negative: then the slice is empty). -/
noncomputable def len (x : ℝ) : ℝ :=
  min (upX c θ x) (upY c θ x) - max (lowX c θ x) (lowY c θ x)

/-- The abscissa of the leftmost vertex. -/
noncomputable def xmin : ℝ := c.1 - (Real.cos θ + Real.sin θ) / 2

variable {c θ}

lemma mem_sq_iff_slice (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (x y : ℝ) :
    (x, y) ∈ sq c θ 1 ↔ max (lowX c θ x) (lowY c θ x) ≤ y ∧ y ≤ min (upX c θ x) (upY c θ x) := by
  have k1 : ∀ (A b : ℝ) {k : ℝ}, 0 < k → (c.2 + A / k ≤ b ↔ A ≤ (b - c.2) * k) := by
    intro A b k hk; rw [← le_sub_iff_add_le', div_le_iff₀ hk]
  have k2 : ∀ (A b : ℝ) {k : ℝ}, 0 < k → (b ≤ c.2 + A / k ↔ (b - c.2) * k ≤ A) := by
    intro A b k hk; rw [← sub_le_iff_le_add', le_div_iff₀ hk]
  simp only [sq, coord, mem_ofPred_eq, abs_le, max_le_iff, le_min_iff, lowX, upX, lowY, upY]
  rw [k1 _ _ hs, k1 _ _ hc, k2 _ _ hs, k2 _ _ hc]
  constructor
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> nlinarith
  · rintro ⟨⟨h1, h2⟩, h3, h4⟩
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;> nlinarith

/-- **Fubini**: the area of the part of `Q` left of `x = a` is the integral of the slice length. -/
theorem volume_sq_inter_Iio (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (a : ℝ) :
    volume (sq c θ 1 ∩ {p | p.1 < a}) =
      ∫⁻ x, (Iio a).indicator (fun x => ENNReal.ofReal (len c θ x)) x := by
  have hmeas : MeasurableSet (sq c θ 1 ∩ {p : ℝ × ℝ | p.1 < a}) :=
    (isClosed_sq' c θ 1).measurableSet.inter (measurableSet_lt measurable_fst measurable_const)
  rw [Measure.volume_eq_prod, Measure.prod_apply hmeas]
  refine lintegral_congr fun x => ?_
  by_cases hx : x < a
  · rw [indicator_of_mem (mem_Iio.mpr hx)]
    have e : Prod.mk x ⁻¹' (sq c θ 1 ∩ {p : ℝ × ℝ | p.1 < a}) =
        Icc (max (lowX c θ x) (lowY c θ x)) (min (upX c θ x) (upY c θ x)) := by
      ext y
      simp only [mem_preimage, mem_inter_iff, mem_ofPred_eq, mem_Icc, mem_sq_iff_slice hs hc, hx,
        and_true]
    rw [e, Real.volume_Icc, len]
  · rw [indicator_of_notMem (by simpa using hx)]
    have e : Prod.mk x ⁻¹' (sq c θ 1 ∩ {p : ℝ × ℝ | p.1 < a}) = ∅ := by
      ext y
      simp only [mem_preimage, mem_inter_iff, mem_ofPred_eq, hx, and_false, mem_empty_iff_false]
    rw [e, measure_empty]

/-- `min a b − max c d` is the least of the four differences. -/
lemma min_sub_max (a b c d : ℝ) :
    min a b - max c d = min (min (a - c) (a - d)) (min (b - c) (b - d)) := by
  apply le_antisymm
  · simp only [le_min_iff]
    refine ⟨⟨?_, ?_⟩, ?_, ?_⟩ <;>
      linarith [min_le_left a b, min_le_right a b, le_max_left c d, le_max_right c d]
  · rcases le_total a b with h1 | h1 <;> rcases le_total c d with h2 | h2
    · rw [min_eq_left h1, max_eq_right h2]; exact min_le_of_left_le (min_le_right _ _)
    · rw [min_eq_left h1, max_eq_left h2]; exact min_le_of_left_le (min_le_left _ _)
    · rw [min_eq_right h1, max_eq_right h2]; exact min_le_of_right_le (min_le_right _ _)
    · rw [min_eq_right h1, max_eq_left h2]; exact min_le_of_right_le (min_le_left _ _)

lemma upY_sub_lowX (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (x : ℝ) :
    upY c θ x - lowX c θ x = (x - xmin c θ) / (Real.sin θ * Real.cos θ) := by
  have h := Real.sin_sq_add_cos_sq θ
  simp only [upY, lowX, xmin]
  field_simp
  linear_combination 2 * (x - c.1) * h

lemma upX_sub_lowY (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (x : ℝ) :
    upX c θ x - lowY c θ x =
      (c.1 + (Real.cos θ + Real.sin θ) / 2 - x) / (Real.sin θ * Real.cos θ) := by
  have h := Real.sin_sq_add_cos_sq θ
  simp only [upX, lowY]
  field_simp
  linear_combination 2 * (c.1 - x) * h

lemma upY_sub_lowY (hc : 0 < Real.cos θ) (x : ℝ) : upY c θ x - lowY c θ x = 1 / Real.cos θ := by
  simp only [upY, lowY]; field_simp; ring

lemma upX_sub_lowX (hs : 0 < Real.sin θ) (x : ℝ) : upX c θ x - lowX c θ x = 1 / Real.sin θ := by
  simp only [upX, lowX]; field_simp; ring

/-- The slice length is at most the width between the two edges at the leftmost vertex. -/
lemma len_le_lin (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (x : ℝ) :
    len c θ x ≤ (x - xmin c θ) / (Real.sin θ * Real.cos θ) := by
  rw [len, ← upY_sub_lowX hs hc]
  exact sub_le_sub (min_le_right _ _) (le_max_left _ _)

/-- The slice length is at most `1/cos θ` (the two edges `|Y| = ½`). -/
lemma len_le_inv_cos (hc : 0 < Real.cos θ) (x : ℝ) : len c θ x ≤ 1 / Real.cos θ := by
  rw [len, ← upY_sub_lowY hc]
  exact sub_le_sub (min_le_right _ _) (le_max_right _ _)

/-- The slice length is at most `1/sin θ` (the two edges `|X| = ½`). -/
lemma len_le_inv_sin (hs : 0 < Real.sin θ) (x : ℝ) : len c θ x ≤ 1 / Real.sin θ := by
  rw [len, ← upX_sub_lowX hs]
  exact sub_le_sub (min_le_left _ _) (le_max_left _ _)

/-- **The width lemma**: left of the centre the slice length does not decrease. -/
lemma len_mono (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {x a : ℝ} (hxa : x ≤ a)
    (ha : a ≤ c.1) : len c θ x ≤ len c θ a := by
  have hsc : 0 < Real.sin θ * Real.cos θ := mul_pos hs hc
  rw [len, len, min_sub_max, min_sub_max, upX_sub_lowX hs, upX_sub_lowX hs, upY_sub_lowY hc,
    upY_sub_lowY hc, upY_sub_lowX hs hc, upY_sub_lowX hs hc, upX_sub_lowY hs hc,
    upX_sub_lowY hs hc]
  -- the decreasing difference, at `a ≤ c_x`, is at least `1/(2c) + 1/(2s) ≥ min(1/s, 1/c)`
  have hdec : min (1 / Real.sin θ) (1 / Real.cos θ) ≤
      (c.1 + (Real.cos θ + Real.sin θ) / 2 - a) / (Real.sin θ * Real.cos θ) := by
    have e : (Real.cos θ + Real.sin θ) / 2 / (Real.sin θ * Real.cos θ) =
        (1 / Real.sin θ + 1 / Real.cos θ) / 2 := by field_simp
    have h1 : (Real.cos θ + Real.sin θ) / 2 / (Real.sin θ * Real.cos θ) ≤
        (c.1 + (Real.cos θ + Real.sin θ) / 2 - a) / (Real.sin θ * Real.cos θ) :=
      div_le_div_of_nonneg_right (by linarith) hsc.le
    rw [e] at h1
    rcases le_total (1 / Real.sin θ) (1 / Real.cos θ) with h | h
    · rw [min_eq_left h]; linarith
    · rw [min_eq_right h]; linarith
  have hinc : (x - xmin c θ) / (Real.sin θ * Real.cos θ) ≤
      (a - xmin c θ) / (Real.sin θ * Real.cos θ) :=
    div_le_div_of_nonneg_right (by linarith) hsc.le
  simp only [le_min_iff]
  refine ⟨⟨?_, ?_⟩, ?_, ?_⟩
  · exact min_le_of_left_le (min_le_left _ _)
  · refine le_trans ?_ hdec
    exact le_min (min_le_of_left_le (min_le_left _ _)) (min_le_of_right_le (min_le_right _ _))
  · exact le_trans (min_le_of_right_le (min_le_left _ _)) hinc
  · exact min_le_of_right_le (min_le_right _ _)

end slices

/-! ## 3.  The left cap -/

section cap

variable {c : ℝ × ℝ} {θ : ℝ}

/-- `ĝ(d)`: `0` for `d ≤ 0`, `d²/(2sc)` for `0 ≤ d ≤ s`, `(d − s/2)/c` for `d ≥ s`. -/
noncomputable def ghat (s co d : ℝ) : ℝ :=
  if d ≤ 0 then 0 else if d ≤ s then d ^ 2 / (2 * s * co) else (d - s / 2) / co

/-- The majorant of the slice length: `min((x − x_min)/(sc), 1/c)` right of `x_min`. -/
noncomputable def capF (s co x0 x : ℝ) : ℝ := min ((x - x0) / (s * co)) (1 / co)

lemma integral_capF {s co : ℝ} (hs : 0 < s) (hc : 0 < co) (x0 d : ℝ) (hd : 0 ≤ d) :
    ∫ x in x0..x0 + d, capF s co x0 x = ghat s co d := by
  have hsc : 0 < s * co := mul_pos hs hc
  -- on `[x0, x0 + s]` the linear term is the minimum, beyond it the constant
  have hlin : ∀ x ∈ uIcc x0 (x0 + min d s), capF s co x0 x = (x - x0) / (s * co) := by
    intro x hx
    rw [uIcc_of_le (by have := le_min hd hs.le; linarith)] at hx
    refine min_eq_left ?_
    rw [div_le_div_iff₀ hsc hc]
    nlinarith [hx.2, min_le_right d s]
  have I1 : ∫ x in x0..x0 + min d s, capF s co x0 x = (min d s) ^ 2 / (2 * s * co) := by
    rw [intervalIntegral.integral_congr hlin, intervalIntegral.integral_div,
      intervalIntegral.integral_comp_sub_right (fun x => x)]
    simp only [sub_self, add_sub_cancel_left, integral_id]
    field_simp
    ring
  unfold ghat
  rcases eq_or_lt_of_le hd with h0 | hpos
  · subst h0; simp
  rw [if_neg (not_le.mpr hpos)]
  by_cases hds : d ≤ s
  · rw [if_pos hds]; rw [min_eq_left hds] at I1; exact I1
  · rw [if_neg hds]
    have hsd : s < d := not_le.mp hds
    have hcont : Continuous (capF s co x0) := by unfold capF; fun_prop
    rw [← intervalIntegral.integral_add_adjacent_intervals (b := x0 + min d s)
      (hcont.intervalIntegrable _ _) (hcont.intervalIntegrable _ _), I1, min_eq_right hsd.le]
    have hconst : ∀ x ∈ uIcc (x0 + s) (x0 + d), capF s co x0 x = 1 / co := by
      intro x hx
      rw [uIcc_of_le (by linarith)] at hx
      refine min_eq_right ?_
      rw [div_le_div_iff₀ hc hsc]
      nlinarith [hx.1]
    rw [intervalIntegral.integral_congr hconst, intervalIntegral.integral_const, smul_eq_mul]
    field_simp
    ring

/-- **The left cap** (`E′`): the area of `Q` left of `x = a` is at most `ĝ(a − x_min)`. -/
theorem cap_le_ghat (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (a : ℝ) :
    volume (sq c θ 1 ∩ {p | p.1 < a}) ≤
      ENNReal.ofReal (ghat (Real.sin θ) (Real.cos θ) (a - xmin c θ)) := by
  set x0 := xmin c θ
  rw [volume_sq_inter_Iio hs hc]
  rcases le_or_gt a x0 with ha | ha
  · -- no part of `Q` lies left of `a`
    have : ∀ x, (Iio a).indicator (fun x => ENNReal.ofReal (len c θ x)) x = 0 := by
      intro x
      by_cases hx : x < a
      · rw [indicator_of_mem (mem_Iio.mpr hx), ENNReal.ofReal_eq_zero]
        refine le_trans (len_le_lin hs hc x) ?_
        exact div_nonpos_of_nonpos_of_nonneg (by linarith) (mul_pos hs hc).le
      · exact indicator_of_notMem (by simpa using hx) _
    simp only [this, lintegral_zero, zero_le]
  · have hd : 0 ≤ a - x0 := by linarith
    have hcont : Continuous (capF (Real.sin θ) (Real.cos θ) x0) := by unfold capF; fun_prop
    calc ∫⁻ x, (Iio a).indicator (fun x => ENNReal.ofReal (len c θ x)) x
        ≤ ∫⁻ x, (Ioc x0 a).indicator
            (fun x => ENNReal.ofReal (capF (Real.sin θ) (Real.cos θ) x0 x)) x := by
          refine lintegral_mono fun x => ?_
          by_cases hx : x < a
          · rw [indicator_of_mem (mem_Iio.mpr hx)]
            by_cases hx0 : x0 < x
            · rw [indicator_of_mem (mem_Ioc.mpr ⟨hx0, hx.le⟩)]
              exact ENNReal.ofReal_le_ofReal (le_min (len_le_lin hs hc x) (len_le_inv_cos hc x))
            · rw [ENNReal.ofReal_eq_zero.mpr]
              · exact zero_le
              refine le_trans (len_le_lin hs hc x) ?_
              exact div_nonpos_of_nonpos_of_nonneg (by linarith) (mul_pos hs hc).le
          · rw [indicator_of_notMem (by simpa using hx)]
            exact zero_le
      _ = ENNReal.ofReal (∫ x in x0..x0 + (a - x0), capF (Real.sin θ) (Real.cos θ) x0 x) := by
          rw [lintegral_indicator measurableSet_Ioc, add_sub_cancel,
            intervalIntegral.integral_of_le ha.le]
          rw [ofReal_integral_eq_lintegral_ofReal]
          · exact (hcont.integrableOn_Icc).mono_set Ioc_subset_Icc_self
          · refine ae_restrict_of_forall_mem measurableSet_Ioc fun x hx => ?_
            exact le_min (div_nonneg (by linarith [hx.1]) (mul_pos hs hc).le) (by positivity)
      _ = _ := by rw [integral_capF hs hc x0 _ hd]

/-- **The width lemma of Lemma K**: left of the centre, the area of `Q` left of `x = a` is at most
the depth `a − x_min` times the chord `len(a)` of `Q` on the line `x = a`. -/
theorem cap_le_chord (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) {a : ℝ} (ha : a ≤ c.1) :
    volume (sq c θ 1 ∩ {p | p.1 < a}) ≤
      ENNReal.ofReal ((a - xmin c θ) * len c θ a) := by
  set x0 := xmin c θ
  rw [volume_sq_inter_Iio hs hc]
  have hlen0 : ∀ x, x ≤ x0 → ENNReal.ofReal (len c θ x) = 0 := fun x hx =>
    ENNReal.ofReal_eq_zero.mpr (le_trans (len_le_lin hs hc x)
      (div_nonpos_of_nonpos_of_nonneg (by linarith) (mul_pos hs hc).le))
  calc ∫⁻ x, (Iio a).indicator (fun x => ENNReal.ofReal (len c θ x)) x
      ≤ ∫⁻ x, (Ioc x0 a).indicator (fun _ => ENNReal.ofReal (len c θ a)) x := by
        refine lintegral_mono fun x => ?_
        by_cases hx : x < a
        · rw [indicator_of_mem (mem_Iio.mpr hx)]
          by_cases hx0 : x0 < x
          · rw [indicator_of_mem (mem_Ioc.mpr ⟨hx0, hx.le⟩)]
            exact ENNReal.ofReal_le_ofReal (len_mono hs hc hx.le ha)
          · rw [hlen0 x (not_lt.mp hx0)]
            exact zero_le
        · rw [indicator_of_notMem (by simpa using hx)]
          exact zero_le
    _ ≤ ENNReal.ofReal ((a - x0) * len c θ a) := by
        rw [lintegral_indicator_const measurableSet_Ioc, Real.volume_Ioc]
        rcases le_total a x0 with hax | hax
        · rw [ENNReal.ofReal_of_nonpos (by linarith : a - x0 ≤ 0), mul_zero]; exact zero_le
        · rcases le_total (len c θ a) 0 with hl | hl
          · rw [ENNReal.ofReal_of_nonpos hl, zero_mul]; exact zero_le
          · rw [ENNReal.ofReal_mul (by linarith), mul_comm]

/-- **The left cap, other plateau**: `|Q ∩ {x < a}| ≤ ĝ(d)` with the roles of `sin θ` and `cos θ`
exchanged (the slice length is also at most `1/sin θ`).  Used for the bottom cap through `x ↔ y`. -/
theorem cap_le_ghat' (hs : 0 < Real.sin θ) (hc : 0 < Real.cos θ) (a : ℝ) :
    volume (sq c θ 1 ∩ {p | p.1 < a}) ≤
      ENNReal.ofReal (ghat (Real.cos θ) (Real.sin θ) (a - xmin c θ)) := by
  set x0 := xmin c θ
  rw [volume_sq_inter_Iio hs hc]
  have hlin : ∀ x, len c θ x ≤ (x - x0) / (Real.cos θ * Real.sin θ) := fun x => by
    rw [mul_comm]; exact len_le_lin hs hc x
  rcases le_or_gt a x0 with ha | ha
  · have : ∀ x, (Iio a).indicator (fun x => ENNReal.ofReal (len c θ x)) x = 0 := by
      intro x
      by_cases hx : x < a
      · rw [indicator_of_mem (mem_Iio.mpr hx), ENNReal.ofReal_eq_zero]
        refine le_trans (hlin x) ?_
        exact div_nonpos_of_nonpos_of_nonneg (by linarith) (mul_pos hc hs).le
      · exact indicator_of_notMem (by simpa using hx) _
    simp only [this, lintegral_zero, zero_le]
  · have hd : 0 ≤ a - x0 := by linarith
    have hcont : Continuous (capF (Real.cos θ) (Real.sin θ) x0) := by unfold capF; fun_prop
    calc ∫⁻ x, (Iio a).indicator (fun x => ENNReal.ofReal (len c θ x)) x
        ≤ ∫⁻ x, (Ioc x0 a).indicator
            (fun x => ENNReal.ofReal (capF (Real.cos θ) (Real.sin θ) x0 x)) x := by
          refine lintegral_mono fun x => ?_
          by_cases hx : x < a
          · rw [indicator_of_mem (mem_Iio.mpr hx)]
            by_cases hx0 : x0 < x
            · rw [indicator_of_mem (mem_Ioc.mpr ⟨hx0, hx.le⟩)]
              exact ENNReal.ofReal_le_ofReal (le_min (hlin x) (len_le_inv_sin hs x))
            · rw [ENNReal.ofReal_eq_zero.mpr]
              · exact zero_le
              refine le_trans (hlin x) ?_
              exact div_nonpos_of_nonpos_of_nonneg (by linarith) (mul_pos hc hs).le
          · rw [indicator_of_notMem (by simpa using hx)]
            exact zero_le
      _ = ENNReal.ofReal (∫ x in x0..x0 + (a - x0), capF (Real.cos θ) (Real.sin θ) x0 x) := by
          rw [lintegral_indicator measurableSet_Ioc, add_sub_cancel,
            intervalIntegral.integral_of_le ha.le]
          rw [ofReal_integral_eq_lintegral_ofReal]
          · exact (hcont.integrableOn_Icc).mono_set Ioc_subset_Icc_self
          · refine ae_restrict_of_forall_mem measurableSet_Ioc fun x hx => ?_
            exact le_min (div_nonneg (by linarith [hx.1]) (mul_pos hc hs).le) (by positivity)
      _ = _ := by rw [integral_capF hc hs x0 _ hd]

end cap

end SqArea
end SquarePacking
