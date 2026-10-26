import Compact.Bridge.C981TwoTipRows
import Compact.Bridge.C981Row27
import Compact.Bridge.C981InwardWallRows
import Compact.Completion.C981.OutwardRows
import Compact.Completion.C981.ShortRows.CoreRows
import Compact.Completion.C981.ShortWallRows
import Compact.Completion.C981.ShortWall71
import Compact.Completion.C981.Common107
import Compact.Completion.C981.Last104
import Compact.Completion.C981.NewSimpleShortRows
import Compact.Completion.C981.OutwardTranspose
import Compact.Completion.C981.ShortCentralRows

/-! Forty-two whole original representative exclusions, independently of
fresh acceptance of the larger classification and complete case-981 assembly.
The last twenty contracts use shared continuous geometry and original owners. -/
namespace N12Compact.C981Progress
open S12Completion.C981
set_option Elab.async false

def previousIds : List Nat :=
  ((C981TwoTipRows.coveredIds ++ [27]) ++ C981InwardWallRows.coveredIds) ++
    C981CompletionOutwardRows.coveredIds

def earlierIds : List Nat :=
  ((previousIds ++ [101]) ++ C981CompletionShortWallRows.coveredIds) ++ [71]

/-- The exact twenty original-vector contracts added by the simplified
common/last cycles and the two outward-neighbor reductions. -/
def completionIds : List Nat :=
  (((C981CompletionCommonRows.coveredIds ++ [107,29,104]) ++
    C981CompletionNewSimpleShortRows.coveredIds) ++ [55]) ++
    C981CompletionShortCentralRows.coveredIds

def newIds : List Nat := earlierIds ++ completionIds

theorem completionIds_exact : completionIds =
    [2,28,30,34,37,41,43,69,103,107,29,104,54,56,58,73,109,55,93,98] := by
  decide +kernel

theorem completionIds_count : completionIds.length = 20 := by decide +kernel

theorem newIds_exact : newIds =
    [25,31,40,70,32,33,38,57,99,94,95,27,36,106,24,26,39,101,59,105,108,71,
      2,28,30,34,37,41,43,69,103,107,29,104,54,56,58,73,109,55,93,98] := by
  decide +kernel

theorem newIds_count : newIds.length = 42 := by decide +kernel
theorem newIds_distinct : newIds.Nodup := by decide +kernel
theorem newIds_bound : ∀ i ∈ newIds, i < 117 := by decide +kernel

theorem previous_excluded (i : Nat) (hi : i ∈ previousIds) :
    ExcludesVector (representativeVectors[i]!) := by
  rcases List.mem_append.mp hi with previous | outward
  · rcases List.mem_append.mp previous with earlier | inward
    · rcases List.mem_append.mp earlier with tips | row
      · exact C981TwoTipRows.covered_excluded i tips
      · have same : i = 27 := List.mem_singleton.mp row
        subst i
        exact C981Row27.representative27_excluded
    · exact C981InwardWallRows.covered_excluded i inward
  · exact C981CompletionOutwardRows.covered_excluded i outward

theorem earlier_excluded (i : Nat) (hi : i ∈ earlierIds) :
    ExcludesVector (representativeVectors[i]!) := by
  rcases List.mem_append.mp hi with earlier | row71
  · rcases List.mem_append.mp earlier with earlier | shortWall
    · rcases List.mem_append.mp earlier with previous | row101
      · exact previous_excluded i previous
      · have same : i = 101 := List.mem_singleton.mp row101
        subst i
        exact C981CompletionShortRows.representative101_excluded
    · exact C981CompletionShortWallRows.covered_excluded i shortWall
  · have same : i = 71 := List.mem_singleton.mp row71
    subst i
    exact C981CompletionShortWall71.representative71_excluded

theorem completion_excluded (i : Nat) (hi : i ∈ completionIds) :
    ExcludesVector (representativeVectors[i]!) := by
  rcases List.mem_append.mp hi with previous | central
  · rcases List.mem_append.mp previous with previous | row55
    · rcases List.mem_append.mp previous with cycles | simple
      · rcases List.mem_append.mp cycles with common | singles
        · exact C981CompletionCommonRows.covered_excluded i common
        · simp only [List.mem_cons,List.not_mem_nil,or_false] at singles
          rcases singles with rfl | rfl | rfl
          · exact C981CompletionCommon107.representative107_excluded
          · exact C981CompletionLastRows.representative29_excluded
          · exact C981CompletionLast104.representative104_excluded
      · exact C981CompletionNewSimpleShortRows.covered_excluded i simple
    · have same : i = 55 := List.mem_singleton.mp row55
      subst i
      exact C981CompletionOutwardTranspose.representative55_excluded
  · exact C981CompletionShortCentralRows.covered_excluded i central

theorem new_excluded (i : Nat) (hi : i ∈ newIds) :
    ExcludesVector (representativeVectors[i]!) := by
  rcases List.mem_append.mp hi with earlier | completed
  · exact earlier_excluded i earlier
  · exact completion_excluded i completed

#check new_excluded
#print axioms new_excluded
end N12Compact.C981Progress
