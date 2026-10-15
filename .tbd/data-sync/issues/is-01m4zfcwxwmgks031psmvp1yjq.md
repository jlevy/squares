---
type: is
id: is-01m4zfcwxwmgks031psmvp1yjq
title: Preserve results-table geometry while tightening significance spacing
kind: bug
status: in_progress
priority: 1
version: 2
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zaazfxmv8px64xvdvdqnc7
hold: null
hold_until: null
created_at: 2026-10-15T09:48:21.305Z
updated_at: 2026-10-15T09:49:14.512Z
started_at: 2026-10-15T09:49:14.511Z
---
Final reachable d022 run completed10973pass49skip1xfail but12result-column layout guards fail: changing global significance width5.5em→5em narrowed tablefloor by8.4px (1116.1vs1124.5). User requested internal gap reduction, not boxwidth shrink. Restore original fixed5.5em while retaining justify-content:center and0.08emgap; update designnotes ifneeded. Run complete results-column native module and News shared-meter regressions, preserve fullfailed receipt. Avoid changing expectedtablegeometry or loosening guards.
