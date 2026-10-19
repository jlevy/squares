---
type: is
id: is-01m59kfzac51p79k9q2myr0t18
title: Include the historical writer in reviewed no-change release scopes
kind: bug
status: in_progress
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-release-fix
labels: []
dependencies: []
parent_id: is-01m4v4ehd59t1r89qwksx77bmh
hold: null
hold_until: null
created_at: 2026-10-19T08:12:20.683Z
updated_at: 2026-10-19T08:45:50.087Z
started_at: 2026-10-19T08:12:27.736Z
---
The n29 writer repair added adopt_houses.py to two conservative paper input closures. Their existing reviewed no-public-change decisions omitted that path, so the release gate correctly refused them. Add the exact reviewed path and source-level rationale to the two decisions (25 and 53 paths), preserving editions, prior comparison limits and the strict checker.
