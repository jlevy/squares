---
type: is
id: is-01m4wtv34pphy5w434wk13b85x
title: Resolve four scheduled main test-time ceiling overruns without weakening assertions
kind: bug
status: in_progress
priority: 1
version: 4
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
updated_at: 2026-10-14T11:22:38.097Z
started_at: 2026-10-14T10:03:10.224Z
---
Optional scheduled full integration run38536321398 at f73 passes functional tests but violates12s per-test ceiling for four nodes: site_forwarders no-script redirect13.08s; results_register full-part citations T15312.17s; overview_sections no-script canonical atlas20.10s; regularized_drawings edited-block check13.44s. Main push full gate and Pages deployment passed sameSHA. Diagnose full integration contention/cold-path cost, optimize or explicitly classify measured expensive cases while preserving assertions and meaningful CI coverage; avoid broad ceiling increases.

## Notes

PR599 current472b72da75f0b1e9aa7ec6c84a4762cb23cddafa integrates verified main287. A-C reviews8fae; B1 fixed6c97 confirmed D5517019394, retained integration; E exact472/base287 approves10/10 files/no new findings. Bookkeeping24entries/49deliveries/36represented/13omissions/22frozen, earlier history/component editions unchanged. Full-enforced dispatch38555598547 at472 running; PRPacking38555564233/Pages38555564312/mergeability38555560096 running/passing. Completion requires actual pytest/browser fixtures and unchanged12sCALLfloor then merge and liveverification. No hosted speed claim yet. Scratch full, no internal fallback.
