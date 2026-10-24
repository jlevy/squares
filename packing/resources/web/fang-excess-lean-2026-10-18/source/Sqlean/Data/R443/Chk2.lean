import Sqlean.Data.R443

namespace UnitSquarePacking.Data.R443

open UnitSquarePacking.Cert

theorem chunk_2 : headsOK D 103 (L.drop (103 * 2)) = true := by decide +kernel

end UnitSquarePacking.Data.R443
