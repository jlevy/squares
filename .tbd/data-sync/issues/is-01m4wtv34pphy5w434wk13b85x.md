---
type: is
id: is-01m4wtv34pphy5w434wk13b85x
title: Resolve four scheduled main test-time ceiling overruns without weakening assertions
kind: bug
status: in_progress
priority: 1
version: 8
spec_path: docs/project/specs/active/plan-2026-10-13-site-changelog.md
delegate: codex@spud10.local
labels: []
dependencies: []
parent_id: is-01m4vns6xeff13savsant84279
child_order_hints:
  - is-01m4wzs72rh8db5f4mp5y8w4wr
  - is-01m4x4c32d5wdje51ep66pbzmm
  - is-01m4x4c3gx5fggqnt3ha5v8gpw
  - is-01m4x5q04a41ca6rsj99gpd11d
hold: null
hold_until: null
created_at: 2026-10-14T09:10:37.460Z
updated_at: 2026-10-14T12:53:00.943Z
started_at: 2026-10-14T10:03:10.224Z
---
Optional scheduled full integration run38536321398 at f73 passes functional tests but violates12s per-test ceiling for four nodes: site_forwarders no-script redirect13.08s; results_register full-part citations T15312.17s; overview_sections no-script canonical atlas20.10s; regularized_drawings edited-block check13.44s. Main push full gate and Pages deployment passed sameSHA. Diagnose full integration contention/cold-path cost, optimize or explicitly classify measured expensive cases while preserving assertions and meaningful CI coverage; avoid broad ceiling increases.

## Notes

Final PR599 head e709021197c7cb63702e44ef2d21a64b632a5e15 integrates verified main e1f14898d549/#598. First enforced candidate472 failed real CALL floors25.20s atlas and12.10s malformed coverage while all functional assertions passed. Actual profiling led to shared exact side decoding without vertex expansion; safe whole-document serialization, sparse real clone, orientation and full forwarder mutation coverage retained. ReviewF5518136600 approves16/16 current files, B1 resolved. Normal PRPacking38565309880/Pages38565310127/mergeability38565305311 all pass. Actual full38565361504 pending, all12 workers must bind finalSHA and unchanged12sCALL floor pass. Changelog25/50/37/13/22 frozen preserves editions/source pins; merge and liveverification remain. No local heavy build: external scratch full. Short JUnit decimals include phases and are upper bounds, not unpublished exactCALL timings.
