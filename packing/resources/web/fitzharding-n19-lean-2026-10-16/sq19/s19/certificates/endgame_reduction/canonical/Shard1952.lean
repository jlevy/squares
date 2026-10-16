import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1952
open Sq19.Endgame.Reduction

theorem case2882 : checkNat 2882 = true := by native_decide
#print axioms case2882

theorem case3906 : checkNat 3906 = true := by
  apply check_of_normalize (Case.ofNat 3906)
  have he : (Case.ofNat 3906).normalize = Case.ofNat 2882 := by decide
  rw [he]
  exact case2882
#print axioms case3906

theorem case2883 : checkNat 2883 = true := by native_decide
#print axioms case2883

theorem case2886 : checkNat 2886 = true := by native_decide
#print axioms case2886

theorem case3910 : checkNat 3910 = true := by
  apply check_of_normalize (Case.ofNat 3910)
  have he : (Case.ofNat 3910).normalize = Case.ofNat 2886 := by decide
  rw [he]
  exact case2886
#print axioms case3910

theorem case2887 : checkNat 2887 = true := by native_decide
#print axioms case2887

theorem case2890 : checkNat 2890 = true := by native_decide
#print axioms case2890

theorem case3914 : checkNat 3914 = true := by
  apply check_of_normalize (Case.ofNat 3914)
  have he : (Case.ofNat 3914).normalize = Case.ofNat 2890 := by decide
  rw [he]
  exact case2890
#print axioms case3914

theorem case2891 : checkNat 2891 = true := by native_decide
#print axioms case2891

theorem case2894 : checkNat 2894 = true := by native_decide
#print axioms case2894

theorem case3918 : checkNat 3918 = true := by
  apply check_of_normalize (Case.ofNat 3918)
  have he : (Case.ofNat 3918).normalize = Case.ofNat 2894 := by decide
  rw [he]
  exact case2894
#print axioms case3918

theorem case2895 : checkNat 2895 = true := by native_decide
#print axioms case2895

theorem case2898 : checkNat 2898 = true := by native_decide
#print axioms case2898

theorem case3922 : checkNat 3922 = true := by
  apply check_of_normalize (Case.ofNat 3922)
  have he : (Case.ofNat 3922).normalize = Case.ofNat 2898 := by decide
  rw [he]
  exact case2898
#print axioms case3922

theorem case2899 : checkNat 2899 = true := by native_decide
#print axioms case2899

theorem case2902 : checkNat 2902 = true := by native_decide
#print axioms case2902

theorem case3926 : checkNat 3926 = true := by
  apply check_of_normalize (Case.ofNat 3926)
  have he : (Case.ofNat 3926).normalize = Case.ofNat 2902 := by decide
  rw [he]
  exact case2902
#print axioms case3926

theorem case2903 : checkNat 2903 = true := by native_decide
#print axioms case2903

theorem case2906 : checkNat 2906 = true := by native_decide
#print axioms case2906

theorem case3930 : checkNat 3930 = true := by
  apply check_of_normalize (Case.ofNat 3930)
  have he : (Case.ofNat 3930).normalize = Case.ofNat 2906 := by decide
  rw [he]
  exact case2906
#print axioms case3930

theorem case2907 : checkNat 2907 = true := by native_decide
#print axioms case2907

theorem case2910 : checkNat 2910 = true := by native_decide
#print axioms case2910

theorem case3934 : checkNat 3934 = true := by
  apply check_of_normalize (Case.ofNat 3934)
  have he : (Case.ofNat 3934).normalize = Case.ofNat 2910 := by decide
  rw [he]
  exact case2910
#print axioms case3934

theorem case2911 : checkNat 2911 = true := by native_decide
#print axioms case2911

theorem case2914 : checkNat 2914 = true := by native_decide
#print axioms case2914

theorem case3938 : checkNat 3938 = true := by
  apply check_of_normalize (Case.ofNat 3938)
  have he : (Case.ofNat 3938).normalize = Case.ofNat 2914 := by decide
  rw [he]
  exact case2914
#print axioms case3938

theorem case2915 : checkNat 2915 = true := by native_decide
#print axioms case2915

theorem case2918 : checkNat 2918 = true := by native_decide
#print axioms case2918

theorem case3942 : checkNat 3942 = true := by
  apply check_of_normalize (Case.ofNat 3942)
  have he : (Case.ofNat 3942).normalize = Case.ofNat 2918 := by decide
  rw [he]
  exact case2918
#print axioms case3942

theorem case2919 : checkNat 2919 = true := by native_decide
#print axioms case2919

theorem case2922 : checkNat 2922 = true := by native_decide
#print axioms case2922

theorem case3946 : checkNat 3946 = true := by
  apply check_of_normalize (Case.ofNat 3946)
  have he : (Case.ofNat 3946).normalize = Case.ofNat 2922 := by decide
  rw [he]
  exact case2922
#print axioms case3946

theorem case2923 : checkNat 2923 = true := by native_decide
#print axioms case2923

theorem case2926 : checkNat 2926 = true := by native_decide
#print axioms case2926

theorem case3950 : checkNat 3950 = true := by
  apply check_of_normalize (Case.ofNat 3950)
  have he : (Case.ofNat 3950).normalize = Case.ofNat 2926 := by decide
  rw [he]
  exact case2926
#print axioms case3950

theorem case2927 : checkNat 2927 = true := by native_decide
#print axioms case2927

theorem case2930 : checkNat 2930 = true := by native_decide
#print axioms case2930

theorem case3954 : checkNat 3954 = true := by
  apply check_of_normalize (Case.ofNat 3954)
  have he : (Case.ofNat 3954).normalize = Case.ofNat 2930 := by decide
  rw [he]
  exact case2930
#print axioms case3954

theorem case2931 : checkNat 2931 = true := by native_decide
#print axioms case2931

theorem case2934 : checkNat 2934 = true := by native_decide
#print axioms case2934

theorem case3958 : checkNat 3958 = true := by
  apply check_of_normalize (Case.ofNat 3958)
  have he : (Case.ofNat 3958).normalize = Case.ofNat 2934 := by decide
  rw [he]
  exact case2934
#print axioms case3958

theorem case2935 : checkNat 2935 = true := by native_decide
#print axioms case2935

theorem case2938 : checkNat 2938 = true := by native_decide
#print axioms case2938

theorem case3962 : checkNat 3962 = true := by
  apply check_of_normalize (Case.ofNat 3962)
  have he : (Case.ofNat 3962).normalize = Case.ofNat 2938 := by decide
  rw [he]
  exact case2938
#print axioms case3962

theorem case2939 : checkNat 2939 = true := by native_decide
#print axioms case2939

theorem case2942 : checkNat 2942 = true := by native_decide
#print axioms case2942

theorem case3966 : checkNat 3966 = true := by
  apply check_of_normalize (Case.ofNat 3966)
  have he : (Case.ofNat 3966).normalize = Case.ofNat 2942 := by decide
  rw [he]
  exact case2942
#print axioms case3966

theorem case2943 : checkNat 2943 = true := by native_decide
#print axioms case2943

theorem accepted :
    checkNat 2882 = true ∧
    checkNat 2883 = true ∧
    checkNat 2886 = true ∧
    checkNat 2887 = true ∧
    checkNat 2890 = true ∧
    checkNat 2891 = true ∧
    checkNat 2894 = true ∧
    checkNat 2895 = true ∧
    checkNat 2898 = true ∧
    checkNat 2899 = true ∧
    checkNat 2902 = true ∧
    checkNat 2903 = true ∧
    checkNat 2906 = true ∧
    checkNat 2907 = true ∧
    checkNat 2910 = true ∧
    checkNat 2911 = true ∧
    checkNat 2914 = true ∧
    checkNat 2915 = true ∧
    checkNat 2918 = true ∧
    checkNat 2919 = true ∧
    checkNat 2922 = true ∧
    checkNat 2923 = true ∧
    checkNat 2926 = true ∧
    checkNat 2927 = true ∧
    checkNat 2930 = true ∧
    checkNat 2931 = true ∧
    checkNat 2934 = true ∧
    checkNat 2935 = true ∧
    checkNat 2938 = true ∧
    checkNat 2939 = true ∧
    checkNat 2942 = true ∧
    checkNat 2943 = true ∧
    checkNat 3906 = true ∧
    checkNat 3910 = true ∧
    checkNat 3914 = true ∧
    checkNat 3918 = true ∧
    checkNat 3922 = true ∧
    checkNat 3926 = true ∧
    checkNat 3930 = true ∧
    checkNat 3934 = true ∧
    checkNat 3938 = true ∧
    checkNat 3942 = true ∧
    checkNat 3946 = true ∧
    checkNat 3950 = true ∧
    checkNat 3954 = true ∧
    checkNat 3958 = true ∧
    checkNat 3962 = true ∧
    checkNat 3966 = true := by
  exact ⟨case2882, case2883, case2886, case2887, case2890, case2891, case2894, case2895, case2898, case2899, case2902, case2903, case2906, case2907, case2910, case2911, case2914, case2915, case2918, case2919, case2922, case2923, case2926, case2927, case2930, case2931, case2934, case2935, case2938, case2939, case2942, case2943, case3906, case3910, case3914, case3918, case3922, case3926, case3930, case3934, case3938, case3942, case3946, case3950, case3954, case3958, case3962, case3966⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1952
