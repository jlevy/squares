---
type: is
id: is-01m4h9s465x7mphy1xxkmdyqc9
title: Refresh generated credit inventories and fix final validation consistency failures
kind: bug
status: in_progress
priority: 1
version: 3
delegate: claude-code@spud10.local
labels: []
dependencies: []
parent_id: is-01m4h26vpd0pe8frzehv70rt4p
child_order_hints:
  - is-01m4h9vctvqc2xap8b7hb68bt0
hold: null
hold_until: null
created_at: 2026-10-09T21:40:48.440Z
updated_at: 2026-10-09T21:42:02.815Z
started_at: 2026-10-09T21:40:56.042Z
---
Final b4b127c54 push validation found Ruff smart apostrophes in test_bound_citations.py, stale site URL register/docs, and stale T-007 consumer audit after the dedicated Ahmed attribution rename and upstream integration. Reproduce at frozen source, make narrow corrections using maintained generators, preserve handles and source custody, verify lint and both generated-record checks, then requalify PR474. Track any independently confirmed fixture-lifetime failure in the same final-validation repair slice.
