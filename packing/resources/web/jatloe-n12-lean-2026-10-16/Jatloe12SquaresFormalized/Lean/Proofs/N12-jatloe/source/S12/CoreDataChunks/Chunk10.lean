import S12.CoreExclusion
import S12.DomainSpecDataChunks.Chunk00
import S12.DomainSpecDataChunks.Chunk01
import S12.DomainSpecDataChunks.Chunk02
import S12.DomainSpecDataChunks.Chunk03
import S12.DomainSpecDataChunks.Chunk04
import S12.DomainSpecDataChunks.Chunk05
import S12.DomainSpecDataChunks.Chunk06
import S12.DomainSpecDataChunks.Chunk07
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def coreProof320 : CoreProof := ⟨{1,2,12,16,32,256,512,1024,2240,4096,8192,32768},2,[.combined combinedSpec14 combinedSpec14_checked]⟩
theorem coreProof320_checked : coreProof320.Check := by native_decide
def coreProof321 : CoreProof := ⟨{1,2,12,16,32,256,512,1024,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof321_checked : coreProof321.Check := by native_decide
def coreProof322 : CoreProof := ⟨{1,2,12,16,32,256,512,1024,4096,8192,16384,35008},0,[.single 0 singleSpec102 singleSpec102_checked]⟩
theorem coreProof322_checked : coreProof322.Check := by native_decide
def coreProof323 : CoreProof := ⟨{1,2,12,16,32,256,512,1024,4288,8192,16384,34816},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof323_checked : coreProof323.Check := by native_decide
def coreProof324 : CoreProof := ⟨{1,2,12,16,32,256,512,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof324_checked : coreProof324.Check := by native_decide
def coreProof325 : CoreProof := ⟨{1,2,12,16,32,256,512,2048,4096,8192,17408,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof325_checked : coreProof325.Check := by native_decide
def coreProof326 : CoreProof := ⟨{1,2,12,16,32,256,512,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof326_checked : coreProof326.Check := by native_decide
def coreProof327 : CoreProof := ⟨{1,2,12,16,32,256,512,2048,4288,8192,16384,33792},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof327_checked : coreProof327.Check := by native_decide
def coreProof328 : CoreProof := ⟨{1,2,12,16,32,256,512,2048,4288,8192,17408,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof328_checked : coreProof328.Check := by native_decide
def coreProof329 : CoreProof := ⟨{1,2,12,16,32,256,512,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec17 singleSpec17_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof329_checked : coreProof329.Check := by native_decide
def coreProof330 : CoreProof := ⟨{1,2,12,16,32,256,512,2240,4096,8192,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec17 singleSpec17_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof330_checked : coreProof330.Check := by native_decide
def coreProof331 : CoreProof := ⟨{1,2,12,16,32,256,512,2240,4096,8192,17408,32768},2,[.combined combinedSpec14 combinedSpec14_checked]⟩
theorem coreProof331_checked : coreProof331.Check := by native_decide
def coreProof332 : CoreProof := ⟨{1,2,12,16,32,256,512,3072,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof332_checked : coreProof332.Check := by native_decide
def coreProof333 : CoreProof := ⟨{1,2,12,16,32,256,512,3072,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof333_checked : coreProof333.Check := by native_decide
def coreProof334 : CoreProof := ⟨{1,2,12,16,32,256,1024,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof334_checked : coreProof334.Check := by native_decide
def coreProof335 : CoreProof := ⟨{1,2,12,16,32,256,1024,2048,4096,8192,16896,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof335_checked : coreProof335.Check := by native_decide
def coreProof336 : CoreProof := ⟨{1,2,12,16,32,256,1024,2048,4096,8704,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof336_checked : coreProof336.Check := by native_decide
def coreProof337 : CoreProof := ⟨{1,2,12,16,32,256,1024,2240,4096,8192,16384,32768},2,[.combined combinedSpec14 combinedSpec14_checked]⟩
theorem coreProof337_checked : coreProof337.Check := by native_decide
def coreProof338 : CoreProof := ⟨{1,2,12,16,32,256,1024,2240,4096,8192,16896,32768},2,[.combined combinedSpec14 combinedSpec14_checked]⟩
theorem coreProof338_checked : coreProof338.Check := by native_decide
def coreProof339 : CoreProof := ⟨{1,2,12,16,32,256,1536,2048,4096,8192,16384,32960},1,[.single 1 singleSpec99 singleSpec99_checked]⟩
theorem coreProof339_checked : coreProof339.Check := by native_decide
def coreProof340 : CoreProof := ⟨{1,2,12,16,32,256,1536,2048,4288,8192,16384,32768},1,[.single 1 singleSpec63 singleSpec63_checked]⟩
theorem coreProof340_checked : coreProof340.Check := by native_decide
def coreProof341 : CoreProof := ⟨{1,2,12,16,32,256,1536,2240,4096,8192,16384,32768},2,[.combined combinedSpec4 combinedSpec4_checked,.combined combinedSpec15 combinedSpec15_checked,.combined combinedSpec23 combinedSpec23_checked]⟩
theorem coreProof341_checked : coreProof341.Check := by native_decide
def coreProof342 : CoreProof := ⟨{1,2,12,16,192,256,512,1024,2048,4096,8192,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec6 singleSpec6_checked,.single 1 singleSpec16 singleSpec16_checked,.single 1 singleSpec90 singleSpec90_checked,.single 1 singleSpec22 singleSpec22_checked,.single 1 singleSpec44 singleSpec44_checked,.single 1 singleSpec57 singleSpec57_checked]⟩
theorem coreProof342_checked : coreProof342.Check := by native_decide
def coreProof343 : CoreProof := ⟨{1,2,12,16,192,256,512,1024,2048,4096,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec6 singleSpec6_checked,.single 1 singleSpec16 singleSpec16_checked,.single 1 singleSpec90 singleSpec90_checked,.single 1 singleSpec22 singleSpec22_checked,.single 1 singleSpec44 singleSpec44_checked,.single 1 singleSpec57 singleSpec57_checked]⟩
theorem coreProof343_checked : coreProof343.Check := by native_decide
def coreProof344 : CoreProof := ⟨{1,2,12,16,192,256,512,1024,2048,4096,16416,32768},0,[.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec14 singleSpec14_checked,.single 0 singleSpec82 singleSpec82_checked,.single 0 singleSpec55 singleSpec55_checked,.single 0 singleSpec34 singleSpec34_checked,.single 0 singleSpec42 singleSpec42_checked,.single 0 singleSpec88 singleSpec88_checked]⟩
theorem coreProof344_checked : coreProof344.Check := by native_decide
def coreProof345 : CoreProof := ⟨{1,2,12,16,192,256,512,1056,2048,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec14 singleSpec14_checked,.single 0 singleSpec38 singleSpec38_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof345_checked : coreProof345.Check := by native_decide
def coreProof346 : CoreProof := ⟨{1,2,12,16,192,256,512,1056,2048,4096,8192,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec6 singleSpec6_checked,.single 1 singleSpec16 singleSpec16_checked,.single 1 singleSpec90 singleSpec90_checked,.single 1 singleSpec22 singleSpec22_checked,.single 1 singleSpec44 singleSpec44_checked,.single 1 singleSpec57 singleSpec57_checked]⟩
theorem coreProof346_checked : coreProof346.Check := by native_decide
def coreProof347 : CoreProof := ⟨{1,2,12,16,192,256,512,1056,2048,4096,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec6 singleSpec6_checked,.single 1 singleSpec16 singleSpec16_checked,.single 1 singleSpec90 singleSpec90_checked,.single 1 singleSpec22 singleSpec22_checked,.single 1 singleSpec44 singleSpec44_checked,.single 1 singleSpec57 singleSpec57_checked]⟩
theorem coreProof347_checked : coreProof347.Check := by native_decide
def coreProof348 : CoreProof := ⟨{1,2,12,16,192,256,512,1056,2048,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec14 singleSpec14_checked,.single 0 singleSpec38 singleSpec38_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof348_checked : coreProof348.Check := by native_decide
def coreProof349 : CoreProof := ⟨{1,2,12,16,192,256,512,1056,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec14 singleSpec14_checked,.single 0 singleSpec38 singleSpec38_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof349_checked : coreProof349.Check := by native_decide
def coreProof350 : CoreProof := ⟨{1,2,12,16,192,256,512,1056,4096,8192,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec14 singleSpec14_checked,.single 0 singleSpec38 singleSpec38_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof350_checked : coreProof350.Check := by native_decide
def coreProof351 : CoreProof := ⟨{1,2,12,16,192,256,512,1056,6144,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec14 singleSpec14_checked,.single 0 singleSpec38 singleSpec38_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof351_checked : coreProof351.Check := by native_decide
end S12
