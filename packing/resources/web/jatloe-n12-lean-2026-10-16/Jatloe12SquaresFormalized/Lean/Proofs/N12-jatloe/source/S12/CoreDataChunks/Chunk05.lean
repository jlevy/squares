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
def coreProof160 : CoreProof := ⟨{1,2,4,8,48,512,1024,2304,4288,8192,16384,32768},0,[.single 0 singleSpec1 singleSpec1_checked,.single 0 singleSpec9 singleSpec9_checked,.single 0 singleSpec12 singleSpec12_checked,.single 0 singleSpec67 singleSpec67_checked,.single 0 singleSpec26 singleSpec26_checked]⟩
theorem coreProof160_checked : coreProof160.Check := by native_decide
def coreProof161 : CoreProof := ⟨{1,2,4,8,48,768,1024,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof161_checked : coreProof161.Check := by native_decide
def coreProof162 : CoreProof := ⟨{1,2,4,8,48,768,1024,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof162_checked : coreProof162.Check := by native_decide
def coreProof163 : CoreProof := ⟨{1,2,4,8,48,768,1024,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof163_checked : coreProof163.Check := by native_decide
def coreProof164 : CoreProof := ⟨{1,2,4,8,256,512,1024,2048,4096,8192,16432,32960},0,[.single 0 singleSpec84 singleSpec84_checked]⟩
theorem coreProof164_checked : coreProof164.Check := by native_decide
def coreProof165 : CoreProof := ⟨{1,2,4,8,256,512,1024,2048,4288,8192,16432,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof165_checked : coreProof165.Check := by native_decide
def coreProof166 : CoreProof := ⟨{1,2,4,8,256,512,1024,2240,4096,8192,16384,32816},0,[.single 0 singleSpec94 singleSpec94_checked]⟩
theorem coreProof166_checked : coreProof166.Check := by native_decide
def coreProof167 : CoreProof := ⟨{1,2,4,8,256,512,1024,2240,4096,8192,16432,32768},0,[.single 0 singleSpec84 singleSpec84_checked]⟩
theorem coreProof167_checked : coreProof167.Check := by native_decide
def coreProof168 : CoreProof := ⟨{1,2,4,8,256,512,1072,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof168_checked : coreProof168.Check := by native_decide
def coreProof169 : CoreProof := ⟨{1,2,4,16,32,192,256,3584,4096,8192,16384,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof169_checked : coreProof169.Check := by native_decide
def coreProof170 : CoreProof := ⟨{1,2,4,16,32,192,256,3584,4096,8192,16392,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof170_checked : coreProof170.Check := by native_decide
def coreProof171 : CoreProof := ⟨{1,2,4,16,32,192,512,3328,4096,8192,16384,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof171_checked : coreProof171.Check := by native_decide
def coreProof172 : CoreProof := ⟨{1,2,4,16,32,192,512,3328,4096,8192,16392,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof172_checked : coreProof172.Check := by native_decide
def coreProof173 : CoreProof := ⟨{1,2,4,16,32,192,520,3328,4096,8192,16384,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof173_checked : coreProof173.Check := by native_decide
def coreProof174 : CoreProof := ⟨{1,2,4,16,32,192,1024,2816,4096,8192,16384,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof174_checked : coreProof174.Check := by native_decide
def coreProof175 : CoreProof := ⟨{1,2,4,16,32,192,1024,2816,4096,8192,16392,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof175_checked : coreProof175.Check := by native_decide
def coreProof176 : CoreProof := ⟨{1,2,4,16,32,192,1792,2048,4096,8192,16384,32768},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof176_checked : coreProof176.Check := by native_decide
def coreProof177 : CoreProof := ⟨{1,2,4,16,32,192,1792,2048,4096,8192,16392,32768},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof177_checked : coreProof177.Check := by native_decide
def coreProof178 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,2048,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof178_checked : coreProof178.Check := by native_decide
def coreProof179 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,2048,4096,8192,16392},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof179_checked : coreProof179.Check := by native_decide
def coreProof180 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,2048,4096,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof180_checked : coreProof180.Check := by native_decide
def coreProof181 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,2048,4096,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof181_checked : coreProof181.Check := by native_decide
def coreProof182 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,2048,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof182_checked : coreProof182.Check := by native_decide
def coreProof183 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,2048,8192,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof183_checked : coreProof183.Check := by native_decide
def coreProof184 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof184_checked : coreProof184.Check := by native_decide
def coreProof185 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,4096,8192,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof185_checked : coreProof185.Check := by native_decide
def coreProof186 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,4096,8192,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof186_checked : coreProof186.Check := by native_decide
def coreProof187 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,4096,8192,16392,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof187_checked : coreProof187.Check := by native_decide
def coreProof188 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,6144,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof188_checked : coreProof188.Check := by native_decide
def coreProof189 : CoreProof := ⟨{1,2,4,48,192,256,512,1024,6144,8192,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof189_checked : coreProof189.Check := by native_decide
def coreProof190 : CoreProof := ⟨{1,2,4,48,192,256,512,2048,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof190_checked : coreProof190.Check := by native_decide
def coreProof191 : CoreProof := ⟨{1,2,4,48,192,256,512,2048,4096,8192,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof191_checked : coreProof191.Check := by native_decide
end S12
