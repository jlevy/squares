import S12.DomainSpecs
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def singleSpec32 : SingleSpec := ⟨524,1,0,0,[∅],[]⟩
theorem singleSpec32_checked : singleSpec32.Check := by native_decide
def singleSpec33 : SingleSpec := ⟨768,0,1,1,[{4}],[744,745,746,747,748,749,750,751,752]⟩
theorem singleSpec33_checked : singleSpec33.Check := by native_decide
def singleSpec34 : SingleSpec := ⟨1024,0,1,1,[{5},{7},{9}],[753,754,755,756,757,758,759]⟩
theorem singleSpec34_checked : singleSpec34.Check := by native_decide
def singleSpec35 : SingleSpec := ⟨1024,1,1,1,[{6},{7},{9}],[760,761,762,763,764,765,766]⟩
theorem singleSpec35_checked : singleSpec35.Check := by native_decide
def singleSpec36 : SingleSpec := ⟨1040,0,1,1,[{7},{9}],[767,768,769,770,771,772,773,774]⟩
theorem singleSpec36_checked : singleSpec36.Check := by native_decide
def singleSpec37 : SingleSpec := ⟨1040,1,1,1,[{7},{9}],[775,776,777,778,779,780,781,782]⟩
theorem singleSpec37_checked : singleSpec37.Check := by native_decide
def singleSpec38 : SingleSpec := ⟨1056,0,1,1,[{7},{9}],[784,785,786,787,788,789,790,791]⟩
theorem singleSpec38_checked : singleSpec38.Check := by native_decide
def singleSpec39 : SingleSpec := ⟨1072,0,0,1,[∅,{7},{9}],[792,793,794,795,796,797,798,799]⟩
theorem singleSpec39_checked : singleSpec39.Check := by native_decide
def singleSpec40 : SingleSpec := ⟨1072,1,0,1,[∅,{7},{9}],[800,801,802,803,804,805,806,807]⟩
theorem singleSpec40_checked : singleSpec40.Check := by native_decide
def singleSpec41 : SingleSpec := ⟨1792,0,0,0,[],[812]⟩
theorem singleSpec41_checked : singleSpec41.Check := by native_decide
def singleSpec42 : SingleSpec := ⟨2048,0,1,1,[{1},{3},{5}],[813,814,819,824,831,838,847]⟩
theorem singleSpec42_checked : singleSpec42.Check := by native_decide
def singleSpec43 : SingleSpec := ⟨2048,0,1,2,[{1},{3},{5},{0,1},{0,5},{1,3},{1,4},{1,5},{3,5},{4,5},{5,7}],[813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830,831,832,833,834,835,836,837,838,839,840,841,842,843,844,845,846,847,848,849,850,851,852,853,854,855,856]⟩
theorem singleSpec43_checked : singleSpec43.Check := by native_decide
def singleSpec44 : SingleSpec := ⟨2048,1,1,1,[{1},{3},{4}],[857,859,865,871,876,882,891]⟩
theorem singleSpec44_checked : singleSpec44.Check := by native_decide
def singleSpec45 : SingleSpec := ⟨2048,1,1,2,[{1},{3},{4},{0,3},{1,3},{1,4},{3,4},{3,6},{3,7},{4,6},{4,7}],[857,858,859,860,861,862,863,864,865,866,867,868,869,870,871,872,873,874,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,895,896,897,898,899,900]⟩
theorem singleSpec45_checked : singleSpec45.Check := by native_decide
def singleSpec46 : SingleSpec := ⟨2176,0,1,1,[{1},{3}],[958,959,960,961,962,963,964,965]⟩
theorem singleSpec46_checked : singleSpec46.Check := by native_decide
def singleSpec47 : SingleSpec := ⟨2240,0,0,0,[∅],[]⟩
theorem singleSpec47_checked : singleSpec47.Check := by native_decide
end S12
