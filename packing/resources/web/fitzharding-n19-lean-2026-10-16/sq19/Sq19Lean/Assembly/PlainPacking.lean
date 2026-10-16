import Sq19Lean.EndpointPacking
import Sq17Lean.PropagationWall

/-! A set-based statement of square packing, independent of the computational
classification. This bridge only assumes the coordinate lower bound. -/
namespace Sq19
open Sq17.Propagation

/-- Nineteen congruent closed unit squares, with arbitrary translations and
rotations, fit in `[0,L]²` with pairwise disjoint interiors. Touching is allowed. -/
def Feasible19 (L : ℝ) : Prop :=
  ∃ S : Fin 19 → Set (ℝ × ℝ),
    (∀ i, IsUnitSquare (S i)) ∧
    (∀ i, ∀ z ∈ S i, 0 ≤ z.1 ∧ z.1 ≤ L ∧ 0 ≤ z.2 ∧ z.2 ≤ L) ∧
    (∀ i j, i ≠ j → Disjoint (interior (S i)) (interior (S j)))

abbrev CoordinateLowerBound19 : Prop :=
  ∀ (L : ℝ) (p u : Fin 19 → ℝ × ℝ),
    (∀ i, (u i).1 ^ 2 + (u i).2 ^ 2 = 1) →
    (∀ i, Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2 ⊆ containerBox L) →
    (∀ i j, i ≠ j → Disjoint
      (interior (Sq17.sq (p i).1 (p i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (p j).1 (p j).2 (u j).1 (u j).2))) → side19 ≤ L

theorem feasible19_iff_of_lower (lower : CoordinateLowerBound19) (L : ℝ) :
    Feasible19 L ↔ side19 ≤ L := by
  constructor
  · rintro ⟨S, hunit, hfit, hdis⟩
    choose cx cy ux uy hu hS using hunit
    have hS' (i : Fin 19) : S i = Sq17.sq (cx i) (cy i) (ux i) (uy i) := by
      simpa only [Sq19.sq, Sq17.sq] using hS i
    apply lower L (fun i => (cx i, cy i)) (fun i => (ux i, uy i)) hu
    · intro i z hz
      change z ∈ containerBox L
      rw [← hS' i] at hz
      exact hfit i z hz
    · intro i j hij
      change Disjoint (interior (Sq17.sq (cx i) (cy i) (ux i) (uy i)))
        (interior (Sq17.sq (cx j) (cy j) (ux j) (uy j)))
      rw [← hS' i, ← hS' j]
      exact hdis i j hij
  · intro hL
    obtain ⟨S, hunit, hfit, hdis⟩ := endpoint_packing
    refine ⟨S, hunit, ?_, hdis⟩
    intro i z hz
    obtain ⟨hx0, hx1, hy0, hy1⟩ := hfit i z hz
    exact ⟨hx0, hx1.trans hL, hy0, hy1.trans hL⟩

end Sq19

#print axioms Sq19.feasible19_iff_of_lower
