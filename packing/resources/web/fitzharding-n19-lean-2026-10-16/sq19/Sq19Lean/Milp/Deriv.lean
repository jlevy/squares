import Sq19Lean.Milp.Expr

/-!
# Derivatives of angle expressions and a one-step monotonicity bound

`Ex.deriv k e` is the symbolic derivative of `e` in the angle `θ_k`. `Ex.hasDerivAt` proves it is the
derivative along that coordinate. `Ex.step_lb`: moving `θ_k` from `u` to `v ≥ u` inside a box changes
`e` by at least `(v - u) * inf deriv`, where the infimum is the lower end of the derivative's Taylor
range on the box (`TF.mem_range`). Applied one coordinate at a time this gives `f(g) - f(0)` with a
remainder proportional to `|g|`, which the monotone step of the local theorem needs.
-/
namespace Sq19.Milp

/-- Does `e` depend on the angle `θ_k`? -/
def Ex.mentions (k : ℕ) : Ex → Bool
  | .c _ => false
  | .cs s _ => s = k
  | .sn s _ => s = k
  | .add a b => a.mentions k || b.mentions k
  | .mul a b => a.mentions k || b.mentions k
  | .neg a => a.mentions k
  | .abs a => a.mentions k

/-- No absolute value in `e` depends on `θ_k` (so `e` is differentiable in `θ_k`). -/
def Ex.absFree (k : ℕ) : Ex → Bool
  | .c _ => true
  | .cs _ _ => true
  | .sn _ _ => true
  | .add a b => a.absFree k && b.absFree k
  | .mul a b => a.absFree k && b.absFree k
  | .neg a => a.absFree k
  | .abs a => !a.mentions k

theorem Ex.real_update_of_not_mentions (k : ℕ) (θ : ℕ → ℝ) (x : ℝ) (e : Ex) (h : e.mentions k = false) :
    e.real (Function.update θ k x) = e.real θ := by
  induction e with
  | c q => rfl
  | cs s M =>
    simp only [Ex.mentions, decide_eq_false_iff_not] at h
    simp only [Ex.real, Function.update_of_ne h]
  | sn s M =>
    simp only [Ex.mentions, decide_eq_false_iff_not] at h
    simp only [Ex.real, Function.update_of_ne h]
  | add a b ha hb =>
    simp only [Ex.mentions, Bool.or_eq_false_iff] at h
    simp only [Ex.real, ha h.1, hb h.2]
  | mul a b ha hb =>
    simp only [Ex.mentions, Bool.or_eq_false_iff] at h
    simp only [Ex.real, ha h.1, hb h.2]
  | neg a ha => simp only [Ex.mentions] at h; simp only [Ex.real, ha h]
  | abs a ha => simp only [Ex.mentions] at h; simp only [Ex.real, ha h]

/-- Derivative in `θ_k`. -/
def Ex.deriv (k : ℕ) : Ex → Ex
  | .c _ => .c 0
  | .cs s M => if s = k then .neg (.sn s M) else .c 0
  | .sn s M => if s = k then .cs s M else .c 0
  | .add a b => .add (a.deriv k) (b.deriv k)
  | .mul a b => .add (.mul (a.deriv k) b) (.mul a (b.deriv k))
  | .neg a => .neg (a.deriv k)
  | .abs _ => .c 0

theorem Ex.hasDerivAt (k : ℕ) (θ : ℕ → ℝ) (e : Ex) (t : ℝ) (hf : e.absFree k = true) :
    HasDerivAt (fun x => e.real (Function.update θ k x)) ((e.deriv k).real (Function.update θ k t)) t := by
  induction e with
  | c q => simp only [Ex.real, Ex.deriv]; simpa using hasDerivAt_const t (q : ℝ)
  | cs s M =>
    simp only [Ex.real, Ex.deriv]
    by_cases h : s = k
    · subst h
      simp only [if_true, Ex.real, Function.update_self]
      have := ((hasDerivAt_id t).const_add ((M:ℝ) * Real.pi / 4)).cos
      simpa using this
    · simp only [h, if_false, Ex.real, Function.update_of_ne h]
      simpa using hasDerivAt_const t (Real.cos (M * Real.pi / 4 + θ s))
  | sn s M =>
    simp only [Ex.real, Ex.deriv]
    by_cases h : s = k
    · subst h
      simp only [if_true, Ex.real, Function.update_self]
      have := ((hasDerivAt_id t).const_add ((M:ℝ) * Real.pi / 4)).sin
      simpa using this
    · simp only [h, if_false, Ex.real, Function.update_of_ne h]
      simpa using hasDerivAt_const t (Real.sin (M * Real.pi / 4 + θ s))
  | add a b ha hb =>
    simp only [Ex.absFree, Bool.and_eq_true] at hf
    simp only [Ex.real, Ex.deriv]; exact (ha hf.1).add (hb hf.2)
  | mul a b ha hb =>
    simp only [Ex.absFree, Bool.and_eq_true] at hf
    simp only [Ex.real, Ex.deriv]; exact (ha hf.1).mul (hb hf.2)
  | neg a ha => simp only [Ex.absFree] at hf; simp only [Ex.real, Ex.deriv]; exact (ha hf).neg
  | abs a _ =>
    simp only [Ex.absFree, Bool.not_eq_true'] at hf
    have : (fun x => |a.real (Function.update θ k x)|) = fun _ => |a.real θ| := by
      funext x; rw [Ex.real_update_of_not_mentions k θ x a hf]
    simp only [Ex.real, Ex.deriv]
    rw [this]; simpa using hasDerivAt_const t (|a.real θ|)

/-- **One step.** If every point of the segment `θ_k ∈ [u, v]` (other angles fixed) lies in the
Taylor box `(T, H)`, then `e(v) - e(u) ≥ (v - u) * D` for `D` the lower end of the derivative's range. -/
theorem Ex.step_lb {T : Trig} (hT : T.Valid) (H : ℕ → ℚ) (e : Ex) (k : ℕ) (θ : ℕ → ℝ) {u v : ℝ}
    (hf : e.absFree k = true) (huv : u ≤ v)
    (hbox : ∀ x ∈ Set.Icc u v, ∀ j, |Function.update θ k x j - T.cen j| ≤ H j) :
    (v - u) * ((((e.deriv k).tf T H).range H).lo : ℝ) ≤
      e.real (Function.update θ k v) - e.real (Function.update θ k u) := by
  set f := fun x => e.real (Function.update θ k x)
  set D : ℝ := ((((e.deriv k).tf T H).range H).lo : ℝ)
  have hd : ∀ x, HasDerivAt f ((e.deriv k).real (Function.update θ k x)) x := fun x => Ex.hasDerivAt k θ e x hf
  have hD : ∀ x ∈ Set.Icc u v, D ≤ (e.deriv k).real (Function.update θ k x) := by
    intro x hx
    have hm := TF.mem_range (Ex.tf_encl hT H (e.deriv k)) (fun j => Function.update θ k x j - T.cen j)
      (hbox x hx)
    have e' : (fun s => (T.cen s : ℝ) + (Function.update θ k x s - T.cen s)) = Function.update θ k x := by
      funext s; ring
    rw [e'] at hm
    exact hm.1
  -- f - D x is monotone on [u, v]
  have hdx : ∀ x, HasDerivAt (fun x => f x - D * x) ((e.deriv k).real (Function.update θ k x) - D) x := by
    intro x
    have h2 : HasDerivAt (fun x : ℝ => D * x) D x := by simpa using (hasDerivAt_id x).const_mul D
    exact (hd x).sub h2
  have hmono : MonotoneOn (fun x => f x - D * x) (Set.Icc u v) := by
    apply monotoneOn_of_deriv_nonneg (convex_Icc u v)
    · exact HasDerivAt.continuousOn (fun x _ => hdx x)
    · intro x _
      exact (hdx x).differentiableAt.differentiableWithinAt
    · intro x hx
      rw [interior_Icc] at hx
      rw [(hdx x).deriv]
      have := hD x ⟨hx.1.le, hx.2.le⟩
      linarith
  have := hmono ⟨le_rfl, huv⟩ ⟨huv, le_rfl⟩ huv
  simp only [f] at this ⊢
  linarith

/-- Rename angle indices. -/
def Ex.subst (f : ℕ → ℕ) : Ex → Ex
  | .c q => .c q
  | .cs s M => .cs (f s) M
  | .sn s M => .sn (f s) M
  | .add a b => .add (a.subst f) (b.subst f)
  | .mul a b => .mul (a.subst f) (b.subst f)
  | .neg a => .neg (a.subst f)
  | .abs a => .abs (a.subst f)

theorem Ex.real_subst (f : ℕ → ℕ) (θ : ℕ → ℝ) (e : Ex) : (e.subst f).real θ = e.real (θ ∘ f) := by
  induction e with
  | c q => rfl
  | cs s M => rfl
  | sn s M => rfl
  | add a b ha hb => simp only [Ex.subst, Ex.real, ha, hb]
  | mul a b ha hb => simp only [Ex.subst, Ex.real, ha, hb]
  | neg a ha => simp only [Ex.subst, Ex.real, ha]
  | abs a ha => simp only [Ex.subst, Ex.real, ha]

end Sq19.Milp

#print axioms Sq19.Milp.Ex.hasDerivAt
#print axioms Sq19.Milp.Ex.step_lb
