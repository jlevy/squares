---
type: is
id: is-01m2hez03w34kga7pt7f9vh912
title: "PR #160 review D84: capture, export and ascent write their outputs in place"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:40:00.123Z
updated_at: 2026-09-15T02:40:59.111Z
closed_at: 2026-09-15T02:40:59.110Z
close_reason: "Fixed on #160: capture video encoded to a sibling temporary and renamed, receipt last, SVG via write_svg_atomic and export receipt last (a093ec7a); ascent writes through write_text_atomic (e90187c8)."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

Outputs were written in place: ffmpeg `-y` to the final path then the receipt, the SVG written before its checks, and the ascent's three writes.

Source: #125 F35.

Files: `packages/workbench/tools/workbench_tools/capture_video.py:213`, `:338-339`; `export_animation_svg.py:25`; `ascent.py:234`, `:246`, `:263` (@bb3f7c99).
