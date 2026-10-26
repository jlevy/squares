import Sqpack.ExTree
import Sqpack.LemmaELeafX

/-!
# `EXACT` leaves with the vertex test without combinations (`LemmaELeafX`)
-/

open MeasureTheory

namespace SquarePacking

namespace ZMTreeM

open BoxTree ZMTree

variable {D S Mq R W : ℕ} {pts : List (ℕ × ℕ × ℕ)} {segs : List SegE} {rects : List RectE}
  {x0 x1 y0 y1 u0 u1 : ℕ}

/-- **`EXACT`**, the sub-bins tested by the rows' minima (`LemmaELeaf.exOkX`). -/
theorem CovT.of_exactX (hD : 0 < D) (hS : 0 < S) (hR : 0 < R) {lf : LemmaELeaf.ExLeaf}
    (h : LemmaELeaf.exOkX D S R W x0 x1 y0 y1 u0 u1 segs rects lf = true) :
    CovT D S Mq R W pts segs rects x0 x1 y0 y1 u0 u1 :=
  CovT.of_covMPo (LemmaELeaf.CovMPo.of_exactX hD hS hR h)

end ZMTreeM

end SquarePacking
