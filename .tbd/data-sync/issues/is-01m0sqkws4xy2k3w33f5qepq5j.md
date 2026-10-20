---
type: is
id: is-01m0sqkws4xy2k3w33f5qepq5j
title: H-010 used unit squares where Stromquist requires open boxes of side greater than one
kind: bug
status: closed
priority: 1
version: 7
spec_path: docs/project/specs/paused/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
created_at: 2026-08-24T11:13:45.241Z
updated_at: 2026-10-12T23:51:02.194Z
closed_at: 2026-10-06T08:23:37.075Z
close_reason: "Done: H-010's claim and regime on main use open boxes of side strictly greater than one, and exp-016's control states 'strict open-box semantics'."
resolution: null
duplicate_of: null
---
Soundness correction for H-010. Stromquist Theorem 2 excludes packings by open boxes whose side is strictly greater than 1; the current hypothesis says unit square. Strictness is load-bearing at boundary contacts. Acceptance: hypothesis, experiment, checker, source-facing docs, and retained verdict all state the correct open-box regime; exact/interval checks justify the limiting reduction rather than silently replacing >1 by =1; a mutation control rejects the unit-square wording or semantics.

## Notes

2026-08-24: canonical H-010 and living plans now use open boxes of side >1 with strict boundary semantics. Keep open until exp-016's checker and mutation replay bind that regime.
