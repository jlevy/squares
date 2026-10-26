import S12.CoreExclusion
import S12.DomainSpecDataChunks.Chunk00
import S12.DomainSpecDataChunks.Chunk01
import S12.DomainSpecDataChunks.Chunk02
import S12.DomainSpecDataChunks.Chunk03
import S12.DomainSpecDataChunks.Chunk04
import S12.DomainSpecDataChunks.Chunk05
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def coreProof32 : CoreProof := ⟨{1,2,4,8,32,192,512,3328,4096,8192,16384,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof32_checked : coreProof32.Check := by native_decide
def coreProof33 : CoreProof := ⟨{1,2,4,8,32,192,512,3328,4096,8192,16384,32784},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof33_checked : coreProof33.Check := by native_decide
def coreProof34 : CoreProof := ⟨{1,2,4,8,32,192,1024,2816,4096,8192,16384,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof34_checked : coreProof34.Check := by native_decide
def coreProof35 : CoreProof := ⟨{1,2,4,8,32,192,1024,2816,4096,8192,16384,32784},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof35_checked : coreProof35.Check := by native_decide
def coreProof36 : CoreProof := ⟨{1,2,4,8,32,192,1040,2816,4096,8192,16384,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof36_checked : coreProof36.Check := by native_decide
def coreProof37 : CoreProof := ⟨{1,2,4,8,32,192,1792,2048,4096,8192,16384,32768},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof37_checked : coreProof37.Check := by native_decide
def coreProof38 : CoreProof := ⟨{1,2,4,8,32,192,1792,2048,4096,8192,16384,32784},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof38_checked : coreProof38.Check := by native_decide
def coreProof39 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,2048,4096,8192},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof39_checked : coreProof39.Check := by native_decide
def coreProof40 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,2048,4096,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof40_checked : coreProof40.Check := by native_decide
def coreProof41 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,2048,4096,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof41_checked : coreProof41.Check := by native_decide
def coreProof42 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,2048,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof42_checked : coreProof42.Check := by native_decide
def coreProof43 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof43_checked : coreProof43.Check := by native_decide
def coreProof44 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,4096,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof44_checked : coreProof44.Check := by native_decide
def coreProof45 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,4096,8192,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof45_checked : coreProof45.Check := by native_decide
def coreProof46 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,4096,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof46_checked : coreProof46.Check := by native_decide
def coreProof47 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,4096,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof47_checked : coreProof47.Check := by native_decide
def coreProof48 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,6144,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof48_checked : coreProof48.Check := by native_decide
def coreProof49 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,6144,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof49_checked : coreProof49.Check := by native_decide
def coreProof50 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,6144,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof50_checked : coreProof50.Check := by native_decide
def coreProof51 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof51_checked : coreProof51.Check := by native_decide
def coreProof52 : CoreProof := ⟨{1,2,4,8,48,192,256,512,1024,8192,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof52_checked : coreProof52.Check := by native_decide
def coreProof53 : CoreProof := ⟨{1,2,4,8,48,192,256,512,3072,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof53_checked : coreProof53.Check := by native_decide
def coreProof54 : CoreProof := ⟨{1,2,4,8,48,192,256,512,3072,4096,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof54_checked : coreProof54.Check := by native_decide
def coreProof55 : CoreProof := ⟨{1,2,4,8,48,192,256,512,3072,4096,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof55_checked : coreProof55.Check := by native_decide
def coreProof56 : CoreProof := ⟨{1,2,4,8,48,192,256,512,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof56_checked : coreProof56.Check := by native_decide
def coreProof57 : CoreProof := ⟨{1,2,4,8,48,192,256,512,4096,8192,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof57_checked : coreProof57.Check := by native_decide
def coreProof58 : CoreProof := ⟨{1,2,4,8,48,192,256,512,4096,8192,16384,35840},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof58_checked : coreProof58.Check := by native_decide
def coreProof59 : CoreProof := ⟨{1,2,4,8,48,192,256,512,4096,8192,17408,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof59_checked : coreProof59.Check := by native_decide
def coreProof60 : CoreProof := ⟨{1,2,4,8,48,192,256,512,4096,8192,17408,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof60_checked : coreProof60.Check := by native_decide
def coreProof61 : CoreProof := ⟨{1,2,4,8,48,192,256,512,6144,8192,17408,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof61_checked : coreProof61.Check := by native_decide
def coreProof62 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof62_checked : coreProof62.Check := by native_decide
def coreProof63 : CoreProof := ⟨{1,2,4,8,48,192,256,1024,2048,4096,8192,16896},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof63_checked : coreProof63.Check := by native_decide
end S12
