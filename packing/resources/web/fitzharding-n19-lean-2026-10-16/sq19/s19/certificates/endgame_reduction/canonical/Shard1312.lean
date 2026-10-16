import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1312
open Sq19.Endgame.Reduction

theorem case1601 : checkNat 1601 = true := by native_decide
#print axioms case1601

theorem case3649 : checkNat 3649 = true := by
  apply check_of_normalize (Case.ofNat 3649)
  have he : (Case.ofNat 3649).normalize = Case.ofNat 1601 := by decide
  rw [he]
  exact case1601
#print axioms case3649

theorem case1603 : checkNat 1603 = true := by native_decide
#print axioms case1603

theorem case1605 : checkNat 1605 = true := by native_decide
#print axioms case1605

theorem case3653 : checkNat 3653 = true := by
  apply check_of_normalize (Case.ofNat 3653)
  have he : (Case.ofNat 3653).normalize = Case.ofNat 1605 := by decide
  rw [he]
  exact case1605
#print axioms case3653

theorem case1607 : checkNat 1607 = true := by native_decide
#print axioms case1607

theorem case1609 : checkNat 1609 = true := by native_decide
#print axioms case1609

theorem case3657 : checkNat 3657 = true := by
  apply check_of_normalize (Case.ofNat 3657)
  have he : (Case.ofNat 3657).normalize = Case.ofNat 1609 := by decide
  rw [he]
  exact case1609
#print axioms case3657

theorem case1611 : checkNat 1611 = true := by native_decide
#print axioms case1611

theorem case1613 : checkNat 1613 = true := by native_decide
#print axioms case1613

theorem case3661 : checkNat 3661 = true := by
  apply check_of_normalize (Case.ofNat 3661)
  have he : (Case.ofNat 3661).normalize = Case.ofNat 1613 := by decide
  rw [he]
  exact case1613
#print axioms case3661

theorem case1615 : checkNat 1615 = true := by native_decide
#print axioms case1615

theorem case1617 : checkNat 1617 = true := by native_decide
#print axioms case1617

theorem case3665 : checkNat 3665 = true := by
  apply check_of_normalize (Case.ofNat 3665)
  have he : (Case.ofNat 3665).normalize = Case.ofNat 1617 := by decide
  rw [he]
  exact case1617
#print axioms case3665

theorem case1619 : checkNat 1619 = true := by native_decide
#print axioms case1619

theorem case1621 : checkNat 1621 = true := by native_decide
#print axioms case1621

theorem case3669 : checkNat 3669 = true := by
  apply check_of_normalize (Case.ofNat 3669)
  have he : (Case.ofNat 3669).normalize = Case.ofNat 1621 := by decide
  rw [he]
  exact case1621
#print axioms case3669

theorem case1623 : checkNat 1623 = true := by native_decide
#print axioms case1623

theorem case1625 : checkNat 1625 = true := by native_decide
#print axioms case1625

theorem case3673 : checkNat 3673 = true := by
  apply check_of_normalize (Case.ofNat 3673)
  have he : (Case.ofNat 3673).normalize = Case.ofNat 1625 := by decide
  rw [he]
  exact case1625
#print axioms case3673

theorem case1627 : checkNat 1627 = true := by native_decide
#print axioms case1627

theorem case1629 : checkNat 1629 = true := by native_decide
#print axioms case1629

theorem case3677 : checkNat 3677 = true := by
  apply check_of_normalize (Case.ofNat 3677)
  have he : (Case.ofNat 3677).normalize = Case.ofNat 1629 := by decide
  rw [he]
  exact case1629
#print axioms case3677

theorem case1631 : checkNat 1631 = true := by native_decide
#print axioms case1631

theorem case1633 : checkNat 1633 = true := by native_decide
#print axioms case1633

theorem case3681 : checkNat 3681 = true := by
  apply check_of_normalize (Case.ofNat 3681)
  have he : (Case.ofNat 3681).normalize = Case.ofNat 1633 := by decide
  rw [he]
  exact case1633
#print axioms case3681

theorem case1635 : checkNat 1635 = true := by native_decide
#print axioms case1635

theorem case1637 : checkNat 1637 = true := by native_decide
#print axioms case1637

theorem case3685 : checkNat 3685 = true := by
  apply check_of_normalize (Case.ofNat 3685)
  have he : (Case.ofNat 3685).normalize = Case.ofNat 1637 := by decide
  rw [he]
  exact case1637
#print axioms case3685

theorem case1639 : checkNat 1639 = true := by native_decide
#print axioms case1639

theorem case1641 : checkNat 1641 = true := by native_decide
#print axioms case1641

theorem case3689 : checkNat 3689 = true := by
  apply check_of_normalize (Case.ofNat 3689)
  have he : (Case.ofNat 3689).normalize = Case.ofNat 1641 := by decide
  rw [he]
  exact case1641
#print axioms case3689

theorem case1643 : checkNat 1643 = true := by native_decide
#print axioms case1643

theorem case1645 : checkNat 1645 = true := by native_decide
#print axioms case1645

theorem case3693 : checkNat 3693 = true := by
  apply check_of_normalize (Case.ofNat 3693)
  have he : (Case.ofNat 3693).normalize = Case.ofNat 1645 := by decide
  rw [he]
  exact case1645
#print axioms case3693

theorem case1647 : checkNat 1647 = true := by native_decide
#print axioms case1647

theorem case1649 : checkNat 1649 = true := by native_decide
#print axioms case1649

theorem case3697 : checkNat 3697 = true := by
  apply check_of_normalize (Case.ofNat 3697)
  have he : (Case.ofNat 3697).normalize = Case.ofNat 1649 := by decide
  rw [he]
  exact case1649
#print axioms case3697

theorem case1651 : checkNat 1651 = true := by native_decide
#print axioms case1651

theorem case1653 : checkNat 1653 = true := by native_decide
#print axioms case1653

theorem case3701 : checkNat 3701 = true := by
  apply check_of_normalize (Case.ofNat 3701)
  have he : (Case.ofNat 3701).normalize = Case.ofNat 1653 := by decide
  rw [he]
  exact case1653
#print axioms case3701

theorem case1655 : checkNat 1655 = true := by native_decide
#print axioms case1655

theorem case1657 : checkNat 1657 = true := by native_decide
#print axioms case1657

theorem case3705 : checkNat 3705 = true := by
  apply check_of_normalize (Case.ofNat 3705)
  have he : (Case.ofNat 3705).normalize = Case.ofNat 1657 := by decide
  rw [he]
  exact case1657
#print axioms case3705

theorem case1659 : checkNat 1659 = true := by native_decide
#print axioms case1659

theorem case1661 : checkNat 1661 = true := by native_decide
#print axioms case1661

theorem case3709 : checkNat 3709 = true := by
  apply check_of_normalize (Case.ofNat 3709)
  have he : (Case.ofNat 3709).normalize = Case.ofNat 1661 := by decide
  rw [he]
  exact case1661
#print axioms case3709

theorem case1663 : checkNat 1663 = true := by native_decide
#print axioms case1663

theorem accepted :
    checkNat 1601 = true ∧
    checkNat 1603 = true ∧
    checkNat 1605 = true ∧
    checkNat 1607 = true ∧
    checkNat 1609 = true ∧
    checkNat 1611 = true ∧
    checkNat 1613 = true ∧
    checkNat 1615 = true ∧
    checkNat 1617 = true ∧
    checkNat 1619 = true ∧
    checkNat 1621 = true ∧
    checkNat 1623 = true ∧
    checkNat 1625 = true ∧
    checkNat 1627 = true ∧
    checkNat 1629 = true ∧
    checkNat 1631 = true ∧
    checkNat 1633 = true ∧
    checkNat 1635 = true ∧
    checkNat 1637 = true ∧
    checkNat 1639 = true ∧
    checkNat 1641 = true ∧
    checkNat 1643 = true ∧
    checkNat 1645 = true ∧
    checkNat 1647 = true ∧
    checkNat 1649 = true ∧
    checkNat 1651 = true ∧
    checkNat 1653 = true ∧
    checkNat 1655 = true ∧
    checkNat 1657 = true ∧
    checkNat 1659 = true ∧
    checkNat 1661 = true ∧
    checkNat 1663 = true ∧
    checkNat 3649 = true ∧
    checkNat 3653 = true ∧
    checkNat 3657 = true ∧
    checkNat 3661 = true ∧
    checkNat 3665 = true ∧
    checkNat 3669 = true ∧
    checkNat 3673 = true ∧
    checkNat 3677 = true ∧
    checkNat 3681 = true ∧
    checkNat 3685 = true ∧
    checkNat 3689 = true ∧
    checkNat 3693 = true ∧
    checkNat 3697 = true ∧
    checkNat 3701 = true ∧
    checkNat 3705 = true ∧
    checkNat 3709 = true := by
  exact ⟨case1601, case1603, case1605, case1607, case1609, case1611, case1613, case1615, case1617, case1619, case1621, case1623, case1625, case1627, case1629, case1631, case1633, case1635, case1637, case1639, case1641, case1643, case1645, case1647, case1649, case1651, case1653, case1655, case1657, case1659, case1661, case1663, case3649, case3653, case3657, case3661, case3665, case3669, case3673, case3677, case3681, case3685, case3689, case3693, case3697, case3701, case3705, case3709⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1312
