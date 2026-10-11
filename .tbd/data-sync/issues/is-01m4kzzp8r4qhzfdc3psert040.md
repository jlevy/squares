---
type: is
id: is-01m4kzzp8r4qhzfdc3psert040
title: Render a separate 324-case Row comparison with bottom-left packing alignment
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T22:47:21.111Z
updated_at: 2026-10-11T01:13:23.225Z
started_at: 2026-10-10T22:48:16.662Z
closed_at: 2026-10-11T01:13:23.225Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Produce a separate review SVG using the retained Atlas renderer: Row sizing, packing lower/left edges sharing a baseline, gray row reference frame extending above/right. Preserve every packing geometry/color and approved published SVG/PDF exports. Add only a minimal reusable supported renderer option if needed; inspect candidate alongside current 324 graphic, and provide structural/visual evidence. User has not authorized replacing published PDF outputs for this comparison.

## Notes

Implemented the supported --row-comparison-svg PATH mode in devtools/build_known_best_atlas.py. It reads retained cases, writes only a separate SVG, rejects canonical publication destinations, and leaves the default renderer path unchanged. Mathematical row k uses its k-by-k reference; packing geometry scales isotropically at the bottom-left, with a thicker gray reference frame above/right for smaller packings. Original polygon order/colors and all card labels remain intact. The comparison has its own accurate accessible title/description; default accessible prose is unchanged.

Final artifact: /Users/levy/.codex/visualizations/2026/10/08/01a11dc7-6f9d-7060-be5c-4cff21839702/atlas-324-row-comparison.svg (8,076,288 bytes; 324 ordered cards; 52,650 square polygons). Actual bounded rendered crops atlas-324-fixed-detail.png and atlas-324-row-comparison-detail.png were inspected: n5 shares the lower/left baseline and its gray frame extends above/right; n6-9 retain the same Row reference size.

Verification: the new Row geometry test covers n5-9 and n11, original polygon colors/points under the isotropic transform, equal bottom/left anchors, thicker reference frame and byte-identical card labels. That node plus the existing default grid-transition/card-scale control passed 2 tests in 6.73s. Scoped BasedPyright has 0 errors/warnings/notes; Ruff check/format and git diff --check passed. The maintained default renderer API rendered all 324 retained cases using the approved SVG identity and produced exactly the approved 8,020,096 bytes. Published atlas SVG/PNG/PDF diff is empty. Astra approved the Row geometry source; the final change only corrects Row-specific accessible wording.

Small unique generation, test, type, complete-byte and visual receipts are preserved with byte-verified copies under the durable process-review/24se-row-comparison directory. Parent/header owns the separate local preview copy; canonical homepage PDF cards still point at approved publications. No PDF/PNG export regeneration, source commit or replacement publication was performed. Keep this bead open for owner review and the final branch checkpoint.
