import Sqlean.Data.M156

namespace UnitSquarePacking.Data.M156

open UnitSquarePacking.Cert

theorem unit_ok : L.all unitOK = true := by decide +kernel

theorem box_ok : L.all (boxOK D Wn Hn Sd) = true := by decide +kernel

theorem len_eq : L.length = 156 := by decide +kernel

theorem sorted_ok : sortedX L = true := by decide +kernel

theorem chunk_0 : headsOK D 156 (L.drop (156 * 0)) = true := by decide +kernel

end UnitSquarePacking.Data.M156
