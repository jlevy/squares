---
type: is
id: is-01m134xbayfa25ytw8f1y13ts3
title: "PR #50 review R9: Low: the recorded PSLQ probe is not reproducible as recorded"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - packing
dependencies: []
parent_id: is-01m134wbw78hcnh0fsgqtej4rk
created_at: 2026-08-28T02:59:16.436Z
updated_at: 2026-08-28T03:20:05.322Z
closed_at: 2026-08-28T03:20:05.308Z
close_reason: "Addressed in a236598; disposition map posted to PR #50"
resolution: null
duplicate_of: null
---
X-004:121-137 and the same numbers in both specs, agenda BC-047, the ledger copy and the PR body. Precision, maxcoeff, maxsteps, tolerance and the relation itself are unrecorded. The reviewer reproduced the shape but got 1.19e-85 at dps 100 and 4.54e-84 at dps 98, not the recorded 1.26e-90. Also the serialized side carries exactly 100 significant digits; the '98' is never derived.
