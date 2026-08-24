---
type: is
id: is-01m0sk5n78rejhbbke8vckzbbe
title: Compare the unlabelled n=3 invariant to the unlabelled source
kind: bug
status: closed
priority: 1
version: 3
spec_path: explorations/packing/campaign/hypotheses/H-032-small-n-optimal-moduli.md
labels:
  - packing
  - focus-soundness
dependencies: []
parent_id: is-01m0shdh4arvmv3vyfyfpnqfpx
created_at: 2026-08-24T09:56:04.450Z
updated_at: 2026-08-24T10:13:55.891Z
closed_at: 2026-08-24T10:13:55.878Z
close_reason: "Fixed before the retained H-032 run in 257cb0d: labelled and unlabelled source comparisons are separate and fail closed; n=4 records no unreported f-vector; the orientation identity is derived independently on both sides. Exact generation/replay and focused controls pass."
resolution: null
duplicate_of: null
---
The first uncommitted small-n checker draft passed the labelled Betti vector [2,2] into the Alvarado-Garduño–González unlabelled n=3 comparison, so its source cross-check would always report false. Fix the interface to compare labelled and unlabelled invariants separately, retain source hashes, and require the live unlabelled comparison to pass before recording exp-014.
