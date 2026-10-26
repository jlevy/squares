import S12.CoreExclusion
import S12.DomainSpecDataChunks.Chunk02
import S12.DomainSpecDataChunks.Chunk03
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def coreProof0 : CoreProof := ⟨{1,2,4,8,16,32,192,256,3584,4096,8192,16384},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof0_checked : coreProof0.Check := by native_decide
def coreProof1 : CoreProof := ⟨{1,2,4,8,16,32,192,256,3584,4096,8192,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof1_checked : coreProof1.Check := by native_decide
def coreProof2 : CoreProof := ⟨{1,2,4,8,16,32,192,256,3584,4096,16384,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof2_checked : coreProof2.Check := by native_decide
def coreProof3 : CoreProof := ⟨{1,2,4,8,16,32,192,256,3584,8192,16384,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof3_checked : coreProof3.Check := by native_decide
def coreProof4 : CoreProof := ⟨{1,2,4,8,16,32,192,512,3328,4096,8192,16384},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof4_checked : coreProof4.Check := by native_decide
def coreProof5 : CoreProof := ⟨{1,2,4,8,16,32,192,512,3328,4096,8192,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof5_checked : coreProof5.Check := by native_decide
def coreProof6 : CoreProof := ⟨{1,2,4,8,16,32,192,1792,2048,4096,8192,16384},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof6_checked : coreProof6.Check := by native_decide
def coreProof7 : CoreProof := ⟨{1,2,4,8,16,32,192,1792,2048,4096,8192,32768},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof7_checked : coreProof7.Check := by native_decide
def coreProof8 : CoreProof := ⟨{1,2,4,8,16,32,192,1792,4096,8192,16384,32768},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof8_checked : coreProof8.Check := by native_decide
def coreProof9 : CoreProof := ⟨{1,2,4,8,16,32,192,1792,4096,8192,16384,34816},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof9_checked : coreProof9.Check := by native_decide
def coreProof10 : CoreProof := ⟨{1,2,4,8,16,32,192,2816,4096,8192,16384,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof10_checked : coreProof10.Check := by native_decide
def coreProof11 : CoreProof := ⟨{1,2,4,8,16,32,192,2816,4096,8192,16384,33792},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof11_checked : coreProof11.Check := by native_decide
def coreProof12 : CoreProof := ⟨{1,2,4,8,16,32,192,2816,4096,8192,17408,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof12_checked : coreProof12.Check := by native_decide
def coreProof13 : CoreProof := ⟨{1,2,4,8,16,32,192,3328,4096,8192,16384,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof13_checked : coreProof13.Check := by native_decide
def coreProof14 : CoreProof := ⟨{1,2,4,8,16,32,192,3328,4096,8192,16896,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof14_checked : coreProof14.Check := by native_decide
def coreProof15 : CoreProof := ⟨{1,2,4,8,16,32,192,3840,4096,8192,16384,32768},0,[.single 0 singleSpec54 singleSpec54_checked]⟩
theorem coreProof15_checked : coreProof15.Check := by native_decide
def coreProof16 : CoreProof := ⟨{1,2,4,8,16,32,256,3584,4096,8192,16384,32960},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof16_checked : coreProof16.Check := by native_decide
def coreProof17 : CoreProof := ⟨{1,2,4,8,16,32,256,3584,4288,8192,16384,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof17_checked : coreProof17.Check := by native_decide
def coreProof18 : CoreProof := ⟨{1,2,4,8,16,32,512,3328,4096,8192,16384,32960},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof18_checked : coreProof18.Check := by native_decide
def coreProof19 : CoreProof := ⟨{1,2,4,8,16,32,1792,2048,4096,8192,16384,32960},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof19_checked : coreProof19.Check := by native_decide
def coreProof20 : CoreProof := ⟨{1,2,4,8,16,32,1792,2240,4096,8192,16384,32768},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof20_checked : coreProof20.Check := by native_decide
def coreProof21 : CoreProof := ⟨{1,2,4,8,16,192,256,3584,4096,8192,16384,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof21_checked : coreProof21.Check := by native_decide
def coreProof22 : CoreProof := ⟨{1,2,4,8,16,192,256,3584,4096,8192,16416,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof22_checked : coreProof22.Check := by native_decide
def coreProof23 : CoreProof := ⟨{1,2,4,8,16,192,512,3328,4096,8192,16384,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof23_checked : coreProof23.Check := by native_decide
def coreProof24 : CoreProof := ⟨{1,2,4,8,16,192,512,3328,4096,8192,16416,32768},0,[.single 0 singleSpec52 singleSpec52_checked]⟩
theorem coreProof24_checked : coreProof24.Check := by native_decide
def coreProof25 : CoreProof := ⟨{1,2,4,8,16,192,1024,2816,4096,8192,16384,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof25_checked : coreProof25.Check := by native_decide
def coreProof26 : CoreProof := ⟨{1,2,4,8,16,192,1024,2816,4096,8192,16416,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof26_checked : coreProof26.Check := by native_decide
def coreProof27 : CoreProof := ⟨{1,2,4,8,16,192,1056,2816,4096,8192,16384,32768},0,[.single 0 singleSpec50 singleSpec50_checked]⟩
theorem coreProof27_checked : coreProof27.Check := by native_decide
def coreProof28 : CoreProof := ⟨{1,2,4,8,16,192,1792,2048,4096,8192,16384,32768},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof28_checked : coreProof28.Check := by native_decide
def coreProof29 : CoreProof := ⟨{1,2,4,8,16,192,1792,2048,4096,8192,16416,32768},0,[.single 0 singleSpec41 singleSpec41_checked]⟩
theorem coreProof29_checked : coreProof29.Check := by native_decide
def coreProof30 : CoreProof := ⟨{1,2,4,8,32,192,256,3584,4096,8192,16384,32768},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof30_checked : coreProof30.Check := by native_decide
def coreProof31 : CoreProof := ⟨{1,2,4,8,32,192,256,3584,4096,8192,16384,32784},0,[.single 0 singleSpec53 singleSpec53_checked]⟩
theorem coreProof31_checked : coreProof31.Check := by native_decide
end S12
