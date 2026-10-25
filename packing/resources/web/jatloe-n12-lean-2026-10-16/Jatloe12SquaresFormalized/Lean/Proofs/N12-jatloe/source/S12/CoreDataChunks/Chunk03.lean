import S12.CoreExclusion
import S12.DomainSpecDataChunks.Chunk00
import S12.DomainSpecDataChunks.Chunk01
import S12.DomainSpecDataChunks.Chunk02
import S12.DomainSpecDataChunks.Chunk03
import S12.DomainSpecDataChunks.Chunk04
import S12.DomainSpecDataChunks.Chunk05
import S12.DomainSpecDataChunks.Chunk06
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def coreProof96 : CoreProof := ⟨{1,2,4,8,48,192,256,3072,4096,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof96_checked : coreProof96.Check := by native_decide
def coreProof97 : CoreProof := ⟨{1,2,4,8,48,192,256,3072,4096,8704,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof97_checked : coreProof97.Check := by native_decide
def coreProof98 : CoreProof := ⟨{1,2,4,8,48,192,256,3584,4096,8192,16384,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof98_checked : coreProof98.Check := by native_decide
def coreProof99 : CoreProof := ⟨{1,2,4,8,48,192,768,1024,2048,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof99_checked : coreProof99.Check := by native_decide
def coreProof100 : CoreProof := ⟨{1,2,4,8,48,192,768,1024,2048,4096,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof100_checked : coreProof100.Check := by native_decide
def coreProof101 : CoreProof := ⟨{1,2,4,8,48,192,768,1024,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof101_checked : coreProof101.Check := by native_decide
def coreProof102 : CoreProof := ⟨{1,2,4,8,48,192,768,1024,4096,8192,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof102_checked : coreProof102.Check := by native_decide
def coreProof103 : CoreProof := ⟨{1,2,4,8,48,192,768,1024,6144,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof103_checked : coreProof103.Check := by native_decide
def coreProof104 : CoreProof := ⟨{1,2,4,8,48,192,768,3072,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof104_checked : coreProof104.Check := by native_decide
def coreProof105 : CoreProof := ⟨{1,2,4,8,48,192,1024,2048,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec10 singleSpec10_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof105_checked : coreProof105.Check := by native_decide
def coreProof106 : CoreProof := ⟨{1,2,4,8,48,192,1024,2048,4096,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof106_checked : coreProof106.Check := by native_decide
def coreProof107 : CoreProof := ⟨{1,2,4,8,48,192,1024,2048,4096,8448,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec72 singleSpec72_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof107_checked : coreProof107.Check := by native_decide
def coreProof108 : CoreProof := ⟨{1,2,4,8,48,192,1024,2048,4352,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof108_checked : coreProof108.Check := by native_decide
def coreProof109 : CoreProof := ⟨{1,2,4,8,48,192,1024,2304,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec10 singleSpec10_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof109_checked : coreProof109.Check := by native_decide
def coreProof110 : CoreProof := ⟨{1,2,4,8,48,192,1024,2304,4096,8192,16896,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec12 singleSpec12_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec86 singleSpec86_checked]⟩
theorem coreProof110_checked : coreProof110.Check := by native_decide
def coreProof111 : CoreProof := ⟨{1,2,4,8,48,192,1024,2816,4096,8192,16384,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec51 singleSpec51_checked,.single 0 singleSpec67 singleSpec67_checked]⟩
theorem coreProof111_checked : coreProof111.Check := by native_decide
def coreProof112 : CoreProof := ⟨{1,2,4,8,48,192,1536,2304,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec10 singleSpec10_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof112_checked : coreProof112.Check := by native_decide
def coreProof113 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2048,4096,8192,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof113_checked : coreProof113.Check := by native_decide
def coreProof114 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2048,4096,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof114_checked : coreProof114.Check := by native_decide
def coreProof115 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2048,4288,8192,16384},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof115_checked : coreProof115.Check := by native_decide
def coreProof116 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2048,4288,8192,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof116_checked : coreProof116.Check := by native_decide
def coreProof117 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2048,4288,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof117_checked : coreProof117.Check := by native_decide
def coreProof118 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2048,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof118_checked : coreProof118.Check := by native_decide
def coreProof119 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2240,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof119_checked : coreProof119.Check := by native_decide
def coreProof120 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2240,4096,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof120_checked : coreProof120.Check := by native_decide
def coreProof121 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2240,4096,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof121_checked : coreProof121.Check := by native_decide
def coreProof122 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,2240,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof122_checked : coreProof122.Check := by native_decide
def coreProof123 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof123_checked : coreProof123.Check := by native_decide
def coreProof124 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,4096,8192,16384,35008},0,[.single 0 singleSpec102 singleSpec102_checked]⟩
theorem coreProof124_checked : coreProof124.Check := by native_decide
def coreProof125 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof125_checked : coreProof125.Check := by native_decide
def coreProof126 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,4288,8192,16384,34816},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof126_checked : coreProof126.Check := by native_decide
def coreProof127 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,6144,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof127_checked : coreProof127.Check := by native_decide
end S12
