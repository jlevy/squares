import Sqlean.Data.N421

namespace UnitSquarePacking.Data.N421

open UnitSquarePacking.Cert

theorem chunk_4 : headsOK D 104 (L.drop (104 * 4)) = true := by decide +kernel

end UnitSquarePacking.Data.N421
