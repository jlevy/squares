import Sq19Lean.Cover.Orbit
import Sq19Lean.Census.Pattern

/-! From a packing to the census: every packing of 19 unit squares in a square of side at most
2443/500 gives a census packing (`Sq19.Census.Packs`) of the cells of one census orbit
representative. With the census exclusions (`census_excluded`, generated module Complete) this
leaves only the survivor masks; see `survivor_of_packing`. -/
namespace Sq19.Assembly
open Sq17.Propagation

/-- The cover and the census use the same 25 exact cells. -/
theorem vertices_eq : Sq19.Cover.vertices = Sq19.Census.vertices := by
  funext i; fin_cases i <;> rfl

theorem cell_eq (i : Fin 25) : Sq19.Cover.cell i = Sq19.Census.cell i := by
  simp only [Sq19.Cover.cell, Sq19.Cover.polygon, Sq19.Census.cell, vertices_eq]

/-- Every packing gives a census packing of the cells of a census orbit representative. -/
theorem packing_gives_census_packs (L : ℝ) (hL : L ≤ 2443/500)
    (p u : Fin 19 → ℝ × ℝ) (hunit : ∀ i, (u i).1^2+(u i).2^2=1)
    (hfit : ∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) :
    ∃ k : Fin Sq19.Cover.censusMasks.length, ∃ c : Fin 19 → Fin 25, Function.Injective c ∧
      Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.get k) ∧
      Sq19.Census.Packs c := by
  obtain ⟨g, k, hu, hf, hd, c, hinj, himg, hcell⟩ :=
    Sq19.Cover.packing_reaches_census L hL p u hunit hfit hdis
  refine ⟨k, c, hinj, himg, fun i => Sq19.Cover.actG g (Sq19.Cover.shifted L (p i)),
    fun i => Sq19.Cover.dirG g (u i), hu, fun i => ?_,
    fun i => (hf i).trans (Sq19.Cover.frame_in_container L hL), hd⟩
  rw [← cell_eq]; exact hcell i

/-- The covering hypothesis of `census_excluded` from the image of an assignment. -/
theorem sub_of_image {m : ℕ} (c : Fin 19 → Fin 25)
    (himg : Finset.univ.image c = Sq19.Cover.ofMask m) :
    ∀ d : Fin 25, m.testBit d = true → ∃ j, c j = d := by
  intro d hd
  have : d ∈ Finset.univ.image c := by
    rw [himg]; simp [Sq19.Cover.ofMask, hd]
  simpa using this

/-- With any exclusion predicate in the form `census_excluded` proves, a packing leaves a census
mask that is not excluded and a census packing of its cells. -/
theorem survivor_of_packing (Excluded : ℕ → Prop)
    (hexcl : ∀ m, Excluded m → ∀ {n : ℕ} (assign : Fin n → Fin 25),
      (∀ d : Fin 25, m.testBit d = true → ∃ j, assign j = d) → ¬ Sq19.Census.Packs assign)
    (L : ℝ) (hL : L ≤ 2443/500)
    (p u : Fin 19 → ℝ × ℝ) (hunit : ∀ i, (u i).1^2+(u i).2^2=1)
    (hfit : ∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L)
    (hdis : ∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) :
    ∃ k : Fin Sq19.Cover.censusMasks.length, ¬ Excluded (Sq19.Cover.censusMasks.get k) ∧
      ∃ c : Fin 19 → Fin 25, Function.Injective c ∧
        Finset.univ.image c = Sq19.Cover.ofMask (Sq19.Cover.censusMasks.get k) ∧
        Sq19.Census.Packs c := by
  obtain ⟨k, c, hinj, himg, hp⟩ := packing_gives_census_packs L hL p u hunit hfit hdis
  exact ⟨k, fun he => hexcl _ he c (sub_of_image c himg) hp, c, hinj, himg, hp⟩

end Sq19.Assembly

#print axioms Sq19.Assembly.packing_gives_census_packs
#print axioms Sq19.Assembly.survivor_of_packing
