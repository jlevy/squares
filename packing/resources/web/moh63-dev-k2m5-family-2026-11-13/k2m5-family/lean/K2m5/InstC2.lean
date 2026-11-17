import K2m5.InstFam
/-! Kernel check, in its own module to bound memory. -/
namespace SquarePacking
namespace K2m5Inst
open Fam10
set_option maxRecDepth 1000000 in
theorem boxKeys_eq : boxSegs.map (fun e => keyN (fileIx fam5 11 e)) = boxKeys := by decide +kernel
end K2m5Inst
end SquarePacking
