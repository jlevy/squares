import Sqlean.Data.N553

namespace UnitSquarePacking.Data.N553

open UnitSquarePacking.Cert

theorem chunk_6 : headsOK D 90 (L.drop (90 * 6)) = true := by decide +kernel

end UnitSquarePacking.Data.N553
