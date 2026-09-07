/-
The full-set coverage theorem: all 148,937 audited orientations pass the exact
coverage check in Lean. Kept out of the default build target because its
`native_decide` evaluation replays the entire coverage audit (an expensive,
single-threaded computation). Build with:

  lake build FullTheorem
-/

import Square17.Basic
import Square17.Checker
import Square17.AtomData
import Square17.SampleDataFull

namespace Square17

theorem sample_full_coverage_ok :
    checkSamples atoms sampleFullData sampleFullCount = true := by native_decide

end Square17
