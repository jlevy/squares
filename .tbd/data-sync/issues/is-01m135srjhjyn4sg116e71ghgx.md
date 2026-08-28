---
type: is
id: is-01m135srjhjyn4sg116e71ghgx
title: "PR #43 review M6: loopback service validates no Host header and sets no timeout"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m135s5773qphv8g2qf3c999v
created_at: 2026-08-28T03:14:47.504Z
updated_at: 2026-08-28T03:25:22.265Z
closed_at: 2026-08-28T03:25:22.263Z
close_reason: "Fixed on codex/packing-svg-motion-lab-spike; see PR #43 disposition map."
resolution: null
duplicate_of: null
---
serve_packing_motion_lab.py:139-284. DNS rebinding defeats the loopback bind and CORS preflight. No handler timeout, so a stalled connection holds a thread.
