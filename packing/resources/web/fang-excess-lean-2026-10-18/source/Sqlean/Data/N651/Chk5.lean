import Sqlean.Data.N651

namespace UnitSquarePacking.Data.N651

open UnitSquarePacking.Cert

theorem chunk_5 : headsOK D 82 (L.drop (82 * 5)) = true := by decide +kernel

end UnitSquarePacking.Data.N651
