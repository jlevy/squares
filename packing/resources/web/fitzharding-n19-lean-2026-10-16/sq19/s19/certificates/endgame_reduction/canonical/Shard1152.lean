import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1152
open Sq19.Endgame.Reduction

theorem case1281 : checkNat 1281 = true := by native_decide
#print axioms case1281

theorem case3329 : checkNat 3329 = true := by
  apply check_of_normalize (Case.ofNat 3329)
  have he : (Case.ofNat 3329).normalize = Case.ofNat 1281 := by decide
  rw [he]
  exact case1281
#print axioms case3329

theorem case1283 : checkNat 1283 = true := by native_decide
#print axioms case1283

theorem case1285 : checkNat 1285 = true := by native_decide
#print axioms case1285

theorem case3333 : checkNat 3333 = true := by
  apply check_of_normalize (Case.ofNat 3333)
  have he : (Case.ofNat 3333).normalize = Case.ofNat 1285 := by decide
  rw [he]
  exact case1285
#print axioms case3333

theorem case1287 : checkNat 1287 = true := by native_decide
#print axioms case1287

theorem case1289 : checkNat 1289 = true := by native_decide
#print axioms case1289

theorem case3337 : checkNat 3337 = true := by
  apply check_of_normalize (Case.ofNat 3337)
  have he : (Case.ofNat 3337).normalize = Case.ofNat 1289 := by decide
  rw [he]
  exact case1289
#print axioms case3337

theorem case1291 : checkNat 1291 = true := by native_decide
#print axioms case1291

theorem case1293 : checkNat 1293 = true := by native_decide
#print axioms case1293

theorem case3341 : checkNat 3341 = true := by
  apply check_of_normalize (Case.ofNat 3341)
  have he : (Case.ofNat 3341).normalize = Case.ofNat 1293 := by decide
  rw [he]
  exact case1293
#print axioms case3341

theorem case1295 : checkNat 1295 = true := by native_decide
#print axioms case1295

theorem case1297 : checkNat 1297 = true := by native_decide
#print axioms case1297

theorem case3345 : checkNat 3345 = true := by
  apply check_of_normalize (Case.ofNat 3345)
  have he : (Case.ofNat 3345).normalize = Case.ofNat 1297 := by decide
  rw [he]
  exact case1297
#print axioms case3345

theorem case1299 : checkNat 1299 = true := by native_decide
#print axioms case1299

theorem case1301 : checkNat 1301 = true := by native_decide
#print axioms case1301

theorem case3349 : checkNat 3349 = true := by
  apply check_of_normalize (Case.ofNat 3349)
  have he : (Case.ofNat 3349).normalize = Case.ofNat 1301 := by decide
  rw [he]
  exact case1301
#print axioms case3349

theorem case1303 : checkNat 1303 = true := by native_decide
#print axioms case1303

theorem case1305 : checkNat 1305 = true := by native_decide
#print axioms case1305

theorem case3353 : checkNat 3353 = true := by
  apply check_of_normalize (Case.ofNat 3353)
  have he : (Case.ofNat 3353).normalize = Case.ofNat 1305 := by decide
  rw [he]
  exact case1305
#print axioms case3353

theorem case1307 : checkNat 1307 = true := by native_decide
#print axioms case1307

theorem case1309 : checkNat 1309 = true := by native_decide
#print axioms case1309

theorem case3357 : checkNat 3357 = true := by
  apply check_of_normalize (Case.ofNat 3357)
  have he : (Case.ofNat 3357).normalize = Case.ofNat 1309 := by decide
  rw [he]
  exact case1309
#print axioms case3357

theorem case1311 : checkNat 1311 = true := by native_decide
#print axioms case1311

theorem case1313 : checkNat 1313 = true := by native_decide
#print axioms case1313

theorem case3361 : checkNat 3361 = true := by
  apply check_of_normalize (Case.ofNat 3361)
  have he : (Case.ofNat 3361).normalize = Case.ofNat 1313 := by decide
  rw [he]
  exact case1313
#print axioms case3361

theorem case1315 : checkNat 1315 = true := by native_decide
#print axioms case1315

theorem case1317 : checkNat 1317 = true := by native_decide
#print axioms case1317

theorem case3365 : checkNat 3365 = true := by
  apply check_of_normalize (Case.ofNat 3365)
  have he : (Case.ofNat 3365).normalize = Case.ofNat 1317 := by decide
  rw [he]
  exact case1317
#print axioms case3365

theorem case1319 : checkNat 1319 = true := by native_decide
#print axioms case1319

theorem case1321 : checkNat 1321 = true := by native_decide
#print axioms case1321

theorem case3369 : checkNat 3369 = true := by
  apply check_of_normalize (Case.ofNat 3369)
  have he : (Case.ofNat 3369).normalize = Case.ofNat 1321 := by decide
  rw [he]
  exact case1321
#print axioms case3369

theorem case1323 : checkNat 1323 = true := by native_decide
#print axioms case1323

theorem case1325 : checkNat 1325 = true := by native_decide
#print axioms case1325

theorem case3373 : checkNat 3373 = true := by
  apply check_of_normalize (Case.ofNat 3373)
  have he : (Case.ofNat 3373).normalize = Case.ofNat 1325 := by decide
  rw [he]
  exact case1325
#print axioms case3373

theorem case1327 : checkNat 1327 = true := by native_decide
#print axioms case1327

theorem case1329 : checkNat 1329 = true := by native_decide
#print axioms case1329

theorem case3377 : checkNat 3377 = true := by
  apply check_of_normalize (Case.ofNat 3377)
  have he : (Case.ofNat 3377).normalize = Case.ofNat 1329 := by decide
  rw [he]
  exact case1329
#print axioms case3377

theorem case1331 : checkNat 1331 = true := by native_decide
#print axioms case1331

theorem case1333 : checkNat 1333 = true := by native_decide
#print axioms case1333

theorem case3381 : checkNat 3381 = true := by
  apply check_of_normalize (Case.ofNat 3381)
  have he : (Case.ofNat 3381).normalize = Case.ofNat 1333 := by decide
  rw [he]
  exact case1333
#print axioms case3381

theorem case1335 : checkNat 1335 = true := by native_decide
#print axioms case1335

theorem case1337 : checkNat 1337 = true := by native_decide
#print axioms case1337

theorem case3385 : checkNat 3385 = true := by
  apply check_of_normalize (Case.ofNat 3385)
  have he : (Case.ofNat 3385).normalize = Case.ofNat 1337 := by decide
  rw [he]
  exact case1337
#print axioms case3385

theorem case1339 : checkNat 1339 = true := by native_decide
#print axioms case1339

theorem case1341 : checkNat 1341 = true := by native_decide
#print axioms case1341

theorem case3389 : checkNat 3389 = true := by
  apply check_of_normalize (Case.ofNat 3389)
  have he : (Case.ofNat 3389).normalize = Case.ofNat 1341 := by decide
  rw [he]
  exact case1341
#print axioms case3389

theorem case1343 : checkNat 1343 = true := by native_decide
#print axioms case1343

theorem accepted :
    checkNat 1281 = true ∧
    checkNat 1283 = true ∧
    checkNat 1285 = true ∧
    checkNat 1287 = true ∧
    checkNat 1289 = true ∧
    checkNat 1291 = true ∧
    checkNat 1293 = true ∧
    checkNat 1295 = true ∧
    checkNat 1297 = true ∧
    checkNat 1299 = true ∧
    checkNat 1301 = true ∧
    checkNat 1303 = true ∧
    checkNat 1305 = true ∧
    checkNat 1307 = true ∧
    checkNat 1309 = true ∧
    checkNat 1311 = true ∧
    checkNat 1313 = true ∧
    checkNat 1315 = true ∧
    checkNat 1317 = true ∧
    checkNat 1319 = true ∧
    checkNat 1321 = true ∧
    checkNat 1323 = true ∧
    checkNat 1325 = true ∧
    checkNat 1327 = true ∧
    checkNat 1329 = true ∧
    checkNat 1331 = true ∧
    checkNat 1333 = true ∧
    checkNat 1335 = true ∧
    checkNat 1337 = true ∧
    checkNat 1339 = true ∧
    checkNat 1341 = true ∧
    checkNat 1343 = true ∧
    checkNat 3329 = true ∧
    checkNat 3333 = true ∧
    checkNat 3337 = true ∧
    checkNat 3341 = true ∧
    checkNat 3345 = true ∧
    checkNat 3349 = true ∧
    checkNat 3353 = true ∧
    checkNat 3357 = true ∧
    checkNat 3361 = true ∧
    checkNat 3365 = true ∧
    checkNat 3369 = true ∧
    checkNat 3373 = true ∧
    checkNat 3377 = true ∧
    checkNat 3381 = true ∧
    checkNat 3385 = true ∧
    checkNat 3389 = true := by
  exact ⟨case1281, case1283, case1285, case1287, case1289, case1291, case1293, case1295, case1297, case1299, case1301, case1303, case1305, case1307, case1309, case1311, case1313, case1315, case1317, case1319, case1321, case1323, case1325, case1327, case1329, case1331, case1333, case1335, case1337, case1339, case1341, case1343, case3329, case3333, case3337, case3341, case3345, case3349, case3353, case3357, case3361, case3365, case3369, case3373, case3377, case3381, case3385, case3389⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1152
