import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1440
open Sq19.Endgame.Reduction

theorem case1857 : checkNat 1857 = true := by native_decide
#print axioms case1857

theorem case3905 : checkNat 3905 = true := by
  apply check_of_normalize (Case.ofNat 3905)
  have he : (Case.ofNat 3905).normalize = Case.ofNat 1857 := by decide
  rw [he]
  exact case1857
#print axioms case3905

theorem case1859 : checkNat 1859 = true := by native_decide
#print axioms case1859

theorem case1861 : checkNat 1861 = true := by native_decide
#print axioms case1861

theorem case3909 : checkNat 3909 = true := by
  apply check_of_normalize (Case.ofNat 3909)
  have he : (Case.ofNat 3909).normalize = Case.ofNat 1861 := by decide
  rw [he]
  exact case1861
#print axioms case3909

theorem case1863 : checkNat 1863 = true := by native_decide
#print axioms case1863

theorem case1865 : checkNat 1865 = true := by native_decide
#print axioms case1865

theorem case3913 : checkNat 3913 = true := by
  apply check_of_normalize (Case.ofNat 3913)
  have he : (Case.ofNat 3913).normalize = Case.ofNat 1865 := by decide
  rw [he]
  exact case1865
#print axioms case3913

theorem case1867 : checkNat 1867 = true := by native_decide
#print axioms case1867

theorem case1869 : checkNat 1869 = true := by native_decide
#print axioms case1869

theorem case3917 : checkNat 3917 = true := by
  apply check_of_normalize (Case.ofNat 3917)
  have he : (Case.ofNat 3917).normalize = Case.ofNat 1869 := by decide
  rw [he]
  exact case1869
#print axioms case3917

theorem case1871 : checkNat 1871 = true := by native_decide
#print axioms case1871

theorem case1873 : checkNat 1873 = true := by native_decide
#print axioms case1873

theorem case3921 : checkNat 3921 = true := by
  apply check_of_normalize (Case.ofNat 3921)
  have he : (Case.ofNat 3921).normalize = Case.ofNat 1873 := by decide
  rw [he]
  exact case1873
#print axioms case3921

theorem case1875 : checkNat 1875 = true := by native_decide
#print axioms case1875

theorem case1877 : checkNat 1877 = true := by native_decide
#print axioms case1877

theorem case3925 : checkNat 3925 = true := by
  apply check_of_normalize (Case.ofNat 3925)
  have he : (Case.ofNat 3925).normalize = Case.ofNat 1877 := by decide
  rw [he]
  exact case1877
#print axioms case3925

theorem case1879 : checkNat 1879 = true := by native_decide
#print axioms case1879

theorem case1881 : checkNat 1881 = true := by native_decide
#print axioms case1881

theorem case3929 : checkNat 3929 = true := by
  apply check_of_normalize (Case.ofNat 3929)
  have he : (Case.ofNat 3929).normalize = Case.ofNat 1881 := by decide
  rw [he]
  exact case1881
#print axioms case3929

theorem case1883 : checkNat 1883 = true := by native_decide
#print axioms case1883

theorem case1885 : checkNat 1885 = true := by native_decide
#print axioms case1885

theorem case3933 : checkNat 3933 = true := by
  apply check_of_normalize (Case.ofNat 3933)
  have he : (Case.ofNat 3933).normalize = Case.ofNat 1885 := by decide
  rw [he]
  exact case1885
#print axioms case3933

theorem case1887 : checkNat 1887 = true := by native_decide
#print axioms case1887

theorem case1889 : checkNat 1889 = true := by native_decide
#print axioms case1889

theorem case3937 : checkNat 3937 = true := by
  apply check_of_normalize (Case.ofNat 3937)
  have he : (Case.ofNat 3937).normalize = Case.ofNat 1889 := by decide
  rw [he]
  exact case1889
#print axioms case3937

theorem case1891 : checkNat 1891 = true := by native_decide
#print axioms case1891

theorem case1893 : checkNat 1893 = true := by native_decide
#print axioms case1893

theorem case3941 : checkNat 3941 = true := by
  apply check_of_normalize (Case.ofNat 3941)
  have he : (Case.ofNat 3941).normalize = Case.ofNat 1893 := by decide
  rw [he]
  exact case1893
#print axioms case3941

theorem case1895 : checkNat 1895 = true := by native_decide
#print axioms case1895

theorem case1897 : checkNat 1897 = true := by native_decide
#print axioms case1897

theorem case3945 : checkNat 3945 = true := by
  apply check_of_normalize (Case.ofNat 3945)
  have he : (Case.ofNat 3945).normalize = Case.ofNat 1897 := by decide
  rw [he]
  exact case1897
#print axioms case3945

theorem case1899 : checkNat 1899 = true := by native_decide
#print axioms case1899

theorem case1901 : checkNat 1901 = true := by native_decide
#print axioms case1901

theorem case3949 : checkNat 3949 = true := by
  apply check_of_normalize (Case.ofNat 3949)
  have he : (Case.ofNat 3949).normalize = Case.ofNat 1901 := by decide
  rw [he]
  exact case1901
#print axioms case3949

theorem case1903 : checkNat 1903 = true := by native_decide
#print axioms case1903

theorem case1905 : checkNat 1905 = true := by native_decide
#print axioms case1905

theorem case3953 : checkNat 3953 = true := by
  apply check_of_normalize (Case.ofNat 3953)
  have he : (Case.ofNat 3953).normalize = Case.ofNat 1905 := by decide
  rw [he]
  exact case1905
#print axioms case3953

theorem case1907 : checkNat 1907 = true := by native_decide
#print axioms case1907

theorem case1909 : checkNat 1909 = true := by native_decide
#print axioms case1909

theorem case3957 : checkNat 3957 = true := by
  apply check_of_normalize (Case.ofNat 3957)
  have he : (Case.ofNat 3957).normalize = Case.ofNat 1909 := by decide
  rw [he]
  exact case1909
#print axioms case3957

theorem case1911 : checkNat 1911 = true := by native_decide
#print axioms case1911

theorem case1913 : checkNat 1913 = true := by native_decide
#print axioms case1913

theorem case3961 : checkNat 3961 = true := by
  apply check_of_normalize (Case.ofNat 3961)
  have he : (Case.ofNat 3961).normalize = Case.ofNat 1913 := by decide
  rw [he]
  exact case1913
#print axioms case3961

theorem case1915 : checkNat 1915 = true := by native_decide
#print axioms case1915

theorem case1917 : checkNat 1917 = true := by native_decide
#print axioms case1917

theorem case3965 : checkNat 3965 = true := by
  apply check_of_normalize (Case.ofNat 3965)
  have he : (Case.ofNat 3965).normalize = Case.ofNat 1917 := by decide
  rw [he]
  exact case1917
#print axioms case3965

theorem case1919 : checkNat 1919 = true := by native_decide
#print axioms case1919

theorem accepted :
    checkNat 1857 = true ∧
    checkNat 1859 = true ∧
    checkNat 1861 = true ∧
    checkNat 1863 = true ∧
    checkNat 1865 = true ∧
    checkNat 1867 = true ∧
    checkNat 1869 = true ∧
    checkNat 1871 = true ∧
    checkNat 1873 = true ∧
    checkNat 1875 = true ∧
    checkNat 1877 = true ∧
    checkNat 1879 = true ∧
    checkNat 1881 = true ∧
    checkNat 1883 = true ∧
    checkNat 1885 = true ∧
    checkNat 1887 = true ∧
    checkNat 1889 = true ∧
    checkNat 1891 = true ∧
    checkNat 1893 = true ∧
    checkNat 1895 = true ∧
    checkNat 1897 = true ∧
    checkNat 1899 = true ∧
    checkNat 1901 = true ∧
    checkNat 1903 = true ∧
    checkNat 1905 = true ∧
    checkNat 1907 = true ∧
    checkNat 1909 = true ∧
    checkNat 1911 = true ∧
    checkNat 1913 = true ∧
    checkNat 1915 = true ∧
    checkNat 1917 = true ∧
    checkNat 1919 = true ∧
    checkNat 3905 = true ∧
    checkNat 3909 = true ∧
    checkNat 3913 = true ∧
    checkNat 3917 = true ∧
    checkNat 3921 = true ∧
    checkNat 3925 = true ∧
    checkNat 3929 = true ∧
    checkNat 3933 = true ∧
    checkNat 3937 = true ∧
    checkNat 3941 = true ∧
    checkNat 3945 = true ∧
    checkNat 3949 = true ∧
    checkNat 3953 = true ∧
    checkNat 3957 = true ∧
    checkNat 3961 = true ∧
    checkNat 3965 = true := by
  exact ⟨case1857, case1859, case1861, case1863, case1865, case1867, case1869, case1871, case1873, case1875, case1877, case1879, case1881, case1883, case1885, case1887, case1889, case1891, case1893, case1895, case1897, case1899, case1901, case1903, case1905, case1907, case1909, case1911, case1913, case1915, case1917, case1919, case3905, case3909, case3913, case3917, case3921, case3925, case3929, case3933, case3937, case3941, case3945, case3949, case3953, case3957, case3961, case3965⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1440
