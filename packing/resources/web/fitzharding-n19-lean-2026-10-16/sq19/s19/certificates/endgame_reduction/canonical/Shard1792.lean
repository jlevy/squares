import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1792
open Sq19.Endgame.Reduction

theorem case2562 : checkNat 2562 = true := by native_decide
#print axioms case2562

theorem case3586 : checkNat 3586 = true := by
  apply check_of_normalize (Case.ofNat 3586)
  have he : (Case.ofNat 3586).normalize = Case.ofNat 2562 := by decide
  rw [he]
  exact case2562
#print axioms case3586

theorem case2563 : checkNat 2563 = true := by native_decide
#print axioms case2563

theorem case2566 : checkNat 2566 = true := by native_decide
#print axioms case2566

theorem case3590 : checkNat 3590 = true := by
  apply check_of_normalize (Case.ofNat 3590)
  have he : (Case.ofNat 3590).normalize = Case.ofNat 2566 := by decide
  rw [he]
  exact case2566
#print axioms case3590

theorem case2567 : checkNat 2567 = true := by native_decide
#print axioms case2567

theorem case2570 : checkNat 2570 = true := by native_decide
#print axioms case2570

theorem case3594 : checkNat 3594 = true := by
  apply check_of_normalize (Case.ofNat 3594)
  have he : (Case.ofNat 3594).normalize = Case.ofNat 2570 := by decide
  rw [he]
  exact case2570
#print axioms case3594

theorem case2571 : checkNat 2571 = true := by native_decide
#print axioms case2571

theorem case2574 : checkNat 2574 = true := by native_decide
#print axioms case2574

theorem case3598 : checkNat 3598 = true := by
  apply check_of_normalize (Case.ofNat 3598)
  have he : (Case.ofNat 3598).normalize = Case.ofNat 2574 := by decide
  rw [he]
  exact case2574
#print axioms case3598

theorem case2575 : checkNat 2575 = true := by native_decide
#print axioms case2575

theorem case2578 : checkNat 2578 = true := by native_decide
#print axioms case2578

theorem case3602 : checkNat 3602 = true := by
  apply check_of_normalize (Case.ofNat 3602)
  have he : (Case.ofNat 3602).normalize = Case.ofNat 2578 := by decide
  rw [he]
  exact case2578
#print axioms case3602

theorem case2579 : checkNat 2579 = true := by native_decide
#print axioms case2579

theorem case2582 : checkNat 2582 = true := by native_decide
#print axioms case2582

theorem case3606 : checkNat 3606 = true := by
  apply check_of_normalize (Case.ofNat 3606)
  have he : (Case.ofNat 3606).normalize = Case.ofNat 2582 := by decide
  rw [he]
  exact case2582
#print axioms case3606

theorem case2583 : checkNat 2583 = true := by native_decide
#print axioms case2583

theorem case2586 : checkNat 2586 = true := by native_decide
#print axioms case2586

theorem case3610 : checkNat 3610 = true := by
  apply check_of_normalize (Case.ofNat 3610)
  have he : (Case.ofNat 3610).normalize = Case.ofNat 2586 := by decide
  rw [he]
  exact case2586
#print axioms case3610

theorem case2587 : checkNat 2587 = true := by native_decide
#print axioms case2587

theorem case2590 : checkNat 2590 = true := by native_decide
#print axioms case2590

theorem case3614 : checkNat 3614 = true := by
  apply check_of_normalize (Case.ofNat 3614)
  have he : (Case.ofNat 3614).normalize = Case.ofNat 2590 := by decide
  rw [he]
  exact case2590
#print axioms case3614

theorem case2591 : checkNat 2591 = true := by native_decide
#print axioms case2591

theorem case2594 : checkNat 2594 = true := by native_decide
#print axioms case2594

theorem case3618 : checkNat 3618 = true := by
  apply check_of_normalize (Case.ofNat 3618)
  have he : (Case.ofNat 3618).normalize = Case.ofNat 2594 := by decide
  rw [he]
  exact case2594
#print axioms case3618

theorem case2595 : checkNat 2595 = true := by native_decide
#print axioms case2595

theorem case2598 : checkNat 2598 = true := by native_decide
#print axioms case2598

theorem case3622 : checkNat 3622 = true := by
  apply check_of_normalize (Case.ofNat 3622)
  have he : (Case.ofNat 3622).normalize = Case.ofNat 2598 := by decide
  rw [he]
  exact case2598
#print axioms case3622

theorem case2599 : checkNat 2599 = true := by native_decide
#print axioms case2599

theorem case2602 : checkNat 2602 = true := by native_decide
#print axioms case2602

theorem case3626 : checkNat 3626 = true := by
  apply check_of_normalize (Case.ofNat 3626)
  have he : (Case.ofNat 3626).normalize = Case.ofNat 2602 := by decide
  rw [he]
  exact case2602
#print axioms case3626

theorem case2603 : checkNat 2603 = true := by native_decide
#print axioms case2603

theorem case2606 : checkNat 2606 = true := by native_decide
#print axioms case2606

theorem case3630 : checkNat 3630 = true := by
  apply check_of_normalize (Case.ofNat 3630)
  have he : (Case.ofNat 3630).normalize = Case.ofNat 2606 := by decide
  rw [he]
  exact case2606
#print axioms case3630

theorem case2607 : checkNat 2607 = true := by native_decide
#print axioms case2607

theorem case2610 : checkNat 2610 = true := by native_decide
#print axioms case2610

theorem case3634 : checkNat 3634 = true := by
  apply check_of_normalize (Case.ofNat 3634)
  have he : (Case.ofNat 3634).normalize = Case.ofNat 2610 := by decide
  rw [he]
  exact case2610
#print axioms case3634

theorem case2611 : checkNat 2611 = true := by native_decide
#print axioms case2611

theorem case2614 : checkNat 2614 = true := by native_decide
#print axioms case2614

theorem case3638 : checkNat 3638 = true := by
  apply check_of_normalize (Case.ofNat 3638)
  have he : (Case.ofNat 3638).normalize = Case.ofNat 2614 := by decide
  rw [he]
  exact case2614
#print axioms case3638

theorem case2615 : checkNat 2615 = true := by native_decide
#print axioms case2615

theorem case2618 : checkNat 2618 = true := by native_decide
#print axioms case2618

theorem case3642 : checkNat 3642 = true := by
  apply check_of_normalize (Case.ofNat 3642)
  have he : (Case.ofNat 3642).normalize = Case.ofNat 2618 := by decide
  rw [he]
  exact case2618
#print axioms case3642

theorem case2619 : checkNat 2619 = true := by native_decide
#print axioms case2619

theorem case2622 : checkNat 2622 = true := by native_decide
#print axioms case2622

theorem case3646 : checkNat 3646 = true := by
  apply check_of_normalize (Case.ofNat 3646)
  have he : (Case.ofNat 3646).normalize = Case.ofNat 2622 := by decide
  rw [he]
  exact case2622
#print axioms case3646

theorem case2623 : checkNat 2623 = true := by native_decide
#print axioms case2623

theorem accepted :
    checkNat 2562 = true ∧
    checkNat 2563 = true ∧
    checkNat 2566 = true ∧
    checkNat 2567 = true ∧
    checkNat 2570 = true ∧
    checkNat 2571 = true ∧
    checkNat 2574 = true ∧
    checkNat 2575 = true ∧
    checkNat 2578 = true ∧
    checkNat 2579 = true ∧
    checkNat 2582 = true ∧
    checkNat 2583 = true ∧
    checkNat 2586 = true ∧
    checkNat 2587 = true ∧
    checkNat 2590 = true ∧
    checkNat 2591 = true ∧
    checkNat 2594 = true ∧
    checkNat 2595 = true ∧
    checkNat 2598 = true ∧
    checkNat 2599 = true ∧
    checkNat 2602 = true ∧
    checkNat 2603 = true ∧
    checkNat 2606 = true ∧
    checkNat 2607 = true ∧
    checkNat 2610 = true ∧
    checkNat 2611 = true ∧
    checkNat 2614 = true ∧
    checkNat 2615 = true ∧
    checkNat 2618 = true ∧
    checkNat 2619 = true ∧
    checkNat 2622 = true ∧
    checkNat 2623 = true ∧
    checkNat 3586 = true ∧
    checkNat 3590 = true ∧
    checkNat 3594 = true ∧
    checkNat 3598 = true ∧
    checkNat 3602 = true ∧
    checkNat 3606 = true ∧
    checkNat 3610 = true ∧
    checkNat 3614 = true ∧
    checkNat 3618 = true ∧
    checkNat 3622 = true ∧
    checkNat 3626 = true ∧
    checkNat 3630 = true ∧
    checkNat 3634 = true ∧
    checkNat 3638 = true ∧
    checkNat 3642 = true ∧
    checkNat 3646 = true := by
  exact ⟨case2562, case2563, case2566, case2567, case2570, case2571, case2574, case2575, case2578, case2579, case2582, case2583, case2586, case2587, case2590, case2591, case2594, case2595, case2598, case2599, case2602, case2603, case2606, case2607, case2610, case2611, case2614, case2615, case2618, case2619, case2622, case2623, case3586, case3590, case3594, case3598, case3602, case3606, case3610, case3614, case3618, case3622, case3626, case3630, case3634, case3638, case3642, case3646⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1792
