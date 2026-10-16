import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0832
open Sq19.Endgame.Reduction

theorem case0832 : checkNat 832 = true := by native_decide
#print axioms case0832

theorem case1856 : checkNat 1856 = true := by
  apply check_of_normalize (Case.ofNat 1856)
  have he : (Case.ofNat 1856).normalize = Case.ofNat 832 := by decide
  rw [he]
  exact case0832
#print axioms case1856

theorem case2880 : checkNat 2880 = true := by
  apply check_of_normalize (Case.ofNat 2880)
  have he : (Case.ofNat 2880).normalize = Case.ofNat 832 := by decide
  rw [he]
  exact case0832
#print axioms case2880

theorem case3904 : checkNat 3904 = true := by
  apply check_of_normalize (Case.ofNat 3904)
  have he : (Case.ofNat 3904).normalize = Case.ofNat 832 := by decide
  rw [he]
  exact case0832
#print axioms case3904

theorem case0833 : checkNat 833 = true := by native_decide
#print axioms case0833

theorem case2881 : checkNat 2881 = true := by
  apply check_of_normalize (Case.ofNat 2881)
  have he : (Case.ofNat 2881).normalize = Case.ofNat 833 := by decide
  rw [he]
  exact case0833
#print axioms case2881

theorem case0834 : checkNat 834 = true := by native_decide
#print axioms case0834

theorem case1858 : checkNat 1858 = true := by
  apply check_of_normalize (Case.ofNat 1858)
  have he : (Case.ofNat 1858).normalize = Case.ofNat 834 := by decide
  rw [he]
  exact case0834
#print axioms case1858

theorem case0835 : checkNat 835 = true := by native_decide
#print axioms case0835

theorem case0836 : checkNat 836 = true := by native_decide
#print axioms case0836

theorem case1860 : checkNat 1860 = true := by
  apply check_of_normalize (Case.ofNat 1860)
  have he : (Case.ofNat 1860).normalize = Case.ofNat 836 := by decide
  rw [he]
  exact case0836
#print axioms case1860

theorem case2884 : checkNat 2884 = true := by
  apply check_of_normalize (Case.ofNat 2884)
  have he : (Case.ofNat 2884).normalize = Case.ofNat 836 := by decide
  rw [he]
  exact case0836
#print axioms case2884

theorem case3908 : checkNat 3908 = true := by
  apply check_of_normalize (Case.ofNat 3908)
  have he : (Case.ofNat 3908).normalize = Case.ofNat 836 := by decide
  rw [he]
  exact case0836
#print axioms case3908

theorem case0837 : checkNat 837 = true := by native_decide
#print axioms case0837

theorem case2885 : checkNat 2885 = true := by
  apply check_of_normalize (Case.ofNat 2885)
  have he : (Case.ofNat 2885).normalize = Case.ofNat 837 := by decide
  rw [he]
  exact case0837
#print axioms case2885

theorem case0838 : checkNat 838 = true := by native_decide
#print axioms case0838

theorem case1862 : checkNat 1862 = true := by
  apply check_of_normalize (Case.ofNat 1862)
  have he : (Case.ofNat 1862).normalize = Case.ofNat 838 := by decide
  rw [he]
  exact case0838
#print axioms case1862

theorem case0839 : checkNat 839 = true := by native_decide
#print axioms case0839

theorem case0840 : checkNat 840 = true := by native_decide
#print axioms case0840

theorem case1864 : checkNat 1864 = true := by
  apply check_of_normalize (Case.ofNat 1864)
  have he : (Case.ofNat 1864).normalize = Case.ofNat 840 := by decide
  rw [he]
  exact case0840
#print axioms case1864

theorem case2888 : checkNat 2888 = true := by
  apply check_of_normalize (Case.ofNat 2888)
  have he : (Case.ofNat 2888).normalize = Case.ofNat 840 := by decide
  rw [he]
  exact case0840
#print axioms case2888

theorem case3912 : checkNat 3912 = true := by
  apply check_of_normalize (Case.ofNat 3912)
  have he : (Case.ofNat 3912).normalize = Case.ofNat 840 := by decide
  rw [he]
  exact case0840
#print axioms case3912

theorem case0841 : checkNat 841 = true := by native_decide
#print axioms case0841

theorem case2889 : checkNat 2889 = true := by
  apply check_of_normalize (Case.ofNat 2889)
  have he : (Case.ofNat 2889).normalize = Case.ofNat 841 := by decide
  rw [he]
  exact case0841
#print axioms case2889

theorem case0842 : checkNat 842 = true := by native_decide
#print axioms case0842

theorem case1866 : checkNat 1866 = true := by
  apply check_of_normalize (Case.ofNat 1866)
  have he : (Case.ofNat 1866).normalize = Case.ofNat 842 := by decide
  rw [he]
  exact case0842
#print axioms case1866

theorem case0843 : checkNat 843 = true := by native_decide
#print axioms case0843

theorem case0844 : checkNat 844 = true := by native_decide
#print axioms case0844

theorem case1868 : checkNat 1868 = true := by
  apply check_of_normalize (Case.ofNat 1868)
  have he : (Case.ofNat 1868).normalize = Case.ofNat 844 := by decide
  rw [he]
  exact case0844
#print axioms case1868

theorem case2892 : checkNat 2892 = true := by
  apply check_of_normalize (Case.ofNat 2892)
  have he : (Case.ofNat 2892).normalize = Case.ofNat 844 := by decide
  rw [he]
  exact case0844
#print axioms case2892

theorem case3916 : checkNat 3916 = true := by
  apply check_of_normalize (Case.ofNat 3916)
  have he : (Case.ofNat 3916).normalize = Case.ofNat 844 := by decide
  rw [he]
  exact case0844
#print axioms case3916

theorem case0845 : checkNat 845 = true := by native_decide
#print axioms case0845

theorem case2893 : checkNat 2893 = true := by
  apply check_of_normalize (Case.ofNat 2893)
  have he : (Case.ofNat 2893).normalize = Case.ofNat 845 := by decide
  rw [he]
  exact case0845
#print axioms case2893

theorem case0846 : checkNat 846 = true := by native_decide
#print axioms case0846

theorem case1870 : checkNat 1870 = true := by
  apply check_of_normalize (Case.ofNat 1870)
  have he : (Case.ofNat 1870).normalize = Case.ofNat 846 := by decide
  rw [he]
  exact case0846
#print axioms case1870

theorem case0847 : checkNat 847 = true := by native_decide
#print axioms case0847

theorem case0848 : checkNat 848 = true := by native_decide
#print axioms case0848

theorem case1872 : checkNat 1872 = true := by
  apply check_of_normalize (Case.ofNat 1872)
  have he : (Case.ofNat 1872).normalize = Case.ofNat 848 := by decide
  rw [he]
  exact case0848
#print axioms case1872

theorem case2896 : checkNat 2896 = true := by
  apply check_of_normalize (Case.ofNat 2896)
  have he : (Case.ofNat 2896).normalize = Case.ofNat 848 := by decide
  rw [he]
  exact case0848
#print axioms case2896

theorem case3920 : checkNat 3920 = true := by
  apply check_of_normalize (Case.ofNat 3920)
  have he : (Case.ofNat 3920).normalize = Case.ofNat 848 := by decide
  rw [he]
  exact case0848
#print axioms case3920

theorem case0849 : checkNat 849 = true := by native_decide
#print axioms case0849

theorem case2897 : checkNat 2897 = true := by
  apply check_of_normalize (Case.ofNat 2897)
  have he : (Case.ofNat 2897).normalize = Case.ofNat 849 := by decide
  rw [he]
  exact case0849
#print axioms case2897

theorem case0850 : checkNat 850 = true := by native_decide
#print axioms case0850

theorem case1874 : checkNat 1874 = true := by
  apply check_of_normalize (Case.ofNat 1874)
  have he : (Case.ofNat 1874).normalize = Case.ofNat 850 := by decide
  rw [he]
  exact case0850
#print axioms case1874

theorem case0851 : checkNat 851 = true := by native_decide
#print axioms case0851

theorem case0852 : checkNat 852 = true := by native_decide
#print axioms case0852

theorem case1876 : checkNat 1876 = true := by
  apply check_of_normalize (Case.ofNat 1876)
  have he : (Case.ofNat 1876).normalize = Case.ofNat 852 := by decide
  rw [he]
  exact case0852
#print axioms case1876

theorem case2900 : checkNat 2900 = true := by
  apply check_of_normalize (Case.ofNat 2900)
  have he : (Case.ofNat 2900).normalize = Case.ofNat 852 := by decide
  rw [he]
  exact case0852
#print axioms case2900

theorem case3924 : checkNat 3924 = true := by
  apply check_of_normalize (Case.ofNat 3924)
  have he : (Case.ofNat 3924).normalize = Case.ofNat 852 := by decide
  rw [he]
  exact case0852
#print axioms case3924

theorem case0853 : checkNat 853 = true := by native_decide
#print axioms case0853

theorem case2901 : checkNat 2901 = true := by
  apply check_of_normalize (Case.ofNat 2901)
  have he : (Case.ofNat 2901).normalize = Case.ofNat 853 := by decide
  rw [he]
  exact case0853
#print axioms case2901

theorem case0854 : checkNat 854 = true := by native_decide
#print axioms case0854

theorem case1878 : checkNat 1878 = true := by
  apply check_of_normalize (Case.ofNat 1878)
  have he : (Case.ofNat 1878).normalize = Case.ofNat 854 := by decide
  rw [he]
  exact case0854
#print axioms case1878

theorem case0855 : checkNat 855 = true := by native_decide
#print axioms case0855

theorem case0856 : checkNat 856 = true := by native_decide
#print axioms case0856

theorem case1880 : checkNat 1880 = true := by
  apply check_of_normalize (Case.ofNat 1880)
  have he : (Case.ofNat 1880).normalize = Case.ofNat 856 := by decide
  rw [he]
  exact case0856
#print axioms case1880

theorem case2904 : checkNat 2904 = true := by
  apply check_of_normalize (Case.ofNat 2904)
  have he : (Case.ofNat 2904).normalize = Case.ofNat 856 := by decide
  rw [he]
  exact case0856
#print axioms case2904

theorem case3928 : checkNat 3928 = true := by
  apply check_of_normalize (Case.ofNat 3928)
  have he : (Case.ofNat 3928).normalize = Case.ofNat 856 := by decide
  rw [he]
  exact case0856
#print axioms case3928

theorem case0857 : checkNat 857 = true := by native_decide
#print axioms case0857

theorem case2905 : checkNat 2905 = true := by
  apply check_of_normalize (Case.ofNat 2905)
  have he : (Case.ofNat 2905).normalize = Case.ofNat 857 := by decide
  rw [he]
  exact case0857
#print axioms case2905

theorem case0858 : checkNat 858 = true := by native_decide
#print axioms case0858

theorem case1882 : checkNat 1882 = true := by
  apply check_of_normalize (Case.ofNat 1882)
  have he : (Case.ofNat 1882).normalize = Case.ofNat 858 := by decide
  rw [he]
  exact case0858
#print axioms case1882

theorem case0859 : checkNat 859 = true := by native_decide
#print axioms case0859

theorem case0860 : checkNat 860 = true := by native_decide
#print axioms case0860

theorem case1884 : checkNat 1884 = true := by
  apply check_of_normalize (Case.ofNat 1884)
  have he : (Case.ofNat 1884).normalize = Case.ofNat 860 := by decide
  rw [he]
  exact case0860
#print axioms case1884

theorem case2908 : checkNat 2908 = true := by
  apply check_of_normalize (Case.ofNat 2908)
  have he : (Case.ofNat 2908).normalize = Case.ofNat 860 := by decide
  rw [he]
  exact case0860
#print axioms case2908

theorem case3932 : checkNat 3932 = true := by
  apply check_of_normalize (Case.ofNat 3932)
  have he : (Case.ofNat 3932).normalize = Case.ofNat 860 := by decide
  rw [he]
  exact case0860
#print axioms case3932

theorem case0861 : checkNat 861 = true := by native_decide
#print axioms case0861

theorem case2909 : checkNat 2909 = true := by
  apply check_of_normalize (Case.ofNat 2909)
  have he : (Case.ofNat 2909).normalize = Case.ofNat 861 := by decide
  rw [he]
  exact case0861
#print axioms case2909

theorem case0862 : checkNat 862 = true := by native_decide
#print axioms case0862

theorem case1886 : checkNat 1886 = true := by
  apply check_of_normalize (Case.ofNat 1886)
  have he : (Case.ofNat 1886).normalize = Case.ofNat 862 := by decide
  rw [he]
  exact case0862
#print axioms case1886

theorem case0863 : checkNat 863 = true := by native_decide
#print axioms case0863

theorem accepted :
    checkNat 832 = true ∧
    checkNat 833 = true ∧
    checkNat 834 = true ∧
    checkNat 835 = true ∧
    checkNat 836 = true ∧
    checkNat 837 = true ∧
    checkNat 838 = true ∧
    checkNat 839 = true ∧
    checkNat 840 = true ∧
    checkNat 841 = true ∧
    checkNat 842 = true ∧
    checkNat 843 = true ∧
    checkNat 844 = true ∧
    checkNat 845 = true ∧
    checkNat 846 = true ∧
    checkNat 847 = true ∧
    checkNat 848 = true ∧
    checkNat 849 = true ∧
    checkNat 850 = true ∧
    checkNat 851 = true ∧
    checkNat 852 = true ∧
    checkNat 853 = true ∧
    checkNat 854 = true ∧
    checkNat 855 = true ∧
    checkNat 856 = true ∧
    checkNat 857 = true ∧
    checkNat 858 = true ∧
    checkNat 859 = true ∧
    checkNat 860 = true ∧
    checkNat 861 = true ∧
    checkNat 862 = true ∧
    checkNat 863 = true ∧
    checkNat 1856 = true ∧
    checkNat 1858 = true ∧
    checkNat 1860 = true ∧
    checkNat 1862 = true ∧
    checkNat 1864 = true ∧
    checkNat 1866 = true ∧
    checkNat 1868 = true ∧
    checkNat 1870 = true ∧
    checkNat 1872 = true ∧
    checkNat 1874 = true ∧
    checkNat 1876 = true ∧
    checkNat 1878 = true ∧
    checkNat 1880 = true ∧
    checkNat 1882 = true ∧
    checkNat 1884 = true ∧
    checkNat 1886 = true ∧
    checkNat 2880 = true ∧
    checkNat 2881 = true ∧
    checkNat 2884 = true ∧
    checkNat 2885 = true ∧
    checkNat 2888 = true ∧
    checkNat 2889 = true ∧
    checkNat 2892 = true ∧
    checkNat 2893 = true ∧
    checkNat 2896 = true ∧
    checkNat 2897 = true ∧
    checkNat 2900 = true ∧
    checkNat 2901 = true ∧
    checkNat 2904 = true ∧
    checkNat 2905 = true ∧
    checkNat 2908 = true ∧
    checkNat 2909 = true ∧
    checkNat 3904 = true ∧
    checkNat 3908 = true ∧
    checkNat 3912 = true ∧
    checkNat 3916 = true ∧
    checkNat 3920 = true ∧
    checkNat 3924 = true ∧
    checkNat 3928 = true ∧
    checkNat 3932 = true := by
  exact ⟨case0832, case0833, case0834, case0835, case0836, case0837, case0838, case0839, case0840, case0841, case0842, case0843, case0844, case0845, case0846, case0847, case0848, case0849, case0850, case0851, case0852, case0853, case0854, case0855, case0856, case0857, case0858, case0859, case0860, case0861, case0862, case0863, case1856, case1858, case1860, case1862, case1864, case1866, case1868, case1870, case1872, case1874, case1876, case1878, case1880, case1882, case1884, case1886, case2880, case2881, case2884, case2885, case2888, case2889, case2892, case2893, case2896, case2897, case2900, case2901, case2904, case2905, case2908, case2909, case3904, case3908, case3912, case3916, case3920, case3924, case3928, case3932⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0832
