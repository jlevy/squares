---
type: is
id: is-01m135sqhcq4xy4dtn5nk0e1gv
title: "PR #43 review M3: TimelineEvent.lp_solves changes meaning on the stop event"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m135s5773qphv8g2qf3c999v
created_at: 2026-08-28T03:14:46.443Z
updated_at: 2026-08-28T03:25:19.624Z
closed_at: 2026-08-28T03:25:19.622Z
close_reason: "Fixed on codex/packing-svg-motion-lab-spike; see PR #43 disposition map."
resolution: null
duplicate_of: null
---
quench.py:1164 emits the cumulative total on STOP while every other event carries a per-call count; free-quench.js:474 labels both identically. Per-event values sum to 213 against a true 71 on the retained fixture.
