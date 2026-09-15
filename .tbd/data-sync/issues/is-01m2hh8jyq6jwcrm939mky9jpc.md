---
type: is
id: is-01m2hh8jyq6jwcrm939mky9jpc
title: "PR #160 review D62: the Pack panel's key handlers ignore Ctrl, Meta and Alt"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:11.478Z
updated_at: 2026-09-15T03:32:52.316Z
closed_at: 2026-09-15T03:32:52.315Z
close_reason: "Fixed on PR #160 in dd0858a3: packKeyCommand in view/accessibility.ts is the one Pack key map (modifier chords map to nothing, Shift stride, q/Q and e/E), Node-tested; check_pack_panel presses 16 chords with pose, run and focus unchanged."
resolution: null
duplicate_of: null
---
Canonical defect D62 from the 2026-09-14 stack triage (Medium). Sources: #160 R13; #160 R17 (key-map item).

The Pack panel's key handlers ignored Ctrl, Meta and Alt (Cmd+[, Ctrl+PageUp, Alt+Arrow handled as shortcuts: preventDefault, pause, move, Start -> "given"), and its own key map was untested (Shift+Q did nothing though the label says Q and E rotate).

Files: `packages/workbench/src/app/pack-panel.ts` (:452-515, :517-538, :467-485); a shared tested key map. Related: think-y9pw.
