import S12.CoreExclusion
import S12.DomainSpecDataChunks.Chunk00
import S12.DomainSpecDataChunks.Chunk01
import S12.DomainSpecDataChunks.Chunk03
import S12.DomainSpecDataChunks.Chunk04
import S12.DomainSpecDataChunks.Chunk05
import S12.DomainSpecDataChunks.Chunk06
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def coreProof128 : CoreProof := ⟨{1,2,4,8,48,256,512,1024,6336,8192,16384,32768},0,[.single 0 singleSpec65 singleSpec65_checked]⟩
theorem coreProof128_checked : coreProof128.Check := by native_decide
def coreProof129 : CoreProof := ⟨{1,2,4,8,48,256,512,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof129_checked : coreProof129.Check := by native_decide
def coreProof130 : CoreProof := ⟨{1,2,4,8,48,256,512,2048,4096,8192,17408,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof130_checked : coreProof130.Check := by native_decide
def coreProof131 : CoreProof := ⟨{1,2,4,8,48,256,512,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof131_checked : coreProof131.Check := by native_decide
def coreProof132 : CoreProof := ⟨{1,2,4,8,48,256,512,2048,4288,8192,16384,33792},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof132_checked : coreProof132.Check := by native_decide
def coreProof133 : CoreProof := ⟨{1,2,4,8,48,256,512,2048,4288,8192,17408,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof133_checked : coreProof133.Check := by native_decide
def coreProof134 : CoreProof := ⟨{1,2,4,8,48,256,512,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof134_checked : coreProof134.Check := by native_decide
def coreProof135 : CoreProof := ⟨{1,2,4,8,48,256,512,2240,4096,8192,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof135_checked : coreProof135.Check := by native_decide
def coreProof136 : CoreProof := ⟨{1,2,4,8,48,256,512,2240,4096,8192,17408,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof136_checked : coreProof136.Check := by native_decide
def coreProof137 : CoreProof := ⟨{1,2,4,8,48,256,512,3072,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof137_checked : coreProof137.Check := by native_decide
def coreProof138 : CoreProof := ⟨{1,2,4,8,48,256,512,3072,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof138_checked : coreProof138.Check := by native_decide
def coreProof139 : CoreProof := ⟨{1,2,4,8,48,256,1024,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof139_checked : coreProof139.Check := by native_decide
def coreProof140 : CoreProof := ⟨{1,2,4,8,48,256,1024,2048,4096,8192,16896,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof140_checked : coreProof140.Check := by native_decide
def coreProof141 : CoreProof := ⟨{1,2,4,8,48,256,1024,2048,4096,8704,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof141_checked : coreProof141.Check := by native_decide
def coreProof142 : CoreProof := ⟨{1,2,4,8,48,256,1024,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof142_checked : coreProof142.Check := by native_decide
def coreProof143 : CoreProof := ⟨{1,2,4,8,48,256,1024,2048,4288,8192,16896,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof143_checked : coreProof143.Check := by native_decide
def coreProof144 : CoreProof := ⟨{1,2,4,8,48,256,1024,2048,4288,8704,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof144_checked : coreProof144.Check := by native_decide
def coreProof145 : CoreProof := ⟨{1,2,4,8,48,256,1024,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof145_checked : coreProof145.Check := by native_decide
def coreProof146 : CoreProof := ⟨{1,2,4,8,48,256,1024,2240,4096,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof146_checked : coreProof146.Check := by native_decide
def coreProof147 : CoreProof := ⟨{1,2,4,8,48,256,1024,2240,4096,8704,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof147_checked : coreProof147.Check := by native_decide
def coreProof148 : CoreProof := ⟨{1,2,4,8,48,256,1536,2048,4096,8192,16384,32960},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof148_checked : coreProof148.Check := by native_decide
def coreProof149 : CoreProof := ⟨{1,2,4,8,48,256,1536,2048,4288,8192,16384,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof149_checked : coreProof149.Check := by native_decide
def coreProof150 : CoreProof := ⟨{1,2,4,8,48,256,1536,2240,4096,8192,16384,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof150_checked : coreProof150.Check := by native_decide
def coreProof151 : CoreProof := ⟨{1,2,4,8,48,512,1024,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof151_checked : coreProof151.Check := by native_decide
def coreProof152 : CoreProof := ⟨{1,2,4,8,48,512,1024,2048,4096,8448,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof152_checked : coreProof152.Check := by native_decide
def coreProof153 : CoreProof := ⟨{1,2,4,8,48,512,1024,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof153_checked : coreProof153.Check := by native_decide
def coreProof154 : CoreProof := ⟨{1,2,4,8,48,512,1024,2048,4288,8448,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof154_checked : coreProof154.Check := by native_decide
def coreProof155 : CoreProof := ⟨{1,2,4,8,48,512,1024,2048,4352,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof155_checked : coreProof155.Check := by native_decide
def coreProof156 : CoreProof := ⟨{1,2,4,8,48,512,1024,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof156_checked : coreProof156.Check := by native_decide
def coreProof157 : CoreProof := ⟨{1,2,4,8,48,512,1024,2240,4096,8448,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec72 singleSpec72_checked]⟩
theorem coreProof157_checked : coreProof157.Check := by native_decide
def coreProof158 : CoreProof := ⟨{1,2,4,8,48,512,1024,2240,4352,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec64 singleSpec64_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof158_checked : coreProof158.Check := by native_decide
def coreProof159 : CoreProof := ⟨{1,2,4,8,48,512,1024,2304,4096,8192,16384,32960},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec12 singleSpec12_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec26 singleSpec26_checked]⟩
theorem coreProof159_checked : coreProof159.Check := by native_decide
end S12
