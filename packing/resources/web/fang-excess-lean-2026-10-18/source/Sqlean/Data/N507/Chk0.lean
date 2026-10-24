import Sqlean.Data.N507

namespace UnitSquarePacking.Data.N507

open UnitSquarePacking.Cert

theorem unit_ok : L.all unitOK = true := by decide +kernel

theorem box_ok : L.all (boxOK D Wn Hn Sd) = true := by decide +kernel

theorem len_eq : L.length = 507 := by decide +kernel

theorem sorted_ok : sortedX L = true := by decide +kernel

theorem chunk_0 : headsOK D 94 (L.drop (94 * 0)) = true := by decide +kernel

end UnitSquarePacking.Data.N507
