import Sqlean.Data.N421

namespace UnitSquarePacking.Data.N421

open UnitSquarePacking.Cert

theorem chunk_3 : headsOK D 104 (L.drop (104 * 3)) = true := by decide +kernel

end UnitSquarePacking.Data.N421
