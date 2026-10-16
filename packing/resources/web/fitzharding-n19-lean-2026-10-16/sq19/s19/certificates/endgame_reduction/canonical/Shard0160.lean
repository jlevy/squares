import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0160
open Sq19.Endgame.Reduction

theorem case0160 : checkNat 160 = true := by native_decide
#print axioms case0160

theorem case1184 : checkNat 1184 = true := by
  apply check_of_normalize (Case.ofNat 1184)
  have he : (Case.ofNat 1184).normalize = Case.ofNat 160 := by decide
  rw [he]
  exact case0160
#print axioms case1184

theorem case2208 : checkNat 2208 = true := by
  apply check_of_normalize (Case.ofNat 2208)
  have he : (Case.ofNat 2208).normalize = Case.ofNat 160 := by decide
  rw [he]
  exact case0160
#print axioms case2208

theorem case3232 : checkNat 3232 = true := by
  apply check_of_normalize (Case.ofNat 3232)
  have he : (Case.ofNat 3232).normalize = Case.ofNat 160 := by decide
  rw [he]
  exact case0160
#print axioms case3232

theorem case0161 : checkNat 161 = true := by native_decide
#print axioms case0161

theorem case2209 : checkNat 2209 = true := by
  apply check_of_normalize (Case.ofNat 2209)
  have he : (Case.ofNat 2209).normalize = Case.ofNat 161 := by decide
  rw [he]
  exact case0161
#print axioms case2209

theorem case0162 : checkNat 162 = true := by native_decide
#print axioms case0162

theorem case1186 : checkNat 1186 = true := by
  apply check_of_normalize (Case.ofNat 1186)
  have he : (Case.ofNat 1186).normalize = Case.ofNat 162 := by decide
  rw [he]
  exact case0162
#print axioms case1186

theorem case0163 : checkNat 163 = true := by native_decide
#print axioms case0163

theorem case0164 : checkNat 164 = true := by native_decide
#print axioms case0164

theorem case1188 : checkNat 1188 = true := by
  apply check_of_normalize (Case.ofNat 1188)
  have he : (Case.ofNat 1188).normalize = Case.ofNat 164 := by decide
  rw [he]
  exact case0164
#print axioms case1188

theorem case2212 : checkNat 2212 = true := by
  apply check_of_normalize (Case.ofNat 2212)
  have he : (Case.ofNat 2212).normalize = Case.ofNat 164 := by decide
  rw [he]
  exact case0164
#print axioms case2212

theorem case3236 : checkNat 3236 = true := by
  apply check_of_normalize (Case.ofNat 3236)
  have he : (Case.ofNat 3236).normalize = Case.ofNat 164 := by decide
  rw [he]
  exact case0164
#print axioms case3236

theorem case0165 : checkNat 165 = true := by native_decide
#print axioms case0165

theorem case2213 : checkNat 2213 = true := by
  apply check_of_normalize (Case.ofNat 2213)
  have he : (Case.ofNat 2213).normalize = Case.ofNat 165 := by decide
  rw [he]
  exact case0165
#print axioms case2213

theorem case0166 : checkNat 166 = true := by native_decide
#print axioms case0166

theorem case1190 : checkNat 1190 = true := by
  apply check_of_normalize (Case.ofNat 1190)
  have he : (Case.ofNat 1190).normalize = Case.ofNat 166 := by decide
  rw [he]
  exact case0166
#print axioms case1190

theorem case0167 : checkNat 167 = true := by native_decide
#print axioms case0167

theorem case0168 : checkNat 168 = true := by native_decide
#print axioms case0168

theorem case1192 : checkNat 1192 = true := by
  apply check_of_normalize (Case.ofNat 1192)
  have he : (Case.ofNat 1192).normalize = Case.ofNat 168 := by decide
  rw [he]
  exact case0168
#print axioms case1192

theorem case2216 : checkNat 2216 = true := by
  apply check_of_normalize (Case.ofNat 2216)
  have he : (Case.ofNat 2216).normalize = Case.ofNat 168 := by decide
  rw [he]
  exact case0168
#print axioms case2216

theorem case3240 : checkNat 3240 = true := by
  apply check_of_normalize (Case.ofNat 3240)
  have he : (Case.ofNat 3240).normalize = Case.ofNat 168 := by decide
  rw [he]
  exact case0168
#print axioms case3240

theorem case0169 : checkNat 169 = true := by native_decide
#print axioms case0169

theorem case2217 : checkNat 2217 = true := by
  apply check_of_normalize (Case.ofNat 2217)
  have he : (Case.ofNat 2217).normalize = Case.ofNat 169 := by decide
  rw [he]
  exact case0169
#print axioms case2217

theorem case0170 : checkNat 170 = true := by native_decide
#print axioms case0170

theorem case1194 : checkNat 1194 = true := by
  apply check_of_normalize (Case.ofNat 1194)
  have he : (Case.ofNat 1194).normalize = Case.ofNat 170 := by decide
  rw [he]
  exact case0170
#print axioms case1194

theorem case0171 : checkNat 171 = true := by native_decide
#print axioms case0171

theorem case0172 : checkNat 172 = true := by native_decide
#print axioms case0172

theorem case1196 : checkNat 1196 = true := by
  apply check_of_normalize (Case.ofNat 1196)
  have he : (Case.ofNat 1196).normalize = Case.ofNat 172 := by decide
  rw [he]
  exact case0172
#print axioms case1196

theorem case2220 : checkNat 2220 = true := by
  apply check_of_normalize (Case.ofNat 2220)
  have he : (Case.ofNat 2220).normalize = Case.ofNat 172 := by decide
  rw [he]
  exact case0172
#print axioms case2220

theorem case3244 : checkNat 3244 = true := by
  apply check_of_normalize (Case.ofNat 3244)
  have he : (Case.ofNat 3244).normalize = Case.ofNat 172 := by decide
  rw [he]
  exact case0172
#print axioms case3244

theorem case0173 : checkNat 173 = true := by native_decide
#print axioms case0173

theorem case2221 : checkNat 2221 = true := by
  apply check_of_normalize (Case.ofNat 2221)
  have he : (Case.ofNat 2221).normalize = Case.ofNat 173 := by decide
  rw [he]
  exact case0173
#print axioms case2221

theorem case0174 : checkNat 174 = true := by native_decide
#print axioms case0174

theorem case1198 : checkNat 1198 = true := by
  apply check_of_normalize (Case.ofNat 1198)
  have he : (Case.ofNat 1198).normalize = Case.ofNat 174 := by decide
  rw [he]
  exact case0174
#print axioms case1198

theorem case0175 : checkNat 175 = true := by native_decide
#print axioms case0175

theorem case0176 : checkNat 176 = true := by native_decide
#print axioms case0176

theorem case1200 : checkNat 1200 = true := by
  apply check_of_normalize (Case.ofNat 1200)
  have he : (Case.ofNat 1200).normalize = Case.ofNat 176 := by decide
  rw [he]
  exact case0176
#print axioms case1200

theorem case2224 : checkNat 2224 = true := by
  apply check_of_normalize (Case.ofNat 2224)
  have he : (Case.ofNat 2224).normalize = Case.ofNat 176 := by decide
  rw [he]
  exact case0176
#print axioms case2224

theorem case3248 : checkNat 3248 = true := by
  apply check_of_normalize (Case.ofNat 3248)
  have he : (Case.ofNat 3248).normalize = Case.ofNat 176 := by decide
  rw [he]
  exact case0176
#print axioms case3248

theorem case0177 : checkNat 177 = true := by native_decide
#print axioms case0177

theorem case2225 : checkNat 2225 = true := by
  apply check_of_normalize (Case.ofNat 2225)
  have he : (Case.ofNat 2225).normalize = Case.ofNat 177 := by decide
  rw [he]
  exact case0177
#print axioms case2225

theorem case0178 : checkNat 178 = true := by native_decide
#print axioms case0178

theorem case1202 : checkNat 1202 = true := by
  apply check_of_normalize (Case.ofNat 1202)
  have he : (Case.ofNat 1202).normalize = Case.ofNat 178 := by decide
  rw [he]
  exact case0178
#print axioms case1202

theorem case0179 : checkNat 179 = true := by native_decide
#print axioms case0179

theorem case0180 : checkNat 180 = true := by native_decide
#print axioms case0180

theorem case1204 : checkNat 1204 = true := by
  apply check_of_normalize (Case.ofNat 1204)
  have he : (Case.ofNat 1204).normalize = Case.ofNat 180 := by decide
  rw [he]
  exact case0180
#print axioms case1204

theorem case2228 : checkNat 2228 = true := by
  apply check_of_normalize (Case.ofNat 2228)
  have he : (Case.ofNat 2228).normalize = Case.ofNat 180 := by decide
  rw [he]
  exact case0180
#print axioms case2228

theorem case3252 : checkNat 3252 = true := by
  apply check_of_normalize (Case.ofNat 3252)
  have he : (Case.ofNat 3252).normalize = Case.ofNat 180 := by decide
  rw [he]
  exact case0180
#print axioms case3252

theorem case0181 : checkNat 181 = true := by native_decide
#print axioms case0181

theorem case2229 : checkNat 2229 = true := by
  apply check_of_normalize (Case.ofNat 2229)
  have he : (Case.ofNat 2229).normalize = Case.ofNat 181 := by decide
  rw [he]
  exact case0181
#print axioms case2229

theorem case0182 : checkNat 182 = true := by native_decide
#print axioms case0182

theorem case1206 : checkNat 1206 = true := by
  apply check_of_normalize (Case.ofNat 1206)
  have he : (Case.ofNat 1206).normalize = Case.ofNat 182 := by decide
  rw [he]
  exact case0182
#print axioms case1206

theorem case0183 : checkNat 183 = true := by native_decide
#print axioms case0183

theorem case0184 : checkNat 184 = true := by native_decide
#print axioms case0184

theorem case1208 : checkNat 1208 = true := by
  apply check_of_normalize (Case.ofNat 1208)
  have he : (Case.ofNat 1208).normalize = Case.ofNat 184 := by decide
  rw [he]
  exact case0184
#print axioms case1208

theorem case2232 : checkNat 2232 = true := by
  apply check_of_normalize (Case.ofNat 2232)
  have he : (Case.ofNat 2232).normalize = Case.ofNat 184 := by decide
  rw [he]
  exact case0184
#print axioms case2232

theorem case3256 : checkNat 3256 = true := by
  apply check_of_normalize (Case.ofNat 3256)
  have he : (Case.ofNat 3256).normalize = Case.ofNat 184 := by decide
  rw [he]
  exact case0184
#print axioms case3256

theorem case0185 : checkNat 185 = true := by native_decide
#print axioms case0185

theorem case2233 : checkNat 2233 = true := by
  apply check_of_normalize (Case.ofNat 2233)
  have he : (Case.ofNat 2233).normalize = Case.ofNat 185 := by decide
  rw [he]
  exact case0185
#print axioms case2233

theorem case0186 : checkNat 186 = true := by native_decide
#print axioms case0186

theorem case1210 : checkNat 1210 = true := by
  apply check_of_normalize (Case.ofNat 1210)
  have he : (Case.ofNat 1210).normalize = Case.ofNat 186 := by decide
  rw [he]
  exact case0186
#print axioms case1210

theorem case0187 : checkNat 187 = true := by native_decide
#print axioms case0187

theorem case0188 : checkNat 188 = true := by native_decide
#print axioms case0188

theorem case1212 : checkNat 1212 = true := by
  apply check_of_normalize (Case.ofNat 1212)
  have he : (Case.ofNat 1212).normalize = Case.ofNat 188 := by decide
  rw [he]
  exact case0188
#print axioms case1212

theorem case2236 : checkNat 2236 = true := by
  apply check_of_normalize (Case.ofNat 2236)
  have he : (Case.ofNat 2236).normalize = Case.ofNat 188 := by decide
  rw [he]
  exact case0188
#print axioms case2236

theorem case3260 : checkNat 3260 = true := by
  apply check_of_normalize (Case.ofNat 3260)
  have he : (Case.ofNat 3260).normalize = Case.ofNat 188 := by decide
  rw [he]
  exact case0188
#print axioms case3260

theorem case0189 : checkNat 189 = true := by native_decide
#print axioms case0189

theorem case2237 : checkNat 2237 = true := by
  apply check_of_normalize (Case.ofNat 2237)
  have he : (Case.ofNat 2237).normalize = Case.ofNat 189 := by decide
  rw [he]
  exact case0189
#print axioms case2237

theorem case0190 : checkNat 190 = true := by native_decide
#print axioms case0190

theorem case1214 : checkNat 1214 = true := by
  apply check_of_normalize (Case.ofNat 1214)
  have he : (Case.ofNat 1214).normalize = Case.ofNat 190 := by decide
  rw [he]
  exact case0190
#print axioms case1214

theorem case0191 : checkNat 191 = true := by native_decide
#print axioms case0191

theorem accepted :
    checkNat 160 = true ∧
    checkNat 161 = true ∧
    checkNat 162 = true ∧
    checkNat 163 = true ∧
    checkNat 164 = true ∧
    checkNat 165 = true ∧
    checkNat 166 = true ∧
    checkNat 167 = true ∧
    checkNat 168 = true ∧
    checkNat 169 = true ∧
    checkNat 170 = true ∧
    checkNat 171 = true ∧
    checkNat 172 = true ∧
    checkNat 173 = true ∧
    checkNat 174 = true ∧
    checkNat 175 = true ∧
    checkNat 176 = true ∧
    checkNat 177 = true ∧
    checkNat 178 = true ∧
    checkNat 179 = true ∧
    checkNat 180 = true ∧
    checkNat 181 = true ∧
    checkNat 182 = true ∧
    checkNat 183 = true ∧
    checkNat 184 = true ∧
    checkNat 185 = true ∧
    checkNat 186 = true ∧
    checkNat 187 = true ∧
    checkNat 188 = true ∧
    checkNat 189 = true ∧
    checkNat 190 = true ∧
    checkNat 191 = true ∧
    checkNat 1184 = true ∧
    checkNat 1186 = true ∧
    checkNat 1188 = true ∧
    checkNat 1190 = true ∧
    checkNat 1192 = true ∧
    checkNat 1194 = true ∧
    checkNat 1196 = true ∧
    checkNat 1198 = true ∧
    checkNat 1200 = true ∧
    checkNat 1202 = true ∧
    checkNat 1204 = true ∧
    checkNat 1206 = true ∧
    checkNat 1208 = true ∧
    checkNat 1210 = true ∧
    checkNat 1212 = true ∧
    checkNat 1214 = true ∧
    checkNat 2208 = true ∧
    checkNat 2209 = true ∧
    checkNat 2212 = true ∧
    checkNat 2213 = true ∧
    checkNat 2216 = true ∧
    checkNat 2217 = true ∧
    checkNat 2220 = true ∧
    checkNat 2221 = true ∧
    checkNat 2224 = true ∧
    checkNat 2225 = true ∧
    checkNat 2228 = true ∧
    checkNat 2229 = true ∧
    checkNat 2232 = true ∧
    checkNat 2233 = true ∧
    checkNat 2236 = true ∧
    checkNat 2237 = true ∧
    checkNat 3232 = true ∧
    checkNat 3236 = true ∧
    checkNat 3240 = true ∧
    checkNat 3244 = true ∧
    checkNat 3248 = true ∧
    checkNat 3252 = true ∧
    checkNat 3256 = true ∧
    checkNat 3260 = true := by
  exact ⟨case0160, case0161, case0162, case0163, case0164, case0165, case0166, case0167, case0168, case0169, case0170, case0171, case0172, case0173, case0174, case0175, case0176, case0177, case0178, case0179, case0180, case0181, case0182, case0183, case0184, case0185, case0186, case0187, case0188, case0189, case0190, case0191, case1184, case1186, case1188, case1190, case1192, case1194, case1196, case1198, case1200, case1202, case1204, case1206, case1208, case1210, case1212, case1214, case2208, case2209, case2212, case2213, case2216, case2217, case2220, case2221, case2224, case2225, case2228, case2229, case2232, case2233, case2236, case2237, case3232, case3236, case3240, case3244, case3248, case3252, case3256, case3260⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0160
