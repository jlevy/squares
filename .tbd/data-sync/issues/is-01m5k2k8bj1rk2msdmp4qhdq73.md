---
type: is
id: is-01m5k2k8bj1rk2msdmp4qhdq73
title: Remove obsolete Recent Results daily and weekly renderer helpers
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: followups-coordinator
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:29:26.768Z
updated_at: 2026-10-23T04:12:20.956Z
started_at: 2026-10-23T01:23:20.692Z
closed_at: 2026-10-23T04:12:20.954Z
close_reason: "Implemented in PR743: removed unused Recent Results pipeline/Atlas table script and documented focused-checks then hosted validation with concurrent review and mergeability monitoring."
resolution: null
duplicate_of: null
---
Senior review identified unused daily/weekly Recent Results renderer pipeline after replacement by one table. Remove only helpers/constants/styles proven exclusive and unused; preserve shared landed_day/added_reference and filtering utilities. Non-blocking cleanup follows the UI delivery; review actual consumers before removal.

## Notes

Additional nonblocking Astra review cleanup after Frontier split: render_overview.atlas_page still includes TABLE_SCRIPT although the bounds table moved to frontier.html. Audit actual remaining Atlas consumers and remove the table-script dependency if unused. Keep separate from release acceptance; do not delay the UI delivery. Existing scope also removes obsolete Recent daily/weekly renderer helpers only after proving no shared consumers.
