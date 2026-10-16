import Sq19Lean.Capture.Basic
import Sq19Lean.Census.Pattern

/-! Links between the capture statements and the census frame.

Frame shift: a packing in `[0, L]^2` translated by `(σ, σ)` lies in the census container `[0, 2443/500]^2`
when `L + σ ≤ 2443/500`; the census cells of the translate are the capture cells (vertices shifted by `-σ`) of
the packing itself. The packing in `[0, L]^2` lies in the trace container `[-shift, side + shift]^2` when
`L ≤ side`. No concentric placement is needed: the translation is the same `σ` for every `L`. -/
namespace Sq19.Capture
open Sq17.Propagation Sq17.Propagation.HalfPlaneState

def shiftVertex (s : ℚ) (v : ℚ × ℚ) : ℚ × ℚ := (v.1 - s, v.2 - s)

theorem hull_shift (V : List (ℚ × ℚ)) (s : ℚ) (c : ℝ × ℝ)
    (h : c + ((s:ℝ), (s:ℝ)) ∈ convexHull ℝ (realPoint '' {v | v ∈ V})) :
    c ∈ convexHull ℝ (realPoint '' {v | v ∈ V.map (shiftVertex s)}) := by
  let T : (ℝ × ℝ) →ᵃ[ℝ] (ℝ × ℝ) := (AffineEquiv.constVAdd ℝ (ℝ × ℝ) (-((s:ℝ), (s:ℝ)))).toAffineMap
  have hT : ∀ z, T z = z - ((s:ℝ), (s:ℝ)) := by
    intro z; simp [T, AffineEquiv.constVAdd, sub_eq_neg_add]
  have himg : T '' (realPoint '' {v | v ∈ V}) = realPoint '' {v | v ∈ V.map (shiftVertex s)} := by
    ext z
    simp only [Set.mem_image, Set.mem_setOf_eq, List.mem_map]
    constructor
    · rintro ⟨_, ⟨v, hv, rfl⟩, rfl⟩
      refine ⟨shiftVertex s v, ⟨v, hv, rfl⟩, ?_⟩
      rw [hT]; simp [realPoint, shiftVertex]
    · rintro ⟨_, ⟨v, hv, rfl⟩, rfl⟩
      refine ⟨realPoint v, ⟨v, hv, rfl⟩, ?_⟩
      rw [hT]; simp [realPoint, shiftVertex]
  have := Set.mem_image_of_mem T h
  rw [AffineMap.image_convexHull, himg, hT] at this
  simpa using this

theorem sq_translate (cx cy ux uy a b : ℝ) :
    Sq17.sq (cx + a) (cy + b) ux uy = (fun p => p + (a, b)) '' Sq17.sq cx cy ux uy := by
  ext p
  constructor
  · intro hp
    refine ⟨p - (a, b), ?_, by simp⟩
    simp only [Sq17.sq, Set.mem_setOf_eq, Prod.fst_sub, Prod.snd_sub] at hp ⊢
    convert hp using 3 <;> ring_nf
  · rintro ⟨q, hq, rfl⟩
    simp only [Sq17.sq, Set.mem_setOf_eq, Prod.fst_add, Prod.snd_add] at hq ⊢
    convert hq using 3 <;> ring_nf

theorem translate_disjoint (S S' : Set (ℝ × ℝ)) (a : ℝ × ℝ) (h : Disjoint (interior S) (interior S')) :
    Disjoint (interior ((fun p => p + a) '' S)) (interior ((fun p => p + a) '' S')) := by
  have e := (Homeomorph.addRight a).image_interior
  simp only [Homeomorph.coe_addRight] at e
  rw [← e S, ← e S']
  exact (Set.disjoint_image_iff (add_left_injective a)).mpr h

theorem container_sub_trace (L side shift : ℝ) (hL : L ≤ side) (hs : 0 ≤ shift) :
    containerBox L ⊆ traceContainer side shift := by
  rintro z ⟨h1, h2, h3, h4⟩
  exact ⟨by linarith, by linarith, by linarith, by linarith⟩

theorem translate_container (L s U : ℝ) (hs : 0 ≤ s) (hU : L + s ≤ U) (S : Set (ℝ × ℝ))
    (h : S ⊆ containerBox L) : (fun p => p + (s, s)) '' S ⊆ containerBox U := by
  rintro _ ⟨z, hz, rfl⟩
  obtain ⟨h1, h2, h3, h4⟩ := h hz
  exact ⟨by simp; linarith, by simp; linarith, by simp; linarith, by simp; linarith⟩

/-- A packing in `[0, L]^2`, translated by `(s, s)`, is a packing in the census container with the same
directions; its centres are the translated ones. -/
theorem translate_packing (L s : ℝ) (hs : 0 ≤ s) (hU : L + s ≤ 2443/500) (n : ℕ) (c u : ℕ → ℝ × ℝ)
    (hd : ∀ i j, i < n → j < n → i ≠ j → Disjoint
      (interior (Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2))
      (interior (Sq17.sq (c j).1 (c j).2 (u j).1 (u j).2)))
    (hfit : ∀ i, i < n → Sq17.sq (c i).1 (c i).2 (u i).1 (u i).2 ⊆ containerBox L) :
    (∀ i j, i < n → j < n → i ≠ j → Disjoint
      (interior (Sq17.sq (c i + (s, s)).1 (c i + (s, s)).2 (u i).1 (u i).2))
      (interior (Sq17.sq (c j + (s, s)).1 (c j + (s, s)).2 (u j).1 (u j).2))) ∧
    (∀ i, i < n → Sq17.sq (c i + (s, s)).1 (c i + (s, s)).2 (u i).1 (u i).2 ⊆ containerBox (2443/500)) := by
  refine ⟨fun i j hi hj hij => ?_, fun i hi => ?_⟩
  · simp only [Prod.fst_add, Prod.snd_add, sq_translate]
    exact translate_disjoint _ _ _ (hd i j hi hj hij)
  · simp only [Prod.fst_add, Prod.snd_add, sq_translate]
    exact translate_container L s _ hs hU _ (hfit i hi)

end Sq19.Capture

#print axioms Sq19.Capture.hull_shift
#print axioms Sq19.Capture.translate_packing
#print axioms Sq19.Capture.container_sub_trace
