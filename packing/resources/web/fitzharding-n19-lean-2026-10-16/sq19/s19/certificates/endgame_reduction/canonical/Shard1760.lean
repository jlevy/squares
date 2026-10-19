import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1760
open Sq19.Endgame.Reduction

theorem case2498 : checkNat 2498 = true := by native_decide
#print axioms case2498

theorem case3522 : checkNat 3522 = true := by
  apply check_of_normalize (Case.ofNat 3522)
  have he : (Case.ofNat 3522).normalize = Case.ofNat 2498 := by decide
  rw [he]
  exact case2498
#print axioms case3522

theorem case2499 : checkNat 2499 = true := by native_decide
#print axioms case2499

theorem case2502 : checkNat 2502 = true := by native_decide
#print axioms case2502

theorem case3526 : checkNat 3526 = true := by
  apply check_of_normalize (Case.ofNat 3526)
  have he : (Case.ofNat 3526).normalize = Case.ofNat 2502 := by decide
  rw [he]
  exact case2502
#print axioms case3526

theorem case2503 : checkNat 2503 = true := by native_decide
#print axioms case2503

theorem case2506 : checkNat 2506 = true := by native_decide
#print axioms case2506

theorem case3530 : checkNat 3530 = true := by
  apply check_of_normalize (Case.ofNat 3530)
  have he : (Case.ofNat 3530).normalize = Case.ofNat 2506 := by decide
  rw [he]
  exact case2506
#print axioms case3530

theorem case2507 : checkNat 2507 = true := by native_decide
#print axioms case2507

theorem case2510 : checkNat 2510 = true := by native_decide
#print axioms case2510

theorem case3534 : checkNat 3534 = true := by
  apply check_of_normalize (Case.ofNat 3534)
  have he : (Case.ofNat 3534).normalize = Case.ofNat 2510 := by decide
  rw [he]
  exact case2510
#print axioms case3534

theorem case2511 : checkNat 2511 = true := by native_decide
#print axioms case2511

theorem case2514 : checkNat 2514 = true := by native_decide
#print axioms case2514

theorem case3538 : checkNat 3538 = true := by
  apply check_of_normalize (Case.ofNat 3538)
  have he : (Case.ofNat 3538).normalize = Case.ofNat 2514 := by decide
  rw [he]
  exact case2514
#print axioms case3538

theorem case2515 : checkNat 2515 = true := by native_decide
#print axioms case2515

theorem case2518 : checkNat 2518 = true := by native_decide
#print axioms case2518

theorem case3542 : checkNat 3542 = true := by
  apply check_of_normalize (Case.ofNat 3542)
  have he : (Case.ofNat 3542).normalize = Case.ofNat 2518 := by decide
  rw [he]
  exact case2518
#print axioms case3542

theorem case2519 : checkNat 2519 = true := by native_decide
#print axioms case2519

theorem case2522 : checkNat 2522 = true := by native_decide
#print axioms case2522

theorem case3546 : checkNat 3546 = true := by
  apply check_of_normalize (Case.ofNat 3546)
  have he : (Case.ofNat 3546).normalize = Case.ofNat 2522 := by decide
  rw [he]
  exact case2522
#print axioms case3546

theorem case2523 : checkNat 2523 = true := by native_decide
#print axioms case2523

theorem case2526 : checkNat 2526 = true := by native_decide
#print axioms case2526

theorem case3550 : checkNat 3550 = true := by
  apply check_of_normalize (Case.ofNat 3550)
  have he : (Case.ofNat 3550).normalize = Case.ofNat 2526 := by decide
  rw [he]
  exact case2526
#print axioms case3550

theorem case2527 : checkNat 2527 = true := by native_decide
#print axioms case2527

theorem case2530 : checkNat 2530 = true := by native_decide
#print axioms case2530

theorem case3554 : checkNat 3554 = true := by
  apply check_of_normalize (Case.ofNat 3554)
  have he : (Case.ofNat 3554).normalize = Case.ofNat 2530 := by decide
  rw [he]
  exact case2530
#print axioms case3554

theorem case2531 : checkNat 2531 = true := by native_decide
#print axioms case2531

theorem case2534 : checkNat 2534 = true := by native_decide
#print axioms case2534

theorem case3558 : checkNat 3558 = true := by
  apply check_of_normalize (Case.ofNat 3558)
  have he : (Case.ofNat 3558).normalize = Case.ofNat 2534 := by decide
  rw [he]
  exact case2534
#print axioms case3558

theorem case2535 : checkNat 2535 = true := by native_decide
#print axioms case2535

theorem case2538 : checkNat 2538 = true := by native_decide
#print axioms case2538

theorem case3562 : checkNat 3562 = true := by
  apply check_of_normalize (Case.ofNat 3562)
  have he : (Case.ofNat 3562).normalize = Case.ofNat 2538 := by decide
  rw [he]
  exact case2538
#print axioms case3562

theorem case2539 : checkNat 2539 = true := by native_decide
#print axioms case2539

theorem case2542 : checkNat 2542 = true := by native_decide
#print axioms case2542

theorem case3566 : checkNat 3566 = true := by
  apply check_of_normalize (Case.ofNat 3566)
  have he : (Case.ofNat 3566).normalize = Case.ofNat 2542 := by decide
  rw [he]
  exact case2542
#print axioms case3566

theorem case2543 : checkNat 2543 = true := by native_decide
#print axioms case2543

theorem case2546 : checkNat 2546 = true := by native_decide
#print axioms case2546

theorem case3570 : checkNat 3570 = true := by
  apply check_of_normalize (Case.ofNat 3570)
  have he : (Case.ofNat 3570).normalize = Case.ofNat 2546 := by decide
  rw [he]
  exact case2546
#print axioms case3570

theorem case2547 : checkNat 2547 = true := by native_decide
#print axioms case2547

theorem case2550 : checkNat 2550 = true := by native_decide
#print axioms case2550

theorem case3574 : checkNat 3574 = true := by
  apply check_of_normalize (Case.ofNat 3574)
  have he : (Case.ofNat 3574).normalize = Case.ofNat 2550 := by decide
  rw [he]
  exact case2550
#print axioms case3574

theorem case2551 : checkNat 2551 = true := by native_decide
#print axioms case2551

theorem case2554 : checkNat 2554 = true := by native_decide
#print axioms case2554

theorem case3578 : checkNat 3578 = true := by
  apply check_of_normalize (Case.ofNat 3578)
  have he : (Case.ofNat 3578).normalize = Case.ofNat 2554 := by decide
  rw [he]
  exact case2554
#print axioms case3578

theorem case2555 : checkNat 2555 = true := by native_decide
#print axioms case2555

theorem case2558 : checkNat 2558 = true := by native_decide
#print axioms case2558

theorem case3582 : checkNat 3582 = true := by
  apply check_of_normalize (Case.ofNat 3582)
  have he : (Case.ofNat 3582).normalize = Case.ofNat 2558 := by decide
  rw [he]
  exact case2558
#print axioms case3582

theorem case2559 : checkNat 2559 = true := by native_decide
#print axioms case2559

theorem accepted :
    checkNat 2498 = true ∧
    checkNat 2499 = true ∧
    checkNat 2502 = true ∧
    checkNat 2503 = true ∧
    checkNat 2506 = true ∧
    checkNat 2507 = true ∧
    checkNat 2510 = true ∧
    checkNat 2511 = true ∧
    checkNat 2514 = true ∧
    checkNat 2515 = true ∧
    checkNat 2518 = true ∧
    checkNat 2519 = true ∧
    checkNat 2522 = true ∧
    checkNat 2523 = true ∧
    checkNat 2526 = true ∧
    checkNat 2527 = true ∧
    checkNat 2530 = true ∧
    checkNat 2531 = true ∧
    checkNat 2534 = true ∧
    checkNat 2535 = true ∧
    checkNat 2538 = true ∧
    checkNat 2539 = true ∧
    checkNat 2542 = true ∧
    checkNat 2543 = true ∧
    checkNat 2546 = true ∧
    checkNat 2547 = true ∧
    checkNat 2550 = true ∧
    checkNat 2551 = true ∧
    checkNat 2554 = true ∧
    checkNat 2555 = true ∧
    checkNat 2558 = true ∧
    checkNat 2559 = true ∧
    checkNat 3522 = true ∧
    checkNat 3526 = true ∧
    checkNat 3530 = true ∧
    checkNat 3534 = true ∧
    checkNat 3538 = true ∧
    checkNat 3542 = true ∧
    checkNat 3546 = true ∧
    checkNat 3550 = true ∧
    checkNat 3554 = true ∧
    checkNat 3558 = true ∧
    checkNat 3562 = true ∧
    checkNat 3566 = true ∧
    checkNat 3570 = true ∧
    checkNat 3574 = true ∧
    checkNat 3578 = true ∧
    checkNat 3582 = true := by
  exact ⟨case2498, case2499, case2502, case2503, case2506, case2507, case2510, case2511, case2514, case2515, case2518, case2519, case2522, case2523, case2526, case2527, case2530, case2531, case2534, case2535, case2538, case2539, case2542, case2543, case2546, case2547, case2550, case2551, case2554, case2555, case2558, case2559, case3522, case3526, case3530, case3534, case3538, case3542, case3546, case3550, case3554, case3558, case3562, case3566, case3570, case3574, case3578, case3582⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1760
