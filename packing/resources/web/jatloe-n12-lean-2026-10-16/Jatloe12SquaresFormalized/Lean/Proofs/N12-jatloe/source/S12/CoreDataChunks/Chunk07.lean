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
def coreProof224 : CoreProof := ⟨{1,2,4,48,192,520,1024,2304,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec10 singleSpec10_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof224_checked : coreProof224.Check := by native_decide
def coreProof225 : CoreProof := ⟨{1,2,4,48,192,768,1024,2048,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof225_checked : coreProof225.Check := by native_decide
def coreProof226 : CoreProof := ⟨{1,2,4,48,192,768,1024,2048,4096,8192,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec33 singleSpec33_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof226_checked : coreProof226.Check := by native_decide
def coreProof227 : CoreProof := ⟨{1,2,4,48,256,512,1024,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof227_checked : coreProof227.Check := by native_decide
def coreProof228 : CoreProof := ⟨{1,2,4,48,256,512,1024,2048,4096,8192,16392,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof228_checked : coreProof228.Check := by native_decide
def coreProof229 : CoreProof := ⟨{1,2,4,48,256,512,1024,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof229_checked : coreProof229.Check := by native_decide
def coreProof230 : CoreProof := ⟨{1,2,4,48,256,512,1024,2048,4288,8192,16392,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof230_checked : coreProof230.Check := by native_decide
def coreProof231 : CoreProof := ⟨{1,2,4,48,256,512,1024,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof231_checked : coreProof231.Check := by native_decide
def coreProof232 : CoreProof := ⟨{1,2,4,48,256,512,1024,2240,4096,8192,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof232_checked : coreProof232.Check := by native_decide
def coreProof233 : CoreProof := ⟨{1,2,4,48,256,520,1024,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof233_checked : coreProof233.Check := by native_decide
def coreProof234 : CoreProof := ⟨{1,2,4,48,256,520,1024,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof234_checked : coreProof234.Check := by native_decide
def coreProof235 : CoreProof := ⟨{1,2,4,48,256,520,1024,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof235_checked : coreProof235.Check := by native_decide
def coreProof236 : CoreProof := ⟨{1,2,4,192,256,512,1024,2048,4096,8192,16384,32816},0,[.single 0 singleSpec94 singleSpec94_checked]⟩
theorem coreProof236_checked : coreProof236.Check := by native_decide
def coreProof237 : CoreProof := ⟨{1,2,4,192,256,512,1024,2048,4096,8192,16392,32816},0,[.single 0 singleSpec94 singleSpec94_checked]⟩
theorem coreProof237_checked : coreProof237.Check := by native_decide
def coreProof238 : CoreProof := ⟨{1,2,4,192,256,512,1024,2048,4096,8192,16432,32768},0,[.single 0 singleSpec84 singleSpec84_checked]⟩
theorem coreProof238_checked : coreProof238.Check := by native_decide
def coreProof239 : CoreProof := ⟨{1,2,4,192,256,512,1072,2048,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof239_checked : coreProof239.Check := by native_decide
def coreProof240 : CoreProof := ⟨{1,2,4,192,256,512,1072,2048,4096,8192,16392,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec79 singleSpec79_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof240_checked : coreProof240.Check := by native_decide
def coreProof241 : CoreProof := ⟨{1,2,4,192,256,520,1024,2048,4096,8192,16384,32816},0,[.single 0 singleSpec94 singleSpec94_checked]⟩
theorem coreProof241_checked : coreProof241.Check := by native_decide
def coreProof242 : CoreProof := ⟨{1,2,4,192,256,520,1024,2048,4096,8192,16432,32768},0,[.single 0 singleSpec84 singleSpec84_checked]⟩
theorem coreProof242_checked : coreProof242.Check := by native_decide
def coreProof243 : CoreProof := ⟨{1,2,4,192,256,520,1072,2048,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec8 singleSpec8_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof243_checked : coreProof243.Check := by native_decide
def coreProof244 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,2048,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof244_checked : coreProof244.Check := by native_decide
def coreProof245 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,2048,4096,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof245_checked : coreProof245.Check := by native_decide
def coreProof246 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,2048,4096,8196,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof246_checked : coreProof246.Check := by native_decide
def coreProof247 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,2048,4096,8196,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof247_checked : coreProof247.Check := by native_decide
def coreProof248 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,2048,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof248_checked : coreProof248.Check := by native_decide
def coreProof249 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,2048,8196,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof249_checked : coreProof249.Check := by native_decide
def coreProof250 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof250_checked : coreProof250.Check := by native_decide
def coreProof251 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,4096,8192,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof251_checked : coreProof251.Check := by native_decide
def coreProof252 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,4096,8196,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof252_checked : coreProof252.Check := by native_decide
def coreProof253 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,4096,8196,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof253_checked : coreProof253.Check := by native_decide
def coreProof254 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,6144,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof254_checked : coreProof254.Check := by native_decide
def coreProof255 : CoreProof := ⟨{1,2,8,48,192,256,512,1024,6144,8196,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof255_checked : coreProof255.Check := by native_decide
end S12
