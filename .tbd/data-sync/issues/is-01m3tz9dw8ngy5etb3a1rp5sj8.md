---
type: is
id: is-01m3tz9dw8ngy5etb3a1rp5sj8
title: "Tables: side margins at narrower widths"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T05:34:10.808Z
updated_at: 2026-10-01T07:14:54.079Z
closed_at: 2026-10-01T07:14:54.078Z
close_reason: "Done in 82e49d84c and 182909b92 on claude/overview-page-impl (jlevy/squares#255, pushed at 158820d9d); checked in the built site on 2026-10-01. Wide blocks are sized from the page, not the window: tables and filter bars sit 8 px inside the clip at 1024, 768 and 390; preview_site.clipped and tests/test_site_wide_blocks.py guard it. Open: the n = 11 optimality paper's own tables overflow at phone width (its own stylesheet)."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: the tables still need margins above and below (think-qntw) and also on the sides at narrower widths. Below the width where a table stops bleeding wide, every site table and its filter bar keep a side gutter from the window edge (and from the popover edge inside a popover) at tablet and phone widths; no table touches the edge of the viewport; measured at 1024, 768 and 390 px.
