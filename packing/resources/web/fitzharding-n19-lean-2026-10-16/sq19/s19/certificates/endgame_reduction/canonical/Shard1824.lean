import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1824
open Sq19.Endgame.Reduction

theorem case2626 : checkNat 2626 = true := by native_decide
#print axioms case2626

theorem case3650 : checkNat 3650 = true := by
  apply check_of_normalize (Case.ofNat 3650)
  have he : (Case.ofNat 3650).normalize = Case.ofNat 2626 := by decide
  rw [he]
  exact case2626
#print axioms case3650

theorem case2627 : checkNat 2627 = true := by native_decide
#print axioms case2627

theorem case2630 : checkNat 2630 = true := by native_decide
#print axioms case2630

theorem case3654 : checkNat 3654 = true := by
  apply check_of_normalize (Case.ofNat 3654)
  have he : (Case.ofNat 3654).normalize = Case.ofNat 2630 := by decide
  rw [he]
  exact case2630
#print axioms case3654

theorem case2631 : checkNat 2631 = true := by native_decide
#print axioms case2631

theorem case2634 : checkNat 2634 = true := by native_decide
#print axioms case2634

theorem case3658 : checkNat 3658 = true := by
  apply check_of_normalize (Case.ofNat 3658)
  have he : (Case.ofNat 3658).normalize = Case.ofNat 2634 := by decide
  rw [he]
  exact case2634
#print axioms case3658

theorem case2635 : checkNat 2635 = true := by native_decide
#print axioms case2635

theorem case2638 : checkNat 2638 = true := by native_decide
#print axioms case2638

theorem case3662 : checkNat 3662 = true := by
  apply check_of_normalize (Case.ofNat 3662)
  have he : (Case.ofNat 3662).normalize = Case.ofNat 2638 := by decide
  rw [he]
  exact case2638
#print axioms case3662

theorem case2639 : checkNat 2639 = true := by native_decide
#print axioms case2639

theorem case2642 : checkNat 2642 = true := by native_decide
#print axioms case2642

theorem case3666 : checkNat 3666 = true := by
  apply check_of_normalize (Case.ofNat 3666)
  have he : (Case.ofNat 3666).normalize = Case.ofNat 2642 := by decide
  rw [he]
  exact case2642
#print axioms case3666

theorem case2643 : checkNat 2643 = true := by native_decide
#print axioms case2643

theorem case2646 : checkNat 2646 = true := by native_decide
#print axioms case2646

theorem case3670 : checkNat 3670 = true := by
  apply check_of_normalize (Case.ofNat 3670)
  have he : (Case.ofNat 3670).normalize = Case.ofNat 2646 := by decide
  rw [he]
  exact case2646
#print axioms case3670

theorem case2647 : checkNat 2647 = true := by native_decide
#print axioms case2647

theorem case2650 : checkNat 2650 = true := by native_decide
#print axioms case2650

theorem case3674 : checkNat 3674 = true := by
  apply check_of_normalize (Case.ofNat 3674)
  have he : (Case.ofNat 3674).normalize = Case.ofNat 2650 := by decide
  rw [he]
  exact case2650
#print axioms case3674

theorem case2651 : checkNat 2651 = true := by native_decide
#print axioms case2651

theorem case2654 : checkNat 2654 = true := by native_decide
#print axioms case2654

theorem case3678 : checkNat 3678 = true := by
  apply check_of_normalize (Case.ofNat 3678)
  have he : (Case.ofNat 3678).normalize = Case.ofNat 2654 := by decide
  rw [he]
  exact case2654
#print axioms case3678

theorem case2655 : checkNat 2655 = true := by native_decide
#print axioms case2655

theorem case2658 : checkNat 2658 = true := by native_decide
#print axioms case2658

theorem case3682 : checkNat 3682 = true := by
  apply check_of_normalize (Case.ofNat 3682)
  have he : (Case.ofNat 3682).normalize = Case.ofNat 2658 := by decide
  rw [he]
  exact case2658
#print axioms case3682

theorem case2659 : checkNat 2659 = true := by native_decide
#print axioms case2659

theorem case2662 : checkNat 2662 = true := by native_decide
#print axioms case2662

theorem case3686 : checkNat 3686 = true := by
  apply check_of_normalize (Case.ofNat 3686)
  have he : (Case.ofNat 3686).normalize = Case.ofNat 2662 := by decide
  rw [he]
  exact case2662
#print axioms case3686

theorem case2663 : checkNat 2663 = true := by native_decide
#print axioms case2663

theorem case2666 : checkNat 2666 = true := by native_decide
#print axioms case2666

theorem case3690 : checkNat 3690 = true := by
  apply check_of_normalize (Case.ofNat 3690)
  have he : (Case.ofNat 3690).normalize = Case.ofNat 2666 := by decide
  rw [he]
  exact case2666
#print axioms case3690

theorem case2667 : checkNat 2667 = true := by native_decide
#print axioms case2667

theorem case2670 : checkNat 2670 = true := by native_decide
#print axioms case2670

theorem case3694 : checkNat 3694 = true := by
  apply check_of_normalize (Case.ofNat 3694)
  have he : (Case.ofNat 3694).normalize = Case.ofNat 2670 := by decide
  rw [he]
  exact case2670
#print axioms case3694

theorem case2671 : checkNat 2671 = true := by native_decide
#print axioms case2671

theorem case2674 : checkNat 2674 = true := by native_decide
#print axioms case2674

theorem case3698 : checkNat 3698 = true := by
  apply check_of_normalize (Case.ofNat 3698)
  have he : (Case.ofNat 3698).normalize = Case.ofNat 2674 := by decide
  rw [he]
  exact case2674
#print axioms case3698

theorem case2675 : checkNat 2675 = true := by native_decide
#print axioms case2675

theorem case2678 : checkNat 2678 = true := by native_decide
#print axioms case2678

theorem case3702 : checkNat 3702 = true := by
  apply check_of_normalize (Case.ofNat 3702)
  have he : (Case.ofNat 3702).normalize = Case.ofNat 2678 := by decide
  rw [he]
  exact case2678
#print axioms case3702

theorem case2679 : checkNat 2679 = true := by native_decide
#print axioms case2679

theorem case2682 : checkNat 2682 = true := by native_decide
#print axioms case2682

theorem case3706 : checkNat 3706 = true := by
  apply check_of_normalize (Case.ofNat 3706)
  have he : (Case.ofNat 3706).normalize = Case.ofNat 2682 := by decide
  rw [he]
  exact case2682
#print axioms case3706

theorem case2683 : checkNat 2683 = true := by native_decide
#print axioms case2683

theorem case2686 : checkNat 2686 = true := by native_decide
#print axioms case2686

theorem case3710 : checkNat 3710 = true := by
  apply check_of_normalize (Case.ofNat 3710)
  have he : (Case.ofNat 3710).normalize = Case.ofNat 2686 := by decide
  rw [he]
  exact case2686
#print axioms case3710

theorem case2687 : checkNat 2687 = true := by native_decide
#print axioms case2687

theorem accepted :
    checkNat 2626 = true ∧
    checkNat 2627 = true ∧
    checkNat 2630 = true ∧
    checkNat 2631 = true ∧
    checkNat 2634 = true ∧
    checkNat 2635 = true ∧
    checkNat 2638 = true ∧
    checkNat 2639 = true ∧
    checkNat 2642 = true ∧
    checkNat 2643 = true ∧
    checkNat 2646 = true ∧
    checkNat 2647 = true ∧
    checkNat 2650 = true ∧
    checkNat 2651 = true ∧
    checkNat 2654 = true ∧
    checkNat 2655 = true ∧
    checkNat 2658 = true ∧
    checkNat 2659 = true ∧
    checkNat 2662 = true ∧
    checkNat 2663 = true ∧
    checkNat 2666 = true ∧
    checkNat 2667 = true ∧
    checkNat 2670 = true ∧
    checkNat 2671 = true ∧
    checkNat 2674 = true ∧
    checkNat 2675 = true ∧
    checkNat 2678 = true ∧
    checkNat 2679 = true ∧
    checkNat 2682 = true ∧
    checkNat 2683 = true ∧
    checkNat 2686 = true ∧
    checkNat 2687 = true ∧
    checkNat 3650 = true ∧
    checkNat 3654 = true ∧
    checkNat 3658 = true ∧
    checkNat 3662 = true ∧
    checkNat 3666 = true ∧
    checkNat 3670 = true ∧
    checkNat 3674 = true ∧
    checkNat 3678 = true ∧
    checkNat 3682 = true ∧
    checkNat 3686 = true ∧
    checkNat 3690 = true ∧
    checkNat 3694 = true ∧
    checkNat 3698 = true ∧
    checkNat 3702 = true ∧
    checkNat 3706 = true ∧
    checkNat 3710 = true := by
  exact ⟨case2626, case2627, case2630, case2631, case2634, case2635, case2638, case2639, case2642, case2643, case2646, case2647, case2650, case2651, case2654, case2655, case2658, case2659, case2662, case2663, case2666, case2667, case2670, case2671, case2674, case2675, case2678, case2679, case2682, case2683, case2686, case2687, case3650, case3654, case3658, case3662, case3666, case3670, case3674, case3678, case3682, case3686, case3690, case3694, case3698, case3702, case3706, case3710⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1824
