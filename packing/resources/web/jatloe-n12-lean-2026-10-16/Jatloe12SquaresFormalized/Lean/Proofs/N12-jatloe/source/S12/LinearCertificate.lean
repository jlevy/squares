import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Pi
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace S12
open scoped BigOperators

structure Affine (n : Nat) where
  coeff : Fin n → ℚ
  constant : ℚ
  deriving DecidableEq

def Affine.eval {n : Nat} (f : Affine n) (x : Fin n → ℝ) : ℝ :=
  (∑ i, (f.coeff i : ℝ)*x i) + f.constant

def Affine.zero (n : Nat) : Affine n := ⟨fun _ => 0,0⟩
def Affine.add {n : Nat} (f g : Affine n) : Affine n :=
  ⟨fun i => f.coeff i+g.coeff i,f.constant+g.constant⟩
def Affine.scale {n : Nat} (a : ℚ) (f : Affine n) : Affine n :=
  ⟨fun i => a*f.coeff i,a*f.constant⟩

@[simp] theorem Affine.eval_zero {n : Nat} (x : Fin n → ℝ) :
    (Affine.zero n).eval x = 0 := by simp [Affine.eval,Affine.zero]

@[simp] theorem Affine.eval_add {n : Nat} (f g : Affine n) (x : Fin n → ℝ) :
    (f.add g).eval x = f.eval x+g.eval x := by
  simp [Affine.eval,Affine.add,add_mul,Finset.sum_add_distrib]
  ring

@[simp] theorem Affine.eval_scale {n : Nat} (a : ℚ) (f : Affine n) (x : Fin n → ℝ) :
    (f.scale a).eval x = (a : ℝ)*f.eval x := by
  simp [Affine.eval,Affine.scale,mul_add,Finset.mul_sum,mul_assoc]

structure LinearConstraint (n : Nat) where
  form : Affine n
  strict : Bool
  deriving DecidableEq

def LinearConstraint.Holds {n : Nat} (r : LinearConstraint n) (x : Fin n → ℝ) : Prop :=
  if r.strict then 0 < r.form.eval x else 0 ≤ r.form.eval x

def LinearConstraint.zero (n : Nat) : LinearConstraint n := ⟨Affine.zero n,false⟩
def LinearConstraint.add {n : Nat} (r s : LinearConstraint n) : LinearConstraint n :=
  ⟨r.form.add s.form,r.strict || s.strict⟩
def LinearConstraint.scale {n : Nat} (a : ℚ) (r : LinearConstraint n) : LinearConstraint n :=
  ⟨r.form.scale a,decide (0<a) && r.strict⟩

theorem LinearConstraint.holds_add {n : Nat} (r s : LinearConstraint n) (x : Fin n → ℝ)
    (hr : r.Holds x) (hs : s.Holds x) : (r.add s).Holds x := by
  rcases r with ⟨r,b⟩
  rcases s with ⟨s,c⟩
  cases b <;> cases c <;>
    simp_all [LinearConstraint.Holds,LinearConstraint.add] <;> linarith

theorem LinearConstraint.holds_scale {n : Nat} (a : ℚ) (r : LinearConstraint n)
    (x : Fin n → ℝ) (ha : 0 ≤ a) (hr : r.Holds x) : (r.scale a).Holds x := by
  have ha' : (0 : ℝ) ≤ a := by exact_mod_cast ha
  rcases r with ⟨r,b⟩
  by_cases hp : 0<a
  · have hp' : (0 : ℝ) < a := by exact_mod_cast hp
    cases b <;> simp_all [LinearConstraint.Holds,LinearConstraint.scale]
  · have hz : a=0 := by linarith
    subst a
    simp [LinearConstraint.Holds,LinearConstraint.scale,Affine.eval_scale]

def linearCombination {n : Nat} : List (ℚ × LinearConstraint n) → LinearConstraint n
  | [] => LinearConstraint.zero n
  | (a,r)::terms => (r.scale a).add (linearCombination terms)

def LinearCertificateCheck {n : Nat} (inputs : List (LinearConstraint n))
    (terms : List (ℚ × LinearConstraint n)) : Prop :=
  (∀ t ∈ terms, 0 ≤ t.1 ∧ t.2 ∈ inputs) ∧
  (linearCombination terms).strict = true ∧
  (linearCombination terms).form = Affine.zero n
instance {n : Nat} (inputs : List (LinearConstraint n)) (terms : List (ℚ × LinearConstraint n)) :
    Decidable (LinearCertificateCheck inputs terms) := inferInstanceAs (Decidable (_ ∧ _))

theorem linearCombination_holds {n : Nat} (terms : List (ℚ × LinearConstraint n))
    (x : Fin n → ℝ) (h : ∀ t ∈ terms, 0 ≤ t.1 ∧ t.2.Holds x) :
    (linearCombination terms).Holds x := by
  induction terms with
  | nil => simp [linearCombination,LinearConstraint.zero,LinearConstraint.Holds]
  | cons t terms ih =>
    obtain ⟨ha,hr⟩ := h t (by simp)
    apply LinearConstraint.holds_add
    · exact LinearConstraint.holds_scale t.1 t.2 x ha hr
    · apply ih
      intro t ht; exact h t (by simp [ht])

/-- Soundness of exact rational linear-infeasibility certificates. The external
solver need only supply nonnegative weights; every arithmetic identity is
checked, and this theorem connects acceptance to real infeasibility. -/
theorem linear_certificate_sound {n : Nat} (inputs : List (LinearConstraint n))
    (terms : List (ℚ × LinearConstraint n)) (hc : LinearCertificateCheck inputs terms) :
    ¬ ∃ x : Fin n → ℝ, ∀ r ∈ inputs, r.Holds x := by
  rintro ⟨x,hx⟩
  have hh := linearCombination_holds terms x (by
    intro t ht
    obtain ⟨ha,hr⟩ := hc.1 t ht
    exact ⟨ha,hx t.2 hr⟩)
  unfold LinearConstraint.Holds at hh
  rw [hc.2.1,hc.2.2] at hh
  simp at hh

#print axioms linear_certificate_sound
end S12
