import Sq19Lean.Endgame.ReductionCases

/-! Logical assembly of blocks. This module evaluates no numerical checker. -/
namespace Sq19.Endgame.Reduction

/-- Division/remainder dispatch covers every index exactly, without evaluating P. -/
theorem indices_of_blocks {P : ℕ → Prop} (width count : ℕ) (hw : 0 < width)
    (blocks : ∀ b < count, ∀ r < width, P (width * b + r)) :
    ∀ n < width * count, P n := by
  intro n hn
  have hq : n / width < count :=
    (Nat.div_lt_iff_lt_mul hw).2 (by simpa only [Nat.mul_comm] using hn)
  have hr : n % width < width := Nat.mod_lt n hw
  have he : width * (n / width) + n % width = n := by
    simpa only [Nat.add_comm] using Nat.mod_add_div n width
  simpa only [he] using blocks (n / width) hq (n % width) hr

end Sq19.Endgame.Reduction
#print axioms Sq19.Endgame.Reduction.indices_of_blocks
