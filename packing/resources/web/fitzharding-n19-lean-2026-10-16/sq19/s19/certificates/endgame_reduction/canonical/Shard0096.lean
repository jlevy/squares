import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0096
open Sq19.Endgame.Reduction

theorem case0096 : checkNat 96 = true := by native_decide
#print axioms case0096

theorem case1120 : checkNat 1120 = true := by
  apply check_of_normalize (Case.ofNat 1120)
  have he : (Case.ofNat 1120).normalize = Case.ofNat 96 := by decide
  rw [he]
  exact case0096
#print axioms case1120

theorem case2144 : checkNat 2144 = true := by
  apply check_of_normalize (Case.ofNat 2144)
  have he : (Case.ofNat 2144).normalize = Case.ofNat 96 := by decide
  rw [he]
  exact case0096
#print axioms case2144

theorem case3168 : checkNat 3168 = true := by
  apply check_of_normalize (Case.ofNat 3168)
  have he : (Case.ofNat 3168).normalize = Case.ofNat 96 := by decide
  rw [he]
  exact case0096
#print axioms case3168

theorem case0097 : checkNat 97 = true := by native_decide
#print axioms case0097

theorem case2145 : checkNat 2145 = true := by
  apply check_of_normalize (Case.ofNat 2145)
  have he : (Case.ofNat 2145).normalize = Case.ofNat 97 := by decide
  rw [he]
  exact case0097
#print axioms case2145

theorem case0098 : checkNat 98 = true := by native_decide
#print axioms case0098

theorem case1122 : checkNat 1122 = true := by
  apply check_of_normalize (Case.ofNat 1122)
  have he : (Case.ofNat 1122).normalize = Case.ofNat 98 := by decide
  rw [he]
  exact case0098
#print axioms case1122

theorem case0099 : checkNat 99 = true := by native_decide
#print axioms case0099

theorem case0100 : checkNat 100 = true := by native_decide
#print axioms case0100

theorem case1124 : checkNat 1124 = true := by
  apply check_of_normalize (Case.ofNat 1124)
  have he : (Case.ofNat 1124).normalize = Case.ofNat 100 := by decide
  rw [he]
  exact case0100
#print axioms case1124

theorem case2148 : checkNat 2148 = true := by
  apply check_of_normalize (Case.ofNat 2148)
  have he : (Case.ofNat 2148).normalize = Case.ofNat 100 := by decide
  rw [he]
  exact case0100
#print axioms case2148

theorem case3172 : checkNat 3172 = true := by
  apply check_of_normalize (Case.ofNat 3172)
  have he : (Case.ofNat 3172).normalize = Case.ofNat 100 := by decide
  rw [he]
  exact case0100
#print axioms case3172

theorem case0101 : checkNat 101 = true := by native_decide
#print axioms case0101

theorem case2149 : checkNat 2149 = true := by
  apply check_of_normalize (Case.ofNat 2149)
  have he : (Case.ofNat 2149).normalize = Case.ofNat 101 := by decide
  rw [he]
  exact case0101
#print axioms case2149

theorem case0102 : checkNat 102 = true := by native_decide
#print axioms case0102

theorem case1126 : checkNat 1126 = true := by
  apply check_of_normalize (Case.ofNat 1126)
  have he : (Case.ofNat 1126).normalize = Case.ofNat 102 := by decide
  rw [he]
  exact case0102
#print axioms case1126

theorem case0103 : checkNat 103 = true := by native_decide
#print axioms case0103

theorem case0104 : checkNat 104 = true := by native_decide
#print axioms case0104

theorem case1128 : checkNat 1128 = true := by
  apply check_of_normalize (Case.ofNat 1128)
  have he : (Case.ofNat 1128).normalize = Case.ofNat 104 := by decide
  rw [he]
  exact case0104
#print axioms case1128

theorem case2152 : checkNat 2152 = true := by
  apply check_of_normalize (Case.ofNat 2152)
  have he : (Case.ofNat 2152).normalize = Case.ofNat 104 := by decide
  rw [he]
  exact case0104
#print axioms case2152

theorem case3176 : checkNat 3176 = true := by
  apply check_of_normalize (Case.ofNat 3176)
  have he : (Case.ofNat 3176).normalize = Case.ofNat 104 := by decide
  rw [he]
  exact case0104
#print axioms case3176

theorem case0105 : checkNat 105 = true := by native_decide
#print axioms case0105

theorem case2153 : checkNat 2153 = true := by
  apply check_of_normalize (Case.ofNat 2153)
  have he : (Case.ofNat 2153).normalize = Case.ofNat 105 := by decide
  rw [he]
  exact case0105
#print axioms case2153

theorem case0106 : checkNat 106 = true := by native_decide
#print axioms case0106

theorem case1130 : checkNat 1130 = true := by
  apply check_of_normalize (Case.ofNat 1130)
  have he : (Case.ofNat 1130).normalize = Case.ofNat 106 := by decide
  rw [he]
  exact case0106
#print axioms case1130

theorem case0107 : checkNat 107 = true := by native_decide
#print axioms case0107

theorem case0108 : checkNat 108 = true := by native_decide
#print axioms case0108

theorem case1132 : checkNat 1132 = true := by
  apply check_of_normalize (Case.ofNat 1132)
  have he : (Case.ofNat 1132).normalize = Case.ofNat 108 := by decide
  rw [he]
  exact case0108
#print axioms case1132

theorem case2156 : checkNat 2156 = true := by
  apply check_of_normalize (Case.ofNat 2156)
  have he : (Case.ofNat 2156).normalize = Case.ofNat 108 := by decide
  rw [he]
  exact case0108
#print axioms case2156

theorem case3180 : checkNat 3180 = true := by
  apply check_of_normalize (Case.ofNat 3180)
  have he : (Case.ofNat 3180).normalize = Case.ofNat 108 := by decide
  rw [he]
  exact case0108
#print axioms case3180

theorem case0109 : checkNat 109 = true := by native_decide
#print axioms case0109

theorem case2157 : checkNat 2157 = true := by
  apply check_of_normalize (Case.ofNat 2157)
  have he : (Case.ofNat 2157).normalize = Case.ofNat 109 := by decide
  rw [he]
  exact case0109
#print axioms case2157

theorem case0110 : checkNat 110 = true := by native_decide
#print axioms case0110

theorem case1134 : checkNat 1134 = true := by
  apply check_of_normalize (Case.ofNat 1134)
  have he : (Case.ofNat 1134).normalize = Case.ofNat 110 := by decide
  rw [he]
  exact case0110
#print axioms case1134

theorem case0111 : checkNat 111 = true := by native_decide
#print axioms case0111

theorem case0112 : checkNat 112 = true := by native_decide
#print axioms case0112

theorem case1136 : checkNat 1136 = true := by
  apply check_of_normalize (Case.ofNat 1136)
  have he : (Case.ofNat 1136).normalize = Case.ofNat 112 := by decide
  rw [he]
  exact case0112
#print axioms case1136

theorem case2160 : checkNat 2160 = true := by
  apply check_of_normalize (Case.ofNat 2160)
  have he : (Case.ofNat 2160).normalize = Case.ofNat 112 := by decide
  rw [he]
  exact case0112
#print axioms case2160

theorem case3184 : checkNat 3184 = true := by
  apply check_of_normalize (Case.ofNat 3184)
  have he : (Case.ofNat 3184).normalize = Case.ofNat 112 := by decide
  rw [he]
  exact case0112
#print axioms case3184

theorem case0113 : checkNat 113 = true := by native_decide
#print axioms case0113

theorem case2161 : checkNat 2161 = true := by
  apply check_of_normalize (Case.ofNat 2161)
  have he : (Case.ofNat 2161).normalize = Case.ofNat 113 := by decide
  rw [he]
  exact case0113
#print axioms case2161

theorem case0114 : checkNat 114 = true := by native_decide
#print axioms case0114

theorem case1138 : checkNat 1138 = true := by
  apply check_of_normalize (Case.ofNat 1138)
  have he : (Case.ofNat 1138).normalize = Case.ofNat 114 := by decide
  rw [he]
  exact case0114
#print axioms case1138

theorem case0115 : checkNat 115 = true := by native_decide
#print axioms case0115

theorem case0116 : checkNat 116 = true := by native_decide
#print axioms case0116

theorem case1140 : checkNat 1140 = true := by
  apply check_of_normalize (Case.ofNat 1140)
  have he : (Case.ofNat 1140).normalize = Case.ofNat 116 := by decide
  rw [he]
  exact case0116
#print axioms case1140

theorem case2164 : checkNat 2164 = true := by
  apply check_of_normalize (Case.ofNat 2164)
  have he : (Case.ofNat 2164).normalize = Case.ofNat 116 := by decide
  rw [he]
  exact case0116
#print axioms case2164

theorem case3188 : checkNat 3188 = true := by
  apply check_of_normalize (Case.ofNat 3188)
  have he : (Case.ofNat 3188).normalize = Case.ofNat 116 := by decide
  rw [he]
  exact case0116
#print axioms case3188

theorem case0117 : checkNat 117 = true := by native_decide
#print axioms case0117

theorem case2165 : checkNat 2165 = true := by
  apply check_of_normalize (Case.ofNat 2165)
  have he : (Case.ofNat 2165).normalize = Case.ofNat 117 := by decide
  rw [he]
  exact case0117
#print axioms case2165

theorem case0118 : checkNat 118 = true := by native_decide
#print axioms case0118

theorem case1142 : checkNat 1142 = true := by
  apply check_of_normalize (Case.ofNat 1142)
  have he : (Case.ofNat 1142).normalize = Case.ofNat 118 := by decide
  rw [he]
  exact case0118
#print axioms case1142

theorem case0119 : checkNat 119 = true := by native_decide
#print axioms case0119

theorem case0120 : checkNat 120 = true := by native_decide
#print axioms case0120

theorem case1144 : checkNat 1144 = true := by
  apply check_of_normalize (Case.ofNat 1144)
  have he : (Case.ofNat 1144).normalize = Case.ofNat 120 := by decide
  rw [he]
  exact case0120
#print axioms case1144

theorem case2168 : checkNat 2168 = true := by
  apply check_of_normalize (Case.ofNat 2168)
  have he : (Case.ofNat 2168).normalize = Case.ofNat 120 := by decide
  rw [he]
  exact case0120
#print axioms case2168

theorem case3192 : checkNat 3192 = true := by
  apply check_of_normalize (Case.ofNat 3192)
  have he : (Case.ofNat 3192).normalize = Case.ofNat 120 := by decide
  rw [he]
  exact case0120
#print axioms case3192

theorem case0121 : checkNat 121 = true := by native_decide
#print axioms case0121

theorem case2169 : checkNat 2169 = true := by
  apply check_of_normalize (Case.ofNat 2169)
  have he : (Case.ofNat 2169).normalize = Case.ofNat 121 := by decide
  rw [he]
  exact case0121
#print axioms case2169

theorem case0122 : checkNat 122 = true := by native_decide
#print axioms case0122

theorem case1146 : checkNat 1146 = true := by
  apply check_of_normalize (Case.ofNat 1146)
  have he : (Case.ofNat 1146).normalize = Case.ofNat 122 := by decide
  rw [he]
  exact case0122
#print axioms case1146

theorem case0123 : checkNat 123 = true := by native_decide
#print axioms case0123

theorem case0124 : checkNat 124 = true := by native_decide
#print axioms case0124

theorem case1148 : checkNat 1148 = true := by
  apply check_of_normalize (Case.ofNat 1148)
  have he : (Case.ofNat 1148).normalize = Case.ofNat 124 := by decide
  rw [he]
  exact case0124
#print axioms case1148

theorem case2172 : checkNat 2172 = true := by
  apply check_of_normalize (Case.ofNat 2172)
  have he : (Case.ofNat 2172).normalize = Case.ofNat 124 := by decide
  rw [he]
  exact case0124
#print axioms case2172

theorem case3196 : checkNat 3196 = true := by
  apply check_of_normalize (Case.ofNat 3196)
  have he : (Case.ofNat 3196).normalize = Case.ofNat 124 := by decide
  rw [he]
  exact case0124
#print axioms case3196

theorem case0125 : checkNat 125 = true := by native_decide
#print axioms case0125

theorem case2173 : checkNat 2173 = true := by
  apply check_of_normalize (Case.ofNat 2173)
  have he : (Case.ofNat 2173).normalize = Case.ofNat 125 := by decide
  rw [he]
  exact case0125
#print axioms case2173

theorem case0126 : checkNat 126 = true := by native_decide
#print axioms case0126

theorem case1150 : checkNat 1150 = true := by
  apply check_of_normalize (Case.ofNat 1150)
  have he : (Case.ofNat 1150).normalize = Case.ofNat 126 := by decide
  rw [he]
  exact case0126
#print axioms case1150

theorem case0127 : checkNat 127 = true := by native_decide
#print axioms case0127

theorem accepted :
    checkNat 96 = true ∧
    checkNat 97 = true ∧
    checkNat 98 = true ∧
    checkNat 99 = true ∧
    checkNat 100 = true ∧
    checkNat 101 = true ∧
    checkNat 102 = true ∧
    checkNat 103 = true ∧
    checkNat 104 = true ∧
    checkNat 105 = true ∧
    checkNat 106 = true ∧
    checkNat 107 = true ∧
    checkNat 108 = true ∧
    checkNat 109 = true ∧
    checkNat 110 = true ∧
    checkNat 111 = true ∧
    checkNat 112 = true ∧
    checkNat 113 = true ∧
    checkNat 114 = true ∧
    checkNat 115 = true ∧
    checkNat 116 = true ∧
    checkNat 117 = true ∧
    checkNat 118 = true ∧
    checkNat 119 = true ∧
    checkNat 120 = true ∧
    checkNat 121 = true ∧
    checkNat 122 = true ∧
    checkNat 123 = true ∧
    checkNat 124 = true ∧
    checkNat 125 = true ∧
    checkNat 126 = true ∧
    checkNat 127 = true ∧
    checkNat 1120 = true ∧
    checkNat 1122 = true ∧
    checkNat 1124 = true ∧
    checkNat 1126 = true ∧
    checkNat 1128 = true ∧
    checkNat 1130 = true ∧
    checkNat 1132 = true ∧
    checkNat 1134 = true ∧
    checkNat 1136 = true ∧
    checkNat 1138 = true ∧
    checkNat 1140 = true ∧
    checkNat 1142 = true ∧
    checkNat 1144 = true ∧
    checkNat 1146 = true ∧
    checkNat 1148 = true ∧
    checkNat 1150 = true ∧
    checkNat 2144 = true ∧
    checkNat 2145 = true ∧
    checkNat 2148 = true ∧
    checkNat 2149 = true ∧
    checkNat 2152 = true ∧
    checkNat 2153 = true ∧
    checkNat 2156 = true ∧
    checkNat 2157 = true ∧
    checkNat 2160 = true ∧
    checkNat 2161 = true ∧
    checkNat 2164 = true ∧
    checkNat 2165 = true ∧
    checkNat 2168 = true ∧
    checkNat 2169 = true ∧
    checkNat 2172 = true ∧
    checkNat 2173 = true ∧
    checkNat 3168 = true ∧
    checkNat 3172 = true ∧
    checkNat 3176 = true ∧
    checkNat 3180 = true ∧
    checkNat 3184 = true ∧
    checkNat 3188 = true ∧
    checkNat 3192 = true ∧
    checkNat 3196 = true := by
  exact ⟨case0096, case0097, case0098, case0099, case0100, case0101, case0102, case0103, case0104, case0105, case0106, case0107, case0108, case0109, case0110, case0111, case0112, case0113, case0114, case0115, case0116, case0117, case0118, case0119, case0120, case0121, case0122, case0123, case0124, case0125, case0126, case0127, case1120, case1122, case1124, case1126, case1128, case1130, case1132, case1134, case1136, case1138, case1140, case1142, case1144, case1146, case1148, case1150, case2144, case2145, case2148, case2149, case2152, case2153, case2156, case2157, case2160, case2161, case2164, case2165, case2168, case2169, case2172, case2173, case3168, case3172, case3176, case3180, case3184, case3188, case3192, case3196⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0096
