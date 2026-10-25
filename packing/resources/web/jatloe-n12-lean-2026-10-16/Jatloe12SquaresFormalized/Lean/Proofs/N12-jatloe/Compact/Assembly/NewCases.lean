import Compact.Completion.CommonCases.C702
import Compact.Completion.CommonCases.C48Rows
import Compact.Completion.FiniteCases.C997
import Compact.Completion.FiniteCases.C580581Completion
import Compact.Completion.CommonCases.C888C889
import Compact.Completion.CommonCases.C982
import Compact.Completion.CommonCases.C893
import Compact.Completion.CommonCases.C1084
import Compact.Completion.CommonCases.C1072
import Compact.Completion.OtherCases.C715.WholeCase
import Compact.Completion.OtherCases.C705716.WholeCases
import Compact.Completion.OtherCases.C1090.OriginalEntrance
import Compact.Completion.OtherCases.C974.Completion
import Compact.Completion.OtherCases.C976.Completion
import Compact.Completion.OtherCases.C1089.OriginalEnding
import Compact.Completion.OtherCases.C1091.Completion
import Compact.Completion.OtherCases.C983.F4Completion
import Compact.Completion.FiniteCases.C975Completion
import Compact.Completion.FiniteCases.C896Completion
import Compact.Completion.FiniteCases.C972Completion
import Compact.Cases.C868.Complete
import Compact.Completion.OtherCases.MergedPending.Completion
import Compact.Completion.OtherCases.MergedPending.C700Completion
import Compact.Cases.C981Compact
import Compact.Cases.C1092Compact
import Compact.Assembly.Remaining117

/-! Whole original-case contracts completed after the supplied handoff.
Only unconditional complete contracts enter this source registry. Shared
geometric lemmas and individual auxiliary-vector exclusions enter their own
joins. Source inclusion does not establish compiler acceptance. -/
namespace N12Compact.NewCases
open S12 S12Completion Remaining117
set_option Elab.async false

def registry : List ProvenCase :=
  [⟨48,CommonCases.C48Rows.excludes48⟩,
   ⟨573,CommonCases.C48Rows.excludes573⟩,
   ⟨574,CommonCases.C48Rows.excludes574⟩,
   ⟨580,FiniteCases.C580581Completion.excludes580⟩,
   ⟨581,FiniteCases.C580581Completion.excludes581⟩,
   ⟨683,MergedPending.case683_excluded⟩,
   ⟨700,MergedPending.case700_excluded⟩,
   ⟨702,CommonCases.C702.excludes⟩,
   ⟨705,N12Compact.Completion.OtherCases.C705716.case705_excluded⟩,
   ⟨715,N12Compact.Completion.OtherCases.C715.whole_case⟩,
   ⟨716,N12Compact.Completion.OtherCases.C705716.case716_excluded⟩,
   ⟨867,MergedPending.case867_excluded⟩,
   ⟨868,C868.case_excluded⟩,
   ⟨888,CommonCases.C888C889.excludes888⟩,
   ⟨889,CommonCases.C888C889.excludes889⟩,
   ⟨893,CommonCases.C893.excludes⟩,
   ⟨896,FiniteCases.C896Ending.case_excluded⟩,
   ⟨972,FiniteCases.C972.case_excluded⟩,
   ⟨974,N12Compact.Completion.OtherCases.C974.OriginalData.case_excluded⟩,
   ⟨975,FiniteCases.C975Selection.case_excluded⟩,
   ⟨976,N12Compact.Completion.OtherCases.C976.OriginalData.case_excluded⟩,
   ⟨981,C981Compact.excludes_case_complete⟩,
   ⟨982,CommonCases.C982.excludes⟩,
   ⟨983,N12Compact.Completion.OtherCases.C983.case_excluded⟩,
   ⟨997,FiniteCases.C997.excludes⟩,
   ⟨1072,CommonCases.C1072.excludes⟩,
   ⟨1084,CommonCases.C1084.excludes⟩,
   ⟨1089,N12Compact.Completion.OtherCases.C1089.OriginalData.case_excluded⟩,
   ⟨1090,N12Compact.Completion.OtherCases.C1090.OriginalData.case_excluded⟩,
   ⟨1091,N12Compact.Completion.OtherCases.C1091.Completion.case_excluded⟩,
   ⟨1092,C1092Compact.excludes_case_complete⟩]
def ids : List Nat := [48,573,574,580,581,683,700,702,705,715,716,867,868,888,889,893,896,972,974,975,976,981,982,983,997,1072,1084,1089,1090,1091,1092]
def provenIds : Finset Nat := {48,573,574,580,581,683,700,702,705,715,716,867,868,888,889,893,896,972,974,975,976,981,982,983,997,1072,1084,1089,1090,1091,1092}

theorem registry_ids : registry.map ProvenCase.id = ids := rfl
theorem known_ids : knownIds registry = provenIds := by decide +kernel
theorem count : provenIds.card = 31 := by decide +kernel

#print axioms CommonCases.C982.excludes
#print axioms N12Compact.Completion.OtherCases.C715.whole_case
#print axioms CommonCases.C893.excludes
#print axioms CommonCases.C1084.excludes
#print axioms CommonCases.C1072.excludes
#print axioms N12Compact.Completion.OtherCases.C705716.case705_excluded
#print axioms N12Compact.Completion.OtherCases.C705716.case716_excluded
#print axioms FiniteCases.C580581Completion.excludes580
#print axioms FiniteCases.C580581Completion.excludes581
#print axioms N12Compact.Completion.OtherCases.C1090.OriginalData.case_excluded
#print axioms C981Compact.excludes_case_complete
#print axioms N12Compact.Completion.OtherCases.C974.OriginalData.case_excluded
#print axioms N12Compact.Completion.OtherCases.C976.OriginalData.case_excluded
#print axioms N12Compact.Completion.OtherCases.C1089.OriginalData.case_excluded
#print axioms N12Compact.Completion.OtherCases.C1091.Completion.case_excluded
#print axioms C1092Compact.excludes_case_complete
#print axioms N12Compact.Completion.OtherCases.C983.case_excluded
#print axioms FiniteCases.C975Selection.case_excluded
#print axioms FiniteCases.C896Ending.case_excluded
#print axioms MergedPending.case700_excluded
#print axioms MergedPending.case683_excluded
#print axioms MergedPending.case867_excluded
#print axioms C868.case_excluded
#print axioms FiniteCases.C972.case_excluded
end N12Compact.NewCases
