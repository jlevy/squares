---
type: is
id: is-01m4wtv34pphy5w434wk13b85x
title: Resolve four scheduled main test-time ceiling overruns without weakening assertions
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
child_order_hints:
  - is-01m4wzs72rh8db5f4mp5y8w4wr
hold: null
hold_until: null
created_at: 2026-10-14T09:10:37.460Z
updated_at: 2026-10-14T10:36:58.839Z
started_at: 2026-10-14T10:03:10.224Z
---
Optional scheduled full integration run38536321398 at f73 passes functional tests but violates12s per-test ceiling for four nodes: site_forwarders no-script redirect13.08s; results_register full-part citations T15312.17s; overview_sections no-script canonical atlas20.10s; regularized_drawings edited-block check13.44s. Main push full gate and Pages deployment passed sameSHA. Diagnose full integration contention/cold-path cost, optimize or explicitly classify measured expensive cases while preserving assertions and meaningful CI coverage; avoid broad ceiling increases.
