import ElevenSquare.Cover
import ElevenSquare.Combinatorics

namespace ElevenSquare

theorem packing_has_canonical_mask {S : ℝ} (P : Packing 11 S) (hS : S ≤ coverCap) :
    ∃ m ∈ canonicalMasks, Occupies P m ∨ Occupies P (halfTurnMask m) := by
  obtain ⟨m, hm, hocc⟩ := packing_occupies_eleven_cells P hS
  rcases mask_or_halfTurn_canonical m hm with h | h
  · exact ⟨m, h, Or.inl hocc⟩
  · exact ⟨halfTurnMask m, h, Or.inr (by simpa only [halfTurnMask_twice] using hocc)⟩

end ElevenSquare
