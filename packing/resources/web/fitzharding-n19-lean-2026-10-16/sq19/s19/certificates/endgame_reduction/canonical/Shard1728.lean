import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1728
open Sq19.Endgame.Reduction

theorem case2434 : checkNat 2434 = true := by native_decide
#print axioms case2434

theorem case3458 : checkNat 3458 = true := by
  apply check_of_normalize (Case.ofNat 3458)
  have he : (Case.ofNat 3458).normalize = Case.ofNat 2434 := by decide
  rw [he]
  exact case2434
#print axioms case3458

theorem case2435 : checkNat 2435 = true := by native_decide
#print axioms case2435

theorem case2438 : checkNat 2438 = true := by native_decide
#print axioms case2438

theorem case3462 : checkNat 3462 = true := by
  apply check_of_normalize (Case.ofNat 3462)
  have he : (Case.ofNat 3462).normalize = Case.ofNat 2438 := by decide
  rw [he]
  exact case2438
#print axioms case3462

theorem case2439 : checkNat 2439 = true := by native_decide
#print axioms case2439

theorem case2442 : checkNat 2442 = true := by native_decide
#print axioms case2442

theorem case3466 : checkNat 3466 = true := by
  apply check_of_normalize (Case.ofNat 3466)
  have he : (Case.ofNat 3466).normalize = Case.ofNat 2442 := by decide
  rw [he]
  exact case2442
#print axioms case3466

theorem case2443 : checkNat 2443 = true := by native_decide
#print axioms case2443

theorem case2446 : checkNat 2446 = true := by native_decide
#print axioms case2446

theorem case3470 : checkNat 3470 = true := by
  apply check_of_normalize (Case.ofNat 3470)
  have he : (Case.ofNat 3470).normalize = Case.ofNat 2446 := by decide
  rw [he]
  exact case2446
#print axioms case3470

theorem case2447 : checkNat 2447 = true := by native_decide
#print axioms case2447

theorem case2450 : checkNat 2450 = true := by native_decide
#print axioms case2450

theorem case3474 : checkNat 3474 = true := by
  apply check_of_normalize (Case.ofNat 3474)
  have he : (Case.ofNat 3474).normalize = Case.ofNat 2450 := by decide
  rw [he]
  exact case2450
#print axioms case3474

theorem case2451 : checkNat 2451 = true := by native_decide
#print axioms case2451

theorem case2454 : checkNat 2454 = true := by native_decide
#print axioms case2454

theorem case3478 : checkNat 3478 = true := by
  apply check_of_normalize (Case.ofNat 3478)
  have he : (Case.ofNat 3478).normalize = Case.ofNat 2454 := by decide
  rw [he]
  exact case2454
#print axioms case3478

theorem case2455 : checkNat 2455 = true := by native_decide
#print axioms case2455

theorem case2458 : checkNat 2458 = true := by native_decide
#print axioms case2458

theorem case3482 : checkNat 3482 = true := by
  apply check_of_normalize (Case.ofNat 3482)
  have he : (Case.ofNat 3482).normalize = Case.ofNat 2458 := by decide
  rw [he]
  exact case2458
#print axioms case3482

theorem case2459 : checkNat 2459 = true := by native_decide
#print axioms case2459

theorem case2462 : checkNat 2462 = true := by native_decide
#print axioms case2462

theorem case3486 : checkNat 3486 = true := by
  apply check_of_normalize (Case.ofNat 3486)
  have he : (Case.ofNat 3486).normalize = Case.ofNat 2462 := by decide
  rw [he]
  exact case2462
#print axioms case3486

theorem case2463 : checkNat 2463 = true := by native_decide
#print axioms case2463

theorem case2466 : checkNat 2466 = true := by native_decide
#print axioms case2466

theorem case3490 : checkNat 3490 = true := by
  apply check_of_normalize (Case.ofNat 3490)
  have he : (Case.ofNat 3490).normalize = Case.ofNat 2466 := by decide
  rw [he]
  exact case2466
#print axioms case3490

theorem case2467 : checkNat 2467 = true := by native_decide
#print axioms case2467

theorem case2470 : checkNat 2470 = true := by native_decide
#print axioms case2470

theorem case3494 : checkNat 3494 = true := by
  apply check_of_normalize (Case.ofNat 3494)
  have he : (Case.ofNat 3494).normalize = Case.ofNat 2470 := by decide
  rw [he]
  exact case2470
#print axioms case3494

theorem case2471 : checkNat 2471 = true := by native_decide
#print axioms case2471

theorem case2474 : checkNat 2474 = true := by native_decide
#print axioms case2474

theorem case3498 : checkNat 3498 = true := by
  apply check_of_normalize (Case.ofNat 3498)
  have he : (Case.ofNat 3498).normalize = Case.ofNat 2474 := by decide
  rw [he]
  exact case2474
#print axioms case3498

theorem case2475 : checkNat 2475 = true := by native_decide
#print axioms case2475

theorem case2478 : checkNat 2478 = true := by native_decide
#print axioms case2478

theorem case3502 : checkNat 3502 = true := by
  apply check_of_normalize (Case.ofNat 3502)
  have he : (Case.ofNat 3502).normalize = Case.ofNat 2478 := by decide
  rw [he]
  exact case2478
#print axioms case3502

theorem case2479 : checkNat 2479 = true := by native_decide
#print axioms case2479

theorem case2482 : checkNat 2482 = true := by native_decide
#print axioms case2482

theorem case3506 : checkNat 3506 = true := by
  apply check_of_normalize (Case.ofNat 3506)
  have he : (Case.ofNat 3506).normalize = Case.ofNat 2482 := by decide
  rw [he]
  exact case2482
#print axioms case3506

theorem case2483 : checkNat 2483 = true := by native_decide
#print axioms case2483

theorem case2486 : checkNat 2486 = true := by native_decide
#print axioms case2486

theorem case3510 : checkNat 3510 = true := by
  apply check_of_normalize (Case.ofNat 3510)
  have he : (Case.ofNat 3510).normalize = Case.ofNat 2486 := by decide
  rw [he]
  exact case2486
#print axioms case3510

theorem case2487 : checkNat 2487 = true := by native_decide
#print axioms case2487

theorem case2490 : checkNat 2490 = true := by native_decide
#print axioms case2490

theorem case3514 : checkNat 3514 = true := by
  apply check_of_normalize (Case.ofNat 3514)
  have he : (Case.ofNat 3514).normalize = Case.ofNat 2490 := by decide
  rw [he]
  exact case2490
#print axioms case3514

theorem case2491 : checkNat 2491 = true := by native_decide
#print axioms case2491

theorem case2494 : checkNat 2494 = true := by native_decide
#print axioms case2494

theorem case3518 : checkNat 3518 = true := by
  apply check_of_normalize (Case.ofNat 3518)
  have he : (Case.ofNat 3518).normalize = Case.ofNat 2494 := by decide
  rw [he]
  exact case2494
#print axioms case3518

theorem case2495 : checkNat 2495 = true := by native_decide
#print axioms case2495

theorem accepted :
    checkNat 2434 = true ∧
    checkNat 2435 = true ∧
    checkNat 2438 = true ∧
    checkNat 2439 = true ∧
    checkNat 2442 = true ∧
    checkNat 2443 = true ∧
    checkNat 2446 = true ∧
    checkNat 2447 = true ∧
    checkNat 2450 = true ∧
    checkNat 2451 = true ∧
    checkNat 2454 = true ∧
    checkNat 2455 = true ∧
    checkNat 2458 = true ∧
    checkNat 2459 = true ∧
    checkNat 2462 = true ∧
    checkNat 2463 = true ∧
    checkNat 2466 = true ∧
    checkNat 2467 = true ∧
    checkNat 2470 = true ∧
    checkNat 2471 = true ∧
    checkNat 2474 = true ∧
    checkNat 2475 = true ∧
    checkNat 2478 = true ∧
    checkNat 2479 = true ∧
    checkNat 2482 = true ∧
    checkNat 2483 = true ∧
    checkNat 2486 = true ∧
    checkNat 2487 = true ∧
    checkNat 2490 = true ∧
    checkNat 2491 = true ∧
    checkNat 2494 = true ∧
    checkNat 2495 = true ∧
    checkNat 3458 = true ∧
    checkNat 3462 = true ∧
    checkNat 3466 = true ∧
    checkNat 3470 = true ∧
    checkNat 3474 = true ∧
    checkNat 3478 = true ∧
    checkNat 3482 = true ∧
    checkNat 3486 = true ∧
    checkNat 3490 = true ∧
    checkNat 3494 = true ∧
    checkNat 3498 = true ∧
    checkNat 3502 = true ∧
    checkNat 3506 = true ∧
    checkNat 3510 = true ∧
    checkNat 3514 = true ∧
    checkNat 3518 = true := by
  exact ⟨case2434, case2435, case2438, case2439, case2442, case2443, case2446, case2447, case2450, case2451, case2454, case2455, case2458, case2459, case2462, case2463, case2466, case2467, case2470, case2471, case2474, case2475, case2478, case2479, case2482, case2483, case2486, case2487, case2490, case2491, case2494, case2495, case3458, case3462, case3466, case3470, case3474, case3478, case3482, case3486, case3490, case3494, case3498, case3502, case3506, case3510, case3514, case3518⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1728
