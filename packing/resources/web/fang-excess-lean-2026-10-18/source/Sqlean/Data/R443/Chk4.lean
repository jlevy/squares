import Sqlean.Data.R443

namespace UnitSquarePacking.Data.R443

open UnitSquarePacking.Cert

theorem chunk_4 : headsOK D 103 (L.drop (103 * 4)) = true := by decide +kernel

end UnitSquarePacking.Data.R443
