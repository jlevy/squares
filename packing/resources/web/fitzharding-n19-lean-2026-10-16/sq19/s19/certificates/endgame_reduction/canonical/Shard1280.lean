import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1280
open Sq19.Endgame.Reduction

theorem case1537 : checkNat 1537 = true := by native_decide
#print axioms case1537

theorem case3585 : checkNat 3585 = true := by
  apply check_of_normalize (Case.ofNat 3585)
  have he : (Case.ofNat 3585).normalize = Case.ofNat 1537 := by decide
  rw [he]
  exact case1537
#print axioms case3585

theorem case1539 : checkNat 1539 = true := by native_decide
#print axioms case1539

theorem case1541 : checkNat 1541 = true := by native_decide
#print axioms case1541

theorem case3589 : checkNat 3589 = true := by
  apply check_of_normalize (Case.ofNat 3589)
  have he : (Case.ofNat 3589).normalize = Case.ofNat 1541 := by decide
  rw [he]
  exact case1541
#print axioms case3589

theorem case1543 : checkNat 1543 = true := by native_decide
#print axioms case1543

theorem case1545 : checkNat 1545 = true := by native_decide
#print axioms case1545

theorem case3593 : checkNat 3593 = true := by
  apply check_of_normalize (Case.ofNat 3593)
  have he : (Case.ofNat 3593).normalize = Case.ofNat 1545 := by decide
  rw [he]
  exact case1545
#print axioms case3593

theorem case1547 : checkNat 1547 = true := by native_decide
#print axioms case1547

theorem case1549 : checkNat 1549 = true := by native_decide
#print axioms case1549

theorem case3597 : checkNat 3597 = true := by
  apply check_of_normalize (Case.ofNat 3597)
  have he : (Case.ofNat 3597).normalize = Case.ofNat 1549 := by decide
  rw [he]
  exact case1549
#print axioms case3597

theorem case1551 : checkNat 1551 = true := by native_decide
#print axioms case1551

theorem case1553 : checkNat 1553 = true := by native_decide
#print axioms case1553

theorem case3601 : checkNat 3601 = true := by
  apply check_of_normalize (Case.ofNat 3601)
  have he : (Case.ofNat 3601).normalize = Case.ofNat 1553 := by decide
  rw [he]
  exact case1553
#print axioms case3601

theorem case1555 : checkNat 1555 = true := by native_decide
#print axioms case1555

theorem case1557 : checkNat 1557 = true := by native_decide
#print axioms case1557

theorem case3605 : checkNat 3605 = true := by
  apply check_of_normalize (Case.ofNat 3605)
  have he : (Case.ofNat 3605).normalize = Case.ofNat 1557 := by decide
  rw [he]
  exact case1557
#print axioms case3605

theorem case1559 : checkNat 1559 = true := by native_decide
#print axioms case1559

theorem case1561 : checkNat 1561 = true := by native_decide
#print axioms case1561

theorem case3609 : checkNat 3609 = true := by
  apply check_of_normalize (Case.ofNat 3609)
  have he : (Case.ofNat 3609).normalize = Case.ofNat 1561 := by decide
  rw [he]
  exact case1561
#print axioms case3609

theorem case1563 : checkNat 1563 = true := by native_decide
#print axioms case1563

theorem case1565 : checkNat 1565 = true := by native_decide
#print axioms case1565

theorem case3613 : checkNat 3613 = true := by
  apply check_of_normalize (Case.ofNat 3613)
  have he : (Case.ofNat 3613).normalize = Case.ofNat 1565 := by decide
  rw [he]
  exact case1565
#print axioms case3613

theorem case1567 : checkNat 1567 = true := by native_decide
#print axioms case1567

theorem case1569 : checkNat 1569 = true := by native_decide
#print axioms case1569

theorem case3617 : checkNat 3617 = true := by
  apply check_of_normalize (Case.ofNat 3617)
  have he : (Case.ofNat 3617).normalize = Case.ofNat 1569 := by decide
  rw [he]
  exact case1569
#print axioms case3617

theorem case1571 : checkNat 1571 = true := by native_decide
#print axioms case1571

theorem case1573 : checkNat 1573 = true := by native_decide
#print axioms case1573

theorem case3621 : checkNat 3621 = true := by
  apply check_of_normalize (Case.ofNat 3621)
  have he : (Case.ofNat 3621).normalize = Case.ofNat 1573 := by decide
  rw [he]
  exact case1573
#print axioms case3621

theorem case1575 : checkNat 1575 = true := by native_decide
#print axioms case1575

theorem case1577 : checkNat 1577 = true := by native_decide
#print axioms case1577

theorem case3625 : checkNat 3625 = true := by
  apply check_of_normalize (Case.ofNat 3625)
  have he : (Case.ofNat 3625).normalize = Case.ofNat 1577 := by decide
  rw [he]
  exact case1577
#print axioms case3625

theorem case1579 : checkNat 1579 = true := by native_decide
#print axioms case1579

theorem case1581 : checkNat 1581 = true := by native_decide
#print axioms case1581

theorem case3629 : checkNat 3629 = true := by
  apply check_of_normalize (Case.ofNat 3629)
  have he : (Case.ofNat 3629).normalize = Case.ofNat 1581 := by decide
  rw [he]
  exact case1581
#print axioms case3629

theorem case1583 : checkNat 1583 = true := by native_decide
#print axioms case1583

theorem case1585 : checkNat 1585 = true := by native_decide
#print axioms case1585

theorem case3633 : checkNat 3633 = true := by
  apply check_of_normalize (Case.ofNat 3633)
  have he : (Case.ofNat 3633).normalize = Case.ofNat 1585 := by decide
  rw [he]
  exact case1585
#print axioms case3633

theorem case1587 : checkNat 1587 = true := by native_decide
#print axioms case1587

theorem case1589 : checkNat 1589 = true := by native_decide
#print axioms case1589

theorem case3637 : checkNat 3637 = true := by
  apply check_of_normalize (Case.ofNat 3637)
  have he : (Case.ofNat 3637).normalize = Case.ofNat 1589 := by decide
  rw [he]
  exact case1589
#print axioms case3637

theorem case1591 : checkNat 1591 = true := by native_decide
#print axioms case1591

theorem case1593 : checkNat 1593 = true := by native_decide
#print axioms case1593

theorem case3641 : checkNat 3641 = true := by
  apply check_of_normalize (Case.ofNat 3641)
  have he : (Case.ofNat 3641).normalize = Case.ofNat 1593 := by decide
  rw [he]
  exact case1593
#print axioms case3641

theorem case1595 : checkNat 1595 = true := by native_decide
#print axioms case1595

theorem case1597 : checkNat 1597 = true := by native_decide
#print axioms case1597

theorem case3645 : checkNat 3645 = true := by
  apply check_of_normalize (Case.ofNat 3645)
  have he : (Case.ofNat 3645).normalize = Case.ofNat 1597 := by decide
  rw [he]
  exact case1597
#print axioms case3645

theorem case1599 : checkNat 1599 = true := by native_decide
#print axioms case1599

theorem accepted :
    checkNat 1537 = true ∧
    checkNat 1539 = true ∧
    checkNat 1541 = true ∧
    checkNat 1543 = true ∧
    checkNat 1545 = true ∧
    checkNat 1547 = true ∧
    checkNat 1549 = true ∧
    checkNat 1551 = true ∧
    checkNat 1553 = true ∧
    checkNat 1555 = true ∧
    checkNat 1557 = true ∧
    checkNat 1559 = true ∧
    checkNat 1561 = true ∧
    checkNat 1563 = true ∧
    checkNat 1565 = true ∧
    checkNat 1567 = true ∧
    checkNat 1569 = true ∧
    checkNat 1571 = true ∧
    checkNat 1573 = true ∧
    checkNat 1575 = true ∧
    checkNat 1577 = true ∧
    checkNat 1579 = true ∧
    checkNat 1581 = true ∧
    checkNat 1583 = true ∧
    checkNat 1585 = true ∧
    checkNat 1587 = true ∧
    checkNat 1589 = true ∧
    checkNat 1591 = true ∧
    checkNat 1593 = true ∧
    checkNat 1595 = true ∧
    checkNat 1597 = true ∧
    checkNat 1599 = true ∧
    checkNat 3585 = true ∧
    checkNat 3589 = true ∧
    checkNat 3593 = true ∧
    checkNat 3597 = true ∧
    checkNat 3601 = true ∧
    checkNat 3605 = true ∧
    checkNat 3609 = true ∧
    checkNat 3613 = true ∧
    checkNat 3617 = true ∧
    checkNat 3621 = true ∧
    checkNat 3625 = true ∧
    checkNat 3629 = true ∧
    checkNat 3633 = true ∧
    checkNat 3637 = true ∧
    checkNat 3641 = true ∧
    checkNat 3645 = true := by
  exact ⟨case1537, case1539, case1541, case1543, case1545, case1547, case1549, case1551, case1553, case1555, case1557, case1559, case1561, case1563, case1565, case1567, case1569, case1571, case1573, case1575, case1577, case1579, case1581, case1583, case1585, case1587, case1589, case1591, case1593, case1595, case1597, case1599, case3585, case3589, case3593, case3597, case3601, case3605, case3609, case3613, case3617, case3621, case3625, case3629, case3633, case3637, case3641, case3645⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1280
