---
type: is
id: is-01m135sq64g9q51v522atmvtjc
title: "PR #43 review M2: replay does not verify bytes despite the documented claim"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m135s5773qphv8g2qf3c999v
created_at: 2026-08-28T03:14:46.083Z
updated_at: 2026-08-28T03:25:18.620Z
closed_at: 2026-08-28T03:25:18.619Z
close_reason: "Fixed on codex/packing-svg-motion-lab-spike; see PR #43 disposition map."
resolution: null
duplicate_of: null
---
serve_packing_motion_lab.py:100-109 compares re-serialized parsed JSON, so a reformatted trace passes. The runbook says 'byte for byte' and the docstring says 'byte-level trace drift'.
