import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1120
open Sq19.Endgame.Reduction

theorem case1217 : checkNat 1217 = true := by native_decide
#print axioms case1217

theorem case3265 : checkNat 3265 = true := by
  apply check_of_normalize (Case.ofNat 3265)
  have he : (Case.ofNat 3265).normalize = Case.ofNat 1217 := by decide
  rw [he]
  exact case1217
#print axioms case3265

theorem case1219 : checkNat 1219 = true := by native_decide
#print axioms case1219

theorem case1221 : checkNat 1221 = true := by native_decide
#print axioms case1221

theorem case3269 : checkNat 3269 = true := by
  apply check_of_normalize (Case.ofNat 3269)
  have he : (Case.ofNat 3269).normalize = Case.ofNat 1221 := by decide
  rw [he]
  exact case1221
#print axioms case3269

theorem case1223 : checkNat 1223 = true := by native_decide
#print axioms case1223

theorem case1225 : checkNat 1225 = true := by native_decide
#print axioms case1225

theorem case3273 : checkNat 3273 = true := by
  apply check_of_normalize (Case.ofNat 3273)
  have he : (Case.ofNat 3273).normalize = Case.ofNat 1225 := by decide
  rw [he]
  exact case1225
#print axioms case3273

theorem case1227 : checkNat 1227 = true := by native_decide
#print axioms case1227

theorem case1229 : checkNat 1229 = true := by native_decide
#print axioms case1229

theorem case3277 : checkNat 3277 = true := by
  apply check_of_normalize (Case.ofNat 3277)
  have he : (Case.ofNat 3277).normalize = Case.ofNat 1229 := by decide
  rw [he]
  exact case1229
#print axioms case3277

theorem case1231 : checkNat 1231 = true := by native_decide
#print axioms case1231

theorem case1233 : checkNat 1233 = true := by native_decide
#print axioms case1233

theorem case3281 : checkNat 3281 = true := by
  apply check_of_normalize (Case.ofNat 3281)
  have he : (Case.ofNat 3281).normalize = Case.ofNat 1233 := by decide
  rw [he]
  exact case1233
#print axioms case3281

theorem case1235 : checkNat 1235 = true := by native_decide
#print axioms case1235

theorem case1237 : checkNat 1237 = true := by native_decide
#print axioms case1237

theorem case3285 : checkNat 3285 = true := by
  apply check_of_normalize (Case.ofNat 3285)
  have he : (Case.ofNat 3285).normalize = Case.ofNat 1237 := by decide
  rw [he]
  exact case1237
#print axioms case3285

theorem case1239 : checkNat 1239 = true := by native_decide
#print axioms case1239

theorem case1241 : checkNat 1241 = true := by native_decide
#print axioms case1241

theorem case3289 : checkNat 3289 = true := by
  apply check_of_normalize (Case.ofNat 3289)
  have he : (Case.ofNat 3289).normalize = Case.ofNat 1241 := by decide
  rw [he]
  exact case1241
#print axioms case3289

theorem case1243 : checkNat 1243 = true := by native_decide
#print axioms case1243

theorem case1245 : checkNat 1245 = true := by native_decide
#print axioms case1245

theorem case3293 : checkNat 3293 = true := by
  apply check_of_normalize (Case.ofNat 3293)
  have he : (Case.ofNat 3293).normalize = Case.ofNat 1245 := by decide
  rw [he]
  exact case1245
#print axioms case3293

theorem case1247 : checkNat 1247 = true := by native_decide
#print axioms case1247

theorem case1249 : checkNat 1249 = true := by native_decide
#print axioms case1249

theorem case3297 : checkNat 3297 = true := by
  apply check_of_normalize (Case.ofNat 3297)
  have he : (Case.ofNat 3297).normalize = Case.ofNat 1249 := by decide
  rw [he]
  exact case1249
#print axioms case3297

theorem case1251 : checkNat 1251 = true := by native_decide
#print axioms case1251

theorem case1253 : checkNat 1253 = true := by native_decide
#print axioms case1253

theorem case3301 : checkNat 3301 = true := by
  apply check_of_normalize (Case.ofNat 3301)
  have he : (Case.ofNat 3301).normalize = Case.ofNat 1253 := by decide
  rw [he]
  exact case1253
#print axioms case3301

theorem case1255 : checkNat 1255 = true := by native_decide
#print axioms case1255

theorem case1257 : checkNat 1257 = true := by native_decide
#print axioms case1257

theorem case3305 : checkNat 3305 = true := by
  apply check_of_normalize (Case.ofNat 3305)
  have he : (Case.ofNat 3305).normalize = Case.ofNat 1257 := by decide
  rw [he]
  exact case1257
#print axioms case3305

theorem case1259 : checkNat 1259 = true := by native_decide
#print axioms case1259

theorem case1261 : checkNat 1261 = true := by native_decide
#print axioms case1261

theorem case3309 : checkNat 3309 = true := by
  apply check_of_normalize (Case.ofNat 3309)
  have he : (Case.ofNat 3309).normalize = Case.ofNat 1261 := by decide
  rw [he]
  exact case1261
#print axioms case3309

theorem case1263 : checkNat 1263 = true := by native_decide
#print axioms case1263

theorem case1265 : checkNat 1265 = true := by native_decide
#print axioms case1265

theorem case3313 : checkNat 3313 = true := by
  apply check_of_normalize (Case.ofNat 3313)
  have he : (Case.ofNat 3313).normalize = Case.ofNat 1265 := by decide
  rw [he]
  exact case1265
#print axioms case3313

theorem case1267 : checkNat 1267 = true := by native_decide
#print axioms case1267

theorem case1269 : checkNat 1269 = true := by native_decide
#print axioms case1269

theorem case3317 : checkNat 3317 = true := by
  apply check_of_normalize (Case.ofNat 3317)
  have he : (Case.ofNat 3317).normalize = Case.ofNat 1269 := by decide
  rw [he]
  exact case1269
#print axioms case3317

theorem case1271 : checkNat 1271 = true := by native_decide
#print axioms case1271

theorem case1273 : checkNat 1273 = true := by native_decide
#print axioms case1273

theorem case3321 : checkNat 3321 = true := by
  apply check_of_normalize (Case.ofNat 3321)
  have he : (Case.ofNat 3321).normalize = Case.ofNat 1273 := by decide
  rw [he]
  exact case1273
#print axioms case3321

theorem case1275 : checkNat 1275 = true := by native_decide
#print axioms case1275

theorem case1277 : checkNat 1277 = true := by native_decide
#print axioms case1277

theorem case3325 : checkNat 3325 = true := by
  apply check_of_normalize (Case.ofNat 3325)
  have he : (Case.ofNat 3325).normalize = Case.ofNat 1277 := by decide
  rw [he]
  exact case1277
#print axioms case3325

theorem case1279 : checkNat 1279 = true := by native_decide
#print axioms case1279

theorem accepted :
    checkNat 1217 = true ∧
    checkNat 1219 = true ∧
    checkNat 1221 = true ∧
    checkNat 1223 = true ∧
    checkNat 1225 = true ∧
    checkNat 1227 = true ∧
    checkNat 1229 = true ∧
    checkNat 1231 = true ∧
    checkNat 1233 = true ∧
    checkNat 1235 = true ∧
    checkNat 1237 = true ∧
    checkNat 1239 = true ∧
    checkNat 1241 = true ∧
    checkNat 1243 = true ∧
    checkNat 1245 = true ∧
    checkNat 1247 = true ∧
    checkNat 1249 = true ∧
    checkNat 1251 = true ∧
    checkNat 1253 = true ∧
    checkNat 1255 = true ∧
    checkNat 1257 = true ∧
    checkNat 1259 = true ∧
    checkNat 1261 = true ∧
    checkNat 1263 = true ∧
    checkNat 1265 = true ∧
    checkNat 1267 = true ∧
    checkNat 1269 = true ∧
    checkNat 1271 = true ∧
    checkNat 1273 = true ∧
    checkNat 1275 = true ∧
    checkNat 1277 = true ∧
    checkNat 1279 = true ∧
    checkNat 3265 = true ∧
    checkNat 3269 = true ∧
    checkNat 3273 = true ∧
    checkNat 3277 = true ∧
    checkNat 3281 = true ∧
    checkNat 3285 = true ∧
    checkNat 3289 = true ∧
    checkNat 3293 = true ∧
    checkNat 3297 = true ∧
    checkNat 3301 = true ∧
    checkNat 3305 = true ∧
    checkNat 3309 = true ∧
    checkNat 3313 = true ∧
    checkNat 3317 = true ∧
    checkNat 3321 = true ∧
    checkNat 3325 = true := by
  exact ⟨case1217, case1219, case1221, case1223, case1225, case1227, case1229, case1231, case1233, case1235, case1237, case1239, case1241, case1243, case1245, case1247, case1249, case1251, case1253, case1255, case1257, case1259, case1261, case1263, case1265, case1267, case1269, case1271, case1273, case1275, case1277, case1279, case3265, case3269, case3273, case3277, case3281, case3285, case3289, case3293, case3297, case3301, case3305, case3309, case3313, case3317, case3321, case3325⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1120
