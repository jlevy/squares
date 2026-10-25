import S12.DiameterClassification
import S12.Enumeration

namespace S12
open S12Pilot

/-- A packing of twelve congruent open squares in the closed 4-by-4 container.
The side normalization used for the contradiction is made explicit. -/
structure NormalizedPacking where
  square : Fin 12 → OpenSquare
  commonSide : ℝ
  side_gt_one : 1 < commonSide
  side_le : commonSide ≤ 1001 / 1000
  congruent : ∀ i, (square i).side = commonSide
  contained : ∀ i x y, (square i).Inside x y → 0 ≤ x ∧ x ≤ 4 ∧ 0 ≤ y ∧ y ≤ 4
  disjoint : ∀ i j, i ≠ j → ∀ x y, ¬ ((square i).Inside x y ∧ (square j).Inside x y)

noncomputable def markerOwners (p : NormalizedPacking) (i : Fin 12) : Finset Marker := by
  classical
  exact Finset.univ.filter (Owns (p.square i))

@[simp] theorem mem_markerOwners (p : NormalizedPacking) (i : Fin 12) (m : Marker) :
    m ∈ markerOwners p i ↔ Owns (p.square i) m := by
  classical
  simp [markerOwners]

theorem markerOwners_disjoint (p : NormalizedPacking) (i j : Fin 12) (hij : i ≠ j) :
    Disjoint (markerOwners p i) (markerOwners p j) := by
  apply Finset.disjoint_left.mpr
  intro m hi hj
  exact p.disjoint i j hij _ _ ⟨(mem_markerOwners p i m).mp hi, (mem_markerOwners p j m).mp hj⟩

/-- Every square owns a marker. Proved for all normalized packings in
PackingBridge.lean using the geometric marker-cover theorem. -/
def MarkerCover (p : NormalizedPacking) : Prop :=
  ∀ i, (markerOwners p i).Nonempty

theorem markerOwners_in_table (p : NormalizedPacking) (hcover : MarkerCover p) (i : Fin 12) :
    markerOwners p i ∈ groupTable := by
  apply actual_group_in_table (p.square i) (by rw [p.congruent]; exact p.side_le)
    (markerOwners p i) (hcover i)
  intro m hm
  exact (mem_markerOwners p i m).mp hm

noncomputable def markerFamily (p : NormalizedPacking) : Finset (Finset Marker) :=
  Finset.univ.image (markerOwners p)

theorem markerOwners_injective (p : NormalizedPacking) (hcover : MarkerCover p) :
    Function.Injective (markerOwners p) := by
  intro i j he
  by_contra hne
  obtain ⟨m, hm⟩ := hcover i
  have hm' : m ∈ markerOwners p j := by rw [← he]; exact hm
  exact Finset.disjoint_left.mp (markerOwners_disjoint p i j hne) hm hm'

theorem markerFamily_card (p : NormalizedPacking) (hcover : MarkerCover p) :
    (markerFamily p).card = 12 := by
  rw [markerFamily, Finset.card_image_of_injective _ (markerOwners_injective p hcover)]
  decide

theorem markerFamily_admissible (p : NormalizedPacking) (hcover : MarkerCover p) :
    Admissible groupList id Finset.univ (markerFamily p) := by
  constructor
  · intro g hg
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hg
    refine ⟨?_, hcover i, Finset.subset_univ _⟩
    exact List.mem_toFinset.mp (markerOwners_in_table p hcover i)
  · intro g hg h hh hne
    obtain ⟨i, _, rfl⟩ := Finset.mem_image.mp hg
    obtain ⟨j, _, rfl⟩ := Finset.mem_image.mp hh
    apply markerOwners_disjoint p i j
    intro he; subst j; exact hne rfl

/-- The geometric-to-enumeration connection, with only the named marker cover
premise left open. The no-overlap, nonempty-owner, and diameter details are
proved rather than assumed as unexplained table conditions. -/
theorem packing_in_raw_search (p : NormalizedPacking) (hcover : MarkerCover p) :
    markerFamily p ∈ enumerate groupList id 16 Finset.univ 12 := by
  have h := enumerate_complete groupList id 16 Finset.univ (markerFamily p)
    (by decide) (markerFamily_admissible p hcover)
  simpa only [markerFamily_card p hcover] using h

#print axioms packing_in_raw_search
end S12
