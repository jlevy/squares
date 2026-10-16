import Sq19Lean.Endgame.ReductionCases

/-! The binary case encoding, independent of either completeness proof. -/
namespace Sq19.Endgame.Reduction

def Case.toNat (c : Case) : ℕ :=
  c.pa.toNat + 2*c.qa.toNat + 4*c.owner12.toNat + 8*c.owner58.toNat +
  16*c.b1.toNat + 32*c.b2.toNat + 64*c.b5.toNat + 128*c.b8.toNat +
  256*c.b10.toNat + 512*c.fiveLarger.toNat + 1024*c.pd.toNat + 2048*c.qd.toNat


end Sq19.Endgame.Reduction
