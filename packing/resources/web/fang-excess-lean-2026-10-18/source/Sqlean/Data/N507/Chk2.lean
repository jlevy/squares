import Sqlean.Data.N507

namespace UnitSquarePacking.Data.N507

open UnitSquarePacking.Cert

theorem chunk_2 : headsOK D 94 (L.drop (94 * 2)) = true := by decide +kernel

end UnitSquarePacking.Data.N507
