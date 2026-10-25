import Compact.Assembly.SourceAssembly

/-! Compatibility interface for the continuous case assembly. All original
cases, including C700, now have complete source terms. The historical
Pending interface is retained and is discharged by pending_closed below.
All changed source still awaits Lean replay. -/
namespace N12Compact.ContinuousRemaining

open S12 S12Pilot S12Completion
set_option Elab.async false

/-- The original C977 contract is supplied, without a pending cap field. -/
theorem case977_excludes : ExcludesCase 977 := C977CenterClosure.excludes

/-- C981/C1092's legacy fields are supplied by default; their complete
original-case source is already registered. The other contracts are unchanged. -/
structure Pending : Prop where
  other_cases : ∀ id∈(SourceAssembly.pendingIds.erase 981).erase 1092,
    ExcludesCase id
  case981 : C981Compact.Pending := C981Compact.pending_closed
  case1092 : C1092Compact.Pending := C1092Compact.pending_closed

/-- Only proofs of the displayed remaining endings can fill the
original global assembly. The reduction adds no geometric premise. -/
theorem to_source (work : Pending) : SourceAssembly.Pending :=
  ⟨work.other_cases,work.case981,work.case1092⟩

theorem pending_closed : Pending :=
  { other_cases := SourceAssembly.pending_closed.other_cases }

theorem optimality (work : Pending) : packingConstant12=4 :=
  SourceAssembly.optimality (to_source work)

#print axioms case977_excludes
#print axioms to_source
#print axioms optimality
end N12Compact.ContinuousRemaining
