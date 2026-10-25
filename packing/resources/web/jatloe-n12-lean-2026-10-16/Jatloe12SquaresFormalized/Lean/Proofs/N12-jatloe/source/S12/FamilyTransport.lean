import S12.HullBridge
import S12.MaskTransport
import Mathlib.Data.List.Nodup
import Mathlib.Data.List.Sort

namespace S12
set_option Elab.async false
set_option maxRecDepth 100000
set_option maxHeartbeats 0

def Transform.markerList (t : Transform) : List Nat :=
  (List.finRange 16).map (fun i => (t.markerAction i).val)
def Transform.maskAction (t : Transform) (m : Nat) : Nat := permuteMask t.markerList m

theorem transform_rows_match : allTransforms.map Transform.markerList=markerPerms := by rfl

/-- Distinct supports follow from the already checked classification cardinality.
No second quadratic comparison of the 103 finite sets is needed. -/
theorem candidate_supports_distinct : (candidateMasks.map maskSupport).Nodup := by
  have hc : (↑(candidateMasks.map maskSupport) : Multiset (Finset Marker)).toFinset.card =
      (↑(candidateMasks.map maskSupport) : Multiset (Finset Marker)).card := by
    change (candidateMasks.map maskSupport).toFinset.card =
      (candidateMasks.map maskSupport).length
    rw [masks_match_groups, groupTable_card, List.length_map]
    rfl
  have hn : (↑(candidateMasks.map maskSupport) : Multiset (Finset Marker)).Nodup :=
    (Multiset.toFinset_card_eq_card_iff_nodup
      (m := (↑(candidateMasks.map maskSupport) : Multiset (Finset Marker)))).mp hc
  exact Multiset.coe_nodup.mp hn

theorem candidate_support_injective (m n : Nat) (hm : m∈candidateMasks) (hn : n∈candidateMasks)
    (h : maskSupport m=maskSupport n) : m=n :=
  List.inj_on_of_nodup_map candidate_supports_distinct hm hn h

-- Separate opaque symmetry identities keep reduction caches local to each
-- transformation, while the public argument uses only these eight facts.

private theorem transformed_masks_sorted_fff :
    (candidateMasks.map (Transform.maskAction ⟨false,false,false⟩)).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by decide +kernel

private theorem transformed_masks_sorted_fft :
    (candidateMasks.map (Transform.maskAction ⟨false,false,true⟩)).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by decide +kernel

private theorem transformed_masks_sorted_ftf :
    (candidateMasks.map (Transform.maskAction ⟨false,true,false⟩)).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by decide +kernel

private theorem transformed_masks_sorted_ftt :
    (candidateMasks.map (Transform.maskAction ⟨false,true,true⟩)).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by decide +kernel

private theorem transformed_masks_sorted_tff :
    (candidateMasks.map (Transform.maskAction ⟨true,false,false⟩)).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by decide +kernel

private theorem transformed_masks_sorted_tft :
    (candidateMasks.map (Transform.maskAction ⟨true,false,true⟩)).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by decide +kernel

private theorem transformed_masks_sorted_ttf :
    (candidateMasks.map (Transform.maskAction ⟨true,true,false⟩)).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by decide +kernel

private theorem transformed_masks_sorted_ttt :
    (candidateMasks.map (Transform.maskAction ⟨true,true,true⟩)).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by decide +kernel

private theorem transformed_masks_sorted (t : Transform) :
    (candidateMasks.map t.maskAction).insertionSort (· ≤ ·) =
      candidateMasks.insertionSort (· ≤ ·) := by
  rcases t with ⟨x,y,z⟩
  cases x <;> cases y <;> cases z
  · exact transformed_masks_sorted_fff
  · exact transformed_masks_sorted_fft
  · exact transformed_masks_sorted_ftf
  · exact transformed_masks_sorted_ftt
  · exact transformed_masks_sorted_tff
  · exact transformed_masks_sorted_tft
  · exact transformed_masks_sorted_ttf
  · exact transformed_masks_sorted_ttt

private theorem transformed_masks_perm (t : Transform) :
    (candidateMasks.map t.maskAction).Perm candidateMasks := by
  have hm := List.perm_insertionSort (· ≤ ·) (candidateMasks.map t.maskAction)
  rw [transformed_masks_sorted] at hm
  exact hm.symm.trans (List.perm_insertionSort (· ≤ ·) candidateMasks)

theorem transform_masks_checked : allTransforms.all (fun t => candidateMasks.all (fun m =>
    decide (t.maskAction m∈candidateMasks ∧ maskSupport (t.maskAction m)=(maskSupport m).image t.markerAction)))=true := by
  apply List.all_eq_true.mpr
  intro t _
  apply List.all_eq_true.mpr
  intro m hm
  apply decide_eq_true
  constructor
  · exact (transformed_masks_perm t).mem_iff.mp (List.mem_map.mpr ⟨m,hm,rfl⟩)
  · simpa only [Transform.maskAction, Transform.markerList] using
      MaskEncoding.transform_support t m

theorem mask_action_spec (t : Transform) (ht : t∈allTransforms) (m : Nat) (hm : m∈candidateMasks) :
    t.maskAction m∈candidateMasks ∧ maskSupport (t.maskAction m)=(maskSupport m).image t.markerAction := by
  exact of_decide_eq_true (List.all_eq_true.mp (List.all_eq_true.mp transform_masks_checked t ht) m hm)

/-- Check only the existing row shape; auxiliary-domain payload is irrelevant. -/
private def coverRowShape (r : CoverRow) : Bool :=
  decide (r.groups.card=12 ∧ ∀ m∈r.groups, m∈candidateMasks)

-- Reuse the original24 source chunks. Each opaque fact gets a bounded
-- reduction cache; append composition proves the original universal check.
private theorem coverRow_shapes_0 : rows0.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_1 : rows1.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_2 : rows2.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_3 : rows3.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_4 : rows4.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_5 : rows5.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_6 : rows6.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_7 : rows7.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_8 : rows8.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_9 : rows9.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_10 : rows10.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_11 : rows11.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_12 : rows12.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_13 : rows13.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_14 : rows14.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_15 : rows15.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_16 : rows16.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_17 : rows17.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_18 : rows18.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_19 : rows19.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_20 : rows20.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_21 : rows21.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_22 : rows22.all coverRowShape = true := by
  decide +kernel

private theorem coverRow_shapes_23 : rows23.all coverRowShape = true := by
  decide +kernel

theorem coverRow_shapes_checked : coverRows.all (fun r =>
    decide (r.groups.card=12 ∧ ∀ m∈r.groups, m∈candidateMasks))=true  := by
  change coverRows.all coverRowShape = true
  simp only [coverRows, List.all_append,
    coverRow_shapes_0, coverRow_shapes_1, coverRow_shapes_2, coverRow_shapes_3, coverRow_shapes_4, coverRow_shapes_5,
    coverRow_shapes_6, coverRow_shapes_7, coverRow_shapes_8, coverRow_shapes_9, coverRow_shapes_10, coverRow_shapes_11,
    coverRow_shapes_12, coverRow_shapes_13, coverRow_shapes_14, coverRow_shapes_15, coverRow_shapes_16, coverRow_shapes_17,
    coverRow_shapes_18, coverRow_shapes_19, coverRow_shapes_20, coverRow_shapes_21, coverRow_shapes_22, coverRow_shapes_23,
    Bool.and_self]
theorem coverRow_shape (r : CoverRow) (hr : r∈coverRows) :
    r.groups.card=12 ∧ ∀ m∈r.groups, m∈candidateMasks :=
  of_decide_eq_true (List.all_eq_true.mp coverRow_shapes_checked r hr)

noncomputable def Transform.pullPacking (t : Transform) (p : NormalizedPacking) : NormalizedPacking where
  square := fun i => t.pull (p.square i)
  commonSide := p.commonSide
  side_gt_one := p.side_gt_one
  side_le := p.side_le
  congruent := by intro i; simpa using p.congruent i
  contained := by intro i; exact container_transform t (p.square i) (p.contained i)
  disjoint := by
    intro i j hij x y h
    exact p.disjoint i j hij _ _ ⟨(inside_pull t (p.square i) x y).mp h.1,
      (inside_pull t (p.square j) x y).mp h.2⟩

theorem exact_markers_pull (t : Transform) (ht : t∈allTransforms) (q : S12Pilot.OpenSquare)
    (m : Nat) (hm : m∈candidateMasks) (hq : ExactMarkers q (maskSupport (t.maskAction m))) :
    ExactMarkers (t.pull q) (maskSupport m) := by
  intro i
  rw [owns_transform,hq,(mask_action_spec t ht m hm).2]
  constructor
  · intro h
    obtain ⟨j,hj,he⟩ := Finset.mem_image.mp h
    have hh := t.markerAction_injective he
    simpa [hh] using hj
  · intro h
    exact Finset.mem_image.mpr ⟨i,h,rfl⟩

/-- An orbit membership for all marker owners transports an actual packing
to the representative. The container and every ownership condition move
together; no independent relabeling of a local corner is used. -/
theorem transport_to_representative (p : NormalizedPacking) (r : CoverRow) (hr : r∈coverRows)
    (ho : codedMarkerFamily p∈orbit r.groups) :
    ∃ t∈allTransforms, codedMarkerFamily (t.pullPacking p)=r.groups := by
  have ho' : codedMarkerFamily p∈allTransforms.map (fun t => r.groups.image t.maskAction) := by
    change codedMarkerFamily p ∈ allTransforms.map (fun t => r.groups.image (permuteMask t.markerList))
    simpa only [orbit,← transform_rows_match,List.map_map,Function.comp_def,Transform.maskAction] using ho
  obtain ⟨t,ht,hfam⟩ := List.mem_map.mp ho'
  refine ⟨t,ht,?_⟩
  have hshape := coverRow_shape r hr
  have hsub : r.groups⊆codedMarkerFamily (t.pullPacking p) := by
    intro m hm
    have ha : t.maskAction m∈codedMarkerFamily p := by
      rw [← hfam]
      exact Finset.mem_image.mpr ⟨m,hm,rfl⟩
    obtain ⟨i,_,hi⟩ := Finset.mem_image.mp ha
    have he : ExactMarkers (p.square i) (maskSupport (t.maskAction m)) := by
      rw [← hi]
      exact coded_exact p i
    have hnew := exact_markers_pull t ht (p.square i) m (hshape.2 m hm) he
    have hsupport : maskSupport (markerCode (t.pullPacking p) i)=maskSupport m := by
      apply Finset.ext
      intro j
      exact (coded_exact (t.pullPacking p) i j).symm.trans (hnew j)
    have hcode := candidate_support_injective _ _ (markerCode_spec (t.pullPacking p) i).1
      (hshape.2 m hm) hsupport
    exact Finset.mem_image.mpr ⟨i,Finset.mem_univ _,hcode⟩
  apply (Finset.eq_of_subset_of_card_le hsub _).symm
  rw [codedMarkerFamily_card,hshape.1]

theorem packing_reduction_to_577_representatives (p : NormalizedPacking) :
    ∃ t∈allTransforms, ∃ r∈coverRows, codedMarkerFamily (t.pullPacking p)=r.groups := by
  obtain ⟨r,hr,ho⟩ := packing_reduction_to_577 p
  obtain ⟨t,ht,he⟩ := transport_to_representative p r hr ho
  exact ⟨t,ht,r,hr,he⟩

#print axioms transport_to_representative
#print axioms packing_reduction_to_577_representatives
end S12
