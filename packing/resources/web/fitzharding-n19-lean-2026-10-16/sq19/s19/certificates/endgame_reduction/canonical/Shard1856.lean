import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1856
open Sq19.Endgame.Reduction

theorem case2690 : checkNat 2690 = true := by native_decide
#print axioms case2690

theorem case3714 : checkNat 3714 = true := by
  apply check_of_normalize (Case.ofNat 3714)
  have he : (Case.ofNat 3714).normalize = Case.ofNat 2690 := by decide
  rw [he]
  exact case2690
#print axioms case3714

theorem case2691 : checkNat 2691 = true := by native_decide
#print axioms case2691

theorem case2694 : checkNat 2694 = true := by native_decide
#print axioms case2694

theorem case3718 : checkNat 3718 = true := by
  apply check_of_normalize (Case.ofNat 3718)
  have he : (Case.ofNat 3718).normalize = Case.ofNat 2694 := by decide
  rw [he]
  exact case2694
#print axioms case3718

theorem case2695 : checkNat 2695 = true := by native_decide
#print axioms case2695

theorem case2698 : checkNat 2698 = true := by native_decide
#print axioms case2698

theorem case3722 : checkNat 3722 = true := by
  apply check_of_normalize (Case.ofNat 3722)
  have he : (Case.ofNat 3722).normalize = Case.ofNat 2698 := by decide
  rw [he]
  exact case2698
#print axioms case3722

theorem case2699 : checkNat 2699 = true := by native_decide
#print axioms case2699

theorem case2702 : checkNat 2702 = true := by native_decide
#print axioms case2702

theorem case3726 : checkNat 3726 = true := by
  apply check_of_normalize (Case.ofNat 3726)
  have he : (Case.ofNat 3726).normalize = Case.ofNat 2702 := by decide
  rw [he]
  exact case2702
#print axioms case3726

theorem case2703 : checkNat 2703 = true := by native_decide
#print axioms case2703

theorem case2706 : checkNat 2706 = true := by native_decide
#print axioms case2706

theorem case3730 : checkNat 3730 = true := by
  apply check_of_normalize (Case.ofNat 3730)
  have he : (Case.ofNat 3730).normalize = Case.ofNat 2706 := by decide
  rw [he]
  exact case2706
#print axioms case3730

theorem case2707 : checkNat 2707 = true := by native_decide
#print axioms case2707

theorem case2710 : checkNat 2710 = true := by native_decide
#print axioms case2710

theorem case3734 : checkNat 3734 = true := by
  apply check_of_normalize (Case.ofNat 3734)
  have he : (Case.ofNat 3734).normalize = Case.ofNat 2710 := by decide
  rw [he]
  exact case2710
#print axioms case3734

theorem case2711 : checkNat 2711 = true := by native_decide
#print axioms case2711

theorem case2714 : checkNat 2714 = true := by native_decide
#print axioms case2714

theorem case3738 : checkNat 3738 = true := by
  apply check_of_normalize (Case.ofNat 3738)
  have he : (Case.ofNat 3738).normalize = Case.ofNat 2714 := by decide
  rw [he]
  exact case2714
#print axioms case3738

theorem case2715 : checkNat 2715 = true := by native_decide
#print axioms case2715

theorem case2718 : checkNat 2718 = true := by native_decide
#print axioms case2718

theorem case3742 : checkNat 3742 = true := by
  apply check_of_normalize (Case.ofNat 3742)
  have he : (Case.ofNat 3742).normalize = Case.ofNat 2718 := by decide
  rw [he]
  exact case2718
#print axioms case3742

theorem case2719 : checkNat 2719 = true := by native_decide
#print axioms case2719

theorem case2722 : checkNat 2722 = true := by native_decide
#print axioms case2722

theorem case3746 : checkNat 3746 = true := by
  apply check_of_normalize (Case.ofNat 3746)
  have he : (Case.ofNat 3746).normalize = Case.ofNat 2722 := by decide
  rw [he]
  exact case2722
#print axioms case3746

theorem case2723 : checkNat 2723 = true := by native_decide
#print axioms case2723

theorem case2726 : checkNat 2726 = true := by native_decide
#print axioms case2726

theorem case3750 : checkNat 3750 = true := by
  apply check_of_normalize (Case.ofNat 3750)
  have he : (Case.ofNat 3750).normalize = Case.ofNat 2726 := by decide
  rw [he]
  exact case2726
#print axioms case3750

theorem case2727 : checkNat 2727 = true := by native_decide
#print axioms case2727

theorem case2730 : checkNat 2730 = true := by native_decide
#print axioms case2730

theorem case3754 : checkNat 3754 = true := by
  apply check_of_normalize (Case.ofNat 3754)
  have he : (Case.ofNat 3754).normalize = Case.ofNat 2730 := by decide
  rw [he]
  exact case2730
#print axioms case3754

theorem case2731 : checkNat 2731 = true := by native_decide
#print axioms case2731

theorem case2734 : checkNat 2734 = true := by native_decide
#print axioms case2734

theorem case3758 : checkNat 3758 = true := by
  apply check_of_normalize (Case.ofNat 3758)
  have he : (Case.ofNat 3758).normalize = Case.ofNat 2734 := by decide
  rw [he]
  exact case2734
#print axioms case3758

theorem case2735 : checkNat 2735 = true := by native_decide
#print axioms case2735

theorem case2738 : checkNat 2738 = true := by native_decide
#print axioms case2738

theorem case3762 : checkNat 3762 = true := by
  apply check_of_normalize (Case.ofNat 3762)
  have he : (Case.ofNat 3762).normalize = Case.ofNat 2738 := by decide
  rw [he]
  exact case2738
#print axioms case3762

theorem case2739 : checkNat 2739 = true := by native_decide
#print axioms case2739

theorem case2742 : checkNat 2742 = true := by native_decide
#print axioms case2742

theorem case3766 : checkNat 3766 = true := by
  apply check_of_normalize (Case.ofNat 3766)
  have he : (Case.ofNat 3766).normalize = Case.ofNat 2742 := by decide
  rw [he]
  exact case2742
#print axioms case3766

theorem case2743 : checkNat 2743 = true := by native_decide
#print axioms case2743

theorem case2746 : checkNat 2746 = true := by native_decide
#print axioms case2746

theorem case3770 : checkNat 3770 = true := by
  apply check_of_normalize (Case.ofNat 3770)
  have he : (Case.ofNat 3770).normalize = Case.ofNat 2746 := by decide
  rw [he]
  exact case2746
#print axioms case3770

theorem case2747 : checkNat 2747 = true := by native_decide
#print axioms case2747

theorem case2750 : checkNat 2750 = true := by native_decide
#print axioms case2750

theorem case3774 : checkNat 3774 = true := by
  apply check_of_normalize (Case.ofNat 3774)
  have he : (Case.ofNat 3774).normalize = Case.ofNat 2750 := by decide
  rw [he]
  exact case2750
#print axioms case3774

theorem case2751 : checkNat 2751 = true := by native_decide
#print axioms case2751

theorem accepted :
    checkNat 2690 = true ∧
    checkNat 2691 = true ∧
    checkNat 2694 = true ∧
    checkNat 2695 = true ∧
    checkNat 2698 = true ∧
    checkNat 2699 = true ∧
    checkNat 2702 = true ∧
    checkNat 2703 = true ∧
    checkNat 2706 = true ∧
    checkNat 2707 = true ∧
    checkNat 2710 = true ∧
    checkNat 2711 = true ∧
    checkNat 2714 = true ∧
    checkNat 2715 = true ∧
    checkNat 2718 = true ∧
    checkNat 2719 = true ∧
    checkNat 2722 = true ∧
    checkNat 2723 = true ∧
    checkNat 2726 = true ∧
    checkNat 2727 = true ∧
    checkNat 2730 = true ∧
    checkNat 2731 = true ∧
    checkNat 2734 = true ∧
    checkNat 2735 = true ∧
    checkNat 2738 = true ∧
    checkNat 2739 = true ∧
    checkNat 2742 = true ∧
    checkNat 2743 = true ∧
    checkNat 2746 = true ∧
    checkNat 2747 = true ∧
    checkNat 2750 = true ∧
    checkNat 2751 = true ∧
    checkNat 3714 = true ∧
    checkNat 3718 = true ∧
    checkNat 3722 = true ∧
    checkNat 3726 = true ∧
    checkNat 3730 = true ∧
    checkNat 3734 = true ∧
    checkNat 3738 = true ∧
    checkNat 3742 = true ∧
    checkNat 3746 = true ∧
    checkNat 3750 = true ∧
    checkNat 3754 = true ∧
    checkNat 3758 = true ∧
    checkNat 3762 = true ∧
    checkNat 3766 = true ∧
    checkNat 3770 = true ∧
    checkNat 3774 = true := by
  exact ⟨case2690, case2691, case2694, case2695, case2698, case2699, case2702, case2703, case2706, case2707, case2710, case2711, case2714, case2715, case2718, case2719, case2722, case2723, case2726, case2727, case2730, case2731, case2734, case2735, case2738, case2739, case2742, case2743, case2746, case2747, case2750, case2751, case3714, case3718, case3722, case3726, case3730, case3734, case3738, case3742, case3746, case3750, case3754, case3758, case3762, case3766, case3770, case3774⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1856
