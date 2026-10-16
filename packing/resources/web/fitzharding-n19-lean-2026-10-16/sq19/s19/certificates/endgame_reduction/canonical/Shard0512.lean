import Sq19Lean.Endgame.ReductionDedup

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Shard0512
open Sq19.Endgame.Reduction

theorem case0512 : checkNat 512 = true := by native_decide
#print axioms case0512

theorem case1536 : checkNat 1536 = true := by
  apply check_of_normalize (Case.ofNat 1536)
  have he : (Case.ofNat 1536).normalize = Case.ofNat 512 := by decide
  rw [he]
  exact case0512
#print axioms case1536

theorem case2560 : checkNat 2560 = true := by
  apply check_of_normalize (Case.ofNat 2560)
  have he : (Case.ofNat 2560).normalize = Case.ofNat 512 := by decide
  rw [he]
  exact case0512
#print axioms case2560

theorem case3584 : checkNat 3584 = true := by
  apply check_of_normalize (Case.ofNat 3584)
  have he : (Case.ofNat 3584).normalize = Case.ofNat 512 := by decide
  rw [he]
  exact case0512
#print axioms case3584

theorem case0513 : checkNat 513 = true := by native_decide
#print axioms case0513

theorem case2561 : checkNat 2561 = true := by
  apply check_of_normalize (Case.ofNat 2561)
  have he : (Case.ofNat 2561).normalize = Case.ofNat 513 := by decide
  rw [he]
  exact case0513
#print axioms case2561

theorem case0514 : checkNat 514 = true := by native_decide
#print axioms case0514

theorem case1538 : checkNat 1538 = true := by
  apply check_of_normalize (Case.ofNat 1538)
  have he : (Case.ofNat 1538).normalize = Case.ofNat 514 := by decide
  rw [he]
  exact case0514
#print axioms case1538

theorem case0515 : checkNat 515 = true := by native_decide
#print axioms case0515

theorem case0516 : checkNat 516 = true := by native_decide
#print axioms case0516

theorem case1540 : checkNat 1540 = true := by
  apply check_of_normalize (Case.ofNat 1540)
  have he : (Case.ofNat 1540).normalize = Case.ofNat 516 := by decide
  rw [he]
  exact case0516
#print axioms case1540

theorem case2564 : checkNat 2564 = true := by
  apply check_of_normalize (Case.ofNat 2564)
  have he : (Case.ofNat 2564).normalize = Case.ofNat 516 := by decide
  rw [he]
  exact case0516
#print axioms case2564

theorem case3588 : checkNat 3588 = true := by
  apply check_of_normalize (Case.ofNat 3588)
  have he : (Case.ofNat 3588).normalize = Case.ofNat 516 := by decide
  rw [he]
  exact case0516
#print axioms case3588

theorem case0517 : checkNat 517 = true := by native_decide
#print axioms case0517

theorem case2565 : checkNat 2565 = true := by
  apply check_of_normalize (Case.ofNat 2565)
  have he : (Case.ofNat 2565).normalize = Case.ofNat 517 := by decide
  rw [he]
  exact case0517
#print axioms case2565

theorem case0518 : checkNat 518 = true := by native_decide
#print axioms case0518

theorem case1542 : checkNat 1542 = true := by
  apply check_of_normalize (Case.ofNat 1542)
  have he : (Case.ofNat 1542).normalize = Case.ofNat 518 := by decide
  rw [he]
  exact case0518
#print axioms case1542

theorem case0519 : checkNat 519 = true := by native_decide
#print axioms case0519

theorem case0520 : checkNat 520 = true := by native_decide
#print axioms case0520

theorem case1544 : checkNat 1544 = true := by
  apply check_of_normalize (Case.ofNat 1544)
  have he : (Case.ofNat 1544).normalize = Case.ofNat 520 := by decide
  rw [he]
  exact case0520
#print axioms case1544

theorem case2568 : checkNat 2568 = true := by
  apply check_of_normalize (Case.ofNat 2568)
  have he : (Case.ofNat 2568).normalize = Case.ofNat 520 := by decide
  rw [he]
  exact case0520
#print axioms case2568

theorem case3592 : checkNat 3592 = true := by
  apply check_of_normalize (Case.ofNat 3592)
  have he : (Case.ofNat 3592).normalize = Case.ofNat 520 := by decide
  rw [he]
  exact case0520
#print axioms case3592

theorem case0521 : checkNat 521 = true := by native_decide
#print axioms case0521

theorem case2569 : checkNat 2569 = true := by
  apply check_of_normalize (Case.ofNat 2569)
  have he : (Case.ofNat 2569).normalize = Case.ofNat 521 := by decide
  rw [he]
  exact case0521
#print axioms case2569

theorem case0522 : checkNat 522 = true := by native_decide
#print axioms case0522

theorem case1546 : checkNat 1546 = true := by
  apply check_of_normalize (Case.ofNat 1546)
  have he : (Case.ofNat 1546).normalize = Case.ofNat 522 := by decide
  rw [he]
  exact case0522
#print axioms case1546

theorem case0523 : checkNat 523 = true := by native_decide
#print axioms case0523

theorem case0524 : checkNat 524 = true := by native_decide
#print axioms case0524

theorem case1548 : checkNat 1548 = true := by
  apply check_of_normalize (Case.ofNat 1548)
  have he : (Case.ofNat 1548).normalize = Case.ofNat 524 := by decide
  rw [he]
  exact case0524
#print axioms case1548

theorem case2572 : checkNat 2572 = true := by
  apply check_of_normalize (Case.ofNat 2572)
  have he : (Case.ofNat 2572).normalize = Case.ofNat 524 := by decide
  rw [he]
  exact case0524
#print axioms case2572

theorem case3596 : checkNat 3596 = true := by
  apply check_of_normalize (Case.ofNat 3596)
  have he : (Case.ofNat 3596).normalize = Case.ofNat 524 := by decide
  rw [he]
  exact case0524
#print axioms case3596

theorem case0525 : checkNat 525 = true := by native_decide
#print axioms case0525

theorem case2573 : checkNat 2573 = true := by
  apply check_of_normalize (Case.ofNat 2573)
  have he : (Case.ofNat 2573).normalize = Case.ofNat 525 := by decide
  rw [he]
  exact case0525
#print axioms case2573

theorem case0526 : checkNat 526 = true := by native_decide
#print axioms case0526

theorem case1550 : checkNat 1550 = true := by
  apply check_of_normalize (Case.ofNat 1550)
  have he : (Case.ofNat 1550).normalize = Case.ofNat 526 := by decide
  rw [he]
  exact case0526
#print axioms case1550

theorem case0527 : checkNat 527 = true := by native_decide
#print axioms case0527

theorem case0528 : checkNat 528 = true := by native_decide
#print axioms case0528

theorem case1552 : checkNat 1552 = true := by
  apply check_of_normalize (Case.ofNat 1552)
  have he : (Case.ofNat 1552).normalize = Case.ofNat 528 := by decide
  rw [he]
  exact case0528
#print axioms case1552

theorem case2576 : checkNat 2576 = true := by
  apply check_of_normalize (Case.ofNat 2576)
  have he : (Case.ofNat 2576).normalize = Case.ofNat 528 := by decide
  rw [he]
  exact case0528
#print axioms case2576

theorem case3600 : checkNat 3600 = true := by
  apply check_of_normalize (Case.ofNat 3600)
  have he : (Case.ofNat 3600).normalize = Case.ofNat 528 := by decide
  rw [he]
  exact case0528
#print axioms case3600

theorem case0529 : checkNat 529 = true := by native_decide
#print axioms case0529

theorem case2577 : checkNat 2577 = true := by
  apply check_of_normalize (Case.ofNat 2577)
  have he : (Case.ofNat 2577).normalize = Case.ofNat 529 := by decide
  rw [he]
  exact case0529
#print axioms case2577

theorem case0530 : checkNat 530 = true := by native_decide
#print axioms case0530

theorem case1554 : checkNat 1554 = true := by
  apply check_of_normalize (Case.ofNat 1554)
  have he : (Case.ofNat 1554).normalize = Case.ofNat 530 := by decide
  rw [he]
  exact case0530
#print axioms case1554

theorem case0531 : checkNat 531 = true := by native_decide
#print axioms case0531

theorem case0532 : checkNat 532 = true := by native_decide
#print axioms case0532

theorem case1556 : checkNat 1556 = true := by
  apply check_of_normalize (Case.ofNat 1556)
  have he : (Case.ofNat 1556).normalize = Case.ofNat 532 := by decide
  rw [he]
  exact case0532
#print axioms case1556

theorem case2580 : checkNat 2580 = true := by
  apply check_of_normalize (Case.ofNat 2580)
  have he : (Case.ofNat 2580).normalize = Case.ofNat 532 := by decide
  rw [he]
  exact case0532
#print axioms case2580

theorem case3604 : checkNat 3604 = true := by
  apply check_of_normalize (Case.ofNat 3604)
  have he : (Case.ofNat 3604).normalize = Case.ofNat 532 := by decide
  rw [he]
  exact case0532
#print axioms case3604

theorem case0533 : checkNat 533 = true := by native_decide
#print axioms case0533

theorem case2581 : checkNat 2581 = true := by
  apply check_of_normalize (Case.ofNat 2581)
  have he : (Case.ofNat 2581).normalize = Case.ofNat 533 := by decide
  rw [he]
  exact case0533
#print axioms case2581

theorem case0534 : checkNat 534 = true := by native_decide
#print axioms case0534

theorem case1558 : checkNat 1558 = true := by
  apply check_of_normalize (Case.ofNat 1558)
  have he : (Case.ofNat 1558).normalize = Case.ofNat 534 := by decide
  rw [he]
  exact case0534
#print axioms case1558

theorem case0535 : checkNat 535 = true := by native_decide
#print axioms case0535

theorem case0536 : checkNat 536 = true := by native_decide
#print axioms case0536

theorem case1560 : checkNat 1560 = true := by
  apply check_of_normalize (Case.ofNat 1560)
  have he : (Case.ofNat 1560).normalize = Case.ofNat 536 := by decide
  rw [he]
  exact case0536
#print axioms case1560

theorem case2584 : checkNat 2584 = true := by
  apply check_of_normalize (Case.ofNat 2584)
  have he : (Case.ofNat 2584).normalize = Case.ofNat 536 := by decide
  rw [he]
  exact case0536
#print axioms case2584

theorem case3608 : checkNat 3608 = true := by
  apply check_of_normalize (Case.ofNat 3608)
  have he : (Case.ofNat 3608).normalize = Case.ofNat 536 := by decide
  rw [he]
  exact case0536
#print axioms case3608

theorem case0537 : checkNat 537 = true := by native_decide
#print axioms case0537

theorem case2585 : checkNat 2585 = true := by
  apply check_of_normalize (Case.ofNat 2585)
  have he : (Case.ofNat 2585).normalize = Case.ofNat 537 := by decide
  rw [he]
  exact case0537
#print axioms case2585

theorem case0538 : checkNat 538 = true := by native_decide
#print axioms case0538

theorem case1562 : checkNat 1562 = true := by
  apply check_of_normalize (Case.ofNat 1562)
  have he : (Case.ofNat 1562).normalize = Case.ofNat 538 := by decide
  rw [he]
  exact case0538
#print axioms case1562

theorem case0539 : checkNat 539 = true := by native_decide
#print axioms case0539

theorem case0540 : checkNat 540 = true := by native_decide
#print axioms case0540

theorem case1564 : checkNat 1564 = true := by
  apply check_of_normalize (Case.ofNat 1564)
  have he : (Case.ofNat 1564).normalize = Case.ofNat 540 := by decide
  rw [he]
  exact case0540
#print axioms case1564

theorem case2588 : checkNat 2588 = true := by
  apply check_of_normalize (Case.ofNat 2588)
  have he : (Case.ofNat 2588).normalize = Case.ofNat 540 := by decide
  rw [he]
  exact case0540
#print axioms case2588

theorem case3612 : checkNat 3612 = true := by
  apply check_of_normalize (Case.ofNat 3612)
  have he : (Case.ofNat 3612).normalize = Case.ofNat 540 := by decide
  rw [he]
  exact case0540
#print axioms case3612

theorem case0541 : checkNat 541 = true := by native_decide
#print axioms case0541

theorem case2589 : checkNat 2589 = true := by
  apply check_of_normalize (Case.ofNat 2589)
  have he : (Case.ofNat 2589).normalize = Case.ofNat 541 := by decide
  rw [he]
  exact case0541
#print axioms case2589

theorem case0542 : checkNat 542 = true := by native_decide
#print axioms case0542

theorem case1566 : checkNat 1566 = true := by
  apply check_of_normalize (Case.ofNat 1566)
  have he : (Case.ofNat 1566).normalize = Case.ofNat 542 := by decide
  rw [he]
  exact case0542
#print axioms case1566

theorem case0543 : checkNat 543 = true := by native_decide
#print axioms case0543

theorem accepted :
    checkNat 512 = true ∧
    checkNat 513 = true ∧
    checkNat 514 = true ∧
    checkNat 515 = true ∧
    checkNat 516 = true ∧
    checkNat 517 = true ∧
    checkNat 518 = true ∧
    checkNat 519 = true ∧
    checkNat 520 = true ∧
    checkNat 521 = true ∧
    checkNat 522 = true ∧
    checkNat 523 = true ∧
    checkNat 524 = true ∧
    checkNat 525 = true ∧
    checkNat 526 = true ∧
    checkNat 527 = true ∧
    checkNat 528 = true ∧
    checkNat 529 = true ∧
    checkNat 530 = true ∧
    checkNat 531 = true ∧
    checkNat 532 = true ∧
    checkNat 533 = true ∧
    checkNat 534 = true ∧
    checkNat 535 = true ∧
    checkNat 536 = true ∧
    checkNat 537 = true ∧
    checkNat 538 = true ∧
    checkNat 539 = true ∧
    checkNat 540 = true ∧
    checkNat 541 = true ∧
    checkNat 542 = true ∧
    checkNat 543 = true ∧
    checkNat 1536 = true ∧
    checkNat 1538 = true ∧
    checkNat 1540 = true ∧
    checkNat 1542 = true ∧
    checkNat 1544 = true ∧
    checkNat 1546 = true ∧
    checkNat 1548 = true ∧
    checkNat 1550 = true ∧
    checkNat 1552 = true ∧
    checkNat 1554 = true ∧
    checkNat 1556 = true ∧
    checkNat 1558 = true ∧
    checkNat 1560 = true ∧
    checkNat 1562 = true ∧
    checkNat 1564 = true ∧
    checkNat 1566 = true ∧
    checkNat 2560 = true ∧
    checkNat 2561 = true ∧
    checkNat 2564 = true ∧
    checkNat 2565 = true ∧
    checkNat 2568 = true ∧
    checkNat 2569 = true ∧
    checkNat 2572 = true ∧
    checkNat 2573 = true ∧
    checkNat 2576 = true ∧
    checkNat 2577 = true ∧
    checkNat 2580 = true ∧
    checkNat 2581 = true ∧
    checkNat 2584 = true ∧
    checkNat 2585 = true ∧
    checkNat 2588 = true ∧
    checkNat 2589 = true ∧
    checkNat 3584 = true ∧
    checkNat 3588 = true ∧
    checkNat 3592 = true ∧
    checkNat 3596 = true ∧
    checkNat 3600 = true ∧
    checkNat 3604 = true ∧
    checkNat 3608 = true ∧
    checkNat 3612 = true := by
  exact ⟨case0512, case0513, case0514, case0515, case0516, case0517, case0518, case0519, case0520, case0521, case0522, case0523, case0524, case0525, case0526, case0527, case0528, case0529, case0530, case0531, case0532, case0533, case0534, case0535, case0536, case0537, case0538, case0539, case0540, case0541, case0542, case0543, case1536, case1538, case1540, case1542, case1544, case1546, case1548, case1550, case1552, case1554, case1556, case1558, case1560, case1562, case1564, case1566, case2560, case2561, case2564, case2565, case2568, case2569, case2572, case2573, case2576, case2577, case2580, case2581, case2584, case2585, case2588, case2589, case3584, case3588, case3592, case3596, case3600, case3604, case3608, case3612⟩
#print axioms accepted
end Sq19.Endgame.Reduction.Shard0512
