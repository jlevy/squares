import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard1888
open Sq19.Endgame.Reduction

theorem case2754 : checkNat 2754 = true := by native_decide
#print axioms case2754

theorem case3778 : checkNat 3778 = true := by
  apply check_of_normalize (Case.ofNat 3778)
  have he : (Case.ofNat 3778).normalize = Case.ofNat 2754 := by decide
  rw [he]
  exact case2754
#print axioms case3778

theorem case2755 : checkNat 2755 = true := by native_decide
#print axioms case2755

theorem case2758 : checkNat 2758 = true := by native_decide
#print axioms case2758

theorem case3782 : checkNat 3782 = true := by
  apply check_of_normalize (Case.ofNat 3782)
  have he : (Case.ofNat 3782).normalize = Case.ofNat 2758 := by decide
  rw [he]
  exact case2758
#print axioms case3782

theorem case2759 : checkNat 2759 = true := by native_decide
#print axioms case2759

theorem case2762 : checkNat 2762 = true := by native_decide
#print axioms case2762

theorem case3786 : checkNat 3786 = true := by
  apply check_of_normalize (Case.ofNat 3786)
  have he : (Case.ofNat 3786).normalize = Case.ofNat 2762 := by decide
  rw [he]
  exact case2762
#print axioms case3786

theorem case2763 : checkNat 2763 = true := by native_decide
#print axioms case2763

theorem case2766 : checkNat 2766 = true := by native_decide
#print axioms case2766

theorem case3790 : checkNat 3790 = true := by
  apply check_of_normalize (Case.ofNat 3790)
  have he : (Case.ofNat 3790).normalize = Case.ofNat 2766 := by decide
  rw [he]
  exact case2766
#print axioms case3790

theorem case2767 : checkNat 2767 = true := by native_decide
#print axioms case2767

theorem case2770 : checkNat 2770 = true := by native_decide
#print axioms case2770

theorem case3794 : checkNat 3794 = true := by
  apply check_of_normalize (Case.ofNat 3794)
  have he : (Case.ofNat 3794).normalize = Case.ofNat 2770 := by decide
  rw [he]
  exact case2770
#print axioms case3794

theorem case2771 : checkNat 2771 = true := by native_decide
#print axioms case2771

theorem case2774 : checkNat 2774 = true := by native_decide
#print axioms case2774

theorem case3798 : checkNat 3798 = true := by
  apply check_of_normalize (Case.ofNat 3798)
  have he : (Case.ofNat 3798).normalize = Case.ofNat 2774 := by decide
  rw [he]
  exact case2774
#print axioms case3798

theorem case2775 : checkNat 2775 = true := by native_decide
#print axioms case2775

theorem case2778 : checkNat 2778 = true := by native_decide
#print axioms case2778

theorem case3802 : checkNat 3802 = true := by
  apply check_of_normalize (Case.ofNat 3802)
  have he : (Case.ofNat 3802).normalize = Case.ofNat 2778 := by decide
  rw [he]
  exact case2778
#print axioms case3802

theorem case2779 : checkNat 2779 = true := by native_decide
#print axioms case2779

theorem case2782 : checkNat 2782 = true := by native_decide
#print axioms case2782

theorem case3806 : checkNat 3806 = true := by
  apply check_of_normalize (Case.ofNat 3806)
  have he : (Case.ofNat 3806).normalize = Case.ofNat 2782 := by decide
  rw [he]
  exact case2782
#print axioms case3806

theorem case2783 : checkNat 2783 = true := by native_decide
#print axioms case2783

theorem case2786 : checkNat 2786 = true := by native_decide
#print axioms case2786

theorem case3810 : checkNat 3810 = true := by
  apply check_of_normalize (Case.ofNat 3810)
  have he : (Case.ofNat 3810).normalize = Case.ofNat 2786 := by decide
  rw [he]
  exact case2786
#print axioms case3810

theorem case2787 : checkNat 2787 = true := by native_decide
#print axioms case2787

theorem case2790 : checkNat 2790 = true := by native_decide
#print axioms case2790

theorem case3814 : checkNat 3814 = true := by
  apply check_of_normalize (Case.ofNat 3814)
  have he : (Case.ofNat 3814).normalize = Case.ofNat 2790 := by decide
  rw [he]
  exact case2790
#print axioms case3814

theorem case2791 : checkNat 2791 = true := by native_decide
#print axioms case2791

theorem case2794 : checkNat 2794 = true := by native_decide
#print axioms case2794

theorem case3818 : checkNat 3818 = true := by
  apply check_of_normalize (Case.ofNat 3818)
  have he : (Case.ofNat 3818).normalize = Case.ofNat 2794 := by decide
  rw [he]
  exact case2794
#print axioms case3818

theorem case2795 : checkNat 2795 = true := by native_decide
#print axioms case2795

theorem case2798 : checkNat 2798 = true := by native_decide
#print axioms case2798

theorem case3822 : checkNat 3822 = true := by
  apply check_of_normalize (Case.ofNat 3822)
  have he : (Case.ofNat 3822).normalize = Case.ofNat 2798 := by decide
  rw [he]
  exact case2798
#print axioms case3822

theorem case2799 : checkNat 2799 = true := by native_decide
#print axioms case2799

theorem case2802 : checkNat 2802 = true := by native_decide
#print axioms case2802

theorem case3826 : checkNat 3826 = true := by
  apply check_of_normalize (Case.ofNat 3826)
  have he : (Case.ofNat 3826).normalize = Case.ofNat 2802 := by decide
  rw [he]
  exact case2802
#print axioms case3826

theorem case2803 : checkNat 2803 = true := by native_decide
#print axioms case2803

theorem case2806 : checkNat 2806 = true := by native_decide
#print axioms case2806

theorem case3830 : checkNat 3830 = true := by
  apply check_of_normalize (Case.ofNat 3830)
  have he : (Case.ofNat 3830).normalize = Case.ofNat 2806 := by decide
  rw [he]
  exact case2806
#print axioms case3830

theorem case2807 : checkNat 2807 = true := by native_decide
#print axioms case2807

theorem case2810 : checkNat 2810 = true := by native_decide
#print axioms case2810

theorem case3834 : checkNat 3834 = true := by
  apply check_of_normalize (Case.ofNat 3834)
  have he : (Case.ofNat 3834).normalize = Case.ofNat 2810 := by decide
  rw [he]
  exact case2810
#print axioms case3834

theorem case2811 : checkNat 2811 = true := by native_decide
#print axioms case2811

theorem case2814 : checkNat 2814 = true := by native_decide
#print axioms case2814

theorem case3838 : checkNat 3838 = true := by
  apply check_of_normalize (Case.ofNat 3838)
  have he : (Case.ofNat 3838).normalize = Case.ofNat 2814 := by decide
  rw [he]
  exact case2814
#print axioms case3838

theorem case2815 : checkNat 2815 = true := by native_decide
#print axioms case2815

theorem accepted :
    checkNat 2754 = true ∧
    checkNat 2755 = true ∧
    checkNat 2758 = true ∧
    checkNat 2759 = true ∧
    checkNat 2762 = true ∧
    checkNat 2763 = true ∧
    checkNat 2766 = true ∧
    checkNat 2767 = true ∧
    checkNat 2770 = true ∧
    checkNat 2771 = true ∧
    checkNat 2774 = true ∧
    checkNat 2775 = true ∧
    checkNat 2778 = true ∧
    checkNat 2779 = true ∧
    checkNat 2782 = true ∧
    checkNat 2783 = true ∧
    checkNat 2786 = true ∧
    checkNat 2787 = true ∧
    checkNat 2790 = true ∧
    checkNat 2791 = true ∧
    checkNat 2794 = true ∧
    checkNat 2795 = true ∧
    checkNat 2798 = true ∧
    checkNat 2799 = true ∧
    checkNat 2802 = true ∧
    checkNat 2803 = true ∧
    checkNat 2806 = true ∧
    checkNat 2807 = true ∧
    checkNat 2810 = true ∧
    checkNat 2811 = true ∧
    checkNat 2814 = true ∧
    checkNat 2815 = true ∧
    checkNat 3778 = true ∧
    checkNat 3782 = true ∧
    checkNat 3786 = true ∧
    checkNat 3790 = true ∧
    checkNat 3794 = true ∧
    checkNat 3798 = true ∧
    checkNat 3802 = true ∧
    checkNat 3806 = true ∧
    checkNat 3810 = true ∧
    checkNat 3814 = true ∧
    checkNat 3818 = true ∧
    checkNat 3822 = true ∧
    checkNat 3826 = true ∧
    checkNat 3830 = true ∧
    checkNat 3834 = true ∧
    checkNat 3838 = true := by
  exact ⟨case2754, case2755, case2758, case2759, case2762, case2763, case2766, case2767, case2770, case2771, case2774, case2775, case2778, case2779, case2782, case2783, case2786, case2787, case2790, case2791, case2794, case2795, case2798, case2799, case2802, case2803, case2806, case2807, case2810, case2811, case2814, case2815, case3778, case3782, case3786, case3790, case3794, case3798, case3802, case3806, case3810, case3814, case3818, case3822, case3826, case3830, case3834, case3838⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard1888
