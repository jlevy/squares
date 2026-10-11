---
type: is
id: is-01m3zghkapktp8gmf06mj4v3xn
title: "Big tables: no outer border on the table itself (Recent Results, the Results page's table, the Frontier table)"
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3zgh5vhwpb57pvzhtnd5ece
created_at: 2026-10-02T23:52:42.070Z
updated_at: 2026-10-03T14:37:59.746Z
closed_at: 2026-10-03T14:37:59.736Z
close_reason: Merged in jlevy/squares#312 (c831b4ee0), after a correctness and engineering review round (419a1db5d)
resolution: null
duplicate_of: null
---
Owner, 2026-10-02: 'on the big tables (results on front page, on results page, frontier table) let's remove the outer border on the table itself, it reduces clutter'. Drop the frame around each of the three tables; the rules between rows and under the header stay. Tests and paper-design.md (Tables) follow; shots at 1280 and 390 in both schemes.
