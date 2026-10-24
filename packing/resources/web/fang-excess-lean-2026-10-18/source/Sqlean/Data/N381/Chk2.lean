import Sqlean.Data.N381

namespace UnitSquarePacking.Data.N381

open UnitSquarePacking.Cert

theorem chunk_2 : headsOK D 109 (L.drop (109 * 2)) = true := by decide +kernel

end UnitSquarePacking.Data.N381
