---
type: is
id: is-01m4fkxpt2eacwcrz1sc25s00b
title: Unify the exact-replay job driver used by evand, couzo_refinement and couzo_followup reports
kind: task
status: open
priority: 3
version: 3
delegate: null
labels: []
dependencies: []
parent_id: is-01m4ekeq41zfgtf5dp8r462n05
hold: null
hold_until: null
created_at: 2026-10-09T05:59:35.490Z
updated_at: 2026-10-09T20:40:34.531Z
started_at: 2026-10-09T20:39:30.194Z
---
#469 review A3: _stable/check_certification/run_child/certify copied three times (evand_arrangement_reports.py:387-492, couzo_refinement_reports.py:229-300, couzo_followup_reports.py:704-806) and already drifting (45s vs 600s child deadline; only the new copy maps bad JSON to ReportError). Parameterize the kernel driver.
