import Shard0512
import Shard0544
import Shard1280

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block024 (k : ℕ) (hk : k < 64) : checkNat (1536 + k) = true := by
  interval_cases k
  · exact Shard0512.case1536
  · exact Shard1280.case1537
  · exact Shard0512.case1538
  · exact Shard1280.case1539
  · exact Shard0512.case1540
  · exact Shard1280.case1541
  · exact Shard0512.case1542
  · exact Shard1280.case1543
  · exact Shard0512.case1544
  · exact Shard1280.case1545
  · exact Shard0512.case1546
  · exact Shard1280.case1547
  · exact Shard0512.case1548
  · exact Shard1280.case1549
  · exact Shard0512.case1550
  · exact Shard1280.case1551
  · exact Shard0512.case1552
  · exact Shard1280.case1553
  · exact Shard0512.case1554
  · exact Shard1280.case1555
  · exact Shard0512.case1556
  · exact Shard1280.case1557
  · exact Shard0512.case1558
  · exact Shard1280.case1559
  · exact Shard0512.case1560
  · exact Shard1280.case1561
  · exact Shard0512.case1562
  · exact Shard1280.case1563
  · exact Shard0512.case1564
  · exact Shard1280.case1565
  · exact Shard0512.case1566
  · exact Shard1280.case1567
  · exact Shard0544.case1568
  · exact Shard1280.case1569
  · exact Shard0544.case1570
  · exact Shard1280.case1571
  · exact Shard0544.case1572
  · exact Shard1280.case1573
  · exact Shard0544.case1574
  · exact Shard1280.case1575
  · exact Shard0544.case1576
  · exact Shard1280.case1577
  · exact Shard0544.case1578
  · exact Shard1280.case1579
  · exact Shard0544.case1580
  · exact Shard1280.case1581
  · exact Shard0544.case1582
  · exact Shard1280.case1583
  · exact Shard0544.case1584
  · exact Shard1280.case1585
  · exact Shard0544.case1586
  · exact Shard1280.case1587
  · exact Shard0544.case1588
  · exact Shard1280.case1589
  · exact Shard0544.case1590
  · exact Shard1280.case1591
  · exact Shard0544.case1592
  · exact Shard1280.case1593
  · exact Shard0544.case1594
  · exact Shard1280.case1595
  · exact Shard0544.case1596
  · exact Shard1280.case1597
  · exact Shard0544.case1598
  · exact Shard1280.case1599
end Sq19.Endgame.Reduction.Aggregate
