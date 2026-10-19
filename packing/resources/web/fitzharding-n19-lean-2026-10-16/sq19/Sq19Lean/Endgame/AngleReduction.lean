import Sq19Lean.Endgame.Combine
import Sq19Lean.Milp.Deriv

/-!
# Exact derivatives along signed cone-prefix directions

The relevant path is a ray or a sequence of cone-prefix moves, not an arbitrary
sequence of coordinate moves: the latter can cross the branch where two axis
angles coincide. `Ex.alongDeriv` differentiates in any rational direction.
`Ex.along_step_lb` proves the Taylor certificate's lower bound on that move.
It covers both nonnegative cone slopes and a negative correction paid for by
an independently certified value margin. No numerical assertion about H is
assumed or proved in this module.
-/
namespace Sq19.Milp

/-- A line in angle space; signed prefixes have coefficients in {-1,0,1}. -/
def angleLine (θ : ℕ → ℝ) (v : ℕ → ℚ) (t : ℝ) : ℕ → ℝ :=
  fun k => θ k + (v k : ℝ) * t

/-- Sufficient syntactic test that an expression is constant along a line. -/
def Ex.stationary (v : ℕ → ℚ) : Ex → Bool
  | .c _ => true
  | .cs k _ => v k == 0
  | .sn k _ => v k == 0
  | .add a b => a.stationary v && b.stationary v
  | .mul a b => a.stationary v && b.stationary v
  | .neg a => a.stationary v
  | .abs a => a.stationary v

/-- Every absolute-value operand is constant along the direction. In particular,
absolute values of tilted-angle differences are harmless for an axis-only move. -/
def Ex.smoothAlong (v : ℕ → ℚ) : Ex → Bool
  | .c _ | .cs _ _ | .sn _ _ => true
  | .add a b => a.smoothAlong v && b.smoothAlong v
  | .mul a b => a.smoothAlong v && b.smoothAlong v
  | .neg a => a.smoothAlong v
  | .abs a => a.stationary v

/-- Exact symbolic directional derivative, still in the division-free language. -/
def Ex.alongDeriv (v : ℕ → ℚ) : Ex → Ex
  | .c _ => .c 0
  | .cs k M => .mul (.c (v k)) (.neg (.sn k M))
  | .sn k M => .mul (.c (v k)) (.cs k M)
  | .add a b => .add (a.alongDeriv v) (b.alongDeriv v)
  | .mul a b => .add (.mul (a.alongDeriv v) b) (.mul a (b.alongDeriv v))
  | .neg a => .neg (a.alongDeriv v)
  | .abs _ => .c 0

theorem Ex.real_line_of_stationary (v : ℕ → ℚ) (θ : ℕ → ℝ) (t : ℝ) (e : Ex)
    (h : e.stationary v = true) : e.real (angleLine θ v t) = e.real θ := by
  induction e with
  | c q => rfl
  | cs k M =>
    simp only [Ex.stationary, beq_iff_eq] at h
    simp [Ex.real, angleLine, h]
  | sn k M =>
    simp only [Ex.stationary, beq_iff_eq] at h
    simp [Ex.real, angleLine, h]
  | add a b ha hb =>
    simp only [Ex.stationary, Bool.and_eq_true] at h
    simp only [Ex.real, ha h.1, hb h.2]
  | mul a b ha hb =>
    simp only [Ex.stationary, Bool.and_eq_true] at h
    simp only [Ex.real, ha h.1, hb h.2]
  | neg a ha => simp only [Ex.stationary] at h; simp only [Ex.real, ha h]
  | abs a ha => simp only [Ex.stationary] at h; simp only [Ex.real, ha h]

theorem Ex.hasDerivAt_line (v : ℕ → ℚ) (θ : ℕ → ℝ) (e : Ex) (t : ℝ)
    (hf : e.smoothAlong v = true) :
    HasDerivAt (fun x => e.real (angleLine θ v x))
      ((e.alongDeriv v).real (angleLine θ v t)) t := by
  induction e with
  | c q => simpa [Ex.real, Ex.alongDeriv] using hasDerivAt_const t (q : ℝ)
  | cs k M =>
    have hd : HasDerivAt (fun x : ℝ => (M : ℝ) * Real.pi / 4 +
        (θ k + (v k : ℝ) * x)) (v k : ℝ) t := by
      convert (((hasDerivAt_id t).const_mul (v k : ℝ)).const_add (θ k)).const_add
        ((M : ℝ) * Real.pi / 4) using 1 <;> simp
    simpa [Ex.real, Ex.alongDeriv, angleLine, mul_comm, mul_neg] using hd.cos
  | sn k M =>
    have hd : HasDerivAt (fun x : ℝ => (M : ℝ) * Real.pi / 4 +
        (θ k + (v k : ℝ) * x)) (v k : ℝ) t := by
      convert (((hasDerivAt_id t).const_mul (v k : ℝ)).const_add (θ k)).const_add
        ((M : ℝ) * Real.pi / 4) using 1 <;> simp
    simpa [Ex.real, Ex.alongDeriv, angleLine, mul_comm] using hd.sin
  | add a b ha hb =>
    simp only [Ex.smoothAlong, Bool.and_eq_true] at hf
    simp only [Ex.real, Ex.alongDeriv]
    exact (ha hf.1).add (hb hf.2)
  | mul a b ha hb =>
    simp only [Ex.smoothAlong, Bool.and_eq_true] at hf
    simp only [Ex.real, Ex.alongDeriv]
    exact (ha hf.1).mul (hb hf.2)
  | neg a ha =>
    simp only [Ex.smoothAlong] at hf
    simp only [Ex.real, Ex.alongDeriv]
    exact (ha hf).neg
  | abs a _ =>
    simp only [Ex.smoothAlong] at hf
    have he : (fun x => |a.real (angleLine θ v x)|) = fun _ => |a.real θ| := by
      funext x
      rw [Ex.real_line_of_stationary v θ x a hf]
    simp only [Ex.real, Ex.alongDeriv]
    rw [he]
    simpa using hasDerivAt_const t (|a.real θ|)

/-- A line segment is inside a coordinate box if its two endpoints are. -/
theorem angleLine_box_of_endpoints (θ : ℕ → ℝ) (v : ℕ → ℚ)
    (c : ℕ → ℝ) (H : ℕ → ℚ) {u w : ℝ}
    (hu : ∀ j, |angleLine θ v u j - c j| ≤ H j)
    (hw : ∀ j, |angleLine θ v w j - c j| ≤ H j) :
    ∀ x ∈ Set.Icc u w, ∀ j, |angleLine θ v x j - c j| ≤ H j := by
  intro x hx j
  have huj := abs_le.mp (hu j)
  have hwj := abs_le.mp (hw j)
  simp only [angleLine] at huj hwj ⊢
  rw [abs_le]
  by_cases hv : 0 ≤ (v j : ℝ)
  · have h1 := mul_le_mul_of_nonneg_left hx.1 hv
    have h2 := mul_le_mul_of_nonneg_left hx.2 hv
    constructor <;> linarith
  · have hv' : (v j : ℝ) ≤ 0 := le_of_not_ge hv
    have h1 := mul_le_mul_of_nonpos_left hx.1 hv'
    have h2 := mul_le_mul_of_nonpos_left hx.2 hv'
    constructor <;> linarith

/-- Lower bound from an exact Taylor enclosure of the directional derivative. -/
theorem Ex.along_step_lb {T : Trig} (hT : T.Valid) (H : ℕ → ℚ)
    (e : Ex) (v : ℕ → ℚ) (θ : ℕ → ℝ) {u w : ℝ}
    (hf : e.smoothAlong v = true) (huw : u ≤ w)
    (hbox : ∀ x ∈ Set.Icc u w, ∀ j, |angleLine θ v x j - T.cen j| ≤ H j) :
    (w - u) * ((((e.alongDeriv v).tf T H).range H).lo : ℝ) ≤
      e.real (angleLine θ v w) - e.real (angleLine θ v u) := by
  set f := fun x => e.real (angleLine θ v x)
  set D : ℝ := ((((e.alongDeriv v).tf T H).range H).lo : ℝ)
  have hd : ∀ x, HasDerivAt f ((e.alongDeriv v).real (angleLine θ v x)) x :=
    fun x => Ex.hasDerivAt_line v θ e x hf
  have hD : ∀ x ∈ Set.Icc u w, D ≤ (e.alongDeriv v).real (angleLine θ v x) := by
    intro x hx
    have hm := TF.mem_range (Ex.tf_encl hT H (e.alongDeriv v))
      (fun j => angleLine θ v x j - T.cen j) (hbox x hx)
    have he : (fun s => (T.cen s : ℝ) + (angleLine θ v x s - T.cen s)) =
        angleLine θ v x := by funext s; ring
    rw [he] at hm
    exact hm.1
  have hdx : ∀ x, HasDerivAt (fun x => f x - D * x)
      ((e.alongDeriv v).real (angleLine θ v x) - D) x := by
    intro x
    have h2 : HasDerivAt (fun x : ℝ => D * x) D x := by
      simpa using (hasDerivAt_id x).const_mul D
    exact (hd x).sub h2
  have hmono : MonotoneOn (fun x => f x - D * x) (Set.Icc u w) := by
    apply monotoneOn_of_deriv_nonneg (convex_Icc u w)
    · exact HasDerivAt.continuousOn (fun x _ => hdx x)
    · intro x _; exact (hdx x).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [interior_Icc] at hx
      rw [(hdx x).deriv]
      have := hD x ⟨hx.1.le, hx.2.le⟩
      linarith
  have := hmono ⟨le_rfl, huw⟩ ⟨huw, le_rfl⟩ huw
  simp only [f] at this ⊢
  linarith

/-- Evaluate the Taylor value and directional derivative together. This shares
subexpression values instead of repeatedly evaluating them in a derivative tree. -/
def Ex.alongJet (T : Trig) (H : ℕ → ℚ) (v : ℕ → ℚ) : Ex → TF × TF
  | .c q => (TF.const (Iv.pt q), TF.const (Iv.pt 0))
  | .cs k M => (TF.cosA T H k M,
      TF.mul H (TF.const (Iv.pt (v k))) (TF.sinA T H k M).neg)
  | .sn k M => (TF.sinA T H k M,
      TF.mul H (TF.const (Iv.pt (v k))) (TF.cosA T H k M))
  | .add a b =>
      let x := a.alongJet T H v; let y := b.alongJet T H v
      (x.1.add y.1, x.2.add y.2)
  | .mul a b =>
      let x := a.alongJet T H v; let y := b.alongJet T H v
      (TF.mul H x.1 y.1, (TF.mul H x.2 y.1).add (TF.mul H x.1 y.2))
  | .neg a => let x := a.alongJet T H v; (x.1.neg, x.2.neg)
  | .abs a => ((Ex.abs a).tf T H, TF.const (Iv.pt 0))

theorem Ex.alongJet_eq (T : Trig) (H : ℕ → ℚ) (v : ℕ → ℚ) (e : Ex) :
    e.alongJet T H v = (e.tf T H, (e.alongDeriv v).tf T H) := by
  induction e with
  | c q => rfl
  | cs k M => rfl
  | sn k M => rfl
  | add a b ha hb => simp only [Ex.alongJet, Ex.tf, Ex.alongDeriv, ha, hb]
  | mul a b ha hb => simp only [Ex.alongJet, Ex.tf, Ex.alongDeriv, ha, hb]
  | neg a ha => simp only [Ex.alongJet, Ex.tf, Ex.alongDeriv, ha]
  | abs a ha => rfl

def Ex.alongRange (T : Trig) (H : ℕ → ℚ) (v : ℕ → ℚ) (e : Ex) : Iv :=
  (e.alongJet T H v).2.range H

theorem Ex.alongRange_eq (T : Trig) (H : ℕ → ℚ) (v : ℕ → ℚ) (e : Ex) :
    e.alongRange T H v = ((e.alongDeriv v).tf T H).range H := by
  simp only [Ex.alongRange, Ex.alongJet_eq]

/-- Executable acceptance predicate for one cone-prefix derivative certificate. -/
def Ex.alongNonneg (T : Trig) (H : ℕ → ℚ) (e : Ex) (v : ℕ → ℚ) : Bool :=
  e.smoothAlong v && decide (0 ≤ (e.alongRange T H v).lo)

theorem Ex.along_step_mono {T : Trig} (hT : T.Valid) (H : ℕ → ℚ)
    (e : Ex) (v : ℕ → ℚ) (θ : ℕ → ℝ) {u w : ℝ}
    (hcheck : e.alongNonneg T H v = true) (huw : u ≤ w)
    (hbox : ∀ x ∈ Set.Icc u w, ∀ j, |angleLine θ v x j - T.cen j| ≤ H j) :
    e.real (angleLine θ v u) ≤ e.real (angleLine θ v w) := by
  simp only [Ex.alongNonneg, Ex.alongRange_eq, Bool.and_eq_true, decide_eq_true_eq] at hcheck
  have hh := e.along_step_lb hT H v θ hcheck.1 huw hbox
  have hd : (0 : ℝ) ≤ ((((e.alongDeriv v).tf T H).range H).lo : ℝ) := by
    exact_mod_cast hcheck.2
  have := mul_nonneg (sub_nonneg.mpr huw) hd
  linarith

end Sq19.Milp

namespace Sq19.Endgame
open Sq19.Milp

/-- Clear both positive denominators to compare the same three-row quotient
at the current angles and at the axis-zero angles. -/
def quotientMargin (K : List ℕ) (P Q F : RowE) : Ex :=
  let z := fun j => if j ∈ K then 0 else j
  .add (.mul ((S0E P Q F).subst z) (S1E P Q F))
    (.neg (.mul (S0E P Q F) ((S1E P Q F).subst z)))

theorem quotient_le_of_margin {K : List ℕ} {P Q F : RowE} {θ : ℕ → ℝ}
    (hS : 0 < (S1E P Q F).real θ)
    (hSz : 0 < (S1E P Q F).real (θ ∘ fun j => if j ∈ K then 0 else j))
    (hmargin : 0 ≤ (quotientMargin K P Q F).real θ) :
    -(S0E P Q F).real (θ ∘ fun j => if j ∈ K then 0 else j) /
        (S1E P Q F).real (θ ∘ fun j => if j ∈ K then 0 else j) ≤
      -(S0E P Q F).real θ / (S1E P Q F).real θ := by
  rw [div_le_div_iff₀ hSz hS]
  simp only [quotientMargin, Ex.real, Ex.real_subst] at hmargin
  linarith

/-- Standard three-row assembly once the checker establishes the margin and
an axis-zero endpoint bound. -/
theorem lower_bound_of_margin {K : List ℕ} {P Q F : RowE} {θ : ℕ → ℝ}
    {x y L endpoint : ℝ}
    (hP : P.Holds θ x y L) (hQ : Q.Holds θ x y L) (hF : F.Holds θ x y L)
    (hl1 : 0 ≤ (lam1 P Q F).real θ) (hl2 : 0 ≤ (lam2 P Q F).real θ)
    (hl3 : 0 ≤ (lam3 P Q F).real θ)
    (hS : 0 < (S1E P Q F).real θ)
    (hSz : 0 < (S1E P Q F).real (θ ∘ fun j => if j ∈ K then 0 else j))
    (hmargin : 0 ≤ (quotientMargin K P Q F).real θ)
    (hzero : endpoint ≤ -(S0E P Q F).real (θ ∘ fun j => if j ∈ K then 0 else j) /
      (S1E P Q F).real (θ ∘ fun j => if j ∈ K then 0 else j)) : endpoint ≤ L :=
  hzero.trans ((quotient_le_of_margin hS hSz hmargin).trans
    (combine hP hQ hF hl1 hl2 hl3 hS))

/-- The target side as an expression; index zero must be pinned to zero. -/
def endpointE : Ex := .add (.c 3) (.mul (.c (8/3)) (.cs 0 1))

theorem endpointE_real {θ : ℕ → ℝ} (h0 : θ 0 = 0) :
    endpointE.real θ = 3 + 4 * Real.sqrt 2 / 3 := by
  simp only [endpointE, Ex.real, h0]
  norm_num [Real.cos_pi_div_four]
  <;> ring

/-- Direct endpoint residual, avoiding two copies of the row combination. -/
def endpointMargin (P Q F : RowE) : Ex :=
  .add (.neg (S0E P Q F)) (.neg (.mul endpointE (S1E P Q F)))

theorem lower_bound_of_endpointMargin {P Q F : RowE} {θ : ℕ → ℝ}
    {x y L : ℝ} (h0 : θ 0 = 0)
    (hP : P.Holds θ x y L) (hQ : Q.Holds θ x y L) (hF : F.Holds θ x y L)
    (hl1 : 0 ≤ (lam1 P Q F).real θ) (hl2 : 0 ≤ (lam2 P Q F).real θ)
    (hl3 : 0 ≤ (lam3 P Q F).real θ) (hS : 0 < (S1E P Q F).real θ)
    (hmargin : 0 ≤ (endpointMargin P Q F).real θ) :
    3 + 4 * Real.sqrt 2 / 3 ≤ L := by
  apply le_trans ?_ (combine hP hQ hF hl1 hl2 hl3 hS)
  rw [le_div_iff₀ hS]
  simp only [endpointMargin, Ex.real] at hmargin
  rw [endpointE_real h0] at hmargin
  linarith

end Sq19.Endgame

#print axioms Sq19.Milp.Ex.hasDerivAt_line
#print axioms Sq19.Milp.Ex.along_step_lb
#print axioms Sq19.Milp.Ex.along_step_mono
#print axioms Sq19.Endgame.lower_bound_of_margin
#print axioms Sq19.Endgame.lower_bound_of_endpointMargin
