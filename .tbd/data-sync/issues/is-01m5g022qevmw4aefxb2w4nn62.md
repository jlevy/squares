---
type: is
id: is-01m5g022qevmw4aefxb2w4nn62
title: Resolve integrated profile gate regressions
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
created_at: 2026-10-21T19:47:23.500Z
updated_at: 2026-10-21T19:47:36.583Z
started_at: 2026-10-21T19:47:36.581Z
---
Retained full push diagnostics found workbench navigation extraction omits the new GitHub SVG link, and negative-control source snapshots exceed the existing229MiB limit. Diagnose source snapshot growth and repair correct scope without masking unrelated content or merely increasing limits; frontend owns nav regression. Re-run affected tests and complete broad validation.
