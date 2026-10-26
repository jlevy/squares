import S12.DomainSpecs
import S12.DomainSpecDataChunks.Chunk00
import S12.DomainSpecDataChunks.Chunk01
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def singleSpec96 : SingleSpec := ⟨32832,1,1,1,[{4}],[1683,1684,1685,1686,1687,1688,1689,1690,1691]⟩
theorem singleSpec96_checked : singleSpec96.Check := by native_decide
def singleSpec97 : SingleSpec := ⟨32896,0,1,1,[],[1692,1693,1694,1695,1696,1697,1698,1699,1700,1701]⟩
theorem singleSpec97_checked : singleSpec97.Check := by native_decide
def singleSpec98 : SingleSpec := ⟨32960,0,0,0,[],[1702]⟩
theorem singleSpec98_checked : singleSpec98.Check := by native_decide
def singleSpec99 : SingleSpec := ⟨32960,1,0,0,[],[1703]⟩
theorem singleSpec99_checked : singleSpec99.Check := by native_decide
def singleSpec100 : SingleSpec := ⟨32960,1,0,1,[{4}],[1703,1704,1705,1706,1707,1708,1709,1710,1711,1712]⟩
theorem singleSpec100_checked : singleSpec100.Check := by native_decide
def singleSpec101 : SingleSpec := ⟨33792,1,1,1,[{6},{7},{9}],[1713,1714,1715,1716,1717,1718,1719]⟩
theorem singleSpec101_checked : singleSpec101.Check := by native_decide
def singleSpec102 : SingleSpec := ⟨35008,0,0,0,[],[1720]⟩
theorem singleSpec102_checked : singleSpec102.Check := by native_decide
def combinedSpec0 : CombinedSpec := ⟨1,⟨singleSpec0,singleSpec0_checked⟩,⟨singleSpec2,singleSpec2_checked⟩,[{2,12}],[]⟩
theorem combinedSpec0_checked : combinedSpec0.Check := by native_decide
def combinedSpec1 : CombinedSpec := ⟨1,⟨singleSpec1,singleSpec1_checked⟩,⟨singleSpec3,singleSpec3_checked⟩,[{2,12},{2,10,12}],[]⟩
theorem combinedSpec1_checked : combinedSpec1.Check := by native_decide
def combinedSpec2 : CombinedSpec := ⟨2,⟨singleSpec4,singleSpec4_checked⟩,⟨singleSpec6,singleSpec6_checked⟩,[{0,10}],[]⟩
theorem combinedSpec2_checked : combinedSpec2.Check := by native_decide
def combinedSpec3 : CombinedSpec := ⟨2,⟨singleSpec5,singleSpec5_checked⟩,⟨singleSpec7,singleSpec7_checked⟩,[{0,10},{0,2,10}],[]⟩
theorem combinedSpec3_checked : combinedSpec3.Check := by native_decide
def combinedSpec4 : CombinedSpec := ⟨16,⟨singleSpec15,singleSpec15_checked⟩,⟨singleSpec16,singleSpec16_checked⟩,[{7,17}],[]⟩
theorem combinedSpec4_checked : combinedSpec4.Check := by native_decide
def combinedSpec5 : CombinedSpec := ⟨256,⟨singleSpec20,singleSpec20_checked⟩,⟨singleSpec22,singleSpec22_checked⟩,[{0,10},{0,12},{0,13},{2,10},{2,12},{2,13},{4,10},{4,12},{4,13}],[]⟩
theorem combinedSpec5_checked : combinedSpec5.Check := by native_decide
def combinedSpec6 : CombinedSpec := ⟨256,⟨singleSpec21,singleSpec21_checked⟩,⟨singleSpec23,singleSpec23_checked⟩,[{0,10},{0,12},{0,13},{0,10,12},{0,10,13},{0,12,13},{2,10},{2,12},{2,13},{2,10,12},{2,10,13},{2,12,13},{4,10},{4,12},{4,13},{4,10,12},{4,10,13},{4,12,13},{4,12,15},{4,12,16},{4,13,15},{4,13,16},{0,1,13},{0,1,10,13},{0,1,11,13},{0,1,12,13},{0,2,10},{0,2,12},{0,2,13},{0,2,10,12},{0,2,10,13},{0,2,12,13},{0,4,10},{0,4,12},{0,4,13},{0,4,10,12},{0,4,10,13},{0,4,12,13},{0,4,12,15},{0,4,12,16},{0,4,13,15},{0,4,13,16},{0,5,13},{0,5,10,13},{0,5,12,13},{1,4,13},{1,4,12,13},{1,4,13,15},{1,4,13,16},{2,4,10},{2,4,12},{2,4,13},{2,4,10,12},{2,4,10,13},{2,4,12,13},{2,4,12,15},{2,4,12,16},{2,4,13,16},{4,5,13},{4,5,10,13},{4,5,12,13},{4,5,13,15},{4,5,13,16},{4,6,12,15}],[535,546,560,553,568,536,548,562,555,570,538,517,522,527,547,561,554,569,537,549,563,556,571,539,519,524,529,542,551,565,558,572,518,523,528,533,540,550,564,541,557,520,525,530,543,552,566,521,526,532,531,534,544,545,567,559,573]⟩
theorem combinedSpec6_checked : combinedSpec6.Check := by native_decide
def combinedSpec7 : CombinedSpec := ⟨512,⟨singleSpec25,singleSpec25_checked⟩,⟨singleSpec27,singleSpec27_checked⟩,[{4,15},{4,16},{4,18},{6,15},{6,16},{6,18},{8,15},{8,16},{8,18}],[]⟩
theorem combinedSpec7_checked : combinedSpec7.Check := by native_decide
def combinedSpec8 : CombinedSpec := ⟨512,⟨singleSpec26,singleSpec26_checked⟩,⟨singleSpec28,singleSpec28_checked⟩,[{4,15},{4,16},{4,18},{4,12,15},{4,12,16},{4,13,15},{4,13,16},{4,15,16},{4,15,18},{4,16,18},{6,15},{6,16},{6,18},{6,15,16},{6,15,18},{6,16,18},{8,15},{8,16},{8,18},{8,15,16},{8,15,18},{8,16,18},{2,4,12,15},{4,5,16},{4,5,12,16},{4,5,13,16},{4,5,15,16},{4,5,16,18},{4,6,15},{4,6,16},{4,6,18},{4,6,12,15},{4,6,13,15},{4,6,13,16},{4,6,15,16},{4,6,15,18},{4,6,16,18},{4,8,15},{4,8,16},{4,8,18},{4,8,12,15},{4,8,12,16},{4,8,13,15},{4,8,13,16},{4,8,15,16},{4,8,15,18},{4,8,16,18},{4,9,16},{4,9,12,16},{4,9,13,16},{4,9,15,16},{5,8,16},{5,8,15,16},{5,8,16,18},{6,8,15},{6,8,16},{6,8,18},{6,8,15,16},{6,8,15,18},{6,8,16,18},{8,9,16},{8,9,15,16},{8,9,16,18},{8,9,16,19}],[717,676,692,684,699,720,677,694,685,700,722,670,690,705,691,682,698,704,710,715,718,671,706,675,683,711,719,693,721,723,673,708,680,688,713,716,726,672,707,678,695,686,701,712,724,679,696,687,702,725,674,709,681,697,689,703,714]⟩
theorem combinedSpec8_checked : combinedSpec8.Check := by native_decide
end S12
