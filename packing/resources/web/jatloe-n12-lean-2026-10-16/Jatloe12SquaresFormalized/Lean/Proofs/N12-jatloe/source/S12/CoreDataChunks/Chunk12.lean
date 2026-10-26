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
def coreProof384 : CoreProof := ⟨{1,2,12,32,256,512,1024,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec17 singleSpec17_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof384_checked : coreProof384.Check := by native_decide
def coreProof385 : CoreProof := ⟨{1,2,12,32,256,512,1024,2240,4096,8192,16384,32784},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec17 singleSpec17_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof385_checked : coreProof385.Check := by native_decide
def coreProof386 : CoreProof := ⟨{1,2,12,32,256,512,1040,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof386_checked : coreProof386.Check := by native_decide
def coreProof387 : CoreProof := ⟨{1,2,12,32,256,512,1040,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof387_checked : coreProof387.Check := by native_decide
def coreProof388 : CoreProof := ⟨{1,2,12,32,256,512,1040,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec17 singleSpec17_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof388_checked : coreProof388.Check := by native_decide
def coreProof389 : CoreProof := ⟨{1,2,12,48,256,512,1024,2048,4096,8192,16384,32832},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec6 singleSpec6_checked,.single 1 singleSpec96 singleSpec96_checked,.single 1 singleSpec22 singleSpec22_checked,.single 1 singleSpec44 singleSpec44_checked,.single 1 singleSpec57 singleSpec57_checked]⟩
theorem coreProof389_checked : coreProof389.Check := by native_decide
def coreProof390 : CoreProof := ⟨{1,2,12,48,256,512,1024,2048,4096,8192,16384,32896},0,[.single 0 singleSpec97 singleSpec97_checked]⟩
theorem coreProof390_checked : coreProof390.Check := by native_decide
def coreProof391 : CoreProof := ⟨{1,2,12,48,256,512,1024,2048,4096,8192,16384,32960},1,[.single 1 singleSpec7 singleSpec7_checked,.single 1 singleSpec100 singleSpec100_checked,.single 1 singleSpec3 singleSpec3_checked,.single 1 singleSpec58 singleSpec58_checked,.single 1 singleSpec23 singleSpec23_checked,.single 1 singleSpec45 singleSpec45_checked]⟩
theorem coreProof391_checked : coreProof391.Check := by native_decide
def coreProof392 : CoreProof := ⟨{1,2,12,48,256,512,1024,2048,4160,8192,16384,32768},0,[.single 0 singleSpec60 singleSpec60_checked]⟩
theorem coreProof392_checked : coreProof392.Check := by native_decide
def coreProof393 : CoreProof := ⟨{1,2,12,48,256,512,1024,2048,4224,8192,16384,32832},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec6 singleSpec6_checked,.single 1 singleSpec61 singleSpec61_checked,.single 1 singleSpec96 singleSpec96_checked,.single 1 singleSpec22 singleSpec22_checked,.single 1 singleSpec44 singleSpec44_checked]⟩
theorem coreProof393_checked : coreProof393.Check := by native_decide
def coreProof394 : CoreProof := ⟨{1,2,12,48,256,512,1024,2176,4096,8192,16384,32832},0,[.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec95 singleSpec95_checked,.single 0 singleSpec46 singleSpec46_checked,.single 0 singleSpec55 singleSpec55_checked]⟩
theorem coreProof394_checked : coreProof394.Check := by native_decide
def coreProof395 : CoreProof := ⟨{1,2,12,192,256,512,1024,2048,4096,8192,16384,32800},0,[.single 0 singleSpec93 singleSpec93_checked]⟩
theorem coreProof395_checked : coreProof395.Check := by native_decide
def coreProof396 : CoreProof := ⟨{1,2,12,192,256,512,1040,2048,4096,8192,16384,32768},2,[.combined combinedSpec0 combinedSpec0_checked,.combined combinedSpec2 combinedSpec2_checked,.combined combinedSpec16 combinedSpec16_checked,.combined combinedSpec18 combinedSpec18_checked,.combined combinedSpec20 combinedSpec20_checked,.combined combinedSpec22 combinedSpec22_checked,.combined combinedSpec10 combinedSpec10_checked,.combined combinedSpec5 combinedSpec5_checked,.combined combinedSpec7 combinedSpec7_checked,.combined combinedSpec12 combinedSpec12_checked]⟩
theorem coreProof396_checked : coreProof396.Check := by native_decide
def coreProof397 : CoreProof := ⟨{1,2,12,192,256,512,1040,2048,4096,8192,16416,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec6 singleSpec6_checked,.single 1 singleSpec83 singleSpec83_checked,.single 1 singleSpec37 singleSpec37_checked,.single 1 singleSpec90 singleSpec90_checked,.single 1 singleSpec22 singleSpec22_checked,.single 1 singleSpec44 singleSpec44_checked,.single 1 singleSpec57 singleSpec57_checked]⟩
theorem coreProof397_checked : coreProof397.Check := by native_decide
def coreProof398 : CoreProof := ⟨{1,2,12,192,256,512,1072,2048,4096,8192,16384,32768},2,[.combined combinedSpec1 combinedSpec1_checked,.combined combinedSpec3 combinedSpec3_checked,.combined combinedSpec11 combinedSpec11_checked,.combined combinedSpec17 combinedSpec17_checked,.combined combinedSpec19 combinedSpec19_checked,.combined combinedSpec21 combinedSpec21_checked,.combined combinedSpec24 combinedSpec24_checked,.combined combinedSpec6 combinedSpec6_checked,.combined combinedSpec8 combinedSpec8_checked,.combined combinedSpec13 combinedSpec13_checked]⟩
theorem coreProof398_checked : coreProof398.Check := by native_decide
def coreProof399 : CoreProof := ⟨{1,2,16,32,256,512,1024,2048,4096,8192,16396,32960},0,[.single 0 singleSpec81 singleSpec81_checked]⟩
theorem coreProof399_checked : coreProof399.Check := by native_decide
def coreProof400 : CoreProof := ⟨{1,2,16,32,256,512,1024,2048,4096,8204,16384,32960},0,[.single 0 singleSpec71 singleSpec71_checked]⟩
theorem coreProof400_checked : coreProof400.Check := by native_decide
def coreProof401 : CoreProof := ⟨{1,2,16,32,256,512,1024,2240,4096,8192,16396,32768},0,[.single 0 singleSpec81 singleSpec81_checked]⟩
theorem coreProof401_checked : coreProof401.Check := by native_decide
def coreProof402 : CoreProof := ⟨{1,2,16,32,256,524,1024,2240,4096,8192,16384,32768},2,[.combined combinedSpec9 combinedSpec9_checked]⟩
theorem coreProof402_checked : coreProof402.Check := by native_decide
def coreProof403 : CoreProof := ⟨{1,4,48,192,256,512,1024,2048,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec10 singleSpec10_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof403_checked : coreProof403.Check := by native_decide
def coreProof404 : CoreProof := ⟨{1,4,48,192,256,512,1024,2048,4096,8192,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof404_checked : coreProof404.Check := by native_decide
def coreProof405 : CoreProof := ⟨{1,4,48,192,256,512,1024,2048,4098,8192,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof405_checked : coreProof405.Check := by native_decide
def coreProof406 : CoreProof := ⟨{1,4,48,192,256,520,1024,2048,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec10 singleSpec10_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof406_checked : coreProof406.Check := by native_decide
def coreProof407 : CoreProof := ⟨{1,4,48,192,256,520,1024,2048,4098,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec59 singleSpec59_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof407_checked : coreProof407.Check := by native_decide
def coreProof408 : CoreProof := ⟨{1,4,48,192,258,520,1024,2048,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec10 singleSpec10_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof408_checked : coreProof408.Check := by native_decide
def coreProof409 : CoreProof := ⟨{1,8,48,192,256,512,1024,2048,4098,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec59 singleSpec59_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof409_checked : coreProof409.Check := by native_decide
def coreProof410 : CoreProof := ⟨{1,8,48,192,256,512,1024,2048,4098,8196,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec59 singleSpec59_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof410_checked : coreProof410.Check := by native_decide
def coreProof411 : CoreProof := ⟨{1,8,48,192,256,516,1024,2048,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec13 singleSpec13_checked,.single 1 singleSpec30 singleSpec30_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof411_checked : coreProof411.Check := by native_decide
def coreProof412 : CoreProof := ⟨{1,8,48,192,256,516,1024,2048,4098,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec59 singleSpec59_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof412_checked : coreProof412.Check := by native_decide
def coreProof413 : CoreProof := ⟨{1,8,48,192,258,516,1024,2048,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec13 singleSpec13_checked,.single 1 singleSpec30 singleSpec30_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof413_checked : coreProof413.Check := by native_decide
def coreProof414 : CoreProof := ⟨{1,12,16,192,256,512,1056,2048,4098,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec14 singleSpec14_checked,.single 0 singleSpec59 singleSpec59_checked,.single 0 singleSpec38 singleSpec38_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof414_checked : coreProof414.Check := by native_decide
def coreProof415 : CoreProof := ⟨{1,12,32,192,256,512,1024,2048,4096,8192,16384,32784},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec18 singleSpec18_checked,.single 1 singleSpec92 singleSpec92_checked,.single 1 singleSpec68 singleSpec68_checked,.single 1 singleSpec27 singleSpec27_checked,.single 1 singleSpec35 singleSpec35_checked,.single 1 singleSpec77 singleSpec77_checked]⟩
theorem coreProof415_checked : coreProof415.Check := by native_decide
end S12
