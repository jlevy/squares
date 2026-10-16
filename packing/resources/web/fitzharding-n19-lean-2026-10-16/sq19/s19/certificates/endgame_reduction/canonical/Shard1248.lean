import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1248
open Sq19.Endgame.Reduction

theorem case1473 : checkNat 1473 = true := by native_decide
#print axioms case1473

theorem case3521 : checkNat 3521 = true := by
  apply check_of_normalize (Case.ofNat 3521)
  have he : (Case.ofNat 3521).normalize = Case.ofNat 1473 := by decide
  rw [he]
  exact case1473
#print axioms case3521

theorem case1475 : checkNat 1475 = true := by native_decide
#print axioms case1475

theorem case1477 : checkNat 1477 = true := by native_decide
#print axioms case1477

theorem case3525 : checkNat 3525 = true := by
  apply check_of_normalize (Case.ofNat 3525)
  have he : (Case.ofNat 3525).normalize = Case.ofNat 1477 := by decide
  rw [he]
  exact case1477
#print axioms case3525

theorem case1479 : checkNat 1479 = true := by native_decide
#print axioms case1479

theorem case1481 : checkNat 1481 = true := by native_decide
#print axioms case1481

theorem case3529 : checkNat 3529 = true := by
  apply check_of_normalize (Case.ofNat 3529)
  have he : (Case.ofNat 3529).normalize = Case.ofNat 1481 := by decide
  rw [he]
  exact case1481
#print axioms case3529

theorem case1483 : checkNat 1483 = true := by native_decide
#print axioms case1483

theorem case1485 : checkNat 1485 = true := by native_decide
#print axioms case1485

theorem case3533 : checkNat 3533 = true := by
  apply check_of_normalize (Case.ofNat 3533)
  have he : (Case.ofNat 3533).normalize = Case.ofNat 1485 := by decide
  rw [he]
  exact case1485
#print axioms case3533

theorem case1487 : checkNat 1487 = true := by native_decide
#print axioms case1487

theorem case1489 : checkNat 1489 = true := by native_decide
#print axioms case1489

theorem case3537 : checkNat 3537 = true := by
  apply check_of_normalize (Case.ofNat 3537)
  have he : (Case.ofNat 3537).normalize = Case.ofNat 1489 := by decide
  rw [he]
  exact case1489
#print axioms case3537

theorem case1491 : checkNat 1491 = true := by native_decide
#print axioms case1491

theorem case1493 : checkNat 1493 = true := by native_decide
#print axioms case1493

theorem case3541 : checkNat 3541 = true := by
  apply check_of_normalize (Case.ofNat 3541)
  have he : (Case.ofNat 3541).normalize = Case.ofNat 1493 := by decide
  rw [he]
  exact case1493
#print axioms case3541

theorem case1495 : checkNat 1495 = true := by native_decide
#print axioms case1495

theorem case1497 : checkNat 1497 = true := by native_decide
#print axioms case1497

theorem case3545 : checkNat 3545 = true := by
  apply check_of_normalize (Case.ofNat 3545)
  have he : (Case.ofNat 3545).normalize = Case.ofNat 1497 := by decide
  rw [he]
  exact case1497
#print axioms case3545

theorem case1499 : checkNat 1499 = true := by native_decide
#print axioms case1499

theorem case1501 : checkNat 1501 = true := by native_decide
#print axioms case1501

theorem case3549 : checkNat 3549 = true := by
  apply check_of_normalize (Case.ofNat 3549)
  have he : (Case.ofNat 3549).normalize = Case.ofNat 1501 := by decide
  rw [he]
  exact case1501
#print axioms case3549

theorem case1503 : checkNat 1503 = true := by native_decide
#print axioms case1503

theorem case1505 : checkNat 1505 = true := by native_decide
#print axioms case1505

theorem case3553 : checkNat 3553 = true := by
  apply check_of_normalize (Case.ofNat 3553)
  have he : (Case.ofNat 3553).normalize = Case.ofNat 1505 := by decide
  rw [he]
  exact case1505
#print axioms case3553

theorem case1507 : checkNat 1507 = true := by native_decide
#print axioms case1507

theorem case1509 : checkNat 1509 = true := by native_decide
#print axioms case1509

theorem case3557 : checkNat 3557 = true := by
  apply check_of_normalize (Case.ofNat 3557)
  have he : (Case.ofNat 3557).normalize = Case.ofNat 1509 := by decide
  rw [he]
  exact case1509
#print axioms case3557

theorem case1511 : checkNat 1511 = true := by native_decide
#print axioms case1511

theorem case1513 : checkNat 1513 = true := by native_decide
#print axioms case1513

theorem case3561 : checkNat 3561 = true := by
  apply check_of_normalize (Case.ofNat 3561)
  have he : (Case.ofNat 3561).normalize = Case.ofNat 1513 := by decide
  rw [he]
  exact case1513
#print axioms case3561

theorem case1515 : checkNat 1515 = true := by native_decide
#print axioms case1515

theorem case1517 : checkNat 1517 = true := by native_decide
#print axioms case1517

theorem case3565 : checkNat 3565 = true := by
  apply check_of_normalize (Case.ofNat 3565)
  have he : (Case.ofNat 3565).normalize = Case.ofNat 1517 := by decide
  rw [he]
  exact case1517
#print axioms case3565

theorem case1519 : checkNat 1519 = true := by native_decide
#print axioms case1519

theorem case1521 : checkNat 1521 = true := by native_decide
#print axioms case1521

theorem case3569 : checkNat 3569 = true := by
  apply check_of_normalize (Case.ofNat 3569)
  have he : (Case.ofNat 3569).normalize = Case.ofNat 1521 := by decide
  rw [he]
  exact case1521
#print axioms case3569

theorem case1523 : checkNat 1523 = true := by native_decide
#print axioms case1523

theorem case1525 : checkNat 1525 = true := by native_decide
#print axioms case1525

theorem case3573 : checkNat 3573 = true := by
  apply check_of_normalize (Case.ofNat 3573)
  have he : (Case.ofNat 3573).normalize = Case.ofNat 1525 := by decide
  rw [he]
  exact case1525
#print axioms case3573

theorem case1527 : checkNat 1527 = true := by native_decide
#print axioms case1527

theorem case1529 : checkNat 1529 = true := by native_decide
#print axioms case1529

theorem case3577 : checkNat 3577 = true := by
  apply check_of_normalize (Case.ofNat 3577)
  have he : (Case.ofNat 3577).normalize = Case.ofNat 1529 := by decide
  rw [he]
  exact case1529
#print axioms case3577

theorem case1531 : checkNat 1531 = true := by native_decide
#print axioms case1531

theorem case1533 : checkNat 1533 = true := by native_decide
#print axioms case1533

theorem case3581 : checkNat 3581 = true := by
  apply check_of_normalize (Case.ofNat 3581)
  have he : (Case.ofNat 3581).normalize = Case.ofNat 1533 := by decide
  rw [he]
  exact case1533
#print axioms case3581

theorem case1535 : checkNat 1535 = true := by native_decide
#print axioms case1535

theorem accepted :
    checkNat 1473 = true ∧
    checkNat 1475 = true ∧
    checkNat 1477 = true ∧
    checkNat 1479 = true ∧
    checkNat 1481 = true ∧
    checkNat 1483 = true ∧
    checkNat 1485 = true ∧
    checkNat 1487 = true ∧
    checkNat 1489 = true ∧
    checkNat 1491 = true ∧
    checkNat 1493 = true ∧
    checkNat 1495 = true ∧
    checkNat 1497 = true ∧
    checkNat 1499 = true ∧
    checkNat 1501 = true ∧
    checkNat 1503 = true ∧
    checkNat 1505 = true ∧
    checkNat 1507 = true ∧
    checkNat 1509 = true ∧
    checkNat 1511 = true ∧
    checkNat 1513 = true ∧
    checkNat 1515 = true ∧
    checkNat 1517 = true ∧
    checkNat 1519 = true ∧
    checkNat 1521 = true ∧
    checkNat 1523 = true ∧
    checkNat 1525 = true ∧
    checkNat 1527 = true ∧
    checkNat 1529 = true ∧
    checkNat 1531 = true ∧
    checkNat 1533 = true ∧
    checkNat 1535 = true ∧
    checkNat 3521 = true ∧
    checkNat 3525 = true ∧
    checkNat 3529 = true ∧
    checkNat 3533 = true ∧
    checkNat 3537 = true ∧
    checkNat 3541 = true ∧
    checkNat 3545 = true ∧
    checkNat 3549 = true ∧
    checkNat 3553 = true ∧
    checkNat 3557 = true ∧
    checkNat 3561 = true ∧
    checkNat 3565 = true ∧
    checkNat 3569 = true ∧
    checkNat 3573 = true ∧
    checkNat 3577 = true ∧
    checkNat 3581 = true := by
  exact ⟨case1473, case1475, case1477, case1479, case1481, case1483, case1485, case1487, case1489, case1491, case1493, case1495, case1497, case1499, case1501, case1503, case1505, case1507, case1509, case1511, case1513, case1515, case1517, case1519, case1521, case1523, case1525, case1527, case1529, case1531, case1533, case1535, case3521, case3525, case3529, case3533, case3537, case3541, case3545, case3549, case3553, case3557, case3561, case3565, case3569, case3573, case3577, case3581⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1248
