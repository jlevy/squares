import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0192
open Sq19.Endgame.Reduction

theorem case0192 : checkNat 192 = true := by native_decide
#print axioms case0192

theorem case1216 : checkNat 1216 = true := by
  apply check_of_normalize (Case.ofNat 1216)
  have he : (Case.ofNat 1216).normalize = Case.ofNat 192 := by decide
  rw [he]
  exact case0192
#print axioms case1216

theorem case2240 : checkNat 2240 = true := by
  apply check_of_normalize (Case.ofNat 2240)
  have he : (Case.ofNat 2240).normalize = Case.ofNat 192 := by decide
  rw [he]
  exact case0192
#print axioms case2240

theorem case3264 : checkNat 3264 = true := by
  apply check_of_normalize (Case.ofNat 3264)
  have he : (Case.ofNat 3264).normalize = Case.ofNat 192 := by decide
  rw [he]
  exact case0192
#print axioms case3264

theorem case0193 : checkNat 193 = true := by native_decide
#print axioms case0193

theorem case2241 : checkNat 2241 = true := by
  apply check_of_normalize (Case.ofNat 2241)
  have he : (Case.ofNat 2241).normalize = Case.ofNat 193 := by decide
  rw [he]
  exact case0193
#print axioms case2241

theorem case0194 : checkNat 194 = true := by native_decide
#print axioms case0194

theorem case1218 : checkNat 1218 = true := by
  apply check_of_normalize (Case.ofNat 1218)
  have he : (Case.ofNat 1218).normalize = Case.ofNat 194 := by decide
  rw [he]
  exact case0194
#print axioms case1218

theorem case0195 : checkNat 195 = true := by native_decide
#print axioms case0195

theorem case0196 : checkNat 196 = true := by native_decide
#print axioms case0196

theorem case1220 : checkNat 1220 = true := by
  apply check_of_normalize (Case.ofNat 1220)
  have he : (Case.ofNat 1220).normalize = Case.ofNat 196 := by decide
  rw [he]
  exact case0196
#print axioms case1220

theorem case2244 : checkNat 2244 = true := by
  apply check_of_normalize (Case.ofNat 2244)
  have he : (Case.ofNat 2244).normalize = Case.ofNat 196 := by decide
  rw [he]
  exact case0196
#print axioms case2244

theorem case3268 : checkNat 3268 = true := by
  apply check_of_normalize (Case.ofNat 3268)
  have he : (Case.ofNat 3268).normalize = Case.ofNat 196 := by decide
  rw [he]
  exact case0196
#print axioms case3268

theorem case0197 : checkNat 197 = true := by native_decide
#print axioms case0197

theorem case2245 : checkNat 2245 = true := by
  apply check_of_normalize (Case.ofNat 2245)
  have he : (Case.ofNat 2245).normalize = Case.ofNat 197 := by decide
  rw [he]
  exact case0197
#print axioms case2245

theorem case0198 : checkNat 198 = true := by native_decide
#print axioms case0198

theorem case1222 : checkNat 1222 = true := by
  apply check_of_normalize (Case.ofNat 1222)
  have he : (Case.ofNat 1222).normalize = Case.ofNat 198 := by decide
  rw [he]
  exact case0198
#print axioms case1222

theorem case0199 : checkNat 199 = true := by native_decide
#print axioms case0199

theorem case0200 : checkNat 200 = true := by native_decide
#print axioms case0200

theorem case1224 : checkNat 1224 = true := by
  apply check_of_normalize (Case.ofNat 1224)
  have he : (Case.ofNat 1224).normalize = Case.ofNat 200 := by decide
  rw [he]
  exact case0200
#print axioms case1224

theorem case2248 : checkNat 2248 = true := by
  apply check_of_normalize (Case.ofNat 2248)
  have he : (Case.ofNat 2248).normalize = Case.ofNat 200 := by decide
  rw [he]
  exact case0200
#print axioms case2248

theorem case3272 : checkNat 3272 = true := by
  apply check_of_normalize (Case.ofNat 3272)
  have he : (Case.ofNat 3272).normalize = Case.ofNat 200 := by decide
  rw [he]
  exact case0200
#print axioms case3272

theorem case0201 : checkNat 201 = true := by native_decide
#print axioms case0201

theorem case2249 : checkNat 2249 = true := by
  apply check_of_normalize (Case.ofNat 2249)
  have he : (Case.ofNat 2249).normalize = Case.ofNat 201 := by decide
  rw [he]
  exact case0201
#print axioms case2249

theorem case0202 : checkNat 202 = true := by native_decide
#print axioms case0202

theorem case1226 : checkNat 1226 = true := by
  apply check_of_normalize (Case.ofNat 1226)
  have he : (Case.ofNat 1226).normalize = Case.ofNat 202 := by decide
  rw [he]
  exact case0202
#print axioms case1226

theorem case0203 : checkNat 203 = true := by native_decide
#print axioms case0203

theorem case0204 : checkNat 204 = true := by native_decide
#print axioms case0204

theorem case1228 : checkNat 1228 = true := by
  apply check_of_normalize (Case.ofNat 1228)
  have he : (Case.ofNat 1228).normalize = Case.ofNat 204 := by decide
  rw [he]
  exact case0204
#print axioms case1228

theorem case2252 : checkNat 2252 = true := by
  apply check_of_normalize (Case.ofNat 2252)
  have he : (Case.ofNat 2252).normalize = Case.ofNat 204 := by decide
  rw [he]
  exact case0204
#print axioms case2252

theorem case3276 : checkNat 3276 = true := by
  apply check_of_normalize (Case.ofNat 3276)
  have he : (Case.ofNat 3276).normalize = Case.ofNat 204 := by decide
  rw [he]
  exact case0204
#print axioms case3276

theorem case0205 : checkNat 205 = true := by native_decide
#print axioms case0205

theorem case2253 : checkNat 2253 = true := by
  apply check_of_normalize (Case.ofNat 2253)
  have he : (Case.ofNat 2253).normalize = Case.ofNat 205 := by decide
  rw [he]
  exact case0205
#print axioms case2253

theorem case0206 : checkNat 206 = true := by native_decide
#print axioms case0206

theorem case1230 : checkNat 1230 = true := by
  apply check_of_normalize (Case.ofNat 1230)
  have he : (Case.ofNat 1230).normalize = Case.ofNat 206 := by decide
  rw [he]
  exact case0206
#print axioms case1230

theorem case0207 : checkNat 207 = true := by native_decide
#print axioms case0207

theorem case0208 : checkNat 208 = true := by native_decide
#print axioms case0208

theorem case1232 : checkNat 1232 = true := by
  apply check_of_normalize (Case.ofNat 1232)
  have he : (Case.ofNat 1232).normalize = Case.ofNat 208 := by decide
  rw [he]
  exact case0208
#print axioms case1232

theorem case2256 : checkNat 2256 = true := by
  apply check_of_normalize (Case.ofNat 2256)
  have he : (Case.ofNat 2256).normalize = Case.ofNat 208 := by decide
  rw [he]
  exact case0208
#print axioms case2256

theorem case3280 : checkNat 3280 = true := by
  apply check_of_normalize (Case.ofNat 3280)
  have he : (Case.ofNat 3280).normalize = Case.ofNat 208 := by decide
  rw [he]
  exact case0208
#print axioms case3280

theorem case0209 : checkNat 209 = true := by native_decide
#print axioms case0209

theorem case2257 : checkNat 2257 = true := by
  apply check_of_normalize (Case.ofNat 2257)
  have he : (Case.ofNat 2257).normalize = Case.ofNat 209 := by decide
  rw [he]
  exact case0209
#print axioms case2257

theorem case0210 : checkNat 210 = true := by native_decide
#print axioms case0210

theorem case1234 : checkNat 1234 = true := by
  apply check_of_normalize (Case.ofNat 1234)
  have he : (Case.ofNat 1234).normalize = Case.ofNat 210 := by decide
  rw [he]
  exact case0210
#print axioms case1234

theorem case0211 : checkNat 211 = true := by native_decide
#print axioms case0211

theorem case0212 : checkNat 212 = true := by native_decide
#print axioms case0212

theorem case1236 : checkNat 1236 = true := by
  apply check_of_normalize (Case.ofNat 1236)
  have he : (Case.ofNat 1236).normalize = Case.ofNat 212 := by decide
  rw [he]
  exact case0212
#print axioms case1236

theorem case2260 : checkNat 2260 = true := by
  apply check_of_normalize (Case.ofNat 2260)
  have he : (Case.ofNat 2260).normalize = Case.ofNat 212 := by decide
  rw [he]
  exact case0212
#print axioms case2260

theorem case3284 : checkNat 3284 = true := by
  apply check_of_normalize (Case.ofNat 3284)
  have he : (Case.ofNat 3284).normalize = Case.ofNat 212 := by decide
  rw [he]
  exact case0212
#print axioms case3284

theorem case0213 : checkNat 213 = true := by native_decide
#print axioms case0213

theorem case2261 : checkNat 2261 = true := by
  apply check_of_normalize (Case.ofNat 2261)
  have he : (Case.ofNat 2261).normalize = Case.ofNat 213 := by decide
  rw [he]
  exact case0213
#print axioms case2261

theorem case0214 : checkNat 214 = true := by native_decide
#print axioms case0214

theorem case1238 : checkNat 1238 = true := by
  apply check_of_normalize (Case.ofNat 1238)
  have he : (Case.ofNat 1238).normalize = Case.ofNat 214 := by decide
  rw [he]
  exact case0214
#print axioms case1238

theorem case0215 : checkNat 215 = true := by native_decide
#print axioms case0215

theorem case0216 : checkNat 216 = true := by native_decide
#print axioms case0216

theorem case1240 : checkNat 1240 = true := by
  apply check_of_normalize (Case.ofNat 1240)
  have he : (Case.ofNat 1240).normalize = Case.ofNat 216 := by decide
  rw [he]
  exact case0216
#print axioms case1240

theorem case2264 : checkNat 2264 = true := by
  apply check_of_normalize (Case.ofNat 2264)
  have he : (Case.ofNat 2264).normalize = Case.ofNat 216 := by decide
  rw [he]
  exact case0216
#print axioms case2264

theorem case3288 : checkNat 3288 = true := by
  apply check_of_normalize (Case.ofNat 3288)
  have he : (Case.ofNat 3288).normalize = Case.ofNat 216 := by decide
  rw [he]
  exact case0216
#print axioms case3288

theorem case0217 : checkNat 217 = true := by native_decide
#print axioms case0217

theorem case2265 : checkNat 2265 = true := by
  apply check_of_normalize (Case.ofNat 2265)
  have he : (Case.ofNat 2265).normalize = Case.ofNat 217 := by decide
  rw [he]
  exact case0217
#print axioms case2265

theorem case0218 : checkNat 218 = true := by native_decide
#print axioms case0218

theorem case1242 : checkNat 1242 = true := by
  apply check_of_normalize (Case.ofNat 1242)
  have he : (Case.ofNat 1242).normalize = Case.ofNat 218 := by decide
  rw [he]
  exact case0218
#print axioms case1242

theorem case0219 : checkNat 219 = true := by native_decide
#print axioms case0219

theorem case0220 : checkNat 220 = true := by native_decide
#print axioms case0220

theorem case1244 : checkNat 1244 = true := by
  apply check_of_normalize (Case.ofNat 1244)
  have he : (Case.ofNat 1244).normalize = Case.ofNat 220 := by decide
  rw [he]
  exact case0220
#print axioms case1244

theorem case2268 : checkNat 2268 = true := by
  apply check_of_normalize (Case.ofNat 2268)
  have he : (Case.ofNat 2268).normalize = Case.ofNat 220 := by decide
  rw [he]
  exact case0220
#print axioms case2268

theorem case3292 : checkNat 3292 = true := by
  apply check_of_normalize (Case.ofNat 3292)
  have he : (Case.ofNat 3292).normalize = Case.ofNat 220 := by decide
  rw [he]
  exact case0220
#print axioms case3292

theorem case0221 : checkNat 221 = true := by native_decide
#print axioms case0221

theorem case2269 : checkNat 2269 = true := by
  apply check_of_normalize (Case.ofNat 2269)
  have he : (Case.ofNat 2269).normalize = Case.ofNat 221 := by decide
  rw [he]
  exact case0221
#print axioms case2269

theorem case0222 : checkNat 222 = true := by native_decide
#print axioms case0222

theorem case1246 : checkNat 1246 = true := by
  apply check_of_normalize (Case.ofNat 1246)
  have he : (Case.ofNat 1246).normalize = Case.ofNat 222 := by decide
  rw [he]
  exact case0222
#print axioms case1246

theorem case0223 : checkNat 223 = true := by native_decide
#print axioms case0223

theorem accepted :
    checkNat 192 = true ∧
    checkNat 193 = true ∧
    checkNat 194 = true ∧
    checkNat 195 = true ∧
    checkNat 196 = true ∧
    checkNat 197 = true ∧
    checkNat 198 = true ∧
    checkNat 199 = true ∧
    checkNat 200 = true ∧
    checkNat 201 = true ∧
    checkNat 202 = true ∧
    checkNat 203 = true ∧
    checkNat 204 = true ∧
    checkNat 205 = true ∧
    checkNat 206 = true ∧
    checkNat 207 = true ∧
    checkNat 208 = true ∧
    checkNat 209 = true ∧
    checkNat 210 = true ∧
    checkNat 211 = true ∧
    checkNat 212 = true ∧
    checkNat 213 = true ∧
    checkNat 214 = true ∧
    checkNat 215 = true ∧
    checkNat 216 = true ∧
    checkNat 217 = true ∧
    checkNat 218 = true ∧
    checkNat 219 = true ∧
    checkNat 220 = true ∧
    checkNat 221 = true ∧
    checkNat 222 = true ∧
    checkNat 223 = true ∧
    checkNat 1216 = true ∧
    checkNat 1218 = true ∧
    checkNat 1220 = true ∧
    checkNat 1222 = true ∧
    checkNat 1224 = true ∧
    checkNat 1226 = true ∧
    checkNat 1228 = true ∧
    checkNat 1230 = true ∧
    checkNat 1232 = true ∧
    checkNat 1234 = true ∧
    checkNat 1236 = true ∧
    checkNat 1238 = true ∧
    checkNat 1240 = true ∧
    checkNat 1242 = true ∧
    checkNat 1244 = true ∧
    checkNat 1246 = true ∧
    checkNat 2240 = true ∧
    checkNat 2241 = true ∧
    checkNat 2244 = true ∧
    checkNat 2245 = true ∧
    checkNat 2248 = true ∧
    checkNat 2249 = true ∧
    checkNat 2252 = true ∧
    checkNat 2253 = true ∧
    checkNat 2256 = true ∧
    checkNat 2257 = true ∧
    checkNat 2260 = true ∧
    checkNat 2261 = true ∧
    checkNat 2264 = true ∧
    checkNat 2265 = true ∧
    checkNat 2268 = true ∧
    checkNat 2269 = true ∧
    checkNat 3264 = true ∧
    checkNat 3268 = true ∧
    checkNat 3272 = true ∧
    checkNat 3276 = true ∧
    checkNat 3280 = true ∧
    checkNat 3284 = true ∧
    checkNat 3288 = true ∧
    checkNat 3292 = true := by
  exact ⟨case0192, case0193, case0194, case0195, case0196, case0197, case0198, case0199, case0200, case0201, case0202, case0203, case0204, case0205, case0206, case0207, case0208, case0209, case0210, case0211, case0212, case0213, case0214, case0215, case0216, case0217, case0218, case0219, case0220, case0221, case0222, case0223, case1216, case1218, case1220, case1222, case1224, case1226, case1228, case1230, case1232, case1234, case1236, case1238, case1240, case1242, case1244, case1246, case2240, case2241, case2244, case2245, case2248, case2249, case2252, case2253, case2256, case2257, case2260, case2261, case2264, case2265, case2268, case2269, case3264, case3268, case3272, case3276, case3280, case3284, case3288, case3292⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0192
