import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1696
open Sq19.Endgame.Reduction

theorem case2370 : checkNat 2370 = true := by native_decide
#print axioms case2370

theorem case3394 : checkNat 3394 = true := by
  apply check_of_normalize (Case.ofNat 3394)
  have he : (Case.ofNat 3394).normalize = Case.ofNat 2370 := by decide
  rw [he]
  exact case2370
#print axioms case3394

theorem case2371 : checkNat 2371 = true := by native_decide
#print axioms case2371

theorem case2374 : checkNat 2374 = true := by native_decide
#print axioms case2374

theorem case3398 : checkNat 3398 = true := by
  apply check_of_normalize (Case.ofNat 3398)
  have he : (Case.ofNat 3398).normalize = Case.ofNat 2374 := by decide
  rw [he]
  exact case2374
#print axioms case3398

theorem case2375 : checkNat 2375 = true := by native_decide
#print axioms case2375

theorem case2378 : checkNat 2378 = true := by native_decide
#print axioms case2378

theorem case3402 : checkNat 3402 = true := by
  apply check_of_normalize (Case.ofNat 3402)
  have he : (Case.ofNat 3402).normalize = Case.ofNat 2378 := by decide
  rw [he]
  exact case2378
#print axioms case3402

theorem case2379 : checkNat 2379 = true := by native_decide
#print axioms case2379

theorem case2382 : checkNat 2382 = true := by native_decide
#print axioms case2382

theorem case3406 : checkNat 3406 = true := by
  apply check_of_normalize (Case.ofNat 3406)
  have he : (Case.ofNat 3406).normalize = Case.ofNat 2382 := by decide
  rw [he]
  exact case2382
#print axioms case3406

theorem case2383 : checkNat 2383 = true := by native_decide
#print axioms case2383

theorem case2386 : checkNat 2386 = true := by native_decide
#print axioms case2386

theorem case3410 : checkNat 3410 = true := by
  apply check_of_normalize (Case.ofNat 3410)
  have he : (Case.ofNat 3410).normalize = Case.ofNat 2386 := by decide
  rw [he]
  exact case2386
#print axioms case3410

theorem case2387 : checkNat 2387 = true := by native_decide
#print axioms case2387

theorem case2390 : checkNat 2390 = true := by native_decide
#print axioms case2390

theorem case3414 : checkNat 3414 = true := by
  apply check_of_normalize (Case.ofNat 3414)
  have he : (Case.ofNat 3414).normalize = Case.ofNat 2390 := by decide
  rw [he]
  exact case2390
#print axioms case3414

theorem case2391 : checkNat 2391 = true := by native_decide
#print axioms case2391

theorem case2394 : checkNat 2394 = true := by native_decide
#print axioms case2394

theorem case3418 : checkNat 3418 = true := by
  apply check_of_normalize (Case.ofNat 3418)
  have he : (Case.ofNat 3418).normalize = Case.ofNat 2394 := by decide
  rw [he]
  exact case2394
#print axioms case3418

theorem case2395 : checkNat 2395 = true := by native_decide
#print axioms case2395

theorem case2398 : checkNat 2398 = true := by native_decide
#print axioms case2398

theorem case3422 : checkNat 3422 = true := by
  apply check_of_normalize (Case.ofNat 3422)
  have he : (Case.ofNat 3422).normalize = Case.ofNat 2398 := by decide
  rw [he]
  exact case2398
#print axioms case3422

theorem case2399 : checkNat 2399 = true := by native_decide
#print axioms case2399

theorem case2402 : checkNat 2402 = true := by native_decide
#print axioms case2402

theorem case3426 : checkNat 3426 = true := by
  apply check_of_normalize (Case.ofNat 3426)
  have he : (Case.ofNat 3426).normalize = Case.ofNat 2402 := by decide
  rw [he]
  exact case2402
#print axioms case3426

theorem case2403 : checkNat 2403 = true := by native_decide
#print axioms case2403

theorem case2406 : checkNat 2406 = true := by native_decide
#print axioms case2406

theorem case3430 : checkNat 3430 = true := by
  apply check_of_normalize (Case.ofNat 3430)
  have he : (Case.ofNat 3430).normalize = Case.ofNat 2406 := by decide
  rw [he]
  exact case2406
#print axioms case3430

theorem case2407 : checkNat 2407 = true := by native_decide
#print axioms case2407

theorem case2410 : checkNat 2410 = true := by native_decide
#print axioms case2410

theorem case3434 : checkNat 3434 = true := by
  apply check_of_normalize (Case.ofNat 3434)
  have he : (Case.ofNat 3434).normalize = Case.ofNat 2410 := by decide
  rw [he]
  exact case2410
#print axioms case3434

theorem case2411 : checkNat 2411 = true := by native_decide
#print axioms case2411

theorem case2414 : checkNat 2414 = true := by native_decide
#print axioms case2414

theorem case3438 : checkNat 3438 = true := by
  apply check_of_normalize (Case.ofNat 3438)
  have he : (Case.ofNat 3438).normalize = Case.ofNat 2414 := by decide
  rw [he]
  exact case2414
#print axioms case3438

theorem case2415 : checkNat 2415 = true := by native_decide
#print axioms case2415

theorem case2418 : checkNat 2418 = true := by native_decide
#print axioms case2418

theorem case3442 : checkNat 3442 = true := by
  apply check_of_normalize (Case.ofNat 3442)
  have he : (Case.ofNat 3442).normalize = Case.ofNat 2418 := by decide
  rw [he]
  exact case2418
#print axioms case3442

theorem case2419 : checkNat 2419 = true := by native_decide
#print axioms case2419

theorem case2422 : checkNat 2422 = true := by native_decide
#print axioms case2422

theorem case3446 : checkNat 3446 = true := by
  apply check_of_normalize (Case.ofNat 3446)
  have he : (Case.ofNat 3446).normalize = Case.ofNat 2422 := by decide
  rw [he]
  exact case2422
#print axioms case3446

theorem case2423 : checkNat 2423 = true := by native_decide
#print axioms case2423

theorem case2426 : checkNat 2426 = true := by native_decide
#print axioms case2426

theorem case3450 : checkNat 3450 = true := by
  apply check_of_normalize (Case.ofNat 3450)
  have he : (Case.ofNat 3450).normalize = Case.ofNat 2426 := by decide
  rw [he]
  exact case2426
#print axioms case3450

theorem case2427 : checkNat 2427 = true := by native_decide
#print axioms case2427

theorem case2430 : checkNat 2430 = true := by native_decide
#print axioms case2430

theorem case3454 : checkNat 3454 = true := by
  apply check_of_normalize (Case.ofNat 3454)
  have he : (Case.ofNat 3454).normalize = Case.ofNat 2430 := by decide
  rw [he]
  exact case2430
#print axioms case3454

theorem case2431 : checkNat 2431 = true := by native_decide
#print axioms case2431

theorem accepted :
    checkNat 2370 = true ∧
    checkNat 2371 = true ∧
    checkNat 2374 = true ∧
    checkNat 2375 = true ∧
    checkNat 2378 = true ∧
    checkNat 2379 = true ∧
    checkNat 2382 = true ∧
    checkNat 2383 = true ∧
    checkNat 2386 = true ∧
    checkNat 2387 = true ∧
    checkNat 2390 = true ∧
    checkNat 2391 = true ∧
    checkNat 2394 = true ∧
    checkNat 2395 = true ∧
    checkNat 2398 = true ∧
    checkNat 2399 = true ∧
    checkNat 2402 = true ∧
    checkNat 2403 = true ∧
    checkNat 2406 = true ∧
    checkNat 2407 = true ∧
    checkNat 2410 = true ∧
    checkNat 2411 = true ∧
    checkNat 2414 = true ∧
    checkNat 2415 = true ∧
    checkNat 2418 = true ∧
    checkNat 2419 = true ∧
    checkNat 2422 = true ∧
    checkNat 2423 = true ∧
    checkNat 2426 = true ∧
    checkNat 2427 = true ∧
    checkNat 2430 = true ∧
    checkNat 2431 = true ∧
    checkNat 3394 = true ∧
    checkNat 3398 = true ∧
    checkNat 3402 = true ∧
    checkNat 3406 = true ∧
    checkNat 3410 = true ∧
    checkNat 3414 = true ∧
    checkNat 3418 = true ∧
    checkNat 3422 = true ∧
    checkNat 3426 = true ∧
    checkNat 3430 = true ∧
    checkNat 3434 = true ∧
    checkNat 3438 = true ∧
    checkNat 3442 = true ∧
    checkNat 3446 = true ∧
    checkNat 3450 = true ∧
    checkNat 3454 = true := by
  exact ⟨case2370, case2371, case2374, case2375, case2378, case2379, case2382, case2383, case2386, case2387, case2390, case2391, case2394, case2395, case2398, case2399, case2402, case2403, case2406, case2407, case2410, case2411, case2414, case2415, case2418, case2419, case2422, case2423, case2426, case2427, case2430, case2431, case3394, case3398, case3402, case3406, case3410, case3414, case3418, case3422, case3426, case3430, case3434, case3438, case3442, case3446, case3450, case3454⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1696
