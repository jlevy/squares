---
type: is
id: is-01m4m3n0qvcnzmhyjnxbf1395n
title: Replace print recency stars with crimson case numbers
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-08-site-layout-and-navigation.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4ewpe4eqqjvrq6henxdzkh9
hold: null
hold_until: null
created_at: 2026-10-10T23:51:25.686Z
updated_at: 2026-10-11T01:13:23.060Z
started_at: 2026-10-10T23:51:35.238Z
closed_at: 2026-10-11T01:13:23.060Z
close_reason: Implemented and source-reviewed in PR462 at 53c8d37a2. Final ordinary Packing38100510883 and Pages38100510886 pass, including frontend and publication assembly. Shared Row outlines match width/alignment and paint gray behind black; web case/Atlas/table data retain ordinary ink. Later neutral-number and shared-spacing requests supersede earlier red-number/spacing intents. Final deferred/merge/deploy remain tracked separately by think-mvh7, think-21wu and think-xio5; controlled CI-performance follow-up remains think-ht59.
resolution: null
duplicate_of: null
---
Remove red recency star glyphs from canonical print atlas exports, retaining independent recent contribution accents and a crimson recent-result legend. Color recent case numerals red, preserve non-recency significance markers, regenerate canonical 100/324 SVG PNG PDF families with maintained producer, and visually inspect PDF legend and recent cases. Website recency marks are handled by the parallel web bead.

## Notes

Print implementation and canonical export refresh are staged for integration (no commit/push by this lane). Recent case numbers now use crimson; historical numbers stay gray; independent new bound and optimality accents remain. Removed unused print star constants/helpers. Shared legend marker=None is owned by web lane.

Evidence: regression first failed twice on gray recent numerals, then 11 focused SVG/PDF semantic checks passed (10.69 s) and 3 retained math/layout checks passed (4.39 s). Ruff lint/format and BasedPyright passed, 0 type findings. Maintained --update-composites regenerated 2 SVG, 4 PNG, 2 PDF; --check-composites passed. Identity v0.5.0-c8abd5, data 2026-10-10. 100 PDF 89,683 bytes; 324 PDF 533,984 bytes; complete 324 PNG 7497x5361, 2,847,887 bytes. Actual PDF crops inspected: red n=11, no recency star; recent-result key last after degree, only recent result red; swatches separated vertically.

Preserved evidence: /Users/levy/.codex/visualizations/2026/10/08/01a11dc7-6f9d-7060-be5c-4cff21839702/print-recency-kg7a/ (four PDF crops, producer report/update receipts, JUnit). Canonical PDF Row sizing unchanged. Earlier moving-snapshot full gate cannot cover this delta; final source-pinned integration checks and preview asset hash refresh remain the root lane's responsibility. Bead stays in progress until integration disposition.
