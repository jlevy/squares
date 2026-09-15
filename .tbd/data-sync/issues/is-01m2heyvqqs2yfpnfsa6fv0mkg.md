---
type: is
id: is-01m2heyvqqs2yfpnfsa6fv0mkg
title: "PR #160 review D51: the SVG export does not say its transitions are not packings"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:55.639Z
updated_at: 2026-09-15T02:40:55.363Z
closed_at: 2026-09-15T02:40:55.362Z
close_reason: "Fixed on #160 at a093ec7a: every multi-frame export says transitions are illustrative, not packings, in <desc> and a new receipt with transitions_are_packings false; tests read both back from the written files, and assert no drawn caption."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

The SVG export's honesty channel was invisible: the trajectory view drew only the final frame's caption, with no persistent statement that transitions are illustrative. Coordinator decision: no caption line; the statement goes in `<desc>` and an export receipt, with a test on the rendered file.

Source: #125 F15 (record-frame label item already fixed at 15d97a59).

Files: `packages/workbench/tools/workbench_tools/animation_render.py:216-254`, `export_animation_svg.py`.
