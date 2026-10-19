import Shard0256
import Shard0288
import Shard1152

set_option maxRecDepth 300000
set_option maxHeartbeats 0
namespace Sq19.Endgame.Reduction.Aggregate
theorem block020 (k : ℕ) (hk : k < 64) : checkNat (1280 + k) = true := by
  interval_cases k
  · exact Shard0256.case1280
  · exact Shard1152.case1281
  · exact Shard0256.case1282
  · exact Shard1152.case1283
  · exact Shard0256.case1284
  · exact Shard1152.case1285
  · exact Shard0256.case1286
  · exact Shard1152.case1287
  · exact Shard0256.case1288
  · exact Shard1152.case1289
  · exact Shard0256.case1290
  · exact Shard1152.case1291
  · exact Shard0256.case1292
  · exact Shard1152.case1293
  · exact Shard0256.case1294
  · exact Shard1152.case1295
  · exact Shard0256.case1296
  · exact Shard1152.case1297
  · exact Shard0256.case1298
  · exact Shard1152.case1299
  · exact Shard0256.case1300
  · exact Shard1152.case1301
  · exact Shard0256.case1302
  · exact Shard1152.case1303
  · exact Shard0256.case1304
  · exact Shard1152.case1305
  · exact Shard0256.case1306
  · exact Shard1152.case1307
  · exact Shard0256.case1308
  · exact Shard1152.case1309
  · exact Shard0256.case1310
  · exact Shard1152.case1311
  · exact Shard0288.case1312
  · exact Shard1152.case1313
  · exact Shard0288.case1314
  · exact Shard1152.case1315
  · exact Shard0288.case1316
  · exact Shard1152.case1317
  · exact Shard0288.case1318
  · exact Shard1152.case1319
  · exact Shard0288.case1320
  · exact Shard1152.case1321
  · exact Shard0288.case1322
  · exact Shard1152.case1323
  · exact Shard0288.case1324
  · exact Shard1152.case1325
  · exact Shard0288.case1326
  · exact Shard1152.case1327
  · exact Shard0288.case1328
  · exact Shard1152.case1329
  · exact Shard0288.case1330
  · exact Shard1152.case1331
  · exact Shard0288.case1332
  · exact Shard1152.case1333
  · exact Shard0288.case1334
  · exact Shard1152.case1335
  · exact Shard0288.case1336
  · exact Shard1152.case1337
  · exact Shard0288.case1338
  · exact Shard1152.case1339
  · exact Shard0288.case1340
  · exact Shard1152.case1341
  · exact Shard0288.case1342
  · exact Shard1152.case1343
end Sq19.Endgame.Reduction.Aggregate
