import Sqlean.Data.N241

namespace UnitSquarePacking.Data.N241

open UnitSquarePacking.Cert

theorem chunk_1 : headsOK D 139 (L.drop (139 * 1)) = true := by decide +kernel

end UnitSquarePacking.Data.N241
