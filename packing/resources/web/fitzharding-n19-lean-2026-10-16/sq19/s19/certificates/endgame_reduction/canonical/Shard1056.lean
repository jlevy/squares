import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1056
open Sq19.Endgame.Reduction

theorem case1089 : checkNat 1089 = true := by native_decide
#print axioms case1089

theorem case3137 : checkNat 3137 = true := by
  apply check_of_normalize (Case.ofNat 3137)
  have he : (Case.ofNat 3137).normalize = Case.ofNat 1089 := by decide
  rw [he]
  exact case1089
#print axioms case3137

theorem case1091 : checkNat 1091 = true := by native_decide
#print axioms case1091

theorem case1093 : checkNat 1093 = true := by native_decide
#print axioms case1093

theorem case3141 : checkNat 3141 = true := by
  apply check_of_normalize (Case.ofNat 3141)
  have he : (Case.ofNat 3141).normalize = Case.ofNat 1093 := by decide
  rw [he]
  exact case1093
#print axioms case3141

theorem case1095 : checkNat 1095 = true := by native_decide
#print axioms case1095

theorem case1097 : checkNat 1097 = true := by native_decide
#print axioms case1097

theorem case3145 : checkNat 3145 = true := by
  apply check_of_normalize (Case.ofNat 3145)
  have he : (Case.ofNat 3145).normalize = Case.ofNat 1097 := by decide
  rw [he]
  exact case1097
#print axioms case3145

theorem case1099 : checkNat 1099 = true := by native_decide
#print axioms case1099

theorem case1101 : checkNat 1101 = true := by native_decide
#print axioms case1101

theorem case3149 : checkNat 3149 = true := by
  apply check_of_normalize (Case.ofNat 3149)
  have he : (Case.ofNat 3149).normalize = Case.ofNat 1101 := by decide
  rw [he]
  exact case1101
#print axioms case3149

theorem case1103 : checkNat 1103 = true := by native_decide
#print axioms case1103

theorem case1105 : checkNat 1105 = true := by native_decide
#print axioms case1105

theorem case3153 : checkNat 3153 = true := by
  apply check_of_normalize (Case.ofNat 3153)
  have he : (Case.ofNat 3153).normalize = Case.ofNat 1105 := by decide
  rw [he]
  exact case1105
#print axioms case3153

theorem case1107 : checkNat 1107 = true := by native_decide
#print axioms case1107

theorem case1109 : checkNat 1109 = true := by native_decide
#print axioms case1109

theorem case3157 : checkNat 3157 = true := by
  apply check_of_normalize (Case.ofNat 3157)
  have he : (Case.ofNat 3157).normalize = Case.ofNat 1109 := by decide
  rw [he]
  exact case1109
#print axioms case3157

theorem case1111 : checkNat 1111 = true := by native_decide
#print axioms case1111

theorem case1113 : checkNat 1113 = true := by native_decide
#print axioms case1113

theorem case3161 : checkNat 3161 = true := by
  apply check_of_normalize (Case.ofNat 3161)
  have he : (Case.ofNat 3161).normalize = Case.ofNat 1113 := by decide
  rw [he]
  exact case1113
#print axioms case3161

theorem case1115 : checkNat 1115 = true := by native_decide
#print axioms case1115

theorem case1117 : checkNat 1117 = true := by native_decide
#print axioms case1117

theorem case3165 : checkNat 3165 = true := by
  apply check_of_normalize (Case.ofNat 3165)
  have he : (Case.ofNat 3165).normalize = Case.ofNat 1117 := by decide
  rw [he]
  exact case1117
#print axioms case3165

theorem case1119 : checkNat 1119 = true := by native_decide
#print axioms case1119

theorem case1121 : checkNat 1121 = true := by native_decide
#print axioms case1121

theorem case3169 : checkNat 3169 = true := by
  apply check_of_normalize (Case.ofNat 3169)
  have he : (Case.ofNat 3169).normalize = Case.ofNat 1121 := by decide
  rw [he]
  exact case1121
#print axioms case3169

theorem case1123 : checkNat 1123 = true := by native_decide
#print axioms case1123

theorem case1125 : checkNat 1125 = true := by native_decide
#print axioms case1125

theorem case3173 : checkNat 3173 = true := by
  apply check_of_normalize (Case.ofNat 3173)
  have he : (Case.ofNat 3173).normalize = Case.ofNat 1125 := by decide
  rw [he]
  exact case1125
#print axioms case3173

theorem case1127 : checkNat 1127 = true := by native_decide
#print axioms case1127

theorem case1129 : checkNat 1129 = true := by native_decide
#print axioms case1129

theorem case3177 : checkNat 3177 = true := by
  apply check_of_normalize (Case.ofNat 3177)
  have he : (Case.ofNat 3177).normalize = Case.ofNat 1129 := by decide
  rw [he]
  exact case1129
#print axioms case3177

theorem case1131 : checkNat 1131 = true := by native_decide
#print axioms case1131

theorem case1133 : checkNat 1133 = true := by native_decide
#print axioms case1133

theorem case3181 : checkNat 3181 = true := by
  apply check_of_normalize (Case.ofNat 3181)
  have he : (Case.ofNat 3181).normalize = Case.ofNat 1133 := by decide
  rw [he]
  exact case1133
#print axioms case3181

theorem case1135 : checkNat 1135 = true := by native_decide
#print axioms case1135

theorem case1137 : checkNat 1137 = true := by native_decide
#print axioms case1137

theorem case3185 : checkNat 3185 = true := by
  apply check_of_normalize (Case.ofNat 3185)
  have he : (Case.ofNat 3185).normalize = Case.ofNat 1137 := by decide
  rw [he]
  exact case1137
#print axioms case3185

theorem case1139 : checkNat 1139 = true := by native_decide
#print axioms case1139

theorem case1141 : checkNat 1141 = true := by native_decide
#print axioms case1141

theorem case3189 : checkNat 3189 = true := by
  apply check_of_normalize (Case.ofNat 3189)
  have he : (Case.ofNat 3189).normalize = Case.ofNat 1141 := by decide
  rw [he]
  exact case1141
#print axioms case3189

theorem case1143 : checkNat 1143 = true := by native_decide
#print axioms case1143

theorem case1145 : checkNat 1145 = true := by native_decide
#print axioms case1145

theorem case3193 : checkNat 3193 = true := by
  apply check_of_normalize (Case.ofNat 3193)
  have he : (Case.ofNat 3193).normalize = Case.ofNat 1145 := by decide
  rw [he]
  exact case1145
#print axioms case3193

theorem case1147 : checkNat 1147 = true := by native_decide
#print axioms case1147

theorem case1149 : checkNat 1149 = true := by native_decide
#print axioms case1149

theorem case3197 : checkNat 3197 = true := by
  apply check_of_normalize (Case.ofNat 3197)
  have he : (Case.ofNat 3197).normalize = Case.ofNat 1149 := by decide
  rw [he]
  exact case1149
#print axioms case3197

theorem case1151 : checkNat 1151 = true := by native_decide
#print axioms case1151

theorem accepted :
    checkNat 1089 = true ∧
    checkNat 1091 = true ∧
    checkNat 1093 = true ∧
    checkNat 1095 = true ∧
    checkNat 1097 = true ∧
    checkNat 1099 = true ∧
    checkNat 1101 = true ∧
    checkNat 1103 = true ∧
    checkNat 1105 = true ∧
    checkNat 1107 = true ∧
    checkNat 1109 = true ∧
    checkNat 1111 = true ∧
    checkNat 1113 = true ∧
    checkNat 1115 = true ∧
    checkNat 1117 = true ∧
    checkNat 1119 = true ∧
    checkNat 1121 = true ∧
    checkNat 1123 = true ∧
    checkNat 1125 = true ∧
    checkNat 1127 = true ∧
    checkNat 1129 = true ∧
    checkNat 1131 = true ∧
    checkNat 1133 = true ∧
    checkNat 1135 = true ∧
    checkNat 1137 = true ∧
    checkNat 1139 = true ∧
    checkNat 1141 = true ∧
    checkNat 1143 = true ∧
    checkNat 1145 = true ∧
    checkNat 1147 = true ∧
    checkNat 1149 = true ∧
    checkNat 1151 = true ∧
    checkNat 3137 = true ∧
    checkNat 3141 = true ∧
    checkNat 3145 = true ∧
    checkNat 3149 = true ∧
    checkNat 3153 = true ∧
    checkNat 3157 = true ∧
    checkNat 3161 = true ∧
    checkNat 3165 = true ∧
    checkNat 3169 = true ∧
    checkNat 3173 = true ∧
    checkNat 3177 = true ∧
    checkNat 3181 = true ∧
    checkNat 3185 = true ∧
    checkNat 3189 = true ∧
    checkNat 3193 = true ∧
    checkNat 3197 = true := by
  exact ⟨case1089, case1091, case1093, case1095, case1097, case1099, case1101, case1103, case1105, case1107, case1109, case1111, case1113, case1115, case1117, case1119, case1121, case1123, case1125, case1127, case1129, case1131, case1133, case1135, case1137, case1139, case1141, case1143, case1145, case1147, case1149, case1151, case3137, case3141, case3145, case3149, case3153, case3157, case3161, case3165, case3169, case3173, case3177, case3181, case3185, case3189, case3193, case3197⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1056
