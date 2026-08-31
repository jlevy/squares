---
type: is
id: is-01m0yf2nnnz214akkqe8jzvgav
title: "W7: import full record geometry for n <= 100 into Witness/v1"
kind: feature
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-08-26T07:20:44.469Z
updated_at: 2026-08-26T10:18:41.631Z
closed_at: 2026-08-26T10:18:41.614Z
close_reason: All n=1..100 frontier cases now have retained provenance, normalized Witness/v1 geometry, declared exact or numerical receipts, offline deterministic rebuilds, frontier links, and house-rendered SVGs. The integrated fast gate and dedicated 100-case atlas check pass.
resolution: null
duplicate_of: null
---
Most frontier entries record side values without an imported geometry witness. Build a source adapter from the archived Kingbird catalogue SVGs (resources/web/kingbird-squares-in-squares*.md and per-case square-NNN.svg provenance) into Witness/v1 for every n <= 100 with public full geometry, recording per-case retrieval provenance and typed failures where geometry is absent or ambiguous. Numerical check each import at declared precision; never upgrade a decimal import to verified. This is the corpus H-044's chunk taxonomy and the wider n<=100 categorization both read. See campaign/explorations/X-003-stratified-chunk-enumeration.md and campaign/agendas/agenda-002-constructive-enumeration-groundwork.md BC-023.

## Notes

2026-08-26: auditing all n=1..100 source coverage and building a lossless source-to-Witness/v1-to-render pipeline; public catalogue SVGs, documented subpackings, canonical grids, and newer UnitSquare witnesses are treated as distinct provenance classes.
