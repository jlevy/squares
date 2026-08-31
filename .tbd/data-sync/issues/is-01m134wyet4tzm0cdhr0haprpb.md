---
type: is
id: is-01m134wyet4tzm0cdhr0haprpb
title: "PR #50 review R8: Medium: phase-4 margin rule is not a decidable criterion"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m134wbw78hcnh0fsgqtej4rk
created_at: 2026-08-28T02:59:03.257Z
updated_at: 2026-08-28T03:20:04.697Z
closed_at: 2026-08-28T03:20:04.685Z
close_reason: "Addressed in a236598; disposition map posted to PR #50"
resolution: null
duplicate_of: null
---
impl spec:245-247. 'far below' unquantified; k ambiguous between search bound and actual coefficient size (reproduction shows actual governs); 'digits available' undefined against phase 3's residual bound; and the cheap decisive test, stability under precision, is absent. Not a soundness hole because back-substitution is the guarantee.
