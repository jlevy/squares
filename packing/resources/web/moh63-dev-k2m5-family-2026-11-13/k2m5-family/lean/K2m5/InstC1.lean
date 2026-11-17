import K2m5.InstFam
/-! Kernel check, in its own module to bound memory. -/
namespace SquarePacking
namespace K2m5Inst
open Fam10
set_option maxRecDepth 1000000 in
theorem boxSegs_ok : boxSegs.all (segOK fam5 11) = true := by decide +kernel
end K2m5Inst
end SquarePacking
