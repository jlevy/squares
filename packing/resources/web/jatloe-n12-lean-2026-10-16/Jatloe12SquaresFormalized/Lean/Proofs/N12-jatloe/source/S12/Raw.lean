import S12.RawData
import S12.CoverData
import S12.CachedEnumeration
import Mathlib.Data.Finset.Sort

namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def earlyOK (f : Finset Nat) : Bool :=
  decide (2 ≤ (f ∩ exempt0).card) && decide (2 ≤ (f ∩ exempt1).card) &&
  decide (Disjoint f badMasks) &&
  conflictingPairs.all fun p => !(decide (p.1 ∈ f) && decide (p.2 ∈ f))

def rawFamilies : List (Finset Nat) :=
  cachedEnumerate candidateMasks maskSupport 16 Finset.univ 12

def earlyFamilies : List (Finset Nat) := rawFamilies.filter earlyOK

def coveredFamilies : List (Finset Nat) := coverRows.flatMap fun r => orbit r.groups

theorem raw_count : rawFamilies.length = 157499 := by native_decide

theorem early_count : earlyFamilies.length = 4375 := by native_decide

def familyKey (f : Finset Nat) : List Nat := f.sort (· ≤ ·)

def coveredKeys : List (List Nat) := coveredFamilies.map familyKey

theorem early_covered : earlyFamilies.all (fun f => decide (familyKey f ∈ coveredKeys)) = true := by
  native_decide

/-- Every disjoint twelve-group assignment passing the stated necessary
conditions belongs to one of the 577 listed symmetry orbits. No conclusion
about geometric packings is hidden in the hypotheses. -/
theorem reduction_to_577 (f : Finset Nat)
    (ha : Admissible candidateMasks maskSupport Finset.univ f)
    (hc : f.card = 12) (he : earlyOK f = true) :
    ∃ r ∈ coverRows, f ∈ orbit r.groups := by
  have hr := cachedEnumerate_complete candidateMasks maskSupport 16 Finset.univ f (by decide) ha
  rw [hc] at hr
  have hm : f ∈ earlyFamilies := List.mem_filter.mpr ⟨hr, he⟩
  have ht := List.all_eq_true.mp early_covered f hm
  have hk : familyKey f ∈ coveredKeys := of_decide_eq_true ht
  obtain ⟨g, hg, heq⟩ := List.mem_map.mp hk
  have hfg : g=f := by
    have hh := congrArg List.toFinset heq
    simpa [familyKey] using hh
  subst g
  exact List.mem_flatMap.mp hg

/-- The complete finite reduction, conditional on the geometric interpretation
of its hull and auxiliary-ownership tables. Formalizing those hypotheses from
an arbitrary packing is still required for the full reduction theorem. -/
theorem finite_reduction_to_117 (f : Finset Nat)
    (ha : Admissible candidateMasks maskSupport Finset.univ f)
    (hc : f.card = 12) (he : earlyOK f = true)
    (hgeometry : ∀ r ∈ coverRows, f ∈ orbit r.groups → RowConditions r) :
    ∃ r ∈ coverRows, f ∈ orbit r.groups ∧ r.originalId ∈ expectedIds := by
  obtain ⟨r, hr, ho⟩ := reduction_to_577 f ha hc he
  refine ⟨r, hr, ho, ?_⟩
  rw [← survivors_exact]
  apply List.mem_map.mpr
  exact ⟨r, List.mem_filter.mpr ⟨hr, row_conditions_survive r (hgeometry r hr ho)⟩, rfl⟩

#print axioms reduction_to_577
#print axioms finite_reduction_to_117
end S12
