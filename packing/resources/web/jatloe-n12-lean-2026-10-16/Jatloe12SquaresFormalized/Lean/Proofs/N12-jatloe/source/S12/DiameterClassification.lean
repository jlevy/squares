import S12.Diameter
import S12.MarkerClassification

/-! Original bridge from geometric ownership to the finite marker table. -/
namespace S12
open S12Pilot

theorem actual_group_in_table (q : OpenSquare) (hsize : q.side ≤ 1001/1000)
    (g : Finset Marker) (hne : g.Nonempty)
    (howned : ∀ i ∈ g, Owns q i) : g ∈ groupTable := by
  apply diameter_group_in_table
  refine ⟨hne, ?_⟩
  intro i hi j hj
  have hd := normalized_diameter_bound q hsize _ _ _ _ (howned i hi) (howned j hj)
  unfold distSq diameterLimit
  apply (Rat.cast_lt (K := ℝ)).mp
  simp only [pow_two] at hd ⊢
  push_cast
  exact hd

#print axioms actual_group_in_table
end S12
