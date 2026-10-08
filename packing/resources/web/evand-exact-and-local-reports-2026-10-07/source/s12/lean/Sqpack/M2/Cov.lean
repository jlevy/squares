import Sqpack.M2.Part0

set_option linter.style.longLine false

/-!
# `M2`: the mixed box tree covers the D4 fundamental region (generated; do not edit)

178 `Z` leaves, 664 `E` leaves, 600 clips, in 15 chunks, 1 files.
-/

namespace SquarePacking.M2

open BoxTree ZMTreeM

theorem cov_rootL : CovM 1000 4096 2000 4294967296 1000000 ptsL segsL 0 4096000 0 4096000 0 2147483648 :=
  (CovM.splitX 2048000 ok0 (CovM.splitX 2867200 (CovM.splitX 2457600 ok1 ok2) (CovM.splitX 3276800 (CovM.splitY 2048000 ok3 (CovM.splitY 2867200 ok4 (CovM.splitY 3276800 ok5 ok6))) (CovM.splitX 3686400 (CovM.splitY 2048000 ok7 (CovM.splitY 2867200 ok8 (CovM.splitY 3276800 ok9 ok10))) (CovM.splitY 2048000 ok11 (CovM.splitY 2867200 ok12 (CovM.splitY 3276800 ok13 ok14)))))))

theorem cov_root : CovM 1000 4096 2000 4294967296 1000000 pts.toList segs.toList 0 4096000 0 4096000 0 2147483648 := by
  rw [pts_toList, segs_toList]; exact cov_rootL

end SquarePacking.M2
