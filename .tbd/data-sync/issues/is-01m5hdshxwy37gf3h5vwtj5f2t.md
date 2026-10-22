---
type: is
id: is-01m5hdshxwy37gf3h5vwtj5f2t
title: Audit earlier Couzo imports for 'the source's checkers were not run here' where the manifest names sqpack.verify (RF-1 of the T-226–T-228 review)
kind: task
status: in_progress
priority: 2
version: 2
delegate: coord-intake-1021b
labels:
  - records
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-22T09:06:38.651Z
updated_at: 2026-10-22T09:06:40.458Z
started_at: 2026-10-22T09:06:40.458Z
---
The stage 4 review of T-226-T-228 (scratchpad review-t226-t228/) found the three #670/#672/#675 source manifests name jlevy/squares@37e6757 packing/src/sqpack/verify.py as their first checker, byte-identical to main's and the decider of the maintained sqpack route; so the confirming replay is shared-components (as #678's is), and the record's statement that the source's checkers were not run here is wrong. The same sentence appears in earlier Couzo imports (not audited). Audit every Couzo-sourced evidence entry and claim record for the relation and the wording; fix with re-classification where the manifest names a checker this repository also runs.
blocked_on: none
