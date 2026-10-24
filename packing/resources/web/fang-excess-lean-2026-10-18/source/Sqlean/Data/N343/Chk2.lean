import Sqlean.Data.N343

namespace UnitSquarePacking.Data.N343

open UnitSquarePacking.Cert

theorem chunk_2 : headsOK D 115 (L.drop (115 * 2)) = true := by decide +kernel

end UnitSquarePacking.Data.N343
