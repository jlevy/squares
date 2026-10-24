import Sqlean.Data.N651

namespace UnitSquarePacking.Data.N651

open UnitSquarePacking.Cert

theorem chunk_6 : headsOK D 82 (L.drop (82 * 6)) = true := by decide +kernel

end UnitSquarePacking.Data.N651
