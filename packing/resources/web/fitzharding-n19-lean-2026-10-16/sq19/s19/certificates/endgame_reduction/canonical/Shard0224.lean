import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0224
open Sq19.Endgame.Reduction

theorem case0224 : checkNat 224 = true := by native_decide
#print axioms case0224

theorem case1248 : checkNat 1248 = true := by
  apply check_of_normalize (Case.ofNat 1248)
  have he : (Case.ofNat 1248).normalize = Case.ofNat 224 := by decide
  rw [he]
  exact case0224
#print axioms case1248

theorem case2272 : checkNat 2272 = true := by
  apply check_of_normalize (Case.ofNat 2272)
  have he : (Case.ofNat 2272).normalize = Case.ofNat 224 := by decide
  rw [he]
  exact case0224
#print axioms case2272

theorem case3296 : checkNat 3296 = true := by
  apply check_of_normalize (Case.ofNat 3296)
  have he : (Case.ofNat 3296).normalize = Case.ofNat 224 := by decide
  rw [he]
  exact case0224
#print axioms case3296

theorem case0225 : checkNat 225 = true := by native_decide
#print axioms case0225

theorem case2273 : checkNat 2273 = true := by
  apply check_of_normalize (Case.ofNat 2273)
  have he : (Case.ofNat 2273).normalize = Case.ofNat 225 := by decide
  rw [he]
  exact case0225
#print axioms case2273

theorem case0226 : checkNat 226 = true := by native_decide
#print axioms case0226

theorem case1250 : checkNat 1250 = true := by
  apply check_of_normalize (Case.ofNat 1250)
  have he : (Case.ofNat 1250).normalize = Case.ofNat 226 := by decide
  rw [he]
  exact case0226
#print axioms case1250

theorem case0227 : checkNat 227 = true := by native_decide
#print axioms case0227

theorem case0228 : checkNat 228 = true := by native_decide
#print axioms case0228

theorem case1252 : checkNat 1252 = true := by
  apply check_of_normalize (Case.ofNat 1252)
  have he : (Case.ofNat 1252).normalize = Case.ofNat 228 := by decide
  rw [he]
  exact case0228
#print axioms case1252

theorem case2276 : checkNat 2276 = true := by
  apply check_of_normalize (Case.ofNat 2276)
  have he : (Case.ofNat 2276).normalize = Case.ofNat 228 := by decide
  rw [he]
  exact case0228
#print axioms case2276

theorem case3300 : checkNat 3300 = true := by
  apply check_of_normalize (Case.ofNat 3300)
  have he : (Case.ofNat 3300).normalize = Case.ofNat 228 := by decide
  rw [he]
  exact case0228
#print axioms case3300

theorem case0229 : checkNat 229 = true := by native_decide
#print axioms case0229

theorem case2277 : checkNat 2277 = true := by
  apply check_of_normalize (Case.ofNat 2277)
  have he : (Case.ofNat 2277).normalize = Case.ofNat 229 := by decide
  rw [he]
  exact case0229
#print axioms case2277

theorem case0230 : checkNat 230 = true := by native_decide
#print axioms case0230

theorem case1254 : checkNat 1254 = true := by
  apply check_of_normalize (Case.ofNat 1254)
  have he : (Case.ofNat 1254).normalize = Case.ofNat 230 := by decide
  rw [he]
  exact case0230
#print axioms case1254

theorem case0231 : checkNat 231 = true := by native_decide
#print axioms case0231

theorem case0232 : checkNat 232 = true := by native_decide
#print axioms case0232

theorem case1256 : checkNat 1256 = true := by
  apply check_of_normalize (Case.ofNat 1256)
  have he : (Case.ofNat 1256).normalize = Case.ofNat 232 := by decide
  rw [he]
  exact case0232
#print axioms case1256

theorem case2280 : checkNat 2280 = true := by
  apply check_of_normalize (Case.ofNat 2280)
  have he : (Case.ofNat 2280).normalize = Case.ofNat 232 := by decide
  rw [he]
  exact case0232
#print axioms case2280

theorem case3304 : checkNat 3304 = true := by
  apply check_of_normalize (Case.ofNat 3304)
  have he : (Case.ofNat 3304).normalize = Case.ofNat 232 := by decide
  rw [he]
  exact case0232
#print axioms case3304

theorem case0233 : checkNat 233 = true := by native_decide
#print axioms case0233

theorem case2281 : checkNat 2281 = true := by
  apply check_of_normalize (Case.ofNat 2281)
  have he : (Case.ofNat 2281).normalize = Case.ofNat 233 := by decide
  rw [he]
  exact case0233
#print axioms case2281

theorem case0234 : checkNat 234 = true := by native_decide
#print axioms case0234

theorem case1258 : checkNat 1258 = true := by
  apply check_of_normalize (Case.ofNat 1258)
  have he : (Case.ofNat 1258).normalize = Case.ofNat 234 := by decide
  rw [he]
  exact case0234
#print axioms case1258

theorem case0235 : checkNat 235 = true := by native_decide
#print axioms case0235

theorem case0236 : checkNat 236 = true := by native_decide
#print axioms case0236

theorem case1260 : checkNat 1260 = true := by
  apply check_of_normalize (Case.ofNat 1260)
  have he : (Case.ofNat 1260).normalize = Case.ofNat 236 := by decide
  rw [he]
  exact case0236
#print axioms case1260

theorem case2284 : checkNat 2284 = true := by
  apply check_of_normalize (Case.ofNat 2284)
  have he : (Case.ofNat 2284).normalize = Case.ofNat 236 := by decide
  rw [he]
  exact case0236
#print axioms case2284

theorem case3308 : checkNat 3308 = true := by
  apply check_of_normalize (Case.ofNat 3308)
  have he : (Case.ofNat 3308).normalize = Case.ofNat 236 := by decide
  rw [he]
  exact case0236
#print axioms case3308

theorem case0237 : checkNat 237 = true := by native_decide
#print axioms case0237

theorem case2285 : checkNat 2285 = true := by
  apply check_of_normalize (Case.ofNat 2285)
  have he : (Case.ofNat 2285).normalize = Case.ofNat 237 := by decide
  rw [he]
  exact case0237
#print axioms case2285

theorem case0238 : checkNat 238 = true := by native_decide
#print axioms case0238

theorem case1262 : checkNat 1262 = true := by
  apply check_of_normalize (Case.ofNat 1262)
  have he : (Case.ofNat 1262).normalize = Case.ofNat 238 := by decide
  rw [he]
  exact case0238
#print axioms case1262

theorem case0239 : checkNat 239 = true := by native_decide
#print axioms case0239

theorem case0240 : checkNat 240 = true := by native_decide
#print axioms case0240

theorem case1264 : checkNat 1264 = true := by
  apply check_of_normalize (Case.ofNat 1264)
  have he : (Case.ofNat 1264).normalize = Case.ofNat 240 := by decide
  rw [he]
  exact case0240
#print axioms case1264

theorem case2288 : checkNat 2288 = true := by
  apply check_of_normalize (Case.ofNat 2288)
  have he : (Case.ofNat 2288).normalize = Case.ofNat 240 := by decide
  rw [he]
  exact case0240
#print axioms case2288

theorem case3312 : checkNat 3312 = true := by
  apply check_of_normalize (Case.ofNat 3312)
  have he : (Case.ofNat 3312).normalize = Case.ofNat 240 := by decide
  rw [he]
  exact case0240
#print axioms case3312

theorem case0241 : checkNat 241 = true := by native_decide
#print axioms case0241

theorem case2289 : checkNat 2289 = true := by
  apply check_of_normalize (Case.ofNat 2289)
  have he : (Case.ofNat 2289).normalize = Case.ofNat 241 := by decide
  rw [he]
  exact case0241
#print axioms case2289

theorem case0242 : checkNat 242 = true := by native_decide
#print axioms case0242

theorem case1266 : checkNat 1266 = true := by
  apply check_of_normalize (Case.ofNat 1266)
  have he : (Case.ofNat 1266).normalize = Case.ofNat 242 := by decide
  rw [he]
  exact case0242
#print axioms case1266

theorem case0243 : checkNat 243 = true := by native_decide
#print axioms case0243

theorem case0244 : checkNat 244 = true := by native_decide
#print axioms case0244

theorem case1268 : checkNat 1268 = true := by
  apply check_of_normalize (Case.ofNat 1268)
  have he : (Case.ofNat 1268).normalize = Case.ofNat 244 := by decide
  rw [he]
  exact case0244
#print axioms case1268

theorem case2292 : checkNat 2292 = true := by
  apply check_of_normalize (Case.ofNat 2292)
  have he : (Case.ofNat 2292).normalize = Case.ofNat 244 := by decide
  rw [he]
  exact case0244
#print axioms case2292

theorem case3316 : checkNat 3316 = true := by
  apply check_of_normalize (Case.ofNat 3316)
  have he : (Case.ofNat 3316).normalize = Case.ofNat 244 := by decide
  rw [he]
  exact case0244
#print axioms case3316

theorem case0245 : checkNat 245 = true := by native_decide
#print axioms case0245

theorem case2293 : checkNat 2293 = true := by
  apply check_of_normalize (Case.ofNat 2293)
  have he : (Case.ofNat 2293).normalize = Case.ofNat 245 := by decide
  rw [he]
  exact case0245
#print axioms case2293

theorem case0246 : checkNat 246 = true := by native_decide
#print axioms case0246

theorem case1270 : checkNat 1270 = true := by
  apply check_of_normalize (Case.ofNat 1270)
  have he : (Case.ofNat 1270).normalize = Case.ofNat 246 := by decide
  rw [he]
  exact case0246
#print axioms case1270

theorem case0247 : checkNat 247 = true := by native_decide
#print axioms case0247

theorem case0248 : checkNat 248 = true := by native_decide
#print axioms case0248

theorem case1272 : checkNat 1272 = true := by
  apply check_of_normalize (Case.ofNat 1272)
  have he : (Case.ofNat 1272).normalize = Case.ofNat 248 := by decide
  rw [he]
  exact case0248
#print axioms case1272

theorem case2296 : checkNat 2296 = true := by
  apply check_of_normalize (Case.ofNat 2296)
  have he : (Case.ofNat 2296).normalize = Case.ofNat 248 := by decide
  rw [he]
  exact case0248
#print axioms case2296

theorem case3320 : checkNat 3320 = true := by
  apply check_of_normalize (Case.ofNat 3320)
  have he : (Case.ofNat 3320).normalize = Case.ofNat 248 := by decide
  rw [he]
  exact case0248
#print axioms case3320

theorem case0249 : checkNat 249 = true := by native_decide
#print axioms case0249

theorem case2297 : checkNat 2297 = true := by
  apply check_of_normalize (Case.ofNat 2297)
  have he : (Case.ofNat 2297).normalize = Case.ofNat 249 := by decide
  rw [he]
  exact case0249
#print axioms case2297

theorem case0250 : checkNat 250 = true := by native_decide
#print axioms case0250

theorem case1274 : checkNat 1274 = true := by
  apply check_of_normalize (Case.ofNat 1274)
  have he : (Case.ofNat 1274).normalize = Case.ofNat 250 := by decide
  rw [he]
  exact case0250
#print axioms case1274

theorem case0251 : checkNat 251 = true := by native_decide
#print axioms case0251

theorem case0252 : checkNat 252 = true := by native_decide
#print axioms case0252

theorem case1276 : checkNat 1276 = true := by
  apply check_of_normalize (Case.ofNat 1276)
  have he : (Case.ofNat 1276).normalize = Case.ofNat 252 := by decide
  rw [he]
  exact case0252
#print axioms case1276

theorem case2300 : checkNat 2300 = true := by
  apply check_of_normalize (Case.ofNat 2300)
  have he : (Case.ofNat 2300).normalize = Case.ofNat 252 := by decide
  rw [he]
  exact case0252
#print axioms case2300

theorem case3324 : checkNat 3324 = true := by
  apply check_of_normalize (Case.ofNat 3324)
  have he : (Case.ofNat 3324).normalize = Case.ofNat 252 := by decide
  rw [he]
  exact case0252
#print axioms case3324

theorem case0253 : checkNat 253 = true := by native_decide
#print axioms case0253

theorem case2301 : checkNat 2301 = true := by
  apply check_of_normalize (Case.ofNat 2301)
  have he : (Case.ofNat 2301).normalize = Case.ofNat 253 := by decide
  rw [he]
  exact case0253
#print axioms case2301

theorem case0254 : checkNat 254 = true := by native_decide
#print axioms case0254

theorem case1278 : checkNat 1278 = true := by
  apply check_of_normalize (Case.ofNat 1278)
  have he : (Case.ofNat 1278).normalize = Case.ofNat 254 := by decide
  rw [he]
  exact case0254
#print axioms case1278

theorem case0255 : checkNat 255 = true := by native_decide
#print axioms case0255

theorem accepted :
    checkNat 224 = true ∧
    checkNat 225 = true ∧
    checkNat 226 = true ∧
    checkNat 227 = true ∧
    checkNat 228 = true ∧
    checkNat 229 = true ∧
    checkNat 230 = true ∧
    checkNat 231 = true ∧
    checkNat 232 = true ∧
    checkNat 233 = true ∧
    checkNat 234 = true ∧
    checkNat 235 = true ∧
    checkNat 236 = true ∧
    checkNat 237 = true ∧
    checkNat 238 = true ∧
    checkNat 239 = true ∧
    checkNat 240 = true ∧
    checkNat 241 = true ∧
    checkNat 242 = true ∧
    checkNat 243 = true ∧
    checkNat 244 = true ∧
    checkNat 245 = true ∧
    checkNat 246 = true ∧
    checkNat 247 = true ∧
    checkNat 248 = true ∧
    checkNat 249 = true ∧
    checkNat 250 = true ∧
    checkNat 251 = true ∧
    checkNat 252 = true ∧
    checkNat 253 = true ∧
    checkNat 254 = true ∧
    checkNat 255 = true ∧
    checkNat 1248 = true ∧
    checkNat 1250 = true ∧
    checkNat 1252 = true ∧
    checkNat 1254 = true ∧
    checkNat 1256 = true ∧
    checkNat 1258 = true ∧
    checkNat 1260 = true ∧
    checkNat 1262 = true ∧
    checkNat 1264 = true ∧
    checkNat 1266 = true ∧
    checkNat 1268 = true ∧
    checkNat 1270 = true ∧
    checkNat 1272 = true ∧
    checkNat 1274 = true ∧
    checkNat 1276 = true ∧
    checkNat 1278 = true ∧
    checkNat 2272 = true ∧
    checkNat 2273 = true ∧
    checkNat 2276 = true ∧
    checkNat 2277 = true ∧
    checkNat 2280 = true ∧
    checkNat 2281 = true ∧
    checkNat 2284 = true ∧
    checkNat 2285 = true ∧
    checkNat 2288 = true ∧
    checkNat 2289 = true ∧
    checkNat 2292 = true ∧
    checkNat 2293 = true ∧
    checkNat 2296 = true ∧
    checkNat 2297 = true ∧
    checkNat 2300 = true ∧
    checkNat 2301 = true ∧
    checkNat 3296 = true ∧
    checkNat 3300 = true ∧
    checkNat 3304 = true ∧
    checkNat 3308 = true ∧
    checkNat 3312 = true ∧
    checkNat 3316 = true ∧
    checkNat 3320 = true ∧
    checkNat 3324 = true := by
  exact ⟨case0224, case0225, case0226, case0227, case0228, case0229, case0230, case0231, case0232, case0233, case0234, case0235, case0236, case0237, case0238, case0239, case0240, case0241, case0242, case0243, case0244, case0245, case0246, case0247, case0248, case0249, case0250, case0251, case0252, case0253, case0254, case0255, case1248, case1250, case1252, case1254, case1256, case1258, case1260, case1262, case1264, case1266, case1268, case1270, case1272, case1274, case1276, case1278, case2272, case2273, case2276, case2277, case2280, case2281, case2284, case2285, case2288, case2289, case2292, case2293, case2296, case2297, case2300, case2301, case3296, case3300, case3304, case3308, case3312, case3316, case3320, case3324⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0224
