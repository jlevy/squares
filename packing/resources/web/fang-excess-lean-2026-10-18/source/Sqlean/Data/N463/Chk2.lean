import Sqlean.Data.N463

namespace UnitSquarePacking.Data.N463

open UnitSquarePacking.Cert

theorem chunk_2 : headsOK D 99 (L.drop (99 * 2)) = true := by decide +kernel

end UnitSquarePacking.Data.N463
