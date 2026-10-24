import Sqlean.Data.N651

namespace UnitSquarePacking.Data.N651

open UnitSquarePacking.Cert

theorem unit_ok : L.all unitOK = true := by decide +kernel

theorem box_ok : L.all (boxOK D Wn Hn Sd) = true := by decide +kernel

theorem len_eq : L.length = 651 := by decide +kernel

theorem sorted_ok : sortedX L = true := by decide +kernel

theorem chunk_0 : headsOK D 82 (L.drop (82 * 0)) = true := by decide +kernel

end UnitSquarePacking.Data.N651
