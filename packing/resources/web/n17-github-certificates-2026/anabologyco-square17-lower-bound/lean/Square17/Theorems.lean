/-
Kernel-accepted facts about the certificate (via `native_decide`, which trusts
the Lean compiler in addition to the kernel — see README for the trust model).

These theorems cover, in Lean, the finite checks corresponding to:
  - scripts/check_certificate.py  (certificate arithmetic + D4 symmetry)
  - src/verify_endpoints.cpp      (theta = 0 and theta = pi/4 audits)
  - src/verify_coverage_segment.cpp at a 152-sample subset of the 148,937
    audited orientations (the full-set theorem is built separately; see
    FullTheorem.lean and the README status table).
-/

import Square17.Basic
import Square17.Checker
import Square17.AtomData
import Square17.SampleData

namespace Square17

theorem certificate_ok : certOK atoms = true := by native_decide

theorem theta0_coverage_ok : theta0OK atoms = true := by native_decide

theorem quarter_turn_coverage_ok : quarterOK atoms = true := by native_decide

theorem sample_subset_coverage_ok :
    checkSamples atoms sampleSubsetData sampleSubsetCount = true := by native_decide

end Square17
