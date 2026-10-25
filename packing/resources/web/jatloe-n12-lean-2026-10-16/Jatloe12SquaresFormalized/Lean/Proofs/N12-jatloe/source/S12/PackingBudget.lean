import S12.PackingBridge
import S12.AuxPairCover
import S12.Budget

namespace S12
set_option Elab.async false

def fPairSupport (g : Finset Marker) : Prop :=
  (0∈g ∧ 1∈g) ∨ (2∈g ∧ 3∈g) ∨ (4∈g ∧ 5∈g) ∨ (6∈g ∧ 7∈g) ∨
  (8∈g ∧ 11∈g) ∨ (9∈g ∧ 10∈g)
def gPairSupport (g : Finset Marker) : Prop :=
  (0∈g ∧ 1∈g) ∨ (2∈g ∧ 3∈g) ∨ (4∈g ∧ 5∈g) ∨ (6∈g ∧ 7∈g) ∨
  (8∈g ∧ 9∈g) ∨ (10∈g ∧ 11∈g)
instance (g : Finset Marker) : Decidable (fPairSupport g) := inferInstanceAs (Decidable (_ ∨ _))
instance (g : Finset Marker) : Decidable (gPairSupport g) := inferInstanceAs (Decidable (_ ∨ _))

/- Decode each of the 103 candidate supports once, then use the literal
small marker groups. The original public tables still state mask semantics. -/
private theorem candidate_supports : candidateMasks.map maskSupport = groupList := by rfl

private theorem all_zip_map {α β : Type} (xs : List α) (f : α → β)
    (test : α → β → Bool) :
    (xs.zip (xs.map f)).all (fun pair => test pair.1 pair.2) =
      xs.all (fun x => test x (f x)) := by
  induction xs with
  | nil => rfl
  | cons x xs ih => simp only [List.map_cons,List.zip_cons_cons,List.all_cons,ih]

theorem f_exempt_table : candidateMasks.all (fun m => decide (m∈exempt0 ↔ fPairSupport (maskSupport m)))=true := by
  rw [← all_zip_map candidateMasks maskSupport
    (fun m g => decide (m∈exempt0 ↔ fPairSupport g)), candidate_supports]
  decide

theorem g_exempt_table : candidateMasks.all (fun m => decide (m∈exempt1 ↔ gPairSupport (maskSupport m)))=true := by
  rw [← all_zip_map candidateMasks maskSupport
    (fun m g => decide (m∈exempt1 ↔ gPairSupport g)), candidate_supports]
  decide

theorem code_f_exempt (p : NormalizedPacking) (i : Fin 12) :
    markerCode p i ∈ exempt0 ↔ FExempt (p.square i) := by
  have h := of_decide_eq_true (List.all_eq_true.mp f_exempt_table _ (markerCode_spec p i).1)
  rw [(markerCode_spec p i).2] at h
  simpa only [fPairSupport,mem_markerOwners,FExempt,CornerPairOwned,or_assoc] using h
theorem code_g_exempt (p : NormalizedPacking) (i : Fin 12) :
    markerCode p i ∈ exempt1 ↔ GExempt (p.square i) := by
  have h := of_decide_eq_true (List.all_eq_true.mp g_exempt_table _ (markerCode_spec p i).1)
  rw [(markerCode_spec p i).2] at h
  simpa only [gPairSupport,mem_markerOwners,GExempt,CornerPairOwned,or_assoc] using h

noncomputable def fOwners (p : NormalizedPacking) (i : Fin 12) : Finset (Fin 10) := by
  classical
  exact Finset.univ.filter fun m => (p.square i).Inside (fPoint m).1 (fPoint m).2
noncomputable def gOwners (p : NormalizedPacking) (i : Fin 12) : Finset (Fin 10) := by
  classical
  exact Finset.univ.filter fun m => (p.square i).Inside (fPoint m).2 (fPoint m).1
noncomputable def fExemptOwners (p : NormalizedPacking) : Finset (Fin 12) := by
  classical
  exact Finset.univ.filter fun i => FExempt (p.square i)
noncomputable def gExemptOwners (p : NormalizedPacking) : Finset (Fin 12) := by
  classical
  exact Finset.univ.filter fun i => GExempt (p.square i)

theorem fOwners_disjoint (p : NormalizedPacking) (i j : Fin 12) (hij : i≠j) :
    Disjoint (fOwners p i) (fOwners p j) := by
  classical
  apply Finset.disjoint_left.mpr
  intro m hi hj
  exact p.disjoint i j hij _ _ ⟨(Finset.mem_filter.mp hi).2,(Finset.mem_filter.mp hj).2⟩
theorem gOwners_disjoint (p : NormalizedPacking) (i j : Fin 12) (hij : i≠j) :
    Disjoint (gOwners p i) (gOwners p j) := by
  classical
  apply Finset.disjoint_left.mpr
  intro m hi hj
  exact p.disjoint i j hij _ _ ⟨(Finset.mem_filter.mp hi).2,(Finset.mem_filter.mp hj).2⟩

theorem fOwners_forced (p : NormalizedPacking) (i : Fin 12) (hi : i∉fExemptOwners p) :
    (fOwners p i).Nonempty := by
  classical
  by_contra he
  have hf : AvoidsF (p.square i) := by
    intro m hm
    exact he ⟨m,Finset.mem_filter.mpr ⟨Finset.mem_univ _,hm⟩⟩
  have hp := avoidingF_forces_pair (p.square i)
    (by rw [p.congruent]; exact p.side_gt_one) (p.contained i) hf
  exact hi (Finset.mem_filter.mpr ⟨Finset.mem_univ _,hp⟩)
theorem gOwners_forced (p : NormalizedPacking) (i : Fin 12) (hi : i∉gExemptOwners p) :
    (gOwners p i).Nonempty := by
  classical
  by_contra he
  have hf : AvoidsG (p.square i) := by
    intro m hm
    exact he ⟨m,Finset.mem_filter.mpr ⟨Finset.mem_univ _,hm⟩⟩
  have hp := avoidingG_forces_pair (p.square i)
    (by rw [p.congruent]; exact p.side_gt_one) (p.contained i) hf
  exact hi (Finset.mem_filter.mpr ⟨Finset.mem_univ _,hp⟩)

theorem f_exempt_image (p : NormalizedPacking) :
    (fExemptOwners p).image (markerCode p) = codedMarkerFamily p ∩ exempt0 := by
  classical
  ext m
  constructor
  · intro hm
    obtain ⟨i,hi,rfl⟩ := Finset.mem_image.mp hm
    exact Finset.mem_inter.mpr ⟨Finset.mem_image.mpr ⟨i,Finset.mem_univ _,rfl⟩,
      (code_f_exempt p i).mpr (Finset.mem_filter.mp hi).2⟩
  · intro hm
    obtain ⟨hf,he⟩ := Finset.mem_inter.mp hm
    obtain ⟨i,_,rfl⟩ := Finset.mem_image.mp hf
    exact Finset.mem_image.mpr ⟨i,Finset.mem_filter.mpr ⟨Finset.mem_univ _,(code_f_exempt p i).mp he⟩,rfl⟩
theorem g_exempt_image (p : NormalizedPacking) :
    (gExemptOwners p).image (markerCode p) = codedMarkerFamily p ∩ exempt1 := by
  classical
  ext m
  constructor
  · intro hm
    obtain ⟨i,hi,rfl⟩ := Finset.mem_image.mp hm
    exact Finset.mem_inter.mpr ⟨Finset.mem_image.mpr ⟨i,Finset.mem_univ _,rfl⟩,
      (code_g_exempt p i).mpr (Finset.mem_filter.mp hi).2⟩
  · intro hm
    obtain ⟨hf,he⟩ := Finset.mem_inter.mp hm
    obtain ⟨i,_,rfl⟩ := Finset.mem_image.mp hf
    exact Finset.mem_image.mpr ⟨i,Finset.mem_filter.mpr ⟨Finset.mem_univ _,(code_g_exempt p i).mp he⟩,rfl⟩

/-- Both exemption budgets appearing in the concrete early filter now follow
from the geometry of every normalized packing. -/
theorem packing_pair_budgets (p : NormalizedPacking) :
    2≤(codedMarkerFamily p ∩ exempt0).card ∧ 2≤(codedMarkerFamily p ∩ exempt1).card := by
  have hf := pair_budget (fOwners p) (fExemptOwners p) (fOwners_disjoint p) (fOwners_forced p)
  have hg := pair_budget (gOwners p) (gExemptOwners p) (gOwners_disjoint p) (gOwners_forced p)
  rw [← f_exempt_image p,Finset.card_image_of_injective _ (markerCode_injective p)]
  rw [← g_exempt_image p,Finset.card_image_of_injective _ (markerCode_injective p)]
  exact ⟨hf,hg⟩

theorem packing_f_owner_budget (p : NormalizedPacking) (i : Fin 12) :
    (fOwners p i).card ≤ (fExemptOwners p).card - 2 + (if i∈fExemptOwners p then 0 else 1) := by
  classical
  exact individual_budget _ _ (fOwners_disjoint p) (fOwners_forced p) i
theorem packing_g_owner_budget (p : NormalizedPacking) (i : Fin 12) :
    (gOwners p i).card ≤ (gExemptOwners p).card - 2 + (if i∈gExemptOwners p then 0 else 1) := by
  classical
  exact individual_budget _ _ (gOwners_disjoint p) (gOwners_forced p) i

#print axioms packing_pair_budgets
end S12
