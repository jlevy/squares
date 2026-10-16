import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1408
open Sq19.Endgame.Reduction

theorem case1793 : checkNat 1793 = true := by native_decide
#print axioms case1793

theorem case3841 : checkNat 3841 = true := by
  apply check_of_normalize (Case.ofNat 3841)
  have he : (Case.ofNat 3841).normalize = Case.ofNat 1793 := by decide
  rw [he]
  exact case1793
#print axioms case3841

theorem case1795 : checkNat 1795 = true := by native_decide
#print axioms case1795

theorem case1797 : checkNat 1797 = true := by native_decide
#print axioms case1797

theorem case3845 : checkNat 3845 = true := by
  apply check_of_normalize (Case.ofNat 3845)
  have he : (Case.ofNat 3845).normalize = Case.ofNat 1797 := by decide
  rw [he]
  exact case1797
#print axioms case3845

theorem case1799 : checkNat 1799 = true := by native_decide
#print axioms case1799

theorem case1801 : checkNat 1801 = true := by native_decide
#print axioms case1801

theorem case3849 : checkNat 3849 = true := by
  apply check_of_normalize (Case.ofNat 3849)
  have he : (Case.ofNat 3849).normalize = Case.ofNat 1801 := by decide
  rw [he]
  exact case1801
#print axioms case3849

theorem case1803 : checkNat 1803 = true := by native_decide
#print axioms case1803

theorem case1805 : checkNat 1805 = true := by native_decide
#print axioms case1805

theorem case3853 : checkNat 3853 = true := by
  apply check_of_normalize (Case.ofNat 3853)
  have he : (Case.ofNat 3853).normalize = Case.ofNat 1805 := by decide
  rw [he]
  exact case1805
#print axioms case3853

theorem case1807 : checkNat 1807 = true := by native_decide
#print axioms case1807

theorem case1809 : checkNat 1809 = true := by native_decide
#print axioms case1809

theorem case3857 : checkNat 3857 = true := by
  apply check_of_normalize (Case.ofNat 3857)
  have he : (Case.ofNat 3857).normalize = Case.ofNat 1809 := by decide
  rw [he]
  exact case1809
#print axioms case3857

theorem case1811 : checkNat 1811 = true := by native_decide
#print axioms case1811

theorem case1813 : checkNat 1813 = true := by native_decide
#print axioms case1813

theorem case3861 : checkNat 3861 = true := by
  apply check_of_normalize (Case.ofNat 3861)
  have he : (Case.ofNat 3861).normalize = Case.ofNat 1813 := by decide
  rw [he]
  exact case1813
#print axioms case3861

theorem case1815 : checkNat 1815 = true := by native_decide
#print axioms case1815

theorem case1817 : checkNat 1817 = true := by native_decide
#print axioms case1817

theorem case3865 : checkNat 3865 = true := by
  apply check_of_normalize (Case.ofNat 3865)
  have he : (Case.ofNat 3865).normalize = Case.ofNat 1817 := by decide
  rw [he]
  exact case1817
#print axioms case3865

theorem case1819 : checkNat 1819 = true := by native_decide
#print axioms case1819

theorem case1821 : checkNat 1821 = true := by native_decide
#print axioms case1821

theorem case3869 : checkNat 3869 = true := by
  apply check_of_normalize (Case.ofNat 3869)
  have he : (Case.ofNat 3869).normalize = Case.ofNat 1821 := by decide
  rw [he]
  exact case1821
#print axioms case3869

theorem case1823 : checkNat 1823 = true := by native_decide
#print axioms case1823

theorem case1825 : checkNat 1825 = true := by native_decide
#print axioms case1825

theorem case3873 : checkNat 3873 = true := by
  apply check_of_normalize (Case.ofNat 3873)
  have he : (Case.ofNat 3873).normalize = Case.ofNat 1825 := by decide
  rw [he]
  exact case1825
#print axioms case3873

theorem case1827 : checkNat 1827 = true := by native_decide
#print axioms case1827

theorem case1829 : checkNat 1829 = true := by native_decide
#print axioms case1829

theorem case3877 : checkNat 3877 = true := by
  apply check_of_normalize (Case.ofNat 3877)
  have he : (Case.ofNat 3877).normalize = Case.ofNat 1829 := by decide
  rw [he]
  exact case1829
#print axioms case3877

theorem case1831 : checkNat 1831 = true := by native_decide
#print axioms case1831

theorem case1833 : checkNat 1833 = true := by native_decide
#print axioms case1833

theorem case3881 : checkNat 3881 = true := by
  apply check_of_normalize (Case.ofNat 3881)
  have he : (Case.ofNat 3881).normalize = Case.ofNat 1833 := by decide
  rw [he]
  exact case1833
#print axioms case3881

theorem case1835 : checkNat 1835 = true := by native_decide
#print axioms case1835

theorem case1837 : checkNat 1837 = true := by native_decide
#print axioms case1837

theorem case3885 : checkNat 3885 = true := by
  apply check_of_normalize (Case.ofNat 3885)
  have he : (Case.ofNat 3885).normalize = Case.ofNat 1837 := by decide
  rw [he]
  exact case1837
#print axioms case3885

theorem case1839 : checkNat 1839 = true := by native_decide
#print axioms case1839

theorem case1841 : checkNat 1841 = true := by native_decide
#print axioms case1841

theorem case3889 : checkNat 3889 = true := by
  apply check_of_normalize (Case.ofNat 3889)
  have he : (Case.ofNat 3889).normalize = Case.ofNat 1841 := by decide
  rw [he]
  exact case1841
#print axioms case3889

theorem case1843 : checkNat 1843 = true := by native_decide
#print axioms case1843

theorem case1845 : checkNat 1845 = true := by native_decide
#print axioms case1845

theorem case3893 : checkNat 3893 = true := by
  apply check_of_normalize (Case.ofNat 3893)
  have he : (Case.ofNat 3893).normalize = Case.ofNat 1845 := by decide
  rw [he]
  exact case1845
#print axioms case3893

theorem case1847 : checkNat 1847 = true := by native_decide
#print axioms case1847

theorem case1849 : checkNat 1849 = true := by native_decide
#print axioms case1849

theorem case3897 : checkNat 3897 = true := by
  apply check_of_normalize (Case.ofNat 3897)
  have he : (Case.ofNat 3897).normalize = Case.ofNat 1849 := by decide
  rw [he]
  exact case1849
#print axioms case3897

theorem case1851 : checkNat 1851 = true := by native_decide
#print axioms case1851

theorem case1853 : checkNat 1853 = true := by native_decide
#print axioms case1853

theorem case3901 : checkNat 3901 = true := by
  apply check_of_normalize (Case.ofNat 3901)
  have he : (Case.ofNat 3901).normalize = Case.ofNat 1853 := by decide
  rw [he]
  exact case1853
#print axioms case3901

theorem case1855 : checkNat 1855 = true := by native_decide
#print axioms case1855

theorem accepted :
    checkNat 1793 = true ∧
    checkNat 1795 = true ∧
    checkNat 1797 = true ∧
    checkNat 1799 = true ∧
    checkNat 1801 = true ∧
    checkNat 1803 = true ∧
    checkNat 1805 = true ∧
    checkNat 1807 = true ∧
    checkNat 1809 = true ∧
    checkNat 1811 = true ∧
    checkNat 1813 = true ∧
    checkNat 1815 = true ∧
    checkNat 1817 = true ∧
    checkNat 1819 = true ∧
    checkNat 1821 = true ∧
    checkNat 1823 = true ∧
    checkNat 1825 = true ∧
    checkNat 1827 = true ∧
    checkNat 1829 = true ∧
    checkNat 1831 = true ∧
    checkNat 1833 = true ∧
    checkNat 1835 = true ∧
    checkNat 1837 = true ∧
    checkNat 1839 = true ∧
    checkNat 1841 = true ∧
    checkNat 1843 = true ∧
    checkNat 1845 = true ∧
    checkNat 1847 = true ∧
    checkNat 1849 = true ∧
    checkNat 1851 = true ∧
    checkNat 1853 = true ∧
    checkNat 1855 = true ∧
    checkNat 3841 = true ∧
    checkNat 3845 = true ∧
    checkNat 3849 = true ∧
    checkNat 3853 = true ∧
    checkNat 3857 = true ∧
    checkNat 3861 = true ∧
    checkNat 3865 = true ∧
    checkNat 3869 = true ∧
    checkNat 3873 = true ∧
    checkNat 3877 = true ∧
    checkNat 3881 = true ∧
    checkNat 3885 = true ∧
    checkNat 3889 = true ∧
    checkNat 3893 = true ∧
    checkNat 3897 = true ∧
    checkNat 3901 = true := by
  exact ⟨case1793, case1795, case1797, case1799, case1801, case1803, case1805, case1807, case1809, case1811, case1813, case1815, case1817, case1819, case1821, case1823, case1825, case1827, case1829, case1831, case1833, case1835, case1837, case1839, case1841, case1843, case1845, case1847, case1849, case1851, case1853, case1855, case3841, case3845, case3849, case3853, case3857, case3861, case3865, case3869, case3873, case3877, case3881, case3885, case3889, case3893, case3897, case3901⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1408
