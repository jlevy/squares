---
type: is
id: is-01m3zghmwnzat781k59837wpwv
title: "Big tables: a filter at its default value reads gray, an active one black; the tally reads black"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3zgh5vhwpb57pvzhtnd5ece
created_at: 2026-10-02T23:52:43.669Z
updated_at: 2026-10-03T14:38:00.712Z
closed_at: 2026-10-03T14:38:00.711Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'make the default values like "all" gray if they are selected as they dont show any filtering active. if they are active the value shoul be black. the tallies (e.g. "324 cases") should be black as that is more important and significant'. A control showing its no-filter value (All, any, an empty field) is set in the support gray; a control that filters is set in the text colour, live as the reader changes it (table.js). The count at the bar's end ("324 cases", "7 of 65 results") is the text colour. Tests and paper-design.md follow.

## Notes

Committed 71ef614d5.
