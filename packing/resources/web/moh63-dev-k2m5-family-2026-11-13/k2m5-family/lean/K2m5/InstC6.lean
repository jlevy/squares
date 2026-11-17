import K2m5.InstFam
/-! Kernel check, in its own module to bound memory. -/
namespace SquarePacking
namespace K2m5Inst
open Fam10
set_option maxRecDepth 1000000 in
theorem gkPart_true : gkPart true = boxGridKeys.drop 6622 := by decide +kernel
end K2m5Inst
end SquarePacking
