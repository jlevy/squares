---
type: is
id: is-01m31gph947ach34rm8wnd19c6
title: check_session_clocks measures a terminal phase against wall-clock now
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m31gn7263sfhfbq8xfabkh3p
created_at: 2026-09-21T08:18:10.851Z
updated_at: 2026-09-21T08:18:10.851Z
---
Found during PR 204 re-review; pre-existing, PR 204 does not touch the file. The records gate printed 'phase 2 review-planning-oversight 1482 min against a budget of 60' for session-143. At check_session_clocks.py:168-170 the last phase has no successor so ended = now, ignoring the ended_at the record carries. session-143 is status: completed with ended_at 2026-09-20T07:24:00Z and phase 2 started_at 07:05:00Z, so true elapsed is 19 min, inside budget. The figure is non-deterministic and grows every run. Report-only so it cannot fail a gate, but it misleads any reader of the gate log. Fix: prefer session.ended_at for the terminal phase.
