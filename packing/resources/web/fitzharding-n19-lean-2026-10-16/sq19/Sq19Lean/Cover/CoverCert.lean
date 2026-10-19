import Sq17Lean.CellCoverGeometry
import Sq17Lean.PropagationHullTriangle

/-!
# Slab cover certificates for the 25 cells

The 17 project's certificate format (`Sq17.CellCover.SlabCertificate`) with the owner index
ranging over `Fin 25`. The geometric lemmas (`interval_chain_cover`, `trapezoid_mem`,
`triangleHullCheck_sound`) are the 17 project's own, imported unchanged.
-/
namespace Sq19.Cover
open Sq17.CellCover Sq17.Propagation

structure BandCertificate where
  owner : Fin 25
  lowerLeft : HullTriangleWitness
  lowerRight : HullTriangleWitness
  upperLeft : HullTriangleWitness
  upperRight : HullTriangleWitness

private def zeroTriangle : HullTriangleWitness := ⟨(0,0),(0,0),(0,0),1,0,0⟩
private def zeroBand : BandCertificate := ⟨0,zeroTriangle,zeroTriangle,zeroTriangle,zeroTriangle⟩

structure SlabCertificate where
  left : ℚ
  right : ℚ
  levels : List (ℚ × ℚ)
  bands : List BandCertificate

def SlabCertificate.count (s : SlabCertificate) : ℕ := s.levels.length - 1

def SlabCertificate.level (s : SlabCertificate) (j : ℕ) : ℚ × ℚ :=
  s.levels.getD j (0,0)

def SlabCertificate.band (s : SlabCertificate) (j : ℕ) : BandCertificate :=
  s.bands.getD j zeroBand

def BandCertificate.check (b : BandCertificate) (V : Fin 25 → List (ℚ × ℚ))
    (left right : ℚ) (lo hi : ℚ × ℚ) : Bool :=
  triangleHullCheck (V b.owner) (left,lo.1) b.lowerLeft &&
  triangleHullCheck (V b.owner) (right,lo.2) b.lowerRight &&
  triangleHullCheck (V b.owner) (left,hi.1) b.upperLeft &&
  triangleHullCheck (V b.owner) (right,hi.2) b.upperRight

def SlabCertificate.check (s : SlabCertificate) (V : Fin 25 → List (ℚ × ℚ))
    (bottom top : ℚ) : Bool :=
  decide (s.left < s.right ∧ 0 < s.count ∧ s.bands.length = s.count ∧
    s.level 0 = (bottom,bottom) ∧ s.level s.count = (top,top)) &&
  (List.range s.count).all (fun j =>
    (s.band j).check V s.left s.right (s.level j) (s.level (j+1)))

/-- The closed convex hull of an exact rational vertex list. -/
def polygon (V : Fin 25 → List (ℚ × ℚ)) (i : Fin 25) : Set (ℝ × ℝ) :=
  convexHull ℝ (realPoint '' {v | v ∈ V i})

theorem BandCertificate.check_sound (b : BandCertificate) (V : Fin 25 → List (ℚ × ℚ))
    (left right : ℚ) (lo hi : ℚ × ℚ)
    (hc : b.check V left right lo hi = true)
    (x y : ℝ) (hw : (left : ℝ) < right) (hx0 : (left : ℝ) ≤ x) (hx1 : x ≤ right)
    (hy0 : blend lo.1 lo.2 ((x-left)/(right-left)) ≤ y)
    (hy1 : y ≤ blend hi.1 hi.2 ((x-left)/(right-left))) :
    (x,y) ∈ polygon V b.owner := by
  simp only [BandCertificate.check, Bool.and_eq_true] at hc
  rcases hc with ⟨⟨⟨hll,hlr⟩,hhl⟩,hhr⟩
  exact trapezoid_mem (convex_convexHull ℝ _) left right lo.1 lo.2 hi.1 hi.2 x y
    hw hx0 hx1 (triangleHullCheck_sound _ _ _ hll)
    (triangleHullCheck_sound _ _ _ hlr) (triangleHullCheck_sound _ _ _ hhl)
    (triangleHullCheck_sound _ _ _ hhr) hy0 hy1

/-- Every point of the closed slab belongs to a certified owner hull. -/
theorem SlabCertificate.check_sound (s : SlabCertificate)
    (V : Fin 25 → List (ℚ × ℚ)) (bottom top : ℚ)
    (hc : s.check V bottom top = true) (x y : ℝ)
    (hx0 : (s.left : ℝ) ≤ x) (hx1 : x ≤ s.right)
    (hy0 : (bottom : ℝ) ≤ y) (hy1 : y ≤ top) :
    ∃ i : Fin 25, (x,y) ∈ polygon V i := by
  simp only [SlabCertificate.check, Bool.and_eq_true, decide_eq_true_eq,
    List.all_eq_true, List.mem_range] at hc
  rcases hc with ⟨⟨hw,hn,_hlen,hfirst,hlast⟩,hbands⟩
  let f : ℕ → ℝ := fun j => blend (s.level j).1 (s.level j).2
    ((x-s.left)/(s.right-s.left))
  have hf0 : f 0 = bottom := by dsimp [f]; rw [hfirst]; dsimp [blend]; ring
  have hfn : f s.count = top := by dsimp [f]; rw [hlast]; dsimp [blend]; ring
  obtain ⟨j,hj,hlo,hhi⟩ := interval_chain_cover s.count hn f y
    (by rwa [hf0]) (by rwa [hfn])
  refine ⟨(s.band j).owner, ?_⟩
  apply BandCertificate.check_sound _ _ _ _ _ _ (hbands j hj) x y _ hx0 hx1 hlo hhi
  exact_mod_cast hw

end Sq19.Cover
