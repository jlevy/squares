import Shard0512
import Shard0544
import Shard1280
import Shard1792
import Shard2176

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block056 (k : ℕ) (hk : k < 64) : checkNat (3584 + k) = true := by
  interval_cases k
  · exact Shard0512.case3584
  · exact Shard1280.case3585
  · exact Shard1792.case3586
  · exact Shard2176.case3587
  · exact Shard0512.case3588
  · exact Shard1280.case3589
  · exact Shard1792.case3590
  · exact Shard2176.case3591
  · exact Shard0512.case3592
  · exact Shard1280.case3593
  · exact Shard1792.case3594
  · exact Shard2176.case3595
  · exact Shard0512.case3596
  · exact Shard1280.case3597
  · exact Shard1792.case3598
  · exact Shard2176.case3599
  · exact Shard0512.case3600
  · exact Shard1280.case3601
  · exact Shard1792.case3602
  · exact Shard2176.case3603
  · exact Shard0512.case3604
  · exact Shard1280.case3605
  · exact Shard1792.case3606
  · exact Shard2176.case3607
  · exact Shard0512.case3608
  · exact Shard1280.case3609
  · exact Shard1792.case3610
  · exact Shard2176.case3611
  · exact Shard0512.case3612
  · exact Shard1280.case3613
  · exact Shard1792.case3614
  · exact Shard2176.case3615
  · exact Shard0544.case3616
  · exact Shard1280.case3617
  · exact Shard1792.case3618
  · exact Shard2176.case3619
  · exact Shard0544.case3620
  · exact Shard1280.case3621
  · exact Shard1792.case3622
  · exact Shard2176.case3623
  · exact Shard0544.case3624
  · exact Shard1280.case3625
  · exact Shard1792.case3626
  · exact Shard2176.case3627
  · exact Shard0544.case3628
  · exact Shard1280.case3629
  · exact Shard1792.case3630
  · exact Shard2176.case3631
  · exact Shard0544.case3632
  · exact Shard1280.case3633
  · exact Shard1792.case3634
  · exact Shard2176.case3635
  · exact Shard0544.case3636
  · exact Shard1280.case3637
  · exact Shard1792.case3638
  · exact Shard2176.case3639
  · exact Shard0544.case3640
  · exact Shard1280.case3641
  · exact Shard1792.case3642
  · exact Shard2176.case3643
  · exact Shard0544.case3644
  · exact Shard1280.case3645
  · exact Shard1792.case3646
  · exact Shard2176.case3647
end Sq19.Endgame.Reduction.Aggregate
