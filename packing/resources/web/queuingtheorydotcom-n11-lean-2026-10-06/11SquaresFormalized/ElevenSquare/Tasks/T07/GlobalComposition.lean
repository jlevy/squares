import ElevenSquare.Tasks.T07.D4Transport
import ElevenSquare.Tasks.T07.LocalRigidity

/-! The remaining global certificate can be stated without weakening the public
optimality theorem. `case438_near_certificate` is the exact capture and geometry
obligation: the output retains the original centered side and represents every
physical square in the focused local chart. -/
namespace ElevenSquare.Tasks.T07
open ElevenSquare.Pending
noncomputable section

def Case438NearCertificate : Prop :=
  ∀ (S : ℝ) (Q : Packing 11 coverCap),
    S ≤ T →
    Occupies Q (caseMask ⟨438, by omega⟩) →
    CenteredPacking Q S →
    ∃ R : Packing 11 T, CenteredPacking R S ∧
      ∃ h : Displacement, InRectangle focusedRadii h ∧
        ∀ i,
          (R.squares i).center = perturbedCenter constructionSquare h i ∧
          (R.squares i).axis = perturbedAxis constructionSquare h i

theorem global_lower_bound_of_case438_certificate
    (hcertificate : Case438NearCertificate)
    {S : ℝ} (P : Packing 11 S) : T ≤ S := by
  by_contra h
  have hST : S ≤ T := le_of_lt (lt_of_not_ge h)
  obtain ⟨Q, hocc, hsmall⟩ := case438_centered_reduction P hST
  obtain ⟨R, hRsmall, hpose, hrect, hrepresentation⟩ :=
    hcertificate S Q hST hocc hsmall
  exact h (focused_centered_requires_T R hRsmall hpose hrect hrepresentation)

end
end ElevenSquare.Tasks.T07
