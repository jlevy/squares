import Sqpack.S12W.Part0
import Sqpack.S12W.Part1
import Sqpack.S12W.Part2
import Sqpack.S12W.Part3

set_option linter.style.longLine false

/-!
# `S12W`: the box tree covers the D4 fundamental region (generated; do not edit)

25127 leaves (25126 splits, depth 35) in 111 chunks of at most 600 leaves, 4 files;
spatial scale `Q = 1994·4096`, angle `u = U/73400320`, root `u ∈ [0, 30408704/73400320]`.
-/

namespace SquarePacking.S12W

open BoxTree

/-- **The box tree covers the D4 fundamental region.** -/
theorem cov_root : Cov 1994 4096 7840 73400320 10000000 pts.toList 0 16056320 0 16056320 0 30408704 :=
  (Cov.splitX 8028160 (Cov.splitX 4014080 ok0 (Cov.splitY 8028160 ok1 (Cov.splitY 12042240 (Cov.splitY 10035200 ok2 (Cov.splitX 6021120 (Cov.splitU 15204352 (Cov.splitY 11038720 ok3 (Cov.splitU 7602176 (Cov.splitX 5017600 (Cov.splitY 11540480 ok4 (Cov.splitU 3801088 ok5 ok6)) (Cov.splitY 11540480 ok7 (Cov.splitY 11791360 ok8 ok9))) (Cov.splitX 5017600 ok10 ok11))) ok12) ok13)) (Cov.splitX 6021120 (Cov.splitY 14049280 ok14 ok15) ok16)))) (Cov.splitY 8028160 (Cov.splitY 4014080 ok17 (Cov.splitX 12042240 (Cov.splitX 10035200 ok18 (Cov.splitY 6021120 (Cov.splitU 15204352 ok19 ok20) ok21)) (Cov.splitX 14049280 (Cov.splitY 6021120 (Cov.splitX 13045760 (Cov.splitU 15204352 (Cov.splitU 7602176 ok22 ok23) ok24) ok25) ok26) ok27))) (Cov.splitX 12042240 (Cov.splitY 12042240 (Cov.splitX 10035200 (Cov.splitY 10035200 ok28 (Cov.splitY 11038720 ok29 (Cov.splitX 9031680 ok30 (Cov.splitU 15204352 ok31 (Cov.splitX 9533440 ok32 (Cov.splitU 22806528 ok33 (Cov.splitY 11540480 ok34 (Cov.splitX 9784320 (Cov.splitY 11791360 ok35 (Cov.splitU 26607616 ok36 (Cov.splitX 9658880 ok37 ok38))) (Cov.splitY 11791360 (Cov.splitU 26607616 ok39 (Cov.splitX 9909760 ok40 ok41)) (Cov.splitX 9909760 (Cov.splitU 26607616 ok42 (Cov.splitU 28508160 ok43 ok44)) ok45)))))))))) (Cov.splitY 10035200 (Cov.splitX 11038720 ok46 (Cov.splitY 9031680 ok47 (Cov.splitU 15204352 ok48 (Cov.splitX 11540480 ok49 (Cov.splitU 22806528 ok50 (Cov.splitY 9533440 ok51 (Cov.splitX 11791360 (Cov.splitU 26607616 ok52 (Cov.splitY 9784320 ok53 (Cov.splitU 28508160 ok54 ok55))) (Cov.splitY 9784320 (Cov.splitU 26607616 ok56 (Cov.splitU 28508160 ok57 ok58)) ok59)))))))) (Cov.splitX 11038720 (Cov.splitY 11038720 ok60 (Cov.splitU 15204352 ok61 (Cov.splitX 10536960 (Cov.splitY 11540480 (Cov.splitU 22806528 ok62 (Cov.splitX 10286080 ok63 ok64)) ok65) ok66))) (Cov.splitU 15204352 (Cov.splitY 11038720 ok67 (Cov.splitY 11540480 ok68 ok69)) (Cov.splitY 11038720 (Cov.splitX 11540480 (Cov.splitY 10536960 ok70 ok71) ok72) ok73))))) (Cov.splitX 10035200 (Cov.splitY 14049280 (Cov.splitY 13045760 (Cov.splitU 15204352 ok74 (Cov.splitX 9031680 ok75 (Cov.splitY 12544000 (Cov.splitU 22806528 ok76 (Cov.splitX 9533440 ok77 (Cov.splitY 12293120 (Cov.splitX 9784320 ok78 ok79) ok80))) ok81))) ok82) ok83) (Cov.splitY 14049280 (Cov.splitX 11038720 ok84 ok85) ok86))) (Cov.splitY 12042240 (Cov.splitX 14049280 (Cov.splitY 10035200 (Cov.splitX 13045760 (Cov.splitX 12544000 (Cov.splitU 15204352 ok87 (Cov.splitY 9031680 ok88 (Cov.splitU 22806528 ok89 (Cov.splitY 9533440 ok90 (Cov.splitX 12293120 ok91 ok92))))) ok93) ok94) (Cov.splitX 13045760 (Cov.splitU 15204352 ok95 ok96) ok97)) ok98) (Cov.splitX 14049280 (Cov.splitY 14049280 (Cov.splitX 13045760 (Cov.splitU 15204352 (Cov.splitY 13045760 (Cov.splitU 7602176 (Cov.splitX 12544000 ok99 ok100) (Cov.splitY 12544000 ok101 (Cov.splitX 12544000 ok102 ok103))) ok104) ok105) ok106) ok107) (Cov.splitY 14049280 (Cov.splitY 13045760 ok108 ok109) ok110))))))

end SquarePacking.S12W
