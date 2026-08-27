---
type: is
id: is-01m10e2vm0xm642sgwwetyar63
title: Make SVG angle and full-adjacency classification precision-safe
kind: bug
status: closed
priority: 1
version: 5
labels: []
dependencies: []
created_at: 2026-08-27T01:41:50.832Z
updated_at: 2026-08-27T02:43:02.261Z
closed_at: 2026-08-27T02:43:02.245Z
close_reason: Implemented and validated precision-safe angle/contact classification; regenerated and replayed all 213 SVGs; exact pushed head cee9007 passed required CI.
resolution: null
duplicate_of: null
---

## Notes

Final implementation: default full-side endpoint tolerance 2e-6 (measured natural cutoff); wall contacts require axis agreement; square contacts require pairwise angle agreement; strict contacts merge tolerance-seeded angle classes. SVG metadata exposes orientation, class residual, contact partners, maximum contact residual, and the classification contract. n=68 confirms square-019 is genuinely 0.0463000909 degrees off-axis in the retained numerical witness and receives no false wall contact; n=105 regression proves strict neighbors share a class. All 213 SVGs regenerated/replayed; corpus audit covers 26,967 fills and 102,638 reciprocal contact records. Local strict reached 34/36 with all code/artifact/exact stages green; its only generated-doc contract was corrected and all 67 negative controls plus synopsis/ledger checks then passed.
