---
type: is
id: is-01m0sy3hy65kzwwpyb7m3r66tx
title: H-041 record must distinguish runtime source hashes from attested extraction hashes
kind: bug
status: closed
priority: 2
version: 2
spec_path: explorations/packing/campaign/hypotheses/H-041-repaired-stromquist-point-set.md
labels: []
dependencies: []
parent_id: is-01m0srspsyjecv6bdatrx8r5bx
created_at: 2026-08-24T13:07:09.893Z
updated_at: 2026-08-24T13:18:00.695Z
closed_at: 2026-08-24T13:18:00.695Z
close_reason: H-041 source binding now distinguishes decisive runtime PDF/raw checks from non-runtime, non-decisive extraction attestations, and replay enforces that scope. Exact generate/replay passes; D-158 records the correction.
resolution: null
duplicate_of: null
---
Record-validity gap found before the scientific run. The first draft placed page-SVG and topology-path digests beside PDF/raw source hashes under a blanket runtime-hashes-verified statement even though the derived SVG/path artifacts are not retained or recomputed. Acceptance: label only PDF/raw hashes runtime-verified and decisive, label SVG/path digests non-runtime provenance attestations and non-decisive, record the correction, and replay the exact distinction.
