---
type: is
id: is-01m4ffmmj2d5xhzg8axzntn67s
title: Arm the records-tier budget with a reading at its reference shape
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
created_at: 2026-10-09T04:44:43.969Z
updated_at: 2026-10-09T20:40:31.500Z
started_at: 2026-10-09T20:39:30.176Z
---
gate-budgets.yaml records: ceiling 300s, reference jobs2/inner1/cpus2, measured_seconds null, so drift is unarmed and off-shape readings (e.g. 456s on a loaded 10-CPU host) are only reported. Measure at the reference shape on a quiet host and record it through the maintained budget workflow.
