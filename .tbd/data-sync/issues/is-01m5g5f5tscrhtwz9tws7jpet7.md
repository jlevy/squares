---
type: is
id: is-01m5g5f5tscrhtwz9tws7jpet7
title: Reuse canonical profile context in project tally behavioral tests
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
created_at: 2026-10-21T21:21:55.543Z
updated_at: 2026-10-21T21:22:49.931Z
started_at: 2026-10-21T21:22:49.930Z
---
Hosted CI at e162a870a reports three tests in test_site_project_tallies.py exceeding the unchanged 45-second CALL guard without assertion failures. Diagnose repeated expensive test/render work and fix only this module and narrowly relevant shared fixtures, coordinating before production edits. Preserve exact project result and credit counts, links, ordering and selection coverage. Validate meaningful per-test runtimes in the existing external Python 3.14 environment. No push or PR mutations.
