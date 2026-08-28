---
type: is
id: is-01m135sps16n6pvg7mwpapnkpx
title: "PR #43 review M1: failed quench leaves stale trace downloadable"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m135s5773qphv8g2qf3c999v
created_at: 2026-08-28T03:14:45.656Z
updated_at: 2026-08-28T03:25:17.645Z
closed_at: 2026-08-28T03:25:17.630Z
close_reason: "Fixed on codex/packing-svg-motion-lab-spike; see PR #43 disposition map."
resolution: null
duplicate_of: null
---
free-quench.js:653 assigns traceText before the response.ok check; the catch does not clear it or re-disable the download button. A failed run after a successful one downloads the MotionLabError record under a quench-trace-*.json name.
