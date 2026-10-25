import S12.DomainSpecs
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def singleSpec64 : SingleSpec := ⟨4352,0,1,1,[{0},{2},{4}],[1137,1138,1139,1140,1141,1142,1143]⟩
theorem singleSpec64_checked : singleSpec64.Check := by native_decide
def singleSpec65 : SingleSpec := ⟨6336,0,0,0,[],[1144]⟩
theorem singleSpec65_checked : singleSpec65.Check := by native_decide
def singleSpec66 : SingleSpec := ⟨8192,0,1,1,[{2},{4},{6}],[1145,1146,1150,1157,1167,1175,1184]⟩
theorem singleSpec66_checked : singleSpec66.Check := by native_decide
def singleSpec67 : SingleSpec := ⟨8192,0,1,2,[{2},{4},{6},{2,4},{2,6},{4,6}],[1145,1146,1147,1148,1149,1150,1151,1152,1153,1154,1155,1156,1157,1158,1159,1160,1161,1162,1163,1164,1165,1166,1167,1168,1169,1170,1171,1172,1173,1174,1175,1176,1177,1178,1179,1180,1181,1182,1183,1184,1185,1186,1187,1188,1189,1190,1191,1192,1193]⟩
theorem singleSpec67_checked : singleSpec67.Check := by native_decide
def singleSpec68 : SingleSpec := ⟨8192,1,1,1,[{2},{5}],[1194,1195,1198,1202,1211,1218,1226,1234]⟩
theorem singleSpec68_checked : singleSpec68.Check := by native_decide
def singleSpec69 : SingleSpec := ⟨8192,1,1,2,[{2},{5},{0,2},{2,5},{5,8}],[1194,1195,1196,1197,1198,1199,1200,1201,1202,1203,1204,1205,1206,1207,1208,1209,1210,1211,1212,1213,1214,1215,1216,1217,1218,1219,1220,1221,1222,1223,1224,1225,1226,1227,1228,1229,1230,1231,1232,1233,1234,1235,1236,1237,1238,1239,1240,1241,1242,1243]⟩
theorem singleSpec69_checked : singleSpec69.Check := by native_decide
def singleSpec70 : SingleSpec := ⟨8196,0,1,1,[{6}],[1263,1264,1265,1266,1267,1268,1269,1270,1271]⟩
theorem singleSpec70_checked : singleSpec70.Check := by native_decide
def singleSpec71 : SingleSpec := ⟨8204,0,0,0,[],[1272]⟩
theorem singleSpec71_checked : singleSpec71.Check := by native_decide
def singleSpec72 : SingleSpec := ⟨8448,0,1,1,[{2},{4},{6}],[1273,1274,1275,1276,1277,1278,1279]⟩
theorem singleSpec72_checked : singleSpec72.Check := by native_decide
def singleSpec73 : SingleSpec := ⟨8448,1,1,1,[{0},{2},{3}],[1280,1281,1282,1283,1284,1285,1286]⟩
theorem singleSpec73_checked : singleSpec73.Check := by native_decide
def singleSpec74 : SingleSpec := ⟨8704,0,1,1,[{2},{4},{6}],[1287,1288,1289,1290,1291,1292,1293]⟩
theorem singleSpec74_checked : singleSpec74.Check := by native_decide
def singleSpec75 : SingleSpec := ⟨16384,0,1,1,[{8},{9}],[1294,1295,1297,1300,1304,1309,1315,1322]⟩
theorem singleSpec75_checked : singleSpec75.Check := by native_decide
def singleSpec76 : SingleSpec := ⟨16384,0,1,2,[{8},{9},{6,8},{7,9},{8,9}],[1294,1295,1296,1297,1298,1299,1300,1301,1302,1303,1304,1305,1306,1307,1308,1309,1310,1311,1312,1313,1314,1315,1316,1317,1318,1319,1320,1321,1322,1323,1324,1325,1326,1327,1328,1329,1330,1331,1332,1333,1334,1335,1336,1337,1338,1339,1340,1341,1342,1343]⟩
theorem singleSpec76_checked : singleSpec76.Check := by native_decide
def singleSpec77 : SingleSpec := ⟨16384,1,1,1,[{6},{8},{9}],[1344,1345,1347,1350,1354,1359,1371]⟩
theorem singleSpec77_checked : singleSpec77.Check := by native_decide
def singleSpec78 : SingleSpec := ⟨16384,1,1,2,[{6},{8},{9},{6,8},{6,9},{8,9}],[1344,1345,1346,1347,1348,1349,1350,1351,1352,1353,1354,1355,1356,1357,1358,1359,1360,1361,1362,1363,1364,1365,1366,1367,1368,1369,1370,1371,1372,1373,1374,1375,1376,1377,1378,1379,1380,1381,1382,1383,1384,1385,1386,1387,1388,1389,1390,1391,1392]⟩
theorem singleSpec78_checked : singleSpec78.Check := by native_decide
def singleSpec79 : SingleSpec := ⟨16392,0,1,1,[{8}],[1412,1413,1415,1418,1422,1427,1433,1440,1455]⟩
theorem singleSpec79_checked : singleSpec79.Check := by native_decide
end S12
