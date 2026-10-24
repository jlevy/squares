import Sqlean.Data.M132

namespace UnitSquarePacking.Data.M132

open UnitSquarePacking.Cert

theorem unit_ok : L.all unitOK = true := by decide +kernel

theorem box_ok : L.all (boxOK D Wn Hn Sd) = true := by decide +kernel

theorem len_eq : L.length = 132 := by decide +kernel

theorem sorted_ok : sortedX L = true := by decide +kernel

theorem chunk_0 : headsOK D 132 (L.drop (132 * 0)) = true := by decide +kernel

end UnitSquarePacking.Data.M132
