import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1344
open Sq19.Endgame.Reduction

theorem case1665 : checkNat 1665 = true := by native_decide
#print axioms case1665

theorem case3713 : checkNat 3713 = true := by
  apply check_of_normalize (Case.ofNat 3713)
  have he : (Case.ofNat 3713).normalize = Case.ofNat 1665 := by decide
  rw [he]
  exact case1665
#print axioms case3713

theorem case1667 : checkNat 1667 = true := by native_decide
#print axioms case1667

theorem case1669 : checkNat 1669 = true := by native_decide
#print axioms case1669

theorem case3717 : checkNat 3717 = true := by
  apply check_of_normalize (Case.ofNat 3717)
  have he : (Case.ofNat 3717).normalize = Case.ofNat 1669 := by decide
  rw [he]
  exact case1669
#print axioms case3717

theorem case1671 : checkNat 1671 = true := by native_decide
#print axioms case1671

theorem case1673 : checkNat 1673 = true := by native_decide
#print axioms case1673

theorem case3721 : checkNat 3721 = true := by
  apply check_of_normalize (Case.ofNat 3721)
  have he : (Case.ofNat 3721).normalize = Case.ofNat 1673 := by decide
  rw [he]
  exact case1673
#print axioms case3721

theorem case1675 : checkNat 1675 = true := by native_decide
#print axioms case1675

theorem case1677 : checkNat 1677 = true := by native_decide
#print axioms case1677

theorem case3725 : checkNat 3725 = true := by
  apply check_of_normalize (Case.ofNat 3725)
  have he : (Case.ofNat 3725).normalize = Case.ofNat 1677 := by decide
  rw [he]
  exact case1677
#print axioms case3725

theorem case1679 : checkNat 1679 = true := by native_decide
#print axioms case1679

theorem case1681 : checkNat 1681 = true := by native_decide
#print axioms case1681

theorem case3729 : checkNat 3729 = true := by
  apply check_of_normalize (Case.ofNat 3729)
  have he : (Case.ofNat 3729).normalize = Case.ofNat 1681 := by decide
  rw [he]
  exact case1681
#print axioms case3729

theorem case1683 : checkNat 1683 = true := by native_decide
#print axioms case1683

theorem case1685 : checkNat 1685 = true := by native_decide
#print axioms case1685

theorem case3733 : checkNat 3733 = true := by
  apply check_of_normalize (Case.ofNat 3733)
  have he : (Case.ofNat 3733).normalize = Case.ofNat 1685 := by decide
  rw [he]
  exact case1685
#print axioms case3733

theorem case1687 : checkNat 1687 = true := by native_decide
#print axioms case1687

theorem case1689 : checkNat 1689 = true := by native_decide
#print axioms case1689

theorem case3737 : checkNat 3737 = true := by
  apply check_of_normalize (Case.ofNat 3737)
  have he : (Case.ofNat 3737).normalize = Case.ofNat 1689 := by decide
  rw [he]
  exact case1689
#print axioms case3737

theorem case1691 : checkNat 1691 = true := by native_decide
#print axioms case1691

theorem case1693 : checkNat 1693 = true := by native_decide
#print axioms case1693

theorem case3741 : checkNat 3741 = true := by
  apply check_of_normalize (Case.ofNat 3741)
  have he : (Case.ofNat 3741).normalize = Case.ofNat 1693 := by decide
  rw [he]
  exact case1693
#print axioms case3741

theorem case1695 : checkNat 1695 = true := by native_decide
#print axioms case1695

theorem case1697 : checkNat 1697 = true := by native_decide
#print axioms case1697

theorem case3745 : checkNat 3745 = true := by
  apply check_of_normalize (Case.ofNat 3745)
  have he : (Case.ofNat 3745).normalize = Case.ofNat 1697 := by decide
  rw [he]
  exact case1697
#print axioms case3745

theorem case1699 : checkNat 1699 = true := by native_decide
#print axioms case1699

theorem case1701 : checkNat 1701 = true := by native_decide
#print axioms case1701

theorem case3749 : checkNat 3749 = true := by
  apply check_of_normalize (Case.ofNat 3749)
  have he : (Case.ofNat 3749).normalize = Case.ofNat 1701 := by decide
  rw [he]
  exact case1701
#print axioms case3749

theorem case1703 : checkNat 1703 = true := by native_decide
#print axioms case1703

theorem case1705 : checkNat 1705 = true := by native_decide
#print axioms case1705

theorem case3753 : checkNat 3753 = true := by
  apply check_of_normalize (Case.ofNat 3753)
  have he : (Case.ofNat 3753).normalize = Case.ofNat 1705 := by decide
  rw [he]
  exact case1705
#print axioms case3753

theorem case1707 : checkNat 1707 = true := by native_decide
#print axioms case1707

theorem case1709 : checkNat 1709 = true := by native_decide
#print axioms case1709

theorem case3757 : checkNat 3757 = true := by
  apply check_of_normalize (Case.ofNat 3757)
  have he : (Case.ofNat 3757).normalize = Case.ofNat 1709 := by decide
  rw [he]
  exact case1709
#print axioms case3757

theorem case1711 : checkNat 1711 = true := by native_decide
#print axioms case1711

theorem case1713 : checkNat 1713 = true := by native_decide
#print axioms case1713

theorem case3761 : checkNat 3761 = true := by
  apply check_of_normalize (Case.ofNat 3761)
  have he : (Case.ofNat 3761).normalize = Case.ofNat 1713 := by decide
  rw [he]
  exact case1713
#print axioms case3761

theorem case1715 : checkNat 1715 = true := by native_decide
#print axioms case1715

theorem case1717 : checkNat 1717 = true := by native_decide
#print axioms case1717

theorem case3765 : checkNat 3765 = true := by
  apply check_of_normalize (Case.ofNat 3765)
  have he : (Case.ofNat 3765).normalize = Case.ofNat 1717 := by decide
  rw [he]
  exact case1717
#print axioms case3765

theorem case1719 : checkNat 1719 = true := by native_decide
#print axioms case1719

theorem case1721 : checkNat 1721 = true := by native_decide
#print axioms case1721

theorem case3769 : checkNat 3769 = true := by
  apply check_of_normalize (Case.ofNat 3769)
  have he : (Case.ofNat 3769).normalize = Case.ofNat 1721 := by decide
  rw [he]
  exact case1721
#print axioms case3769

theorem case1723 : checkNat 1723 = true := by native_decide
#print axioms case1723

theorem case1725 : checkNat 1725 = true := by native_decide
#print axioms case1725

theorem case3773 : checkNat 3773 = true := by
  apply check_of_normalize (Case.ofNat 3773)
  have he : (Case.ofNat 3773).normalize = Case.ofNat 1725 := by decide
  rw [he]
  exact case1725
#print axioms case3773

theorem case1727 : checkNat 1727 = true := by native_decide
#print axioms case1727

theorem accepted :
    checkNat 1665 = true ∧
    checkNat 1667 = true ∧
    checkNat 1669 = true ∧
    checkNat 1671 = true ∧
    checkNat 1673 = true ∧
    checkNat 1675 = true ∧
    checkNat 1677 = true ∧
    checkNat 1679 = true ∧
    checkNat 1681 = true ∧
    checkNat 1683 = true ∧
    checkNat 1685 = true ∧
    checkNat 1687 = true ∧
    checkNat 1689 = true ∧
    checkNat 1691 = true ∧
    checkNat 1693 = true ∧
    checkNat 1695 = true ∧
    checkNat 1697 = true ∧
    checkNat 1699 = true ∧
    checkNat 1701 = true ∧
    checkNat 1703 = true ∧
    checkNat 1705 = true ∧
    checkNat 1707 = true ∧
    checkNat 1709 = true ∧
    checkNat 1711 = true ∧
    checkNat 1713 = true ∧
    checkNat 1715 = true ∧
    checkNat 1717 = true ∧
    checkNat 1719 = true ∧
    checkNat 1721 = true ∧
    checkNat 1723 = true ∧
    checkNat 1725 = true ∧
    checkNat 1727 = true ∧
    checkNat 3713 = true ∧
    checkNat 3717 = true ∧
    checkNat 3721 = true ∧
    checkNat 3725 = true ∧
    checkNat 3729 = true ∧
    checkNat 3733 = true ∧
    checkNat 3737 = true ∧
    checkNat 3741 = true ∧
    checkNat 3745 = true ∧
    checkNat 3749 = true ∧
    checkNat 3753 = true ∧
    checkNat 3757 = true ∧
    checkNat 3761 = true ∧
    checkNat 3765 = true ∧
    checkNat 3769 = true ∧
    checkNat 3773 = true := by
  exact ⟨case1665, case1667, case1669, case1671, case1673, case1675, case1677, case1679, case1681, case1683, case1685, case1687, case1689, case1691, case1693, case1695, case1697, case1699, case1701, case1703, case1705, case1707, case1709, case1711, case1713, case1715, case1717, case1719, case1721, case1723, case1725, case1727, case3713, case3717, case3721, case3725, case3729, case3733, case3737, case3741, case3745, case3749, case3753, case3757, case3761, case3765, case3769, case3773⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1344
