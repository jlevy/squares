import Sq19Lean.Endgame.RowsA
import Sq19Lean.Endgame.Separations
import Sq19Lean.Endgame.PhiExpr

/-!
# Offset enclosures and sign facts on H (owner-a rows)

`offsetP` and `offsetQ` (the corner projections O1, O2 of `mkcap.c`) lie in rational intervals on
every configuration of H, by Taylor ranges of the angle parts and the position boxes. The sign facts
used by `rowP_a`, `rowQ_a` (all relative angles involved stay in the first quadrant) also hold on H.
That P (Q) is the extreme corner of square 2 (10) is `cornerP_support` (`cornerQ_support`) in
`RowsA`; its hypotheses are among the sign facts here.
-/
namespace Sq19.Endgame
open Sq19.Milp Sq19.Endgame.Hull

/-- Taylor range of an angle expression on H. -/
def rngH (e : Ex) : Iv := (e.tf (boxTrig prob.rootAng) (boxH prob.rootAng)).range (boxH prob.rootAng)

/-- Angle part of `offsetP`: `e1(13) . R(φ2)(1/2, -1/2)`. -/
def offPE : Ex :=
  .mul (.c (1/2)) (.add (.mul (.cs 13 1) (.add (.cs 2 0) (.sn 2 0)))
    (.mul (.sn 13 1) (.add (.sn 2 0) (.neg (.cs 2 0)))))

/-- Angle part of `offsetQ`: `-e2(13) . R(φ10)(-1/2, -1/2)`. -/
def offQE : Ex :=
  .mul (.c (1/2)) (.add (.mul (.sn 13 1) (.add (.sn 10 0) (.neg (.cs 10 0))))
    (.mul (.cs 13 1) (.add (.sn 10 0) (.cs 10 0))))

/-- Position differences on H: `c2 - c14` and `c11 - c10`. -/
def dPx : Iv := dIv (prob.sq 8).rx (prob.sq 1).rx (prob.sq 8).x (prob.sq 1).x
def dPy : Iv := dIv (prob.sq 8).ry (prob.sq 1).ry (prob.sq 8).y (prob.sq 1).y
def dQx : Iv := dIv (prob.sq 5).rx (prob.sq 6).rx (prob.sq 5).x (prob.sq 6).x
def dQy : Iv := dIv (prob.sq 5).ry (prob.sq 6).ry (prob.sq 5).y (prob.sq 6).y

/-- An interval moved to be centred at `0`. -/
def ivCen (I : Iv) : Iv := ⟨I.lo - I.mid, I.hi - I.mid⟩

theorem mem_ivCen {x : ℝ} {I : Iv} (h : Iv.mem x I) : Iv.mem (x - I.mid) (ivCen I) := by
  simp only [Iv.mem, ivCen] at h ⊢; push_cast; constructor <;> linarith [h.1, h.2]

/-- Enclosure of `offsetP` on H (squares 2, 14 at list positions 1, 8), in centred form. -/
def offPIv : Iv :=
  (rngH (.add offPE (.add (.mul (.cs 13 1) (.c dPx.mid)) (.mul (.sn 13 1) (.c dPy.mid))))).add
    (((rngH (.cs 13 1)).mul (ivCen dPx)).add ((rngH (.sn 13 1)).mul (ivCen dPy)))

/-- Enclosure of `offsetQ` on H (squares 10, 11 at list positions 5, 6), in centred form. -/
def offQIv : Iv :=
  (rngH (.add offQE (.add (.mul (.neg (.sn 13 1)) (.c dQx.mid)) (.mul (.cs 13 1) (.c dQy.mid))))).add
    (((rngH (.neg (.sn 13 1))).mul (ivCen dQx)).add ((rngH (.cs 13 1)).mul (ivCen dQy)))

section
variable {θ dx dy : ℕ → ℝ} {L : ℝ}

theorem mem_rngH (hg : Good prob θ dx dy L) (e : Ex) : Iv.mem (e.real θ) (rngH e) :=
  ex_mem_range hg.ang e

theorem offsetP_mem (hg : Good prob θ dx dy L) :
    Iv.mem (offsetP (cH dx dy 1) (cH dx dy 8) (angE θ 2 0) (angE θ 13 1)) offPIv := by
  have p1 := hg.pos _ (prob.sq_mem (i := 1) (by decide))
  have p8 := hg.pos _ (prob.sq_mem (i := 8) (by decide))
  have hx : Iv.mem _ dPx := mem_dIv (rA := (prob.sq 8).rx) (rB := (prob.sq 1).rx) p8.1 p1.1
  have hy : Iv.mem _ dPy := mem_dIv (rA := (prob.sq 8).ry) (rB := (prob.sq 1).ry) p8.2 p1.2
  have key : offsetP (cH dx dy 1) (cH dx dy 8) (angE θ 2 0) (angE θ 13 1) =
      offPE.real θ + ((Ex.cs 13 1).real θ * ((((prob.sq 1).rx : ℝ) + dx (prob.sq 1).s) -
        (((prob.sq 8).rx : ℝ) + dx (prob.sq 8).s)) +
      (Ex.sn 13 1).real θ * ((((prob.sq 1).ry : ℝ) + dy (prob.sq 1).s) -
        (((prob.sq 8).ry : ℝ) + dy (prob.sq 8).s))) := by
    simp only [offsetP, proj1, corner, cH, cenOf, offPE, Ex.real, vx, vy, ox, oy, angE,
      Prod.fst_sub, Prod.snd_sub]
    norm_num; ring
  have h : Iv.mem _ offPIv := Iv.mem_add (mem_rngH hg _)
    (Iv.mem_add (Iv.mem_mul (mem_rngH hg _) (mem_ivCen hx)) (Iv.mem_mul (mem_rngH hg _) (mem_ivCen hy)))
  rw [key]; convert h using 1; simp only [Ex.real]; ring

theorem offsetQ_mem (hg : Good prob θ dx dy L) :
    Iv.mem (offsetQ (cH dx dy 5) (cH dx dy 6) (angE θ 10 0) (angE θ 13 1)) offQIv := by
  have p5 := hg.pos _ (prob.sq_mem (i := 5) (by decide))
  have p6 := hg.pos _ (prob.sq_mem (i := 6) (by decide))
  have hx : Iv.mem _ dQx := mem_dIv (rA := (prob.sq 5).rx) (rB := (prob.sq 6).rx) p5.1 p6.1
  have hy : Iv.mem _ dQy := mem_dIv (rA := (prob.sq 5).ry) (rB := (prob.sq 6).ry) p5.2 p6.2
  have key : offsetQ (cH dx dy 5) (cH dx dy 6) (angE θ 10 0) (angE θ 13 1) =
      offQE.real θ + ((Ex.neg (.sn 13 1)).real θ * ((((prob.sq 6).rx : ℝ) + dx (prob.sq 6).s) -
        (((prob.sq 5).rx : ℝ) + dx (prob.sq 5).s)) +
      (Ex.cs 13 1).real θ * ((((prob.sq 6).ry : ℝ) + dy (prob.sq 6).s) -
        (((prob.sq 5).ry : ℝ) + dy (prob.sq 5).s))) := by
    simp only [offsetQ, proj2, corner, cH, cenOf, offQE, Ex.real, vx, vy, ox, oy, angE,
      Prod.fst_sub, Prod.snd_sub]
    norm_num; ring
  have h : Iv.mem _ offQIv := Iv.mem_add (mem_rngH hg _)
    (Iv.mem_add (Iv.mem_mul (mem_rngH hg _) (mem_ivCen hx)) (Iv.mem_mul (mem_rngH hg _) (mem_ivCen hy)))
  rw [key]; convert h using 1; simp only [Ex.real]; ring

/-- List positions of H against square numbers: `φH θ i = angE θ s m`. -/
theorem φH_eq (θ : ℕ → ℝ) :
    φH θ 0 = angE θ 1 0 ∧ φH θ 1 = angE θ 2 0 ∧ φH θ 2 = angE θ 5 0 ∧ φH θ 3 = angE θ 7 0 ∧
    φH θ 4 = angE θ 8 0 ∧ φH θ 5 = angE θ 10 0 ∧ φH θ 6 = angE θ 11 1 ∧ φH θ 7 = angE θ 13 1 ∧
    φH θ 8 = angE θ 14 1 :=
  ⟨rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl, rfl⟩

/-- A sign certificate: the Taylor range on H is positive. -/
theorem pos_of_rngH (hg : Good prob θ dx dy L) (e : Ex) (h : 0 < (rngH e).lo) : 0 < e.real θ := by
  have m := (mem_rngH hg e).1
  have : (0 : ℝ) < ((rngH e).lo : ℝ) := by exact_mod_cast h
  linarith

/-- An enclosure gives the `sin d * O ≤ sin d * offset` hypothesis of the owner-a rows, either sign. -/
theorem mul_endpoint_le {s x : ℝ} {I : Iv} (hx : Iv.mem x I) :
    (0 ≤ s → s * I.lo ≤ s * x) ∧ (s ≤ 0 → s * I.hi ≤ s * x) :=
  ⟨fun h => mul_le_mul_of_nonneg_left hx.1 h, fun h => mul_le_mul_of_nonpos_left hx.2 h⟩

set_option maxRecDepth 100000 in
/-- The sign facts of `rowP_a`, `rowQ_a` (and of `cornerP_support`, `cornerQ_support`) on H. -/
theorem ownerA_signs (hg : Good prob θ dx dy L) :
    0 < Real.sin (angE θ 13 1) ∧ 0 < Real.cos (angE θ 13 1) ∧
    0 < Real.sin (angE θ 13 1 - angE θ 2 0) ∧ 0 < Real.cos (angE θ 13 1 - angE θ 2 0) ∧
    0 < Real.cos (angE θ 14 1 - angE θ 13 1) ∧
    0 < Real.sin (angE θ 13 1 - angE θ 10 0) ∧ 0 < Real.cos (angE θ 13 1 - angE θ 10 0) ∧
    0 < Real.cos (angE θ 11 1 - angE θ 13 1) ∧
    0 < Real.cos (angE θ 1 0) ∧ 0 < Real.cos (angE θ 2 0) := by
  have p := fun e h => pos_of_rngH (θ := θ) hg e h
  rw [← sinD_real, ← cosD_real, ← cosD_real, ← sinD_real, ← cosD_real, ← cosD_real]
  exact ⟨p (.sn 13 1) (by decide +kernel), p (.cs 13 1) (by decide +kernel),
    p _ (by decide +kernel), p _ (by decide +kernel), p _ (by decide +kernel),
    p _ (by decide +kernel), p _ (by decide +kernel), p _ (by decide +kernel),
    p (.cs 1 0) (by decide +kernel), p (.cs 2 0) (by decide +kernel)⟩

end

end Sq19.Endgame

open Sq19.Endgame in
#eval [offPIv.lo, offPIv.hi, offQIv.lo, offQIv.hi].map (fun q : ℚ => ⌊q * 1000000⌋)
#print axioms Sq19.Endgame.offsetP_mem
#print axioms Sq19.Endgame.offsetQ_mem
#print axioms Sq19.Endgame.ownerA_signs
