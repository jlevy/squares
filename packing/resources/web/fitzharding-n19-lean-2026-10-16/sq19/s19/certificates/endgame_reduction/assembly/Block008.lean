import Shard0512
import Shard0544

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block008 (k : ℕ) (hk : k < 64) : checkNat (512 + k) = true := by
  interval_cases k
  · exact Shard0512.case0512
  · exact Shard0512.case0513
  · exact Shard0512.case0514
  · exact Shard0512.case0515
  · exact Shard0512.case0516
  · exact Shard0512.case0517
  · exact Shard0512.case0518
  · exact Shard0512.case0519
  · exact Shard0512.case0520
  · exact Shard0512.case0521
  · exact Shard0512.case0522
  · exact Shard0512.case0523
  · exact Shard0512.case0524
  · exact Shard0512.case0525
  · exact Shard0512.case0526
  · exact Shard0512.case0527
  · exact Shard0512.case0528
  · exact Shard0512.case0529
  · exact Shard0512.case0530
  · exact Shard0512.case0531
  · exact Shard0512.case0532
  · exact Shard0512.case0533
  · exact Shard0512.case0534
  · exact Shard0512.case0535
  · exact Shard0512.case0536
  · exact Shard0512.case0537
  · exact Shard0512.case0538
  · exact Shard0512.case0539
  · exact Shard0512.case0540
  · exact Shard0512.case0541
  · exact Shard0512.case0542
  · exact Shard0512.case0543
  · exact Shard0544.case0544
  · exact Shard0544.case0545
  · exact Shard0544.case0546
  · exact Shard0544.case0547
  · exact Shard0544.case0548
  · exact Shard0544.case0549
  · exact Shard0544.case0550
  · exact Shard0544.case0551
  · exact Shard0544.case0552
  · exact Shard0544.case0553
  · exact Shard0544.case0554
  · exact Shard0544.case0555
  · exact Shard0544.case0556
  · exact Shard0544.case0557
  · exact Shard0544.case0558
  · exact Shard0544.case0559
  · exact Shard0544.case0560
  · exact Shard0544.case0561
  · exact Shard0544.case0562
  · exact Shard0544.case0563
  · exact Shard0544.case0564
  · exact Shard0544.case0565
  · exact Shard0544.case0566
  · exact Shard0544.case0567
  · exact Shard0544.case0568
  · exact Shard0544.case0569
  · exact Shard0544.case0570
  · exact Shard0544.case0571
  · exact Shard0544.case0572
  · exact Shard0544.case0573
  · exact Shard0544.case0574
  · exact Shard0544.case0575
end Sq19.Endgame.Reduction.Aggregate
