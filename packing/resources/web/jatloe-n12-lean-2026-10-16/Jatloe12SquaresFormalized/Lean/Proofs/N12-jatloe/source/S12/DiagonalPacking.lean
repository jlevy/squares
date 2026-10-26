import S12.FamilyTransport

namespace S12
open S12Pilot

theorem diagonal_not_realized (q : OpenSquare) (m : Nat)
    (hm : ExactMarkers q (maskSupport m)) : diagonalBad m=false := by
  have hr : Realizes q ⟨m.testBit 8,m.testBit 9,m.testBit 10,m.testBit 11⟩ := by
    have h8 := hm 8
    have h9 := hm 9
    have h10 := hm 10
    have h11 := hm 11
    norm_num [Owns,marker,maskSupport] at h8 h9 h10 h11
    exact ⟨h8,h9,h10,h11⟩
  cases h : diagonalBad m with
  | false => rfl
  | true =>
    exact False.elim (rejects_sound ⟨m.testBit 8,m.testBit 9,m.testBit 10,m.testBit 11⟩ h ⟨q,hr⟩)

theorem packing_no_diagonal (p : NormalizedPacking) (m : Nat)
    (hm : m∈codedMarkerFamily p) : diagonalBad m=false := by
  obtain ⟨i,_,rfl⟩ := Finset.mem_image.mp hm
  exact diagonal_not_realized _ _ (coded_exact p i)

#print axioms packing_no_diagonal
end S12
