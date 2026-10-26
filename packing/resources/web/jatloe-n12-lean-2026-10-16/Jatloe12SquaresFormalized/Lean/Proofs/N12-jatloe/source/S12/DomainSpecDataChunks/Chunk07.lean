import S12.DomainSpecs
import S12.DomainSpecDataChunks.Chunk01
import S12.DomainSpecDataChunks.Chunk02
import S12.DomainSpecDataChunks.Chunk03
import S12.DomainSpecDataChunks.Chunk04
import S12.DomainSpecDataChunks.Chunk05
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def combinedSpec9 : CombinedSpec := ⟨524,⟨singleSpec31,singleSpec31_checked⟩,⟨singleSpec32,singleSpec32_checked⟩,[],[743]⟩
theorem combinedSpec9_checked : combinedSpec9.Check := by native_decide
def combinedSpec10 : CombinedSpec := ⟨1040,⟨singleSpec36,singleSpec36_checked⟩,⟨singleSpec37,singleSpec37_checked⟩,[{7,17},{7,19},{9,19}],[783]⟩
theorem combinedSpec10_checked : combinedSpec10.Check := by native_decide
def combinedSpec11 : CombinedSpec := ⟨1072,⟨singleSpec39,singleSpec39_checked⟩,⟨singleSpec40,singleSpec40_checked⟩,[{19},{7},{7,17},{7,19},{9,19}],[808,810,809,811]⟩
theorem combinedSpec11_checked : combinedSpec11.Check := by native_decide
def combinedSpec12 : CombinedSpec := ⟨2048,⟨singleSpec42,singleSpec42_checked⟩,⟨singleSpec44,singleSpec44_checked⟩,[{1,11},{1,13},{1,14},{3,11},{3,13},{3,14},{5,11},{5,13},{5,14}],[]⟩
theorem combinedSpec12_checked : combinedSpec12.Check := by native_decide
def combinedSpec13 : CombinedSpec := ⟨2048,⟨singleSpec43,singleSpec43_checked⟩,⟨singleSpec45,singleSpec45_checked⟩,[{1,11},{1,13},{1,14},{1,11,13},{1,11,14},{1,13,14},{3,11},{3,13},{3,14},{3,11,13},{3,11,14},{3,13,14},{5,11},{5,13},{5,14},{5,11,13},{5,11,14},{5,13,14},{5,13,16},{5,13,17},{5,14,16},{5,14,17},{0,1,13},{0,1,10,13},{0,1,11,13},{0,1,13,14},{0,5,13},{0,5,13,14},{0,5,13,16},{0,5,13,17},{1,3,11},{1,3,13},{1,3,14},{1,3,11,13},{1,3,11,14},{1,3,13,14},{1,4,13},{1,4,11,13},{1,4,13,14},{1,5,11},{1,5,13},{1,5,14},{1,5,11,13},{1,5,11,14},{1,5,13,14},{1,5,13,16},{1,5,13,17},{1,5,14,16},{1,5,14,17},{3,5,11},{3,5,13},{3,5,14},{3,5,11,13},{3,5,11,14},{3,5,13,14},{3,5,13,16},{3,5,14,16},{3,5,14,17},{4,5,13},{4,5,11,13},{4,5,13,14},{4,5,13,16},{4,5,13,17},{5,7,14,17}],[907,930,944,936,951,908,932,946,938,953,911,901,919,924,931,945,937,952,903,921,912,917,926,941,956,909,933,947,939,954,902,920,910,925,934,948,940,955,913,914,949,904,922,915,927,942,957,905,906,923,916,918,928,929,935,950,943]⟩
theorem combinedSpec13_checked : combinedSpec13.Check := by native_decide
def combinedSpec14 : CombinedSpec := ⟨2240,⟨singleSpec47,singleSpec47_checked⟩,⟨singleSpec49,singleSpec49_checked⟩,[],[974]⟩
theorem combinedSpec14_checked : combinedSpec14.Check := by native_decide
def combinedSpec15 : CombinedSpec := ⟨2240,⟨singleSpec48,singleSpec48_checked⟩,⟨singleSpec49,singleSpec49_checked⟩,[{3}],[974,975]⟩
theorem combinedSpec15_checked : combinedSpec15.Check := by native_decide
def combinedSpec16 : CombinedSpec := ⟨4096,⟨singleSpec55,singleSpec55_checked⟩,⟨singleSpec57,singleSpec57_checked⟩,[{0,10},{1,11}],[1090,1096,1088,1097]⟩
theorem combinedSpec16_checked : combinedSpec16.Check := by native_decide
def combinedSpec17 : CombinedSpec := ⟨4096,⟨singleSpec56,singleSpec56_checked⟩,⟨singleSpec58,singleSpec58_checked⟩,[{0,10},{0,10,13},{1,11},{1,11,13},{0,1,10},{0,1,11},{0,1,10,11},{0,1,10,13},{0,1,11,13},{0,2,10},{1,3,11}],[1090,1096,1092,1104,1088,1097,1093,1101,1098,1091,1099,1094,1102,1105,1089,1100,1095,1103,1106]⟩
theorem combinedSpec17_checked : combinedSpec17.Check := by native_decide
def combinedSpec18 : CombinedSpec := ⟨8192,⟨singleSpec66,singleSpec66_checked⟩,⟨singleSpec68,singleSpec68_checked⟩,[{2,12},{6,15}],[1253,1244,1254,1245]⟩
theorem combinedSpec18_checked : combinedSpec18.Check := by native_decide
def combinedSpec19 : CombinedSpec := ⟨8192,⟨singleSpec67,singleSpec67_checked⟩,⟨singleSpec69,singleSpec69_checked⟩,[{2,12},{2,10,12},{2,12,15},{6,15},{6,12,15},{6,15,18},{2,4,12},{2,4,12,15},{2,6,12,15},{4,6,15},{4,6,12,15}],[1253,1258,1244,1254,1248,1257,1259,1245,1250,1255,1249,1260,1246,1256,1251,1261,1247,1252,1262]⟩
theorem combinedSpec19_checked : combinedSpec19.Check := by native_decide
def combinedSpec20 : CombinedSpec := ⟨16384,⟨singleSpec75,singleSpec75_checked⟩,⟨singleSpec77,singleSpec77_checked⟩,[{8,18},{9,19}],[1393,1403,1395,1398]⟩
theorem combinedSpec20_checked : combinedSpec20.Check := by native_decide
def combinedSpec21 : CombinedSpec := ⟨16384,⟨singleSpec76,singleSpec76_checked⟩,⟨singleSpec78,singleSpec78_checked⟩,[{8,18},{8,16,18},{9,19},{9,16,19},{6,8,18},{7,9,19},{8,9,18},{8,9,19},{8,9,16,18},{8,9,16,19},{8,9,18,19}],[1393,1403,1405,1408,1395,1398,1401,1410,1394,1404,1400,1406,1409,1396,1399,1402,1407,1411,1397]⟩
theorem combinedSpec21_checked : combinedSpec21.Check := by native_decide
def combinedSpec22 : CombinedSpec := ⟨32768,⟨singleSpec88,singleSpec88_checked⟩,⟨singleSpec90,singleSpec90_checked⟩,[{3,14},{7,17}],[1644,1635,1645,1636]⟩
theorem combinedSpec22_checked : combinedSpec22.Check := by native_decide
def combinedSpec23 : CombinedSpec := ⟨32768,⟨singleSpec89,singleSpec89_checked⟩,⟨singleSpec90,singleSpec90_checked⟩,[{3,14},{7,17},{3,5,14},{5,7,17}],[1644,1635,1645,1636,1646,1637,1647,1638]⟩
theorem combinedSpec23_checked : combinedSpec23.Check := by native_decide
def combinedSpec24 : CombinedSpec := ⟨32768,⟨singleSpec89,singleSpec89_checked⟩,⟨singleSpec91,singleSpec91_checked⟩,[{3,14},{3,11,14},{3,14,17},{7,17},{7,14,17},{7,17,19},{3,5,14},{3,5,14,17},{3,7,14,17},{5,7,17},{5,7,14,17}],[1644,1649,1635,1645,1639,1648,1650,1636,1641,1646,1640,1651,1637,1647,1642,1652,1638,1643,1653]⟩
theorem combinedSpec24_checked : combinedSpec24.Check := by native_decide
end S12
