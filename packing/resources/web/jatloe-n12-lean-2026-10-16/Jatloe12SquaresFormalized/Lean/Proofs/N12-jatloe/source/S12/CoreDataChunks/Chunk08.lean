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
def coreProof256 : CoreProof := ⟨{1,2,8,48,192,256,512,2048,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof256_checked : coreProof256.Check := by native_decide
def coreProof257 : CoreProof := ⟨{1,2,8,48,192,256,512,2048,4096,8192,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof257_checked : coreProof257.Check := by native_decide
def coreProof258 : CoreProof := ⟨{1,2,8,48,192,256,512,2048,4096,8192,17408,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof258_checked : coreProof258.Check := by native_decide
def coreProof259 : CoreProof := ⟨{1,2,8,48,192,256,512,2048,4096,8196,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof259_checked : coreProof259.Check := by native_decide
def coreProof260 : CoreProof := ⟨{1,2,8,48,192,256,512,2048,4096,8196,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof260_checked : coreProof260.Check := by native_decide
def coreProof261 : CoreProof := ⟨{1,2,8,48,192,256,512,2048,4096,8196,17408,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof261_checked : coreProof261.Check := by native_decide
def coreProof262 : CoreProof := ⟨{1,2,8,48,192,256,512,3072,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof262_checked : coreProof262.Check := by native_decide
def coreProof263 : CoreProof := ⟨{1,2,8,48,192,256,512,3072,4096,8196,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof263_checked : coreProof263.Check := by native_decide
def coreProof264 : CoreProof := ⟨{1,2,8,48,192,256,516,1024,2048,4096,8192,16384},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof264_checked : coreProof264.Check := by native_decide
def coreProof265 : CoreProof := ⟨{1,2,8,48,192,256,516,1024,2048,4096,8192,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof265_checked : coreProof265.Check := by native_decide
def coreProof266 : CoreProof := ⟨{1,2,8,48,192,256,516,1024,2048,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof266_checked : coreProof266.Check := by native_decide
def coreProof267 : CoreProof := ⟨{1,2,8,48,192,256,516,1024,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof267_checked : coreProof267.Check := by native_decide
def coreProof268 : CoreProof := ⟨{1,2,8,48,192,256,516,1024,4096,8192,16384,34816},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof268_checked : coreProof268.Check := by native_decide
def coreProof269 : CoreProof := ⟨{1,2,8,48,192,256,516,1024,6144,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof269_checked : coreProof269.Check := by native_decide
def coreProof270 : CoreProof := ⟨{1,2,8,48,192,256,516,2048,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof270_checked : coreProof270.Check := by native_decide
def coreProof271 : CoreProof := ⟨{1,2,8,48,192,256,516,2048,4096,8192,16384,33792},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof271_checked : coreProof271.Check := by native_decide
def coreProof272 : CoreProof := ⟨{1,2,8,48,192,256,516,2048,4096,8192,17408,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof272_checked : coreProof272.Check := by native_decide
def coreProof273 : CoreProof := ⟨{1,2,8,48,192,256,516,3072,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof273_checked : coreProof273.Check := by native_decide
def coreProof274 : CoreProof := ⟨{1,2,8,48,192,256,1024,2048,4096,8192,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec66 singleSpec66_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof274_checked : coreProof274.Check := by native_decide
def coreProof275 : CoreProof := ⟨{1,2,8,48,192,256,1024,2048,4096,8196,16896,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec85 singleSpec85_checked]⟩
theorem coreProof275_checked : coreProof275.Check := by native_decide
def coreProof276 : CoreProof := ⟨{1,2,8,48,192,512,1024,2048,4352,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec64 singleSpec64_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof276_checked : coreProof276.Check := by native_decide
def coreProof277 : CoreProof := ⟨{1,2,8,48,192,512,1024,2048,4352,8196,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec64 singleSpec64_checked]⟩
theorem coreProof277_checked : coreProof277.Check := by native_decide
def coreProof278 : CoreProof := ⟨{1,2,8,48,192,516,1024,2048,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec13 singleSpec13_checked,.single 1 singleSpec30 singleSpec30_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof278_checked : coreProof278.Check := by native_decide
def coreProof279 : CoreProof := ⟨{1,2,8,48,192,516,1024,2048,4352,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec29 singleSpec29_checked,.single 0 singleSpec64 singleSpec64_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof279_checked : coreProof279.Check := by native_decide
def coreProof280 : CoreProof := ⟨{1,2,8,48,192,516,1024,2304,4096,8192,16384,32768},1,[.single 1 singleSpec2 singleSpec2_checked,.single 1 singleSpec13 singleSpec13_checked,.single 1 singleSpec30 singleSpec30_checked,.single 1 singleSpec68 singleSpec68_checked]⟩
theorem coreProof280_checked : coreProof280.Check := by native_decide
def coreProof281 : CoreProof := ⟨{1,2,8,48,256,512,1024,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof281_checked : coreProof281.Check := by native_decide
def coreProof282 : CoreProof := ⟨{1,2,8,48,256,512,1024,2048,4096,8196,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof282_checked : coreProof282.Check := by native_decide
def coreProof283 : CoreProof := ⟨{1,2,8,48,256,512,1024,2048,4288,8192,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof283_checked : coreProof283.Check := by native_decide
def coreProof284 : CoreProof := ⟨{1,2,8,48,256,512,1024,2048,4288,8196,16384,32768},0,[.single 0 singleSpec62 singleSpec62_checked]⟩
theorem coreProof284_checked : coreProof284.Check := by native_decide
def coreProof285 : CoreProof := ⟨{1,2,8,48,256,512,1024,2240,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof285_checked : coreProof285.Check := by native_decide
def coreProof286 : CoreProof := ⟨{1,2,8,48,256,512,1024,2240,4096,8196,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec4 singleSpec4_checked,.single 0 singleSpec11 singleSpec11_checked,.single 0 singleSpec70 singleSpec70_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked]⟩
theorem coreProof286_checked : coreProof286.Check := by native_decide
def coreProof287 : CoreProof := ⟨{1,2,8,48,256,516,1024,2048,4096,8192,16384,32960},0,[.single 0 singleSpec98 singleSpec98_checked]⟩
theorem coreProof287_checked : coreProof287.Check := by native_decide
end S12
