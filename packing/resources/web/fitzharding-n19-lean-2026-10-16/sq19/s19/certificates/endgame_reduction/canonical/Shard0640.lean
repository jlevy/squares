import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0640
open Sq19.Endgame.Reduction

theorem case0640 : checkNat 640 = true := by native_decide
#print axioms case0640

theorem case1664 : checkNat 1664 = true := by
  apply check_of_normalize (Case.ofNat 1664)
  have he : (Case.ofNat 1664).normalize = Case.ofNat 640 := by decide
  rw [he]
  exact case0640
#print axioms case1664

theorem case2688 : checkNat 2688 = true := by
  apply check_of_normalize (Case.ofNat 2688)
  have he : (Case.ofNat 2688).normalize = Case.ofNat 640 := by decide
  rw [he]
  exact case0640
#print axioms case2688

theorem case3712 : checkNat 3712 = true := by
  apply check_of_normalize (Case.ofNat 3712)
  have he : (Case.ofNat 3712).normalize = Case.ofNat 640 := by decide
  rw [he]
  exact case0640
#print axioms case3712

theorem case0641 : checkNat 641 = true := by native_decide
#print axioms case0641

theorem case2689 : checkNat 2689 = true := by
  apply check_of_normalize (Case.ofNat 2689)
  have he : (Case.ofNat 2689).normalize = Case.ofNat 641 := by decide
  rw [he]
  exact case0641
#print axioms case2689

theorem case0642 : checkNat 642 = true := by native_decide
#print axioms case0642

theorem case1666 : checkNat 1666 = true := by
  apply check_of_normalize (Case.ofNat 1666)
  have he : (Case.ofNat 1666).normalize = Case.ofNat 642 := by decide
  rw [he]
  exact case0642
#print axioms case1666

theorem case0643 : checkNat 643 = true := by native_decide
#print axioms case0643

theorem case0644 : checkNat 644 = true := by native_decide
#print axioms case0644

theorem case1668 : checkNat 1668 = true := by
  apply check_of_normalize (Case.ofNat 1668)
  have he : (Case.ofNat 1668).normalize = Case.ofNat 644 := by decide
  rw [he]
  exact case0644
#print axioms case1668

theorem case2692 : checkNat 2692 = true := by
  apply check_of_normalize (Case.ofNat 2692)
  have he : (Case.ofNat 2692).normalize = Case.ofNat 644 := by decide
  rw [he]
  exact case0644
#print axioms case2692

theorem case3716 : checkNat 3716 = true := by
  apply check_of_normalize (Case.ofNat 3716)
  have he : (Case.ofNat 3716).normalize = Case.ofNat 644 := by decide
  rw [he]
  exact case0644
#print axioms case3716

theorem case0645 : checkNat 645 = true := by native_decide
#print axioms case0645

theorem case2693 : checkNat 2693 = true := by
  apply check_of_normalize (Case.ofNat 2693)
  have he : (Case.ofNat 2693).normalize = Case.ofNat 645 := by decide
  rw [he]
  exact case0645
#print axioms case2693

theorem case0646 : checkNat 646 = true := by native_decide
#print axioms case0646

theorem case1670 : checkNat 1670 = true := by
  apply check_of_normalize (Case.ofNat 1670)
  have he : (Case.ofNat 1670).normalize = Case.ofNat 646 := by decide
  rw [he]
  exact case0646
#print axioms case1670

theorem case0647 : checkNat 647 = true := by native_decide
#print axioms case0647

theorem case0648 : checkNat 648 = true := by native_decide
#print axioms case0648

theorem case1672 : checkNat 1672 = true := by
  apply check_of_normalize (Case.ofNat 1672)
  have he : (Case.ofNat 1672).normalize = Case.ofNat 648 := by decide
  rw [he]
  exact case0648
#print axioms case1672

theorem case2696 : checkNat 2696 = true := by
  apply check_of_normalize (Case.ofNat 2696)
  have he : (Case.ofNat 2696).normalize = Case.ofNat 648 := by decide
  rw [he]
  exact case0648
#print axioms case2696

theorem case3720 : checkNat 3720 = true := by
  apply check_of_normalize (Case.ofNat 3720)
  have he : (Case.ofNat 3720).normalize = Case.ofNat 648 := by decide
  rw [he]
  exact case0648
#print axioms case3720

theorem case0649 : checkNat 649 = true := by native_decide
#print axioms case0649

theorem case2697 : checkNat 2697 = true := by
  apply check_of_normalize (Case.ofNat 2697)
  have he : (Case.ofNat 2697).normalize = Case.ofNat 649 := by decide
  rw [he]
  exact case0649
#print axioms case2697

theorem case0650 : checkNat 650 = true := by native_decide
#print axioms case0650

theorem case1674 : checkNat 1674 = true := by
  apply check_of_normalize (Case.ofNat 1674)
  have he : (Case.ofNat 1674).normalize = Case.ofNat 650 := by decide
  rw [he]
  exact case0650
#print axioms case1674

theorem case0651 : checkNat 651 = true := by native_decide
#print axioms case0651

theorem case0652 : checkNat 652 = true := by native_decide
#print axioms case0652

theorem case1676 : checkNat 1676 = true := by
  apply check_of_normalize (Case.ofNat 1676)
  have he : (Case.ofNat 1676).normalize = Case.ofNat 652 := by decide
  rw [he]
  exact case0652
#print axioms case1676

theorem case2700 : checkNat 2700 = true := by
  apply check_of_normalize (Case.ofNat 2700)
  have he : (Case.ofNat 2700).normalize = Case.ofNat 652 := by decide
  rw [he]
  exact case0652
#print axioms case2700

theorem case3724 : checkNat 3724 = true := by
  apply check_of_normalize (Case.ofNat 3724)
  have he : (Case.ofNat 3724).normalize = Case.ofNat 652 := by decide
  rw [he]
  exact case0652
#print axioms case3724

theorem case0653 : checkNat 653 = true := by native_decide
#print axioms case0653

theorem case2701 : checkNat 2701 = true := by
  apply check_of_normalize (Case.ofNat 2701)
  have he : (Case.ofNat 2701).normalize = Case.ofNat 653 := by decide
  rw [he]
  exact case0653
#print axioms case2701

theorem case0654 : checkNat 654 = true := by native_decide
#print axioms case0654

theorem case1678 : checkNat 1678 = true := by
  apply check_of_normalize (Case.ofNat 1678)
  have he : (Case.ofNat 1678).normalize = Case.ofNat 654 := by decide
  rw [he]
  exact case0654
#print axioms case1678

theorem case0655 : checkNat 655 = true := by native_decide
#print axioms case0655

theorem case0656 : checkNat 656 = true := by native_decide
#print axioms case0656

theorem case1680 : checkNat 1680 = true := by
  apply check_of_normalize (Case.ofNat 1680)
  have he : (Case.ofNat 1680).normalize = Case.ofNat 656 := by decide
  rw [he]
  exact case0656
#print axioms case1680

theorem case2704 : checkNat 2704 = true := by
  apply check_of_normalize (Case.ofNat 2704)
  have he : (Case.ofNat 2704).normalize = Case.ofNat 656 := by decide
  rw [he]
  exact case0656
#print axioms case2704

theorem case3728 : checkNat 3728 = true := by
  apply check_of_normalize (Case.ofNat 3728)
  have he : (Case.ofNat 3728).normalize = Case.ofNat 656 := by decide
  rw [he]
  exact case0656
#print axioms case3728

theorem case0657 : checkNat 657 = true := by native_decide
#print axioms case0657

theorem case2705 : checkNat 2705 = true := by
  apply check_of_normalize (Case.ofNat 2705)
  have he : (Case.ofNat 2705).normalize = Case.ofNat 657 := by decide
  rw [he]
  exact case0657
#print axioms case2705

theorem case0658 : checkNat 658 = true := by native_decide
#print axioms case0658

theorem case1682 : checkNat 1682 = true := by
  apply check_of_normalize (Case.ofNat 1682)
  have he : (Case.ofNat 1682).normalize = Case.ofNat 658 := by decide
  rw [he]
  exact case0658
#print axioms case1682

theorem case0659 : checkNat 659 = true := by native_decide
#print axioms case0659

theorem case0660 : checkNat 660 = true := by native_decide
#print axioms case0660

theorem case1684 : checkNat 1684 = true := by
  apply check_of_normalize (Case.ofNat 1684)
  have he : (Case.ofNat 1684).normalize = Case.ofNat 660 := by decide
  rw [he]
  exact case0660
#print axioms case1684

theorem case2708 : checkNat 2708 = true := by
  apply check_of_normalize (Case.ofNat 2708)
  have he : (Case.ofNat 2708).normalize = Case.ofNat 660 := by decide
  rw [he]
  exact case0660
#print axioms case2708

theorem case3732 : checkNat 3732 = true := by
  apply check_of_normalize (Case.ofNat 3732)
  have he : (Case.ofNat 3732).normalize = Case.ofNat 660 := by decide
  rw [he]
  exact case0660
#print axioms case3732

theorem case0661 : checkNat 661 = true := by native_decide
#print axioms case0661

theorem case2709 : checkNat 2709 = true := by
  apply check_of_normalize (Case.ofNat 2709)
  have he : (Case.ofNat 2709).normalize = Case.ofNat 661 := by decide
  rw [he]
  exact case0661
#print axioms case2709

theorem case0662 : checkNat 662 = true := by native_decide
#print axioms case0662

theorem case1686 : checkNat 1686 = true := by
  apply check_of_normalize (Case.ofNat 1686)
  have he : (Case.ofNat 1686).normalize = Case.ofNat 662 := by decide
  rw [he]
  exact case0662
#print axioms case1686

theorem case0663 : checkNat 663 = true := by native_decide
#print axioms case0663

theorem case0664 : checkNat 664 = true := by native_decide
#print axioms case0664

theorem case1688 : checkNat 1688 = true := by
  apply check_of_normalize (Case.ofNat 1688)
  have he : (Case.ofNat 1688).normalize = Case.ofNat 664 := by decide
  rw [he]
  exact case0664
#print axioms case1688

theorem case2712 : checkNat 2712 = true := by
  apply check_of_normalize (Case.ofNat 2712)
  have he : (Case.ofNat 2712).normalize = Case.ofNat 664 := by decide
  rw [he]
  exact case0664
#print axioms case2712

theorem case3736 : checkNat 3736 = true := by
  apply check_of_normalize (Case.ofNat 3736)
  have he : (Case.ofNat 3736).normalize = Case.ofNat 664 := by decide
  rw [he]
  exact case0664
#print axioms case3736

theorem case0665 : checkNat 665 = true := by native_decide
#print axioms case0665

theorem case2713 : checkNat 2713 = true := by
  apply check_of_normalize (Case.ofNat 2713)
  have he : (Case.ofNat 2713).normalize = Case.ofNat 665 := by decide
  rw [he]
  exact case0665
#print axioms case2713

theorem case0666 : checkNat 666 = true := by native_decide
#print axioms case0666

theorem case1690 : checkNat 1690 = true := by
  apply check_of_normalize (Case.ofNat 1690)
  have he : (Case.ofNat 1690).normalize = Case.ofNat 666 := by decide
  rw [he]
  exact case0666
#print axioms case1690

theorem case0667 : checkNat 667 = true := by native_decide
#print axioms case0667

theorem case0668 : checkNat 668 = true := by native_decide
#print axioms case0668

theorem case1692 : checkNat 1692 = true := by
  apply check_of_normalize (Case.ofNat 1692)
  have he : (Case.ofNat 1692).normalize = Case.ofNat 668 := by decide
  rw [he]
  exact case0668
#print axioms case1692

theorem case2716 : checkNat 2716 = true := by
  apply check_of_normalize (Case.ofNat 2716)
  have he : (Case.ofNat 2716).normalize = Case.ofNat 668 := by decide
  rw [he]
  exact case0668
#print axioms case2716

theorem case3740 : checkNat 3740 = true := by
  apply check_of_normalize (Case.ofNat 3740)
  have he : (Case.ofNat 3740).normalize = Case.ofNat 668 := by decide
  rw [he]
  exact case0668
#print axioms case3740

theorem case0669 : checkNat 669 = true := by native_decide
#print axioms case0669

theorem case2717 : checkNat 2717 = true := by
  apply check_of_normalize (Case.ofNat 2717)
  have he : (Case.ofNat 2717).normalize = Case.ofNat 669 := by decide
  rw [he]
  exact case0669
#print axioms case2717

theorem case0670 : checkNat 670 = true := by native_decide
#print axioms case0670

theorem case1694 : checkNat 1694 = true := by
  apply check_of_normalize (Case.ofNat 1694)
  have he : (Case.ofNat 1694).normalize = Case.ofNat 670 := by decide
  rw [he]
  exact case0670
#print axioms case1694

theorem case0671 : checkNat 671 = true := by native_decide
#print axioms case0671

theorem accepted :
    checkNat 640 = true ∧
    checkNat 641 = true ∧
    checkNat 642 = true ∧
    checkNat 643 = true ∧
    checkNat 644 = true ∧
    checkNat 645 = true ∧
    checkNat 646 = true ∧
    checkNat 647 = true ∧
    checkNat 648 = true ∧
    checkNat 649 = true ∧
    checkNat 650 = true ∧
    checkNat 651 = true ∧
    checkNat 652 = true ∧
    checkNat 653 = true ∧
    checkNat 654 = true ∧
    checkNat 655 = true ∧
    checkNat 656 = true ∧
    checkNat 657 = true ∧
    checkNat 658 = true ∧
    checkNat 659 = true ∧
    checkNat 660 = true ∧
    checkNat 661 = true ∧
    checkNat 662 = true ∧
    checkNat 663 = true ∧
    checkNat 664 = true ∧
    checkNat 665 = true ∧
    checkNat 666 = true ∧
    checkNat 667 = true ∧
    checkNat 668 = true ∧
    checkNat 669 = true ∧
    checkNat 670 = true ∧
    checkNat 671 = true ∧
    checkNat 1664 = true ∧
    checkNat 1666 = true ∧
    checkNat 1668 = true ∧
    checkNat 1670 = true ∧
    checkNat 1672 = true ∧
    checkNat 1674 = true ∧
    checkNat 1676 = true ∧
    checkNat 1678 = true ∧
    checkNat 1680 = true ∧
    checkNat 1682 = true ∧
    checkNat 1684 = true ∧
    checkNat 1686 = true ∧
    checkNat 1688 = true ∧
    checkNat 1690 = true ∧
    checkNat 1692 = true ∧
    checkNat 1694 = true ∧
    checkNat 2688 = true ∧
    checkNat 2689 = true ∧
    checkNat 2692 = true ∧
    checkNat 2693 = true ∧
    checkNat 2696 = true ∧
    checkNat 2697 = true ∧
    checkNat 2700 = true ∧
    checkNat 2701 = true ∧
    checkNat 2704 = true ∧
    checkNat 2705 = true ∧
    checkNat 2708 = true ∧
    checkNat 2709 = true ∧
    checkNat 2712 = true ∧
    checkNat 2713 = true ∧
    checkNat 2716 = true ∧
    checkNat 2717 = true ∧
    checkNat 3712 = true ∧
    checkNat 3716 = true ∧
    checkNat 3720 = true ∧
    checkNat 3724 = true ∧
    checkNat 3728 = true ∧
    checkNat 3732 = true ∧
    checkNat 3736 = true ∧
    checkNat 3740 = true := by
  exact ⟨case0640, case0641, case0642, case0643, case0644, case0645, case0646, case0647, case0648, case0649, case0650, case0651, case0652, case0653, case0654, case0655, case0656, case0657, case0658, case0659, case0660, case0661, case0662, case0663, case0664, case0665, case0666, case0667, case0668, case0669, case0670, case0671, case1664, case1666, case1668, case1670, case1672, case1674, case1676, case1678, case1680, case1682, case1684, case1686, case1688, case1690, case1692, case1694, case2688, case2689, case2692, case2693, case2696, case2697, case2700, case2701, case2704, case2705, case2708, case2709, case2712, case2713, case2716, case2717, case3712, case3716, case3720, case3724, case3728, case3732, case3736, case3740⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0640
