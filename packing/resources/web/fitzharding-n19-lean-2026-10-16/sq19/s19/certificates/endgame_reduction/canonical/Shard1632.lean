import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1632
open Sq19.Endgame.Reduction

theorem case2242 : checkNat 2242 = true := by native_decide
#print axioms case2242

theorem case3266 : checkNat 3266 = true := by
  apply check_of_normalize (Case.ofNat 3266)
  have he : (Case.ofNat 3266).normalize = Case.ofNat 2242 := by decide
  rw [he]
  exact case2242
#print axioms case3266

theorem case2243 : checkNat 2243 = true := by native_decide
#print axioms case2243

theorem case2246 : checkNat 2246 = true := by native_decide
#print axioms case2246

theorem case3270 : checkNat 3270 = true := by
  apply check_of_normalize (Case.ofNat 3270)
  have he : (Case.ofNat 3270).normalize = Case.ofNat 2246 := by decide
  rw [he]
  exact case2246
#print axioms case3270

theorem case2247 : checkNat 2247 = true := by native_decide
#print axioms case2247

theorem case2250 : checkNat 2250 = true := by native_decide
#print axioms case2250

theorem case3274 : checkNat 3274 = true := by
  apply check_of_normalize (Case.ofNat 3274)
  have he : (Case.ofNat 3274).normalize = Case.ofNat 2250 := by decide
  rw [he]
  exact case2250
#print axioms case3274

theorem case2251 : checkNat 2251 = true := by native_decide
#print axioms case2251

theorem case2254 : checkNat 2254 = true := by native_decide
#print axioms case2254

theorem case3278 : checkNat 3278 = true := by
  apply check_of_normalize (Case.ofNat 3278)
  have he : (Case.ofNat 3278).normalize = Case.ofNat 2254 := by decide
  rw [he]
  exact case2254
#print axioms case3278

theorem case2255 : checkNat 2255 = true := by native_decide
#print axioms case2255

theorem case2258 : checkNat 2258 = true := by native_decide
#print axioms case2258

theorem case3282 : checkNat 3282 = true := by
  apply check_of_normalize (Case.ofNat 3282)
  have he : (Case.ofNat 3282).normalize = Case.ofNat 2258 := by decide
  rw [he]
  exact case2258
#print axioms case3282

theorem case2259 : checkNat 2259 = true := by native_decide
#print axioms case2259

theorem case2262 : checkNat 2262 = true := by native_decide
#print axioms case2262

theorem case3286 : checkNat 3286 = true := by
  apply check_of_normalize (Case.ofNat 3286)
  have he : (Case.ofNat 3286).normalize = Case.ofNat 2262 := by decide
  rw [he]
  exact case2262
#print axioms case3286

theorem case2263 : checkNat 2263 = true := by native_decide
#print axioms case2263

theorem case2266 : checkNat 2266 = true := by native_decide
#print axioms case2266

theorem case3290 : checkNat 3290 = true := by
  apply check_of_normalize (Case.ofNat 3290)
  have he : (Case.ofNat 3290).normalize = Case.ofNat 2266 := by decide
  rw [he]
  exact case2266
#print axioms case3290

theorem case2267 : checkNat 2267 = true := by native_decide
#print axioms case2267

theorem case2270 : checkNat 2270 = true := by native_decide
#print axioms case2270

theorem case3294 : checkNat 3294 = true := by
  apply check_of_normalize (Case.ofNat 3294)
  have he : (Case.ofNat 3294).normalize = Case.ofNat 2270 := by decide
  rw [he]
  exact case2270
#print axioms case3294

theorem case2271 : checkNat 2271 = true := by native_decide
#print axioms case2271

theorem case2274 : checkNat 2274 = true := by native_decide
#print axioms case2274

theorem case3298 : checkNat 3298 = true := by
  apply check_of_normalize (Case.ofNat 3298)
  have he : (Case.ofNat 3298).normalize = Case.ofNat 2274 := by decide
  rw [he]
  exact case2274
#print axioms case3298

theorem case2275 : checkNat 2275 = true := by native_decide
#print axioms case2275

theorem case2278 : checkNat 2278 = true := by native_decide
#print axioms case2278

theorem case3302 : checkNat 3302 = true := by
  apply check_of_normalize (Case.ofNat 3302)
  have he : (Case.ofNat 3302).normalize = Case.ofNat 2278 := by decide
  rw [he]
  exact case2278
#print axioms case3302

theorem case2279 : checkNat 2279 = true := by native_decide
#print axioms case2279

theorem case2282 : checkNat 2282 = true := by native_decide
#print axioms case2282

theorem case3306 : checkNat 3306 = true := by
  apply check_of_normalize (Case.ofNat 3306)
  have he : (Case.ofNat 3306).normalize = Case.ofNat 2282 := by decide
  rw [he]
  exact case2282
#print axioms case3306

theorem case2283 : checkNat 2283 = true := by native_decide
#print axioms case2283

theorem case2286 : checkNat 2286 = true := by native_decide
#print axioms case2286

theorem case3310 : checkNat 3310 = true := by
  apply check_of_normalize (Case.ofNat 3310)
  have he : (Case.ofNat 3310).normalize = Case.ofNat 2286 := by decide
  rw [he]
  exact case2286
#print axioms case3310

theorem case2287 : checkNat 2287 = true := by native_decide
#print axioms case2287

theorem case2290 : checkNat 2290 = true := by native_decide
#print axioms case2290

theorem case3314 : checkNat 3314 = true := by
  apply check_of_normalize (Case.ofNat 3314)
  have he : (Case.ofNat 3314).normalize = Case.ofNat 2290 := by decide
  rw [he]
  exact case2290
#print axioms case3314

theorem case2291 : checkNat 2291 = true := by native_decide
#print axioms case2291

theorem case2294 : checkNat 2294 = true := by native_decide
#print axioms case2294

theorem case3318 : checkNat 3318 = true := by
  apply check_of_normalize (Case.ofNat 3318)
  have he : (Case.ofNat 3318).normalize = Case.ofNat 2294 := by decide
  rw [he]
  exact case2294
#print axioms case3318

theorem case2295 : checkNat 2295 = true := by native_decide
#print axioms case2295

theorem case2298 : checkNat 2298 = true := by native_decide
#print axioms case2298

theorem case3322 : checkNat 3322 = true := by
  apply check_of_normalize (Case.ofNat 3322)
  have he : (Case.ofNat 3322).normalize = Case.ofNat 2298 := by decide
  rw [he]
  exact case2298
#print axioms case3322

theorem case2299 : checkNat 2299 = true := by native_decide
#print axioms case2299

theorem case2302 : checkNat 2302 = true := by native_decide
#print axioms case2302

theorem case3326 : checkNat 3326 = true := by
  apply check_of_normalize (Case.ofNat 3326)
  have he : (Case.ofNat 3326).normalize = Case.ofNat 2302 := by decide
  rw [he]
  exact case2302
#print axioms case3326

theorem case2303 : checkNat 2303 = true := by native_decide
#print axioms case2303

theorem accepted :
    checkNat 2242 = true ∧
    checkNat 2243 = true ∧
    checkNat 2246 = true ∧
    checkNat 2247 = true ∧
    checkNat 2250 = true ∧
    checkNat 2251 = true ∧
    checkNat 2254 = true ∧
    checkNat 2255 = true ∧
    checkNat 2258 = true ∧
    checkNat 2259 = true ∧
    checkNat 2262 = true ∧
    checkNat 2263 = true ∧
    checkNat 2266 = true ∧
    checkNat 2267 = true ∧
    checkNat 2270 = true ∧
    checkNat 2271 = true ∧
    checkNat 2274 = true ∧
    checkNat 2275 = true ∧
    checkNat 2278 = true ∧
    checkNat 2279 = true ∧
    checkNat 2282 = true ∧
    checkNat 2283 = true ∧
    checkNat 2286 = true ∧
    checkNat 2287 = true ∧
    checkNat 2290 = true ∧
    checkNat 2291 = true ∧
    checkNat 2294 = true ∧
    checkNat 2295 = true ∧
    checkNat 2298 = true ∧
    checkNat 2299 = true ∧
    checkNat 2302 = true ∧
    checkNat 2303 = true ∧
    checkNat 3266 = true ∧
    checkNat 3270 = true ∧
    checkNat 3274 = true ∧
    checkNat 3278 = true ∧
    checkNat 3282 = true ∧
    checkNat 3286 = true ∧
    checkNat 3290 = true ∧
    checkNat 3294 = true ∧
    checkNat 3298 = true ∧
    checkNat 3302 = true ∧
    checkNat 3306 = true ∧
    checkNat 3310 = true ∧
    checkNat 3314 = true ∧
    checkNat 3318 = true ∧
    checkNat 3322 = true ∧
    checkNat 3326 = true := by
  exact ⟨case2242, case2243, case2246, case2247, case2250, case2251, case2254, case2255, case2258, case2259, case2262, case2263, case2266, case2267, case2270, case2271, case2274, case2275, case2278, case2279, case2282, case2283, case2286, case2287, case2290, case2291, case2294, case2295, case2298, case2299, case2302, case2303, case3266, case3270, case3274, case3278, case3282, case3286, case3290, case3294, case3298, case3302, case3306, case3310, case3314, case3318, case3322, case3326⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1632
