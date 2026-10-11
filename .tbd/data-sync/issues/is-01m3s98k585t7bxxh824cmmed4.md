---
type: is
id: is-01m3s98k585t7bxxh824cmmed4
title: Repair solved n11 consumers before final PR publication
kind: bug
status: closed
priority: 1
version: 6
labels: []
dependencies: []
parent_id: is-01m3qcan8g6wnnpkvaemzt7rfm
created_at: 2026-09-30T13:50:00.359Z
updated_at: 2026-09-30T15:23:38.507Z
closed_at: 2026-09-30T15:23:38.507Z
close_reason: Published b6c97667b and verified in hosted runs36735084578/36735084788. Solved n11 consumer and SVG/PDF/page checks pass. The live wall audit now reports its conservative265s endpoint and correctly propagates the separate suite-B budget failure; no timestamp observation defect remains. Remaining integration work is third-shard capacity think-o18s under think-fjdd and final certification think-niqx.
resolution: null
duplicate_of: null
---
Incremental push at41af4f3c1 found11 test failures and30 setup errors: algebraic lower-bound rendering, DS7 restricted parser, solved-case assertions, and atlas data pin. Parallel Sol renderer/atlas and Astra-max comparison lanes. Keep proof receipts frozen; focused tests then incremental gate and hosted CI.

## Notes

Published6c8542175 passes local delta52checks/1639tests. Hosted Pages exposed solved-mode SVG rendering bug: omitted VERIFIED_MARK leaves raw-HTML break and SVG lines render as pre/code; print overflow1446px scalesPDF to13 instead of22pages. Sol owns minimal markup fix and rendered structural regression plus focused print/PDF verification. Do not relax geometry/pagecountguards. Mathematical receipts unchanged.
