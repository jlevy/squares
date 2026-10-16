import Sq19Lean.Endgame.ReductionEncodingDefs

/-!
# Arithmetic proof that the finite case encoding is exhaustive

This proof bounds twelve binary digits and recovers them by division and parity.
It does not enumerate 4096 cases and does not invoke a native decision procedure.
Only the encoding definitions are imported; the legacy native-backed
completeness module is not part of this import closure.
-/
namespace Sq19.Endgame.Reduction

private theorem bool_bit {n : ℕ} {b : Bool} (h : n=b.toNat) : (n==1)=b := by
  rw [h]
  cases b <;> rfl

/-- Pure arithmetic replacement for the native-backed finite encoding check. -/
theorem Case.encoding_complete_pure (c : Case) :
    c.toNat < 4096 ∧ Case.ofNat c.toNat = c := by
  rcases c with ⟨pa,qa,o12,o58,b1,b2,b5,b8,b10,large,pd,qd⟩
  have hpa := Bool.toNat_le pa
  have hqa := Bool.toNat_le qa
  have ho12 := Bool.toNat_le o12
  have ho58 := Bool.toNat_le o58
  have hb1 := Bool.toNat_le b1
  have hb2 := Bool.toNat_le b2
  have hb5 := Bool.toNat_le b5
  have hb8 := Bool.toNat_le b8
  have hb10 := Bool.toNat_le b10
  have hl := Bool.toNat_le large
  have hpd := Bool.toNat_le pd
  have hqd := Bool.toNat_le qd
  constructor
  · dsimp only [Case.toNat]
    omega
  · simp only [Case.ofNat,Case.toNat]
    congr 1 <;> apply bool_bit <;> norm_num only [Nat.reducePow] <;> omega

/-- Surjectivity with only the ordinary axioms. -/
theorem Case.ofNat_surjective_pure (c : Case) : ∃ n < 4096, Case.ofNat n=c :=
  ⟨c.toNat,(c.encoding_complete_pure).1,(c.encoding_complete_pure).2⟩

/-- The finite-to-universal bridge does not require a native encoding check. -/
theorem all_cases_of_all_indices_pure
    (h : ∀ n < 4096, checkNat n=true) (c : Case) : check c=true := by
  rcases c.ofNat_surjective_pure with ⟨n,hn,hc⟩
  simpa only [checkNat,hc] using h n hn

end Sq19.Endgame.Reduction

#print axioms Sq19.Endgame.Reduction.Case.encoding_complete_pure
#print axioms Sq19.Endgame.Reduction.all_cases_of_all_indices_pure
