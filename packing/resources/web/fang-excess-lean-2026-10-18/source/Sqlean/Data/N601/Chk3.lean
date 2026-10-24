import Sqlean.Data.N601

namespace UnitSquarePacking.Data.N601

open UnitSquarePacking.Cert

theorem chunk_3 : headsOK D 86 (L.drop (86 * 3)) = true := by decide +kernel

end UnitSquarePacking.Data.N601
