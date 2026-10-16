import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1376
open Sq19.Endgame.Reduction

theorem case1729 : checkNat 1729 = true := by native_decide
#print axioms case1729

theorem case3777 : checkNat 3777 = true := by
  apply check_of_normalize (Case.ofNat 3777)
  have he : (Case.ofNat 3777).normalize = Case.ofNat 1729 := by decide
  rw [he]
  exact case1729
#print axioms case3777

theorem case1731 : checkNat 1731 = true := by native_decide
#print axioms case1731

theorem case1733 : checkNat 1733 = true := by native_decide
#print axioms case1733

theorem case3781 : checkNat 3781 = true := by
  apply check_of_normalize (Case.ofNat 3781)
  have he : (Case.ofNat 3781).normalize = Case.ofNat 1733 := by decide
  rw [he]
  exact case1733
#print axioms case3781

theorem case1735 : checkNat 1735 = true := by native_decide
#print axioms case1735

theorem case1737 : checkNat 1737 = true := by native_decide
#print axioms case1737

theorem case3785 : checkNat 3785 = true := by
  apply check_of_normalize (Case.ofNat 3785)
  have he : (Case.ofNat 3785).normalize = Case.ofNat 1737 := by decide
  rw [he]
  exact case1737
#print axioms case3785

theorem case1739 : checkNat 1739 = true := by native_decide
#print axioms case1739

theorem case1741 : checkNat 1741 = true := by native_decide
#print axioms case1741

theorem case3789 : checkNat 3789 = true := by
  apply check_of_normalize (Case.ofNat 3789)
  have he : (Case.ofNat 3789).normalize = Case.ofNat 1741 := by decide
  rw [he]
  exact case1741
#print axioms case3789

theorem case1743 : checkNat 1743 = true := by native_decide
#print axioms case1743

theorem case1745 : checkNat 1745 = true := by native_decide
#print axioms case1745

theorem case3793 : checkNat 3793 = true := by
  apply check_of_normalize (Case.ofNat 3793)
  have he : (Case.ofNat 3793).normalize = Case.ofNat 1745 := by decide
  rw [he]
  exact case1745
#print axioms case3793

theorem case1747 : checkNat 1747 = true := by native_decide
#print axioms case1747

theorem case1749 : checkNat 1749 = true := by native_decide
#print axioms case1749

theorem case3797 : checkNat 3797 = true := by
  apply check_of_normalize (Case.ofNat 3797)
  have he : (Case.ofNat 3797).normalize = Case.ofNat 1749 := by decide
  rw [he]
  exact case1749
#print axioms case3797

theorem case1751 : checkNat 1751 = true := by native_decide
#print axioms case1751

theorem case1753 : checkNat 1753 = true := by native_decide
#print axioms case1753

theorem case3801 : checkNat 3801 = true := by
  apply check_of_normalize (Case.ofNat 3801)
  have he : (Case.ofNat 3801).normalize = Case.ofNat 1753 := by decide
  rw [he]
  exact case1753
#print axioms case3801

theorem case1755 : checkNat 1755 = true := by native_decide
#print axioms case1755

theorem case1757 : checkNat 1757 = true := by native_decide
#print axioms case1757

theorem case3805 : checkNat 3805 = true := by
  apply check_of_normalize (Case.ofNat 3805)
  have he : (Case.ofNat 3805).normalize = Case.ofNat 1757 := by decide
  rw [he]
  exact case1757
#print axioms case3805

theorem case1759 : checkNat 1759 = true := by native_decide
#print axioms case1759

theorem case1761 : checkNat 1761 = true := by native_decide
#print axioms case1761

theorem case3809 : checkNat 3809 = true := by
  apply check_of_normalize (Case.ofNat 3809)
  have he : (Case.ofNat 3809).normalize = Case.ofNat 1761 := by decide
  rw [he]
  exact case1761
#print axioms case3809

theorem case1763 : checkNat 1763 = true := by native_decide
#print axioms case1763

theorem case1765 : checkNat 1765 = true := by native_decide
#print axioms case1765

theorem case3813 : checkNat 3813 = true := by
  apply check_of_normalize (Case.ofNat 3813)
  have he : (Case.ofNat 3813).normalize = Case.ofNat 1765 := by decide
  rw [he]
  exact case1765
#print axioms case3813

theorem case1767 : checkNat 1767 = true := by native_decide
#print axioms case1767

theorem case1769 : checkNat 1769 = true := by native_decide
#print axioms case1769

theorem case3817 : checkNat 3817 = true := by
  apply check_of_normalize (Case.ofNat 3817)
  have he : (Case.ofNat 3817).normalize = Case.ofNat 1769 := by decide
  rw [he]
  exact case1769
#print axioms case3817

theorem case1771 : checkNat 1771 = true := by native_decide
#print axioms case1771

theorem case1773 : checkNat 1773 = true := by native_decide
#print axioms case1773

theorem case3821 : checkNat 3821 = true := by
  apply check_of_normalize (Case.ofNat 3821)
  have he : (Case.ofNat 3821).normalize = Case.ofNat 1773 := by decide
  rw [he]
  exact case1773
#print axioms case3821

theorem case1775 : checkNat 1775 = true := by native_decide
#print axioms case1775

theorem case1777 : checkNat 1777 = true := by native_decide
#print axioms case1777

theorem case3825 : checkNat 3825 = true := by
  apply check_of_normalize (Case.ofNat 3825)
  have he : (Case.ofNat 3825).normalize = Case.ofNat 1777 := by decide
  rw [he]
  exact case1777
#print axioms case3825

theorem case1779 : checkNat 1779 = true := by native_decide
#print axioms case1779

theorem case1781 : checkNat 1781 = true := by native_decide
#print axioms case1781

theorem case3829 : checkNat 3829 = true := by
  apply check_of_normalize (Case.ofNat 3829)
  have he : (Case.ofNat 3829).normalize = Case.ofNat 1781 := by decide
  rw [he]
  exact case1781
#print axioms case3829

theorem case1783 : checkNat 1783 = true := by native_decide
#print axioms case1783

theorem case1785 : checkNat 1785 = true := by native_decide
#print axioms case1785

theorem case3833 : checkNat 3833 = true := by
  apply check_of_normalize (Case.ofNat 3833)
  have he : (Case.ofNat 3833).normalize = Case.ofNat 1785 := by decide
  rw [he]
  exact case1785
#print axioms case3833

theorem case1787 : checkNat 1787 = true := by native_decide
#print axioms case1787

theorem case1789 : checkNat 1789 = true := by native_decide
#print axioms case1789

theorem case3837 : checkNat 3837 = true := by
  apply check_of_normalize (Case.ofNat 3837)
  have he : (Case.ofNat 3837).normalize = Case.ofNat 1789 := by decide
  rw [he]
  exact case1789
#print axioms case3837

theorem case1791 : checkNat 1791 = true := by native_decide
#print axioms case1791

theorem accepted :
    checkNat 1729 = true ∧
    checkNat 1731 = true ∧
    checkNat 1733 = true ∧
    checkNat 1735 = true ∧
    checkNat 1737 = true ∧
    checkNat 1739 = true ∧
    checkNat 1741 = true ∧
    checkNat 1743 = true ∧
    checkNat 1745 = true ∧
    checkNat 1747 = true ∧
    checkNat 1749 = true ∧
    checkNat 1751 = true ∧
    checkNat 1753 = true ∧
    checkNat 1755 = true ∧
    checkNat 1757 = true ∧
    checkNat 1759 = true ∧
    checkNat 1761 = true ∧
    checkNat 1763 = true ∧
    checkNat 1765 = true ∧
    checkNat 1767 = true ∧
    checkNat 1769 = true ∧
    checkNat 1771 = true ∧
    checkNat 1773 = true ∧
    checkNat 1775 = true ∧
    checkNat 1777 = true ∧
    checkNat 1779 = true ∧
    checkNat 1781 = true ∧
    checkNat 1783 = true ∧
    checkNat 1785 = true ∧
    checkNat 1787 = true ∧
    checkNat 1789 = true ∧
    checkNat 1791 = true ∧
    checkNat 3777 = true ∧
    checkNat 3781 = true ∧
    checkNat 3785 = true ∧
    checkNat 3789 = true ∧
    checkNat 3793 = true ∧
    checkNat 3797 = true ∧
    checkNat 3801 = true ∧
    checkNat 3805 = true ∧
    checkNat 3809 = true ∧
    checkNat 3813 = true ∧
    checkNat 3817 = true ∧
    checkNat 3821 = true ∧
    checkNat 3825 = true ∧
    checkNat 3829 = true ∧
    checkNat 3833 = true ∧
    checkNat 3837 = true := by
  exact ⟨case1729, case1731, case1733, case1735, case1737, case1739, case1741, case1743, case1745, case1747, case1749, case1751, case1753, case1755, case1757, case1759, case1761, case1763, case1765, case1767, case1769, case1771, case1773, case1775, case1777, case1779, case1781, case1783, case1785, case1787, case1789, case1791, case3777, case3781, case3785, case3789, case3793, case3797, case3801, case3805, case3809, case3813, case3817, case3821, case3825, case3829, case3833, case3837⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1376
