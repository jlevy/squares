import Shard0000
import Shard0032
import Shard1536

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block032 (k : ℕ) (hk : k < 64) : checkNat (2048 + k) = true := by
  interval_cases k
  · exact Shard0000.case2048
  · exact Shard0000.case2049
  · exact Shard1536.case2050
  · exact Shard1536.case2051
  · exact Shard0000.case2052
  · exact Shard0000.case2053
  · exact Shard1536.case2054
  · exact Shard1536.case2055
  · exact Shard0000.case2056
  · exact Shard0000.case2057
  · exact Shard1536.case2058
  · exact Shard1536.case2059
  · exact Shard0000.case2060
  · exact Shard0000.case2061
  · exact Shard1536.case2062
  · exact Shard1536.case2063
  · exact Shard0000.case2064
  · exact Shard0000.case2065
  · exact Shard1536.case2066
  · exact Shard1536.case2067
  · exact Shard0000.case2068
  · exact Shard0000.case2069
  · exact Shard1536.case2070
  · exact Shard1536.case2071
  · exact Shard0000.case2072
  · exact Shard0000.case2073
  · exact Shard1536.case2074
  · exact Shard1536.case2075
  · exact Shard0000.case2076
  · exact Shard0000.case2077
  · exact Shard1536.case2078
  · exact Shard1536.case2079
  · exact Shard0032.case2080
  · exact Shard0032.case2081
  · exact Shard1536.case2082
  · exact Shard1536.case2083
  · exact Shard0032.case2084
  · exact Shard0032.case2085
  · exact Shard1536.case2086
  · exact Shard1536.case2087
  · exact Shard0032.case2088
  · exact Shard0032.case2089
  · exact Shard1536.case2090
  · exact Shard1536.case2091
  · exact Shard0032.case2092
  · exact Shard0032.case2093
  · exact Shard1536.case2094
  · exact Shard1536.case2095
  · exact Shard0032.case2096
  · exact Shard0032.case2097
  · exact Shard1536.case2098
  · exact Shard1536.case2099
  · exact Shard0032.case2100
  · exact Shard0032.case2101
  · exact Shard1536.case2102
  · exact Shard1536.case2103
  · exact Shard0032.case2104
  · exact Shard0032.case2105
  · exact Shard1536.case2106
  · exact Shard1536.case2107
  · exact Shard0032.case2108
  · exact Shard0032.case2109
  · exact Shard1536.case2110
  · exact Shard1536.case2111
end Sq19.Endgame.Reduction.Aggregate
