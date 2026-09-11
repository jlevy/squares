---
type: is
id: is-01m27341tgrm865t7htkcacdf5
title: Preserve display mode in the explainer math-face CI probe
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m26sv4284ry42pyavjhmmzqs
created_at: 2026-09-11T02:00:38.479Z
updated_at: 2026-09-11T08:05:53.474Z
closed_at: 2026-09-11T08:05:53.473Z
close_reason: Preserved KaTeX displayMode in the explainer math-face probe and retained all serif/sans screen/print comparisons plus the checker self-test. Local checks passed, and the pushed PR148 Pages build and Firefox/WebKit font-loading jobs all pass at 6e3f6bd9.
resolution: null
duplicate_of: null
---
The Pages math-face checker re-typesets a representative displayed formula with KaTeX's inline default. Once the exact T-026 radical became the first prose fraction, the live display geometry could never match either metric-table probe and PR148's build failed in serif/sans and screen/print. Re-render with displayMode taken from the source formula, retain the four-mode live check and checker self-test, and close only after hosted Pages passes.

## Notes

Implemented locally: the re-render probe now carries displayMode from the live KaTeX node. The current explainer passes all four serif/sans and screen/print checks with zero findings; check_math_faces --self-test passes; 86 focused explainer/math-loading tests pass. Hosted confirmation remains pending the PR148 push.
