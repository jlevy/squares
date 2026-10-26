import S12.Packing
import S12.MarkerCoverGeometry
import S12.Raw

namespace S12

/-- No covering premise remains in the connection from geometry to the raw search. -/
theorem packing_marker_cover (p : NormalizedPacking) : MarkerCover p := by
  intro i
  obtain ⟨m, hm⟩ := marker_nonavoidance (p.square i)
    (by rw [p.congruent]; exact p.side_gt_one) (p.contained i)
  exact ⟨m, (mem_markerOwners p i m).mpr hm⟩

theorem packing_in_raw_search_unconditional (p : NormalizedPacking) :
    markerFamily p ∈ enumerate groupList id 16 Finset.univ 12 :=
  packing_in_raw_search p (packing_marker_cover p)

theorem exists_marker_code (p : NormalizedPacking) (i : Fin 12) :
    ∃ m ∈ candidateMasks, maskSupport m = markerOwners p i := by
  have h := markerOwners_in_table p (packing_marker_cover p) i
  rw [← masks_match_groups, List.mem_toFinset] at h
  exact List.mem_map.mp h

noncomputable def markerCode (p : NormalizedPacking) (i : Fin 12) : Nat :=
  Classical.choose (exists_marker_code p i)

theorem markerCode_spec (p : NormalizedPacking) (i : Fin 12) :
    markerCode p i ∈ candidateMasks ∧ maskSupport (markerCode p i) = markerOwners p i :=
  Classical.choose_spec (exists_marker_code p i)

theorem markerCode_injective (p : NormalizedPacking) : Function.Injective (markerCode p) := by
  intro i j h
  apply markerOwners_injective p (packing_marker_cover p)
  rw [← (markerCode_spec p i).2, ← (markerCode_spec p j).2, h]

noncomputable def codedMarkerFamily (p : NormalizedPacking) : Finset Nat :=
  Finset.univ.image (markerCode p)

theorem codedMarkerFamily_card (p : NormalizedPacking) : (codedMarkerFamily p).card = 12 := by
  rw [codedMarkerFamily, Finset.card_image_of_injective _ (markerCode_injective p)]
  decide

theorem codedMarkerFamily_admissible (p : NormalizedPacking) :
    Admissible candidateMasks maskSupport Finset.univ (codedMarkerFamily p) := by
  constructor
  · intro g hg
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hg
    refine ⟨(markerCode_spec p i).1, ?_, Finset.subset_univ _⟩
    rw [(markerCode_spec p i).2]
    exact packing_marker_cover p i
  · intro g hg h hh hne
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hg
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hh
    rw [(markerCode_spec p i).2, (markerCode_spec p j).2]
    apply markerOwners_disjoint p i j
    intro he; subst j; exact hne rfl

/-- Every actual normalized packing occurs in the concrete 157,499-family
enumeration, before the additional geometric pruning rules. -/
theorem packing_in_concrete_raw_search (p : NormalizedPacking) :
    codedMarkerFamily p ∈ rawFamilies := by
  have h := cachedEnumerate_complete candidateMasks maskSupport 16 Finset.univ
    (codedMarkerFamily p) (by decide) (codedMarkerFamily_admissible p)
  simpa only [codedMarkerFamily_card p, rawFamilies] using h

#print axioms packing_marker_cover
#print axioms packing_in_concrete_raw_search
end S12
