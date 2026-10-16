import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1024
open Sq19.Endgame.Reduction

theorem case1025 : checkNat 1025 = true := by native_decide
#print axioms case1025

theorem case3073 : checkNat 3073 = true := by
  apply check_of_normalize (Case.ofNat 3073)
  have he : (Case.ofNat 3073).normalize = Case.ofNat 1025 := by decide
  rw [he]
  exact case1025
#print axioms case3073

theorem case1027 : checkNat 1027 = true := by native_decide
#print axioms case1027

theorem case1029 : checkNat 1029 = true := by native_decide
#print axioms case1029

theorem case3077 : checkNat 3077 = true := by
  apply check_of_normalize (Case.ofNat 3077)
  have he : (Case.ofNat 3077).normalize = Case.ofNat 1029 := by decide
  rw [he]
  exact case1029
#print axioms case3077

theorem case1031 : checkNat 1031 = true := by native_decide
#print axioms case1031

theorem case1033 : checkNat 1033 = true := by native_decide
#print axioms case1033

theorem case3081 : checkNat 3081 = true := by
  apply check_of_normalize (Case.ofNat 3081)
  have he : (Case.ofNat 3081).normalize = Case.ofNat 1033 := by decide
  rw [he]
  exact case1033
#print axioms case3081

theorem case1035 : checkNat 1035 = true := by native_decide
#print axioms case1035

theorem case1037 : checkNat 1037 = true := by native_decide
#print axioms case1037

theorem case3085 : checkNat 3085 = true := by
  apply check_of_normalize (Case.ofNat 3085)
  have he : (Case.ofNat 3085).normalize = Case.ofNat 1037 := by decide
  rw [he]
  exact case1037
#print axioms case3085

theorem case1039 : checkNat 1039 = true := by native_decide
#print axioms case1039

theorem case1041 : checkNat 1041 = true := by native_decide
#print axioms case1041

theorem case3089 : checkNat 3089 = true := by
  apply check_of_normalize (Case.ofNat 3089)
  have he : (Case.ofNat 3089).normalize = Case.ofNat 1041 := by decide
  rw [he]
  exact case1041
#print axioms case3089

theorem case1043 : checkNat 1043 = true := by native_decide
#print axioms case1043

theorem case1045 : checkNat 1045 = true := by native_decide
#print axioms case1045

theorem case3093 : checkNat 3093 = true := by
  apply check_of_normalize (Case.ofNat 3093)
  have he : (Case.ofNat 3093).normalize = Case.ofNat 1045 := by decide
  rw [he]
  exact case1045
#print axioms case3093

theorem case1047 : checkNat 1047 = true := by native_decide
#print axioms case1047

theorem case1049 : checkNat 1049 = true := by native_decide
#print axioms case1049

theorem case3097 : checkNat 3097 = true := by
  apply check_of_normalize (Case.ofNat 3097)
  have he : (Case.ofNat 3097).normalize = Case.ofNat 1049 := by decide
  rw [he]
  exact case1049
#print axioms case3097

theorem case1051 : checkNat 1051 = true := by native_decide
#print axioms case1051

theorem case1053 : checkNat 1053 = true := by native_decide
#print axioms case1053

theorem case3101 : checkNat 3101 = true := by
  apply check_of_normalize (Case.ofNat 3101)
  have he : (Case.ofNat 3101).normalize = Case.ofNat 1053 := by decide
  rw [he]
  exact case1053
#print axioms case3101

theorem case1055 : checkNat 1055 = true := by native_decide
#print axioms case1055

theorem case1057 : checkNat 1057 = true := by native_decide
#print axioms case1057

theorem case3105 : checkNat 3105 = true := by
  apply check_of_normalize (Case.ofNat 3105)
  have he : (Case.ofNat 3105).normalize = Case.ofNat 1057 := by decide
  rw [he]
  exact case1057
#print axioms case3105

theorem case1059 : checkNat 1059 = true := by native_decide
#print axioms case1059

theorem case1061 : checkNat 1061 = true := by native_decide
#print axioms case1061

theorem case3109 : checkNat 3109 = true := by
  apply check_of_normalize (Case.ofNat 3109)
  have he : (Case.ofNat 3109).normalize = Case.ofNat 1061 := by decide
  rw [he]
  exact case1061
#print axioms case3109

theorem case1063 : checkNat 1063 = true := by native_decide
#print axioms case1063

theorem case1065 : checkNat 1065 = true := by native_decide
#print axioms case1065

theorem case3113 : checkNat 3113 = true := by
  apply check_of_normalize (Case.ofNat 3113)
  have he : (Case.ofNat 3113).normalize = Case.ofNat 1065 := by decide
  rw [he]
  exact case1065
#print axioms case3113

theorem case1067 : checkNat 1067 = true := by native_decide
#print axioms case1067

theorem case1069 : checkNat 1069 = true := by native_decide
#print axioms case1069

theorem case3117 : checkNat 3117 = true := by
  apply check_of_normalize (Case.ofNat 3117)
  have he : (Case.ofNat 3117).normalize = Case.ofNat 1069 := by decide
  rw [he]
  exact case1069
#print axioms case3117

theorem case1071 : checkNat 1071 = true := by native_decide
#print axioms case1071

theorem case1073 : checkNat 1073 = true := by native_decide
#print axioms case1073

theorem case3121 : checkNat 3121 = true := by
  apply check_of_normalize (Case.ofNat 3121)
  have he : (Case.ofNat 3121).normalize = Case.ofNat 1073 := by decide
  rw [he]
  exact case1073
#print axioms case3121

theorem case1075 : checkNat 1075 = true := by native_decide
#print axioms case1075

theorem case1077 : checkNat 1077 = true := by native_decide
#print axioms case1077

theorem case3125 : checkNat 3125 = true := by
  apply check_of_normalize (Case.ofNat 3125)
  have he : (Case.ofNat 3125).normalize = Case.ofNat 1077 := by decide
  rw [he]
  exact case1077
#print axioms case3125

theorem case1079 : checkNat 1079 = true := by native_decide
#print axioms case1079

theorem case1081 : checkNat 1081 = true := by native_decide
#print axioms case1081

theorem case3129 : checkNat 3129 = true := by
  apply check_of_normalize (Case.ofNat 3129)
  have he : (Case.ofNat 3129).normalize = Case.ofNat 1081 := by decide
  rw [he]
  exact case1081
#print axioms case3129

theorem case1083 : checkNat 1083 = true := by native_decide
#print axioms case1083

theorem case1085 : checkNat 1085 = true := by native_decide
#print axioms case1085

theorem case3133 : checkNat 3133 = true := by
  apply check_of_normalize (Case.ofNat 3133)
  have he : (Case.ofNat 3133).normalize = Case.ofNat 1085 := by decide
  rw [he]
  exact case1085
#print axioms case3133

theorem case1087 : checkNat 1087 = true := by native_decide
#print axioms case1087

theorem accepted :
    checkNat 1025 = true ∧
    checkNat 1027 = true ∧
    checkNat 1029 = true ∧
    checkNat 1031 = true ∧
    checkNat 1033 = true ∧
    checkNat 1035 = true ∧
    checkNat 1037 = true ∧
    checkNat 1039 = true ∧
    checkNat 1041 = true ∧
    checkNat 1043 = true ∧
    checkNat 1045 = true ∧
    checkNat 1047 = true ∧
    checkNat 1049 = true ∧
    checkNat 1051 = true ∧
    checkNat 1053 = true ∧
    checkNat 1055 = true ∧
    checkNat 1057 = true ∧
    checkNat 1059 = true ∧
    checkNat 1061 = true ∧
    checkNat 1063 = true ∧
    checkNat 1065 = true ∧
    checkNat 1067 = true ∧
    checkNat 1069 = true ∧
    checkNat 1071 = true ∧
    checkNat 1073 = true ∧
    checkNat 1075 = true ∧
    checkNat 1077 = true ∧
    checkNat 1079 = true ∧
    checkNat 1081 = true ∧
    checkNat 1083 = true ∧
    checkNat 1085 = true ∧
    checkNat 1087 = true ∧
    checkNat 3073 = true ∧
    checkNat 3077 = true ∧
    checkNat 3081 = true ∧
    checkNat 3085 = true ∧
    checkNat 3089 = true ∧
    checkNat 3093 = true ∧
    checkNat 3097 = true ∧
    checkNat 3101 = true ∧
    checkNat 3105 = true ∧
    checkNat 3109 = true ∧
    checkNat 3113 = true ∧
    checkNat 3117 = true ∧
    checkNat 3121 = true ∧
    checkNat 3125 = true ∧
    checkNat 3129 = true ∧
    checkNat 3133 = true := by
  exact ⟨case1025, case1027, case1029, case1031, case1033, case1035, case1037, case1039, case1041, case1043, case1045, case1047, case1049, case1051, case1053, case1055, case1057, case1059, case1061, case1063, case1065, case1067, case1069, case1071, case1073, case1075, case1077, case1079, case1081, case1083, case1085, case1087, case3073, case3077, case3081, case3085, case3089, case3093, case3097, case3101, case3105, case3109, case3113, case3117, case3121, case3125, case3129, case3133⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1024
