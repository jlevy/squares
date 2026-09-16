---
type: is
id: is-01m2mdrqhcra5d9n5xhvgc6vqs
title: "PR #178 integration: animate contract imports concrete driver type"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2m4brc46s3a2pqbaqthnyz7
created_at: 2026-09-16T06:16:49.451Z
updated_at: 2026-09-16T06:17:01.401Z
closed_at: 2026-09-16T06:17:01.400Z
close_reason: Fixed in c72b968e with a structural Session Protocol; full BasedPyright floor reports 0 errors, 0 warnings, 0 notes.
resolution: null
duplicate_of: null
---
After propagating PR #175 into #178, the Python type floor found that animate_view_contract imported check_animate_view.Session under TYPE_CHECKING. Because both the script and package module names are analyzed, the two nominal Session identities made the combined SECTIONS tuple invalid. Replace the circular concrete import with a structural Protocol and verify the full BasedPyright floor at zero findings.
