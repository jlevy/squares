import Sq19Lean.Endgame.ReductionBase
import Sq19Lean.Endgame.ReductionRows

/-! Conditional assembly of the full local hull theorem. The only unproved
input is acceptance of the finite family of executable checks. -/
namespace Sq19.Endgame.Reduction
open Sq19.Milp

theorem side19_le_of_matching_check {c : Case} {θ dx dy : ℕ → ℝ} {L : ℝ}
    (hg : Good Hull.prob θ dx dy L) (hm : c.Matches θ dx dy)
    (hc : check c = true) : side19 ≤ L := by
  simp only [check, Bool.and_eq_true] at hc
  obtain ⟨hgeometry, hslope⟩ := hc
  obtain ⟨hp, hq, hf⟩ := hm.rows hg
  obtain ⟨hl1, hl2, hl3, hS⟩ := geometry_sound c hgeometry hg.ang
  have hbase := c.base_margin_nonneg hgeometry hg.ang (theta0 hg)
  have hmove := margin_axisZero_le c hslope hg.ang
    hm.sign1 hm.sign2 hm.sign5 hm.sign8 hm.sign10 hm.order58
  exact lower_bound_of_endpointMargin (theta0 hg) hp hq hf hl1 hl2 hl3 hS
    (hbase.trans hmove)

/-- Every actual hull packing is covered by the executable finite checker.
This remains conditional until all cases, or their proved equivalents, pass. -/
theorem side19_le_of_hull_of_all_checks
    (checks : ∀ c : Case, check c = true)
    {θ dx dy : ℕ → ℝ} {L : ℝ} (hg : Good Hull.prob θ dx dy L) : side19 ≤ L := by
  obtain ⟨c, hm⟩ := exists_matching_case hg
  exact side19_le_of_matching_check hg hm (checks c)

end Sq19.Endgame.Reduction

#print axioms Sq19.Endgame.Reduction.side19_le_of_matching_check
#print axioms Sq19.Endgame.Reduction.side19_le_of_hull_of_all_checks
