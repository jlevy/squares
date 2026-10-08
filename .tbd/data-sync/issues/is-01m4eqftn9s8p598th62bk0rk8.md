---
type: is
id: is-01m4eqftn9s8p598th62bk0rk8
title: Calibrate portable control snapshot budget for retained rigidity metadata
kind: task
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m4e35s7r1e65r1qmpz250h0p
created_at: 2026-10-08T21:42:40.552Z
updated_at: 2026-10-08T21:42:40.552Z
---
The cleanup pre-push run found 201,971,305 copied worker bytes against a 192 MiB cap (201,326,592), with unchanged PDF pruning. The prior gap-export revision had only45,663 bytes headroom; most growth is564,800 bytes of structured rigidity source/date metadata in composite-figure.json, consumed by validate_schemas. Independently review the measured budget disposition, preserve scientific inputs and cap assertions, then validate the three affected controls.
