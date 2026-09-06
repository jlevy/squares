---
type: is
id: is-01m1t5y2x1hxpa8n6ja66davj8
title: Define the 24-hour plan as active agent effort
kind: task
status: closed
priority: 1
version: 5
labels:
  - planning
  - process
dependencies:
  - type: blocks
    target: is-01m1t5yjssbd51cnnw2zwkqah6
parent_id: is-01m1t5xm3xv343zpxen49r7m5g
created_at: 2026-09-06T01:39:41.088Z
updated_at: 2026-09-06T02:46:37.959Z
closed_at: 2026-09-06T02:46:37.958Z
close_reason: Agenda-024, both child agendas, X-016 and SYNOPSIS define 24 hours as active portfolio time, keep agent/wall/CPU clocks separate, and pause the portfolio clock for operational disruption and landing mechanics.
resolution: null
duplicate_of: null
---
Revise the owning strategy plan, agendas, and any reader-facing summary that currently implies an uninterrupted wall-clock day. Define the roughly 24-hour horizon as cumulative active agent work; exclude interruptions, quota pauses, host outages, handoff delay, and other operational downtime; retain per-command scientific timeboxes and honest session elapsed-time records where those guard a live computation.

## Notes

Defined roughly 24 hours as active portfolio schedule time in agenda-024 and X-016; propagated active-minute semantics to every agent-work budget in agenda-025/026. Operational pauses do not consume the horizon or advance a shared gate. Parallel labor is tracked separately as agent_minutes; actual wall/CPU cost and frozen scientific timeboxes remain independently reported and preregistered.
