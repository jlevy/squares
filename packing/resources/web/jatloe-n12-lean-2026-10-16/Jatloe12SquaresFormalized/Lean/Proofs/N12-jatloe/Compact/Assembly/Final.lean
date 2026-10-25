import Compact.Assembly.SourceAssembly

/-! Unconditional source assembly for the original twelve-square optimum.
All 117 retained original cases are supplied by proof terms. The original
normalization and classification give the lower bound, and the original
grid construction attains 4. No pending geometric hypothesis is exposed.

The finite classification retains its inherited native-compiler trust.
The verification driver checks the final theorem's type and approved axioms. -/
namespace N12Compact.Final
set_option Elab.async false

/-- The original unrestricted packing constant, assembled without premises. -/
theorem optimality : S12.packingConstant12 = 4 :=
  SourceAssembly.optimality SourceAssembly.pending_closed

#print axioms optimality
end N12Compact.Final
