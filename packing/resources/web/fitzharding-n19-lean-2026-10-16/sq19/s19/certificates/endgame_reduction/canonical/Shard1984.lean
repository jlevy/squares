import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1984
open Sq19.Endgame.Reduction

theorem case2946 : checkNat 2946 = true := by native_decide
#print axioms case2946

theorem case3970 : checkNat 3970 = true := by
  apply check_of_normalize (Case.ofNat 3970)
  have he : (Case.ofNat 3970).normalize = Case.ofNat 2946 := by decide
  rw [he]
  exact case2946
#print axioms case3970

theorem case2947 : checkNat 2947 = true := by native_decide
#print axioms case2947

theorem case2950 : checkNat 2950 = true := by native_decide
#print axioms case2950

theorem case3974 : checkNat 3974 = true := by
  apply check_of_normalize (Case.ofNat 3974)
  have he : (Case.ofNat 3974).normalize = Case.ofNat 2950 := by decide
  rw [he]
  exact case2950
#print axioms case3974

theorem case2951 : checkNat 2951 = true := by native_decide
#print axioms case2951

theorem case2954 : checkNat 2954 = true := by native_decide
#print axioms case2954

theorem case3978 : checkNat 3978 = true := by
  apply check_of_normalize (Case.ofNat 3978)
  have he : (Case.ofNat 3978).normalize = Case.ofNat 2954 := by decide
  rw [he]
  exact case2954
#print axioms case3978

theorem case2955 : checkNat 2955 = true := by native_decide
#print axioms case2955

theorem case2958 : checkNat 2958 = true := by native_decide
#print axioms case2958

theorem case3982 : checkNat 3982 = true := by
  apply check_of_normalize (Case.ofNat 3982)
  have he : (Case.ofNat 3982).normalize = Case.ofNat 2958 := by decide
  rw [he]
  exact case2958
#print axioms case3982

theorem case2959 : checkNat 2959 = true := by native_decide
#print axioms case2959

theorem case2962 : checkNat 2962 = true := by native_decide
#print axioms case2962

theorem case3986 : checkNat 3986 = true := by
  apply check_of_normalize (Case.ofNat 3986)
  have he : (Case.ofNat 3986).normalize = Case.ofNat 2962 := by decide
  rw [he]
  exact case2962
#print axioms case3986

theorem case2963 : checkNat 2963 = true := by native_decide
#print axioms case2963

theorem case2966 : checkNat 2966 = true := by native_decide
#print axioms case2966

theorem case3990 : checkNat 3990 = true := by
  apply check_of_normalize (Case.ofNat 3990)
  have he : (Case.ofNat 3990).normalize = Case.ofNat 2966 := by decide
  rw [he]
  exact case2966
#print axioms case3990

theorem case2967 : checkNat 2967 = true := by native_decide
#print axioms case2967

theorem case2970 : checkNat 2970 = true := by native_decide
#print axioms case2970

theorem case3994 : checkNat 3994 = true := by
  apply check_of_normalize (Case.ofNat 3994)
  have he : (Case.ofNat 3994).normalize = Case.ofNat 2970 := by decide
  rw [he]
  exact case2970
#print axioms case3994

theorem case2971 : checkNat 2971 = true := by native_decide
#print axioms case2971

theorem case2974 : checkNat 2974 = true := by native_decide
#print axioms case2974

theorem case3998 : checkNat 3998 = true := by
  apply check_of_normalize (Case.ofNat 3998)
  have he : (Case.ofNat 3998).normalize = Case.ofNat 2974 := by decide
  rw [he]
  exact case2974
#print axioms case3998

theorem case2975 : checkNat 2975 = true := by native_decide
#print axioms case2975

theorem case2978 : checkNat 2978 = true := by native_decide
#print axioms case2978

theorem case4002 : checkNat 4002 = true := by
  apply check_of_normalize (Case.ofNat 4002)
  have he : (Case.ofNat 4002).normalize = Case.ofNat 2978 := by decide
  rw [he]
  exact case2978
#print axioms case4002

theorem case2979 : checkNat 2979 = true := by native_decide
#print axioms case2979

theorem case2982 : checkNat 2982 = true := by native_decide
#print axioms case2982

theorem case4006 : checkNat 4006 = true := by
  apply check_of_normalize (Case.ofNat 4006)
  have he : (Case.ofNat 4006).normalize = Case.ofNat 2982 := by decide
  rw [he]
  exact case2982
#print axioms case4006

theorem case2983 : checkNat 2983 = true := by native_decide
#print axioms case2983

theorem case2986 : checkNat 2986 = true := by native_decide
#print axioms case2986

theorem case4010 : checkNat 4010 = true := by
  apply check_of_normalize (Case.ofNat 4010)
  have he : (Case.ofNat 4010).normalize = Case.ofNat 2986 := by decide
  rw [he]
  exact case2986
#print axioms case4010

theorem case2987 : checkNat 2987 = true := by native_decide
#print axioms case2987

theorem case2990 : checkNat 2990 = true := by native_decide
#print axioms case2990

theorem case4014 : checkNat 4014 = true := by
  apply check_of_normalize (Case.ofNat 4014)
  have he : (Case.ofNat 4014).normalize = Case.ofNat 2990 := by decide
  rw [he]
  exact case2990
#print axioms case4014

theorem case2991 : checkNat 2991 = true := by native_decide
#print axioms case2991

theorem case2994 : checkNat 2994 = true := by native_decide
#print axioms case2994

theorem case4018 : checkNat 4018 = true := by
  apply check_of_normalize (Case.ofNat 4018)
  have he : (Case.ofNat 4018).normalize = Case.ofNat 2994 := by decide
  rw [he]
  exact case2994
#print axioms case4018

theorem case2995 : checkNat 2995 = true := by native_decide
#print axioms case2995

theorem case2998 : checkNat 2998 = true := by native_decide
#print axioms case2998

theorem case4022 : checkNat 4022 = true := by
  apply check_of_normalize (Case.ofNat 4022)
  have he : (Case.ofNat 4022).normalize = Case.ofNat 2998 := by decide
  rw [he]
  exact case2998
#print axioms case4022

theorem case2999 : checkNat 2999 = true := by native_decide
#print axioms case2999

theorem case3002 : checkNat 3002 = true := by native_decide
#print axioms case3002

theorem case4026 : checkNat 4026 = true := by
  apply check_of_normalize (Case.ofNat 4026)
  have he : (Case.ofNat 4026).normalize = Case.ofNat 3002 := by decide
  rw [he]
  exact case3002
#print axioms case4026

theorem case3003 : checkNat 3003 = true := by native_decide
#print axioms case3003

theorem case3006 : checkNat 3006 = true := by native_decide
#print axioms case3006

theorem case4030 : checkNat 4030 = true := by
  apply check_of_normalize (Case.ofNat 4030)
  have he : (Case.ofNat 4030).normalize = Case.ofNat 3006 := by decide
  rw [he]
  exact case3006
#print axioms case4030

theorem case3007 : checkNat 3007 = true := by native_decide
#print axioms case3007

theorem accepted :
    checkNat 2946 = true ∧
    checkNat 2947 = true ∧
    checkNat 2950 = true ∧
    checkNat 2951 = true ∧
    checkNat 2954 = true ∧
    checkNat 2955 = true ∧
    checkNat 2958 = true ∧
    checkNat 2959 = true ∧
    checkNat 2962 = true ∧
    checkNat 2963 = true ∧
    checkNat 2966 = true ∧
    checkNat 2967 = true ∧
    checkNat 2970 = true ∧
    checkNat 2971 = true ∧
    checkNat 2974 = true ∧
    checkNat 2975 = true ∧
    checkNat 2978 = true ∧
    checkNat 2979 = true ∧
    checkNat 2982 = true ∧
    checkNat 2983 = true ∧
    checkNat 2986 = true ∧
    checkNat 2987 = true ∧
    checkNat 2990 = true ∧
    checkNat 2991 = true ∧
    checkNat 2994 = true ∧
    checkNat 2995 = true ∧
    checkNat 2998 = true ∧
    checkNat 2999 = true ∧
    checkNat 3002 = true ∧
    checkNat 3003 = true ∧
    checkNat 3006 = true ∧
    checkNat 3007 = true ∧
    checkNat 3970 = true ∧
    checkNat 3974 = true ∧
    checkNat 3978 = true ∧
    checkNat 3982 = true ∧
    checkNat 3986 = true ∧
    checkNat 3990 = true ∧
    checkNat 3994 = true ∧
    checkNat 3998 = true ∧
    checkNat 4002 = true ∧
    checkNat 4006 = true ∧
    checkNat 4010 = true ∧
    checkNat 4014 = true ∧
    checkNat 4018 = true ∧
    checkNat 4022 = true ∧
    checkNat 4026 = true ∧
    checkNat 4030 = true := by
  exact ⟨case2946, case2947, case2950, case2951, case2954, case2955, case2958, case2959, case2962, case2963, case2966, case2967, case2970, case2971, case2974, case2975, case2978, case2979, case2982, case2983, case2986, case2987, case2990, case2991, case2994, case2995, case2998, case2999, case3002, case3003, case3006, case3007, case3970, case3974, case3978, case3982, case3986, case3990, case3994, case3998, case4002, case4006, case4010, case4014, case4018, case4022, case4026, case4030⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1984
