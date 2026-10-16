import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0064
open Sq19.Endgame.Reduction

theorem case0064 : checkNat 64 = true := by native_decide
#print axioms case0064

theorem case1088 : checkNat 1088 = true := by
  apply check_of_normalize (Case.ofNat 1088)
  have he : (Case.ofNat 1088).normalize = Case.ofNat 64 := by decide
  rw [he]
  exact case0064
#print axioms case1088

theorem case2112 : checkNat 2112 = true := by
  apply check_of_normalize (Case.ofNat 2112)
  have he : (Case.ofNat 2112).normalize = Case.ofNat 64 := by decide
  rw [he]
  exact case0064
#print axioms case2112

theorem case3136 : checkNat 3136 = true := by
  apply check_of_normalize (Case.ofNat 3136)
  have he : (Case.ofNat 3136).normalize = Case.ofNat 64 := by decide
  rw [he]
  exact case0064
#print axioms case3136

theorem case0065 : checkNat 65 = true := by native_decide
#print axioms case0065

theorem case2113 : checkNat 2113 = true := by
  apply check_of_normalize (Case.ofNat 2113)
  have he : (Case.ofNat 2113).normalize = Case.ofNat 65 := by decide
  rw [he]
  exact case0065
#print axioms case2113

theorem case0066 : checkNat 66 = true := by native_decide
#print axioms case0066

theorem case1090 : checkNat 1090 = true := by
  apply check_of_normalize (Case.ofNat 1090)
  have he : (Case.ofNat 1090).normalize = Case.ofNat 66 := by decide
  rw [he]
  exact case0066
#print axioms case1090

theorem case0067 : checkNat 67 = true := by native_decide
#print axioms case0067

theorem case0068 : checkNat 68 = true := by native_decide
#print axioms case0068

theorem case1092 : checkNat 1092 = true := by
  apply check_of_normalize (Case.ofNat 1092)
  have he : (Case.ofNat 1092).normalize = Case.ofNat 68 := by decide
  rw [he]
  exact case0068
#print axioms case1092

theorem case2116 : checkNat 2116 = true := by
  apply check_of_normalize (Case.ofNat 2116)
  have he : (Case.ofNat 2116).normalize = Case.ofNat 68 := by decide
  rw [he]
  exact case0068
#print axioms case2116

theorem case3140 : checkNat 3140 = true := by
  apply check_of_normalize (Case.ofNat 3140)
  have he : (Case.ofNat 3140).normalize = Case.ofNat 68 := by decide
  rw [he]
  exact case0068
#print axioms case3140

theorem case0069 : checkNat 69 = true := by native_decide
#print axioms case0069

theorem case2117 : checkNat 2117 = true := by
  apply check_of_normalize (Case.ofNat 2117)
  have he : (Case.ofNat 2117).normalize = Case.ofNat 69 := by decide
  rw [he]
  exact case0069
#print axioms case2117

theorem case0070 : checkNat 70 = true := by native_decide
#print axioms case0070

theorem case1094 : checkNat 1094 = true := by
  apply check_of_normalize (Case.ofNat 1094)
  have he : (Case.ofNat 1094).normalize = Case.ofNat 70 := by decide
  rw [he]
  exact case0070
#print axioms case1094

theorem case0071 : checkNat 71 = true := by native_decide
#print axioms case0071

theorem case0072 : checkNat 72 = true := by native_decide
#print axioms case0072

theorem case1096 : checkNat 1096 = true := by
  apply check_of_normalize (Case.ofNat 1096)
  have he : (Case.ofNat 1096).normalize = Case.ofNat 72 := by decide
  rw [he]
  exact case0072
#print axioms case1096

theorem case2120 : checkNat 2120 = true := by
  apply check_of_normalize (Case.ofNat 2120)
  have he : (Case.ofNat 2120).normalize = Case.ofNat 72 := by decide
  rw [he]
  exact case0072
#print axioms case2120

theorem case3144 : checkNat 3144 = true := by
  apply check_of_normalize (Case.ofNat 3144)
  have he : (Case.ofNat 3144).normalize = Case.ofNat 72 := by decide
  rw [he]
  exact case0072
#print axioms case3144

theorem case0073 : checkNat 73 = true := by native_decide
#print axioms case0073

theorem case2121 : checkNat 2121 = true := by
  apply check_of_normalize (Case.ofNat 2121)
  have he : (Case.ofNat 2121).normalize = Case.ofNat 73 := by decide
  rw [he]
  exact case0073
#print axioms case2121

theorem case0074 : checkNat 74 = true := by native_decide
#print axioms case0074

theorem case1098 : checkNat 1098 = true := by
  apply check_of_normalize (Case.ofNat 1098)
  have he : (Case.ofNat 1098).normalize = Case.ofNat 74 := by decide
  rw [he]
  exact case0074
#print axioms case1098

theorem case0075 : checkNat 75 = true := by native_decide
#print axioms case0075

theorem case0076 : checkNat 76 = true := by native_decide
#print axioms case0076

theorem case1100 : checkNat 1100 = true := by
  apply check_of_normalize (Case.ofNat 1100)
  have he : (Case.ofNat 1100).normalize = Case.ofNat 76 := by decide
  rw [he]
  exact case0076
#print axioms case1100

theorem case2124 : checkNat 2124 = true := by
  apply check_of_normalize (Case.ofNat 2124)
  have he : (Case.ofNat 2124).normalize = Case.ofNat 76 := by decide
  rw [he]
  exact case0076
#print axioms case2124

theorem case3148 : checkNat 3148 = true := by
  apply check_of_normalize (Case.ofNat 3148)
  have he : (Case.ofNat 3148).normalize = Case.ofNat 76 := by decide
  rw [he]
  exact case0076
#print axioms case3148

theorem case0077 : checkNat 77 = true := by native_decide
#print axioms case0077

theorem case2125 : checkNat 2125 = true := by
  apply check_of_normalize (Case.ofNat 2125)
  have he : (Case.ofNat 2125).normalize = Case.ofNat 77 := by decide
  rw [he]
  exact case0077
#print axioms case2125

theorem case0078 : checkNat 78 = true := by native_decide
#print axioms case0078

theorem case1102 : checkNat 1102 = true := by
  apply check_of_normalize (Case.ofNat 1102)
  have he : (Case.ofNat 1102).normalize = Case.ofNat 78 := by decide
  rw [he]
  exact case0078
#print axioms case1102

theorem case0079 : checkNat 79 = true := by native_decide
#print axioms case0079

theorem case0080 : checkNat 80 = true := by native_decide
#print axioms case0080

theorem case1104 : checkNat 1104 = true := by
  apply check_of_normalize (Case.ofNat 1104)
  have he : (Case.ofNat 1104).normalize = Case.ofNat 80 := by decide
  rw [he]
  exact case0080
#print axioms case1104

theorem case2128 : checkNat 2128 = true := by
  apply check_of_normalize (Case.ofNat 2128)
  have he : (Case.ofNat 2128).normalize = Case.ofNat 80 := by decide
  rw [he]
  exact case0080
#print axioms case2128

theorem case3152 : checkNat 3152 = true := by
  apply check_of_normalize (Case.ofNat 3152)
  have he : (Case.ofNat 3152).normalize = Case.ofNat 80 := by decide
  rw [he]
  exact case0080
#print axioms case3152

theorem case0081 : checkNat 81 = true := by native_decide
#print axioms case0081

theorem case2129 : checkNat 2129 = true := by
  apply check_of_normalize (Case.ofNat 2129)
  have he : (Case.ofNat 2129).normalize = Case.ofNat 81 := by decide
  rw [he]
  exact case0081
#print axioms case2129

theorem case0082 : checkNat 82 = true := by native_decide
#print axioms case0082

theorem case1106 : checkNat 1106 = true := by
  apply check_of_normalize (Case.ofNat 1106)
  have he : (Case.ofNat 1106).normalize = Case.ofNat 82 := by decide
  rw [he]
  exact case0082
#print axioms case1106

theorem case0083 : checkNat 83 = true := by native_decide
#print axioms case0083

theorem case0084 : checkNat 84 = true := by native_decide
#print axioms case0084

theorem case1108 : checkNat 1108 = true := by
  apply check_of_normalize (Case.ofNat 1108)
  have he : (Case.ofNat 1108).normalize = Case.ofNat 84 := by decide
  rw [he]
  exact case0084
#print axioms case1108

theorem case2132 : checkNat 2132 = true := by
  apply check_of_normalize (Case.ofNat 2132)
  have he : (Case.ofNat 2132).normalize = Case.ofNat 84 := by decide
  rw [he]
  exact case0084
#print axioms case2132

theorem case3156 : checkNat 3156 = true := by
  apply check_of_normalize (Case.ofNat 3156)
  have he : (Case.ofNat 3156).normalize = Case.ofNat 84 := by decide
  rw [he]
  exact case0084
#print axioms case3156

theorem case0085 : checkNat 85 = true := by native_decide
#print axioms case0085

theorem case2133 : checkNat 2133 = true := by
  apply check_of_normalize (Case.ofNat 2133)
  have he : (Case.ofNat 2133).normalize = Case.ofNat 85 := by decide
  rw [he]
  exact case0085
#print axioms case2133

theorem case0086 : checkNat 86 = true := by native_decide
#print axioms case0086

theorem case1110 : checkNat 1110 = true := by
  apply check_of_normalize (Case.ofNat 1110)
  have he : (Case.ofNat 1110).normalize = Case.ofNat 86 := by decide
  rw [he]
  exact case0086
#print axioms case1110

theorem case0087 : checkNat 87 = true := by native_decide
#print axioms case0087

theorem case0088 : checkNat 88 = true := by native_decide
#print axioms case0088

theorem case1112 : checkNat 1112 = true := by
  apply check_of_normalize (Case.ofNat 1112)
  have he : (Case.ofNat 1112).normalize = Case.ofNat 88 := by decide
  rw [he]
  exact case0088
#print axioms case1112

theorem case2136 : checkNat 2136 = true := by
  apply check_of_normalize (Case.ofNat 2136)
  have he : (Case.ofNat 2136).normalize = Case.ofNat 88 := by decide
  rw [he]
  exact case0088
#print axioms case2136

theorem case3160 : checkNat 3160 = true := by
  apply check_of_normalize (Case.ofNat 3160)
  have he : (Case.ofNat 3160).normalize = Case.ofNat 88 := by decide
  rw [he]
  exact case0088
#print axioms case3160

theorem case0089 : checkNat 89 = true := by native_decide
#print axioms case0089

theorem case2137 : checkNat 2137 = true := by
  apply check_of_normalize (Case.ofNat 2137)
  have he : (Case.ofNat 2137).normalize = Case.ofNat 89 := by decide
  rw [he]
  exact case0089
#print axioms case2137

theorem case0090 : checkNat 90 = true := by native_decide
#print axioms case0090

theorem case1114 : checkNat 1114 = true := by
  apply check_of_normalize (Case.ofNat 1114)
  have he : (Case.ofNat 1114).normalize = Case.ofNat 90 := by decide
  rw [he]
  exact case0090
#print axioms case1114

theorem case0091 : checkNat 91 = true := by native_decide
#print axioms case0091

theorem case0092 : checkNat 92 = true := by native_decide
#print axioms case0092

theorem case1116 : checkNat 1116 = true := by
  apply check_of_normalize (Case.ofNat 1116)
  have he : (Case.ofNat 1116).normalize = Case.ofNat 92 := by decide
  rw [he]
  exact case0092
#print axioms case1116

theorem case2140 : checkNat 2140 = true := by
  apply check_of_normalize (Case.ofNat 2140)
  have he : (Case.ofNat 2140).normalize = Case.ofNat 92 := by decide
  rw [he]
  exact case0092
#print axioms case2140

theorem case3164 : checkNat 3164 = true := by
  apply check_of_normalize (Case.ofNat 3164)
  have he : (Case.ofNat 3164).normalize = Case.ofNat 92 := by decide
  rw [he]
  exact case0092
#print axioms case3164

theorem case0093 : checkNat 93 = true := by native_decide
#print axioms case0093

theorem case2141 : checkNat 2141 = true := by
  apply check_of_normalize (Case.ofNat 2141)
  have he : (Case.ofNat 2141).normalize = Case.ofNat 93 := by decide
  rw [he]
  exact case0093
#print axioms case2141

theorem case0094 : checkNat 94 = true := by native_decide
#print axioms case0094

theorem case1118 : checkNat 1118 = true := by
  apply check_of_normalize (Case.ofNat 1118)
  have he : (Case.ofNat 1118).normalize = Case.ofNat 94 := by decide
  rw [he]
  exact case0094
#print axioms case1118

theorem case0095 : checkNat 95 = true := by native_decide
#print axioms case0095

theorem accepted :
    checkNat 64 = true ∧
    checkNat 65 = true ∧
    checkNat 66 = true ∧
    checkNat 67 = true ∧
    checkNat 68 = true ∧
    checkNat 69 = true ∧
    checkNat 70 = true ∧
    checkNat 71 = true ∧
    checkNat 72 = true ∧
    checkNat 73 = true ∧
    checkNat 74 = true ∧
    checkNat 75 = true ∧
    checkNat 76 = true ∧
    checkNat 77 = true ∧
    checkNat 78 = true ∧
    checkNat 79 = true ∧
    checkNat 80 = true ∧
    checkNat 81 = true ∧
    checkNat 82 = true ∧
    checkNat 83 = true ∧
    checkNat 84 = true ∧
    checkNat 85 = true ∧
    checkNat 86 = true ∧
    checkNat 87 = true ∧
    checkNat 88 = true ∧
    checkNat 89 = true ∧
    checkNat 90 = true ∧
    checkNat 91 = true ∧
    checkNat 92 = true ∧
    checkNat 93 = true ∧
    checkNat 94 = true ∧
    checkNat 95 = true ∧
    checkNat 1088 = true ∧
    checkNat 1090 = true ∧
    checkNat 1092 = true ∧
    checkNat 1094 = true ∧
    checkNat 1096 = true ∧
    checkNat 1098 = true ∧
    checkNat 1100 = true ∧
    checkNat 1102 = true ∧
    checkNat 1104 = true ∧
    checkNat 1106 = true ∧
    checkNat 1108 = true ∧
    checkNat 1110 = true ∧
    checkNat 1112 = true ∧
    checkNat 1114 = true ∧
    checkNat 1116 = true ∧
    checkNat 1118 = true ∧
    checkNat 2112 = true ∧
    checkNat 2113 = true ∧
    checkNat 2116 = true ∧
    checkNat 2117 = true ∧
    checkNat 2120 = true ∧
    checkNat 2121 = true ∧
    checkNat 2124 = true ∧
    checkNat 2125 = true ∧
    checkNat 2128 = true ∧
    checkNat 2129 = true ∧
    checkNat 2132 = true ∧
    checkNat 2133 = true ∧
    checkNat 2136 = true ∧
    checkNat 2137 = true ∧
    checkNat 2140 = true ∧
    checkNat 2141 = true ∧
    checkNat 3136 = true ∧
    checkNat 3140 = true ∧
    checkNat 3144 = true ∧
    checkNat 3148 = true ∧
    checkNat 3152 = true ∧
    checkNat 3156 = true ∧
    checkNat 3160 = true ∧
    checkNat 3164 = true := by
  exact ⟨case0064, case0065, case0066, case0067, case0068, case0069, case0070, case0071, case0072, case0073, case0074, case0075, case0076, case0077, case0078, case0079, case0080, case0081, case0082, case0083, case0084, case0085, case0086, case0087, case0088, case0089, case0090, case0091, case0092, case0093, case0094, case0095, case1088, case1090, case1092, case1094, case1096, case1098, case1100, case1102, case1104, case1106, case1108, case1110, case1112, case1114, case1116, case1118, case2112, case2113, case2116, case2117, case2120, case2121, case2124, case2125, case2128, case2129, case2132, case2133, case2136, case2137, case2140, case2141, case3136, case3140, case3144, case3148, case3152, case3156, case3160, case3164⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0064
