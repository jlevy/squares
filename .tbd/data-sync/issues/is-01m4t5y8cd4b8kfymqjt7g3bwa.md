---
type: is
id: is-01m4t5y8cd4b8kfymqjt7g3bwa
title: "PR #549 A4: record every row-3 output's side so select's minimality is checkable"
kind: bug
status: open
priority: 2
version: 5
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4mdbqsgkdz008e42ffjx4ej
hold: null
hold_until: null
created_at: 2026-10-13T08:26:52.172Z
updated_at: 2026-10-13T09:07:15.373Z
started_at: 2026-10-13T08:54:58.859Z
---
Low suggestion. selection.json. Review A https://github.com/jlevy/squares/pull/549#pullrequestreview-5500738911.

## Notes

Deferred from PR #549 review A4. 296a0dd2b makes select record row_three_sides and --check hold a row's view to the least where the row shows it (34 of 59 committed rows). The other 25 rows (a same view taken over a solved one) need the solved sides, which only the run reports (full, same2, same3, ladder; not retained) hold. Waits on think-q61d (retaining each run's per-count decisions) or a re-run of select over retained runs.
