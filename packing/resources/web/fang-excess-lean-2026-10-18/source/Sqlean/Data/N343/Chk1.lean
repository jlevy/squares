import Sqlean.Data.N343

namespace UnitSquarePacking.Data.N343

open UnitSquarePacking.Cert

theorem chunk_1 : headsOK D 115 (L.drop (115 * 1)) = true := by decide +kernel

end UnitSquarePacking.Data.N343
