---
type: is
id: is-01m135sqw9d072bwbahcq17wrp
title: "PR #43 review M4: UI claims the optimizer receives the container side"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m135s5773qphv8g2qf3c999v
created_at: 2026-08-28T03:14:46.792Z
updated_at: 2026-08-28T03:25:20.440Z
closed_at: 2026-08-28T03:25:20.437Z
close_reason: "Fixed on codex/packing-svg-motion-lab-spike; see PR #43 disposition map."
resolution: null
duplicate_of: null
---
render_general_motion_lab.py:90-91. quench_bracket has no side parameter; QuenchRequest.side reaches only the setup frame. Verified: side=1.6 and side=19.0 give bit-identical results.
