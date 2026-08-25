---
type: is
id: is-01m0whda395zbm3fnc98r7c849
title: Retarget open-defect bead mutation to an open record
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-037-asymptotic-waste-exponent.md
labels:
  - packing
  - validity
  - testing
dependencies: []
parent_id: is-01m0wdnhn0xexxff41877prth2
created_at: 2026-08-25T13:23:01.352Z
updated_at: 2026-08-25T13:47:57.739Z
closed_at: 2026-08-25T13:47:57.738Z
close_reason: Retargeted the exact-once mutation from fixed D-021 to outstanding D-039; all 62 mutation controls now fire and the control again exercises its named invariant.
resolution: null
duplicate_of: null
---
The negative control removed D-021's bead after D-021 had become fixed, so it no longer exercised the invariant that outstanding/contained defects require beads. Retarget the exact mutation to outstanding D-039 and rerun the isolated control and suite.
