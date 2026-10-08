import ElevenSquare.Tasks.T07.GlobalComposition
import ElevenSquare.Tasks.T07.Ext.Case438Global

namespace ElevenSquare.Tasks.T07
open ElevenSquare.Pending
noncomputable section

/-- Remaining global geometry: every centered case438 packing of side at most T
has a representation in the focused local rectangle. It is supplied by the
extended traces of `ElevenSquare/Tasks/T07/Ext/` (generated node modules fetched and
checked against `integrations/wand125/release/MANIFEST_U5.sha256`): the closed-cell seed,
the archived phase 2, the capture tree, and the inclusion in the near packet. -/
theorem case438_near_certificate : Case438NearCertificate :=
  Ext.case438_near_certificate'

end
end ElevenSquare.Tasks.T07
