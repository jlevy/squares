import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0128
open Sq19.Endgame.Reduction

theorem case0128 : checkNat 128 = true := by native_decide
#print axioms case0128

theorem case1152 : checkNat 1152 = true := by
  apply check_of_normalize (Case.ofNat 1152)
  have he : (Case.ofNat 1152).normalize = Case.ofNat 128 := by decide
  rw [he]
  exact case0128
#print axioms case1152

theorem case2176 : checkNat 2176 = true := by
  apply check_of_normalize (Case.ofNat 2176)
  have he : (Case.ofNat 2176).normalize = Case.ofNat 128 := by decide
  rw [he]
  exact case0128
#print axioms case2176

theorem case3200 : checkNat 3200 = true := by
  apply check_of_normalize (Case.ofNat 3200)
  have he : (Case.ofNat 3200).normalize = Case.ofNat 128 := by decide
  rw [he]
  exact case0128
#print axioms case3200

theorem case0129 : checkNat 129 = true := by native_decide
#print axioms case0129

theorem case2177 : checkNat 2177 = true := by
  apply check_of_normalize (Case.ofNat 2177)
  have he : (Case.ofNat 2177).normalize = Case.ofNat 129 := by decide
  rw [he]
  exact case0129
#print axioms case2177

theorem case0130 : checkNat 130 = true := by native_decide
#print axioms case0130

theorem case1154 : checkNat 1154 = true := by
  apply check_of_normalize (Case.ofNat 1154)
  have he : (Case.ofNat 1154).normalize = Case.ofNat 130 := by decide
  rw [he]
  exact case0130
#print axioms case1154

theorem case0131 : checkNat 131 = true := by native_decide
#print axioms case0131

theorem case0132 : checkNat 132 = true := by native_decide
#print axioms case0132

theorem case1156 : checkNat 1156 = true := by
  apply check_of_normalize (Case.ofNat 1156)
  have he : (Case.ofNat 1156).normalize = Case.ofNat 132 := by decide
  rw [he]
  exact case0132
#print axioms case1156

theorem case2180 : checkNat 2180 = true := by
  apply check_of_normalize (Case.ofNat 2180)
  have he : (Case.ofNat 2180).normalize = Case.ofNat 132 := by decide
  rw [he]
  exact case0132
#print axioms case2180

theorem case3204 : checkNat 3204 = true := by
  apply check_of_normalize (Case.ofNat 3204)
  have he : (Case.ofNat 3204).normalize = Case.ofNat 132 := by decide
  rw [he]
  exact case0132
#print axioms case3204

theorem case0133 : checkNat 133 = true := by native_decide
#print axioms case0133

theorem case2181 : checkNat 2181 = true := by
  apply check_of_normalize (Case.ofNat 2181)
  have he : (Case.ofNat 2181).normalize = Case.ofNat 133 := by decide
  rw [he]
  exact case0133
#print axioms case2181

theorem case0134 : checkNat 134 = true := by native_decide
#print axioms case0134

theorem case1158 : checkNat 1158 = true := by
  apply check_of_normalize (Case.ofNat 1158)
  have he : (Case.ofNat 1158).normalize = Case.ofNat 134 := by decide
  rw [he]
  exact case0134
#print axioms case1158

theorem case0135 : checkNat 135 = true := by native_decide
#print axioms case0135

theorem case0136 : checkNat 136 = true := by native_decide
#print axioms case0136

theorem case1160 : checkNat 1160 = true := by
  apply check_of_normalize (Case.ofNat 1160)
  have he : (Case.ofNat 1160).normalize = Case.ofNat 136 := by decide
  rw [he]
  exact case0136
#print axioms case1160

theorem case2184 : checkNat 2184 = true := by
  apply check_of_normalize (Case.ofNat 2184)
  have he : (Case.ofNat 2184).normalize = Case.ofNat 136 := by decide
  rw [he]
  exact case0136
#print axioms case2184

theorem case3208 : checkNat 3208 = true := by
  apply check_of_normalize (Case.ofNat 3208)
  have he : (Case.ofNat 3208).normalize = Case.ofNat 136 := by decide
  rw [he]
  exact case0136
#print axioms case3208

theorem case0137 : checkNat 137 = true := by native_decide
#print axioms case0137

theorem case2185 : checkNat 2185 = true := by
  apply check_of_normalize (Case.ofNat 2185)
  have he : (Case.ofNat 2185).normalize = Case.ofNat 137 := by decide
  rw [he]
  exact case0137
#print axioms case2185

theorem case0138 : checkNat 138 = true := by native_decide
#print axioms case0138

theorem case1162 : checkNat 1162 = true := by
  apply check_of_normalize (Case.ofNat 1162)
  have he : (Case.ofNat 1162).normalize = Case.ofNat 138 := by decide
  rw [he]
  exact case0138
#print axioms case1162

theorem case0139 : checkNat 139 = true := by native_decide
#print axioms case0139

theorem case0140 : checkNat 140 = true := by native_decide
#print axioms case0140

theorem case1164 : checkNat 1164 = true := by
  apply check_of_normalize (Case.ofNat 1164)
  have he : (Case.ofNat 1164).normalize = Case.ofNat 140 := by decide
  rw [he]
  exact case0140
#print axioms case1164

theorem case2188 : checkNat 2188 = true := by
  apply check_of_normalize (Case.ofNat 2188)
  have he : (Case.ofNat 2188).normalize = Case.ofNat 140 := by decide
  rw [he]
  exact case0140
#print axioms case2188

theorem case3212 : checkNat 3212 = true := by
  apply check_of_normalize (Case.ofNat 3212)
  have he : (Case.ofNat 3212).normalize = Case.ofNat 140 := by decide
  rw [he]
  exact case0140
#print axioms case3212

theorem case0141 : checkNat 141 = true := by native_decide
#print axioms case0141

theorem case2189 : checkNat 2189 = true := by
  apply check_of_normalize (Case.ofNat 2189)
  have he : (Case.ofNat 2189).normalize = Case.ofNat 141 := by decide
  rw [he]
  exact case0141
#print axioms case2189

theorem case0142 : checkNat 142 = true := by native_decide
#print axioms case0142

theorem case1166 : checkNat 1166 = true := by
  apply check_of_normalize (Case.ofNat 1166)
  have he : (Case.ofNat 1166).normalize = Case.ofNat 142 := by decide
  rw [he]
  exact case0142
#print axioms case1166

theorem case0143 : checkNat 143 = true := by native_decide
#print axioms case0143

theorem case0144 : checkNat 144 = true := by native_decide
#print axioms case0144

theorem case1168 : checkNat 1168 = true := by
  apply check_of_normalize (Case.ofNat 1168)
  have he : (Case.ofNat 1168).normalize = Case.ofNat 144 := by decide
  rw [he]
  exact case0144
#print axioms case1168

theorem case2192 : checkNat 2192 = true := by
  apply check_of_normalize (Case.ofNat 2192)
  have he : (Case.ofNat 2192).normalize = Case.ofNat 144 := by decide
  rw [he]
  exact case0144
#print axioms case2192

theorem case3216 : checkNat 3216 = true := by
  apply check_of_normalize (Case.ofNat 3216)
  have he : (Case.ofNat 3216).normalize = Case.ofNat 144 := by decide
  rw [he]
  exact case0144
#print axioms case3216

theorem case0145 : checkNat 145 = true := by native_decide
#print axioms case0145

theorem case2193 : checkNat 2193 = true := by
  apply check_of_normalize (Case.ofNat 2193)
  have he : (Case.ofNat 2193).normalize = Case.ofNat 145 := by decide
  rw [he]
  exact case0145
#print axioms case2193

theorem case0146 : checkNat 146 = true := by native_decide
#print axioms case0146

theorem case1170 : checkNat 1170 = true := by
  apply check_of_normalize (Case.ofNat 1170)
  have he : (Case.ofNat 1170).normalize = Case.ofNat 146 := by decide
  rw [he]
  exact case0146
#print axioms case1170

theorem case0147 : checkNat 147 = true := by native_decide
#print axioms case0147

theorem case0148 : checkNat 148 = true := by native_decide
#print axioms case0148

theorem case1172 : checkNat 1172 = true := by
  apply check_of_normalize (Case.ofNat 1172)
  have he : (Case.ofNat 1172).normalize = Case.ofNat 148 := by decide
  rw [he]
  exact case0148
#print axioms case1172

theorem case2196 : checkNat 2196 = true := by
  apply check_of_normalize (Case.ofNat 2196)
  have he : (Case.ofNat 2196).normalize = Case.ofNat 148 := by decide
  rw [he]
  exact case0148
#print axioms case2196

theorem case3220 : checkNat 3220 = true := by
  apply check_of_normalize (Case.ofNat 3220)
  have he : (Case.ofNat 3220).normalize = Case.ofNat 148 := by decide
  rw [he]
  exact case0148
#print axioms case3220

theorem case0149 : checkNat 149 = true := by native_decide
#print axioms case0149

theorem case2197 : checkNat 2197 = true := by
  apply check_of_normalize (Case.ofNat 2197)
  have he : (Case.ofNat 2197).normalize = Case.ofNat 149 := by decide
  rw [he]
  exact case0149
#print axioms case2197

theorem case0150 : checkNat 150 = true := by native_decide
#print axioms case0150

theorem case1174 : checkNat 1174 = true := by
  apply check_of_normalize (Case.ofNat 1174)
  have he : (Case.ofNat 1174).normalize = Case.ofNat 150 := by decide
  rw [he]
  exact case0150
#print axioms case1174

theorem case0151 : checkNat 151 = true := by native_decide
#print axioms case0151

theorem case0152 : checkNat 152 = true := by native_decide
#print axioms case0152

theorem case1176 : checkNat 1176 = true := by
  apply check_of_normalize (Case.ofNat 1176)
  have he : (Case.ofNat 1176).normalize = Case.ofNat 152 := by decide
  rw [he]
  exact case0152
#print axioms case1176

theorem case2200 : checkNat 2200 = true := by
  apply check_of_normalize (Case.ofNat 2200)
  have he : (Case.ofNat 2200).normalize = Case.ofNat 152 := by decide
  rw [he]
  exact case0152
#print axioms case2200

theorem case3224 : checkNat 3224 = true := by
  apply check_of_normalize (Case.ofNat 3224)
  have he : (Case.ofNat 3224).normalize = Case.ofNat 152 := by decide
  rw [he]
  exact case0152
#print axioms case3224

theorem case0153 : checkNat 153 = true := by native_decide
#print axioms case0153

theorem case2201 : checkNat 2201 = true := by
  apply check_of_normalize (Case.ofNat 2201)
  have he : (Case.ofNat 2201).normalize = Case.ofNat 153 := by decide
  rw [he]
  exact case0153
#print axioms case2201

theorem case0154 : checkNat 154 = true := by native_decide
#print axioms case0154

theorem case1178 : checkNat 1178 = true := by
  apply check_of_normalize (Case.ofNat 1178)
  have he : (Case.ofNat 1178).normalize = Case.ofNat 154 := by decide
  rw [he]
  exact case0154
#print axioms case1178

theorem case0155 : checkNat 155 = true := by native_decide
#print axioms case0155

theorem case0156 : checkNat 156 = true := by native_decide
#print axioms case0156

theorem case1180 : checkNat 1180 = true := by
  apply check_of_normalize (Case.ofNat 1180)
  have he : (Case.ofNat 1180).normalize = Case.ofNat 156 := by decide
  rw [he]
  exact case0156
#print axioms case1180

theorem case2204 : checkNat 2204 = true := by
  apply check_of_normalize (Case.ofNat 2204)
  have he : (Case.ofNat 2204).normalize = Case.ofNat 156 := by decide
  rw [he]
  exact case0156
#print axioms case2204

theorem case3228 : checkNat 3228 = true := by
  apply check_of_normalize (Case.ofNat 3228)
  have he : (Case.ofNat 3228).normalize = Case.ofNat 156 := by decide
  rw [he]
  exact case0156
#print axioms case3228

theorem case0157 : checkNat 157 = true := by native_decide
#print axioms case0157

theorem case2205 : checkNat 2205 = true := by
  apply check_of_normalize (Case.ofNat 2205)
  have he : (Case.ofNat 2205).normalize = Case.ofNat 157 := by decide
  rw [he]
  exact case0157
#print axioms case2205

theorem case0158 : checkNat 158 = true := by native_decide
#print axioms case0158

theorem case1182 : checkNat 1182 = true := by
  apply check_of_normalize (Case.ofNat 1182)
  have he : (Case.ofNat 1182).normalize = Case.ofNat 158 := by decide
  rw [he]
  exact case0158
#print axioms case1182

theorem case0159 : checkNat 159 = true := by native_decide
#print axioms case0159

theorem accepted :
    checkNat 128 = true ∧
    checkNat 129 = true ∧
    checkNat 130 = true ∧
    checkNat 131 = true ∧
    checkNat 132 = true ∧
    checkNat 133 = true ∧
    checkNat 134 = true ∧
    checkNat 135 = true ∧
    checkNat 136 = true ∧
    checkNat 137 = true ∧
    checkNat 138 = true ∧
    checkNat 139 = true ∧
    checkNat 140 = true ∧
    checkNat 141 = true ∧
    checkNat 142 = true ∧
    checkNat 143 = true ∧
    checkNat 144 = true ∧
    checkNat 145 = true ∧
    checkNat 146 = true ∧
    checkNat 147 = true ∧
    checkNat 148 = true ∧
    checkNat 149 = true ∧
    checkNat 150 = true ∧
    checkNat 151 = true ∧
    checkNat 152 = true ∧
    checkNat 153 = true ∧
    checkNat 154 = true ∧
    checkNat 155 = true ∧
    checkNat 156 = true ∧
    checkNat 157 = true ∧
    checkNat 158 = true ∧
    checkNat 159 = true ∧
    checkNat 1152 = true ∧
    checkNat 1154 = true ∧
    checkNat 1156 = true ∧
    checkNat 1158 = true ∧
    checkNat 1160 = true ∧
    checkNat 1162 = true ∧
    checkNat 1164 = true ∧
    checkNat 1166 = true ∧
    checkNat 1168 = true ∧
    checkNat 1170 = true ∧
    checkNat 1172 = true ∧
    checkNat 1174 = true ∧
    checkNat 1176 = true ∧
    checkNat 1178 = true ∧
    checkNat 1180 = true ∧
    checkNat 1182 = true ∧
    checkNat 2176 = true ∧
    checkNat 2177 = true ∧
    checkNat 2180 = true ∧
    checkNat 2181 = true ∧
    checkNat 2184 = true ∧
    checkNat 2185 = true ∧
    checkNat 2188 = true ∧
    checkNat 2189 = true ∧
    checkNat 2192 = true ∧
    checkNat 2193 = true ∧
    checkNat 2196 = true ∧
    checkNat 2197 = true ∧
    checkNat 2200 = true ∧
    checkNat 2201 = true ∧
    checkNat 2204 = true ∧
    checkNat 2205 = true ∧
    checkNat 3200 = true ∧
    checkNat 3204 = true ∧
    checkNat 3208 = true ∧
    checkNat 3212 = true ∧
    checkNat 3216 = true ∧
    checkNat 3220 = true ∧
    checkNat 3224 = true ∧
    checkNat 3228 = true := by
  exact ⟨case0128, case0129, case0130, case0131, case0132, case0133, case0134, case0135, case0136, case0137, case0138, case0139, case0140, case0141, case0142, case0143, case0144, case0145, case0146, case0147, case0148, case0149, case0150, case0151, case0152, case0153, case0154, case0155, case0156, case0157, case0158, case0159, case1152, case1154, case1156, case1158, case1160, case1162, case1164, case1166, case1168, case1170, case1172, case1174, case1176, case1178, case1180, case1182, case2176, case2177, case2180, case2181, case2184, case2185, case2188, case2189, case2192, case2193, case2196, case2197, case2200, case2201, case2204, case2205, case3200, case3204, case3208, case3212, case3216, case3220, case3224, case3228⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0128
