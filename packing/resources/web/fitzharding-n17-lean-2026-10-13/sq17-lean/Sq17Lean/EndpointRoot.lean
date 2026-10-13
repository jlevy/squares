import Sq17Lean.EndpointRootData
import Sq17Lean.PolynomialNewtonRoot

/-! Existence and uniqueness of the exact two-variable endpoint root in the
closed box specified by root_chart_data.json. This theorem does not assert
packing feasibility or global uniqueness outside that box. -/
namespace Sq17.EndpointRoot
open Sq17.PolynomialBox

theorem unique_root : ∃! z : ℝ × ℝ,
    z ∈ rootBox ((midpoint.1:ℝ),(midpoint.2:ℝ)) radius ∧
      eval polynomial0 z=0 ∧ eval polynomial1 z=0 :=
  newton_unique_root polynomial0 polynomial1 newton0 newton1
    ((midpoint.1:ℝ),(midpoint.2:ℝ)) radius c00 c01 c10 c11
    radius_pos inverse_nonsingular contraction_checked newton0_identity newton1_identity

noncomputable def coordinates : ℝ × ℝ := Classical.choose unique_root

theorem coordinates_spec :
    coordinates ∈ rootBox ((midpoint.1:ℝ),(midpoint.2:ℝ)) radius ∧
      eval polynomial0 coordinates=0 ∧ eval polynomial1 coordinates=0 :=
  (Classical.choose_spec unique_root).1

theorem coordinates_unique (z : ℝ × ℝ)
    (hz : z ∈ rootBox ((midpoint.1:ℝ),(midpoint.2:ℝ)) radius)
    (h0 : eval polynomial0 z=0) (h1 : eval polynomial1 z=0) : z = coordinates :=
  (Classical.choose_spec unique_root).2 z ⟨hz,h0,h1⟩

end Sq17.EndpointRoot
#print axioms Sq17.EndpointRoot.unique_root
#print axioms Sq17.EndpointRoot.coordinates_spec
#print axioms Sq17.EndpointRoot.coordinates_unique
