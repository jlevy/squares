import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1920
open Sq19.Endgame.Reduction

theorem case2818 : checkNat 2818 = true := by native_decide
#print axioms case2818

theorem case3842 : checkNat 3842 = true := by
  apply check_of_normalize (Case.ofNat 3842)
  have he : (Case.ofNat 3842).normalize = Case.ofNat 2818 := by decide
  rw [he]
  exact case2818
#print axioms case3842

theorem case2819 : checkNat 2819 = true := by native_decide
#print axioms case2819

theorem case2822 : checkNat 2822 = true := by native_decide
#print axioms case2822

theorem case3846 : checkNat 3846 = true := by
  apply check_of_normalize (Case.ofNat 3846)
  have he : (Case.ofNat 3846).normalize = Case.ofNat 2822 := by decide
  rw [he]
  exact case2822
#print axioms case3846

theorem case2823 : checkNat 2823 = true := by native_decide
#print axioms case2823

theorem case2826 : checkNat 2826 = true := by native_decide
#print axioms case2826

theorem case3850 : checkNat 3850 = true := by
  apply check_of_normalize (Case.ofNat 3850)
  have he : (Case.ofNat 3850).normalize = Case.ofNat 2826 := by decide
  rw [he]
  exact case2826
#print axioms case3850

theorem case2827 : checkNat 2827 = true := by native_decide
#print axioms case2827

theorem case2830 : checkNat 2830 = true := by native_decide
#print axioms case2830

theorem case3854 : checkNat 3854 = true := by
  apply check_of_normalize (Case.ofNat 3854)
  have he : (Case.ofNat 3854).normalize = Case.ofNat 2830 := by decide
  rw [he]
  exact case2830
#print axioms case3854

theorem case2831 : checkNat 2831 = true := by native_decide
#print axioms case2831

theorem case2834 : checkNat 2834 = true := by native_decide
#print axioms case2834

theorem case3858 : checkNat 3858 = true := by
  apply check_of_normalize (Case.ofNat 3858)
  have he : (Case.ofNat 3858).normalize = Case.ofNat 2834 := by decide
  rw [he]
  exact case2834
#print axioms case3858

theorem case2835 : checkNat 2835 = true := by native_decide
#print axioms case2835

theorem case2838 : checkNat 2838 = true := by native_decide
#print axioms case2838

theorem case3862 : checkNat 3862 = true := by
  apply check_of_normalize (Case.ofNat 3862)
  have he : (Case.ofNat 3862).normalize = Case.ofNat 2838 := by decide
  rw [he]
  exact case2838
#print axioms case3862

theorem case2839 : checkNat 2839 = true := by native_decide
#print axioms case2839

theorem case2842 : checkNat 2842 = true := by native_decide
#print axioms case2842

theorem case3866 : checkNat 3866 = true := by
  apply check_of_normalize (Case.ofNat 3866)
  have he : (Case.ofNat 3866).normalize = Case.ofNat 2842 := by decide
  rw [he]
  exact case2842
#print axioms case3866

theorem case2843 : checkNat 2843 = true := by native_decide
#print axioms case2843

theorem case2846 : checkNat 2846 = true := by native_decide
#print axioms case2846

theorem case3870 : checkNat 3870 = true := by
  apply check_of_normalize (Case.ofNat 3870)
  have he : (Case.ofNat 3870).normalize = Case.ofNat 2846 := by decide
  rw [he]
  exact case2846
#print axioms case3870

theorem case2847 : checkNat 2847 = true := by native_decide
#print axioms case2847

theorem case2850 : checkNat 2850 = true := by native_decide
#print axioms case2850

theorem case3874 : checkNat 3874 = true := by
  apply check_of_normalize (Case.ofNat 3874)
  have he : (Case.ofNat 3874).normalize = Case.ofNat 2850 := by decide
  rw [he]
  exact case2850
#print axioms case3874

theorem case2851 : checkNat 2851 = true := by native_decide
#print axioms case2851

theorem case2854 : checkNat 2854 = true := by native_decide
#print axioms case2854

theorem case3878 : checkNat 3878 = true := by
  apply check_of_normalize (Case.ofNat 3878)
  have he : (Case.ofNat 3878).normalize = Case.ofNat 2854 := by decide
  rw [he]
  exact case2854
#print axioms case3878

theorem case2855 : checkNat 2855 = true := by native_decide
#print axioms case2855

theorem case2858 : checkNat 2858 = true := by native_decide
#print axioms case2858

theorem case3882 : checkNat 3882 = true := by
  apply check_of_normalize (Case.ofNat 3882)
  have he : (Case.ofNat 3882).normalize = Case.ofNat 2858 := by decide
  rw [he]
  exact case2858
#print axioms case3882

theorem case2859 : checkNat 2859 = true := by native_decide
#print axioms case2859

theorem case2862 : checkNat 2862 = true := by native_decide
#print axioms case2862

theorem case3886 : checkNat 3886 = true := by
  apply check_of_normalize (Case.ofNat 3886)
  have he : (Case.ofNat 3886).normalize = Case.ofNat 2862 := by decide
  rw [he]
  exact case2862
#print axioms case3886

theorem case2863 : checkNat 2863 = true := by native_decide
#print axioms case2863

theorem case2866 : checkNat 2866 = true := by native_decide
#print axioms case2866

theorem case3890 : checkNat 3890 = true := by
  apply check_of_normalize (Case.ofNat 3890)
  have he : (Case.ofNat 3890).normalize = Case.ofNat 2866 := by decide
  rw [he]
  exact case2866
#print axioms case3890

theorem case2867 : checkNat 2867 = true := by native_decide
#print axioms case2867

theorem case2870 : checkNat 2870 = true := by native_decide
#print axioms case2870

theorem case3894 : checkNat 3894 = true := by
  apply check_of_normalize (Case.ofNat 3894)
  have he : (Case.ofNat 3894).normalize = Case.ofNat 2870 := by decide
  rw [he]
  exact case2870
#print axioms case3894

theorem case2871 : checkNat 2871 = true := by native_decide
#print axioms case2871

theorem case2874 : checkNat 2874 = true := by native_decide
#print axioms case2874

theorem case3898 : checkNat 3898 = true := by
  apply check_of_normalize (Case.ofNat 3898)
  have he : (Case.ofNat 3898).normalize = Case.ofNat 2874 := by decide
  rw [he]
  exact case2874
#print axioms case3898

theorem case2875 : checkNat 2875 = true := by native_decide
#print axioms case2875

theorem case2878 : checkNat 2878 = true := by native_decide
#print axioms case2878

theorem case3902 : checkNat 3902 = true := by
  apply check_of_normalize (Case.ofNat 3902)
  have he : (Case.ofNat 3902).normalize = Case.ofNat 2878 := by decide
  rw [he]
  exact case2878
#print axioms case3902

theorem case2879 : checkNat 2879 = true := by native_decide
#print axioms case2879

theorem accepted :
    checkNat 2818 = true ∧
    checkNat 2819 = true ∧
    checkNat 2822 = true ∧
    checkNat 2823 = true ∧
    checkNat 2826 = true ∧
    checkNat 2827 = true ∧
    checkNat 2830 = true ∧
    checkNat 2831 = true ∧
    checkNat 2834 = true ∧
    checkNat 2835 = true ∧
    checkNat 2838 = true ∧
    checkNat 2839 = true ∧
    checkNat 2842 = true ∧
    checkNat 2843 = true ∧
    checkNat 2846 = true ∧
    checkNat 2847 = true ∧
    checkNat 2850 = true ∧
    checkNat 2851 = true ∧
    checkNat 2854 = true ∧
    checkNat 2855 = true ∧
    checkNat 2858 = true ∧
    checkNat 2859 = true ∧
    checkNat 2862 = true ∧
    checkNat 2863 = true ∧
    checkNat 2866 = true ∧
    checkNat 2867 = true ∧
    checkNat 2870 = true ∧
    checkNat 2871 = true ∧
    checkNat 2874 = true ∧
    checkNat 2875 = true ∧
    checkNat 2878 = true ∧
    checkNat 2879 = true ∧
    checkNat 3842 = true ∧
    checkNat 3846 = true ∧
    checkNat 3850 = true ∧
    checkNat 3854 = true ∧
    checkNat 3858 = true ∧
    checkNat 3862 = true ∧
    checkNat 3866 = true ∧
    checkNat 3870 = true ∧
    checkNat 3874 = true ∧
    checkNat 3878 = true ∧
    checkNat 3882 = true ∧
    checkNat 3886 = true ∧
    checkNat 3890 = true ∧
    checkNat 3894 = true ∧
    checkNat 3898 = true ∧
    checkNat 3902 = true := by
  exact ⟨case2818, case2819, case2822, case2823, case2826, case2827, case2830, case2831, case2834, case2835, case2838, case2839, case2842, case2843, case2846, case2847, case2850, case2851, case2854, case2855, case2858, case2859, case2862, case2863, case2866, case2867, case2870, case2871, case2874, case2875, case2878, case2879, case3842, case3846, case3850, case3854, case3858, case3862, case3866, case3870, case3874, case3878, case3882, case3886, case3890, case3894, case3898, case3902⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1920
