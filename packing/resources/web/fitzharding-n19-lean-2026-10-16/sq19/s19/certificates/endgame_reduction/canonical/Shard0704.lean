import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0704
open Sq19.Endgame.Reduction

theorem case0704 : checkNat 704 = true := by native_decide
#print axioms case0704

theorem case1728 : checkNat 1728 = true := by
  apply check_of_normalize (Case.ofNat 1728)
  have he : (Case.ofNat 1728).normalize = Case.ofNat 704 := by decide
  rw [he]
  exact case0704
#print axioms case1728

theorem case2752 : checkNat 2752 = true := by
  apply check_of_normalize (Case.ofNat 2752)
  have he : (Case.ofNat 2752).normalize = Case.ofNat 704 := by decide
  rw [he]
  exact case0704
#print axioms case2752

theorem case3776 : checkNat 3776 = true := by
  apply check_of_normalize (Case.ofNat 3776)
  have he : (Case.ofNat 3776).normalize = Case.ofNat 704 := by decide
  rw [he]
  exact case0704
#print axioms case3776

theorem case0705 : checkNat 705 = true := by native_decide
#print axioms case0705

theorem case2753 : checkNat 2753 = true := by
  apply check_of_normalize (Case.ofNat 2753)
  have he : (Case.ofNat 2753).normalize = Case.ofNat 705 := by decide
  rw [he]
  exact case0705
#print axioms case2753

theorem case0706 : checkNat 706 = true := by native_decide
#print axioms case0706

theorem case1730 : checkNat 1730 = true := by
  apply check_of_normalize (Case.ofNat 1730)
  have he : (Case.ofNat 1730).normalize = Case.ofNat 706 := by decide
  rw [he]
  exact case0706
#print axioms case1730

theorem case0707 : checkNat 707 = true := by native_decide
#print axioms case0707

theorem case0708 : checkNat 708 = true := by native_decide
#print axioms case0708

theorem case1732 : checkNat 1732 = true := by
  apply check_of_normalize (Case.ofNat 1732)
  have he : (Case.ofNat 1732).normalize = Case.ofNat 708 := by decide
  rw [he]
  exact case0708
#print axioms case1732

theorem case2756 : checkNat 2756 = true := by
  apply check_of_normalize (Case.ofNat 2756)
  have he : (Case.ofNat 2756).normalize = Case.ofNat 708 := by decide
  rw [he]
  exact case0708
#print axioms case2756

theorem case3780 : checkNat 3780 = true := by
  apply check_of_normalize (Case.ofNat 3780)
  have he : (Case.ofNat 3780).normalize = Case.ofNat 708 := by decide
  rw [he]
  exact case0708
#print axioms case3780

theorem case0709 : checkNat 709 = true := by native_decide
#print axioms case0709

theorem case2757 : checkNat 2757 = true := by
  apply check_of_normalize (Case.ofNat 2757)
  have he : (Case.ofNat 2757).normalize = Case.ofNat 709 := by decide
  rw [he]
  exact case0709
#print axioms case2757

theorem case0710 : checkNat 710 = true := by native_decide
#print axioms case0710

theorem case1734 : checkNat 1734 = true := by
  apply check_of_normalize (Case.ofNat 1734)
  have he : (Case.ofNat 1734).normalize = Case.ofNat 710 := by decide
  rw [he]
  exact case0710
#print axioms case1734

theorem case0711 : checkNat 711 = true := by native_decide
#print axioms case0711

theorem case0712 : checkNat 712 = true := by native_decide
#print axioms case0712

theorem case1736 : checkNat 1736 = true := by
  apply check_of_normalize (Case.ofNat 1736)
  have he : (Case.ofNat 1736).normalize = Case.ofNat 712 := by decide
  rw [he]
  exact case0712
#print axioms case1736

theorem case2760 : checkNat 2760 = true := by
  apply check_of_normalize (Case.ofNat 2760)
  have he : (Case.ofNat 2760).normalize = Case.ofNat 712 := by decide
  rw [he]
  exact case0712
#print axioms case2760

theorem case3784 : checkNat 3784 = true := by
  apply check_of_normalize (Case.ofNat 3784)
  have he : (Case.ofNat 3784).normalize = Case.ofNat 712 := by decide
  rw [he]
  exact case0712
#print axioms case3784

theorem case0713 : checkNat 713 = true := by native_decide
#print axioms case0713

theorem case2761 : checkNat 2761 = true := by
  apply check_of_normalize (Case.ofNat 2761)
  have he : (Case.ofNat 2761).normalize = Case.ofNat 713 := by decide
  rw [he]
  exact case0713
#print axioms case2761

theorem case0714 : checkNat 714 = true := by native_decide
#print axioms case0714

theorem case1738 : checkNat 1738 = true := by
  apply check_of_normalize (Case.ofNat 1738)
  have he : (Case.ofNat 1738).normalize = Case.ofNat 714 := by decide
  rw [he]
  exact case0714
#print axioms case1738

theorem case0715 : checkNat 715 = true := by native_decide
#print axioms case0715

theorem case0716 : checkNat 716 = true := by native_decide
#print axioms case0716

theorem case1740 : checkNat 1740 = true := by
  apply check_of_normalize (Case.ofNat 1740)
  have he : (Case.ofNat 1740).normalize = Case.ofNat 716 := by decide
  rw [he]
  exact case0716
#print axioms case1740

theorem case2764 : checkNat 2764 = true := by
  apply check_of_normalize (Case.ofNat 2764)
  have he : (Case.ofNat 2764).normalize = Case.ofNat 716 := by decide
  rw [he]
  exact case0716
#print axioms case2764

theorem case3788 : checkNat 3788 = true := by
  apply check_of_normalize (Case.ofNat 3788)
  have he : (Case.ofNat 3788).normalize = Case.ofNat 716 := by decide
  rw [he]
  exact case0716
#print axioms case3788

theorem case0717 : checkNat 717 = true := by native_decide
#print axioms case0717

theorem case2765 : checkNat 2765 = true := by
  apply check_of_normalize (Case.ofNat 2765)
  have he : (Case.ofNat 2765).normalize = Case.ofNat 717 := by decide
  rw [he]
  exact case0717
#print axioms case2765

theorem case0718 : checkNat 718 = true := by native_decide
#print axioms case0718

theorem case1742 : checkNat 1742 = true := by
  apply check_of_normalize (Case.ofNat 1742)
  have he : (Case.ofNat 1742).normalize = Case.ofNat 718 := by decide
  rw [he]
  exact case0718
#print axioms case1742

theorem case0719 : checkNat 719 = true := by native_decide
#print axioms case0719

theorem case0720 : checkNat 720 = true := by native_decide
#print axioms case0720

theorem case1744 : checkNat 1744 = true := by
  apply check_of_normalize (Case.ofNat 1744)
  have he : (Case.ofNat 1744).normalize = Case.ofNat 720 := by decide
  rw [he]
  exact case0720
#print axioms case1744

theorem case2768 : checkNat 2768 = true := by
  apply check_of_normalize (Case.ofNat 2768)
  have he : (Case.ofNat 2768).normalize = Case.ofNat 720 := by decide
  rw [he]
  exact case0720
#print axioms case2768

theorem case3792 : checkNat 3792 = true := by
  apply check_of_normalize (Case.ofNat 3792)
  have he : (Case.ofNat 3792).normalize = Case.ofNat 720 := by decide
  rw [he]
  exact case0720
#print axioms case3792

theorem case0721 : checkNat 721 = true := by native_decide
#print axioms case0721

theorem case2769 : checkNat 2769 = true := by
  apply check_of_normalize (Case.ofNat 2769)
  have he : (Case.ofNat 2769).normalize = Case.ofNat 721 := by decide
  rw [he]
  exact case0721
#print axioms case2769

theorem case0722 : checkNat 722 = true := by native_decide
#print axioms case0722

theorem case1746 : checkNat 1746 = true := by
  apply check_of_normalize (Case.ofNat 1746)
  have he : (Case.ofNat 1746).normalize = Case.ofNat 722 := by decide
  rw [he]
  exact case0722
#print axioms case1746

theorem case0723 : checkNat 723 = true := by native_decide
#print axioms case0723

theorem case0724 : checkNat 724 = true := by native_decide
#print axioms case0724

theorem case1748 : checkNat 1748 = true := by
  apply check_of_normalize (Case.ofNat 1748)
  have he : (Case.ofNat 1748).normalize = Case.ofNat 724 := by decide
  rw [he]
  exact case0724
#print axioms case1748

theorem case2772 : checkNat 2772 = true := by
  apply check_of_normalize (Case.ofNat 2772)
  have he : (Case.ofNat 2772).normalize = Case.ofNat 724 := by decide
  rw [he]
  exact case0724
#print axioms case2772

theorem case3796 : checkNat 3796 = true := by
  apply check_of_normalize (Case.ofNat 3796)
  have he : (Case.ofNat 3796).normalize = Case.ofNat 724 := by decide
  rw [he]
  exact case0724
#print axioms case3796

theorem case0725 : checkNat 725 = true := by native_decide
#print axioms case0725

theorem case2773 : checkNat 2773 = true := by
  apply check_of_normalize (Case.ofNat 2773)
  have he : (Case.ofNat 2773).normalize = Case.ofNat 725 := by decide
  rw [he]
  exact case0725
#print axioms case2773

theorem case0726 : checkNat 726 = true := by native_decide
#print axioms case0726

theorem case1750 : checkNat 1750 = true := by
  apply check_of_normalize (Case.ofNat 1750)
  have he : (Case.ofNat 1750).normalize = Case.ofNat 726 := by decide
  rw [he]
  exact case0726
#print axioms case1750

theorem case0727 : checkNat 727 = true := by native_decide
#print axioms case0727

theorem case0728 : checkNat 728 = true := by native_decide
#print axioms case0728

theorem case1752 : checkNat 1752 = true := by
  apply check_of_normalize (Case.ofNat 1752)
  have he : (Case.ofNat 1752).normalize = Case.ofNat 728 := by decide
  rw [he]
  exact case0728
#print axioms case1752

theorem case2776 : checkNat 2776 = true := by
  apply check_of_normalize (Case.ofNat 2776)
  have he : (Case.ofNat 2776).normalize = Case.ofNat 728 := by decide
  rw [he]
  exact case0728
#print axioms case2776

theorem case3800 : checkNat 3800 = true := by
  apply check_of_normalize (Case.ofNat 3800)
  have he : (Case.ofNat 3800).normalize = Case.ofNat 728 := by decide
  rw [he]
  exact case0728
#print axioms case3800

theorem case0729 : checkNat 729 = true := by native_decide
#print axioms case0729

theorem case2777 : checkNat 2777 = true := by
  apply check_of_normalize (Case.ofNat 2777)
  have he : (Case.ofNat 2777).normalize = Case.ofNat 729 := by decide
  rw [he]
  exact case0729
#print axioms case2777

theorem case0730 : checkNat 730 = true := by native_decide
#print axioms case0730

theorem case1754 : checkNat 1754 = true := by
  apply check_of_normalize (Case.ofNat 1754)
  have he : (Case.ofNat 1754).normalize = Case.ofNat 730 := by decide
  rw [he]
  exact case0730
#print axioms case1754

theorem case0731 : checkNat 731 = true := by native_decide
#print axioms case0731

theorem case0732 : checkNat 732 = true := by native_decide
#print axioms case0732

theorem case1756 : checkNat 1756 = true := by
  apply check_of_normalize (Case.ofNat 1756)
  have he : (Case.ofNat 1756).normalize = Case.ofNat 732 := by decide
  rw [he]
  exact case0732
#print axioms case1756

theorem case2780 : checkNat 2780 = true := by
  apply check_of_normalize (Case.ofNat 2780)
  have he : (Case.ofNat 2780).normalize = Case.ofNat 732 := by decide
  rw [he]
  exact case0732
#print axioms case2780

theorem case3804 : checkNat 3804 = true := by
  apply check_of_normalize (Case.ofNat 3804)
  have he : (Case.ofNat 3804).normalize = Case.ofNat 732 := by decide
  rw [he]
  exact case0732
#print axioms case3804

theorem case0733 : checkNat 733 = true := by native_decide
#print axioms case0733

theorem case2781 : checkNat 2781 = true := by
  apply check_of_normalize (Case.ofNat 2781)
  have he : (Case.ofNat 2781).normalize = Case.ofNat 733 := by decide
  rw [he]
  exact case0733
#print axioms case2781

theorem case0734 : checkNat 734 = true := by native_decide
#print axioms case0734

theorem case1758 : checkNat 1758 = true := by
  apply check_of_normalize (Case.ofNat 1758)
  have he : (Case.ofNat 1758).normalize = Case.ofNat 734 := by decide
  rw [he]
  exact case0734
#print axioms case1758

theorem case0735 : checkNat 735 = true := by native_decide
#print axioms case0735

theorem accepted :
    checkNat 704 = true ∧
    checkNat 705 = true ∧
    checkNat 706 = true ∧
    checkNat 707 = true ∧
    checkNat 708 = true ∧
    checkNat 709 = true ∧
    checkNat 710 = true ∧
    checkNat 711 = true ∧
    checkNat 712 = true ∧
    checkNat 713 = true ∧
    checkNat 714 = true ∧
    checkNat 715 = true ∧
    checkNat 716 = true ∧
    checkNat 717 = true ∧
    checkNat 718 = true ∧
    checkNat 719 = true ∧
    checkNat 720 = true ∧
    checkNat 721 = true ∧
    checkNat 722 = true ∧
    checkNat 723 = true ∧
    checkNat 724 = true ∧
    checkNat 725 = true ∧
    checkNat 726 = true ∧
    checkNat 727 = true ∧
    checkNat 728 = true ∧
    checkNat 729 = true ∧
    checkNat 730 = true ∧
    checkNat 731 = true ∧
    checkNat 732 = true ∧
    checkNat 733 = true ∧
    checkNat 734 = true ∧
    checkNat 735 = true ∧
    checkNat 1728 = true ∧
    checkNat 1730 = true ∧
    checkNat 1732 = true ∧
    checkNat 1734 = true ∧
    checkNat 1736 = true ∧
    checkNat 1738 = true ∧
    checkNat 1740 = true ∧
    checkNat 1742 = true ∧
    checkNat 1744 = true ∧
    checkNat 1746 = true ∧
    checkNat 1748 = true ∧
    checkNat 1750 = true ∧
    checkNat 1752 = true ∧
    checkNat 1754 = true ∧
    checkNat 1756 = true ∧
    checkNat 1758 = true ∧
    checkNat 2752 = true ∧
    checkNat 2753 = true ∧
    checkNat 2756 = true ∧
    checkNat 2757 = true ∧
    checkNat 2760 = true ∧
    checkNat 2761 = true ∧
    checkNat 2764 = true ∧
    checkNat 2765 = true ∧
    checkNat 2768 = true ∧
    checkNat 2769 = true ∧
    checkNat 2772 = true ∧
    checkNat 2773 = true ∧
    checkNat 2776 = true ∧
    checkNat 2777 = true ∧
    checkNat 2780 = true ∧
    checkNat 2781 = true ∧
    checkNat 3776 = true ∧
    checkNat 3780 = true ∧
    checkNat 3784 = true ∧
    checkNat 3788 = true ∧
    checkNat 3792 = true ∧
    checkNat 3796 = true ∧
    checkNat 3800 = true ∧
    checkNat 3804 = true := by
  exact ⟨case0704, case0705, case0706, case0707, case0708, case0709, case0710, case0711, case0712, case0713, case0714, case0715, case0716, case0717, case0718, case0719, case0720, case0721, case0722, case0723, case0724, case0725, case0726, case0727, case0728, case0729, case0730, case0731, case0732, case0733, case0734, case0735, case1728, case1730, case1732, case1734, case1736, case1738, case1740, case1742, case1744, case1746, case1748, case1750, case1752, case1754, case1756, case1758, case2752, case2753, case2756, case2757, case2760, case2761, case2764, case2765, case2768, case2769, case2772, case2773, case2776, case2777, case2780, case2781, case3776, case3780, case3784, case3788, case3792, case3796, case3800, case3804⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0704
