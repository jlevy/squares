---
type: is
id: is-01m4zfcwxwmgks031psmvp1yjq
title: Preserve results-table geometry while tightening significance spacing
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4zaazfxmv8px64xvdvdqnc7
hold: null
hold_until: null
created_at: 2026-10-15T09:48:21.305Z
updated_at: 2026-10-15T10:14:16.054Z
started_at: 2026-10-15T09:49:14.511Z
closed_at: 2026-10-15T10:14:16.053Z
close_reason: "Fixed by e5e51b43: restored the shared meter's 5.5em outer width while keeping the tighter 0.08em score gap. All 78 native result-column tests passed in 67.93s; desktop/mobile measurements preserve the calibrated width and five bars."
resolution: null
duplicate_of: null
---
Final reachable d022 run completed10973pass49skip1xfail but12result-column layout guards fail: changing global significance width5.5em→5em narrowed tablefloor by8.4px (1116.1vs1124.5). User requested internal gap reduction, not boxwidth shrink. Restore original fixed5.5em while retaining justify-content:center and0.08emgap; update designnotes ifneeded. Run complete results-column native module and News shared-meter regressions, preserve fullfailed receipt. Avoid changing expectedtablegeometry or loosening guards.
