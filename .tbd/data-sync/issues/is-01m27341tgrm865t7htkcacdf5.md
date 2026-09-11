---
type: is
id: is-01m27341tgrm865t7htkcacdf5
title: Preserve display mode in the explainer math-face CI probe
kind: bug
status: in_progress
priority: 1
version: 2
labels: []
dependencies: []
parent_id: is-01m26sv4284ry42pyavjhmmzqs
created_at: 2026-09-11T02:00:38.479Z
updated_at: 2026-09-11T02:00:50.590Z
---
The Pages math-face checker re-typesets a representative displayed formula with KaTeX's inline default. Once the exact T-026 radical became the first prose fraction, the live display geometry could never match either metric-table probe and PR148's build failed in serif/sans and screen/print. Re-render with displayMode taken from the source formula, retain the four-mode live check and checker self-test, and close only after hosted Pages passes.

## Notes

Implemented locally: the re-render probe now carries displayMode from the live KaTeX node. The current explainer passes all four serif/sans and screen/print checks with zero findings; check_math_faces --self-test passes; 86 focused explainer/math-loading tests pass. Hosted confirmation remains pending the PR148 push.
