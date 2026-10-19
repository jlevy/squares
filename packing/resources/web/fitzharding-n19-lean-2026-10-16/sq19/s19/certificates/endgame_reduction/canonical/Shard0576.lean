import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0576
open Sq19.Endgame.Reduction

theorem case0576 : checkNat 576 = true := by native_decide
#print axioms case0576

theorem case1600 : checkNat 1600 = true := by
  apply check_of_normalize (Case.ofNat 1600)
  have he : (Case.ofNat 1600).normalize = Case.ofNat 576 := by decide
  rw [he]
  exact case0576
#print axioms case1600

theorem case2624 : checkNat 2624 = true := by
  apply check_of_normalize (Case.ofNat 2624)
  have he : (Case.ofNat 2624).normalize = Case.ofNat 576 := by decide
  rw [he]
  exact case0576
#print axioms case2624

theorem case3648 : checkNat 3648 = true := by
  apply check_of_normalize (Case.ofNat 3648)
  have he : (Case.ofNat 3648).normalize = Case.ofNat 576 := by decide
  rw [he]
  exact case0576
#print axioms case3648

theorem case0577 : checkNat 577 = true := by native_decide
#print axioms case0577

theorem case2625 : checkNat 2625 = true := by
  apply check_of_normalize (Case.ofNat 2625)
  have he : (Case.ofNat 2625).normalize = Case.ofNat 577 := by decide
  rw [he]
  exact case0577
#print axioms case2625

theorem case0578 : checkNat 578 = true := by native_decide
#print axioms case0578

theorem case1602 : checkNat 1602 = true := by
  apply check_of_normalize (Case.ofNat 1602)
  have he : (Case.ofNat 1602).normalize = Case.ofNat 578 := by decide
  rw [he]
  exact case0578
#print axioms case1602

theorem case0579 : checkNat 579 = true := by native_decide
#print axioms case0579

theorem case0580 : checkNat 580 = true := by native_decide
#print axioms case0580

theorem case1604 : checkNat 1604 = true := by
  apply check_of_normalize (Case.ofNat 1604)
  have he : (Case.ofNat 1604).normalize = Case.ofNat 580 := by decide
  rw [he]
  exact case0580
#print axioms case1604

theorem case2628 : checkNat 2628 = true := by
  apply check_of_normalize (Case.ofNat 2628)
  have he : (Case.ofNat 2628).normalize = Case.ofNat 580 := by decide
  rw [he]
  exact case0580
#print axioms case2628

theorem case3652 : checkNat 3652 = true := by
  apply check_of_normalize (Case.ofNat 3652)
  have he : (Case.ofNat 3652).normalize = Case.ofNat 580 := by decide
  rw [he]
  exact case0580
#print axioms case3652

theorem case0581 : checkNat 581 = true := by native_decide
#print axioms case0581

theorem case2629 : checkNat 2629 = true := by
  apply check_of_normalize (Case.ofNat 2629)
  have he : (Case.ofNat 2629).normalize = Case.ofNat 581 := by decide
  rw [he]
  exact case0581
#print axioms case2629

theorem case0582 : checkNat 582 = true := by native_decide
#print axioms case0582

theorem case1606 : checkNat 1606 = true := by
  apply check_of_normalize (Case.ofNat 1606)
  have he : (Case.ofNat 1606).normalize = Case.ofNat 582 := by decide
  rw [he]
  exact case0582
#print axioms case1606

theorem case0583 : checkNat 583 = true := by native_decide
#print axioms case0583

theorem case0584 : checkNat 584 = true := by native_decide
#print axioms case0584

theorem case1608 : checkNat 1608 = true := by
  apply check_of_normalize (Case.ofNat 1608)
  have he : (Case.ofNat 1608).normalize = Case.ofNat 584 := by decide
  rw [he]
  exact case0584
#print axioms case1608

theorem case2632 : checkNat 2632 = true := by
  apply check_of_normalize (Case.ofNat 2632)
  have he : (Case.ofNat 2632).normalize = Case.ofNat 584 := by decide
  rw [he]
  exact case0584
#print axioms case2632

theorem case3656 : checkNat 3656 = true := by
  apply check_of_normalize (Case.ofNat 3656)
  have he : (Case.ofNat 3656).normalize = Case.ofNat 584 := by decide
  rw [he]
  exact case0584
#print axioms case3656

theorem case0585 : checkNat 585 = true := by native_decide
#print axioms case0585

theorem case2633 : checkNat 2633 = true := by
  apply check_of_normalize (Case.ofNat 2633)
  have he : (Case.ofNat 2633).normalize = Case.ofNat 585 := by decide
  rw [he]
  exact case0585
#print axioms case2633

theorem case0586 : checkNat 586 = true := by native_decide
#print axioms case0586

theorem case1610 : checkNat 1610 = true := by
  apply check_of_normalize (Case.ofNat 1610)
  have he : (Case.ofNat 1610).normalize = Case.ofNat 586 := by decide
  rw [he]
  exact case0586
#print axioms case1610

theorem case0587 : checkNat 587 = true := by native_decide
#print axioms case0587

theorem case0588 : checkNat 588 = true := by native_decide
#print axioms case0588

theorem case1612 : checkNat 1612 = true := by
  apply check_of_normalize (Case.ofNat 1612)
  have he : (Case.ofNat 1612).normalize = Case.ofNat 588 := by decide
  rw [he]
  exact case0588
#print axioms case1612

theorem case2636 : checkNat 2636 = true := by
  apply check_of_normalize (Case.ofNat 2636)
  have he : (Case.ofNat 2636).normalize = Case.ofNat 588 := by decide
  rw [he]
  exact case0588
#print axioms case2636

theorem case3660 : checkNat 3660 = true := by
  apply check_of_normalize (Case.ofNat 3660)
  have he : (Case.ofNat 3660).normalize = Case.ofNat 588 := by decide
  rw [he]
  exact case0588
#print axioms case3660

theorem case0589 : checkNat 589 = true := by native_decide
#print axioms case0589

theorem case2637 : checkNat 2637 = true := by
  apply check_of_normalize (Case.ofNat 2637)
  have he : (Case.ofNat 2637).normalize = Case.ofNat 589 := by decide
  rw [he]
  exact case0589
#print axioms case2637

theorem case0590 : checkNat 590 = true := by native_decide
#print axioms case0590

theorem case1614 : checkNat 1614 = true := by
  apply check_of_normalize (Case.ofNat 1614)
  have he : (Case.ofNat 1614).normalize = Case.ofNat 590 := by decide
  rw [he]
  exact case0590
#print axioms case1614

theorem case0591 : checkNat 591 = true := by native_decide
#print axioms case0591

theorem case0592 : checkNat 592 = true := by native_decide
#print axioms case0592

theorem case1616 : checkNat 1616 = true := by
  apply check_of_normalize (Case.ofNat 1616)
  have he : (Case.ofNat 1616).normalize = Case.ofNat 592 := by decide
  rw [he]
  exact case0592
#print axioms case1616

theorem case2640 : checkNat 2640 = true := by
  apply check_of_normalize (Case.ofNat 2640)
  have he : (Case.ofNat 2640).normalize = Case.ofNat 592 := by decide
  rw [he]
  exact case0592
#print axioms case2640

theorem case3664 : checkNat 3664 = true := by
  apply check_of_normalize (Case.ofNat 3664)
  have he : (Case.ofNat 3664).normalize = Case.ofNat 592 := by decide
  rw [he]
  exact case0592
#print axioms case3664

theorem case0593 : checkNat 593 = true := by native_decide
#print axioms case0593

theorem case2641 : checkNat 2641 = true := by
  apply check_of_normalize (Case.ofNat 2641)
  have he : (Case.ofNat 2641).normalize = Case.ofNat 593 := by decide
  rw [he]
  exact case0593
#print axioms case2641

theorem case0594 : checkNat 594 = true := by native_decide
#print axioms case0594

theorem case1618 : checkNat 1618 = true := by
  apply check_of_normalize (Case.ofNat 1618)
  have he : (Case.ofNat 1618).normalize = Case.ofNat 594 := by decide
  rw [he]
  exact case0594
#print axioms case1618

theorem case0595 : checkNat 595 = true := by native_decide
#print axioms case0595

theorem case0596 : checkNat 596 = true := by native_decide
#print axioms case0596

theorem case1620 : checkNat 1620 = true := by
  apply check_of_normalize (Case.ofNat 1620)
  have he : (Case.ofNat 1620).normalize = Case.ofNat 596 := by decide
  rw [he]
  exact case0596
#print axioms case1620

theorem case2644 : checkNat 2644 = true := by
  apply check_of_normalize (Case.ofNat 2644)
  have he : (Case.ofNat 2644).normalize = Case.ofNat 596 := by decide
  rw [he]
  exact case0596
#print axioms case2644

theorem case3668 : checkNat 3668 = true := by
  apply check_of_normalize (Case.ofNat 3668)
  have he : (Case.ofNat 3668).normalize = Case.ofNat 596 := by decide
  rw [he]
  exact case0596
#print axioms case3668

theorem case0597 : checkNat 597 = true := by native_decide
#print axioms case0597

theorem case2645 : checkNat 2645 = true := by
  apply check_of_normalize (Case.ofNat 2645)
  have he : (Case.ofNat 2645).normalize = Case.ofNat 597 := by decide
  rw [he]
  exact case0597
#print axioms case2645

theorem case0598 : checkNat 598 = true := by native_decide
#print axioms case0598

theorem case1622 : checkNat 1622 = true := by
  apply check_of_normalize (Case.ofNat 1622)
  have he : (Case.ofNat 1622).normalize = Case.ofNat 598 := by decide
  rw [he]
  exact case0598
#print axioms case1622

theorem case0599 : checkNat 599 = true := by native_decide
#print axioms case0599

theorem case0600 : checkNat 600 = true := by native_decide
#print axioms case0600

theorem case1624 : checkNat 1624 = true := by
  apply check_of_normalize (Case.ofNat 1624)
  have he : (Case.ofNat 1624).normalize = Case.ofNat 600 := by decide
  rw [he]
  exact case0600
#print axioms case1624

theorem case2648 : checkNat 2648 = true := by
  apply check_of_normalize (Case.ofNat 2648)
  have he : (Case.ofNat 2648).normalize = Case.ofNat 600 := by decide
  rw [he]
  exact case0600
#print axioms case2648

theorem case3672 : checkNat 3672 = true := by
  apply check_of_normalize (Case.ofNat 3672)
  have he : (Case.ofNat 3672).normalize = Case.ofNat 600 := by decide
  rw [he]
  exact case0600
#print axioms case3672

theorem case0601 : checkNat 601 = true := by native_decide
#print axioms case0601

theorem case2649 : checkNat 2649 = true := by
  apply check_of_normalize (Case.ofNat 2649)
  have he : (Case.ofNat 2649).normalize = Case.ofNat 601 := by decide
  rw [he]
  exact case0601
#print axioms case2649

theorem case0602 : checkNat 602 = true := by native_decide
#print axioms case0602

theorem case1626 : checkNat 1626 = true := by
  apply check_of_normalize (Case.ofNat 1626)
  have he : (Case.ofNat 1626).normalize = Case.ofNat 602 := by decide
  rw [he]
  exact case0602
#print axioms case1626

theorem case0603 : checkNat 603 = true := by native_decide
#print axioms case0603

theorem case0604 : checkNat 604 = true := by native_decide
#print axioms case0604

theorem case1628 : checkNat 1628 = true := by
  apply check_of_normalize (Case.ofNat 1628)
  have he : (Case.ofNat 1628).normalize = Case.ofNat 604 := by decide
  rw [he]
  exact case0604
#print axioms case1628

theorem case2652 : checkNat 2652 = true := by
  apply check_of_normalize (Case.ofNat 2652)
  have he : (Case.ofNat 2652).normalize = Case.ofNat 604 := by decide
  rw [he]
  exact case0604
#print axioms case2652

theorem case3676 : checkNat 3676 = true := by
  apply check_of_normalize (Case.ofNat 3676)
  have he : (Case.ofNat 3676).normalize = Case.ofNat 604 := by decide
  rw [he]
  exact case0604
#print axioms case3676

theorem case0605 : checkNat 605 = true := by native_decide
#print axioms case0605

theorem case2653 : checkNat 2653 = true := by
  apply check_of_normalize (Case.ofNat 2653)
  have he : (Case.ofNat 2653).normalize = Case.ofNat 605 := by decide
  rw [he]
  exact case0605
#print axioms case2653

theorem case0606 : checkNat 606 = true := by native_decide
#print axioms case0606

theorem case1630 : checkNat 1630 = true := by
  apply check_of_normalize (Case.ofNat 1630)
  have he : (Case.ofNat 1630).normalize = Case.ofNat 606 := by decide
  rw [he]
  exact case0606
#print axioms case1630

theorem case0607 : checkNat 607 = true := by native_decide
#print axioms case0607

theorem accepted :
    checkNat 576 = true ∧
    checkNat 577 = true ∧
    checkNat 578 = true ∧
    checkNat 579 = true ∧
    checkNat 580 = true ∧
    checkNat 581 = true ∧
    checkNat 582 = true ∧
    checkNat 583 = true ∧
    checkNat 584 = true ∧
    checkNat 585 = true ∧
    checkNat 586 = true ∧
    checkNat 587 = true ∧
    checkNat 588 = true ∧
    checkNat 589 = true ∧
    checkNat 590 = true ∧
    checkNat 591 = true ∧
    checkNat 592 = true ∧
    checkNat 593 = true ∧
    checkNat 594 = true ∧
    checkNat 595 = true ∧
    checkNat 596 = true ∧
    checkNat 597 = true ∧
    checkNat 598 = true ∧
    checkNat 599 = true ∧
    checkNat 600 = true ∧
    checkNat 601 = true ∧
    checkNat 602 = true ∧
    checkNat 603 = true ∧
    checkNat 604 = true ∧
    checkNat 605 = true ∧
    checkNat 606 = true ∧
    checkNat 607 = true ∧
    checkNat 1600 = true ∧
    checkNat 1602 = true ∧
    checkNat 1604 = true ∧
    checkNat 1606 = true ∧
    checkNat 1608 = true ∧
    checkNat 1610 = true ∧
    checkNat 1612 = true ∧
    checkNat 1614 = true ∧
    checkNat 1616 = true ∧
    checkNat 1618 = true ∧
    checkNat 1620 = true ∧
    checkNat 1622 = true ∧
    checkNat 1624 = true ∧
    checkNat 1626 = true ∧
    checkNat 1628 = true ∧
    checkNat 1630 = true ∧
    checkNat 2624 = true ∧
    checkNat 2625 = true ∧
    checkNat 2628 = true ∧
    checkNat 2629 = true ∧
    checkNat 2632 = true ∧
    checkNat 2633 = true ∧
    checkNat 2636 = true ∧
    checkNat 2637 = true ∧
    checkNat 2640 = true ∧
    checkNat 2641 = true ∧
    checkNat 2644 = true ∧
    checkNat 2645 = true ∧
    checkNat 2648 = true ∧
    checkNat 2649 = true ∧
    checkNat 2652 = true ∧
    checkNat 2653 = true ∧
    checkNat 3648 = true ∧
    checkNat 3652 = true ∧
    checkNat 3656 = true ∧
    checkNat 3660 = true ∧
    checkNat 3664 = true ∧
    checkNat 3668 = true ∧
    checkNat 3672 = true ∧
    checkNat 3676 = true := by
  exact ⟨case0576, case0577, case0578, case0579, case0580, case0581, case0582, case0583, case0584, case0585, case0586, case0587, case0588, case0589, case0590, case0591, case0592, case0593, case0594, case0595, case0596, case0597, case0598, case0599, case0600, case0601, case0602, case0603, case0604, case0605, case0606, case0607, case1600, case1602, case1604, case1606, case1608, case1610, case1612, case1614, case1616, case1618, case1620, case1622, case1624, case1626, case1628, case1630, case2624, case2625, case2628, case2629, case2632, case2633, case2636, case2637, case2640, case2641, case2644, case2645, case2648, case2649, case2652, case2653, case3648, case3652, case3656, case3660, case3664, case3668, case3672, case3676⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0576
