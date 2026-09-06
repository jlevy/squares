---
type: is
id: is-01m1sx0q5s610zc3b6r61azdx0
title: Serialize fractional colgen deadline summaries as strict JSON
kind: bug
status: closed
priority: 1
version: 4
labels:
  - research
dependencies: []
parent_id: is-01m1sp7k7txpwp2y4pbhen30jv
created_at: 2026-09-05T23:03:50.194Z
updated_at: 2026-09-05T23:48:08.159Z
closed_at: 2026-09-05T23:48:08.159Z
close_reason: "Launch packets independently spiked and reconciled; strict fractional deadline JSON implemented and covered; local push tier and PR #89 CI green at d1f13695."
resolution: null
duplicate_of: null
---
The devtools.run_fractional_colgen command currently serializes bare Infinity and NaN when a deadline expires before the first LP round; strict JSON consumers must reject those bytes and jq silently coerces them. Reproduce with the zero-budget BC-233 preflight, add a failing test first, emit an explicit JSON-safe unavailable value while preserving the time-limited stop reason, set the serializer to reject all remaining non-finite floats, and verify normal summaries are unchanged. This must be resolved or explicitly guard-refused before a deadline-stopped BC-233 arm can satisfy its exit.
