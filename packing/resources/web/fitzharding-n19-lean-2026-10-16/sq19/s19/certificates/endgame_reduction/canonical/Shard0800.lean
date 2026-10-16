import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0800
open Sq19.Endgame.Reduction

theorem case0800 : checkNat 800 = true := by native_decide
#print axioms case0800

theorem case1824 : checkNat 1824 = true := by
  apply check_of_normalize (Case.ofNat 1824)
  have he : (Case.ofNat 1824).normalize = Case.ofNat 800 := by decide
  rw [he]
  exact case0800
#print axioms case1824

theorem case2848 : checkNat 2848 = true := by
  apply check_of_normalize (Case.ofNat 2848)
  have he : (Case.ofNat 2848).normalize = Case.ofNat 800 := by decide
  rw [he]
  exact case0800
#print axioms case2848

theorem case3872 : checkNat 3872 = true := by
  apply check_of_normalize (Case.ofNat 3872)
  have he : (Case.ofNat 3872).normalize = Case.ofNat 800 := by decide
  rw [he]
  exact case0800
#print axioms case3872

theorem case0801 : checkNat 801 = true := by native_decide
#print axioms case0801

theorem case2849 : checkNat 2849 = true := by
  apply check_of_normalize (Case.ofNat 2849)
  have he : (Case.ofNat 2849).normalize = Case.ofNat 801 := by decide
  rw [he]
  exact case0801
#print axioms case2849

theorem case0802 : checkNat 802 = true := by native_decide
#print axioms case0802

theorem case1826 : checkNat 1826 = true := by
  apply check_of_normalize (Case.ofNat 1826)
  have he : (Case.ofNat 1826).normalize = Case.ofNat 802 := by decide
  rw [he]
  exact case0802
#print axioms case1826

theorem case0803 : checkNat 803 = true := by native_decide
#print axioms case0803

theorem case0804 : checkNat 804 = true := by native_decide
#print axioms case0804

theorem case1828 : checkNat 1828 = true := by
  apply check_of_normalize (Case.ofNat 1828)
  have he : (Case.ofNat 1828).normalize = Case.ofNat 804 := by decide
  rw [he]
  exact case0804
#print axioms case1828

theorem case2852 : checkNat 2852 = true := by
  apply check_of_normalize (Case.ofNat 2852)
  have he : (Case.ofNat 2852).normalize = Case.ofNat 804 := by decide
  rw [he]
  exact case0804
#print axioms case2852

theorem case3876 : checkNat 3876 = true := by
  apply check_of_normalize (Case.ofNat 3876)
  have he : (Case.ofNat 3876).normalize = Case.ofNat 804 := by decide
  rw [he]
  exact case0804
#print axioms case3876

theorem case0805 : checkNat 805 = true := by native_decide
#print axioms case0805

theorem case2853 : checkNat 2853 = true := by
  apply check_of_normalize (Case.ofNat 2853)
  have he : (Case.ofNat 2853).normalize = Case.ofNat 805 := by decide
  rw [he]
  exact case0805
#print axioms case2853

theorem case0806 : checkNat 806 = true := by native_decide
#print axioms case0806

theorem case1830 : checkNat 1830 = true := by
  apply check_of_normalize (Case.ofNat 1830)
  have he : (Case.ofNat 1830).normalize = Case.ofNat 806 := by decide
  rw [he]
  exact case0806
#print axioms case1830

theorem case0807 : checkNat 807 = true := by native_decide
#print axioms case0807

theorem case0808 : checkNat 808 = true := by native_decide
#print axioms case0808

theorem case1832 : checkNat 1832 = true := by
  apply check_of_normalize (Case.ofNat 1832)
  have he : (Case.ofNat 1832).normalize = Case.ofNat 808 := by decide
  rw [he]
  exact case0808
#print axioms case1832

theorem case2856 : checkNat 2856 = true := by
  apply check_of_normalize (Case.ofNat 2856)
  have he : (Case.ofNat 2856).normalize = Case.ofNat 808 := by decide
  rw [he]
  exact case0808
#print axioms case2856

theorem case3880 : checkNat 3880 = true := by
  apply check_of_normalize (Case.ofNat 3880)
  have he : (Case.ofNat 3880).normalize = Case.ofNat 808 := by decide
  rw [he]
  exact case0808
#print axioms case3880

theorem case0809 : checkNat 809 = true := by native_decide
#print axioms case0809

theorem case2857 : checkNat 2857 = true := by
  apply check_of_normalize (Case.ofNat 2857)
  have he : (Case.ofNat 2857).normalize = Case.ofNat 809 := by decide
  rw [he]
  exact case0809
#print axioms case2857

theorem case0810 : checkNat 810 = true := by native_decide
#print axioms case0810

theorem case1834 : checkNat 1834 = true := by
  apply check_of_normalize (Case.ofNat 1834)
  have he : (Case.ofNat 1834).normalize = Case.ofNat 810 := by decide
  rw [he]
  exact case0810
#print axioms case1834

theorem case0811 : checkNat 811 = true := by native_decide
#print axioms case0811

theorem case0812 : checkNat 812 = true := by native_decide
#print axioms case0812

theorem case1836 : checkNat 1836 = true := by
  apply check_of_normalize (Case.ofNat 1836)
  have he : (Case.ofNat 1836).normalize = Case.ofNat 812 := by decide
  rw [he]
  exact case0812
#print axioms case1836

theorem case2860 : checkNat 2860 = true := by
  apply check_of_normalize (Case.ofNat 2860)
  have he : (Case.ofNat 2860).normalize = Case.ofNat 812 := by decide
  rw [he]
  exact case0812
#print axioms case2860

theorem case3884 : checkNat 3884 = true := by
  apply check_of_normalize (Case.ofNat 3884)
  have he : (Case.ofNat 3884).normalize = Case.ofNat 812 := by decide
  rw [he]
  exact case0812
#print axioms case3884

theorem case0813 : checkNat 813 = true := by native_decide
#print axioms case0813

theorem case2861 : checkNat 2861 = true := by
  apply check_of_normalize (Case.ofNat 2861)
  have he : (Case.ofNat 2861).normalize = Case.ofNat 813 := by decide
  rw [he]
  exact case0813
#print axioms case2861

theorem case0814 : checkNat 814 = true := by native_decide
#print axioms case0814

theorem case1838 : checkNat 1838 = true := by
  apply check_of_normalize (Case.ofNat 1838)
  have he : (Case.ofNat 1838).normalize = Case.ofNat 814 := by decide
  rw [he]
  exact case0814
#print axioms case1838

theorem case0815 : checkNat 815 = true := by native_decide
#print axioms case0815

theorem case0816 : checkNat 816 = true := by native_decide
#print axioms case0816

theorem case1840 : checkNat 1840 = true := by
  apply check_of_normalize (Case.ofNat 1840)
  have he : (Case.ofNat 1840).normalize = Case.ofNat 816 := by decide
  rw [he]
  exact case0816
#print axioms case1840

theorem case2864 : checkNat 2864 = true := by
  apply check_of_normalize (Case.ofNat 2864)
  have he : (Case.ofNat 2864).normalize = Case.ofNat 816 := by decide
  rw [he]
  exact case0816
#print axioms case2864

theorem case3888 : checkNat 3888 = true := by
  apply check_of_normalize (Case.ofNat 3888)
  have he : (Case.ofNat 3888).normalize = Case.ofNat 816 := by decide
  rw [he]
  exact case0816
#print axioms case3888

theorem case0817 : checkNat 817 = true := by native_decide
#print axioms case0817

theorem case2865 : checkNat 2865 = true := by
  apply check_of_normalize (Case.ofNat 2865)
  have he : (Case.ofNat 2865).normalize = Case.ofNat 817 := by decide
  rw [he]
  exact case0817
#print axioms case2865

theorem case0818 : checkNat 818 = true := by native_decide
#print axioms case0818

theorem case1842 : checkNat 1842 = true := by
  apply check_of_normalize (Case.ofNat 1842)
  have he : (Case.ofNat 1842).normalize = Case.ofNat 818 := by decide
  rw [he]
  exact case0818
#print axioms case1842

theorem case0819 : checkNat 819 = true := by native_decide
#print axioms case0819

theorem case0820 : checkNat 820 = true := by native_decide
#print axioms case0820

theorem case1844 : checkNat 1844 = true := by
  apply check_of_normalize (Case.ofNat 1844)
  have he : (Case.ofNat 1844).normalize = Case.ofNat 820 := by decide
  rw [he]
  exact case0820
#print axioms case1844

theorem case2868 : checkNat 2868 = true := by
  apply check_of_normalize (Case.ofNat 2868)
  have he : (Case.ofNat 2868).normalize = Case.ofNat 820 := by decide
  rw [he]
  exact case0820
#print axioms case2868

theorem case3892 : checkNat 3892 = true := by
  apply check_of_normalize (Case.ofNat 3892)
  have he : (Case.ofNat 3892).normalize = Case.ofNat 820 := by decide
  rw [he]
  exact case0820
#print axioms case3892

theorem case0821 : checkNat 821 = true := by native_decide
#print axioms case0821

theorem case2869 : checkNat 2869 = true := by
  apply check_of_normalize (Case.ofNat 2869)
  have he : (Case.ofNat 2869).normalize = Case.ofNat 821 := by decide
  rw [he]
  exact case0821
#print axioms case2869

theorem case0822 : checkNat 822 = true := by native_decide
#print axioms case0822

theorem case1846 : checkNat 1846 = true := by
  apply check_of_normalize (Case.ofNat 1846)
  have he : (Case.ofNat 1846).normalize = Case.ofNat 822 := by decide
  rw [he]
  exact case0822
#print axioms case1846

theorem case0823 : checkNat 823 = true := by native_decide
#print axioms case0823

theorem case0824 : checkNat 824 = true := by native_decide
#print axioms case0824

theorem case1848 : checkNat 1848 = true := by
  apply check_of_normalize (Case.ofNat 1848)
  have he : (Case.ofNat 1848).normalize = Case.ofNat 824 := by decide
  rw [he]
  exact case0824
#print axioms case1848

theorem case2872 : checkNat 2872 = true := by
  apply check_of_normalize (Case.ofNat 2872)
  have he : (Case.ofNat 2872).normalize = Case.ofNat 824 := by decide
  rw [he]
  exact case0824
#print axioms case2872

theorem case3896 : checkNat 3896 = true := by
  apply check_of_normalize (Case.ofNat 3896)
  have he : (Case.ofNat 3896).normalize = Case.ofNat 824 := by decide
  rw [he]
  exact case0824
#print axioms case3896

theorem case0825 : checkNat 825 = true := by native_decide
#print axioms case0825

theorem case2873 : checkNat 2873 = true := by
  apply check_of_normalize (Case.ofNat 2873)
  have he : (Case.ofNat 2873).normalize = Case.ofNat 825 := by decide
  rw [he]
  exact case0825
#print axioms case2873

theorem case0826 : checkNat 826 = true := by native_decide
#print axioms case0826

theorem case1850 : checkNat 1850 = true := by
  apply check_of_normalize (Case.ofNat 1850)
  have he : (Case.ofNat 1850).normalize = Case.ofNat 826 := by decide
  rw [he]
  exact case0826
#print axioms case1850

theorem case0827 : checkNat 827 = true := by native_decide
#print axioms case0827

theorem case0828 : checkNat 828 = true := by native_decide
#print axioms case0828

theorem case1852 : checkNat 1852 = true := by
  apply check_of_normalize (Case.ofNat 1852)
  have he : (Case.ofNat 1852).normalize = Case.ofNat 828 := by decide
  rw [he]
  exact case0828
#print axioms case1852

theorem case2876 : checkNat 2876 = true := by
  apply check_of_normalize (Case.ofNat 2876)
  have he : (Case.ofNat 2876).normalize = Case.ofNat 828 := by decide
  rw [he]
  exact case0828
#print axioms case2876

theorem case3900 : checkNat 3900 = true := by
  apply check_of_normalize (Case.ofNat 3900)
  have he : (Case.ofNat 3900).normalize = Case.ofNat 828 := by decide
  rw [he]
  exact case0828
#print axioms case3900

theorem case0829 : checkNat 829 = true := by native_decide
#print axioms case0829

theorem case2877 : checkNat 2877 = true := by
  apply check_of_normalize (Case.ofNat 2877)
  have he : (Case.ofNat 2877).normalize = Case.ofNat 829 := by decide
  rw [he]
  exact case0829
#print axioms case2877

theorem case0830 : checkNat 830 = true := by native_decide
#print axioms case0830

theorem case1854 : checkNat 1854 = true := by
  apply check_of_normalize (Case.ofNat 1854)
  have he : (Case.ofNat 1854).normalize = Case.ofNat 830 := by decide
  rw [he]
  exact case0830
#print axioms case1854

theorem case0831 : checkNat 831 = true := by native_decide
#print axioms case0831

theorem accepted :
    checkNat 800 = true ∧
    checkNat 801 = true ∧
    checkNat 802 = true ∧
    checkNat 803 = true ∧
    checkNat 804 = true ∧
    checkNat 805 = true ∧
    checkNat 806 = true ∧
    checkNat 807 = true ∧
    checkNat 808 = true ∧
    checkNat 809 = true ∧
    checkNat 810 = true ∧
    checkNat 811 = true ∧
    checkNat 812 = true ∧
    checkNat 813 = true ∧
    checkNat 814 = true ∧
    checkNat 815 = true ∧
    checkNat 816 = true ∧
    checkNat 817 = true ∧
    checkNat 818 = true ∧
    checkNat 819 = true ∧
    checkNat 820 = true ∧
    checkNat 821 = true ∧
    checkNat 822 = true ∧
    checkNat 823 = true ∧
    checkNat 824 = true ∧
    checkNat 825 = true ∧
    checkNat 826 = true ∧
    checkNat 827 = true ∧
    checkNat 828 = true ∧
    checkNat 829 = true ∧
    checkNat 830 = true ∧
    checkNat 831 = true ∧
    checkNat 1824 = true ∧
    checkNat 1826 = true ∧
    checkNat 1828 = true ∧
    checkNat 1830 = true ∧
    checkNat 1832 = true ∧
    checkNat 1834 = true ∧
    checkNat 1836 = true ∧
    checkNat 1838 = true ∧
    checkNat 1840 = true ∧
    checkNat 1842 = true ∧
    checkNat 1844 = true ∧
    checkNat 1846 = true ∧
    checkNat 1848 = true ∧
    checkNat 1850 = true ∧
    checkNat 1852 = true ∧
    checkNat 1854 = true ∧
    checkNat 2848 = true ∧
    checkNat 2849 = true ∧
    checkNat 2852 = true ∧
    checkNat 2853 = true ∧
    checkNat 2856 = true ∧
    checkNat 2857 = true ∧
    checkNat 2860 = true ∧
    checkNat 2861 = true ∧
    checkNat 2864 = true ∧
    checkNat 2865 = true ∧
    checkNat 2868 = true ∧
    checkNat 2869 = true ∧
    checkNat 2872 = true ∧
    checkNat 2873 = true ∧
    checkNat 2876 = true ∧
    checkNat 2877 = true ∧
    checkNat 3872 = true ∧
    checkNat 3876 = true ∧
    checkNat 3880 = true ∧
    checkNat 3884 = true ∧
    checkNat 3888 = true ∧
    checkNat 3892 = true ∧
    checkNat 3896 = true ∧
    checkNat 3900 = true := by
  exact ⟨case0800, case0801, case0802, case0803, case0804, case0805, case0806, case0807, case0808, case0809, case0810, case0811, case0812, case0813, case0814, case0815, case0816, case0817, case0818, case0819, case0820, case0821, case0822, case0823, case0824, case0825, case0826, case0827, case0828, case0829, case0830, case0831, case1824, case1826, case1828, case1830, case1832, case1834, case1836, case1838, case1840, case1842, case1844, case1846, case1848, case1850, case1852, case1854, case2848, case2849, case2852, case2853, case2856, case2857, case2860, case2861, case2864, case2865, case2868, case2869, case2872, case2873, case2876, case2877, case3872, case3876, case3880, case3884, case3888, case3892, case3896, case3900⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0800
