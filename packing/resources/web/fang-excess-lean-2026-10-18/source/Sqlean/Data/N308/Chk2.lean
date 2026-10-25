import Sqlean.Data.N308

namespace UnitSquarePacking.Data.N308

open UnitSquarePacking.Cert

theorem chunk_2 : headsOK D 122 (L.drop (122 * 2)) = true := by decide +kernel

end UnitSquarePacking.Data.N308
