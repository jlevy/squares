---
type: is
id: is-01m59kfzac51p79k9q2myr0t18
title: Include the historical writer in reviewed no-change release scopes
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-release-fix
labels: []
dependencies: []
parent_id: is-01m4v4ehd59t1r89qwksx77bmh
hold: null
hold_until: null
created_at: 2026-10-19T08:12:20.683Z
updated_at: 2026-10-19T09:09:19.420Z
started_at: 2026-10-19T08:12:27.736Z
closed_at: 2026-10-19T09:09:19.420Z
close_reason: "Reviewed fixes integrated at b76a24fd29bdab28b5c946adeff88313fd28eb47. Standard packing and publication CI passed; full checkpoint passed with 14 successful jobs and 10 intentional skips: https://github.com/jlevy/squares/actions/runs/39223503977 . Final integration review: https://github.com/jlevy/squares/pull/578#pullrequestreview-5568927630 ."
resolution: null
duplicate_of: null
---
The n29 writer repair added adopt_houses.py to two conservative paper input closures. Their existing reviewed no-public-change decisions omitted that path, so the release gate correctly refused them. Add the exact reviewed path and source-level rationale to the two decisions (25 and 53 paths), preserving editions, prior comparison limits and the strict checker.
