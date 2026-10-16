import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1184
open Sq19.Endgame.Reduction

theorem case1345 : checkNat 1345 = true := by native_decide
#print axioms case1345

theorem case3393 : checkNat 3393 = true := by
  apply check_of_normalize (Case.ofNat 3393)
  have he : (Case.ofNat 3393).normalize = Case.ofNat 1345 := by decide
  rw [he]
  exact case1345
#print axioms case3393

theorem case1347 : checkNat 1347 = true := by native_decide
#print axioms case1347

theorem case1349 : checkNat 1349 = true := by native_decide
#print axioms case1349

theorem case3397 : checkNat 3397 = true := by
  apply check_of_normalize (Case.ofNat 3397)
  have he : (Case.ofNat 3397).normalize = Case.ofNat 1349 := by decide
  rw [he]
  exact case1349
#print axioms case3397

theorem case1351 : checkNat 1351 = true := by native_decide
#print axioms case1351

theorem case1353 : checkNat 1353 = true := by native_decide
#print axioms case1353

theorem case3401 : checkNat 3401 = true := by
  apply check_of_normalize (Case.ofNat 3401)
  have he : (Case.ofNat 3401).normalize = Case.ofNat 1353 := by decide
  rw [he]
  exact case1353
#print axioms case3401

theorem case1355 : checkNat 1355 = true := by native_decide
#print axioms case1355

theorem case1357 : checkNat 1357 = true := by native_decide
#print axioms case1357

theorem case3405 : checkNat 3405 = true := by
  apply check_of_normalize (Case.ofNat 3405)
  have he : (Case.ofNat 3405).normalize = Case.ofNat 1357 := by decide
  rw [he]
  exact case1357
#print axioms case3405

theorem case1359 : checkNat 1359 = true := by native_decide
#print axioms case1359

theorem case1361 : checkNat 1361 = true := by native_decide
#print axioms case1361

theorem case3409 : checkNat 3409 = true := by
  apply check_of_normalize (Case.ofNat 3409)
  have he : (Case.ofNat 3409).normalize = Case.ofNat 1361 := by decide
  rw [he]
  exact case1361
#print axioms case3409

theorem case1363 : checkNat 1363 = true := by native_decide
#print axioms case1363

theorem case1365 : checkNat 1365 = true := by native_decide
#print axioms case1365

theorem case3413 : checkNat 3413 = true := by
  apply check_of_normalize (Case.ofNat 3413)
  have he : (Case.ofNat 3413).normalize = Case.ofNat 1365 := by decide
  rw [he]
  exact case1365
#print axioms case3413

theorem case1367 : checkNat 1367 = true := by native_decide
#print axioms case1367

theorem case1369 : checkNat 1369 = true := by native_decide
#print axioms case1369

theorem case3417 : checkNat 3417 = true := by
  apply check_of_normalize (Case.ofNat 3417)
  have he : (Case.ofNat 3417).normalize = Case.ofNat 1369 := by decide
  rw [he]
  exact case1369
#print axioms case3417

theorem case1371 : checkNat 1371 = true := by native_decide
#print axioms case1371

theorem case1373 : checkNat 1373 = true := by native_decide
#print axioms case1373

theorem case3421 : checkNat 3421 = true := by
  apply check_of_normalize (Case.ofNat 3421)
  have he : (Case.ofNat 3421).normalize = Case.ofNat 1373 := by decide
  rw [he]
  exact case1373
#print axioms case3421

theorem case1375 : checkNat 1375 = true := by native_decide
#print axioms case1375

theorem case1377 : checkNat 1377 = true := by native_decide
#print axioms case1377

theorem case3425 : checkNat 3425 = true := by
  apply check_of_normalize (Case.ofNat 3425)
  have he : (Case.ofNat 3425).normalize = Case.ofNat 1377 := by decide
  rw [he]
  exact case1377
#print axioms case3425

theorem case1379 : checkNat 1379 = true := by native_decide
#print axioms case1379

theorem case1381 : checkNat 1381 = true := by native_decide
#print axioms case1381

theorem case3429 : checkNat 3429 = true := by
  apply check_of_normalize (Case.ofNat 3429)
  have he : (Case.ofNat 3429).normalize = Case.ofNat 1381 := by decide
  rw [he]
  exact case1381
#print axioms case3429

theorem case1383 : checkNat 1383 = true := by native_decide
#print axioms case1383

theorem case1385 : checkNat 1385 = true := by native_decide
#print axioms case1385

theorem case3433 : checkNat 3433 = true := by
  apply check_of_normalize (Case.ofNat 3433)
  have he : (Case.ofNat 3433).normalize = Case.ofNat 1385 := by decide
  rw [he]
  exact case1385
#print axioms case3433

theorem case1387 : checkNat 1387 = true := by native_decide
#print axioms case1387

theorem case1389 : checkNat 1389 = true := by native_decide
#print axioms case1389

theorem case3437 : checkNat 3437 = true := by
  apply check_of_normalize (Case.ofNat 3437)
  have he : (Case.ofNat 3437).normalize = Case.ofNat 1389 := by decide
  rw [he]
  exact case1389
#print axioms case3437

theorem case1391 : checkNat 1391 = true := by native_decide
#print axioms case1391

theorem case1393 : checkNat 1393 = true := by native_decide
#print axioms case1393

theorem case3441 : checkNat 3441 = true := by
  apply check_of_normalize (Case.ofNat 3441)
  have he : (Case.ofNat 3441).normalize = Case.ofNat 1393 := by decide
  rw [he]
  exact case1393
#print axioms case3441

theorem case1395 : checkNat 1395 = true := by native_decide
#print axioms case1395

theorem case1397 : checkNat 1397 = true := by native_decide
#print axioms case1397

theorem case3445 : checkNat 3445 = true := by
  apply check_of_normalize (Case.ofNat 3445)
  have he : (Case.ofNat 3445).normalize = Case.ofNat 1397 := by decide
  rw [he]
  exact case1397
#print axioms case3445

theorem case1399 : checkNat 1399 = true := by native_decide
#print axioms case1399

theorem case1401 : checkNat 1401 = true := by native_decide
#print axioms case1401

theorem case3449 : checkNat 3449 = true := by
  apply check_of_normalize (Case.ofNat 3449)
  have he : (Case.ofNat 3449).normalize = Case.ofNat 1401 := by decide
  rw [he]
  exact case1401
#print axioms case3449

theorem case1403 : checkNat 1403 = true := by native_decide
#print axioms case1403

theorem case1405 : checkNat 1405 = true := by native_decide
#print axioms case1405

theorem case3453 : checkNat 3453 = true := by
  apply check_of_normalize (Case.ofNat 3453)
  have he : (Case.ofNat 3453).normalize = Case.ofNat 1405 := by decide
  rw [he]
  exact case1405
#print axioms case3453

theorem case1407 : checkNat 1407 = true := by native_decide
#print axioms case1407

theorem accepted :
    checkNat 1345 = true ∧
    checkNat 1347 = true ∧
    checkNat 1349 = true ∧
    checkNat 1351 = true ∧
    checkNat 1353 = true ∧
    checkNat 1355 = true ∧
    checkNat 1357 = true ∧
    checkNat 1359 = true ∧
    checkNat 1361 = true ∧
    checkNat 1363 = true ∧
    checkNat 1365 = true ∧
    checkNat 1367 = true ∧
    checkNat 1369 = true ∧
    checkNat 1371 = true ∧
    checkNat 1373 = true ∧
    checkNat 1375 = true ∧
    checkNat 1377 = true ∧
    checkNat 1379 = true ∧
    checkNat 1381 = true ∧
    checkNat 1383 = true ∧
    checkNat 1385 = true ∧
    checkNat 1387 = true ∧
    checkNat 1389 = true ∧
    checkNat 1391 = true ∧
    checkNat 1393 = true ∧
    checkNat 1395 = true ∧
    checkNat 1397 = true ∧
    checkNat 1399 = true ∧
    checkNat 1401 = true ∧
    checkNat 1403 = true ∧
    checkNat 1405 = true ∧
    checkNat 1407 = true ∧
    checkNat 3393 = true ∧
    checkNat 3397 = true ∧
    checkNat 3401 = true ∧
    checkNat 3405 = true ∧
    checkNat 3409 = true ∧
    checkNat 3413 = true ∧
    checkNat 3417 = true ∧
    checkNat 3421 = true ∧
    checkNat 3425 = true ∧
    checkNat 3429 = true ∧
    checkNat 3433 = true ∧
    checkNat 3437 = true ∧
    checkNat 3441 = true ∧
    checkNat 3445 = true ∧
    checkNat 3449 = true ∧
    checkNat 3453 = true := by
  exact ⟨case1345, case1347, case1349, case1351, case1353, case1355, case1357, case1359, case1361, case1363, case1365, case1367, case1369, case1371, case1373, case1375, case1377, case1379, case1381, case1383, case1385, case1387, case1389, case1391, case1393, case1395, case1397, case1399, case1401, case1403, case1405, case1407, case3393, case3397, case3401, case3405, case3409, case3413, case3417, case3421, case3425, case3429, case3433, case3437, case3441, case3445, case3449, case3453⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1184
