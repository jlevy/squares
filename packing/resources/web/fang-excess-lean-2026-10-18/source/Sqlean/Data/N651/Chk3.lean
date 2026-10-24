import Sqlean.Data.N651

namespace UnitSquarePacking.Data.N651

open UnitSquarePacking.Cert

theorem chunk_3 : headsOK D 82 (L.drop (82 * 3)) = true := by decide +kernel

end UnitSquarePacking.Data.N651
