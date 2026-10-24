import Sqlean.Data.M182

namespace UnitSquarePacking.Data.M182

open UnitSquarePacking.Cert

theorem chunk_1 : headsOK D 163 (L.drop (163 * 1)) = true := by decide +kernel

end UnitSquarePacking.Data.M182
