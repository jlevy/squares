---
type: is
id: is-01m5k60tb3vcvhr0ezjwphzz0s
title: Consolidate result collections into canonical All Results
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: frontier-split
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
child_order_hints:
  - is-01m5k6s4z0ffnjkgnvqfppdn7j
hold: null
hold_until: null
created_at: 2026-10-23T01:29:16.886Z
updated_at: 2026-10-23T01:42:34.207Z
started_at: 2026-10-23T01:29:31.134Z
closed_at: 2026-10-23T01:41:24.668Z
close_reason: "Implemented and coordinator-published in PR #737: Frontier split and legacy queries (b64b66c2a, 6be4f08a5, 2be15b7e1, 25a704066), canonical All Results consolidation (41a3d74e5), Tutorials-first Learn and Read Papers action (cbb421dc1). Validation: 89 Frontier/URL semantic tests; 21 forwarding Node tests; 21 legacy-query/inventory browser tests; 5 Atlas default/no-JS browser cases; 2 case-consumer tests; 4 final collection/Learn semantic tests; 8 Recent Results compatibility/inventory browser tests all passed. Focused Ruff and Biome checks passed. Final integrated CI/publication remains under the parent validation bead think-kmpp."
resolution: null
duplicate_of: null
---
Replace duplicate Recent Results and Results Archive pages with one canonical All Results at results.html, preserve the sortable/filterable table and historical query/fragment links, and keep the bounded homepage preview with one All Results action.
