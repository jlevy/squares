---
type: is
id: is-01m4magbbw3y4tzva4jykt8xje
title: Measure forwarder arrival waits in the published-site audit
kind: task
status: in_progress
priority: 3
version: 2
spec_path: docs/project/specs/active/plan-2026-10-10-website-development-loop.md
delegate: codex@spud10
labels:
  - ci
dependencies: []
parent_id: is-01m4ke1dkg5m43rszjm49ar77r
hold: null
hold_until: null
created_at: 2026-10-11T01:51:12.763Z
updated_at: 2026-10-11T02:02:43.852Z
started_at: 2026-10-11T02:02:43.852Z
---
Independent Astra inspection found forwarder_arrivals documents arrival commitment but uses wait_until=load. After phase timing is available, measure this discrepancy and use commitment waiting if appropriate. Preserve exact destination, query and fragment assertions; a deliberately slow destination should not delay arrival verification. This is a secondary hypothesis, not the cause of the twelve GitHub503 failures. Do not claim a speedup before measuring.
