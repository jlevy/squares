import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0608
open Sq19.Endgame.Reduction

theorem case0608 : checkNat 608 = true := by native_decide
#print axioms case0608

theorem case1632 : checkNat 1632 = true := by
  apply check_of_normalize (Case.ofNat 1632)
  have he : (Case.ofNat 1632).normalize = Case.ofNat 608 := by decide
  rw [he]
  exact case0608
#print axioms case1632

theorem case2656 : checkNat 2656 = true := by
  apply check_of_normalize (Case.ofNat 2656)
  have he : (Case.ofNat 2656).normalize = Case.ofNat 608 := by decide
  rw [he]
  exact case0608
#print axioms case2656

theorem case3680 : checkNat 3680 = true := by
  apply check_of_normalize (Case.ofNat 3680)
  have he : (Case.ofNat 3680).normalize = Case.ofNat 608 := by decide
  rw [he]
  exact case0608
#print axioms case3680

theorem case0609 : checkNat 609 = true := by native_decide
#print axioms case0609

theorem case2657 : checkNat 2657 = true := by
  apply check_of_normalize (Case.ofNat 2657)
  have he : (Case.ofNat 2657).normalize = Case.ofNat 609 := by decide
  rw [he]
  exact case0609
#print axioms case2657

theorem case0610 : checkNat 610 = true := by native_decide
#print axioms case0610

theorem case1634 : checkNat 1634 = true := by
  apply check_of_normalize (Case.ofNat 1634)
  have he : (Case.ofNat 1634).normalize = Case.ofNat 610 := by decide
  rw [he]
  exact case0610
#print axioms case1634

theorem case0611 : checkNat 611 = true := by native_decide
#print axioms case0611

theorem case0612 : checkNat 612 = true := by native_decide
#print axioms case0612

theorem case1636 : checkNat 1636 = true := by
  apply check_of_normalize (Case.ofNat 1636)
  have he : (Case.ofNat 1636).normalize = Case.ofNat 612 := by decide
  rw [he]
  exact case0612
#print axioms case1636

theorem case2660 : checkNat 2660 = true := by
  apply check_of_normalize (Case.ofNat 2660)
  have he : (Case.ofNat 2660).normalize = Case.ofNat 612 := by decide
  rw [he]
  exact case0612
#print axioms case2660

theorem case3684 : checkNat 3684 = true := by
  apply check_of_normalize (Case.ofNat 3684)
  have he : (Case.ofNat 3684).normalize = Case.ofNat 612 := by decide
  rw [he]
  exact case0612
#print axioms case3684

theorem case0613 : checkNat 613 = true := by native_decide
#print axioms case0613

theorem case2661 : checkNat 2661 = true := by
  apply check_of_normalize (Case.ofNat 2661)
  have he : (Case.ofNat 2661).normalize = Case.ofNat 613 := by decide
  rw [he]
  exact case0613
#print axioms case2661

theorem case0614 : checkNat 614 = true := by native_decide
#print axioms case0614

theorem case1638 : checkNat 1638 = true := by
  apply check_of_normalize (Case.ofNat 1638)
  have he : (Case.ofNat 1638).normalize = Case.ofNat 614 := by decide
  rw [he]
  exact case0614
#print axioms case1638

theorem case0615 : checkNat 615 = true := by native_decide
#print axioms case0615

theorem case0616 : checkNat 616 = true := by native_decide
#print axioms case0616

theorem case1640 : checkNat 1640 = true := by
  apply check_of_normalize (Case.ofNat 1640)
  have he : (Case.ofNat 1640).normalize = Case.ofNat 616 := by decide
  rw [he]
  exact case0616
#print axioms case1640

theorem case2664 : checkNat 2664 = true := by
  apply check_of_normalize (Case.ofNat 2664)
  have he : (Case.ofNat 2664).normalize = Case.ofNat 616 := by decide
  rw [he]
  exact case0616
#print axioms case2664

theorem case3688 : checkNat 3688 = true := by
  apply check_of_normalize (Case.ofNat 3688)
  have he : (Case.ofNat 3688).normalize = Case.ofNat 616 := by decide
  rw [he]
  exact case0616
#print axioms case3688

theorem case0617 : checkNat 617 = true := by native_decide
#print axioms case0617

theorem case2665 : checkNat 2665 = true := by
  apply check_of_normalize (Case.ofNat 2665)
  have he : (Case.ofNat 2665).normalize = Case.ofNat 617 := by decide
  rw [he]
  exact case0617
#print axioms case2665

theorem case0618 : checkNat 618 = true := by native_decide
#print axioms case0618

theorem case1642 : checkNat 1642 = true := by
  apply check_of_normalize (Case.ofNat 1642)
  have he : (Case.ofNat 1642).normalize = Case.ofNat 618 := by decide
  rw [he]
  exact case0618
#print axioms case1642

theorem case0619 : checkNat 619 = true := by native_decide
#print axioms case0619

theorem case0620 : checkNat 620 = true := by native_decide
#print axioms case0620

theorem case1644 : checkNat 1644 = true := by
  apply check_of_normalize (Case.ofNat 1644)
  have he : (Case.ofNat 1644).normalize = Case.ofNat 620 := by decide
  rw [he]
  exact case0620
#print axioms case1644

theorem case2668 : checkNat 2668 = true := by
  apply check_of_normalize (Case.ofNat 2668)
  have he : (Case.ofNat 2668).normalize = Case.ofNat 620 := by decide
  rw [he]
  exact case0620
#print axioms case2668

theorem case3692 : checkNat 3692 = true := by
  apply check_of_normalize (Case.ofNat 3692)
  have he : (Case.ofNat 3692).normalize = Case.ofNat 620 := by decide
  rw [he]
  exact case0620
#print axioms case3692

theorem case0621 : checkNat 621 = true := by native_decide
#print axioms case0621

theorem case2669 : checkNat 2669 = true := by
  apply check_of_normalize (Case.ofNat 2669)
  have he : (Case.ofNat 2669).normalize = Case.ofNat 621 := by decide
  rw [he]
  exact case0621
#print axioms case2669

theorem case0622 : checkNat 622 = true := by native_decide
#print axioms case0622

theorem case1646 : checkNat 1646 = true := by
  apply check_of_normalize (Case.ofNat 1646)
  have he : (Case.ofNat 1646).normalize = Case.ofNat 622 := by decide
  rw [he]
  exact case0622
#print axioms case1646

theorem case0623 : checkNat 623 = true := by native_decide
#print axioms case0623

theorem case0624 : checkNat 624 = true := by native_decide
#print axioms case0624

theorem case1648 : checkNat 1648 = true := by
  apply check_of_normalize (Case.ofNat 1648)
  have he : (Case.ofNat 1648).normalize = Case.ofNat 624 := by decide
  rw [he]
  exact case0624
#print axioms case1648

theorem case2672 : checkNat 2672 = true := by
  apply check_of_normalize (Case.ofNat 2672)
  have he : (Case.ofNat 2672).normalize = Case.ofNat 624 := by decide
  rw [he]
  exact case0624
#print axioms case2672

theorem case3696 : checkNat 3696 = true := by
  apply check_of_normalize (Case.ofNat 3696)
  have he : (Case.ofNat 3696).normalize = Case.ofNat 624 := by decide
  rw [he]
  exact case0624
#print axioms case3696

theorem case0625 : checkNat 625 = true := by native_decide
#print axioms case0625

theorem case2673 : checkNat 2673 = true := by
  apply check_of_normalize (Case.ofNat 2673)
  have he : (Case.ofNat 2673).normalize = Case.ofNat 625 := by decide
  rw [he]
  exact case0625
#print axioms case2673

theorem case0626 : checkNat 626 = true := by native_decide
#print axioms case0626

theorem case1650 : checkNat 1650 = true := by
  apply check_of_normalize (Case.ofNat 1650)
  have he : (Case.ofNat 1650).normalize = Case.ofNat 626 := by decide
  rw [he]
  exact case0626
#print axioms case1650

theorem case0627 : checkNat 627 = true := by native_decide
#print axioms case0627

theorem case0628 : checkNat 628 = true := by native_decide
#print axioms case0628

theorem case1652 : checkNat 1652 = true := by
  apply check_of_normalize (Case.ofNat 1652)
  have he : (Case.ofNat 1652).normalize = Case.ofNat 628 := by decide
  rw [he]
  exact case0628
#print axioms case1652

theorem case2676 : checkNat 2676 = true := by
  apply check_of_normalize (Case.ofNat 2676)
  have he : (Case.ofNat 2676).normalize = Case.ofNat 628 := by decide
  rw [he]
  exact case0628
#print axioms case2676

theorem case3700 : checkNat 3700 = true := by
  apply check_of_normalize (Case.ofNat 3700)
  have he : (Case.ofNat 3700).normalize = Case.ofNat 628 := by decide
  rw [he]
  exact case0628
#print axioms case3700

theorem case0629 : checkNat 629 = true := by native_decide
#print axioms case0629

theorem case2677 : checkNat 2677 = true := by
  apply check_of_normalize (Case.ofNat 2677)
  have he : (Case.ofNat 2677).normalize = Case.ofNat 629 := by decide
  rw [he]
  exact case0629
#print axioms case2677

theorem case0630 : checkNat 630 = true := by native_decide
#print axioms case0630

theorem case1654 : checkNat 1654 = true := by
  apply check_of_normalize (Case.ofNat 1654)
  have he : (Case.ofNat 1654).normalize = Case.ofNat 630 := by decide
  rw [he]
  exact case0630
#print axioms case1654

theorem case0631 : checkNat 631 = true := by native_decide
#print axioms case0631

theorem case0632 : checkNat 632 = true := by native_decide
#print axioms case0632

theorem case1656 : checkNat 1656 = true := by
  apply check_of_normalize (Case.ofNat 1656)
  have he : (Case.ofNat 1656).normalize = Case.ofNat 632 := by decide
  rw [he]
  exact case0632
#print axioms case1656

theorem case2680 : checkNat 2680 = true := by
  apply check_of_normalize (Case.ofNat 2680)
  have he : (Case.ofNat 2680).normalize = Case.ofNat 632 := by decide
  rw [he]
  exact case0632
#print axioms case2680

theorem case3704 : checkNat 3704 = true := by
  apply check_of_normalize (Case.ofNat 3704)
  have he : (Case.ofNat 3704).normalize = Case.ofNat 632 := by decide
  rw [he]
  exact case0632
#print axioms case3704

theorem case0633 : checkNat 633 = true := by native_decide
#print axioms case0633

theorem case2681 : checkNat 2681 = true := by
  apply check_of_normalize (Case.ofNat 2681)
  have he : (Case.ofNat 2681).normalize = Case.ofNat 633 := by decide
  rw [he]
  exact case0633
#print axioms case2681

theorem case0634 : checkNat 634 = true := by native_decide
#print axioms case0634

theorem case1658 : checkNat 1658 = true := by
  apply check_of_normalize (Case.ofNat 1658)
  have he : (Case.ofNat 1658).normalize = Case.ofNat 634 := by decide
  rw [he]
  exact case0634
#print axioms case1658

theorem case0635 : checkNat 635 = true := by native_decide
#print axioms case0635

theorem case0636 : checkNat 636 = true := by native_decide
#print axioms case0636

theorem case1660 : checkNat 1660 = true := by
  apply check_of_normalize (Case.ofNat 1660)
  have he : (Case.ofNat 1660).normalize = Case.ofNat 636 := by decide
  rw [he]
  exact case0636
#print axioms case1660

theorem case2684 : checkNat 2684 = true := by
  apply check_of_normalize (Case.ofNat 2684)
  have he : (Case.ofNat 2684).normalize = Case.ofNat 636 := by decide
  rw [he]
  exact case0636
#print axioms case2684

theorem case3708 : checkNat 3708 = true := by
  apply check_of_normalize (Case.ofNat 3708)
  have he : (Case.ofNat 3708).normalize = Case.ofNat 636 := by decide
  rw [he]
  exact case0636
#print axioms case3708

theorem case0637 : checkNat 637 = true := by native_decide
#print axioms case0637

theorem case2685 : checkNat 2685 = true := by
  apply check_of_normalize (Case.ofNat 2685)
  have he : (Case.ofNat 2685).normalize = Case.ofNat 637 := by decide
  rw [he]
  exact case0637
#print axioms case2685

theorem case0638 : checkNat 638 = true := by native_decide
#print axioms case0638

theorem case1662 : checkNat 1662 = true := by
  apply check_of_normalize (Case.ofNat 1662)
  have he : (Case.ofNat 1662).normalize = Case.ofNat 638 := by decide
  rw [he]
  exact case0638
#print axioms case1662

theorem case0639 : checkNat 639 = true := by native_decide
#print axioms case0639

theorem accepted :
    checkNat 608 = true ∧
    checkNat 609 = true ∧
    checkNat 610 = true ∧
    checkNat 611 = true ∧
    checkNat 612 = true ∧
    checkNat 613 = true ∧
    checkNat 614 = true ∧
    checkNat 615 = true ∧
    checkNat 616 = true ∧
    checkNat 617 = true ∧
    checkNat 618 = true ∧
    checkNat 619 = true ∧
    checkNat 620 = true ∧
    checkNat 621 = true ∧
    checkNat 622 = true ∧
    checkNat 623 = true ∧
    checkNat 624 = true ∧
    checkNat 625 = true ∧
    checkNat 626 = true ∧
    checkNat 627 = true ∧
    checkNat 628 = true ∧
    checkNat 629 = true ∧
    checkNat 630 = true ∧
    checkNat 631 = true ∧
    checkNat 632 = true ∧
    checkNat 633 = true ∧
    checkNat 634 = true ∧
    checkNat 635 = true ∧
    checkNat 636 = true ∧
    checkNat 637 = true ∧
    checkNat 638 = true ∧
    checkNat 639 = true ∧
    checkNat 1632 = true ∧
    checkNat 1634 = true ∧
    checkNat 1636 = true ∧
    checkNat 1638 = true ∧
    checkNat 1640 = true ∧
    checkNat 1642 = true ∧
    checkNat 1644 = true ∧
    checkNat 1646 = true ∧
    checkNat 1648 = true ∧
    checkNat 1650 = true ∧
    checkNat 1652 = true ∧
    checkNat 1654 = true ∧
    checkNat 1656 = true ∧
    checkNat 1658 = true ∧
    checkNat 1660 = true ∧
    checkNat 1662 = true ∧
    checkNat 2656 = true ∧
    checkNat 2657 = true ∧
    checkNat 2660 = true ∧
    checkNat 2661 = true ∧
    checkNat 2664 = true ∧
    checkNat 2665 = true ∧
    checkNat 2668 = true ∧
    checkNat 2669 = true ∧
    checkNat 2672 = true ∧
    checkNat 2673 = true ∧
    checkNat 2676 = true ∧
    checkNat 2677 = true ∧
    checkNat 2680 = true ∧
    checkNat 2681 = true ∧
    checkNat 2684 = true ∧
    checkNat 2685 = true ∧
    checkNat 3680 = true ∧
    checkNat 3684 = true ∧
    checkNat 3688 = true ∧
    checkNat 3692 = true ∧
    checkNat 3696 = true ∧
    checkNat 3700 = true ∧
    checkNat 3704 = true ∧
    checkNat 3708 = true := by
  exact ⟨case0608, case0609, case0610, case0611, case0612, case0613, case0614, case0615, case0616, case0617, case0618, case0619, case0620, case0621, case0622, case0623, case0624, case0625, case0626, case0627, case0628, case0629, case0630, case0631, case0632, case0633, case0634, case0635, case0636, case0637, case0638, case0639, case1632, case1634, case1636, case1638, case1640, case1642, case1644, case1646, case1648, case1650, case1652, case1654, case1656, case1658, case1660, case1662, case2656, case2657, case2660, case2661, case2664, case2665, case2668, case2669, case2672, case2673, case2676, case2677, case2680, case2681, case2684, case2685, case3680, case3684, case3688, case3692, case3696, case3700, case3704, case3708⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0608
