---
type: is
id: is-01m3yrwb9sp1hwjq783nttxdy9
title: "Results tables: a Status column holds the status chips (verified, confirmed and the rest), out of the Rungs cell; the kind stays under the rungs; check every row's status against the record"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T16:59:08.473Z
updated_at: 2026-10-02T22:41:20.010Z
closed_at: 2026-10-02T22:41:20.009Z
close_reason: "Merged in jlevy/squares#310 (03cf705ea): the status line has a Status column; statuses checked against result_status."
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'let's move "verified" and "confirmed" to a status column, and check we have this status column accurate and use that as it is really more of a status than a "rung". "optimality" is the type of the result so it can stay out of status'. In both tables of results (the Overview's Recent Results and all-results.html), the status line now under the rung chips (status_marks: confirmed, verified, recorded, superseded and the rest) becomes a Status column of its own, after Rungs: Date, Result, n, Credit, Rungs, Status, ID. The kind chip (optimality, lower bound, ...) stays under the rungs. Check each row's status against its record (result_status), so the column says what the register says; the Status filter, sorting, the phone card, the row popover and the column-width tests follow. Tests and paper-design.md updated.

## Notes

2026-10-02: committed 03cf705ea (Status column; statuses checked against result_status: 56 confirmed, 4 reviewed, 3 recorded, 2 incomplete; T-003 rightly unmarked). Widths pinned in 1fb775810 (think-e4o3). PR jlevy/squares#310 opened 2026-10-02 (head 38346bf4a); close when it merges.
