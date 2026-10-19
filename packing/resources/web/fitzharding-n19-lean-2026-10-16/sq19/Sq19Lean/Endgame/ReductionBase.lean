import Sq19Lean.Endgame.ReductionPath
import Sq19Lean.Endgame.ZeroRowIdentity

/-!
# The endpoint residual at the start of every cone-prefix path

The zero-axis rows are identified algebraically with the wedge rows. No packing
is assumed at the zeroed angles. Only angle membership in H, the fixed zero
coordinate, and an accepted geometry check are needed.
-/
namespace Sq19.Endgame.Reduction
open Sq19.Milp Real

private theorem scale_one (r : RealRow) : r.scale 1 = r := by
  cases r; simp [RealRow.scale]

private theorem tilted_angles {θ : ℕ → ℝ} (hθ : InAng θ Hull.prob.rootAng) :
    |θ 11| ≤ 82/10000 ∧ |θ 13| ≤ 82/10000 ∧ |θ 14| ≤ 82/10000 := by
  have h11 := hθ 11
  have h13 := hθ 13
  have h14 := hθ 14
  norm_num [Prob.rootAng,Hull.prob,Iv.mem] at h11 h13 h14
  exact ⟨abs_le.mpr ⟨by linarith,by linarith⟩,
    abs_le.mpr ⟨by linarith,by linarith⟩,
    abs_le.mpr ⟨by linarith,by linarith⟩⟩

private theorem relative_cos_ne {a b : ℝ} (ha : |a| ≤ 82/10000) (hb : |b| ≤ 82/10000) :
    cos ((π/4+a)-(π/4+b)) ≠ 0 := by
  obtain ⟨hal,hah⟩ := abs_le.mp ha
  obtain ⟨hbl,hbh⟩ := abs_le.mp hb
  apply ne_of_gt
  apply cos_pos_of_mem_Ioo
  constructor <;> linarith [pi_gt_three]

/-- Every expression case starts with nonnegative endpoint residual.
This conclusion uses only the geometric check, never a packing at the zeroed angles. -/
theorem Case.base_margin_nonneg (c : Case) (hc : geometryCheck c = true)
    {θ : ℕ → ℝ} (hθ : InAng θ Hull.prob.rootAng) (h0 : θ 0=0) :
    0 ≤ c.margin.real (axisZero θ) := by
  let z := axisZero θ
  have z0 : z 0=0 := by simp [z,axisZero,h0]
  have z1 : z 1=0 := by simp [z,axisZero]
  have z2 : z 2=0 := by simp [z,axisZero]
  have z5 : z 5=0 := by simp [z,axisZero]
  have z8 : z 8=0 := by simp [z,axisZero]
  have z10 : z 10=0 := by simp [z,axisZero]
  have z11 : z 11=θ 11 := by simp [z,axisZero]
  have z13 : z 13=θ 13 := by simp [z,axisZero]
  have z14 : z 14=θ 14 := by simp [z,axisZero]
  have zj12 : z c.j12=0 := by unfold Case.j12; split_ifs <;> assumption
  have zj58 : z c.j58=0 := by unfold Case.j58; split_ifs <;> assumption
  obtain ⟨h11,h13,h14⟩ := tilted_angles hθ
  have hd14 := relative_cos_ne h14 h13
  have hd11 := relative_cos_ne h11 h13
  have ns13 := Wedge.tilted_normal_pos h13
  let o1 : ℚ := if c.pd then tightOffPIv.lo else tightOffPIv.hi
  let o2 : ℚ := if c.qd then tightOffQIv.lo else tightOffQIv.hi
  let u : ℝ := if c.pa then cos ((π/4+θ 14)-(π/4+θ 13)) else 1
  let v : ℝ := if c.qa then cos ((π/4+θ 11)-(π/4+θ 13)) else 1
  have hu : u ≠ 0 := by dsimp [u]; split_ifs <;> first | assumption | norm_num
  have hv : v ≠ 0 := by dsimp [v]; split_ifs <;> first | assumption | norm_num
  have hp : c.P.at z = (zeroP c.pa (θ 13) (θ 14) o1).scale u := by
    cases he : c.pa
    · simp only [Case.P,he,Bool.false_eq_true,↓reduceIte,u,scale_one]
      exact (ProwB_at_zero z0 z1 z2 c.j12 (if c.owner12 then 1 else 2) zj12
        (if (if c.owner12 then c.b2 else c.b1) then dY12.hi else dY12.lo) c.b1 c.b2 o1).trans
        (by rw [z13,z14])
    · simp only [Case.P,he,↓reduceIte,u]
      simpa only [z13,z14] using ProwA_at_zero z0 z1 z2 c.j12 zj12
        (if (if c.owner12 then c.b2 else c.b1) then dY12.hi else dY12.lo)
        o1 c.b1 c.b2 (by simpa only [z13,z14] using hd14)
  have hq : c.Q.at z = (zeroQ c.qa (θ 13) (θ 11) o2).scale v := by
    cases he : c.qa
    · simp only [Case.Q,he,Bool.false_eq_true,↓reduceIte,v,scale_one]
      exact (QrowB_at_zero z0 z10 c.b10 o2).trans (by rw [z13,z11])
    · simp only [Case.Q,he,↓reduceIte,v]
      simpa only [z13,z11] using QrowA_at_zero z0 z10 o2 c.b10
        (by simpa only [z13,z11] using hd11)
  have hf : c.F.at z = (zeroF (θ 13)).scale 1 := by
    rw [scale_one]
    have hcos : 0 ≤ cos (π/4+z 13) := by rw [z13]; exact ns13.1.le
    have hsin : 0 ≤ sin (π/4+z 13) := by rw [z13]; exact ns13.2.le
    cases hb8 : c.b8
    · simp only [Case.F,hb8,Bool.false_eq_true,↓reduceIte]
      simpa only [z13,hb8] using F1rowNeg_at_zero z0 z5 z8 c.j58 c.other58 zj58
        (if (if c.owner58 then c.b8 else c.b5) then dX58.lo else dX58.hi)
        dX813.hi c.b5 c.bd58 hcos hsin
    · cases h58 : c.owner58
      · simp only [Case.F,hb8,h58,Bool.false_eq_true,↓reduceIte]
        simpa only [z13] using F1rowPos5_at_zero z0 z5 z8
          (if c.b5 then (absX 2).hi else (absX 2).lo)
          (if c.bd58 then (absX 4).hi else (absX 4).lo)
          (if c.bd58 == c.b5 then (absY 4).hi else (absY 4).lo)
          c.b5 c.bd58 hcos hsin
      · simp only [Case.F,hb8,h58,↓reduceIte]
        simpa only [z13] using F1rowPos8_at_zero z0 z5 z8 (absX 2).hi c.b5 c.bd58 hcos hsin
  have ho1 : (1589/10000 : ℝ) ≤ o1 ∧ (o1 : ℝ) ≤ 2893/10000 := by
    dsimp [o1,tightOffPIv]; split_ifs <;> norm_num
  have ho2 : (-1322/10000 : ℝ) ≤ o2 ∧ (o2 : ℝ) ≤ 365/10000 := by
    dsimp [o2,tightOffQIv]; split_ifs <;> norm_num
  have hS : 0 < (S1E c.P c.Q c.F).real z := (geometry_sound c hc (axisZero_mem hθ)).2.2.2
  have h := zero_rows_margin_nonneg c.pa c.qa h11 h13 h14 ho1.1 ho1.2 ho2.1 ho2.2
    hp hq hf hu hv (by norm_num : (1:ℝ) ≠ 0) hS
  change 0 ≤ c.margin.real z
  simpa only [Case.margin,endpointMargin,Ex.real,endpointE_real z0,side19,sub_eq_add_neg] using h

end Sq19.Endgame.Reduction

#print axioms Sq19.Endgame.Reduction.Case.base_margin_nonneg
