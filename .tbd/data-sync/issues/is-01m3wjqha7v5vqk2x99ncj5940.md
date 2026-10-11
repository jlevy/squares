---
type: is
id: is-01m3wjqha7v5vqk2x99ncj5940
title: "Atlas: a Grid | Triangle toggle, with the perfect squares n = k^2 down the triangle's right edge and an animated transition"
kind: feature
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T20:33:10.469Z
updated_at: 2026-10-02T00:02:32.715Z
closed_at: 2026-10-02T00:02:32.712Z
close_reason: "Merged as jlevy/squares#286 (merge 07f014386): Grid | Triangle toggle on the homepage atlas, perfect squares down the right edge, animated transition (100 tiles 383 ms, 0 missed frames; 324 tiles 420 ms); on narrow screens rows wrap left to right with the last partial line right-aligned."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'a toggle (same style as the Film | Workbench toggle on the visualize tab) that lets you choose between Grid | Triangle for the atlas visualization. The current visualization is a grid, but we should have a triangle where the numbers match the structure of the perfect packings of n = k^2 along the right edge. It should toggle between. There should be a nice, clean transition, too, where the blocks move into the right place in a fast and efficient way. This can be done separately as a new bead on a new branch.' Triangle: row k holds n = (k-1)^2 + 1 … k^2, that is 2k - 1 cells, right-aligned so 1, 4, 9, 16, … run down the right edge. Own branch and PR.

## Notes

Draft jlevy/squares#286 (claude/atlas-triangle). Owner's wrap rule, final (2026-10-01, three messages): a row wider than the container wraps in reading order, full lines first and the remainder last ('wrap front to back, go across left to right always'), and 'the very last line of a row that is partial but wrapped can still be right aligned', so every row ends with its perfect square at the right edge; 19 tiles at 8 per line is 8, 8, 3 with the 3 right-aligned. A row that fits is one right-aligned line. Agent (Fable) is applying this and the Show More / Show Less control (think-0dkn) on the same PR.
