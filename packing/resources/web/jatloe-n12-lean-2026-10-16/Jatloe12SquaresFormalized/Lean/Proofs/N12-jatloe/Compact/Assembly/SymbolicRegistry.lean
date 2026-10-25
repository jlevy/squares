import Compact.Assembly.Remaining117
import Compact.Assembly.FourSquareCases
import Compact.Assembly.FourSquareVariantCases
import Compact.Assembly.FourSquareConvexCases
import Compact.Assembly.FourSquareHighRightCases
import Compact.Assembly.FourSquareUnusedCases
import Compact.Assembly.FourSquareHighRightExtraCases
import Compact.Assembly.MergedLowerCases
import Compact.Assembly.Endpoint684
import Compact.Assembly.C849851
import Compact.Assembly.MergedTopFurther
import Compact.Assembly.OppositeCentralWalls
import Compact.Bridge.C696OwnedWestClosure
import Compact.Assembly.C84
import Compact.Bridge.C977CenterClosure

/-! Actual source proof terms for 79 original case obligations.
Every entry uses a whole-case exclusion, including its retained-row identity.
No archive receipt, proposed ID, or partial vector certificate removes a case.
The module and its source dependencies still require the parent replay. -/

namespace N12Compact.SymbolicRegistry
open S12 S12Completion Remaining117
set_option Elab.async false
set_option maxRecDepth 10000

/-- Shared symbolic families, with a full original exclusion in every entry. -/
def registry : List ProvenCase := [
  ⟨28, FourSquareCases.covered_cases_excluded 28 (by decide +kernel)⟩,
  ⟨78, FourSquareCases.covered_cases_excluded 78 (by decide +kernel)⟩,
  ⟨537, FourSquareCases.covered_cases_excluded 537 (by decide +kernel)⟩,
  ⟨556, FourSquareCases.covered_cases_excluded 556 (by decide +kernel)⟩,
  ⟨565, FourSquareCases.covered_cases_excluded 565 (by decide +kernel)⟩,
  ⟨567, FourSquareCases.covered_cases_excluded 567 (by decide +kernel)⟩,
  ⟨569, FourSquareCases.covered_cases_excluded 569 (by decide +kernel)⟩,
  ⟨570, FourSquareCases.covered_cases_excluded 570 (by decide +kernel)⟩,
  ⟨575, FourSquareCases.covered_cases_excluded 575 (by decide +kernel)⟩,
  ⟨576, FourSquareCases.covered_cases_excluded 576 (by decide +kernel)⟩,
  ⟨577, FourSquareCases.covered_cases_excluded 577 (by decide +kernel)⟩,
  ⟨585, FourSquareCases.covered_cases_excluded 585 (by decide +kernel)⟩,
  ⟨1085, FourSquareCases.covered_cases_excluded 1085 (by decide +kernel)⟩,
  ⟨1086, FourSquareCases.covered_cases_excluded 1086 (by decide +kernel)⟩,
  ⟨1087, FourSquareCases.covered_cases_excluded 1087 (by decide +kernel)⟩,
  ⟨405, FourSquareVariantCases.covered_cases_excluded 405 (by decide +kernel)⟩,
  ⟨424, FourSquareVariantCases.covered_cases_excluded 424 (by decide +kernel)⟩,
  ⟨985, FourSquareVariantCases.covered_cases_excluded 985 (by decide +kernel)⟩,
  ⟨990, FourSquareVariantCases.covered_cases_excluded 990 (by decide +kernel)⟩,
  ⟨993, FourSquareVariantCases.covered_cases_excluded 993 (by decide +kernel)⟩,
  ⟨994, FourSquareVariantCases.covered_cases_excluded 994 (by decide +kernel)⟩,
  ⟨999, FourSquareVariantCases.covered_cases_excluded 999 (by decide +kernel)⟩,
  ⟨1063, FourSquareVariantCases.covered_cases_excluded 1063 (by decide +kernel)⟩,
  ⟨1064, FourSquareVariantCases.covered_cases_excluded 1064 (by decide +kernel)⟩,
  ⟨1069, FourSquareVariantCases.covered_cases_excluded 1069 (by decide +kernel)⟩,
  ⟨1070, FourSquareVariantCases.covered_cases_excluded 1070 (by decide +kernel)⟩,
  ⟨445, FourSquareConvexCases.covered_cases_excluded 445 (by decide +kernel)⟩,
  ⟨454, FourSquareConvexCases.covered_cases_excluded 454 (by decide +kernel)⟩,
  ⟨862, FourSquareConvexCases.covered_cases_excluded 862 (by decide +kernel)⟩,
  ⟨864, FourSquareConvexCases.covered_cases_excluded 864 (by decide +kernel)⟩,
  ⟨992, FourSquareConvexCases.covered_cases_excluded 992 (by decide +kernel)⟩,
  ⟨995, FourSquareConvexCases.covered_cases_excluded 995 (by decide +kernel)⟩,
  ⟨998, FourSquareConvexCases.covered_cases_excluded 998 (by decide +kernel)⟩,
  ⟨1001, FourSquareConvexCases.covered_cases_excluded 1001 (by decide +kernel)⟩,
  ⟨1002, FourSquareConvexCases.covered_cases_excluded 1002 (by decide +kernel)⟩,
  ⟨678, FourSquareHighRightCases.covered_cases_excluded 678 (by decide +kernel)⟩,
  ⟨680, FourSquareHighRightCases.covered_cases_excluded 680 (by decide +kernel)⟩,
  ⟨691, FourSquareHighRightCases.covered_cases_excluded 691 (by decide +kernel)⟩,
  ⟨694, FourSquareHighRightCases.covered_cases_excluded 694 (by decide +kernel)⟩,
  ⟨711, FourSquareHighRightCases.covered_cases_excluded 711 (by decide +kernel)⟩,
  ⟨846, FourSquareHighRightCases.covered_cases_excluded 846 (by decide +kernel)⟩,
  ⟨847, FourSquareHighRightCases.covered_cases_excluded 847 (by decide +kernel)⟩,
  ⟨852, FourSquareHighRightCases.covered_cases_excluded 852 (by decide +kernel)⟩,
  ⟨853, FourSquareHighRightCases.covered_cases_excluded 853 (by decide +kernel)⟩,
  ⟨886, FourSquareHighRightCases.covered_cases_excluded 886 (by decide +kernel)⟩,
  ⟨887, FourSquareHighRightCases.covered_cases_excluded 887 (by decide +kernel)⟩,
  ⟨1073, FourSquareHighRightCases.covered_cases_excluded 1073 (by decide +kernel)⟩,
  ⟨1074, FourSquareHighRightCases.covered_cases_excluded 1074 (by decide +kernel)⟩,
  ⟨841, FourSquareUnusedCases.covered_cases_excluded 841 (by decide +kernel)⟩,
  ⟨842, FourSquareUnusedCases.covered_cases_excluded 842 (by decide +kernel)⟩,
  ⟨669, FourSquareHighRightExtraCases.covered_cases_excluded 669 (by decide +kernel)⟩,
  ⟨670, FourSquareHighRightExtraCases.covered_cases_excluded 670 (by decide +kernel)⟩,
  ⟨673, FourSquareHighRightExtraCases.covered_cases_excluded 673 (by decide +kernel)⟩,
  ⟨674, FourSquareHighRightExtraCases.covered_cases_excluded 674 (by decide +kernel)⟩,
  ⟨675, FourSquareHighRightExtraCases.covered_cases_excluded 675 (by decide +kernel)⟩,
  ⟨690, FourSquareHighRightExtraCases.covered_cases_excluded 690 (by decide +kernel)⟩,
  ⟨848, FourSquareHighRightExtraCases.covered_cases_excluded 848 (by decide +kernel)⟩,
  ⟨850, FourSquareHighRightExtraCases.covered_cases_excluded 850 (by decide +kernel)⟩,
  ⟨71, MergedLowerCases.covered_cases_excluded 71 (by decide +kernel)⟩,
  ⟨80, MergedLowerCases.covered_cases_excluded 80 (by decide +kernel)⟩,
  ⟨589, MergedLowerCases.covered_cases_excluded 589 (by decide +kernel)⟩,
  ⟨590, MergedLowerCases.covered_cases_excluded 590 (by decide +kernel)⟩,
  ⟨684, Endpoint684Assembly.excludes_case⟩,
  ⟨849, C849851Assembly.excludes849⟩,
  ⟨851, C849851Assembly.excludes851⟩,
  ⟨697, MergedTopFurtherAssembly.excludes697⟩,
  ⟨698, MergedTopFurtherAssembly.excludes698⟩,
  ⟨699, MergedTopFurtherAssembly.excludes699⟩,
  ⟨709, OppositeCentralWallsAssembly.excludes709⟩,
  ⟨882, OppositeCentralWallsAssembly.excludes882⟩,
  ⟨890, OppositeCentralWallsAssembly.excludes890⟩,
  ⟨1075, OppositeCentralWallsAssembly.excludes1075⟩,
  ⟨1077, OppositeCentralWallsAssembly.excludes1077⟩,
  ⟨1078, OppositeCentralWallsAssembly.excludes1078⟩,
  ⟨1081, OppositeCentralWallsAssembly.excludes1081⟩,
  ⟨1083, OppositeCentralWallsAssembly.excludes1083⟩,
  ⟨696, C696OwnedWestClosure.excludes⟩,
  ⟨84, C84Assembly.excludes_case⟩,
  ⟨977, C977CenterClosure.excludes⟩
]

/-- Explicit view of the proof-bearing registry, checked below. -/
def provenIds : Finset Nat :=
  {28,71,78,80,84,405,424,445,454,537,556,565,567,569,570,575,576,577,585,589,590,669,670,673,674,675,678,680,684,690,691,694,696,697,698,699,709,711,841,842,846,847,848,849,850,851,852,853,862,864,882,886,887,890,977,985,990,992,993,994,995,998,999,1001,1002,1063,1064,1069,1070,1073,1074,1075,1077,1078,1081,1083,1085,1086,1087}

/-- Every original obligation outside that registry; C898 is still included. -/
def pendingIds : Finset Nat :=
  {48,573,574,580,581,683,700,701,702,705,713,715,716,717,867,868,888,889,893,896,898,972,973,974,975,976,978,979,981,982,983,997,1072,1084,1089,1090,1091,1092}

/-- Project identifiers once; exclusion proof terms are never evaluated by
the finite set checks below. -/
theorem registry_ids : registry.map ProvenCase.id =
    [28,78,537,556,565,567,569,570,575,576,577,585,1085,1086,1087,405,424,985,990,993,994,999,1063,1064,1069,1070,445,454,862,864,992,995,998,1001,1002,678,680,691,694,711,846,847,852,853,886,887,1073,1074,841,842,669,670,673,674,675,690,848,850,71,80,589,590,684,849,851,697,698,699,709,882,890,1075,1077,1078,1081,1083,696,84,977] := by rfl

theorem registry_length : registry.length = 79 := by
  have h := congrArg List.length registry_ids
  simpa only [List.length_map, List.length_cons, List.length_nil] using h

theorem known_ids_exact : knownIds registry = provenIds := by
  unfold knownIds
  rw [registry_ids]
  decide +kernel

theorem remaining_ids_exact : remainingIds registry = pendingIds := by
  unfold remainingIds
  rw [known_ids_exact]
  decide +kernel

theorem proven_count : provenIds.card = 79 := by decide +kernel

theorem pending_count : pendingIds.card = 38 := by decide +kernel

theorem registered_count : (knownIds registry).card = 79 := by
  rw [known_ids_exact]
  exact proven_count

theorem remaining_count : (remainingIds registry).card = 38 := by
  rw [remaining_ids_exact]
  exact pending_count

theorem partition : provenIds ∪ pendingIds = allIds := by
  rw [← known_ids_exact, ← remaining_ids_exact]
  exact Remaining117.complete_partition registry

theorem partition_disjoint : Disjoint provenIds pendingIds := by
  rw [← known_ids_exact, ← remaining_ids_exact]
  exact Remaining117.partition_disjoint registry

theorem registered_exclusion (id : Nat) (hid : id ∈ provenIds) : ExcludesCase id :=
  Remaining117.known_exclusions registry id (by simpa only [known_ids_exact] using hid)

/-- Exactly the 38 original whole-case obligations still needed by this route. -/
def Pending : Prop := ∀ id ∈ pendingIds, ExcludesCase id

/-- Conditional global target in the unchanged original model.
The only case assumptions are the displayed 38 pending exclusions. -/
theorem optimality (remainingExclusions : Pending) : packingConstant12 = 4 := by
  apply Remaining117.optimality registry
  intro id hid
  exact remainingExclusions id (by simpa only [remaining_ids_exact] using hid)

#print axioms registered_exclusion
#print axioms optimality
end N12Compact.SymbolicRegistry
