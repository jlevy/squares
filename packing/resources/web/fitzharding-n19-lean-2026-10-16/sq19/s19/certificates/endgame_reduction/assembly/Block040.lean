import Shard0512
import Shard0544
import Shard1792

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block040 (k : ℕ) (hk : k < 64) : checkNat (2560 + k) = true := by
  interval_cases k
  · exact Shard0512.case2560
  · exact Shard0512.case2561
  · exact Shard1792.case2562
  · exact Shard1792.case2563
  · exact Shard0512.case2564
  · exact Shard0512.case2565
  · exact Shard1792.case2566
  · exact Shard1792.case2567
  · exact Shard0512.case2568
  · exact Shard0512.case2569
  · exact Shard1792.case2570
  · exact Shard1792.case2571
  · exact Shard0512.case2572
  · exact Shard0512.case2573
  · exact Shard1792.case2574
  · exact Shard1792.case2575
  · exact Shard0512.case2576
  · exact Shard0512.case2577
  · exact Shard1792.case2578
  · exact Shard1792.case2579
  · exact Shard0512.case2580
  · exact Shard0512.case2581
  · exact Shard1792.case2582
  · exact Shard1792.case2583
  · exact Shard0512.case2584
  · exact Shard0512.case2585
  · exact Shard1792.case2586
  · exact Shard1792.case2587
  · exact Shard0512.case2588
  · exact Shard0512.case2589
  · exact Shard1792.case2590
  · exact Shard1792.case2591
  · exact Shard0544.case2592
  · exact Shard0544.case2593
  · exact Shard1792.case2594
  · exact Shard1792.case2595
  · exact Shard0544.case2596
  · exact Shard0544.case2597
  · exact Shard1792.case2598
  · exact Shard1792.case2599
  · exact Shard0544.case2600
  · exact Shard0544.case2601
  · exact Shard1792.case2602
  · exact Shard1792.case2603
  · exact Shard0544.case2604
  · exact Shard0544.case2605
  · exact Shard1792.case2606
  · exact Shard1792.case2607
  · exact Shard0544.case2608
  · exact Shard0544.case2609
  · exact Shard1792.case2610
  · exact Shard1792.case2611
  · exact Shard0544.case2612
  · exact Shard0544.case2613
  · exact Shard1792.case2614
  · exact Shard1792.case2615
  · exact Shard0544.case2616
  · exact Shard0544.case2617
  · exact Shard1792.case2618
  · exact Shard1792.case2619
  · exact Shard0544.case2620
  · exact Shard0544.case2621
  · exact Shard1792.case2622
  · exact Shard1792.case2623
end Sq19.Endgame.Reduction.Aggregate
