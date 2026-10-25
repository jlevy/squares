import S12.DomainSpecs
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def singleSpec0 : SingleSpec := ⟨1,0,1,1,[{2}],[0,1,5,9,14,20,27,35,44]⟩
theorem singleSpec0_checked : singleSpec0.Check := by native_decide
def singleSpec1 : SingleSpec := ⟨1,0,1,2,[{2}],[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53]⟩
theorem singleSpec1_checked : singleSpec1.Check := by native_decide
def singleSpec2 : SingleSpec := ⟨1,1,1,1,[{2}],[54,55,58,62,67,73,80,88,97]⟩
theorem singleSpec2_checked : singleSpec2.Check := by native_decide
def singleSpec3 : SingleSpec := ⟨1,1,1,2,[{2},{0,2}],[54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106]⟩
theorem singleSpec3_checked : singleSpec3.Check := by native_decide
def singleSpec4 : SingleSpec := ⟨2,0,1,1,[{0}],[107,109,111,115,120,126,133,141,150]⟩
theorem singleSpec4_checked : singleSpec4.Check := by native_decide
def singleSpec5 : SingleSpec := ⟨2,0,1,2,[{0},{0,2}],[107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159]⟩
theorem singleSpec5_checked : singleSpec5.Check := by native_decide
def singleSpec6 : SingleSpec := ⟨2,1,1,1,[{0}],[160,162,165,169,174,180,187,195,204]⟩
theorem singleSpec6_checked : singleSpec6.Check := by native_decide
def singleSpec7 : SingleSpec := ⟨2,1,1,2,[{0}],[160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213]⟩
theorem singleSpec7_checked : singleSpec7.Check := by native_decide
def singleSpec8 : SingleSpec := ⟨4,0,1,1,[{6}],[214,215,217,220,224,229,241,249,258]⟩
theorem singleSpec8_checked : singleSpec8.Check := by native_decide
def singleSpec9 : SingleSpec := ⟨4,0,1,2,[{6}],[214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267]⟩
theorem singleSpec9_checked : singleSpec9.Check := by native_decide
def singleSpec10 : SingleSpec := ⟨4,1,1,1,[{5}],[268,269,270,271,272,273,274,275,276]⟩
theorem singleSpec10_checked : singleSpec10.Check := by native_decide
def singleSpec11 : SingleSpec := ⟨8,0,1,1,[{8}],[277,278,280,283,287,292,298,305,320]⟩
theorem singleSpec11_checked : singleSpec11.Check := by native_decide
def singleSpec12 : SingleSpec := ⟨8,0,1,2,[{8},{6,8}],[277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329]⟩
theorem singleSpec12_checked : singleSpec12.Check := by native_decide
def singleSpec13 : SingleSpec := ⟨8,1,1,1,[{8}],[330,331,332,333,334,335,336,337,338]⟩
theorem singleSpec13_checked : singleSpec13.Check := by native_decide
def singleSpec14 : SingleSpec := ⟨16,0,1,1,[{7}],[339,340,342,345,349,354,360,374,383]⟩
theorem singleSpec14_checked : singleSpec14.Check := by native_decide
def singleSpec15 : SingleSpec := ⟨16,0,1,2,[{7}],[339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392]⟩
theorem singleSpec15_checked : singleSpec15.Check := by native_decide
end S12
