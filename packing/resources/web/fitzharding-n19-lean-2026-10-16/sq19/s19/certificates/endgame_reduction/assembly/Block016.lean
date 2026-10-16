import Shard0000
import Shard0032
import Shard1024

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block016 (k : ℕ) (hk : k < 64) : checkNat (1024 + k) = true := by
  interval_cases k
  · exact Shard0000.case1024
  · exact Shard1024.case1025
  · exact Shard0000.case1026
  · exact Shard1024.case1027
  · exact Shard0000.case1028
  · exact Shard1024.case1029
  · exact Shard0000.case1030
  · exact Shard1024.case1031
  · exact Shard0000.case1032
  · exact Shard1024.case1033
  · exact Shard0000.case1034
  · exact Shard1024.case1035
  · exact Shard0000.case1036
  · exact Shard1024.case1037
  · exact Shard0000.case1038
  · exact Shard1024.case1039
  · exact Shard0000.case1040
  · exact Shard1024.case1041
  · exact Shard0000.case1042
  · exact Shard1024.case1043
  · exact Shard0000.case1044
  · exact Shard1024.case1045
  · exact Shard0000.case1046
  · exact Shard1024.case1047
  · exact Shard0000.case1048
  · exact Shard1024.case1049
  · exact Shard0000.case1050
  · exact Shard1024.case1051
  · exact Shard0000.case1052
  · exact Shard1024.case1053
  · exact Shard0000.case1054
  · exact Shard1024.case1055
  · exact Shard0032.case1056
  · exact Shard1024.case1057
  · exact Shard0032.case1058
  · exact Shard1024.case1059
  · exact Shard0032.case1060
  · exact Shard1024.case1061
  · exact Shard0032.case1062
  · exact Shard1024.case1063
  · exact Shard0032.case1064
  · exact Shard1024.case1065
  · exact Shard0032.case1066
  · exact Shard1024.case1067
  · exact Shard0032.case1068
  · exact Shard1024.case1069
  · exact Shard0032.case1070
  · exact Shard1024.case1071
  · exact Shard0032.case1072
  · exact Shard1024.case1073
  · exact Shard0032.case1074
  · exact Shard1024.case1075
  · exact Shard0032.case1076
  · exact Shard1024.case1077
  · exact Shard0032.case1078
  · exact Shard1024.case1079
  · exact Shard0032.case1080
  · exact Shard1024.case1081
  · exact Shard0032.case1082
  · exact Shard1024.case1083
  · exact Shard0032.case1084
  · exact Shard1024.case1085
  · exact Shard0032.case1086
  · exact Shard1024.case1087
end Sq19.Endgame.Reduction.Aggregate
