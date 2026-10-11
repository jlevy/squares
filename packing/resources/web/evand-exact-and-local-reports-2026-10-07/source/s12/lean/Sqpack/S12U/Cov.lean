import Sqpack.S12U.Part0
import Sqpack.S12U.Part1
import Sqpack.S12U.Part2
import Sqpack.S12U.Part3

set_option linter.style.longLine false

/-!
# `S12U`: the box tree covers the D4 fundamental region (generated; do not edit)

29529 leaves (29528 splits, depth 34) in 124 chunks of at most 600 leaves, 4 files;
spatial scale `Q = 7920·4096`, angle `u = U/73400320`, root `u ∈ [0, 30408704/73400320]`.
-/

namespace SquarePacking.S12U

open BoxTree

/-- **The box tree covers the D4 fundamental region.** -/
theorem cov_root : Cov 7920 4096 30800 73400320 7 pts.toList 0 63078400 0 63078400 0 30408704 :=
  (Cov.splitX 31539200 (Cov.splitX 15769600 ok0 (Cov.splitY 31539200 ok1 (Cov.splitY 47308800 ok2 (Cov.splitX 23654400 (Cov.splitY 55193600 (Cov.splitU 15204352 (Cov.splitX 19712000 (Cov.splitU 7602176 ok3 ok4) ok5) ok6) ok7) ok8)))) (Cov.splitY 31539200 (Cov.splitY 15769600 ok9 (Cov.splitX 47308800 (Cov.splitX 39424000 ok10 ok11) (Cov.splitX 55193600 (Cov.splitY 23654400 ok12 ok13) ok14))) (Cov.splitX 47308800 (Cov.splitY 47308800 (Cov.splitX 39424000 ok15 (Cov.splitY 39424000 ok16 (Cov.splitX 43366400 ok17 (Cov.splitY 43366400 (Cov.splitU 15204352 ok18 (Cov.splitX 45337600 (Cov.splitY 41395200 ok19 (Cov.splitU 22806528 (Cov.splitU 19005440 (Cov.splitX 44352000 ok20 (Cov.splitY 42380800 (Cov.splitU 17104896 ok21 (Cov.splitX 44844800 ok22 (Cov.splitY 41888000 ok23 (Cov.splitU 18055168 (Cov.splitX 45091200 ok24 ok25) ok26)))) (Cov.splitU 17104896 (Cov.splitX 44844800 ok27 ok28) ok29))) ok30) ok31)) (Cov.splitY 41395200 ok32 (Cov.splitU 22806528 (Cov.splitU 19005440 (Cov.splitX 46323200 (Cov.splitY 42380800 (Cov.splitU 17104896 ok33 (Cov.splitX 45830400 (Cov.splitY 41888000 ok34 (Cov.splitU 18055168 (Cov.splitX 45584000 ok35 ok36) (Cov.splitX 45584000 ok37 ok38))) ok39)) (Cov.splitU 17104896 (Cov.splitX 45830400 (Cov.splitY 42873600 (Cov.splitY 42627200 ok40 ok41) ok42) (Cov.splitY 42873600 ok43 ok44)) (Cov.splitX 45830400 (Cov.splitY 42873600 (Cov.splitU 18055168 (Cov.splitX 45584000 ok45 ok46) ok47) ok48) (Cov.splitY 42873600 (Cov.splitU 18055168 (Cov.splitX 46076800 ok49 ok50) ok51) ok52)))) (Cov.splitY 42380800 ok53 (Cov.splitU 17104896 (Cov.splitY 42873600 ok54 (Cov.splitX 46816000 ok55 ok56)) (Cov.splitX 46816000 (Cov.splitY 42873600 (Cov.splitU 18055168 ok57 ok58) ok59) (Cov.splitY 42873600 ok60 (Cov.splitU 18055168 (Cov.splitX 47062400 ok61 ok62) ok63)))))) (Cov.splitX 46323200 (Cov.splitY 42380800 (Cov.splitU 20905984 (Cov.splitX 45830400 ok64 ok65) ok66) ok67) ok68)) ok69)))) (Cov.splitU 15204352 ok70 (Cov.splitX 45337600 ok71 ok72)))))) ok73) (Cov.splitY 47308800 (Cov.splitX 55193600 (Cov.splitY 39424000 ok74 (Cov.splitY 43366400 (Cov.splitU 15204352 ok75 (Cov.splitX 51251200 (Cov.splitU 22806528 (Cov.splitX 49280000 (Cov.splitY 41395200 ok76 (Cov.splitU 19005440 (Cov.splitX 48294400 (Cov.splitY 42380800 ok77 (Cov.splitU 17104896 ok78 (Cov.splitY 42873600 ok79 (Cov.splitX 47801600 (Cov.splitU 18055168 ok80 ok81) ok82)))) ok83) ok84)) ok85) ok86) ok87)) (Cov.splitX 51251200 (Cov.splitX 49280000 (Cov.splitU 15204352 ok88 (Cov.splitU 22806528 (Cov.splitY 45337600 (Cov.splitX 48294400 (Cov.splitY 44352000 (Cov.splitU 19005440 (Cov.splitU 17104896 (Cov.splitX 47801600 (Cov.splitY 43859200 (Cov.splitU 16154624 ok89 ok90) ok91) ok92) (Cov.splitY 43859200 (Cov.splitX 47801600 ok93 (Cov.splitU 18055168 (Cov.splitX 48048000 ok94 ok95) ok96)) ok97)) ok98) ok99) ok100) ok101) ok102)) (Cov.splitU 15204352 ok103 (Cov.splitU 22806528 (Cov.splitY 45337600 (Cov.splitU 19005440 (Cov.splitX 50265600 ok104 (Cov.splitY 44352000 ok105 (Cov.splitU 17104896 ok106 ok107))) ok108) ok109) ok110))) (Cov.splitU 15204352 ok111 (Cov.splitX 53222400 (Cov.splitY 45337600 ok112 (Cov.splitU 22806528 (Cov.splitY 46323200 (Cov.splitU 19005440 (Cov.splitX 52236800 (Cov.splitU 17104896 ok113 (Cov.splitY 45830400 (Cov.splitX 51744000 ok114 ok115) ok116)) ok117) ok118) ok119) ok120)) ok121))))) ok122) ok123))))

end SquarePacking.S12U
