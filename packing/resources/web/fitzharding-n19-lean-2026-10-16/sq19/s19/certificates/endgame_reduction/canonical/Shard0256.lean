import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0256
open Sq19.Endgame.Reduction

theorem case0256 : checkNat 256 = true := by native_decide
#print axioms case0256

theorem case1280 : checkNat 1280 = true := by
  apply check_of_normalize (Case.ofNat 1280)
  have he : (Case.ofNat 1280).normalize = Case.ofNat 256 := by decide
  rw [he]
  exact case0256
#print axioms case1280

theorem case2304 : checkNat 2304 = true := by
  apply check_of_normalize (Case.ofNat 2304)
  have he : (Case.ofNat 2304).normalize = Case.ofNat 256 := by decide
  rw [he]
  exact case0256
#print axioms case2304

theorem case3328 : checkNat 3328 = true := by
  apply check_of_normalize (Case.ofNat 3328)
  have he : (Case.ofNat 3328).normalize = Case.ofNat 256 := by decide
  rw [he]
  exact case0256
#print axioms case3328

theorem case0257 : checkNat 257 = true := by native_decide
#print axioms case0257

theorem case2305 : checkNat 2305 = true := by
  apply check_of_normalize (Case.ofNat 2305)
  have he : (Case.ofNat 2305).normalize = Case.ofNat 257 := by decide
  rw [he]
  exact case0257
#print axioms case2305

theorem case0258 : checkNat 258 = true := by native_decide
#print axioms case0258

theorem case1282 : checkNat 1282 = true := by
  apply check_of_normalize (Case.ofNat 1282)
  have he : (Case.ofNat 1282).normalize = Case.ofNat 258 := by decide
  rw [he]
  exact case0258
#print axioms case1282

theorem case0259 : checkNat 259 = true := by native_decide
#print axioms case0259

theorem case0260 : checkNat 260 = true := by native_decide
#print axioms case0260

theorem case1284 : checkNat 1284 = true := by
  apply check_of_normalize (Case.ofNat 1284)
  have he : (Case.ofNat 1284).normalize = Case.ofNat 260 := by decide
  rw [he]
  exact case0260
#print axioms case1284

theorem case2308 : checkNat 2308 = true := by
  apply check_of_normalize (Case.ofNat 2308)
  have he : (Case.ofNat 2308).normalize = Case.ofNat 260 := by decide
  rw [he]
  exact case0260
#print axioms case2308

theorem case3332 : checkNat 3332 = true := by
  apply check_of_normalize (Case.ofNat 3332)
  have he : (Case.ofNat 3332).normalize = Case.ofNat 260 := by decide
  rw [he]
  exact case0260
#print axioms case3332

theorem case0261 : checkNat 261 = true := by native_decide
#print axioms case0261

theorem case2309 : checkNat 2309 = true := by
  apply check_of_normalize (Case.ofNat 2309)
  have he : (Case.ofNat 2309).normalize = Case.ofNat 261 := by decide
  rw [he]
  exact case0261
#print axioms case2309

theorem case0262 : checkNat 262 = true := by native_decide
#print axioms case0262

theorem case1286 : checkNat 1286 = true := by
  apply check_of_normalize (Case.ofNat 1286)
  have he : (Case.ofNat 1286).normalize = Case.ofNat 262 := by decide
  rw [he]
  exact case0262
#print axioms case1286

theorem case0263 : checkNat 263 = true := by native_decide
#print axioms case0263

theorem case0264 : checkNat 264 = true := by native_decide
#print axioms case0264

theorem case1288 : checkNat 1288 = true := by
  apply check_of_normalize (Case.ofNat 1288)
  have he : (Case.ofNat 1288).normalize = Case.ofNat 264 := by decide
  rw [he]
  exact case0264
#print axioms case1288

theorem case2312 : checkNat 2312 = true := by
  apply check_of_normalize (Case.ofNat 2312)
  have he : (Case.ofNat 2312).normalize = Case.ofNat 264 := by decide
  rw [he]
  exact case0264
#print axioms case2312

theorem case3336 : checkNat 3336 = true := by
  apply check_of_normalize (Case.ofNat 3336)
  have he : (Case.ofNat 3336).normalize = Case.ofNat 264 := by decide
  rw [he]
  exact case0264
#print axioms case3336

theorem case0265 : checkNat 265 = true := by native_decide
#print axioms case0265

theorem case2313 : checkNat 2313 = true := by
  apply check_of_normalize (Case.ofNat 2313)
  have he : (Case.ofNat 2313).normalize = Case.ofNat 265 := by decide
  rw [he]
  exact case0265
#print axioms case2313

theorem case0266 : checkNat 266 = true := by native_decide
#print axioms case0266

theorem case1290 : checkNat 1290 = true := by
  apply check_of_normalize (Case.ofNat 1290)
  have he : (Case.ofNat 1290).normalize = Case.ofNat 266 := by decide
  rw [he]
  exact case0266
#print axioms case1290

theorem case0267 : checkNat 267 = true := by native_decide
#print axioms case0267

theorem case0268 : checkNat 268 = true := by native_decide
#print axioms case0268

theorem case1292 : checkNat 1292 = true := by
  apply check_of_normalize (Case.ofNat 1292)
  have he : (Case.ofNat 1292).normalize = Case.ofNat 268 := by decide
  rw [he]
  exact case0268
#print axioms case1292

theorem case2316 : checkNat 2316 = true := by
  apply check_of_normalize (Case.ofNat 2316)
  have he : (Case.ofNat 2316).normalize = Case.ofNat 268 := by decide
  rw [he]
  exact case0268
#print axioms case2316

theorem case3340 : checkNat 3340 = true := by
  apply check_of_normalize (Case.ofNat 3340)
  have he : (Case.ofNat 3340).normalize = Case.ofNat 268 := by decide
  rw [he]
  exact case0268
#print axioms case3340

theorem case0269 : checkNat 269 = true := by native_decide
#print axioms case0269

theorem case2317 : checkNat 2317 = true := by
  apply check_of_normalize (Case.ofNat 2317)
  have he : (Case.ofNat 2317).normalize = Case.ofNat 269 := by decide
  rw [he]
  exact case0269
#print axioms case2317

theorem case0270 : checkNat 270 = true := by native_decide
#print axioms case0270

theorem case1294 : checkNat 1294 = true := by
  apply check_of_normalize (Case.ofNat 1294)
  have he : (Case.ofNat 1294).normalize = Case.ofNat 270 := by decide
  rw [he]
  exact case0270
#print axioms case1294

theorem case0271 : checkNat 271 = true := by native_decide
#print axioms case0271

theorem case0272 : checkNat 272 = true := by native_decide
#print axioms case0272

theorem case1296 : checkNat 1296 = true := by
  apply check_of_normalize (Case.ofNat 1296)
  have he : (Case.ofNat 1296).normalize = Case.ofNat 272 := by decide
  rw [he]
  exact case0272
#print axioms case1296

theorem case2320 : checkNat 2320 = true := by
  apply check_of_normalize (Case.ofNat 2320)
  have he : (Case.ofNat 2320).normalize = Case.ofNat 272 := by decide
  rw [he]
  exact case0272
#print axioms case2320

theorem case3344 : checkNat 3344 = true := by
  apply check_of_normalize (Case.ofNat 3344)
  have he : (Case.ofNat 3344).normalize = Case.ofNat 272 := by decide
  rw [he]
  exact case0272
#print axioms case3344

theorem case0273 : checkNat 273 = true := by native_decide
#print axioms case0273

theorem case2321 : checkNat 2321 = true := by
  apply check_of_normalize (Case.ofNat 2321)
  have he : (Case.ofNat 2321).normalize = Case.ofNat 273 := by decide
  rw [he]
  exact case0273
#print axioms case2321

theorem case0274 : checkNat 274 = true := by native_decide
#print axioms case0274

theorem case1298 : checkNat 1298 = true := by
  apply check_of_normalize (Case.ofNat 1298)
  have he : (Case.ofNat 1298).normalize = Case.ofNat 274 := by decide
  rw [he]
  exact case0274
#print axioms case1298

theorem case0275 : checkNat 275 = true := by native_decide
#print axioms case0275

theorem case0276 : checkNat 276 = true := by native_decide
#print axioms case0276

theorem case1300 : checkNat 1300 = true := by
  apply check_of_normalize (Case.ofNat 1300)
  have he : (Case.ofNat 1300).normalize = Case.ofNat 276 := by decide
  rw [he]
  exact case0276
#print axioms case1300

theorem case2324 : checkNat 2324 = true := by
  apply check_of_normalize (Case.ofNat 2324)
  have he : (Case.ofNat 2324).normalize = Case.ofNat 276 := by decide
  rw [he]
  exact case0276
#print axioms case2324

theorem case3348 : checkNat 3348 = true := by
  apply check_of_normalize (Case.ofNat 3348)
  have he : (Case.ofNat 3348).normalize = Case.ofNat 276 := by decide
  rw [he]
  exact case0276
#print axioms case3348

theorem case0277 : checkNat 277 = true := by native_decide
#print axioms case0277

theorem case2325 : checkNat 2325 = true := by
  apply check_of_normalize (Case.ofNat 2325)
  have he : (Case.ofNat 2325).normalize = Case.ofNat 277 := by decide
  rw [he]
  exact case0277
#print axioms case2325

theorem case0278 : checkNat 278 = true := by native_decide
#print axioms case0278

theorem case1302 : checkNat 1302 = true := by
  apply check_of_normalize (Case.ofNat 1302)
  have he : (Case.ofNat 1302).normalize = Case.ofNat 278 := by decide
  rw [he]
  exact case0278
#print axioms case1302

theorem case0279 : checkNat 279 = true := by native_decide
#print axioms case0279

theorem case0280 : checkNat 280 = true := by native_decide
#print axioms case0280

theorem case1304 : checkNat 1304 = true := by
  apply check_of_normalize (Case.ofNat 1304)
  have he : (Case.ofNat 1304).normalize = Case.ofNat 280 := by decide
  rw [he]
  exact case0280
#print axioms case1304

theorem case2328 : checkNat 2328 = true := by
  apply check_of_normalize (Case.ofNat 2328)
  have he : (Case.ofNat 2328).normalize = Case.ofNat 280 := by decide
  rw [he]
  exact case0280
#print axioms case2328

theorem case3352 : checkNat 3352 = true := by
  apply check_of_normalize (Case.ofNat 3352)
  have he : (Case.ofNat 3352).normalize = Case.ofNat 280 := by decide
  rw [he]
  exact case0280
#print axioms case3352

theorem case0281 : checkNat 281 = true := by native_decide
#print axioms case0281

theorem case2329 : checkNat 2329 = true := by
  apply check_of_normalize (Case.ofNat 2329)
  have he : (Case.ofNat 2329).normalize = Case.ofNat 281 := by decide
  rw [he]
  exact case0281
#print axioms case2329

theorem case0282 : checkNat 282 = true := by native_decide
#print axioms case0282

theorem case1306 : checkNat 1306 = true := by
  apply check_of_normalize (Case.ofNat 1306)
  have he : (Case.ofNat 1306).normalize = Case.ofNat 282 := by decide
  rw [he]
  exact case0282
#print axioms case1306

theorem case0283 : checkNat 283 = true := by native_decide
#print axioms case0283

theorem case0284 : checkNat 284 = true := by native_decide
#print axioms case0284

theorem case1308 : checkNat 1308 = true := by
  apply check_of_normalize (Case.ofNat 1308)
  have he : (Case.ofNat 1308).normalize = Case.ofNat 284 := by decide
  rw [he]
  exact case0284
#print axioms case1308

theorem case2332 : checkNat 2332 = true := by
  apply check_of_normalize (Case.ofNat 2332)
  have he : (Case.ofNat 2332).normalize = Case.ofNat 284 := by decide
  rw [he]
  exact case0284
#print axioms case2332

theorem case3356 : checkNat 3356 = true := by
  apply check_of_normalize (Case.ofNat 3356)
  have he : (Case.ofNat 3356).normalize = Case.ofNat 284 := by decide
  rw [he]
  exact case0284
#print axioms case3356

theorem case0285 : checkNat 285 = true := by native_decide
#print axioms case0285

theorem case2333 : checkNat 2333 = true := by
  apply check_of_normalize (Case.ofNat 2333)
  have he : (Case.ofNat 2333).normalize = Case.ofNat 285 := by decide
  rw [he]
  exact case0285
#print axioms case2333

theorem case0286 : checkNat 286 = true := by native_decide
#print axioms case0286

theorem case1310 : checkNat 1310 = true := by
  apply check_of_normalize (Case.ofNat 1310)
  have he : (Case.ofNat 1310).normalize = Case.ofNat 286 := by decide
  rw [he]
  exact case0286
#print axioms case1310

theorem case0287 : checkNat 287 = true := by native_decide
#print axioms case0287

theorem accepted :
    checkNat 256 = true ∧
    checkNat 257 = true ∧
    checkNat 258 = true ∧
    checkNat 259 = true ∧
    checkNat 260 = true ∧
    checkNat 261 = true ∧
    checkNat 262 = true ∧
    checkNat 263 = true ∧
    checkNat 264 = true ∧
    checkNat 265 = true ∧
    checkNat 266 = true ∧
    checkNat 267 = true ∧
    checkNat 268 = true ∧
    checkNat 269 = true ∧
    checkNat 270 = true ∧
    checkNat 271 = true ∧
    checkNat 272 = true ∧
    checkNat 273 = true ∧
    checkNat 274 = true ∧
    checkNat 275 = true ∧
    checkNat 276 = true ∧
    checkNat 277 = true ∧
    checkNat 278 = true ∧
    checkNat 279 = true ∧
    checkNat 280 = true ∧
    checkNat 281 = true ∧
    checkNat 282 = true ∧
    checkNat 283 = true ∧
    checkNat 284 = true ∧
    checkNat 285 = true ∧
    checkNat 286 = true ∧
    checkNat 287 = true ∧
    checkNat 1280 = true ∧
    checkNat 1282 = true ∧
    checkNat 1284 = true ∧
    checkNat 1286 = true ∧
    checkNat 1288 = true ∧
    checkNat 1290 = true ∧
    checkNat 1292 = true ∧
    checkNat 1294 = true ∧
    checkNat 1296 = true ∧
    checkNat 1298 = true ∧
    checkNat 1300 = true ∧
    checkNat 1302 = true ∧
    checkNat 1304 = true ∧
    checkNat 1306 = true ∧
    checkNat 1308 = true ∧
    checkNat 1310 = true ∧
    checkNat 2304 = true ∧
    checkNat 2305 = true ∧
    checkNat 2308 = true ∧
    checkNat 2309 = true ∧
    checkNat 2312 = true ∧
    checkNat 2313 = true ∧
    checkNat 2316 = true ∧
    checkNat 2317 = true ∧
    checkNat 2320 = true ∧
    checkNat 2321 = true ∧
    checkNat 2324 = true ∧
    checkNat 2325 = true ∧
    checkNat 2328 = true ∧
    checkNat 2329 = true ∧
    checkNat 2332 = true ∧
    checkNat 2333 = true ∧
    checkNat 3328 = true ∧
    checkNat 3332 = true ∧
    checkNat 3336 = true ∧
    checkNat 3340 = true ∧
    checkNat 3344 = true ∧
    checkNat 3348 = true ∧
    checkNat 3352 = true ∧
    checkNat 3356 = true := by
  exact ⟨case0256, case0257, case0258, case0259, case0260, case0261, case0262, case0263, case0264, case0265, case0266, case0267, case0268, case0269, case0270, case0271, case0272, case0273, case0274, case0275, case0276, case0277, case0278, case0279, case0280, case0281, case0282, case0283, case0284, case0285, case0286, case0287, case1280, case1282, case1284, case1286, case1288, case1290, case1292, case1294, case1296, case1298, case1300, case1302, case1304, case1306, case1308, case1310, case2304, case2305, case2308, case2309, case2312, case2313, case2316, case2317, case2320, case2321, case2324, case2325, case2328, case2329, case2332, case2333, case3328, case3332, case3336, case3340, case3344, case3348, case3352, case3356⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0256
