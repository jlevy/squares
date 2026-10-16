import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard2016
open Sq19.Endgame.Reduction

theorem case3010 : checkNat 3010 = true := by native_decide
#print axioms case3010

theorem case4034 : checkNat 4034 = true := by
  apply check_of_normalize (Case.ofNat 4034)
  have he : (Case.ofNat 4034).normalize = Case.ofNat 3010 := by decide
  rw [he]
  exact case3010
#print axioms case4034

theorem case3011 : checkNat 3011 = true := by native_decide
#print axioms case3011

theorem case3014 : checkNat 3014 = true := by native_decide
#print axioms case3014

theorem case4038 : checkNat 4038 = true := by
  apply check_of_normalize (Case.ofNat 4038)
  have he : (Case.ofNat 4038).normalize = Case.ofNat 3014 := by decide
  rw [he]
  exact case3014
#print axioms case4038

theorem case3015 : checkNat 3015 = true := by native_decide
#print axioms case3015

theorem case3018 : checkNat 3018 = true := by native_decide
#print axioms case3018

theorem case4042 : checkNat 4042 = true := by
  apply check_of_normalize (Case.ofNat 4042)
  have he : (Case.ofNat 4042).normalize = Case.ofNat 3018 := by decide
  rw [he]
  exact case3018
#print axioms case4042

theorem case3019 : checkNat 3019 = true := by native_decide
#print axioms case3019

theorem case3022 : checkNat 3022 = true := by native_decide
#print axioms case3022

theorem case4046 : checkNat 4046 = true := by
  apply check_of_normalize (Case.ofNat 4046)
  have he : (Case.ofNat 4046).normalize = Case.ofNat 3022 := by decide
  rw [he]
  exact case3022
#print axioms case4046

theorem case3023 : checkNat 3023 = true := by native_decide
#print axioms case3023

theorem case3026 : checkNat 3026 = true := by native_decide
#print axioms case3026

theorem case4050 : checkNat 4050 = true := by
  apply check_of_normalize (Case.ofNat 4050)
  have he : (Case.ofNat 4050).normalize = Case.ofNat 3026 := by decide
  rw [he]
  exact case3026
#print axioms case4050

theorem case3027 : checkNat 3027 = true := by native_decide
#print axioms case3027

theorem case3030 : checkNat 3030 = true := by native_decide
#print axioms case3030

theorem case4054 : checkNat 4054 = true := by
  apply check_of_normalize (Case.ofNat 4054)
  have he : (Case.ofNat 4054).normalize = Case.ofNat 3030 := by decide
  rw [he]
  exact case3030
#print axioms case4054

theorem case3031 : checkNat 3031 = true := by native_decide
#print axioms case3031

theorem case3034 : checkNat 3034 = true := by native_decide
#print axioms case3034

theorem case4058 : checkNat 4058 = true := by
  apply check_of_normalize (Case.ofNat 4058)
  have he : (Case.ofNat 4058).normalize = Case.ofNat 3034 := by decide
  rw [he]
  exact case3034
#print axioms case4058

theorem case3035 : checkNat 3035 = true := by native_decide
#print axioms case3035

theorem case3038 : checkNat 3038 = true := by native_decide
#print axioms case3038

theorem case4062 : checkNat 4062 = true := by
  apply check_of_normalize (Case.ofNat 4062)
  have he : (Case.ofNat 4062).normalize = Case.ofNat 3038 := by decide
  rw [he]
  exact case3038
#print axioms case4062

theorem case3039 : checkNat 3039 = true := by native_decide
#print axioms case3039

theorem case3042 : checkNat 3042 = true := by native_decide
#print axioms case3042

theorem case4066 : checkNat 4066 = true := by
  apply check_of_normalize (Case.ofNat 4066)
  have he : (Case.ofNat 4066).normalize = Case.ofNat 3042 := by decide
  rw [he]
  exact case3042
#print axioms case4066

theorem case3043 : checkNat 3043 = true := by native_decide
#print axioms case3043

theorem case3046 : checkNat 3046 = true := by native_decide
#print axioms case3046

theorem case4070 : checkNat 4070 = true := by
  apply check_of_normalize (Case.ofNat 4070)
  have he : (Case.ofNat 4070).normalize = Case.ofNat 3046 := by decide
  rw [he]
  exact case3046
#print axioms case4070

theorem case3047 : checkNat 3047 = true := by native_decide
#print axioms case3047

theorem case3050 : checkNat 3050 = true := by native_decide
#print axioms case3050

theorem case4074 : checkNat 4074 = true := by
  apply check_of_normalize (Case.ofNat 4074)
  have he : (Case.ofNat 4074).normalize = Case.ofNat 3050 := by decide
  rw [he]
  exact case3050
#print axioms case4074

theorem case3051 : checkNat 3051 = true := by native_decide
#print axioms case3051

theorem case3054 : checkNat 3054 = true := by native_decide
#print axioms case3054

theorem case4078 : checkNat 4078 = true := by
  apply check_of_normalize (Case.ofNat 4078)
  have he : (Case.ofNat 4078).normalize = Case.ofNat 3054 := by decide
  rw [he]
  exact case3054
#print axioms case4078

theorem case3055 : checkNat 3055 = true := by native_decide
#print axioms case3055

theorem case3058 : checkNat 3058 = true := by native_decide
#print axioms case3058

theorem case4082 : checkNat 4082 = true := by
  apply check_of_normalize (Case.ofNat 4082)
  have he : (Case.ofNat 4082).normalize = Case.ofNat 3058 := by decide
  rw [he]
  exact case3058
#print axioms case4082

theorem case3059 : checkNat 3059 = true := by native_decide
#print axioms case3059

theorem case3062 : checkNat 3062 = true := by native_decide
#print axioms case3062

theorem case4086 : checkNat 4086 = true := by
  apply check_of_normalize (Case.ofNat 4086)
  have he : (Case.ofNat 4086).normalize = Case.ofNat 3062 := by decide
  rw [he]
  exact case3062
#print axioms case4086

theorem case3063 : checkNat 3063 = true := by native_decide
#print axioms case3063

theorem case3066 : checkNat 3066 = true := by native_decide
#print axioms case3066

theorem case4090 : checkNat 4090 = true := by
  apply check_of_normalize (Case.ofNat 4090)
  have he : (Case.ofNat 4090).normalize = Case.ofNat 3066 := by decide
  rw [he]
  exact case3066
#print axioms case4090

theorem case3067 : checkNat 3067 = true := by native_decide
#print axioms case3067

theorem case3070 : checkNat 3070 = true := by native_decide
#print axioms case3070

theorem case4094 : checkNat 4094 = true := by
  apply check_of_normalize (Case.ofNat 4094)
  have he : (Case.ofNat 4094).normalize = Case.ofNat 3070 := by decide
  rw [he]
  exact case3070
#print axioms case4094

theorem case3071 : checkNat 3071 = true := by native_decide
#print axioms case3071

theorem accepted :
    checkNat 3010 = true ∧
    checkNat 3011 = true ∧
    checkNat 3014 = true ∧
    checkNat 3015 = true ∧
    checkNat 3018 = true ∧
    checkNat 3019 = true ∧
    checkNat 3022 = true ∧
    checkNat 3023 = true ∧
    checkNat 3026 = true ∧
    checkNat 3027 = true ∧
    checkNat 3030 = true ∧
    checkNat 3031 = true ∧
    checkNat 3034 = true ∧
    checkNat 3035 = true ∧
    checkNat 3038 = true ∧
    checkNat 3039 = true ∧
    checkNat 3042 = true ∧
    checkNat 3043 = true ∧
    checkNat 3046 = true ∧
    checkNat 3047 = true ∧
    checkNat 3050 = true ∧
    checkNat 3051 = true ∧
    checkNat 3054 = true ∧
    checkNat 3055 = true ∧
    checkNat 3058 = true ∧
    checkNat 3059 = true ∧
    checkNat 3062 = true ∧
    checkNat 3063 = true ∧
    checkNat 3066 = true ∧
    checkNat 3067 = true ∧
    checkNat 3070 = true ∧
    checkNat 3071 = true ∧
    checkNat 4034 = true ∧
    checkNat 4038 = true ∧
    checkNat 4042 = true ∧
    checkNat 4046 = true ∧
    checkNat 4050 = true ∧
    checkNat 4054 = true ∧
    checkNat 4058 = true ∧
    checkNat 4062 = true ∧
    checkNat 4066 = true ∧
    checkNat 4070 = true ∧
    checkNat 4074 = true ∧
    checkNat 4078 = true ∧
    checkNat 4082 = true ∧
    checkNat 4086 = true ∧
    checkNat 4090 = true ∧
    checkNat 4094 = true := by
  exact ⟨case3010, case3011, case3014, case3015, case3018, case3019, case3022, case3023, case3026, case3027, case3030, case3031, case3034, case3035, case3038, case3039, case3042, case3043, case3046, case3047, case3050, case3051, case3054, case3055, case3058, case3059, case3062, case3063, case3066, case3067, case3070, case3071, case4034, case4038, case4042, case4046, case4050, case4054, case4058, case4062, case4066, case4070, case4074, case4078, case4082, case4086, case4090, case4094⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard2016
