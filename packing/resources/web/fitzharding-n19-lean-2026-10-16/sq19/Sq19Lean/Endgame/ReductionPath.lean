import Sq19Lean.Endgame.ReductionCases

/-!
# Composition along the signed cone-prefix path

The five relevant axes are restored in the order 1, 2, 10, the excess of the
larger of |θ5| and |θ8|, then their common magnitude. Every endpoint remains in
the actual hull interval. No packing is assumed after zeroing the angles.
-/
namespace Sq19.Endgame.Reduction
open Sq19.Milp

/-- Zero precisely the five axis angles used by the local expression. -/
def axisZero (θ : ℕ → ℝ) : ℕ → ℝ :=
  fun k => if k ∈ [1,2,5,8,10] then 0 else θ k

private def partialAxes (θ : ℕ → ℝ) (x1 x2 x5 x8 x10 : ℝ) : ℕ → ℝ :=
  fun k => if k=1 then x1 else if k=2 then x2 else if k=5 then x5
    else if k=8 then x8 else if k=10 then x10 else θ k

private theorem partial_zero (θ : ℕ → ℝ) : partialAxes θ 0 0 0 0 0 = axisZero θ := by
  funext k
  simp only [partialAxes, axisZero, List.mem_cons, List.not_mem_nil, or_false]
  split_ifs <;> simp_all

private theorem partial_full (θ : ℕ → ℝ) : partialAxes θ (θ 1) (θ 2) (θ 5) (θ 8) (θ 10) = θ := by
  funext k
  simp only [partialAxes]
  split_ifs <;> simp_all

/-- The hull contains zero at every axis coordinate used by the path. -/
theorem axis_zero_mem {k : ℕ} (hk : k ∈ [1,2,5,8,10]) :
    Iv.mem (0 : ℝ) (Hull.prob.rootAng k) := by
  have h : (Hull.prob.rootAng k).lo ≤ 0 ∧ 0 ≤ (Hull.prob.rootAng k).hi := by
    simp only [List.mem_cons, List.not_mem_nil, or_false] at hk
    rcases hk with rfl | rfl | rfl | rfl | rfl <;> decide +kernel
  constructor
  · exact_mod_cast h.1
  · exact_mod_cast h.2

private theorem partial_mem {θ : ℕ → ℝ} (hθ : InAng θ Hull.prob.rootAng)
    {x1 x2 x5 x8 x10 : ℝ}
    (h1 : Iv.mem x1 (Hull.prob.rootAng 1)) (h2 : Iv.mem x2 (Hull.prob.rootAng 2))
    (h5 : Iv.mem x5 (Hull.prob.rootAng 5)) (h8 : Iv.mem x8 (Hull.prob.rootAng 8))
    (h10 : Iv.mem x10 (Hull.prob.rootAng 10)) :
    InAng (partialAxes θ x1 x2 x5 x8 x10) Hull.prob.rootAng := by
  intro k
  simp only [partialAxes]
  split_ifs <;> subst_vars <;> first | assumption | exact hθ _

/-- Zeroing the axis coordinates stays in H. -/
theorem axisZero_mem {θ : ℕ → ℝ} (hθ : InAng θ Hull.prob.rootAng) :
    InAng (axisZero θ) Hull.prob.rootAng := by
  rw [← partial_zero]
  exact partial_mem hθ (axis_zero_mem (by simp)) (axis_zero_mem (by simp))
    (axis_zero_mem (by simp)) (axis_zero_mem (by simp)) (axis_zero_mem (by simp))

private theorem sg_abs {x : ℝ} {b : Bool} (h : 0 ≤ (sg b : ℝ)*x) :
    (sg b : ℝ)*|x| = x := by
  cases b <;> simp only [sg] at h ⊢ <;> push_cast at h ⊢
  · rw [abs_of_nonpos (by linarith)]; ring
  · rw [abs_of_nonneg (by linarith)]; ring

/-- A point with the same sign and smaller magnitude remains between zero and x. -/
private theorem signed_mem {I : Iv} {x t : ℝ} {b : Bool}
    (h0 : Iv.mem (0 : ℝ) I) (hx : Iv.mem x I) (hs : 0 ≤ (sg b : ℝ)*x)
    (ht0 : 0 ≤ t) (htx : t ≤ |x|) : Iv.mem ((sg b : ℝ)*t) I := by
  cases b <;> simp only [sg] at hs ⊢ <;> push_cast at hs ⊢
  · have hx0 : x ≤ 0 := by linarith
    rw [abs_of_nonpos hx0] at htx
    constructor <;> linarith [h0.1,h0.2,hx.1,hx.2]
  · have hx0 : 0 ≤ x := by linarith
    rw [abs_of_nonneg hx0] at htx
    constructor <;> linarith [h0.1,h0.2,hx.1,hx.2]

/-- Apply one accepted direction using interval membership at its two endpoints. -/
theorem step_between (c : Case) (hc : slopeCheck c = true)
    (v : ℕ → ℚ) (hv : v ∈ c.directions) {α β : ℕ → ℝ} {t : ℝ}
    (ht : 0 ≤ t) (he : angleLine α v t = β)
    (hα : InAng α Hull.prob.rootAng) (hβ : InAng β Hull.prob.rootAng) :
    c.margin.real α ≤ c.margin.real β := by
  have ez : angleLine α v 0 = α := by funext k; simp [angleLine]
  have h := step_mono c hc v hv α ht
    (by simpa only [ez,table,radii] using boxH_bound hα)
    (by rw [he]; exact boxH_bound hβ)
  rw [ez,he] at h
  exact h

private theorem line1 (θ : ℕ → ℝ) (x1 x2 x5 x8 x10 t : ℝ) (b : Bool) :
    angleLine (partialAxes θ x1 x2 x5 x8 x10) (coordinate 1 b) t =
      partialAxes θ (x1+(sg b : ℝ)*t) x2 x5 x8 x10 := by
  funext k
  simp only [angleLine,partialAxes,coordinate,beq_iff_eq]
  split_ifs <;> simp_all

private theorem line2 (θ : ℕ → ℝ) (x1 x2 x5 x8 x10 t : ℝ) (b : Bool) :
    angleLine (partialAxes θ x1 x2 x5 x8 x10) (coordinate 2 b) t =
      partialAxes θ x1 (x2+(sg b : ℝ)*t) x5 x8 x10 := by
  funext k
  simp only [angleLine,partialAxes,coordinate,beq_iff_eq]
  split_ifs <;> simp_all

private theorem line10 (θ : ℕ → ℝ) (x1 x2 x5 x8 x10 t : ℝ) (b : Bool) :
    angleLine (partialAxes θ x1 x2 x5 x8 x10) (coordinate 10 b) t =
      partialAxes θ x1 x2 x5 x8 (x10+(sg b : ℝ)*t) := by
  funext k
  simp only [angleLine,partialAxes,coordinate,beq_iff_eq]
  split_ifs <;> simp_all

private theorem line5 (θ : ℕ → ℝ) (x1 x2 x5 x8 x10 t : ℝ) (b : Bool) :
    angleLine (partialAxes θ x1 x2 x5 x8 x10) (coordinate 5 b) t =
      partialAxes θ x1 x2 (x5+(sg b : ℝ)*t) x8 x10 := by
  funext k
  simp only [angleLine,partialAxes,coordinate,beq_iff_eq]
  split_ifs <;> simp_all

private theorem line8 (θ : ℕ → ℝ) (x1 x2 x5 x8 x10 t : ℝ) (b : Bool) :
    angleLine (partialAxes θ x1 x2 x5 x8 x10) (coordinate 8 b) t =
      partialAxes θ x1 x2 x5 (x8+(sg b : ℝ)*t) x10 := by
  funext k
  simp only [angleLine,partialAxes,coordinate,beq_iff_eq]
  split_ifs <;> simp_all

private theorem line58 (θ : ℕ → ℝ) (x1 x2 x5 x8 x10 t : ℝ) (b5 b8 : Bool) :
    angleLine (partialAxes θ x1 x2 x5 x8 x10)
      (fun j => coordinate 5 b5 j+coordinate 8 b8 j) t =
      partialAxes θ x1 x2 (x5+(sg b5 : ℝ)*t) (x8+(sg b8 : ℝ)*t) x10 := by
  funext k
  simp only [angleLine,partialAxes,coordinate,beq_iff_eq]
  split_ifs <;> simp_all

/-- Five signed cone-prefix steps increase the endpoint residual from the
axis-zero evaluation to the original configuration. No packing at zero is used. -/
theorem margin_axisZero_le (c : Case) (hc : slopeCheck c = true)
    {θ : ℕ → ℝ} (hθ : InAng θ Hull.prob.rootAng)
    (h1 : 0 ≤ (sg c.b1 : ℝ)*θ 1) (h2 : 0 ≤ (sg c.b2 : ℝ)*θ 2)
    (h5 : 0 ≤ (sg c.b5 : ℝ)*θ 5) (h8 : 0 ≤ (sg c.b8 : ℝ)*θ 8)
    (h10 : 0 ≤ (sg c.b10 : ℝ)*θ 10)
    (horder : if c.fiveLarger then |θ 8| ≤ |θ 5| else |θ 5| ≤ |θ 8|) :
    c.margin.real (axisZero θ) ≤ c.margin.real θ := by
  have z1 : Iv.mem (0 : ℝ) (Hull.prob.rootAng 1) := axis_zero_mem (by simp)
  have z2 : Iv.mem (0 : ℝ) (Hull.prob.rootAng 2) := axis_zero_mem (by simp)
  have z5 : Iv.mem (0 : ℝ) (Hull.prob.rootAng 5) := axis_zero_mem (by simp)
  have z8 : Iv.mem (0 : ℝ) (Hull.prob.rootAng 8) := axis_zero_mem (by simp)
  have z10 : Iv.mem (0 : ℝ) (Hull.prob.rootAng 10) := axis_zero_mem (by simp)
  let a0 := partialAxes θ 0 0 0 0 0
  let a1 := partialAxes θ (θ 1) 0 0 0 0
  let a2 := partialAxes θ (θ 1) (θ 2) 0 0 0
  let a3 := partialAxes θ (θ 1) (θ 2) 0 0 (θ 10)
  have m0 : InAng a0 Hull.prob.rootAng := partial_mem hθ z1 z2 z5 z8 z10
  have m1 : InAng a1 Hull.prob.rootAng := partial_mem hθ (hθ 1) z2 z5 z8 z10
  have m2 : InAng a2 Hull.prob.rootAng := partial_mem hθ (hθ 1) (hθ 2) z5 z8 z10
  have m3 : InAng a3 Hull.prob.rootAng := partial_mem hθ (hθ 1) (hθ 2) z5 z8 (hθ 10)
  have p1 : c.margin.real a0 ≤ c.margin.real a1 := by
    apply step_between c hc (coordinate 1 c.b1) (by simp [Case.directions]) (abs_nonneg (θ 1)) ?_ m0 m1
    simp only [a0,a1,line1,zero_add,sg_abs h1]
  have p2 : c.margin.real a1 ≤ c.margin.real a2 := by
    apply step_between c hc (coordinate 2 c.b2) (by simp [Case.directions]) (abs_nonneg (θ 2)) ?_ m1 m2
    simp only [a1,a2,line2,zero_add,sg_abs h2]
  have p3 : c.margin.real a2 ≤ c.margin.real a3 := by
    apply step_between c hc (coordinate 10 c.b10) (by simp [Case.directions]) (abs_nonneg (θ 10)) ?_ m2 m3
    simp only [a2,a3,line10,zero_add,sg_abs h10]
  have tail : c.margin.real a3 ≤ c.margin.real θ := by
    cases he : c.fiveLarger
    · simp only [he,Bool.false_eq_true,↓reduceIte] at horder
      let t := |θ 8|-|θ 5|
      let a4 := partialAxes θ (θ 1) (θ 2) 0 ((sg c.b8 : ℝ)*t) (θ 10)
      have ht : 0 ≤ t := sub_nonneg.mpr horder
      have mt : Iv.mem ((sg c.b8 : ℝ)*t) (Hull.prob.rootAng 8) :=
        signed_mem z8 (hθ 8) h8 ht (by dsimp [t]; linarith [abs_nonneg (θ 5)])
      have m4 : InAng a4 Hull.prob.rootAng := partial_mem hθ (hθ 1) (hθ 2) z5 mt (hθ 10)
      have p4 : c.margin.real a3 ≤ c.margin.real a4 := by
        apply step_between c hc (coordinate 8 c.b8) (by simp [Case.directions,he]) ht ?_ m3 m4
        simp only [a3,a4,line8,zero_add]
      have p5 : c.margin.real a4 ≤ c.margin.real θ := by
        apply step_between c hc (fun j => coordinate 5 c.b5 j+coordinate 8 c.b8 j)
          (by simp [Case.directions]) (abs_nonneg (θ 5)) ?_ m4 hθ
        rw [show a4 = partialAxes θ (θ 1) (θ 2) 0 ((sg c.b8 : ℝ)*t) (θ 10) from rfl,
          line58,zero_add,sg_abs h5]
        have ee : (sg c.b8 : ℝ)*t+(sg c.b8 : ℝ)*|θ 5| = θ 8 := by
          rw [← mul_add]; dsimp only [t]; rw [sub_add_cancel,sg_abs h8]
        rw [ee,partial_full]
      exact p4.trans p5
    · simp only [he,↓reduceIte] at horder
      let t := |θ 5|-|θ 8|
      let a4 := partialAxes θ (θ 1) (θ 2) ((sg c.b5 : ℝ)*t) 0 (θ 10)
      have ht : 0 ≤ t := sub_nonneg.mpr horder
      have mt : Iv.mem ((sg c.b5 : ℝ)*t) (Hull.prob.rootAng 5) :=
        signed_mem z5 (hθ 5) h5 ht (by dsimp [t]; linarith [abs_nonneg (θ 8)])
      have m4 : InAng a4 Hull.prob.rootAng := partial_mem hθ (hθ 1) (hθ 2) mt z8 (hθ 10)
      have p4 : c.margin.real a3 ≤ c.margin.real a4 := by
        apply step_between c hc (coordinate 5 c.b5) (by simp [Case.directions,he]) ht ?_ m3 m4
        simp only [a3,a4,line5,zero_add]
      have p5 : c.margin.real a4 ≤ c.margin.real θ := by
        apply step_between c hc (fun j => coordinate 5 c.b5 j+coordinate 8 c.b8 j)
          (by simp [Case.directions]) (abs_nonneg (θ 8)) ?_ m4 hθ
        rw [show a4 = partialAxes θ (θ 1) (θ 2) ((sg c.b5 : ℝ)*t) 0 (θ 10) from rfl,
          line58,zero_add,sg_abs h8]
        have ee : (sg c.b5 : ℝ)*t+(sg c.b5 : ℝ)*|θ 8| = θ 5 := by
          rw [← mul_add]; dsimp only [t]; rw [sub_add_cancel,sg_abs h5]
        rw [ee,partial_full]
      exact p4.trans p5
  simpa only [a0,partial_zero] using p1.trans (p2.trans (p3.trans tail))

end Sq19.Endgame.Reduction

#print axioms Sq19.Endgame.Reduction.axisZero_mem
#print axioms Sq19.Endgame.Reduction.margin_axisZero_le
