import S12.DomainSearch

namespace S12
structure CoverRow where
  originalId : Nat
  groups : Finset Nat
  domains : List (List (Finset Nat))

def diagonalBad (m : Nat) : Bool :=
  (m.testBit 8 && m.testBit 10 && !m.testBit 9 && !m.testBit 11) ||
  (m.testBit 9 && m.testBit 11 && !m.testBit 8 && !m.testBit 10)

def keepRow (r : CoverRow) : Bool :=
  !(decide (∃ m ∈ r.groups, diagonalBad m = true)) && feasible r.domains ∅

/-- The geometric bridge remains an explicit requirement: the exact group
cannot realize a diagonal-only square, and its actual auxiliary owners are
contained in the supplied domains. This is not asserted as a packing theorem. -/
def RowConditions (r : CoverRow) : Prop :=
  (∀ m ∈ r.groups, diagonalBad m = false) ∧ Assignment r.domains ∅

theorem row_conditions_survive (r : CoverRow) (h : RowConditions r) :
    keepRow r = true := by
  have hd : ¬ ∃ m ∈ r.groups, diagonalBad m = true := by
    rintro ⟨m, hm, he⟩
    have hf := h.1 m hm
    simp [hf] at he
  simp [keepRow, hd, (feasible_iff _ _).mpr h.2]
end S12
