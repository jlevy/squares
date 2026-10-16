import Sq19Lean.Cover.CoverData

/-!
# The 25 cells cover the centre box

`cell i` is the closed convex hull of the exact vertex list `vertices i`
(`s19/data/cells25.txt`, same order). Every point of `[1/2, 2193/500]^2` lies in some cell.
Proof: 9 closed vertical slabs and 45 trapezoid bands, each corner of each band an explicit
convex combination of three owner vertices, all rechecked by kernel reduction.
-/
namespace Sq19.Cover
open Sq17.CellCover Sq17.Propagation

/-- The 25 closed cells. -/
def cell (i : Fin 25) : Set (ℝ × ℝ) := polygon vertices i

set_option maxRecDepth 8192 in
set_option maxHeartbeats 4000000 in
theorem all_slab_checks : ∀ i : Fin 9,
    (slabs i).check vertices (1/2) (2193/500) = true ∧
      (slabs i).left = xBreaks i.val ∧ (slabs i).right = xBreaks (i.val+1) := by
  decide +kernel

/-- Every point of the closed centre box `[1/2, 2193/500]^2` lies in at least one cell. -/
theorem centre_box_covered (x y : ℝ)
    (hx0 : 1/2 ≤ x) (hx1 : x ≤ 2193/500)
    (hy0 : 1/2 ≤ y) (hy1 : y ≤ 2193/500) :
    ∃ i : Fin 25, (x,y) ∈ cell i := by
  obtain ⟨j,hj,hlo,hhi⟩ := interval_chain_cover 9 (by decide)
    (fun k => (xBreaks k : ℝ)) x
    (by simpa [xBreaks] using hx0) (by simpa [xBreaks] using hx1)
  let i : Fin 9 := ⟨j,hj⟩
  have hc := all_slab_checks i
  apply (slabs i).check_sound vertices (1/2) (2193/500) hc.1 x y
  · simpa only [hc.2.1] using hlo
  · simpa only [hc.2.2] using hhi
  · norm_num only [Rat.cast_div, Rat.cast_ofNat] at *
    exact hy0
  · norm_num only [Rat.cast_div, Rat.cast_ofNat] at *
    exact hy1

end Sq19.Cover

#print axioms Sq19.Cover.all_slab_checks
#print axioms Sq19.Cover.centre_box_covered
