import Sq17Lean.HalfPlaneAssemblySkeleton

/-! A statement-level bridge to seventeen sets that are genuine unit squares.
No cells, traces, cached bounds, or representation predicate appear here. -/
namespace Sq17.HalfPlaneAssembly

def PlainPacking (L : ℝ) : Prop :=
  ∃ squares : Fin 17 → Set (ℝ × ℝ),
    (∀ i, Sq17.IsUnitSquare (squares i)) ∧
    (∀ i, squares i ⊆ Propagation.containerBox L) ∧
    (∀ i j, i ≠ j → Disjoint (interior (squares i)) (interior (squares j)))

theorem feasible_iff_plainPacking (L : ℝ) : Feasible L ↔ PlainPacking L := by
  constructor
  · rintro ⟨c, u, hu, hf, hd⟩
    refine ⟨fun i => Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2, ?_, hf, hd⟩
    intro i
    exact ⟨(c i).1, (c i).2, (u i).1, (u i).2, hu i, rfl⟩
  · rintro ⟨squares, hu, hf, hd⟩
    choose cx cy ux uy hunit heq using hu
    refine ⟨fun i => (cx i, cy i), fun i => (ux i, uy i), hunit, ?_, ?_⟩
    · intro i
      change Sq17.sq (cx i) (cy i) (ux i) (uy i) ⊆ _
      rw [← heq i]
      exact hf i
    · intro i j hij
      change Disjoint (interior (Sq17.sq (cx i) (cy i) (ux i) (uy i)))
        (interior (Sq17.sq (cx j) (cy j) (ux j) (uy j)))
      rw [← heq i, ← heq j]
      exact hd i j hij

/-- The already established upper bound is a nonvacuous witness to the plain
packing definition, independently of all lower-bound assembly obligations. -/
theorem endpoint_plainPacking : PlainPacking EndpointGeometry.side :=
  EndpointGeometry.endpoint_packing

end Sq17.HalfPlaneAssembly

#print axioms Sq17.HalfPlaneAssembly.feasible_iff_plainPacking
#print axioms Sq17.HalfPlaneAssembly.endpoint_plainPacking
