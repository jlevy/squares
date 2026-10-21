---
type: is
id: is-01m5frh64q04x1zngbk2cmxx1q
title: Derive profile years active from credited result dates
kind: task
status: in_progress
priority: 2
version: 3
delegate: profiles_data_integration
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T17:35:49.910Z
updated_at: 2026-10-21T17:40:38.148Z
started_at: 2026-10-21T17:35:55.878Z
---
Show Years active in directory and individual profiles, derived from earliest and latest years among reviewed credited distinct results using shared result date semantics. Render single year when equal, otherwise an en-dash range; no invented year for profiles without dated results.

## Notes

Pure years_active helper implemented and tested. UI mapping must use reviewed published/established dates only; no registered/import fallback for activity. Single year, range, or unspecified. Integrated render checks pending.
