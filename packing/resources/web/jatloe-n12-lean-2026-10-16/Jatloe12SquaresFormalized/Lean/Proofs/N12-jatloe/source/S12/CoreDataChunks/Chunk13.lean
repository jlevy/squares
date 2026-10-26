import S12.CoreExclusion
import S12.DomainSpecDataChunks.Chunk00
import S12.DomainSpecDataChunks.Chunk01
import S12.DomainSpecDataChunks.Chunk02
import S12.DomainSpecDataChunks.Chunk03
import S12.DomainSpecDataChunks.Chunk04
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def coreProof416 : CoreProof := ⟨{1,12,32,192,256,512,1024,2048,4098,8192,16384,32784},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec17 singleSpec17_checked,.single 0 singleSpec59 singleSpec59_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof416_checked : coreProof416.Check := by native_decide
def coreProof417 : CoreProof := ⟨{1,12,32,192,256,512,1040,2048,4098,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec17 singleSpec17_checked,.single 0 singleSpec59 singleSpec59_checked,.single 0 singleSpec75 singleSpec75_checked,.single 0 singleSpec20 singleSpec20_checked,.single 0 singleSpec25 singleSpec25_checked,.single 0 singleSpec66 singleSpec66_checked]⟩
theorem coreProof417_checked : coreProof417.Check := by native_decide
def coreProof418 : CoreProof := ⟨{1,12,48,64,258,512,1024,2176,4096,8192,16384,32768},0,[.single 0 singleSpec0 singleSpec0_checked,.single 0 singleSpec19 singleSpec19_checked,.single 0 singleSpec24 singleSpec24_checked,.single 0 singleSpec46 singleSpec46_checked,.single 0 singleSpec55 singleSpec55_checked]⟩
theorem coreProof418_checked : coreProof418.Check := by native_decide
end S12
