import Sqlean.Data.R443

namespace UnitSquarePacking.Data.R443

open UnitSquarePacking.Cert

theorem unit_ok : L.all unitOK = true := by decide +kernel

theorem box_ok : L.all (boxOK D Wn Hn Sd) = true := by decide +kernel

theorem len_eq : L.length = 443 := by decide +kernel

theorem sorted_ok : sortedX L = true := by decide +kernel

theorem chunk_0 : headsOK D 103 (L.drop (103 * 0)) = true := by decide +kernel

end UnitSquarePacking.Data.R443
