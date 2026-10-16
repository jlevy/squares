import Sq19Lean.Survivors.O1.Tree
import Sq19Lean.Survivors.O2.Tree
import Sq19Lean.Survivors.O5423.Tree
import Sq19Lean.Survivors.O5453.Tree

/-! The four survivor exclusions in the census frame.
This module is accepted only after all replay, split-cover, table and seed checks
in its dependencies have built. The C search verdicts alone do not establish it. -/
namespace Sq19.Survivors

theorem orbit1_free : ¬ Census.Packs O1.roster := O1.free
theorem orbit2_free : ¬ Census.Packs O2.roster := O2.free
theorem orbit5423_free : ¬ Census.Packs O5423.roster := O5423.free
theorem orbit5453_free : ¬ Census.Packs O5453.roster := O5453.free

end Sq19.Survivors
#print axioms Sq19.Survivors.orbit1_free
#print axioms Sq19.Survivors.orbit2_free
#print axioms Sq19.Survivors.orbit5423_free
#print axioms Sq19.Survivors.orbit5453_free
