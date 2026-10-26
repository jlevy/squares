import S12.DomainSpecs
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def singleSpec16 : SingleSpec := ⟨16,1,1,1,[{7}],[393,394,395,396,397,398,399,400,401]⟩
theorem singleSpec16_checked : singleSpec16.Check := by native_decide
def singleSpec17 : SingleSpec := ⟨32,0,1,1,[{9}],[402,403,404,405,406,407,408,409,410]⟩
theorem singleSpec17_checked : singleSpec17.Check := by native_decide
def singleSpec18 : SingleSpec := ⟨32,1,1,1,[{9}],[411,412,413,414,415,416,417,418,419]⟩
theorem singleSpec18_checked : singleSpec18.Check := by native_decide
def singleSpec19 : SingleSpec := ⟨64,0,1,1,[{3}],[420,421,422,423,424,425,426,427,428]⟩
theorem singleSpec19_checked : singleSpec19.Check := by native_decide
def singleSpec20 : SingleSpec := ⟨256,0,1,1,[{0},{2},{4}],[429,431,436,440,446,454,463]⟩
theorem singleSpec20_checked : singleSpec20.Check := by native_decide
def singleSpec21 : SingleSpec := ⟨256,0,1,2,[{0},{2},{4},{0,1},{0,2},{0,4},{0,5},{1,4},{2,4},{4,5},{4,6}],[429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472]⟩
theorem singleSpec21_checked : singleSpec21.Check := by native_decide
def singleSpec22 : SingleSpec := ⟨256,1,1,1,[{0},{2},{3}],[473,476,481,485,490,498,507]⟩
theorem singleSpec22_checked : singleSpec22.Check := by native_decide
def singleSpec23 : SingleSpec := ⟨256,1,1,2,[{0},{2},{3},{0,2},{0,3},{1,3},{2,3},{2,5},{2,6},{3,5},{3,6}],[473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516]⟩
theorem singleSpec23_checked : singleSpec23.Check := by native_decide
def singleSpec24 : SingleSpec := ⟨258,0,1,1,[{0},{2}],[574,575,576,577,578,579,580,581]⟩
theorem singleSpec24_checked : singleSpec24.Check := by native_decide
def singleSpec25 : SingleSpec := ⟨512,0,1,1,[{4},{6},{8}],[582,583,585,588,595,605,618]⟩
theorem singleSpec25_checked : singleSpec25.Check := by native_decide
def singleSpec26 : SingleSpec := ⟨512,0,1,2,[{4},{6},{8},{2,4},{4,5},{4,6},{4,8},{4,9},{5,8},{6,8},{8,9}],[582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625]⟩
theorem singleSpec26_checked : singleSpec26.Check := by native_decide
def singleSpec27 : SingleSpec := ⟨512,1,1,1,[{5},{6},{8}],[626,627,629,632,636,647,661]⟩
theorem singleSpec27_checked : singleSpec27.Check := by native_decide
def singleSpec28 : SingleSpec := ⟨512,1,1,2,[{5},{6},{8},{2,5},{2,6},{3,5},{3,6},{5,6},{5,8},{6,8},{6,9}],[626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669]⟩
theorem singleSpec28_checked : singleSpec28.Check := by native_decide
def singleSpec29 : SingleSpec := ⟨516,0,1,1,[{6},{8}],[727,728,729,730,731,732,733,734]⟩
theorem singleSpec29_checked : singleSpec29.Check := by native_decide
def singleSpec30 : SingleSpec := ⟨516,1,1,1,[{5},{8}],[735,736,737,738,739,740,741,742]⟩
theorem singleSpec30_checked : singleSpec30.Check := by native_decide
def singleSpec31 : SingleSpec := ⟨524,0,0,0,[∅],[]⟩
theorem singleSpec31_checked : singleSpec31.Check := by native_decide
end S12
