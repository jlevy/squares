import Sq19Lean.Endgame.HullData
import Sq19Lean.Endgame.RowsA

/-!
# Actual owner-a offsets on the capture hull

The only input is `Good Hull.prob`: the offsets below are computed from the
actual centres and angles, not additional free interval parameters. Elementary
small-angle enclosures and rational interval arithmetic prove the advertised
bounds. No floating point computation or native decision procedure is used.
-/
namespace Sq19.Endgame
open Sq19.Milp

namespace OffsetBounds

def cosSmall (I : Iv) : Iv := ⟨1 - I.mag^2/2, 1⟩
def sinSmall (I : Iv) : Iv := ⟨I.lo - I.mag^3/6, I.hi + I.mag^3/6⟩

theorem mem_cosSmall {x : ℝ} {I : Iv} (h : Iv.mem x I) :
    Iv.mem (Real.cos x) (cosSmall I) := by
  have hm := Iv.abs_le_mag h
  have hm0 : (0 : ℝ) ≤ I.mag := (abs_nonneg x).trans hm
  have hp : x^2 ≤ (I.mag : ℝ)^2 := by
    rw [← sq_abs]; exact pow_le_pow_left₀ (abs_nonneg x) hm 2
  have hc := Real.one_sub_sq_div_two_le_cos (x := x)
  simp only [Iv.mem, cosSmall, Rat.cast_sub, Rat.cast_one, Rat.cast_div,
    Rat.cast_pow, Rat.cast_ofNat]
  exact ⟨by linarith, Real.cos_le_one x⟩

theorem mem_sinSmall {x : ℝ} {I : Iv} (h : Iv.mem x I) :
    Iv.mem (Real.sin x) (sinSmall I) := by
  have hm := Iv.abs_le_mag h
  have hp : |x|^3 ≤ (I.mag : ℝ)^3 := pow_le_pow_left₀ (abs_nonneg x) hm 3
  have hs := abs_le.mp (abs_sin_sub_self_le x)
  simp only [Iv.mem, sinSmall, Rat.cast_sub, Rat.cast_add, Rat.cast_div,
    Rat.cast_pow, Rat.cast_ofNat]
  exact ⟨by linarith [h.1], by linarith [h.2]⟩

def cosTilt (I : Iv) : Iv := s2.mul ((cosSmall I).sub (sinSmall I))
def sinTilt (I : Iv) : Iv := s2.mul ((cosSmall I).add (sinSmall I))

theorem mem_cosTilt {x : ℝ} {I : Iv} (h : Iv.mem x I) :
    Iv.mem (Real.cos (Real.pi/4 + x)) (cosTilt I) := by
  have hh := Iv.mem_mul mem_s2 (Iv.mem_sub (mem_cosSmall h) (mem_sinSmall h))
  convert hh using 1
  · rw [Real.cos_add, Real.cos_pi_div_four, Real.sin_pi_div_four]; ring
  · rfl

theorem mem_sinTilt {x : ℝ} {I : Iv} (h : Iv.mem x I) :
    Iv.mem (Real.sin (Real.pi/4 + x)) (sinTilt I) := by
  have hh := Iv.mem_mul mem_s2 (Iv.mem_add (mem_cosSmall h) (mem_sinSmall h))
  convert hh using 1
  · rw [Real.sin_add, Real.cos_pi_div_four, Real.sin_pi_div_four]; ring
  · rfl

/-- The square indices in the nine-square hull problem, as opposed to labels. -/
def q2 : Sq := Hull.prob.sq 1
def q10 : Sq := Hull.prob.sq 5
def q11 : Sq := Hull.prob.sq 6
def q14 : Sq := Hull.prob.sq 8

def cIv (r : ℚ) (I : Iv) : Iv := (Iv.pt r).add I

def pX : Iv := (cIv q2.rx q2.x).add
  ((Iv.pt (1/2)).mul ((cosSmall q2.a).add (sinSmall q2.a)))
def pY : Iv := (cIv q2.ry q2.y).add
  ((Iv.pt (1/2)).mul ((sinSmall q2.a).sub (cosSmall q2.a)))
def qX : Iv := (cIv q10.rx q10.x).add
  ((Iv.pt (1/2)).mul ((sinSmall q10.a).sub (cosSmall q10.a)))
def qY : Iv := (cIv q10.ry q10.y).sub
  ((Iv.pt (1/2)).mul ((sinSmall q10.a).add (cosSmall q10.a)))

def angle13 : Iv := Hull.prob.rootAng 13

def offsetPIv : Iv :=
  ((cosTilt angle13).mul (pX.sub (cIv q14.rx q14.x))).add
    ((sinTilt angle13).mul (pY.sub (cIv q14.ry q14.y)))
def offsetQIv : Iv :=
  (((sinTilt angle13).neg).mul ((cIv q11.rx q11.x).sub qX)).add
    ((cosTilt angle13).mul ((cIv q11.ry q11.y).sub qY))

private theorem cen_mem {dx dy : ℕ → ℝ} {q : Sq} (h : InPos dx dy q) :
    Iv.mem (cenOf dx dy q).1 (cIv q.rx q.x) ∧
    Iv.mem (cenOf dx dy q).2 (cIv q.ry q.y) :=
  ⟨Iv.mem_add (Iv.mem_pt _) h.1, Iv.mem_add (Iv.mem_pt _) h.2⟩

private theorem mem_p {θ dx dy : ℕ → ℝ} {L : ℝ} (h : Good Hull.prob θ dx dy L) :
    Iv.mem (corner (cenOf dx dy q2) (angOf θ q2) 1).1 pX ∧
    Iv.mem (corner (cenOf dx dy q2) (angOf θ q2) 1).2 pY := by
  have hc := cen_mem (h.pos q2 (Hull.prob.sq_mem (by decide : 1 < Hull.prob.n)))
  have ha : Iv.mem (θ 2) q2.a := h.ang 2
  have hcos := mem_cosSmall ha
  have hsin := mem_sinSmall ha
  have hx := Iv.mem_add hc.1 (Iv.mem_mul (Iv.mem_pt (1/2)) (Iv.mem_add hcos hsin))
  have hy := Iv.mem_add hc.2 (Iv.mem_mul (Iv.mem_pt (1/2)) (Iv.mem_sub hsin hcos))
  constructor
  · convert hx using 1 <;> norm_num [corner, vx, ox, oy, angOf, q2, Hull.prob,
      Prob.sq, pX] <;> ring
  · convert hy using 1 <;> norm_num [corner, vy, ox, oy, angOf, q2, Hull.prob,
      Prob.sq, pY] <;> ring

private theorem mem_q {θ dx dy : ℕ → ℝ} {L : ℝ} (h : Good Hull.prob θ dx dy L) :
    Iv.mem (corner (cenOf dx dy q10) (angOf θ q10) 0).1 qX ∧
    Iv.mem (corner (cenOf dx dy q10) (angOf θ q10) 0).2 qY := by
  have hc := cen_mem (h.pos q10 (Hull.prob.sq_mem (by decide : 5 < Hull.prob.n)))
  have ha : Iv.mem (θ 10) q10.a := h.ang 10
  have hcos := mem_cosSmall ha
  have hsin := mem_sinSmall ha
  have hx := Iv.mem_add hc.1 (Iv.mem_mul (Iv.mem_pt (1/2)) (Iv.mem_sub hsin hcos))
  have hy := Iv.mem_sub hc.2 (Iv.mem_mul (Iv.mem_pt (1/2)) (Iv.mem_add hsin hcos))
  constructor
  · convert hx using 1 <;> norm_num [corner, vx, ox, oy, angOf, q10, Hull.prob,
      Prob.sq, qX] <;> ring
  · convert hy using 1 <;> norm_num [corner, vy, ox, oy, angOf, q10, Hull.prob,
      Prob.sq, qY] <;> ring

theorem offsetP_mem {θ dx dy : ℕ → ℝ} {L : ℝ} (h : Good Hull.prob θ dx dy L) :
    Iv.mem (offsetP (cenOf dx dy q2) (cenOf dx dy q14)
      (angOf θ q2) (Real.pi/4 + θ 13)) offsetPIv := by
  have hp := mem_p h
  have hc := cen_mem (h.pos q14 (Hull.prob.sq_mem (by decide : 8 < Hull.prob.n)))
  exact Iv.mem_add
    (Iv.mem_mul (mem_cosTilt (h.ang 13)) (Iv.mem_sub hp.1 hc.1))
    (Iv.mem_mul (mem_sinTilt (h.ang 13)) (Iv.mem_sub hp.2 hc.2))

theorem offsetQ_mem {θ dx dy : ℕ → ℝ} {L : ℝ} (h : Good Hull.prob θ dx dy L) :
    Iv.mem (offsetQ (cenOf dx dy q10) (cenOf dx dy q11)
      (angOf θ q10) (Real.pi/4 + θ 13)) offsetQIv := by
  have hq := mem_q h
  have hc := cen_mem (h.pos q11 (Hull.prob.sq_mem (by decide : 6 < Hull.prob.n)))
  exact Iv.mem_add
    (Iv.mem_mul (Iv.mem_neg (mem_sinTilt (h.ang 13))) (Iv.mem_sub hc.1 hq.1))
    (Iv.mem_mul (mem_cosTilt (h.ang 13)) (Iv.mem_sub hc.2 hq.2))

set_option maxRecDepth 10000 in
set_option maxHeartbeats 4000000 in
private theorem offsetP_check : (1589/10000 : ℚ) ≤ offsetPIv.lo ∧ offsetPIv.hi ≤ 2893/10000 := by
  decide +kernel

set_option maxRecDepth 10000 in
set_option maxHeartbeats 4000000 in
private theorem offsetQ_check : (-1322/10000 : ℚ) ≤ offsetQIv.lo ∧ offsetQIv.hi ≤ 365/10000 := by
  decide +kernel

end OffsetBounds

/-- Both owner-a offsets lie in the wedge theorem's ranges on the actual hull H. -/
theorem hull_offset_bounds {θ dx dy : ℕ → ℝ} {L : ℝ} (h : Good Hull.prob θ dx dy L) :
    (1589/10000 ≤ offsetP (cenOf dx dy OffsetBounds.q2) (cenOf dx dy OffsetBounds.q14)
      (angOf θ OffsetBounds.q2) (Real.pi/4 + θ 13) ∧
     offsetP (cenOf dx dy OffsetBounds.q2) (cenOf dx dy OffsetBounds.q14)
      (angOf θ OffsetBounds.q2) (Real.pi/4 + θ 13) ≤ 2893/10000) ∧
    (-1322/10000 ≤ offsetQ (cenOf dx dy OffsetBounds.q10) (cenOf dx dy OffsetBounds.q11)
      (angOf θ OffsetBounds.q10) (Real.pi/4 + θ 13) ∧
     offsetQ (cenOf dx dy OffsetBounds.q10) (cenOf dx dy OffsetBounds.q11)
      (angOf θ OffsetBounds.q10) (Real.pi/4 + θ 13) ≤ 365/10000) := by
  have hp := OffsetBounds.offsetP_mem h
  have hq := OffsetBounds.offsetQ_mem h
  have hpc : (1589/10000 : ℝ) ≤ OffsetBounds.offsetPIv.lo ∧
      (OffsetBounds.offsetPIv.hi : ℝ) ≤ 2893/10000 := by
    constructor
    · convert (Rat.cast_le (K := ℝ)).mpr OffsetBounds.offsetP_check.1 using 1 <;> norm_num
    · convert (Rat.cast_le (K := ℝ)).mpr OffsetBounds.offsetP_check.2 using 1 <;> norm_num
  have hqc : (-1322/10000 : ℝ) ≤ OffsetBounds.offsetQIv.lo ∧
      (OffsetBounds.offsetQIv.hi : ℝ) ≤ 365/10000 := by
    constructor
    · convert (Rat.cast_le (K := ℝ)).mpr OffsetBounds.offsetQ_check.1 using 1 <;> norm_num
    · convert (Rat.cast_le (K := ℝ)).mpr OffsetBounds.offsetQ_check.2 using 1 <;> norm_num
  exact ⟨⟨hpc.1.trans hp.1, hp.2.trans hpc.2⟩,
    ⟨hqc.1.trans hq.1, hq.2.trans hqc.2⟩⟩

/-- The exact owner-a P interval used by the wedge theorem. -/
def tightOffPIv : Iv := ⟨1589/10000, 2893/10000⟩
/-- The exact owner-a Q interval used by the wedge theorem. -/
def tightOffQIv : Iv := ⟨-1322/10000, 365/10000⟩

/-- Actual P offset membership, in the interval API consumed by owner-a rows. -/
theorem tight_offsetP_mem {θ dx dy : ℕ → ℝ} {L : ℝ} (h : Good Hull.prob θ dx dy L) :
    Iv.mem (offsetP (cenOf dx dy OffsetBounds.q2) (cenOf dx dy OffsetBounds.q14)
      (angOf θ OffsetBounds.q2) (Real.pi/4 + θ 13)) tightOffPIv := by
  simpa only [Iv.mem, tightOffPIv, Rat.cast_div, Rat.cast_ofNat] using (hull_offset_bounds h).1

/-- Actual Q offset membership, in the interval API consumed by owner-a rows. -/
theorem tight_offsetQ_mem {θ dx dy : ℕ → ℝ} {L : ℝ} (h : Good Hull.prob θ dx dy L) :
    Iv.mem (offsetQ (cenOf dx dy OffsetBounds.q10) (cenOf dx dy OffsetBounds.q11)
      (angOf θ OffsetBounds.q10) (Real.pi/4 + θ 13)) tightOffQIv := by
  simpa only [Iv.mem, tightOffQIv, Rat.cast_div, Rat.cast_neg, Rat.cast_ofNat] using (hull_offset_bounds h).2

end Sq19.Endgame

#print axioms Sq19.Endgame.hull_offset_bounds
#print axioms Sq19.Endgame.tight_offsetP_mem
#print axioms Sq19.Endgame.tight_offsetQ_mem
