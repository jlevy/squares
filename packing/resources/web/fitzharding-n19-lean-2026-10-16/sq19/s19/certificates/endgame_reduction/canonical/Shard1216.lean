import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1216
open Sq19.Endgame.Reduction

theorem case1409 : checkNat 1409 = true := by native_decide
#print axioms case1409

theorem case3457 : checkNat 3457 = true := by
  apply check_of_normalize (Case.ofNat 3457)
  have he : (Case.ofNat 3457).normalize = Case.ofNat 1409 := by decide
  rw [he]
  exact case1409
#print axioms case3457

theorem case1411 : checkNat 1411 = true := by native_decide
#print axioms case1411

theorem case1413 : checkNat 1413 = true := by native_decide
#print axioms case1413

theorem case3461 : checkNat 3461 = true := by
  apply check_of_normalize (Case.ofNat 3461)
  have he : (Case.ofNat 3461).normalize = Case.ofNat 1413 := by decide
  rw [he]
  exact case1413
#print axioms case3461

theorem case1415 : checkNat 1415 = true := by native_decide
#print axioms case1415

theorem case1417 : checkNat 1417 = true := by native_decide
#print axioms case1417

theorem case3465 : checkNat 3465 = true := by
  apply check_of_normalize (Case.ofNat 3465)
  have he : (Case.ofNat 3465).normalize = Case.ofNat 1417 := by decide
  rw [he]
  exact case1417
#print axioms case3465

theorem case1419 : checkNat 1419 = true := by native_decide
#print axioms case1419

theorem case1421 : checkNat 1421 = true := by native_decide
#print axioms case1421

theorem case3469 : checkNat 3469 = true := by
  apply check_of_normalize (Case.ofNat 3469)
  have he : (Case.ofNat 3469).normalize = Case.ofNat 1421 := by decide
  rw [he]
  exact case1421
#print axioms case3469

theorem case1423 : checkNat 1423 = true := by native_decide
#print axioms case1423

theorem case1425 : checkNat 1425 = true := by native_decide
#print axioms case1425

theorem case3473 : checkNat 3473 = true := by
  apply check_of_normalize (Case.ofNat 3473)
  have he : (Case.ofNat 3473).normalize = Case.ofNat 1425 := by decide
  rw [he]
  exact case1425
#print axioms case3473

theorem case1427 : checkNat 1427 = true := by native_decide
#print axioms case1427

theorem case1429 : checkNat 1429 = true := by native_decide
#print axioms case1429

theorem case3477 : checkNat 3477 = true := by
  apply check_of_normalize (Case.ofNat 3477)
  have he : (Case.ofNat 3477).normalize = Case.ofNat 1429 := by decide
  rw [he]
  exact case1429
#print axioms case3477

theorem case1431 : checkNat 1431 = true := by native_decide
#print axioms case1431

theorem case1433 : checkNat 1433 = true := by native_decide
#print axioms case1433

theorem case3481 : checkNat 3481 = true := by
  apply check_of_normalize (Case.ofNat 3481)
  have he : (Case.ofNat 3481).normalize = Case.ofNat 1433 := by decide
  rw [he]
  exact case1433
#print axioms case3481

theorem case1435 : checkNat 1435 = true := by native_decide
#print axioms case1435

theorem case1437 : checkNat 1437 = true := by native_decide
#print axioms case1437

theorem case3485 : checkNat 3485 = true := by
  apply check_of_normalize (Case.ofNat 3485)
  have he : (Case.ofNat 3485).normalize = Case.ofNat 1437 := by decide
  rw [he]
  exact case1437
#print axioms case3485

theorem case1439 : checkNat 1439 = true := by native_decide
#print axioms case1439

theorem case1441 : checkNat 1441 = true := by native_decide
#print axioms case1441

theorem case3489 : checkNat 3489 = true := by
  apply check_of_normalize (Case.ofNat 3489)
  have he : (Case.ofNat 3489).normalize = Case.ofNat 1441 := by decide
  rw [he]
  exact case1441
#print axioms case3489

theorem case1443 : checkNat 1443 = true := by native_decide
#print axioms case1443

theorem case1445 : checkNat 1445 = true := by native_decide
#print axioms case1445

theorem case3493 : checkNat 3493 = true := by
  apply check_of_normalize (Case.ofNat 3493)
  have he : (Case.ofNat 3493).normalize = Case.ofNat 1445 := by decide
  rw [he]
  exact case1445
#print axioms case3493

theorem case1447 : checkNat 1447 = true := by native_decide
#print axioms case1447

theorem case1449 : checkNat 1449 = true := by native_decide
#print axioms case1449

theorem case3497 : checkNat 3497 = true := by
  apply check_of_normalize (Case.ofNat 3497)
  have he : (Case.ofNat 3497).normalize = Case.ofNat 1449 := by decide
  rw [he]
  exact case1449
#print axioms case3497

theorem case1451 : checkNat 1451 = true := by native_decide
#print axioms case1451

theorem case1453 : checkNat 1453 = true := by native_decide
#print axioms case1453

theorem case3501 : checkNat 3501 = true := by
  apply check_of_normalize (Case.ofNat 3501)
  have he : (Case.ofNat 3501).normalize = Case.ofNat 1453 := by decide
  rw [he]
  exact case1453
#print axioms case3501

theorem case1455 : checkNat 1455 = true := by native_decide
#print axioms case1455

theorem case1457 : checkNat 1457 = true := by native_decide
#print axioms case1457

theorem case3505 : checkNat 3505 = true := by
  apply check_of_normalize (Case.ofNat 3505)
  have he : (Case.ofNat 3505).normalize = Case.ofNat 1457 := by decide
  rw [he]
  exact case1457
#print axioms case3505

theorem case1459 : checkNat 1459 = true := by native_decide
#print axioms case1459

theorem case1461 : checkNat 1461 = true := by native_decide
#print axioms case1461

theorem case3509 : checkNat 3509 = true := by
  apply check_of_normalize (Case.ofNat 3509)
  have he : (Case.ofNat 3509).normalize = Case.ofNat 1461 := by decide
  rw [he]
  exact case1461
#print axioms case3509

theorem case1463 : checkNat 1463 = true := by native_decide
#print axioms case1463

theorem case1465 : checkNat 1465 = true := by native_decide
#print axioms case1465

theorem case3513 : checkNat 3513 = true := by
  apply check_of_normalize (Case.ofNat 3513)
  have he : (Case.ofNat 3513).normalize = Case.ofNat 1465 := by decide
  rw [he]
  exact case1465
#print axioms case3513

theorem case1467 : checkNat 1467 = true := by native_decide
#print axioms case1467

theorem case1469 : checkNat 1469 = true := by native_decide
#print axioms case1469

theorem case3517 : checkNat 3517 = true := by
  apply check_of_normalize (Case.ofNat 3517)
  have he : (Case.ofNat 3517).normalize = Case.ofNat 1469 := by decide
  rw [he]
  exact case1469
#print axioms case3517

theorem case1471 : checkNat 1471 = true := by native_decide
#print axioms case1471

theorem accepted :
    checkNat 1409 = true ∧
    checkNat 1411 = true ∧
    checkNat 1413 = true ∧
    checkNat 1415 = true ∧
    checkNat 1417 = true ∧
    checkNat 1419 = true ∧
    checkNat 1421 = true ∧
    checkNat 1423 = true ∧
    checkNat 1425 = true ∧
    checkNat 1427 = true ∧
    checkNat 1429 = true ∧
    checkNat 1431 = true ∧
    checkNat 1433 = true ∧
    checkNat 1435 = true ∧
    checkNat 1437 = true ∧
    checkNat 1439 = true ∧
    checkNat 1441 = true ∧
    checkNat 1443 = true ∧
    checkNat 1445 = true ∧
    checkNat 1447 = true ∧
    checkNat 1449 = true ∧
    checkNat 1451 = true ∧
    checkNat 1453 = true ∧
    checkNat 1455 = true ∧
    checkNat 1457 = true ∧
    checkNat 1459 = true ∧
    checkNat 1461 = true ∧
    checkNat 1463 = true ∧
    checkNat 1465 = true ∧
    checkNat 1467 = true ∧
    checkNat 1469 = true ∧
    checkNat 1471 = true ∧
    checkNat 3457 = true ∧
    checkNat 3461 = true ∧
    checkNat 3465 = true ∧
    checkNat 3469 = true ∧
    checkNat 3473 = true ∧
    checkNat 3477 = true ∧
    checkNat 3481 = true ∧
    checkNat 3485 = true ∧
    checkNat 3489 = true ∧
    checkNat 3493 = true ∧
    checkNat 3497 = true ∧
    checkNat 3501 = true ∧
    checkNat 3505 = true ∧
    checkNat 3509 = true ∧
    checkNat 3513 = true ∧
    checkNat 3517 = true := by
  exact ⟨case1409, case1411, case1413, case1415, case1417, case1419, case1421, case1423, case1425, case1427, case1429, case1431, case1433, case1435, case1437, case1439, case1441, case1443, case1445, case1447, case1449, case1451, case1453, case1455, case1457, case1459, case1461, case1463, case1465, case1467, case1469, case1471, case3457, case3461, case3465, case3469, case3473, case3477, case3481, case3485, case3489, case3493, case3497, case3501, case3505, case3509, case3513, case3517⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1216
