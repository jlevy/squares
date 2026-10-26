import S12.Markers
import S12.Cliques
import S12.MarkerCliques
import Mathlib.Data.List.Chain
import Mathlib.Data.List.Sort

/-! Original finite marker classification, separated from geometric definitions.
The theorem statements are preserved. A proved D4 normalization replaces
repeated rational distance evaluation inside the finite kernel check. -/
namespace S12

set_option Elab.async false

def computedGroups : Finset (Finset Marker) :=
  ((cliques markerCompatible (List.finRange 16)).filter fun g => decide g.Nonempty).toFinset

set_option maxRecDepth 100000
set_option maxHeartbeats 0

/-- Extensional change of a clique relation preserves the enumerated list,
independently of the chosen decidability implementations. -/

theorem cliques_relation_congr {M : Type} [DecidableEq M]
    (r s : M → M → Prop) [DecidableRel r] [DecidableRel s]
    (h : ∀ i j, r i j ↔ s i j) (vs : List M) :
    cliques r vs = cliques s vs := by
  induction vs with
  | nil => rfl
  | cons i vs ih =>
      have hp : (fun g : Finset M => decide (∀ j ∈ g, r i j)) =
          (fun g : Finset M => decide (∀ j ∈ g, s i j)) := by
        funext g
        have he : (∀ j ∈ g, r i j) ↔ (∀ j ∈ g, s i j) := by
          constructor
          · intro hr j hj
            exact (h i j).mp (hr j hj)
          · intro hs j hj
            exact (h i j).mpr (hs j hj)
        by_cases hr : ∀ j ∈ g, r i j
        · have hs := he.mp hr
          exact (decide_eq_true hr).trans (decide_eq_true hs).symm
        · have hs : ¬ (∀ j ∈ g, s i j) := fun hs => hr (he.mpr hs)
          exact (decide_eq_false hr).trans (decide_eq_false hs).symm
      simp only [cliques, ih, hp]

/-- Decode a finite marker set from its sixteen membership bits. -/

private def markerGroupOfMask (mask : Nat) : Finset Marker :=
  ((List.finRange 16).filter fun i => mask.testBit i.val).toFinset

private def cachedMarkerMasks : List Nat :=
  [32768, 16384, 8192, 4096, 2048, 34816, 6144, 1024, 33792, 17408, 3072, 35840, 512, 16896, 8704,
   2560, 1536, 17920, 3584, 256, 8448, 4352, 2304, 6400, 1280, 3328, 768, 8960, 2816, 1792, 3840,
   128, 32896, 4224, 2176, 34944, 6272, 64, 32832, 4160, 2112, 34880, 6208, 192, 32960, 4288,
   2240, 35008, 6336, 32, 32800, 16416, 1056, 33824, 17440, 16, 32784, 16400, 1040, 33808, 17424,
   48, 32816, 16432, 1072, 33840, 17456, 8, 16392, 8200, 520, 16904, 8712, 4, 16388, 8196, 516,
   16900, 8708, 12, 16396, 8204, 524, 16908, 8716, 2, 8194, 4098, 258, 8450, 4354, 1, 8193, 4097,
   257, 8449, 4353, 3, 8195, 4099, 259, 8451, 4355]

private def tableMarkerMasks : List Nat :=
  [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 3, 257, 4097,
   8193, 258, 4098, 8194, 12, 516, 8196, 16388, 520, 8200, 16392, 48, 1040, 16400, 32784, 1056,
   16416, 32800, 192, 2112, 4160, 32832, 2176, 4224, 32896, 768, 1280, 2304, 4352, 8448, 1536,
   2560, 8704, 16896, 3072, 17408, 33792, 6144, 34816, 259, 4099, 8195, 4353, 8449, 4354, 8450,
   524, 8204, 16396, 8708, 16900, 8712, 16904, 1072, 16432, 32816, 17424, 33808, 17440, 33824,
   2240, 4288, 32960, 6208, 34880, 6272, 34944, 1792, 2816, 8960, 3328, 6400, 3584, 17920, 35840,
   4355, 8451, 8716, 16908, 17456, 33840, 6336, 35008, 3840]

-- These list equalities compare corresponding groups only. In particular
-- they avoid quadratic equality checks between nested finite sets.

private theorem cachedGroups_masks :
    markerCliques0.filter (fun g => decide g.Nonempty) =
      cachedMarkerMasks.map markerGroupOfMask := by rfl

private theorem groupList_masks :
    groupList = tableMarkerMasks.map markerGroupOfMask := by rfl

private theorem sorted_masks_eq :
    cachedMarkerMasks.insertionSort (· ≤ ·) =
      tableMarkerMasks.insertionSort (· ≤ ·) := by rfl

private theorem markerMasks_eq :
    cachedMarkerMasks.toFinset = tableMarkerMasks.toFinset := by
  have hc := List.perm_insertionSort (· ≤ ·) cachedMarkerMasks
  have ht := List.perm_insertionSort (· ≤ ·) tableMarkerMasks
  rw [sorted_masks_eq] at hc
  have hp := hc.symm.trans ht
  apply Finset.ext
  intro n
  simpa only [List.mem_toFinset] using
    (show n ∈ cachedMarkerMasks ↔ n ∈ tableMarkerMasks from hp.mem_iff)

private theorem tableMarkerMasks_nodup : tableMarkerMasks.Nodup := by
  apply (List.perm_insertionSort (· ≤ ·) tableMarkerMasks).nodup_iff.mp
  have hc : (tableMarkerMasks.insertionSort (· ≤ ·)).IsChain (· < ·) := by decide
  exact (List.isChain_iff_pairwise.mp hc).nodup

private def markerMaskOfGroup (g : Finset Marker) : Nat :=
  (List.finRange 16).foldl
    (fun mask i => if i ∈ g then mask + 2 ^ i.val else mask) 0

private theorem groupList_masks_roundtrip :
    groupList.map markerMaskOfGroup = tableMarkerMasks := by rfl

private theorem groupList_nodup : groupList.Nodup := by
  apply List.Nodup.of_map markerMaskOfGroup
  rw [groupList_masks_roundtrip]
  exact tableMarkerMasks_nodup

theorem computedGroups_eq : computedGroups = groupTable := by
  unfold computedGroups
  rw [cliques_relation_congr markerCompatible fastMarkerCompatible
    markerCompatible_iff_fast (List.finRange 16)]
  change (((cliques fastMarkerCompatible
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] : List Marker)).filter
    fun g => decide g.Nonempty).toFinset = groupTable)
  rw [markerCliques0_correct, cachedGroups_masks]
  unfold groupTable
  rw [groupList_masks]
  have hmem (n : Nat) : n ∈ cachedMarkerMasks ↔ n ∈ tableMarkerMasks := by
    simpa only [List.mem_toFinset] using Finset.ext_iff.mp markerMasks_eq n
  apply Finset.ext
  intro g
  simp only [List.mem_toFinset, List.mem_map, hmem]

theorem groupTable_card : groupTable.card = 103 := by
  calc
    groupTable.card = groupList.length := List.toFinset_card_of_nodup groupList_nodup
    _ = 103 := by decide

theorem diameter_group_in_table (g : Finset Marker) (h : DiameterOK g) :
    g ∈ groupTable := by
  rw [← computedGroups_eq]
  apply List.mem_toFinset.mpr
  apply List.mem_filter.mpr
  refine ⟨cliques_complete markerCompatible (List.finRange 16) g (by simp) h.2, ?_⟩
  exact decide_eq_true h.1

#print axioms diameter_group_in_table
end S12
