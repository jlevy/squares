---
type: is
id: is-01m1gbwfjbzmx7p7v0dajfgmgn
title: Wave-efficiency renderer refuses Claude-to-Codex bridged agenda lanes
kind: bug
status: open
priority: 3
version: 3
spec_path: packing/campaign/agendas/agenda-015-ten-hour-earned-routes-and-guard-repairs.md
labels:
  - agenda-015
  - efficiency
dependencies: []
parent_id: is-01m1hqrbe9zjyvnnnfqharq8xr
created_at: 2026-09-02T06:11:15.658Z
updated_at: 2026-09-03T05:28:06.062Z
---
BC-143 must compare sessions 079-081 with devtools.render_wave_efficiency, but the renderer accepts only CodexTaskTreeDelta receipts. These lanes retain ClaudeEfficiencyRollup receipts, so the exact registered command refuses before producing a W5 table. Preserve the typed no-change receipt in this agenda; add a prospectively tested cross-harness adapter/common measurement surface under OR-10 before a later mixed-harness wave.
