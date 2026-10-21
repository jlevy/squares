---
type: is
id: is-01m5g2wfw0xf50d000t9mn6wbv
title: Compare closing credits and rollup identities semantically after HTML compaction
kind: bug
status: in_progress
priority: 1
version: 2
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T20:36:46.063Z
updated_at: 2026-10-21T20:36:52.171Z
started_at: 2026-10-21T20:36:52.170Z
---
Hosted CI retains correct footer and Couzo/Fitzharding profile links but quote-sensitive assertions reject unquoted href attributes after compaction. Own only the closing-credit assertion section in packing/tests/test_overview.py and quote-sensitive finder-credit assertions in packing/tests/test_results_rollup.py. Compare parsed HTML while preserving exact text, link targets, native-navigation attributes, order and multiplicity. Verify the three hosted failures and meaningful mutation checks; run focused lint and type checks. Renderer/CLS changes belong to the frontend worker; no commit by this worker.
