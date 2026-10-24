import Sqlean.Data.N273

namespace UnitSquarePacking.Data.N273

open UnitSquarePacking.Cert

theorem chunk_1 : headsOK D 130 (L.drop (130 * 1)) = true := by decide +kernel

end UnitSquarePacking.Data.N273
