import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1664
open Sq19.Endgame.Reduction

theorem case2306 : checkNat 2306 = true := by native_decide
#print axioms case2306

theorem case3330 : checkNat 3330 = true := by
  apply check_of_normalize (Case.ofNat 3330)
  have he : (Case.ofNat 3330).normalize = Case.ofNat 2306 := by decide
  rw [he]
  exact case2306
#print axioms case3330

theorem case2307 : checkNat 2307 = true := by native_decide
#print axioms case2307

theorem case2310 : checkNat 2310 = true := by native_decide
#print axioms case2310

theorem case3334 : checkNat 3334 = true := by
  apply check_of_normalize (Case.ofNat 3334)
  have he : (Case.ofNat 3334).normalize = Case.ofNat 2310 := by decide
  rw [he]
  exact case2310
#print axioms case3334

theorem case2311 : checkNat 2311 = true := by native_decide
#print axioms case2311

theorem case2314 : checkNat 2314 = true := by native_decide
#print axioms case2314

theorem case3338 : checkNat 3338 = true := by
  apply check_of_normalize (Case.ofNat 3338)
  have he : (Case.ofNat 3338).normalize = Case.ofNat 2314 := by decide
  rw [he]
  exact case2314
#print axioms case3338

theorem case2315 : checkNat 2315 = true := by native_decide
#print axioms case2315

theorem case2318 : checkNat 2318 = true := by native_decide
#print axioms case2318

theorem case3342 : checkNat 3342 = true := by
  apply check_of_normalize (Case.ofNat 3342)
  have he : (Case.ofNat 3342).normalize = Case.ofNat 2318 := by decide
  rw [he]
  exact case2318
#print axioms case3342

theorem case2319 : checkNat 2319 = true := by native_decide
#print axioms case2319

theorem case2322 : checkNat 2322 = true := by native_decide
#print axioms case2322

theorem case3346 : checkNat 3346 = true := by
  apply check_of_normalize (Case.ofNat 3346)
  have he : (Case.ofNat 3346).normalize = Case.ofNat 2322 := by decide
  rw [he]
  exact case2322
#print axioms case3346

theorem case2323 : checkNat 2323 = true := by native_decide
#print axioms case2323

theorem case2326 : checkNat 2326 = true := by native_decide
#print axioms case2326

theorem case3350 : checkNat 3350 = true := by
  apply check_of_normalize (Case.ofNat 3350)
  have he : (Case.ofNat 3350).normalize = Case.ofNat 2326 := by decide
  rw [he]
  exact case2326
#print axioms case3350

theorem case2327 : checkNat 2327 = true := by native_decide
#print axioms case2327

theorem case2330 : checkNat 2330 = true := by native_decide
#print axioms case2330

theorem case3354 : checkNat 3354 = true := by
  apply check_of_normalize (Case.ofNat 3354)
  have he : (Case.ofNat 3354).normalize = Case.ofNat 2330 := by decide
  rw [he]
  exact case2330
#print axioms case3354

theorem case2331 : checkNat 2331 = true := by native_decide
#print axioms case2331

theorem case2334 : checkNat 2334 = true := by native_decide
#print axioms case2334

theorem case3358 : checkNat 3358 = true := by
  apply check_of_normalize (Case.ofNat 3358)
  have he : (Case.ofNat 3358).normalize = Case.ofNat 2334 := by decide
  rw [he]
  exact case2334
#print axioms case3358

theorem case2335 : checkNat 2335 = true := by native_decide
#print axioms case2335

theorem case2338 : checkNat 2338 = true := by native_decide
#print axioms case2338

theorem case3362 : checkNat 3362 = true := by
  apply check_of_normalize (Case.ofNat 3362)
  have he : (Case.ofNat 3362).normalize = Case.ofNat 2338 := by decide
  rw [he]
  exact case2338
#print axioms case3362

theorem case2339 : checkNat 2339 = true := by native_decide
#print axioms case2339

theorem case2342 : checkNat 2342 = true := by native_decide
#print axioms case2342

theorem case3366 : checkNat 3366 = true := by
  apply check_of_normalize (Case.ofNat 3366)
  have he : (Case.ofNat 3366).normalize = Case.ofNat 2342 := by decide
  rw [he]
  exact case2342
#print axioms case3366

theorem case2343 : checkNat 2343 = true := by native_decide
#print axioms case2343

theorem case2346 : checkNat 2346 = true := by native_decide
#print axioms case2346

theorem case3370 : checkNat 3370 = true := by
  apply check_of_normalize (Case.ofNat 3370)
  have he : (Case.ofNat 3370).normalize = Case.ofNat 2346 := by decide
  rw [he]
  exact case2346
#print axioms case3370

theorem case2347 : checkNat 2347 = true := by native_decide
#print axioms case2347

theorem case2350 : checkNat 2350 = true := by native_decide
#print axioms case2350

theorem case3374 : checkNat 3374 = true := by
  apply check_of_normalize (Case.ofNat 3374)
  have he : (Case.ofNat 3374).normalize = Case.ofNat 2350 := by decide
  rw [he]
  exact case2350
#print axioms case3374

theorem case2351 : checkNat 2351 = true := by native_decide
#print axioms case2351

theorem case2354 : checkNat 2354 = true := by native_decide
#print axioms case2354

theorem case3378 : checkNat 3378 = true := by
  apply check_of_normalize (Case.ofNat 3378)
  have he : (Case.ofNat 3378).normalize = Case.ofNat 2354 := by decide
  rw [he]
  exact case2354
#print axioms case3378

theorem case2355 : checkNat 2355 = true := by native_decide
#print axioms case2355

theorem case2358 : checkNat 2358 = true := by native_decide
#print axioms case2358

theorem case3382 : checkNat 3382 = true := by
  apply check_of_normalize (Case.ofNat 3382)
  have he : (Case.ofNat 3382).normalize = Case.ofNat 2358 := by decide
  rw [he]
  exact case2358
#print axioms case3382

theorem case2359 : checkNat 2359 = true := by native_decide
#print axioms case2359

theorem case2362 : checkNat 2362 = true := by native_decide
#print axioms case2362

theorem case3386 : checkNat 3386 = true := by
  apply check_of_normalize (Case.ofNat 3386)
  have he : (Case.ofNat 3386).normalize = Case.ofNat 2362 := by decide
  rw [he]
  exact case2362
#print axioms case3386

theorem case2363 : checkNat 2363 = true := by native_decide
#print axioms case2363

theorem case2366 : checkNat 2366 = true := by native_decide
#print axioms case2366

theorem case3390 : checkNat 3390 = true := by
  apply check_of_normalize (Case.ofNat 3390)
  have he : (Case.ofNat 3390).normalize = Case.ofNat 2366 := by decide
  rw [he]
  exact case2366
#print axioms case3390

theorem case2367 : checkNat 2367 = true := by native_decide
#print axioms case2367

theorem accepted :
    checkNat 2306 = true ∧
    checkNat 2307 = true ∧
    checkNat 2310 = true ∧
    checkNat 2311 = true ∧
    checkNat 2314 = true ∧
    checkNat 2315 = true ∧
    checkNat 2318 = true ∧
    checkNat 2319 = true ∧
    checkNat 2322 = true ∧
    checkNat 2323 = true ∧
    checkNat 2326 = true ∧
    checkNat 2327 = true ∧
    checkNat 2330 = true ∧
    checkNat 2331 = true ∧
    checkNat 2334 = true ∧
    checkNat 2335 = true ∧
    checkNat 2338 = true ∧
    checkNat 2339 = true ∧
    checkNat 2342 = true ∧
    checkNat 2343 = true ∧
    checkNat 2346 = true ∧
    checkNat 2347 = true ∧
    checkNat 2350 = true ∧
    checkNat 2351 = true ∧
    checkNat 2354 = true ∧
    checkNat 2355 = true ∧
    checkNat 2358 = true ∧
    checkNat 2359 = true ∧
    checkNat 2362 = true ∧
    checkNat 2363 = true ∧
    checkNat 2366 = true ∧
    checkNat 2367 = true ∧
    checkNat 3330 = true ∧
    checkNat 3334 = true ∧
    checkNat 3338 = true ∧
    checkNat 3342 = true ∧
    checkNat 3346 = true ∧
    checkNat 3350 = true ∧
    checkNat 3354 = true ∧
    checkNat 3358 = true ∧
    checkNat 3362 = true ∧
    checkNat 3366 = true ∧
    checkNat 3370 = true ∧
    checkNat 3374 = true ∧
    checkNat 3378 = true ∧
    checkNat 3382 = true ∧
    checkNat 3386 = true ∧
    checkNat 3390 = true := by
  exact ⟨case2306, case2307, case2310, case2311, case2314, case2315, case2318, case2319, case2322, case2323, case2326, case2327, case2330, case2331, case2334, case2335, case2338, case2339, case2342, case2343, case2346, case2347, case2350, case2351, case2354, case2355, case2358, case2359, case2362, case2363, case2366, case2367, case3330, case3334, case3338, case3342, case3346, case3350, case3354, case3358, case3362, case3366, case3370, case3374, case3378, case3382, case3386, case3390⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1664
