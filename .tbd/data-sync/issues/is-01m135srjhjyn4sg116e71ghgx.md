---
type: is
id: is-01m135srjhjyn4sg116e71ghgx
title: "PR #43 review M6: loopback service validates no Host header and sets no timeout"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m135s5773qphv8g2qf3c999v
created_at: 2026-08-28T03:14:47.504Z
updated_at: 2026-08-28T03:14:47.504Z
---
serve_packing_motion_lab.py:139-284. DNS rebinding defeats the loopback bind and CORS preflight. No handler timeout, so a stalled connection holds a thread.
