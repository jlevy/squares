import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1088
open Sq19.Endgame.Reduction

theorem case1153 : checkNat 1153 = true := by native_decide
#print axioms case1153

theorem case3201 : checkNat 3201 = true := by
  apply check_of_normalize (Case.ofNat 3201)
  have he : (Case.ofNat 3201).normalize = Case.ofNat 1153 := by decide
  rw [he]
  exact case1153
#print axioms case3201

theorem case1155 : checkNat 1155 = true := by native_decide
#print axioms case1155

theorem case1157 : checkNat 1157 = true := by native_decide
#print axioms case1157

theorem case3205 : checkNat 3205 = true := by
  apply check_of_normalize (Case.ofNat 3205)
  have he : (Case.ofNat 3205).normalize = Case.ofNat 1157 := by decide
  rw [he]
  exact case1157
#print axioms case3205

theorem case1159 : checkNat 1159 = true := by native_decide
#print axioms case1159

theorem case1161 : checkNat 1161 = true := by native_decide
#print axioms case1161

theorem case3209 : checkNat 3209 = true := by
  apply check_of_normalize (Case.ofNat 3209)
  have he : (Case.ofNat 3209).normalize = Case.ofNat 1161 := by decide
  rw [he]
  exact case1161
#print axioms case3209

theorem case1163 : checkNat 1163 = true := by native_decide
#print axioms case1163

theorem case1165 : checkNat 1165 = true := by native_decide
#print axioms case1165

theorem case3213 : checkNat 3213 = true := by
  apply check_of_normalize (Case.ofNat 3213)
  have he : (Case.ofNat 3213).normalize = Case.ofNat 1165 := by decide
  rw [he]
  exact case1165
#print axioms case3213

theorem case1167 : checkNat 1167 = true := by native_decide
#print axioms case1167

theorem case1169 : checkNat 1169 = true := by native_decide
#print axioms case1169

theorem case3217 : checkNat 3217 = true := by
  apply check_of_normalize (Case.ofNat 3217)
  have he : (Case.ofNat 3217).normalize = Case.ofNat 1169 := by decide
  rw [he]
  exact case1169
#print axioms case3217

theorem case1171 : checkNat 1171 = true := by native_decide
#print axioms case1171

theorem case1173 : checkNat 1173 = true := by native_decide
#print axioms case1173

theorem case3221 : checkNat 3221 = true := by
  apply check_of_normalize (Case.ofNat 3221)
  have he : (Case.ofNat 3221).normalize = Case.ofNat 1173 := by decide
  rw [he]
  exact case1173
#print axioms case3221

theorem case1175 : checkNat 1175 = true := by native_decide
#print axioms case1175

theorem case1177 : checkNat 1177 = true := by native_decide
#print axioms case1177

theorem case3225 : checkNat 3225 = true := by
  apply check_of_normalize (Case.ofNat 3225)
  have he : (Case.ofNat 3225).normalize = Case.ofNat 1177 := by decide
  rw [he]
  exact case1177
#print axioms case3225

theorem case1179 : checkNat 1179 = true := by native_decide
#print axioms case1179

theorem case1181 : checkNat 1181 = true := by native_decide
#print axioms case1181

theorem case3229 : checkNat 3229 = true := by
  apply check_of_normalize (Case.ofNat 3229)
  have he : (Case.ofNat 3229).normalize = Case.ofNat 1181 := by decide
  rw [he]
  exact case1181
#print axioms case3229

theorem case1183 : checkNat 1183 = true := by native_decide
#print axioms case1183

theorem case1185 : checkNat 1185 = true := by native_decide
#print axioms case1185

theorem case3233 : checkNat 3233 = true := by
  apply check_of_normalize (Case.ofNat 3233)
  have he : (Case.ofNat 3233).normalize = Case.ofNat 1185 := by decide
  rw [he]
  exact case1185
#print axioms case3233

theorem case1187 : checkNat 1187 = true := by native_decide
#print axioms case1187

theorem case1189 : checkNat 1189 = true := by native_decide
#print axioms case1189

theorem case3237 : checkNat 3237 = true := by
  apply check_of_normalize (Case.ofNat 3237)
  have he : (Case.ofNat 3237).normalize = Case.ofNat 1189 := by decide
  rw [he]
  exact case1189
#print axioms case3237

theorem case1191 : checkNat 1191 = true := by native_decide
#print axioms case1191

theorem case1193 : checkNat 1193 = true := by native_decide
#print axioms case1193

theorem case3241 : checkNat 3241 = true := by
  apply check_of_normalize (Case.ofNat 3241)
  have he : (Case.ofNat 3241).normalize = Case.ofNat 1193 := by decide
  rw [he]
  exact case1193
#print axioms case3241

theorem case1195 : checkNat 1195 = true := by native_decide
#print axioms case1195

theorem case1197 : checkNat 1197 = true := by native_decide
#print axioms case1197

theorem case3245 : checkNat 3245 = true := by
  apply check_of_normalize (Case.ofNat 3245)
  have he : (Case.ofNat 3245).normalize = Case.ofNat 1197 := by decide
  rw [he]
  exact case1197
#print axioms case3245

theorem case1199 : checkNat 1199 = true := by native_decide
#print axioms case1199

theorem case1201 : checkNat 1201 = true := by native_decide
#print axioms case1201

theorem case3249 : checkNat 3249 = true := by
  apply check_of_normalize (Case.ofNat 3249)
  have he : (Case.ofNat 3249).normalize = Case.ofNat 1201 := by decide
  rw [he]
  exact case1201
#print axioms case3249

theorem case1203 : checkNat 1203 = true := by native_decide
#print axioms case1203

theorem case1205 : checkNat 1205 = true := by native_decide
#print axioms case1205

theorem case3253 : checkNat 3253 = true := by
  apply check_of_normalize (Case.ofNat 3253)
  have he : (Case.ofNat 3253).normalize = Case.ofNat 1205 := by decide
  rw [he]
  exact case1205
#print axioms case3253

theorem case1207 : checkNat 1207 = true := by native_decide
#print axioms case1207

theorem case1209 : checkNat 1209 = true := by native_decide
#print axioms case1209

theorem case3257 : checkNat 3257 = true := by
  apply check_of_normalize (Case.ofNat 3257)
  have he : (Case.ofNat 3257).normalize = Case.ofNat 1209 := by decide
  rw [he]
  exact case1209
#print axioms case3257

theorem case1211 : checkNat 1211 = true := by native_decide
#print axioms case1211

theorem case1213 : checkNat 1213 = true := by native_decide
#print axioms case1213

theorem case3261 : checkNat 3261 = true := by
  apply check_of_normalize (Case.ofNat 3261)
  have he : (Case.ofNat 3261).normalize = Case.ofNat 1213 := by decide
  rw [he]
  exact case1213
#print axioms case3261

theorem case1215 : checkNat 1215 = true := by native_decide
#print axioms case1215

theorem accepted :
    checkNat 1153 = true ∧
    checkNat 1155 = true ∧
    checkNat 1157 = true ∧
    checkNat 1159 = true ∧
    checkNat 1161 = true ∧
    checkNat 1163 = true ∧
    checkNat 1165 = true ∧
    checkNat 1167 = true ∧
    checkNat 1169 = true ∧
    checkNat 1171 = true ∧
    checkNat 1173 = true ∧
    checkNat 1175 = true ∧
    checkNat 1177 = true ∧
    checkNat 1179 = true ∧
    checkNat 1181 = true ∧
    checkNat 1183 = true ∧
    checkNat 1185 = true ∧
    checkNat 1187 = true ∧
    checkNat 1189 = true ∧
    checkNat 1191 = true ∧
    checkNat 1193 = true ∧
    checkNat 1195 = true ∧
    checkNat 1197 = true ∧
    checkNat 1199 = true ∧
    checkNat 1201 = true ∧
    checkNat 1203 = true ∧
    checkNat 1205 = true ∧
    checkNat 1207 = true ∧
    checkNat 1209 = true ∧
    checkNat 1211 = true ∧
    checkNat 1213 = true ∧
    checkNat 1215 = true ∧
    checkNat 3201 = true ∧
    checkNat 3205 = true ∧
    checkNat 3209 = true ∧
    checkNat 3213 = true ∧
    checkNat 3217 = true ∧
    checkNat 3221 = true ∧
    checkNat 3225 = true ∧
    checkNat 3229 = true ∧
    checkNat 3233 = true ∧
    checkNat 3237 = true ∧
    checkNat 3241 = true ∧
    checkNat 3245 = true ∧
    checkNat 3249 = true ∧
    checkNat 3253 = true ∧
    checkNat 3257 = true ∧
    checkNat 3261 = true := by
  exact ⟨case1153, case1155, case1157, case1159, case1161, case1163, case1165, case1167, case1169, case1171, case1173, case1175, case1177, case1179, case1181, case1183, case1185, case1187, case1189, case1191, case1193, case1195, case1197, case1199, case1201, case1203, case1205, case1207, case1209, case1211, case1213, case1215, case3201, case3205, case3209, case3213, case3217, case3221, case3225, case3229, case3233, case3237, case3241, case3245, case3249, case3253, case3257, case3261⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1088
