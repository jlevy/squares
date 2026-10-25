import S12.FourPointData.Chunk00
import S12.FourPointData.Chunk01
import S12.FourPointData.Chunk02
import S12.FourPointData.Chunk03
import S12.FourPointData.Chunk04
import S12.FourPointData.Chunk05
import S12.FourPointData.Chunk06
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def fourPointData : List FourPointDatum := [fourDatum0,fourDatum1,fourDatum2,fourDatum3,fourDatum4,fourDatum5,fourDatum6,fourDatum7,fourDatum8,fourDatum9,fourDatum10,fourDatum11,fourDatum12,fourDatum13,fourDatum14,fourDatum15,fourDatum16,fourDatum17,fourDatum18,fourDatum19,fourDatum20,fourDatum21,fourDatum22,fourDatum23,fourDatum24,fourDatum25,fourDatum26,fourDatum27,fourDatum28,fourDatum29,fourDatum30,fourDatum31,fourDatum32,fourDatum33,fourDatum34,fourDatum35,fourDatum36,fourDatum37,fourDatum38,fourDatum39,fourDatum40,fourDatum41,fourDatum42,fourDatum43,fourDatum44,fourDatum45,fourDatum46,fourDatum47,fourDatum48,fourDatum49,fourDatum50,fourDatum51,fourDatum52,fourDatum53,fourDatum54,fourDatum55,fourDatum56,fourDatum57,fourDatum58,fourDatum59,fourDatum60,fourDatum61,fourDatum62,fourDatum63,fourDatum64,fourDatum65,fourDatum66,fourDatum67,fourDatum68,fourDatum69,fourDatum70,fourDatum71,fourDatum72,fourDatum73,fourDatum74,fourDatum75,fourDatum76,fourDatum77,fourDatum78,fourDatum79,fourDatum80,fourDatum81,fourDatum82,fourDatum83,fourDatum84,fourDatum85,fourDatum86,fourDatum87,fourDatum88,fourDatum89,fourDatum90,fourDatum91,fourDatum92,fourDatum93,fourDatum94,fourDatum95,fourDatum96,fourDatum97,fourDatum98,fourDatum99,fourDatum100,fourDatum101,fourDatum102,fourDatum103,fourDatum104,fourDatum105,fourDatum106,fourDatum107,fourDatum108,fourDatum109,fourDatum110]
theorem fourPointData_count : fourPointData.length = 111 := by decide
/-- Assemble the previously checked certificates directly, without searching
all certificate proofs once for every possible member. -/
private theorem fourPointChecks_cons {w : FourPointDatum} {ws : List FourPointDatum}
    (hw : w.Check) (hws : ∀ x ∈ ws, x.Check) : ∀ x ∈ w :: ws, x.Check := by
  intro x hx
  rcases List.mem_cons.mp hx with rfl | hx
  · exact hw
  · exact hws x hx

theorem fourPointData_checked : ∀ w ∈ fourPointData, w.Check := by
  exact fourPointChecks_cons fourDatum0_checked <|
    fourPointChecks_cons fourDatum1_checked <|
    fourPointChecks_cons fourDatum2_checked <|
    fourPointChecks_cons fourDatum3_checked <|
    fourPointChecks_cons fourDatum4_checked <|
    fourPointChecks_cons fourDatum5_checked <|
    fourPointChecks_cons fourDatum6_checked <|
    fourPointChecks_cons fourDatum7_checked <|
    fourPointChecks_cons fourDatum8_checked <|
    fourPointChecks_cons fourDatum9_checked <|
    fourPointChecks_cons fourDatum10_checked <|
    fourPointChecks_cons fourDatum11_checked <|
    fourPointChecks_cons fourDatum12_checked <|
    fourPointChecks_cons fourDatum13_checked <|
    fourPointChecks_cons fourDatum14_checked <|
    fourPointChecks_cons fourDatum15_checked <|
    fourPointChecks_cons fourDatum16_checked <|
    fourPointChecks_cons fourDatum17_checked <|
    fourPointChecks_cons fourDatum18_checked <|
    fourPointChecks_cons fourDatum19_checked <|
    fourPointChecks_cons fourDatum20_checked <|
    fourPointChecks_cons fourDatum21_checked <|
    fourPointChecks_cons fourDatum22_checked <|
    fourPointChecks_cons fourDatum23_checked <|
    fourPointChecks_cons fourDatum24_checked <|
    fourPointChecks_cons fourDatum25_checked <|
    fourPointChecks_cons fourDatum26_checked <|
    fourPointChecks_cons fourDatum27_checked <|
    fourPointChecks_cons fourDatum28_checked <|
    fourPointChecks_cons fourDatum29_checked <|
    fourPointChecks_cons fourDatum30_checked <|
    fourPointChecks_cons fourDatum31_checked <|
    fourPointChecks_cons fourDatum32_checked <|
    fourPointChecks_cons fourDatum33_checked <|
    fourPointChecks_cons fourDatum34_checked <|
    fourPointChecks_cons fourDatum35_checked <|
    fourPointChecks_cons fourDatum36_checked <|
    fourPointChecks_cons fourDatum37_checked <|
    fourPointChecks_cons fourDatum38_checked <|
    fourPointChecks_cons fourDatum39_checked <|
    fourPointChecks_cons fourDatum40_checked <|
    fourPointChecks_cons fourDatum41_checked <|
    fourPointChecks_cons fourDatum42_checked <|
    fourPointChecks_cons fourDatum43_checked <|
    fourPointChecks_cons fourDatum44_checked <|
    fourPointChecks_cons fourDatum45_checked <|
    fourPointChecks_cons fourDatum46_checked <|
    fourPointChecks_cons fourDatum47_checked <|
    fourPointChecks_cons fourDatum48_checked <|
    fourPointChecks_cons fourDatum49_checked <|
    fourPointChecks_cons fourDatum50_checked <|
    fourPointChecks_cons fourDatum51_checked <|
    fourPointChecks_cons fourDatum52_checked <|
    fourPointChecks_cons fourDatum53_checked <|
    fourPointChecks_cons fourDatum54_checked <|
    fourPointChecks_cons fourDatum55_checked <|
    fourPointChecks_cons fourDatum56_checked <|
    fourPointChecks_cons fourDatum57_checked <|
    fourPointChecks_cons fourDatum58_checked <|
    fourPointChecks_cons fourDatum59_checked <|
    fourPointChecks_cons fourDatum60_checked <|
    fourPointChecks_cons fourDatum61_checked <|
    fourPointChecks_cons fourDatum62_checked <|
    fourPointChecks_cons fourDatum63_checked <|
    fourPointChecks_cons fourDatum64_checked <|
    fourPointChecks_cons fourDatum65_checked <|
    fourPointChecks_cons fourDatum66_checked <|
    fourPointChecks_cons fourDatum67_checked <|
    fourPointChecks_cons fourDatum68_checked <|
    fourPointChecks_cons fourDatum69_checked <|
    fourPointChecks_cons fourDatum70_checked <|
    fourPointChecks_cons fourDatum71_checked <|
    fourPointChecks_cons fourDatum72_checked <|
    fourPointChecks_cons fourDatum73_checked <|
    fourPointChecks_cons fourDatum74_checked <|
    fourPointChecks_cons fourDatum75_checked <|
    fourPointChecks_cons fourDatum76_checked <|
    fourPointChecks_cons fourDatum77_checked <|
    fourPointChecks_cons fourDatum78_checked <|
    fourPointChecks_cons fourDatum79_checked <|
    fourPointChecks_cons fourDatum80_checked <|
    fourPointChecks_cons fourDatum81_checked <|
    fourPointChecks_cons fourDatum82_checked <|
    fourPointChecks_cons fourDatum83_checked <|
    fourPointChecks_cons fourDatum84_checked <|
    fourPointChecks_cons fourDatum85_checked <|
    fourPointChecks_cons fourDatum86_checked <|
    fourPointChecks_cons fourDatum87_checked <|
    fourPointChecks_cons fourDatum88_checked <|
    fourPointChecks_cons fourDatum89_checked <|
    fourPointChecks_cons fourDatum90_checked <|
    fourPointChecks_cons fourDatum91_checked <|
    fourPointChecks_cons fourDatum92_checked <|
    fourPointChecks_cons fourDatum93_checked <|
    fourPointChecks_cons fourDatum94_checked <|
    fourPointChecks_cons fourDatum95_checked <|
    fourPointChecks_cons fourDatum96_checked <|
    fourPointChecks_cons fourDatum97_checked <|
    fourPointChecks_cons fourDatum98_checked <|
    fourPointChecks_cons fourDatum99_checked <|
    fourPointChecks_cons fourDatum100_checked <|
    fourPointChecks_cons fourDatum101_checked <|
    fourPointChecks_cons fourDatum102_checked <|
    fourPointChecks_cons fourDatum103_checked <|
    fourPointChecks_cons fourDatum104_checked <|
    fourPointChecks_cons fourDatum105_checked <|
    fourPointChecks_cons fourDatum106_checked <|
    fourPointChecks_cons fourDatum107_checked <|
    fourPointChecks_cons fourDatum108_checked <|
    fourPointChecks_cons fourDatum109_checked <|
    fourPointChecks_cons fourDatum110_checked <|
    by intro w hw; cases hw
#print axioms fourPointData_checked
end S12
