import Sq19Lean.Milp.Deriv
import Sq19Lean.Endgame.Rows

/-!
# Building blocks of Phi as angle expressions

Angles of squares are `M π/4 + θ_s` (`Ex.cs s M`, `Ex.sn s M`). The rows use cosines and sines of
differences of two such angles and supports `supp φ ψ`; here they are expressions, and on a box where
the signs of `cos (ψ - φ)` and `sin (ψ - φ)` are fixed the support is the signed expression `suppE`.
-/
namespace Sq19.Endgame
open Sq19.Milp

/-- The angle `M π/4 + θ_s`. -/
noncomputable def angE (θ : ℕ → ℝ) (s M : ℕ) : ℝ := M * Real.pi / 4 + θ s

/-- `cos (A - B)` and `sin (A - B)` for `A = M π/4 + θ_s`, `B = M' π/4 + θ_t`. -/
def cosD (s M t M' : ℕ) : Ex := .add (.mul (.cs s M) (.cs t M')) (.mul (.sn s M) (.sn t M'))
def sinD (s M t M' : ℕ) : Ex := .add (.mul (.sn s M) (.cs t M')) (.neg (.mul (.cs s M) (.sn t M')))

theorem cosD_real (θ : ℕ → ℝ) (s M t M' : ℕ) :
    (cosD s M t M').real θ = Real.cos (angE θ s M - angE θ t M') := by
  simp only [cosD, Ex.real, angE, Real.cos_sub]

theorem sinD_real (θ : ℕ → ℝ) (s M t M' : ℕ) :
    (sinD s M t M').real θ = Real.sin (angE θ s M - angE θ t M') := by
  simp only [sinD, Ex.real, angE, Real.sin_sub]; ring

/-- Signed support: `(σc cos (A - B) + σs sin (A - B)) / 2` with `σ ∈ {1, -1}`. -/
def suppE (σc σs : ℚ) (s M t M' : ℕ) : Ex :=
  .mul (.c (1/2)) (.add (.mul (.c σc) (cosD s M t M')) (.mul (.c σs) (sinD s M t M')))

/-- Where the signs are as given, the signed support is the support. -/
theorem suppE_real {θ : ℕ → ℝ} {σc σs : ℚ} {s M t M' : ℕ}
    (hc : σc = 1 ∨ σc = -1) (hs : σs = 1 ∨ σs = -1)
    (hcs : 0 ≤ σc * Real.cos (angE θ s M - angE θ t M'))
    (hss : 0 ≤ σs * Real.sin (angE θ s M - angE θ t M')) :
    (suppE σc σs s M t M').real θ = supp (angE θ t M') (angE θ s M) := by
  simp only [suppE, Ex.real, cosD_real, sinD_real, supp]
  have ac : |Real.cos (angE θ s M - angE θ t M')| = σc * Real.cos (angE θ s M - angE θ t M') := by
    rcases hc with rfl | rfl <;> simp at hcs ⊢ <;> exact hcs
  have as : |Real.sin (angE θ s M - angE θ t M')| = σs * Real.sin (angE θ s M - angE θ t M') := by
    rcases hs with rfl | rfl <;> simp at hss ⊢ <;> exact hss
  rw [ac, as]; push_cast; ring

/-- Exact support, including across a change of sign of the relative angle. -/
def suppAbsE (s M t M' : ℕ) : Ex :=
  .mul (.c (1/2)) (.add (.abs (cosD s M t M')) (.abs (sinD s M t M')))

theorem suppAbsE_real (θ : ℕ → ℝ) (s M t M' : ℕ) :
    (suppAbsE s M t M').real θ = supp (angE θ t M') (angE θ s M) := by
  simp only [suppAbsE, Ex.real, cosD_real, sinD_real, supp]
  push_cast
  ring

/-- Exact tilted-to-tilted supports remain differentiable in every other angle.
In particular the endgame may differentiate in the six axis angles without splitting
on the relative signs of the three tilted angles. -/
theorem suppAbsE_absFree (s M t M' k : ℕ) (hs : s ≠ k) (ht : t ≠ k) :
    (suppAbsE s M t M').absFree k = true := by
  simp [suppAbsE, Ex.absFree, Ex.mentions, cosD, sinD, hs, ht]

/-- The constant half-width is a valid support lower bound for every pair of angles. -/
theorem half_support_lb (θ : ℕ → ℝ) (s M t M' : ℕ) :
    (Ex.c (1/2)).real θ ≤ supp (angE θ t M') (angE θ s M) := by
  simpa [Ex.real] using supp_ge_half (angE θ t M') (angE θ s M)

end Sq19.Endgame

#print axioms Sq19.Endgame.suppE_real

#print axioms Sq19.Endgame.suppAbsE_real
#print axioms Sq19.Endgame.suppAbsE_absFree
#print axioms Sq19.Endgame.half_support_lb
