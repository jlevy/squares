---
type: is
id: is-01m4cmw6hw8hra3h02c6x4zd1s
title: Improve local suite D timing without changing validation or budgets
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4bxdtbvasjn91jwhz448s7b
created_at: 2026-10-08T02:18:31.356Z
updated_at: 2026-10-08T02:18:31.356Z
---
At upper repair fc988788, native suite D passed2853 tests/5skips/1xfail but rawexit1: fresh batch/standalone equivalence14.74s exceeds native12s and tier182.67s exceeds143s. Hosted PR uses declared advisory12/hard45 and must independently pass; no context spoof or waiver. Upper invocation-local reuse improves same-node19.94→12.18 and preserves all108 complete envelopes/all distinct typed checks. Further exact scalar parsing reuse belongs lower-owned packing/devtools/squish_upper_bound_packets.py; review full strict scalar/type/frame binding and literal purity before any memo, keep each call fresh, preserve all budgets/assertions and proper layer ownership. This measured local gate gap remains open independently of the final hosted source acceptance.
