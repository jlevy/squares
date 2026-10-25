import S12.DomainSpecs
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def singleSpec48 : SingleSpec := ⟨2240,0,0,1,[∅,{1},{3}],[966,967,968,969,970,971,972,973]⟩
theorem singleSpec48_checked : singleSpec48.Check := by native_decide
def singleSpec49 : SingleSpec := ⟨2240,1,0,0,[∅],[]⟩
theorem singleSpec49_checked : singleSpec49.Check := by native_decide
def singleSpec50 : SingleSpec := ⟨2816,0,0,0,[],[976]⟩
theorem singleSpec50_checked : singleSpec50.Check := by native_decide
def singleSpec51 : SingleSpec := ⟨2816,0,0,1,[{4}],[976,977,978,979,980,981,982,983,984,985]⟩
theorem singleSpec51_checked : singleSpec51.Check := by native_decide
def singleSpec52 : SingleSpec := ⟨3328,0,0,0,[],[986]⟩
theorem singleSpec52_checked : singleSpec52.Check := by native_decide
def singleSpec53 : SingleSpec := ⟨3584,0,0,0,[],[987]⟩
theorem singleSpec53_checked : singleSpec53.Check := by native_decide
def singleSpec54 : SingleSpec := ⟨3840,0,0,0,[],[988]⟩
theorem singleSpec54_checked : singleSpec54.Check := by native_decide
def singleSpec55 : SingleSpec := ⟨4096,0,1,1,[{0},{1}],[989,991,994,999,1005,1012,1020,1029]⟩
theorem singleSpec55_checked : singleSpec55.Check := by native_decide
def singleSpec56 : SingleSpec := ⟨4096,0,1,2,[{0},{1},{0,1},{0,2},{1,3}],[989,990,991,992,993,994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016,1017,1018,1019,1020,1021,1022,1023,1024,1025,1026,1027,1028,1029,1030,1031,1032,1033,1034,1035,1036,1037,1038]⟩
theorem singleSpec56_checked : singleSpec56.Check := by native_decide
def singleSpec57 : SingleSpec := ⟨4096,1,1,1,[{0},{1},{3}],[1039,1043,1048,1054,1061,1069,1078]⟩
theorem singleSpec57_checked : singleSpec57.Check := by native_decide
def singleSpec58 : SingleSpec := ⟨4096,1,1,2,[{0},{1},{3},{0,1},{0,3},{1,3}],[1039,1040,1041,1042,1043,1044,1045,1046,1047,1048,1049,1050,1051,1052,1053,1054,1055,1056,1057,1058,1059,1060,1061,1062,1063,1064,1065,1066,1067,1068,1069,1070,1071,1072,1073,1074,1075,1076,1077,1078,1079,1080,1081,1082,1083,1084,1085,1086,1087]⟩
theorem singleSpec58_checked : singleSpec58.Check := by native_decide
def singleSpec59 : SingleSpec := ⟨4098,0,1,1,[{0}],[1107,1108,1109,1110,1111,1112,1113,1114,1115]⟩
theorem singleSpec59_checked : singleSpec59.Check := by native_decide
def singleSpec60 : SingleSpec := ⟨4160,0,1,1,[],[1116,1117,1118,1119,1120,1121,1122,1123,1124,1125]⟩
theorem singleSpec60_checked : singleSpec60.Check := by native_decide
def singleSpec61 : SingleSpec := ⟨4224,1,1,1,[{1}],[1126,1127,1128,1129,1130,1131,1132,1133,1134]⟩
theorem singleSpec61_checked : singleSpec61.Check := by native_decide
def singleSpec62 : SingleSpec := ⟨4288,0,0,0,[],[1135]⟩
theorem singleSpec62_checked : singleSpec62.Check := by native_decide
def singleSpec63 : SingleSpec := ⟨4288,1,0,0,[],[1136]⟩
theorem singleSpec63_checked : singleSpec63.Check := by native_decide
end S12
