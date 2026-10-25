import Compact.Assembly.SymbolicRegistry
import Compact.Preservation.Complete.All
import Compact.Cases.C898.CompleteCached
import Compact.Cases.C981Compact
import Compact.Cases.C1092Compact
import Compact.Assembly.NewCases

/-! Complete source-level assembly of the recovered work.

The seven compact historical replacements supply actual original case
exclusions, alongside the 79 symbolic source entries. They are not assumed
from archive receipts. Their entire source closure still awaits the final
ordinary Lean replay, as do the new symbolic proofs.

All 117 original case contracts are registered in source. The historical
conditional API remains available; pending_closed supplies its empty work.
C580/C581 now
compose their genuine original entrances with the complete shared
three-square ending. This is source composition, not a fresh replay.
C1090 supplies its complete actual-family entrance from existing local
certificates, its true merged-left seed and the new wall chord reduction.
C977 is supplied
by its complete original-case continuous source ending. C981 now supplies
all 117 representative contracts together with the original exhaustive
domain and whole-packing symmetry cover. Its legacy empty field is supplied
by default below. The entire new assembly still requires acceptance;
C974/C976 now join their actual owner domains to the continuous endings,
and C1089 exhausts all eight actual wall-center sectors. C1091 supplies
all four closed right/top sectors through its reconstructed actual entrances.
C1092 supplies all four actual whole-packing branches, including the complete
inward reduction and Ordinary sign-state cycle in its windmill branch.
C983 joins the actual singleton corner and stronger seeds to both northeast
sharp-point alternatives, one southeast profile and the two true midpoints.
C975 supplies its genuine merged-top origin and corner reductions, then
exhausts both northeast alternatives and all canonical signs.
C896 supplies genuine merged-bottom and northwest centers, forcing their
actual owners to overlap without assigning a G budget to the exempt merge.
C683/C867/C868 close both upper canonical signs and both southeast branches.
Their surviving negative upper faces produce a closed vertex or edge point
strictly inside the actual top square, throughout its entire orientation range.
C972 supplies its original NE origin, positive SE and NE signs, and the
two-square exclusion through all directed support axes and relative orders.
C700 uses the same three-square missing-corner ending twice: the actual bottom
and left singletons both strictly contain (1,1), contradicting disjointness.
No partial wall,
angle or point result is counted as a completed case.
-/
namespace N12Compact.SourceAssembly
open S12 S12Completion Remaining117
set_option Elab.async false
set_option maxRecDepth 10000

def historicalRegistry : List ProvenCase := [
  ⟨701, Preservation.Complete.C701.excludes_case⟩,
  ⟨713, Preservation.Complete.C713.excludes_case⟩,
  ⟨717, Preservation.Complete.C717.excludes_case⟩,
  ⟨898, C898.excludes_case⟩,
  ⟨973, Preservation.Complete.C973.excludes_case⟩,
  ⟨978, Preservation.Complete.C978.excludes_case⟩,
  ⟨979, Preservation.Complete.C979.excludes_case⟩
]

def registry : List ProvenCase :=
  SymbolicRegistry.registry ++ historicalRegistry ++ NewCases.registry

def historicalIds : Finset Nat := {701,713,717,898,973,978,979}

def sourceIds : Finset Nat :=
  SymbolicRegistry.provenIds ∪ historicalIds ∪ NewCases.provenIds

def pendingIds : Finset Nat :=
  (SymbolicRegistry.pendingIds \ historicalIds) \ NewCases.provenIds

theorem registry_ids : registry.map ProvenCase.id =
    SymbolicRegistry.registry.map ProvenCase.id ++ [701,713,717,898,973,978,979] ++
      NewCases.ids := by
  rw [registry, List.map_append, List.map_append]
  rfl

theorem known_ids_exact : knownIds registry = sourceIds := by
  unfold knownIds
  rw [registry_ids, SymbolicRegistry.registry_ids]
  decide +kernel

theorem remaining_ids_exact : remainingIds registry = pendingIds := by
  unfold remainingIds
  rw [known_ids_exact]
  decide +kernel

theorem source_count : sourceIds.card = 117 := by decide +kernel

theorem pending_count : pendingIds.card = 0 := by decide +kernel

theorem pending_ids_exact : pendingIds = ∅ := by
  decide +kernel

theorem partition : sourceIds ∪ pendingIds = allIds := by
  rw [← known_ids_exact, ← remaining_ids_exact]
  exact Remaining117.complete_partition registry

theorem partition_disjoint : Disjoint sourceIds pendingIds := by
  rw [← known_ids_exact, ← remaining_ids_exact]
  exact Remaining117.partition_disjoint registry

theorem source_exclusion (id : Nat) (hi : id ∈ sourceIds) : ExcludesCase id :=
  Remaining117.known_exclusions registry id (by simpa only [known_ids_exact] using hi)

/-- The remaining whole-case contracts. The historical C981/C1092 fields
are supplied by default; both whole original cases are already registered. -/
structure Pending : Prop where
  other_cases : ∀ id ∈ (pendingIds.erase 981).erase 1092, ExcludesCase id
  case981 : C981Compact.Pending := C981Compact.pending_closed
  case1092 : C1092Compact.Pending := C1092Compact.pending_closed

theorem pending_exclusions (work : Pending) : Remaining registry := by
  intro id hid
  have hp : id ∈ pendingIds := by simpa only [remaining_ids_exact] using hid
  by_cases last : id = 981
  · subst id
    exact C981Compact.excludes_case work.case981
  · by_cases wall : id = 1092
    · subst id
      exact C1092Compact.excludes_case work.case1092
    · exact work.other_cases id
        (Finset.mem_erase.mpr ⟨wall,Finset.mem_erase.mpr ⟨last,hp⟩⟩)

/-- All original case contracts are now registered. No mathematical premise
remains in the historical pending-work interface. -/
theorem pending_closed : Pending := by
  refine { other_cases := ?_ }
  intro id hid
  have hp : id ∈ pendingIds :=
    (Finset.mem_erase.mp (Finset.mem_erase.mp hid).2).2
  rw [pending_ids_exact] at hp
  simp at hp

/-- The original unrestricted target through the retained conditional API.
Use pending_closed or the unconditional Compact.Assembly.Final entry point. -/
theorem optimality (work : Pending) : packingConstant12 = 4 :=
  Remaining117.optimality registry (pending_exclusions work)

#print axioms source_exclusion
#print axioms optimality
end N12Compact.SourceAssembly
