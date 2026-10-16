import Shard0000
import Shard0032
import Shard1024
import Shard1536
import Shard2048

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block048 (k : ℕ) (hk : k < 64) : checkNat (3072 + k) = true := by
  interval_cases k
  · exact Shard0000.case3072
  · exact Shard1024.case3073
  · exact Shard1536.case3074
  · exact Shard2048.case3075
  · exact Shard0000.case3076
  · exact Shard1024.case3077
  · exact Shard1536.case3078
  · exact Shard2048.case3079
  · exact Shard0000.case3080
  · exact Shard1024.case3081
  · exact Shard1536.case3082
  · exact Shard2048.case3083
  · exact Shard0000.case3084
  · exact Shard1024.case3085
  · exact Shard1536.case3086
  · exact Shard2048.case3087
  · exact Shard0000.case3088
  · exact Shard1024.case3089
  · exact Shard1536.case3090
  · exact Shard2048.case3091
  · exact Shard0000.case3092
  · exact Shard1024.case3093
  · exact Shard1536.case3094
  · exact Shard2048.case3095
  · exact Shard0000.case3096
  · exact Shard1024.case3097
  · exact Shard1536.case3098
  · exact Shard2048.case3099
  · exact Shard0000.case3100
  · exact Shard1024.case3101
  · exact Shard1536.case3102
  · exact Shard2048.case3103
  · exact Shard0032.case3104
  · exact Shard1024.case3105
  · exact Shard1536.case3106
  · exact Shard2048.case3107
  · exact Shard0032.case3108
  · exact Shard1024.case3109
  · exact Shard1536.case3110
  · exact Shard2048.case3111
  · exact Shard0032.case3112
  · exact Shard1024.case3113
  · exact Shard1536.case3114
  · exact Shard2048.case3115
  · exact Shard0032.case3116
  · exact Shard1024.case3117
  · exact Shard1536.case3118
  · exact Shard2048.case3119
  · exact Shard0032.case3120
  · exact Shard1024.case3121
  · exact Shard1536.case3122
  · exact Shard2048.case3123
  · exact Shard0032.case3124
  · exact Shard1024.case3125
  · exact Shard1536.case3126
  · exact Shard2048.case3127
  · exact Shard0032.case3128
  · exact Shard1024.case3129
  · exact Shard1536.case3130
  · exact Shard2048.case3131
  · exact Shard0032.case3132
  · exact Shard1024.case3133
  · exact Shard1536.case3134
  · exact Shard2048.case3135
end Sq19.Endgame.Reduction.Aggregate
