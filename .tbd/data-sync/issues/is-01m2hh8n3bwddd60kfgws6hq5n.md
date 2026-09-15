---
type: is
id: is-01m2hh8n3bwddd60kfgws6hq5n
title: "PR #160 review D65: live regions are rewritten on every animation frame"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:13.674Z
updated_at: 2026-09-15T03:32:53.179Z
closed_at: 2026-09-15T03:32:53.178Z
close_reason: "Fixed on PR #160 in dd0858a3: the per-frame status and stage facts are no longer live regions and are written only on change; #pack-announcement announces state changes; check_pack_panel allows at most 3 live-region mutations in a second of Run (124 per region before)."
resolution: null
duplicate_of: null
---
Canonical defect D65 from the 2026-09-14 stack triage (Medium). Source: #160 R16.

Live regions were rewritten on every animation frame: `redraw()` wrote `#pack-status` and `#pack-stage-facts`, both aria-live polite, on every tick (128 mutations of `#pack-stage-facts` in one second of Run), against the plan's "without announcing every animation frame".

Files: `packages/workbench/src/app/pack-panel.ts` (:171, :177); `packages/workbench/assets/template.html` (:65, :299). Related: think-y9pw.
