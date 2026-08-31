---
type: is
id: is-01m0skpc6wnj82yk9am1rc06p6
title: Make the orientation identity check derive both polynomial sides
kind: bug
status: closed
priority: 1
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-032-small-n-optimal-moduli.md
labels:
  - packing
  - focus-soundness
dependencies: []
parent_id: is-01m0shdh4arvmv3vyfyfpnqfpx
created_at: 2026-08-24T10:05:12.272Z
updated_at: 2026-08-24T10:13:55.905Z
closed_at: 2026-08-24T10:13:55.905Z
close_reason: "Fixed before the retained H-032 run in 257cb0d: labelled and unlabelled source comparisons are separate and fail closed; n=4 records no unreported f-vector; the orientation identity is derived independently on both sides. Exact generation/replay and focused controls pass."
resolution: null
duplicate_of: null
---
The first H-032 checker draft assigned the same hard-coded coefficient tuple to both sides of 1/2 - w(1-w/2) = (w-1)^2/2, then called equality a checked result. Derive each polynomial independently from its expression, compare the coefficients, and retain the exact identity plus the quotient-angle endpoint convention before recording the experiment.
