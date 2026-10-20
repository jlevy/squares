---
type: is
id: is-01m0sqkxbpmad9hq69qcb2rw4d
title: Remove stochastic saturation as H-010 known-answer evidence
kind: bug
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/paused/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
created_at: 2026-08-24T11:13:45.845Z
updated_at: 2026-10-12T23:51:02.819Z
closed_at: 2026-10-06T08:23:39.578Z
close_reason: "Done: H-010 on main says a failure to find an escape 'is never a known-answer result or a certificate'. exp-016 decided on a strict algebraic escape with ten mutation controls."
resolution: null
duplicate_of: null
---
Testing/measurement-validity correction. Failure of a continuous search to find an escaping box is not a known-answer test and cannot certify Figure 14 or any implication. Acceptance: living plans and reviews distinguish positive falsifier witnesses from proof certificates; H-010 never accepts on search saturation; retained outcome requires independently replayed finite/exact or interval certificates; controls mutate each proof node and demonstrate refusal.

## Notes

2026-08-24: living docs now treat only positive escape witnesses as falsifier controls; a historical review has a dated erratum. Keep open until exp-016's proof-node certificate mutations land.
