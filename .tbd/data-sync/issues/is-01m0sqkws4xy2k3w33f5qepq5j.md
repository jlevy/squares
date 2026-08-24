---
type: is
id: is-01m0sqkws4xy2k3w33f5qepq5j
title: H-010 used unit squares where Stromquist requires open boxes of side greater than one
kind: bug
status: open
priority: 1
version: 1
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4bxnqxb8dsv2rnqgyp0w8
created_at: 2026-08-24T11:13:45.241Z
updated_at: 2026-08-24T11:13:45.241Z
---
Soundness correction for H-010. Stromquist Theorem 2 excludes packings by open boxes whose side is strictly greater than 1; the current hypothesis says unit square. Strictness is load-bearing at boundary contacts. Acceptance: hypothesis, experiment, checker, source-facing docs, and retained verdict all state the correct open-box regime; exact/interval checks justify the limiting reduction rather than silently replacing >1 by =1; a mutation control rejects the unit-square wording or semantics.
