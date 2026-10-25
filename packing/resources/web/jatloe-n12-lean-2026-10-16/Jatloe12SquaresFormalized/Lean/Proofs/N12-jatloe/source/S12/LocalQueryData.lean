import S12.LocalQueryDataChunks.Chunk00
import S12.LocalQueryDataChunks.Chunk01
import S12.LocalQueryDataChunks.Chunk02
import S12.LocalQueryDataChunks.Chunk03
import S12.LocalQueryDataChunks.Chunk04
import S12.LocalQueryDataChunks.Chunk05
import S12.LocalQueryDataChunks.Chunk06
namespace S12
set_option maxRecDepth 100000
set_option maxHeartbeats 0
set_option Elab.async false
def localQueries : List LocalQuery := queryChunk0 ++ queryChunk1 ++ queryChunk2 ++ queryChunk3 ++ queryChunk4 ++ queryChunk5 ++ queryChunk6 ++ queryChunk7 ++ queryChunk8 ++ queryChunk9 ++ queryChunk10 ++ queryChunk11 ++ queryChunk12 ++ queryChunk13 ++ queryChunk14 ++ queryChunk15 ++ queryChunk16 ++ queryChunk17 ++ queryChunk18 ++ queryChunk19 ++ queryChunk20 ++ queryChunk21 ++ queryChunk22 ++ queryChunk23 ++ queryChunk24 ++ queryChunk25 ++ queryChunk26 ++ queryChunk27 ++ queryChunk28 ++ queryChunk29 ++ queryChunk30 ++ queryChunk31 ++ queryChunk32 ++ queryChunk33 ++ queryChunk34
theorem localQueries_length : localQueries.length=1721 := by
  simp only [localQueries,List.length_append]
  decide
private theorem queryChecks_append {xs ys : List LocalQuery}
    (hx : xs.all (fun w => decide w.Check)=true)
    (hy : ys.all (fun w => decide w.Check)=true) :
    (xs++ys).all (fun w => decide w.Check)=true := by
  rw [List.all_append,hx,hy]
  rfl

theorem localQueries_all_checked : localQueries.all (fun w => decide w.Check)=true := by
  have h1 := queryChecks_append queryChunk0_checked queryChunk1_checked
  have h2 := queryChecks_append h1 queryChunk2_checked
  have h3 := queryChecks_append h2 queryChunk3_checked
  have h4 := queryChecks_append h3 queryChunk4_checked
  have h5 := queryChecks_append h4 queryChunk5_checked
  have h6 := queryChecks_append h5 queryChunk6_checked
  have h7 := queryChecks_append h6 queryChunk7_checked
  have h8 := queryChecks_append h7 queryChunk8_checked
  have h9 := queryChecks_append h8 queryChunk9_checked
  have h10 := queryChecks_append h9 queryChunk10_checked
  have h11 := queryChecks_append h10 queryChunk11_checked
  have h12 := queryChecks_append h11 queryChunk12_checked
  have h13 := queryChecks_append h12 queryChunk13_checked
  have h14 := queryChecks_append h13 queryChunk14_checked
  have h15 := queryChecks_append h14 queryChunk15_checked
  have h16 := queryChecks_append h15 queryChunk16_checked
  have h17 := queryChecks_append h16 queryChunk17_checked
  have h18 := queryChecks_append h17 queryChunk18_checked
  have h19 := queryChecks_append h18 queryChunk19_checked
  have h20 := queryChecks_append h19 queryChunk20_checked
  have h21 := queryChecks_append h20 queryChunk21_checked
  have h22 := queryChecks_append h21 queryChunk22_checked
  have h23 := queryChecks_append h22 queryChunk23_checked
  have h24 := queryChecks_append h23 queryChunk24_checked
  have h25 := queryChecks_append h24 queryChunk25_checked
  have h26 := queryChecks_append h25 queryChunk26_checked
  have h27 := queryChecks_append h26 queryChunk27_checked
  have h28 := queryChecks_append h27 queryChunk28_checked
  have h29 := queryChecks_append h28 queryChunk29_checked
  have h30 := queryChecks_append h29 queryChunk30_checked
  have h31 := queryChecks_append h30 queryChunk31_checked
  have h32 := queryChecks_append h31 queryChunk32_checked
  have h33 := queryChecks_append h32 queryChunk33_checked
  exact queryChecks_append h33 queryChunk34_checked
theorem localQueries_checked : ∀ w∈localQueries, w.Check := by
  intro w hw
  exact of_decide_eq_true (List.all_eq_true.mp localQueries_all_checked w hw)
#print axioms localQueries_checked
end S12
