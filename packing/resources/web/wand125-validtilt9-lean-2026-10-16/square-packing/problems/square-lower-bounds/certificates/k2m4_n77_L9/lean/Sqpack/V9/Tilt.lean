import Sqpack.ExTree
import Sqpack.ValidSplit9

/-!
# `ValidTilt` from a pose tree

`cover_of_tree` (`ExTree.lean`) needs the face `θ = 0` and the D4 symmetry to reach every square;
the tilted region `ValidTilt` (centres in `[0, m/2]²`, `0 < u`, `u² + 2u ≤ 1`) is exactly what a
`CovT` root over `[0, m/2]² × (0, Um/R]` (`Um/R ≥ 1/2`) states, once the measure of a square is
written as its mass (`hmass`, as in `cover_of_tree`).
-/

open MeasureTheory

namespace SquarePacking

namespace ZMTreeM

open BoxTree ZMTree

/-- **`ValidTilt` from a pose tree**: a `CovT` root over the D4 root box `[0, Mq/(2D)]² × (0, Um/R]`
with `Um/R ≥ 1/2` gives `ValidTilt (Mq/D)` for the mixed cover. -/
theorem validTilt_of_tree (D S Mq R Um W : ℕ) (pts : PTree) (segs : STree) (rects : List RectE)
    (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) (hUm : R ≤ 2 * Um)
    (hcov : CovT D S Mq R W pts.toList segs.toList rects 0 (Mq * S - Mq * S / 2) 0
      (Mq * S - Mq * S / 2) 0 Um)
    (hW : 0 < W) :
    ValidSplit.ValidTilt ((Mq : ℝ) / D) (mcoverP D W pts segs rects).measure := by
  classical
  set m : ℝ := (Mq : ℝ) / D with hm
  set M := mcoverP D W pts segs rects with hMdef
  have hWr : (0 : ℝ) < W := by exact_mod_cast hW
  have hDr : (0 : ℝ) < D := by exact_mod_cast hD
  have hSr : (0 : ℝ) < S := by exact_mod_cast hS
  have hRr : (0 : ℝ) < R := by exact_mod_cast hR
  have hnonneg : M.Nonneg :=
    ⟨fun _ _ => by simp only [hMdef, mcoverP]; positivity,
     fun _ _ => by simp only [hMdef, mcoverP]; positivity,
     fun _ _ => by simp only [hMdef, mcoverP]; positivity⟩
  -- the measure of a square is the mass
  have hmass : ∀ (Qs : Set (ℝ × ℝ)), MeasurableSet Qs →
      M.measure Qs = ENNReal.ofReal
        ((ptMass D pts.toList Qs + segMass D segs.toList Qs + rectMass D rects Qs) / W) := by
    intro Qs hQs
    rw [M.measure_apply hnonneg hQs]
    congr 1
    simp only [MixedCover.mass, hMdef, mcoverP, ptMass, segMass, rectMass, gw_areaFrac]
    rw [add_div, add_div, Finset.sum_div, Finset.sum_div, Finset.sum_div]
    congr 1
    · congr 1
      refine Finset.sum_congr rfl fun e _ => ?_
      ring
  intro c u hc1 hc2 hu hu' hsub
  rw [hmass _ (measurableSet_sq _ _ _), ← ENNReal.ofReal_one]
  apply ENNReal.ofReal_le_ofReal
  have hhalf : m / 2 ≤ (((Mq * S - Mq * S / 2 : ℕ) : ℝ)) / (D * S) := by
    have h2 : Mq * S ≤ 2 * (Mq * S - Mq * S / 2) := by omega
    have h2r : ((Mq * S : ℕ) : ℝ) ≤ 2 * ((Mq * S - Mq * S / 2 : ℕ) : ℝ) := by exact_mod_cast h2
    rw [hm, div_div, div_le_div_iff₀ (by positivity) (by positivity)]
    push_cast at h2r
    nlinarith
  have hu2 : u ≤ 1 / 2 := by nlinarith
  have hU1 : u ≤ (Um : ℝ) / R := by
    rw [le_div_iff₀ hRr]
    have : (R : ℝ) ≤ 2 * Um := by exact_mod_cast hUm
    nlinarith
  rw [le_div_iff₀ hWr, one_mul]
  exact hcov c u (by simpa using hc1.1) (le_trans hc1.2 hhalf) (by simpa using hc2.1)
    (le_trans hc2.2 hhalf) (by simpa using hu) hU1 hu' hsub

end ZMTreeM

end SquarePacking
