import Sqlean.Data.N273

namespace UnitSquarePacking.Data.N273

open UnitSquarePacking.Cert

theorem chunk_2 : headsOK D 130 (L.drop (130 * 2)) = true := by decide +kernel

end UnitSquarePacking.Data.N273
