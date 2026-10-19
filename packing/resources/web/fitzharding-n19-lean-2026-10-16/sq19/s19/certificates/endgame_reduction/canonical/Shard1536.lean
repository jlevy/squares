import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1536
open Sq19.Endgame.Reduction

theorem case2050 : checkNat 2050 = true := by native_decide
#print axioms case2050

theorem case3074 : checkNat 3074 = true := by
  apply check_of_normalize (Case.ofNat 3074)
  have he : (Case.ofNat 3074).normalize = Case.ofNat 2050 := by decide
  rw [he]
  exact case2050
#print axioms case3074

theorem case2051 : checkNat 2051 = true := by native_decide
#print axioms case2051

theorem case2054 : checkNat 2054 = true := by native_decide
#print axioms case2054

theorem case3078 : checkNat 3078 = true := by
  apply check_of_normalize (Case.ofNat 3078)
  have he : (Case.ofNat 3078).normalize = Case.ofNat 2054 := by decide
  rw [he]
  exact case2054
#print axioms case3078

theorem case2055 : checkNat 2055 = true := by native_decide
#print axioms case2055

theorem case2058 : checkNat 2058 = true := by native_decide
#print axioms case2058

theorem case3082 : checkNat 3082 = true := by
  apply check_of_normalize (Case.ofNat 3082)
  have he : (Case.ofNat 3082).normalize = Case.ofNat 2058 := by decide
  rw [he]
  exact case2058
#print axioms case3082

theorem case2059 : checkNat 2059 = true := by native_decide
#print axioms case2059

theorem case2062 : checkNat 2062 = true := by native_decide
#print axioms case2062

theorem case3086 : checkNat 3086 = true := by
  apply check_of_normalize (Case.ofNat 3086)
  have he : (Case.ofNat 3086).normalize = Case.ofNat 2062 := by decide
  rw [he]
  exact case2062
#print axioms case3086

theorem case2063 : checkNat 2063 = true := by native_decide
#print axioms case2063

theorem case2066 : checkNat 2066 = true := by native_decide
#print axioms case2066

theorem case3090 : checkNat 3090 = true := by
  apply check_of_normalize (Case.ofNat 3090)
  have he : (Case.ofNat 3090).normalize = Case.ofNat 2066 := by decide
  rw [he]
  exact case2066
#print axioms case3090

theorem case2067 : checkNat 2067 = true := by native_decide
#print axioms case2067

theorem case2070 : checkNat 2070 = true := by native_decide
#print axioms case2070

theorem case3094 : checkNat 3094 = true := by
  apply check_of_normalize (Case.ofNat 3094)
  have he : (Case.ofNat 3094).normalize = Case.ofNat 2070 := by decide
  rw [he]
  exact case2070
#print axioms case3094

theorem case2071 : checkNat 2071 = true := by native_decide
#print axioms case2071

theorem case2074 : checkNat 2074 = true := by native_decide
#print axioms case2074

theorem case3098 : checkNat 3098 = true := by
  apply check_of_normalize (Case.ofNat 3098)
  have he : (Case.ofNat 3098).normalize = Case.ofNat 2074 := by decide
  rw [he]
  exact case2074
#print axioms case3098

theorem case2075 : checkNat 2075 = true := by native_decide
#print axioms case2075

theorem case2078 : checkNat 2078 = true := by native_decide
#print axioms case2078

theorem case3102 : checkNat 3102 = true := by
  apply check_of_normalize (Case.ofNat 3102)
  have he : (Case.ofNat 3102).normalize = Case.ofNat 2078 := by decide
  rw [he]
  exact case2078
#print axioms case3102

theorem case2079 : checkNat 2079 = true := by native_decide
#print axioms case2079

theorem case2082 : checkNat 2082 = true := by native_decide
#print axioms case2082

theorem case3106 : checkNat 3106 = true := by
  apply check_of_normalize (Case.ofNat 3106)
  have he : (Case.ofNat 3106).normalize = Case.ofNat 2082 := by decide
  rw [he]
  exact case2082
#print axioms case3106

theorem case2083 : checkNat 2083 = true := by native_decide
#print axioms case2083

theorem case2086 : checkNat 2086 = true := by native_decide
#print axioms case2086

theorem case3110 : checkNat 3110 = true := by
  apply check_of_normalize (Case.ofNat 3110)
  have he : (Case.ofNat 3110).normalize = Case.ofNat 2086 := by decide
  rw [he]
  exact case2086
#print axioms case3110

theorem case2087 : checkNat 2087 = true := by native_decide
#print axioms case2087

theorem case2090 : checkNat 2090 = true := by native_decide
#print axioms case2090

theorem case3114 : checkNat 3114 = true := by
  apply check_of_normalize (Case.ofNat 3114)
  have he : (Case.ofNat 3114).normalize = Case.ofNat 2090 := by decide
  rw [he]
  exact case2090
#print axioms case3114

theorem case2091 : checkNat 2091 = true := by native_decide
#print axioms case2091

theorem case2094 : checkNat 2094 = true := by native_decide
#print axioms case2094

theorem case3118 : checkNat 3118 = true := by
  apply check_of_normalize (Case.ofNat 3118)
  have he : (Case.ofNat 3118).normalize = Case.ofNat 2094 := by decide
  rw [he]
  exact case2094
#print axioms case3118

theorem case2095 : checkNat 2095 = true := by native_decide
#print axioms case2095

theorem case2098 : checkNat 2098 = true := by native_decide
#print axioms case2098

theorem case3122 : checkNat 3122 = true := by
  apply check_of_normalize (Case.ofNat 3122)
  have he : (Case.ofNat 3122).normalize = Case.ofNat 2098 := by decide
  rw [he]
  exact case2098
#print axioms case3122

theorem case2099 : checkNat 2099 = true := by native_decide
#print axioms case2099

theorem case2102 : checkNat 2102 = true := by native_decide
#print axioms case2102

theorem case3126 : checkNat 3126 = true := by
  apply check_of_normalize (Case.ofNat 3126)
  have he : (Case.ofNat 3126).normalize = Case.ofNat 2102 := by decide
  rw [he]
  exact case2102
#print axioms case3126

theorem case2103 : checkNat 2103 = true := by native_decide
#print axioms case2103

theorem case2106 : checkNat 2106 = true := by native_decide
#print axioms case2106

theorem case3130 : checkNat 3130 = true := by
  apply check_of_normalize (Case.ofNat 3130)
  have he : (Case.ofNat 3130).normalize = Case.ofNat 2106 := by decide
  rw [he]
  exact case2106
#print axioms case3130

theorem case2107 : checkNat 2107 = true := by native_decide
#print axioms case2107

theorem case2110 : checkNat 2110 = true := by native_decide
#print axioms case2110

theorem case3134 : checkNat 3134 = true := by
  apply check_of_normalize (Case.ofNat 3134)
  have he : (Case.ofNat 3134).normalize = Case.ofNat 2110 := by decide
  rw [he]
  exact case2110
#print axioms case3134

theorem case2111 : checkNat 2111 = true := by native_decide
#print axioms case2111

theorem accepted :
    checkNat 2050 = true ∧
    checkNat 2051 = true ∧
    checkNat 2054 = true ∧
    checkNat 2055 = true ∧
    checkNat 2058 = true ∧
    checkNat 2059 = true ∧
    checkNat 2062 = true ∧
    checkNat 2063 = true ∧
    checkNat 2066 = true ∧
    checkNat 2067 = true ∧
    checkNat 2070 = true ∧
    checkNat 2071 = true ∧
    checkNat 2074 = true ∧
    checkNat 2075 = true ∧
    checkNat 2078 = true ∧
    checkNat 2079 = true ∧
    checkNat 2082 = true ∧
    checkNat 2083 = true ∧
    checkNat 2086 = true ∧
    checkNat 2087 = true ∧
    checkNat 2090 = true ∧
    checkNat 2091 = true ∧
    checkNat 2094 = true ∧
    checkNat 2095 = true ∧
    checkNat 2098 = true ∧
    checkNat 2099 = true ∧
    checkNat 2102 = true ∧
    checkNat 2103 = true ∧
    checkNat 2106 = true ∧
    checkNat 2107 = true ∧
    checkNat 2110 = true ∧
    checkNat 2111 = true ∧
    checkNat 3074 = true ∧
    checkNat 3078 = true ∧
    checkNat 3082 = true ∧
    checkNat 3086 = true ∧
    checkNat 3090 = true ∧
    checkNat 3094 = true ∧
    checkNat 3098 = true ∧
    checkNat 3102 = true ∧
    checkNat 3106 = true ∧
    checkNat 3110 = true ∧
    checkNat 3114 = true ∧
    checkNat 3118 = true ∧
    checkNat 3122 = true ∧
    checkNat 3126 = true ∧
    checkNat 3130 = true ∧
    checkNat 3134 = true := by
  exact ⟨case2050, case2051, case2054, case2055, case2058, case2059, case2062, case2063, case2066, case2067, case2070, case2071, case2074, case2075, case2078, case2079, case2082, case2083, case2086, case2087, case2090, case2091, case2094, case2095, case2098, case2099, case2102, case2103, case2106, case2107, case2110, case2111, case3074, case3078, case3082, case3086, case3090, case3094, case3098, case3102, case3106, case3110, case3114, case3118, case3122, case3126, case3130, case3134⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1536
