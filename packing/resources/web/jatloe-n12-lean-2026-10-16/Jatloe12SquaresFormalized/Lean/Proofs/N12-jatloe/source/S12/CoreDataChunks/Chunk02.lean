import S12.CoreExclusion
import S12.DomainSpecDataChunks.Chunk00
import S12.DomainSpecDataChunks.Chunk01
import S12.DomainSpecDataChunks.Chunk04
import S12.DomainSpecDataChunks.Chunk05
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def coreProof64 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,4096,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof64_checked : coreProof64.Check := by native_decide
def coreProof65 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,4096,8704,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof65_checked : coreProof65.Check := by native_decide
def coreProof66 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,4096,8704,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof66_checked : coreProof66.Check := by native_decide
def coreProof67 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,4096,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof67_checked : coreProof67.Check := by native_decide
def coreProof68 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof68_checked : coreProof68.Check := by native_decide
def coreProof69 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof69_checked : coreProof69.Check := by native_decide
def coreProof70 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,8704,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof70_checked : coreProof70.Check := by native_decide
def coreProof71 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof71_checked : coreProof71.Check := by native_decide
def coreProof72 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,4096,8192,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof72_checked : coreProof72.Check := by native_decide
def coreProof73 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,4096,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof73_checked : coreProof73.Check := by native_decide
def coreProof74 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,4096,8192,16896,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof74_checked : coreProof74.Check := by native_decide
def coreProof75 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,4096,8704,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof75_checked : coreProof75.Check := by native_decide
def coreProof76 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,4096,8704,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof76_checked : coreProof76.Check := by native_decide
def coreProof77 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,6144,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof77_checked : coreProof77.Check := by native_decide
def coreProof78 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,6144,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof78_checked : coreProof78.Check := by native_decide
def coreProof79 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,6144,8704,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof79_checked : coreProof79.Check := by native_decide
def coreProof80 : CoreProof := ⟨{1,2,4,8,48,192,256,1536,2048,4096,8192,16384},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof80_checked : coreProof80.Check := by native_decide
def coreProof81 : CoreProof := ⟨{1,2,4,8,48,192,256,1536,2048,4096,8192,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof81_checked : coreProof81.Check := by native_decide
def coreProof82 : CoreProof := ⟨{1,2,4,8,48,192,256,1536,2048,8192,16384,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof82_checked : coreProof82.Check := by native_decide
def coreProof83 : CoreProof := ⟨{1,2,4,8,48,192,256,1536,4096,8192,16384,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof83_checked : coreProof83.Check := by native_decide
def coreProof84 : CoreProof := ⟨{1,2,4,8,48,192,256,1536,4096,8192,16384,34816},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof84_checked : coreProof84.Check := by native_decide
def coreProof85 : CoreProof := ⟨{1,2,4,8,48,192,256,1536,6144,8192,16384,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof85_checked : coreProof85.Check := by native_decide
def coreProof86 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof86_checked : coreProof86.Check := by native_decide
def coreProof87 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8192,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof87_checked : coreProof87.Check := by native_decide
def coreProof88 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof88_checked : coreProof88.Check := by native_decide
def coreProof89 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8192,16896,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof89_checked : coreProof89.Check := by native_decide
def coreProof90 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8192,17408,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof90_checked : coreProof90.Check := by native_decide
def coreProof91 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8192,17920,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec5 singleSpec5_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec21 singleSpec21_checked]⟩
theorem coreProof91_checked : coreProof91.Check := by native_decide
def coreProof92 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8704,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof92_checked : coreProof92.Check := by native_decide
def coreProof93 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8704,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof93_checked : coreProof93.Check := by native_decide
def coreProof94 : CoreProof := ⟨{1,2,4,8,48,192,256,2048,4096,8704,17408,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec74 singleSpec74_checked]⟩
theorem coreProof94_checked : coreProof94.Check := by native_decide
def coreProof95 : CoreProof := ⟨{1,2,4,8,48,192,256,3072,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof95_checked : coreProof95.Check := by native_decide
end S12
