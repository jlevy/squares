import Sq19Lean.Cover.Capacity

/-!
# Reduction of a packing to an injective cell assignment

For `L ≤ U = 2443/500`, a packing of unit squares in `[0, L]^2` is placed concentrically in the
cover frame by the translation `z ↦ z + (σ, σ)`, `σ = (U - L)/2`, as `s19/tools/census.c`
poses states. Every translated centre lies in some cell (`centre_box_covered`), no two in the
same cell (`cell_capacity_one`), so a choice of cells is injective.
-/
namespace Sq19.Cover
open Sq17.WallCapacity Sq17.Propagation

/-- The concentric shift of a container of side `L` into the cover frame. -/
noncomputable def shift (L : ℝ) : ℝ := (2443/500 - L)/2

/-- The translated centre. -/
noncomputable def shifted (L : ℝ) (p : ℝ × ℝ) : ℝ × ℝ := (p.1 + shift L, p.2 + shift L)

theorem shifted_square (L : ℝ) (p u : ℝ × ℝ) (z : ℝ × ℝ)
    (hz : z ∈ Sq17.sq (shifted L p).1 (shifted L p).2 u.1 u.2) :
    (z.1 - shift L, z.2 - shift L) ∈ Sq17.sq p.1 p.2 u.1 u.2 := by
  simp only [Sq17.sq, shifted, Set.mem_ofPred_eq] at hz ⊢
  have e1 : (z.1 - shift L - p.1) = z.1 - (p.1 + shift L) := by ring
  have e2 : (z.2 - shift L - p.2) = z.2 - (p.2 + shift L) := by ring
  rw [e1, e2]
  exact hz

/-- A square inside `[0, L]^2`, `L ≤ U`, is inside `[0, U]^2` after the concentric shift. -/
theorem shifted_fit (L : ℝ) (hL : L ≤ 2443/500) (p u : ℝ × ℝ)
    (hfit : Sq17.sq p.1 p.2 u.1 u.2 ⊆ containerBox L) :
    Sq17.sq (shifted L p).1 (shifted L p).2 u.1 u.2 ⊆ containerBox (2443/500) := by
  intro z hz
  have h := hfit (shifted_square L p u z hz)
  simp only [containerBox, Set.mem_ofPred_eq] at h ⊢
  unfold shift at h
  refine ⟨?_,?_,?_,?_⟩ <;> linarith [h.1, h.2.1, h.2.2.1, h.2.2.2]

/-- Translation preserves disjointness of the interiors. -/
theorem shifted_disjoint (L : ℝ) (p q u v : ℝ × ℝ)
    (hu : u.1^2+u.2^2=1) (hv : v.1^2+v.2^2=1)
    (hd : Disjoint (interior (Sq17.sq p.1 p.2 u.1 u.2)) (interior (Sq17.sq q.1 q.2 v.1 v.2))) :
    Disjoint (interior (Sq17.sq (shifted L p).1 (shifted L p).2 u.1 u.2))
      (interior (Sq17.sq (shifted L q).1 (shifted L q).2 v.1 v.2)) := by
  obtain ⟨a,b,hm,hgap⟩ := square_disjoint_unit_separator p q u.1 u.2 v.1 v.2 hu hv hd
  apply support_gap_disjoint _ _ _ _ _ _ _ _ hu hv hm
  simp only [shifted]
  linarith

/-- **Part (a), centre bound.** The shifted centre of a unit square inside `[0, L]^2`,
`L ≤ U`, lies in the centre box `[1/2, U - 1/2]^2 = [1/2, 2193/500]^2`. -/
theorem shifted_centre_in_box (L : ℝ) (hL : L ≤ 2443/500) (p u : ℝ × ℝ)
    (hu : u.1^2+u.2^2=1) (hfit : Sq17.sq p.1 p.2 u.1 u.2 ⊆ containerBox L) :
    1/2 ≤ (shifted L p).1 ∧ (shifted L p).1 ≤ 2193/500 ∧
      1/2 ≤ (shifted L p).2 ∧ (shifted L p).2 ≤ 2193/500 := by
  obtain ⟨h1,h2,h3,h4⟩ := fitsU_of_subset _ u hu (shifted_fit L hL p u hfit)
  have hh : 1 ≤ |u.1|+|u.2| := by
    have : 1 ≤ (|u.1|+|u.2|)^2 := by
      nlinarith [sq_abs u.1, sq_abs u.2, abs_nonneg u.1, abs_nonneg u.2,
        mul_nonneg (abs_nonneg u.1) (abs_nonneg u.2)]
    nlinarith [abs_nonneg u.1, abs_nonneg u.2]
  refine ⟨?_,?_,?_,?_⟩ <;> linarith

/-- **Reduction.** For `L ≤ 2443/500` and any family of unit squares with pairwise disjoint
interiors inside `[0, L]^2`, there is an injective map to the 25 cells such that every centre,
translated by `(σ, σ)` with `σ = (2443/500 - L)/2`, lies in its cell. -/
theorem exists_injective_cell_assignment {I : Type*} (L : ℝ) (hL : L ≤ 2443/500)
    (p u : I → ℝ × ℝ) (hunit : ∀ i, (u i).1^2+(u i).2^2=1)
    (hfit : ∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) :
    ∃ assign : I → Fin 25, Function.Injective assign ∧
      ∀ i, ((p i).1 + (2443/500 - L)/2, (p i).2 + (2443/500 - L)/2) ∈ cell (assign i) := by
  have hcov : ∀ i, ∃ k : Fin 25, shifted L (p i) ∈ cell k := fun i => by
    obtain ⟨h1,h2,h3,h4⟩ := shifted_centre_in_box L hL (p i) (u i) (hunit i) (hfit i)
    exact centre_box_covered _ _ h1 h2 h3 h4
  choose assign hassign using hcov
  refine ⟨assign, ?_, hassign⟩
  intro i j hij
  by_contra hne
  apply cell_capacity_one (assign i) (shifted L (p i)) (shifted L (p j)) (u i) (u j)
    (hunit i) (hunit j) (shifted_fit L hL _ _ (hfit i)) (shifted_fit L hL _ _ (hfit j))
    (hassign i) (by rw [hij]; exact hassign j)
  exact shifted_disjoint L _ _ _ _ (hunit i) (hunit j) (hdis i j hne)

/-- The nineteen-square form with the original `IsUnitSquare` predicate on sets: the returned
centres and directions describe the given squares exactly, nineteen distinct cells are
occupied, and each translated centre lies in its own cell. -/
theorem square_packing_cell_subset (L : ℝ) (hL : L ≤ 2443/500)
    (Q : Fin 19 → Set (ℝ × ℝ)) (hunit : ∀ i, Sq17.IsUnitSquare (Q i))
    (hfit : ∀ i, Q i ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint (interior (Q i)) (interior (Q j))) :
    ∃ p u : Fin 19 → ℝ × ℝ,
      (∀ i, (u i).1^2+(u i).2^2=1 ∧ Q i = Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2) ∧
      ∃ occupied : Finset (Fin 25), occupied.card = 19 ∧
        ∃ assign : Fin 19 → Fin 25, Function.Injective assign ∧
          ∀ i, assign i ∈ occupied ∧
            ((p i).1 + (2443/500 - L)/2, (p i).2 + (2443/500 - L)/2) ∈ cell (assign i) := by
  classical
  choose cx cy ux uy hn he using hunit
  let p : Fin 19 → ℝ × ℝ := fun i => (cx i, cy i)
  let u : Fin 19 → ℝ × ℝ := fun i => (ux i, uy i)
  refine ⟨p, u, fun i => ⟨hn i, he i⟩, ?_⟩
  obtain ⟨assign, hinj, ha⟩ := exists_injective_cell_assignment L hL p u hn
    (fun i => by dsimp [p, u]; rw [← he i]; exact hfit i)
    (fun i j hij => by dsimp [p, u]; rw [← he i, ← he j]; exact hdis i j hij)
  refine ⟨Finset.univ.image assign, ?_, assign, hinj, fun i => ⟨?_, ha i⟩⟩
  · rw [Finset.card_image_of_injective _ hinj]; simp
  · exact Finset.mem_image.mpr ⟨i, Finset.mem_univ i, rfl⟩

end Sq19.Cover

#print axioms Sq19.Cover.shifted_centre_in_box
#print axioms Sq19.Cover.exists_injective_cell_assignment
#print axioms Sq19.Cover.square_packing_cell_subset
