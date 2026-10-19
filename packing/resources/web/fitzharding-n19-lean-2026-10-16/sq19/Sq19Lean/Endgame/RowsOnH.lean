import Sq19Lean.Endgame.Offsets
import Sq19Lean.Endgame.OffsetBounds
import Sq19Lean.Endgame.RowsAH
import Sq19Lean.Endgame.Farkas3

/-!
# The rows on H

Each row of `RowsH`/`RowsAH` holds on every configuration of H (`Good prob θ dx dy L`), given the
case (which face separates 1-2, 13-14 / 13-11, 5-8) and the orthant (the signs of the axis angles
the row's supports depend on). Supports with a fixed sign pattern on H are certified by Taylor ranges;
supports of an axis angle against a wall depend on the orthant; anchor supports use the lower bound 1/2;
tilted-to-tilted supports are exact (`suppAbsE`).
-/
namespace Sq19.Endgame
open Sq19.Milp Sq19.Endgame.Hull

/-- `true ↦ 1`, `false ↦ -1`. -/
def sg (b : Bool) : ℚ := if b then 1 else -1

theorem sg_pm (b : Bool) : sg b = 1 ∨ sg b = -1 := by cases b <;> simp [sg]

section
variable {θ dx dy : ℕ → ℝ} {L : ℝ}

theorem nonneg_of_rngH (hg : Good prob θ dx dy L) (e : Ex) (h : 0 ≤ (rngH e).lo) : 0 ≤ e.real θ := by
  have m := (mem_rngH hg e).1
  have : (0 : ℝ) ≤ ((rngH e).lo : ℝ) := by exact_mod_cast h
  linarith

/-- The fixed angle index `0` is `0` on H. -/
theorem theta0 (hg : Good prob θ dx dy L) : θ 0 = 0 := by
  have h := hg.ang 0
  have e : (prob.rootAng 0).lo = 0 ∧ (prob.rootAng 0).hi = 0 := by decide +kernel
  have h1 := h.1; have h2 := h.2
  rw [e.1] at h1; rw [e.2] at h2; push_cast at h1 h2; linarith

/-- All angle offsets on H are below 1 in absolute value. -/
theorem theta_abs_le (hg : Good prob θ dx dy L) {k : ℕ} (hk : k ∈ [1, 2, 5, 7, 8, 10, 11, 13, 14]) :
    |θ k| ≤ 1 := by
  have h := hg.ang k
  have b : -1 ≤ (prob.rootAng k).lo ∧ (prob.rootAng k).hi ≤ 1 := by
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hk
    rcases hk with rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl | rfl <;> decide +kernel
  have b1 : ((-1 : ℚ) : ℝ) ≤ ((prob.rootAng k).lo : ℝ) := by exact_mod_cast b.1
  have b2 : ((prob.rootAng k).hi : ℝ) ≤ ((1 : ℚ) : ℝ) := by exact_mod_cast b.2
  push_cast at b1 b2
  rw [abs_le]; exact ⟨by linarith [h.1], by linarith [h.2]⟩

/-- Orthant sign of `sin θ_k`. -/
theorem sin_orth (hg : Good prob θ dx dy L) {k : ℕ} (hk : k ∈ [1, 2, 5, 7, 8, 10, 11, 13, 14]) {b : Bool}
    (hb : 0 ≤ (sg b : ℝ) * θ k) : 0 ≤ (sg b : ℝ) * Real.sin (θ k) := by
  have ha := abs_le.mp (theta_abs_le hg hk)
  have pi3 := Real.pi_gt_three
  cases b
  · simp only [sg] at hb ⊢; push_cast at hb ⊢
    have : Real.sin (θ k) ≤ 0 := Real.sin_nonpos_of_nonpos_of_neg_pi_le (by linarith) (by linarith)
    linarith
  · simp only [sg] at hb ⊢; push_cast at hb ⊢
    have : 0 ≤ Real.sin (θ k) := Real.sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith)
    linarith

theorem angE_axis (θ : ℕ → ℝ) (k : ℕ) : angE θ k 0 = θ k := by simp [angE]

theorem neg_sg_pm (b : Bool) : -sg b = 1 ∨ -sg b = -1 := by cases b <;> simp [sg]

theorem fit_walls (hg : Good prob θ dx dy L) {i : ℕ} (hi : i < 9) :
    supp (φH θ i) 0 ≤ (cH dx dy i).1 ∧ (cH dx dy i).1 ≤ L - supp (φH θ i) 0 ∧
    supp (φH θ i) (Real.pi / 2) ≤ (cH dx dy i).2 ∧ (cH dx dy i).2 ≤ L - supp (φH θ i) (Real.pi / 2) :=
  wall_bounds _ _ L (hg.fit _ (prob.sq_mem (by simpa [Prob.n, prob] using hi)))

/-- Signed products with an enclosure: the endpoint chosen by the sign. -/
theorem mul_choose {s x : ℝ} {I : Iv} (hx : Iv.mem x I) {b : Bool} (hs : 0 ≤ (sg b : ℝ) * s) :
    s * x ≤ s * ((if b then I.hi else I.lo : ℚ) : ℝ) := by
  cases b
  · simp only [sg] at hs; push_cast at hs; simp only [Bool.false_eq_true, ↓reduceIte]
    exact mul_le_mul_of_nonpos_left hx.1 (by linarith)
  · simp only [sg] at hs; push_cast at hs; simp only [↓reduceIte]
    exact mul_le_mul_of_nonneg_left hx.2 (by linarith)

/-- `c2y - c1y` on H. -/
def dY12 : Iv := dIv (prob.sq 0).ry (prob.sq 1).ry (prob.sq 0).y (prob.sq 1).y

/-- Supports of P in case b on the orthant `b1, b2` (signs of θ1, θ2); anchor support 1/2. -/
def σPb (b1 b2 : Bool) : PSigns := ⟨(1, -sg b1), (sg b2, 1), (-1, 1), .c (1/2)⟩

set_option maxRecDepth 100000 in
/-- P row, case b (14's face `-e2` separates 13), on H. `j` owns the 1-2 separation. -/
theorem ProwB_H (hg : Good prob θ dx dy L) {j o : ℕ} (hj : j = 1 ∨ j = 2)
    (hanch : Real.cos (angE θ j 0) * ((cH dx dy 1).1 - (cH dx dy 0).1) +
      Real.sin (angE θ j 0) * ((cH dx dy 1).2 - (cH dx dy 0).2) ≥ 1/2 + supp (angE θ o 0) (angE θ j 0))
    (hb : Sep (cH dx dy 8) (φH θ 8) (cH dx dy 7) (φH θ 7) 3)
    {b1 b2 bj : Bool} (h1 : 0 ≤ (sg b1 : ℝ) * θ 1) (h2 : 0 ≤ (sg b2 : ℝ) * θ 2) (hjb : 0 ≤ (sg bj : ℝ) * θ j) :
    (ProwB j o (if bj then dY12.hi else dY12.lo) (σPb b1 b2)).Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have sgn := ownerA_signs hg
  have hjm : j ∈ [1, 2, 5, 7, 8, 10, 11, 13, 14] := by rcases hj with rfl | rfl <;> simp
  have hcj : 0 < Real.cos (angE θ j 0) := by rcases hj with rfl | rfl; exact sgn.2.2.2.2.2.2.2.2.1; exact sgn.2.2.2.2.2.2.2.2.2
  have p0 := hg.pos _ (prob.sq_mem (i := 0) (by decide))
  have p1 := hg.pos _ (prob.sq_mem (i := 1) (by decide))
  have hdy : Iv.mem _ dY12 := mem_dIv (rA := (prob.sq 0).ry) (rB := (prob.sq 1).ry) p0.2 p1.2
  have hsj := sin_orth hg hjm hjb
  rw [← angE_axis θ j] at hsj
  have hY := mul_choose hdy hsj
  have w0 := fit_walls hg (i := 0) (by decide)
  have w1 := fit_walls hg (i := 1) (by decide)
  have s1 := sin_orth hg (k := 1) (by simp) h1
  have s2 := sin_orth hg (k := 2) (by simp) h2
  have a00 : angE θ 0 0 = 0 := by simp [angE, t0]
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have c1 : 0 < Real.cos (θ 1) := by rw [← angE_axis θ 1]; exact sgn.2.2.2.2.2.2.2.2.1
  have c2 : 0 < Real.cos (θ 2) := by rw [← angE_axis θ 2]; exact sgn.2.2.2.2.2.2.2.2.2
  refine ProwB_holds t0 (sep_2_14 hg) hb hanch w0.1 w1.2.2.2 ?_ hcj
    (nonneg_of_rngH hg (.sn 14 1) (by decide +kernel)) (nonneg_of_rngH hg (.cs 14 1) (by decide +kernel))
    ?_ ?_ ?_ (half_support_lb θ j 0 o 0)
  · simpa [cH, cenOf] using hY
  · show (suppE 1 (-sg b1) 0 0 1 0).real θ = _
    refine suppE_real (Or.inl rfl) (neg_sg_pm b1) ?_ ?_
    · rw [a00, angE_axis, zero_sub, Real.cos_neg]; push_cast; linarith
    · rw [a00, angE_axis, zero_sub, Real.sin_neg]; push_cast
      have : (-(sg b1 : ℝ)) * -Real.sin (θ 1) = (sg b1 : ℝ) * Real.sin (θ 1) := by ring
      linarith
  · show (suppE (sg b2) 1 0 2 2 0).real θ = _
    refine suppE_real (sg_pm b2) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s2
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE (-1) 1 14 3 2 0).real θ = _
    refine suppE_real (Or.inr rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c (-1)) (cosD 14 3 2 0)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 14 3 2 0)) (by decide +kernel)

theorem mul_choose_lb {s x : ℝ} {I : Iv} (hx : Iv.mem x I) {b : Bool} (hs : 0 ≤ (sg b : ℝ) * s) :
    s * ((if b then I.lo else I.hi : ℚ) : ℝ) ≤ s * x := by
  cases b
  · simp only [sg] at hs; push_cast at hs; simp only [Bool.false_eq_true, ↓reduceIte]
    exact mul_le_mul_of_nonpos_left hx.2 (by linarith)
  · simp only [sg] at hs; push_cast at hs; simp only [↓reduceIte]
    exact mul_le_mul_of_nonneg_left hx.1 (by linarith)

/-- Orthant sign of `sin (θ_s - θ_t)` for two tilted squares. -/
theorem sin_orth2 (hg : Good prob θ dx dy L) {s t M : ℕ} (hs : s ∈ [1, 2, 5, 7, 8, 10, 11, 13, 14])
    (ht : t ∈ [1, 2, 5, 7, 8, 10, 11, 13, 14]) {b : Bool} (hb : 0 ≤ (sg b : ℝ) * (θ s - θ t)) :
    0 ≤ (sg b : ℝ) * Real.sin (angE θ s M - angE θ t M) := by
  have e : angE θ s M - angE θ t M = θ s - θ t := by simp only [angE]; ring
  rw [e]
  have ha := abs_le.mp (theta_abs_le hg hs)
  have hb' := abs_le.mp (theta_abs_le hg ht)
  have pi3 := Real.pi_gt_three
  cases b
  · simp only [sg] at hb ⊢; push_cast at hb ⊢
    have : Real.sin (θ s - θ t) ≤ 0 := Real.sin_nonpos_of_nonpos_of_neg_pi_le (by linarith) (by linarith)
    linarith
  · simp only [sg] at hb ⊢; push_cast at hb ⊢
    have : 0 ≤ Real.sin (θ s - θ t) := Real.sin_nonneg_of_nonneg_of_le_pi (by linarith) (by linarith)
    linarith

/-- Supports of P in case a on the orthant `b1, b2`; anchor support 1/2. -/
def σPa (b1 b2 : Bool) : PSigns := ⟨(1, -sg b1), (sg b2, 1), (-1, 1), .c (1/2)⟩

/-- Supports of Q in case b on the orthant `b10`. -/
def σQb (b10 : Bool) : QSigns := ⟨(1, -sg b10), (sg b10, 1), (1, 1)⟩
/-- Supports of Q in case a on the orthant `b10`. -/
def σQa (b10 : Bool) : QSigns := ⟨(1, -sg b10), (sg b10, 1), (1, 1)⟩

set_option maxRecDepth 100000 in
/-- Q row, case b (11's face `-e1` separates 13), on H. -/
theorem QrowB_H (hg : Good prob θ dx dy L)
    (hb : Sep (cH dx dy 6) (φH θ 6) (cH dx dy 7) (φH θ 7) 2)
    {b10 : Bool} (h10 : 0 ≤ (sg b10 : ℝ) * θ 10) :
    (QrowB (σQb b10)).Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have w5 := fit_walls hg (i := 5) (by decide)
  have s10 := sin_orth hg (k := 10) (by simp) h10
  have c10 : 0 < Real.cos (θ 10) := by
    rw [← angE_axis θ 10]; exact pos_of_rngH hg (.cs 10 0) (by decide +kernel)
  have a00 : angE θ 0 0 = 0 := by simp [angE, t0]
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  refine QrowB_holds t0 (sep_10_11 hg) hb w5.2.1 w5.2.2.2
    (nonneg_of_rngH hg (.cs 11 1) (by decide +kernel)) (nonneg_of_rngH hg (.sn 11 1) (by decide +kernel))
    ?_ ?_ ?_
  · show (suppE 1 (-sg b10) 0 0 10 0).real θ = _
    refine suppE_real (Or.inl rfl) (neg_sg_pm b10) ?_ ?_
    · rw [a00, angE_axis, zero_sub, Real.cos_neg]; push_cast; linarith
    · rw [a00, angE_axis, zero_sub, Real.sin_neg]; push_cast
      have : (-(sg b10 : ℝ)) * -Real.sin (θ 10) = (sg b10 : ℝ) * Real.sin (θ 10) := by ring
      linarith
  · show (suppE (sg b10) 1 0 2 10 0).real θ = _
    refine suppE_real (sg_pm b10) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s10
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE 1 1 11 1 10 0).real θ = _
    refine suppE_real (Or.inl rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (cosD 11 1 10 0)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 11 1 10 0)) (by decide +kernel)

set_option maxRecDepth 100000 in
/-- Q row, case a (13's face `+e1` separates 11), on H; `bd` the sign of `θ11 - θ13`. -/
theorem QrowA_H (hg : Good prob θ dx dy L)
    (ha : Sep (cH dx dy 7) (φH θ 7) (cH dx dy 6) (φH θ 6) 0)
    {b10 bd : Bool} (h10 : 0 ≤ (sg b10 : ℝ) * θ 10) (hd : 0 ≤ (sg bd : ℝ) * (θ 11 - θ 13)) :
    (QrowA (if bd then tightOffQIv.lo else tightOffQIv.hi) (σQa b10)).Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have sgn := ownerA_signs hg
  have w5 := fit_walls hg (i := 5) (by decide)
  have s10 := sin_orth hg (k := 10) (by simp) h10
  have c10 : 0 < Real.cos (θ 10) := by
    rw [← angE_axis θ 10]; exact pos_of_rngH hg (.cs 10 0) (by decide +kernel)
  have a00 : angE θ 0 0 = 0 := by simp [angE, t0]
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have hO := mul_choose_lb (tight_offsetQ_mem hg) (sin_orth2 hg (s := 11) (t := 13) (M := 1) (by simp) (by simp) hd)
  refine QrowA_holds t0 (sep_10_11 hg) ha w5.2.1 w5.2.2.2 sgn.2.1.le sgn.1.le
    sgn.2.2.2.2.2.1.le sgn.2.2.2.2.2.2.1.le sgn.2.2.2.2.2.2.2.1 (by simpa [angE, angOf, OffsetBounds.q2, OffsetBounds.q10, OffsetBounds.q11, OffsetBounds.q14, cH, cenOf, prob, Prob.sq] using hO) ?_ ?_ ?_
  · show (suppE 1 (-sg b10) 0 0 10 0).real θ = _
    refine suppE_real (Or.inl rfl) (neg_sg_pm b10) ?_ ?_
    · rw [a00, angE_axis, zero_sub, Real.cos_neg]; push_cast; linarith
    · rw [a00, angE_axis, zero_sub, Real.sin_neg]; push_cast
      have : (-(sg b10 : ℝ)) * -Real.sin (θ 10) = (sg b10 : ℝ) * Real.sin (θ 10) := by ring
      linarith
  · show (suppE (sg b10) 1 0 2 10 0).real θ = _
    refine suppE_real (sg_pm b10) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s10
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE 1 1 13 1 10 0).real θ = _
    refine suppE_real (Or.inl rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (cosD 13 1 10 0)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 13 1 10 0)) (by decide +kernel)

set_option maxRecDepth 100000 in
/-- P row, case a (13's face `+e2` separates 14), on H; `bd` the sign of `θ14 - θ13`. -/
theorem ProwA_H (hg : Good prob θ dx dy L) {j o : ℕ} (hj : j = 1 ∨ j = 2)
    (hanch : Real.cos (angE θ j 0) * ((cH dx dy 1).1 - (cH dx dy 0).1) +
      Real.sin (angE θ j 0) * ((cH dx dy 1).2 - (cH dx dy 0).2) ≥ 1/2 + supp (angE θ o 0) (angE θ j 0))
    (ha : Sep (cH dx dy 7) (φH θ 7) (cH dx dy 8) (φH θ 8) 1)
    {b1 b2 bj bd : Bool} (h1 : 0 ≤ (sg b1 : ℝ) * θ 1) (h2 : 0 ≤ (sg b2 : ℝ) * θ 2)
    (hjb : 0 ≤ (sg bj : ℝ) * θ j) (hd : 0 ≤ (sg bd : ℝ) * (θ 14 - θ 13)) :
    (ProwA j (if bj then dY12.hi else dY12.lo) (if bd then tightOffPIv.lo else tightOffPIv.hi) (σPa b1 b2)).Holds
      θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have sgn := ownerA_signs hg
  have hjm : j ∈ [1, 2, 5, 7, 8, 10, 11, 13, 14] := by rcases hj with rfl | rfl <;> simp
  have hcj : 0 < Real.cos (angE θ j 0) := by
    rcases hj with rfl | rfl; exact sgn.2.2.2.2.2.2.2.2.1; exact sgn.2.2.2.2.2.2.2.2.2
  have p0 := hg.pos _ (prob.sq_mem (i := 0) (by decide))
  have p1 := hg.pos _ (prob.sq_mem (i := 1) (by decide))
  have hdy : Iv.mem _ dY12 := mem_dIv (rA := (prob.sq 0).ry) (rB := (prob.sq 1).ry) p0.2 p1.2
  have hsj := sin_orth hg hjm hjb
  rw [← angE_axis θ j] at hsj
  have hY := mul_choose hdy hsj
  have w0 := fit_walls hg (i := 0) (by decide)
  have w1 := fit_walls hg (i := 1) (by decide)
  have s1 := sin_orth hg (k := 1) (by simp) h1
  have s2 := sin_orth hg (k := 2) (by simp) h2
  have a00 : angE θ 0 0 = 0 := by simp [angE, t0]
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have c1 : 0 < Real.cos (θ 1) := by rw [← angE_axis θ 1]; exact sgn.2.2.2.2.2.2.2.2.1
  have c2 : 0 < Real.cos (θ 2) := by rw [← angE_axis θ 2]; exact sgn.2.2.2.2.2.2.2.2.2
  have hO := mul_choose_lb (tight_offsetP_mem hg) (sin_orth2 hg (s := 14) (t := 13) (M := 1) (by simp) (by simp) hd)
  refine ProwA_holds t0 (sep_2_14 hg) ha hanch w0.1 w1.2.2.2 ?_ hcj sgn.1.le sgn.2.1.le
    sgn.2.2.1.le sgn.2.2.2.1.le sgn.2.2.2.2.1 (by simpa [angE, angOf, OffsetBounds.q2, OffsetBounds.q10, OffsetBounds.q11, OffsetBounds.q14, cH, cenOf, prob, Prob.sq] using hO) ?_ ?_ ?_ (half_support_lb θ j 0 o 0)
  · simpa [cH, cenOf] using hY
  · show (suppE 1 (-sg b1) 0 0 1 0).real θ = _
    refine suppE_real (Or.inl rfl) (neg_sg_pm b1) ?_ ?_
    · rw [a00, angE_axis, zero_sub, Real.cos_neg]; push_cast; linarith
    · rw [a00, angE_axis, zero_sub, Real.sin_neg]; push_cast
      have : (-(sg b1 : ℝ)) * -Real.sin (θ 1) = (sg b1 : ℝ) * Real.sin (θ 1) := by ring
      linarith
  · show (suppE (sg b2) 1 0 2 2 0).real θ = _
    refine suppE_real (sg_pm b2) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s2
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE (-1) 1 13 3 2 0).real θ = _
    refine suppE_real (Or.inr rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c (-1)) (cosD 13 3 2 0)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 13 3 2 0)) (by decide +kernel)

/-! ## The floor row F1 -/

/-- Absolute boxes of the centres on H. -/
def absX (i : ℕ) : Iv := ⟨(prob.sq i).rx + (prob.sq i).x.lo, (prob.sq i).rx + (prob.sq i).x.hi⟩
def absY (i : ℕ) : Iv := ⟨(prob.sq i).ry + (prob.sq i).y.lo, (prob.sq i).ry + (prob.sq i).y.hi⟩

theorem cxy_mem (hg : Good prob θ dx dy L) {i : ℕ} (hi : i < 9) :
    Iv.mem (cH dx dy i).1 (absX i) ∧ Iv.mem (cH dx dy i).2 (absY i) := by
  have p := hg.pos _ (prob.sq_mem (i := i) (by simpa [Prob.n, prob] using hi))
  simp only [InPos, Iv.mem] at p
  simp only [Iv.mem, cH, cenOf, absX, absY]; push_cast
  exact ⟨⟨by linarith [p.1.1], by linarith [p.1.2]⟩, ⟨by linarith [p.2.1], by linarith [p.2.2]⟩⟩

/-- `c8x - c5x` and `c13x - c8x` on H. -/
def dX58 : Iv := dIv (prob.sq 2).rx (prob.sq 4).rx (prob.sq 2).x (prob.sq 4).x
def dX813 : Iv := dIv (prob.sq 4).rx (prob.sq 7).rx (prob.sq 4).x (prob.sq 7).x

theorem sg_beq (a b : Bool) : sg (a == b) = sg a * sg b := by cases a <;> cases b <;> simp [sg]

/-- The 5-8 anchor, owner 5 (5's face `+e2`). -/
theorem anchor58_5 (h : Sep (cH dx dy 2) (φH θ 2) (cH dx dy 4) (φH θ 4) 1) :
    -Real.sin (angE θ 5 0) * ((cH dx dy 4).1 - (cH dx dy 2).1) +
      Real.cos (angE θ 5 0) * ((cH dx dy 4).2 - (cH dx dy 2).2) ≥ 1/2 + supp (angE θ 8 0) (angE θ 5 2) := by
  have g : Real.cos (angE θ 5 0 + ((1:ℕ):ℝ) * (Real.pi / 2)) * ((cH dx dy 4).1 - (cH dx dy 2).1) +
      Real.sin (angE θ 5 0 + ((1:ℕ):ℝ) * (Real.pi / 2)) * ((cH dx dy 4).2 - (cH dx dy 2).2) ≥
      1/2 + supp (angE θ 8 0) (angE θ 5 0 + ((1:ℕ):ℝ) * (Real.pi / 2)) := sep_gap h
  have e : angE θ 5 2 = angE θ 5 0 + Real.pi / 2 := by simp only [angE]; push_cast; ring
  simp only [Nat.cast_one, one_mul, Real.cos_add_pi_div_two, Real.sin_add_pi_div_two] at g
  rw [e]; linarith

/-- The 5-8 anchor, owner 8 (8's face `-e2`). -/
theorem anchor58_8 (h : Sep (cH dx dy 4) (φH θ 4) (cH dx dy 2) (φH θ 2) 3) :
    -Real.sin (angE θ 8 0) * ((cH dx dy 4).1 - (cH dx dy 2).1) +
      Real.cos (angE θ 8 0) * ((cH dx dy 4).2 - (cH dx dy 2).2) ≥ 1/2 + supp (angE θ 5 0) (angE θ 8 2) := by
  have g : Real.cos (angE θ 8 0 + ((3:ℕ):ℝ) * (Real.pi / 2)) * ((cH dx dy 2).1 - (cH dx dy 4).1) +
      Real.sin (angE θ 8 0 + ((3:ℕ):ℝ) * (Real.pi / 2)) * ((cH dx dy 2).2 - (cH dx dy 4).2) ≥
      1/2 + supp (angE θ 5 0) (angE θ 8 0 + ((3:ℕ):ℝ) * (Real.pi / 2)) := sep_gap h
  have e3 : angE θ 8 0 + ((3:ℕ):ℝ) * (Real.pi / 2) = (angE θ 8 0 + Real.pi / 2) + Real.pi := by
    push_cast; ring
  have e : angE θ 8 2 = angE θ 8 0 + Real.pi / 2 := by simp only [angE]; push_cast; ring
  rw [e3, supp_add_pi, Real.cos_add_pi, Real.sin_add_pi, Real.cos_add_pi_div_two,
    Real.sin_add_pi_div_two] at g
  rw [e]; linarith

set_option maxRecDepth 100000 in
/-- F1, `θ8 ≥ 0`, 5-8 owned by 8, on H. -/
theorem F1rowPos8_H (hg : Good prob θ dx dy L) (h58 : Sep (cH dx dy 4) (φH θ 4) (cH dx dy 2) (φH θ 2) 3)
    {b5 : Bool} (h5 : 0 ≤ (sg b5 : ℝ) * θ 5) (h8 : 0 ≤ θ 8) :
    (F1rowPos8 (absX 2).hi (sg b5, 1) (1, 1) (.c (1/2))).Holds θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have s5 := sin_orth hg (k := 5) (by simp) h5
  have c5 : 0 < Real.cos (θ 5) := by
    rw [← angE_axis θ 5]; exact pos_of_rngH hg (.cs 5 0) (by decide +kernel)
  have s8 := sin_orth hg (k := 8) (b := true) (by simp) (by simp [sg]; exact h8)
  simp only [sg, ↓reduceIte] at s8; push_cast at s8
  refine F1rowPos8_holds t0 (sep_8_13 hg) h58 (cxy_mem hg (i := 2) (by decide)).1.2
    (fit_walls hg (i := 2) (by decide)).2.2.1 (by rw [angE_axis]; linarith)
    (nonneg_of_rngH hg (.cs 8 0) (by decide +kernel)) ?_ (half_support_lb θ 8 2 5 0) ?_
  · show (suppE (sg b5) 1 0 2 5 0).real θ = _
    refine suppE_real (sg_pm b5) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s5
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE 1 1 8 2 13 1).real θ = _
    refine suppE_real (Or.inl rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (cosD 8 2 13 1)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 8 2 13 1)) (by decide +kernel)

set_option maxRecDepth 100000 in
/-- F1, `θ8 ≤ 0`, on H; `j` owns the 5-8 separation (anchor from `anchor58_5` or `anchor58_8`). -/
theorem F1rowNeg_H (hg : Good prob θ dx dy L) {j o : ℕ} (hj : j = 5 ∨ j = 8)
    (hanch : -Real.sin (angE θ j 0) * ((cH dx dy 4).1 - (cH dx dy 2).1) +
      Real.cos (angE θ j 0) * ((cH dx dy 4).2 - (cH dx dy 2).2) ≥ 1/2 + supp (angE θ o 0) (angE θ j 2))
    {b5 bj : Bool} (h5 : 0 ≤ (sg b5 : ℝ) * θ 5) (hjb : 0 ≤ (sg bj : ℝ) * θ j) (h8 : θ 8 ≤ 0) :
    (F1rowNeg j o (if bj then dX58.lo else dX58.hi) dX813.hi (sg b5, 1) (1, 1) (.c (1/2))).Holds
      θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have s5 := sin_orth hg (k := 5) (by simp) h5
  have c5 : 0 < Real.cos (θ 5) := by
    rw [← angE_axis θ 5]; exact pos_of_rngH hg (.cs 5 0) (by decide +kernel)
  have s8 := sin_orth hg (k := 8) (b := false) (by simp) (by simp [sg]; exact h8)
  simp only [sg, Bool.false_eq_true, ↓reduceIte] at s8; push_cast at s8
  have hjm : j ∈ [1, 2, 5, 7, 8, 10, 11, 13, 14] := by rcases hj with rfl | rfl <;> simp
  have hsj := sin_orth hg hjm hjb
  rw [← angE_axis θ j] at hsj
  have p2 := hg.pos _ (prob.sq_mem (i := 2) (by decide))
  have p4 := hg.pos _ (prob.sq_mem (i := 4) (by decide))
  have p7 := hg.pos _ (prob.sq_mem (i := 7) (by decide))
  have hx58 : Iv.mem _ dX58 := mem_dIv (rA := (prob.sq 2).rx) (rB := (prob.sq 4).rx) p2.1 p4.1
  have hx813 : Iv.mem _ dX813 := mem_dIv (rA := (prob.sq 4).rx) (rB := (prob.sq 7).rx) p4.1 p7.1
  have hX := mul_choose_lb hx58 hsj
  have hcj : 0 < Real.cos (angE θ j 0) := by
    rcases hj with rfl | rfl
    · exact pos_of_rngH hg (.cs 5 0) (by decide +kernel)
    · exact pos_of_rngH hg (.cs 8 0) (by decide +kernel)
  refine F1rowNeg_holds t0 (sep_8_13 hg) hanch (by simpa [cH, cenOf] using hX)
    (fit_walls hg (i := 2) (by decide)).2.2.1 (by simpa [cH, cenOf] using hx813.2) hcj
    (by rw [angE_axis]; linarith) (pos_of_rngH hg (.cs 8 0) (by decide +kernel)) ?_ ?_
    (half_support_lb θ j 2 o 0)
  · show (suppE (sg b5) 1 0 2 5 0).real θ = _
    refine suppE_real (sg_pm b5) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s5
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE 1 1 8 2 13 1).real θ = _
    refine suppE_real (Or.inl rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (cosD 8 2 13 1)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 8 2 13 1)) (by decide +kernel)

set_option maxRecDepth 100000 in
/-- F1, 5-8 owned by 5 (5's face `+e2`), on H; `bd` the sign of `θ8 - θ5`. -/
theorem F1rowPos5_H (hg : Good prob θ dx dy L) (h58 : Sep (cH dx dy 2) (φH θ 2) (cH dx dy 4) (φH θ 4) 1)
    {b5 bd : Bool} (h5 : 0 ≤ (sg b5 : ℝ) * θ 5) (hd : 0 ≤ (sg bd : ℝ) * (θ 8 - θ 5)) :
    (F1rowPos5 (if b5 then (absX 2).hi else (absX 2).lo) (if bd then (absX 4).hi else (absX 4).lo)
      (if bd == b5 then (absY 4).hi else (absY 4).lo) (sg b5, 1) (1, 1) (.c (1/2))).Holds
      θ (cH dx dy 7).1 (cH dx dy 7).2 L := by
  have t0 := theta0 hg
  have a02 : angE θ 0 2 = Real.pi / 2 := by simp [angE, t0]; ring
  have s5 := sin_orth hg (k := 5) (by simp) h5
  have c5 : 0 < Real.cos (θ 5) := by
    rw [← angE_axis θ 5]; exact pos_of_rngH hg (.cs 5 0) (by decide +kernel)
  have sd := sin_orth2 hg (s := 8) (t := 5) (M := 0) (by simp) (by simp) hd
  have m2 := cxy_mem hg (i := 2) (by decide)
  have m4 := cxy_mem hg (i := 4) (by decide)
  have hs5' : 0 ≤ (sg b5 : ℝ) * Real.sin (angE θ 5 0) := by rw [angE_axis]; exact s5
  have hX5 := mul_choose m2.1 hs5'
  have c5' : 0 < Real.cos (angE θ 5 0) := by rw [angE_axis]; exact c5
  have hx := mul_choose m4.1 (s := Real.sin (angE θ 8 0 - angE θ 5 0) * Real.cos (angE θ 5 0)) (b := bd)
    (by rw [← mul_assoc]; exact mul_nonneg sd c5'.le)
  have hy := mul_choose m4.2 (s := Real.sin (angE θ 8 0 - angE θ 5 0) * Real.sin (angE θ 5 0)) (b := bd == b5)
    (by rw [sg_beq]; push_cast
        have := mul_nonneg sd hs5'
        linarith [show (sg bd : ℝ) * sg b5 * (Real.sin (angE θ 8 0 - angE θ 5 0) * Real.sin (angE θ 5 0)) =
          (sg bd : ℝ) * Real.sin (angE θ 8 0 - angE θ 5 0) * ((sg b5 : ℝ) * Real.sin (angE θ 5 0)) by ring])
  refine F1rowPos5_holds t0 (sep_8_13 hg) h58 hX5 c5'.le (fit_walls hg (i := 2) (by decide)).2.2.1
    (by linarith) (by rw [← cosD_real]; exact nonneg_of_rngH hg (cosD 8 0 5 0) (by decide +kernel)) ?_
    (half_support_lb θ 5 2 8 0) ?_
  · show (suppE (sg b5) 1 0 2 5 0).real θ = _
    refine suppE_real (sg_pm b5) (Or.inl rfl) ?_ ?_
    · rw [a02, angE_axis, Real.cos_pi_div_two_sub]; exact s5
    · rw [a02, angE_axis, Real.sin_pi_div_two_sub]; push_cast; linarith
  · show (suppE 1 1 8 2 13 1).real θ = _
    refine suppE_real (Or.inl rfl) (Or.inl rfl) ?_ ?_
    · rw [← cosD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (cosD 8 2 13 1)) (by decide +kernel)
    · rw [← sinD_real]; exact nonneg_of_rngH hg (.mul (.c 1) (sinD 8 2 13 1)) (by decide +kernel)

end

end Sq19.Endgame

#print axioms Sq19.Endgame.ProwB_H
#print axioms Sq19.Endgame.QrowB_H
#print axioms Sq19.Endgame.QrowA_H
#print axioms Sq19.Endgame.ProwA_H
#print axioms Sq19.Endgame.F1rowPos8_H
#print axioms Sq19.Endgame.F1rowNeg_H
#print axioms Sq19.Endgame.F1rowPos5_H
