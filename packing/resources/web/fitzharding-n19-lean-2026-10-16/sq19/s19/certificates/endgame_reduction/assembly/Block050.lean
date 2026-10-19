import Shard0128
import Shard0160
import Shard1088
import Shard1600
import Shard2080

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block050 (k : ℕ) (hk : k < 64) : checkNat (3200 + k) = true := by
  interval_cases k
  · exact Shard0128.case3200
  · exact Shard1088.case3201
  · exact Shard1600.case3202
  · exact Shard2080.case3203
  · exact Shard0128.case3204
  · exact Shard1088.case3205
  · exact Shard1600.case3206
  · exact Shard2080.case3207
  · exact Shard0128.case3208
  · exact Shard1088.case3209
  · exact Shard1600.case3210
  · exact Shard2080.case3211
  · exact Shard0128.case3212
  · exact Shard1088.case3213
  · exact Shard1600.case3214
  · exact Shard2080.case3215
  · exact Shard0128.case3216
  · exact Shard1088.case3217
  · exact Shard1600.case3218
  · exact Shard2080.case3219
  · exact Shard0128.case3220
  · exact Shard1088.case3221
  · exact Shard1600.case3222
  · exact Shard2080.case3223
  · exact Shard0128.case3224
  · exact Shard1088.case3225
  · exact Shard1600.case3226
  · exact Shard2080.case3227
  · exact Shard0128.case3228
  · exact Shard1088.case3229
  · exact Shard1600.case3230
  · exact Shard2080.case3231
  · exact Shard0160.case3232
  · exact Shard1088.case3233
  · exact Shard1600.case3234
  · exact Shard2080.case3235
  · exact Shard0160.case3236
  · exact Shard1088.case3237
  · exact Shard1600.case3238
  · exact Shard2080.case3239
  · exact Shard0160.case3240
  · exact Shard1088.case3241
  · exact Shard1600.case3242
  · exact Shard2080.case3243
  · exact Shard0160.case3244
  · exact Shard1088.case3245
  · exact Shard1600.case3246
  · exact Shard2080.case3247
  · exact Shard0160.case3248
  · exact Shard1088.case3249
  · exact Shard1600.case3250
  · exact Shard2080.case3251
  · exact Shard0160.case3252
  · exact Shard1088.case3253
  · exact Shard1600.case3254
  · exact Shard2080.case3255
  · exact Shard0160.case3256
  · exact Shard1088.case3257
  · exact Shard1600.case3258
  · exact Shard2080.case3259
  · exact Shard0160.case3260
  · exact Shard1088.case3261
  · exact Shard1600.case3262
  · exact Shard2080.case3263
end Sq19.Endgame.Reduction.Aggregate
