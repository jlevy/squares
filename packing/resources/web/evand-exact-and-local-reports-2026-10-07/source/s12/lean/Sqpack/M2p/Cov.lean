import Sqpack.M2p.Part0

set_option linter.style.longLine false

/-!
# `M2p`: the mixed box tree covers the D4 fundamental region (generated; do not edit)

282 `Z` leaves, 663 `E` leaves, 607 clips, in 20 chunks, 1 files.
-/

namespace SquarePacking.M2p

open BoxTree ZMTreeM

theorem cov_rootL : CovM 1000 4096 2000 4294967296 1000000 ptsL segsL 0 4096000 0 4096000 0 2147483648 :=
  (CovM.splitX 2048000 ok0 (CovM.splitX 2867200 ok1 (CovM.splitX 3276800 (CovM.splitY 2048000 ok2 (CovM.splitY 2867200 ok3 (CovM.splitY 3276800 ok4 ok5))) (CovM.splitX 3686400 (CovM.splitY 2048000 ok6 (CovM.splitY 2867200 ok7 (CovM.splitY 3276800 ok8 ok9))) (CovM.splitY 2048000 ok10 (CovM.splitY 2867200 (CovM.splitY 2457600 (CovM.splitU 1073741824 (CovM.splitU 536870912 (CovM.splitU 268435456 ok11 ok12) ok13) ok14) (CovM.splitU 1073741824 (CovM.splitU 536870912 ok15 ok16) ok17)) (CovM.splitY 3276800 ok18 ok19)))))))

theorem cov_root : CovM 1000 4096 2000 4294967296 1000000 pts.toList segs.toList 0 4096000 0 4096000 0 2147483648 := by
  rw [pts_toList, segs_toList]; exact cov_rootL

end SquarePacking.M2p
