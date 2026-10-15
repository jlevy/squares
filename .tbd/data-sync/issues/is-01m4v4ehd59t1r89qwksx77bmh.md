---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: in_progress
priority: 2
version: 15
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-upstream-1015
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-15T19:51:00.052Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

15 October integration is pushed to draft PR #578 at b055b23c8. Merge c3a8edaf9 incorporates 306 commits through origin/main 4c9af6902, resolving 34 conflicted files. Numeric upstream records and release history are preserved. News has 39 reviewed profile links across 25 entries, and homepage News credits navigate directly to profiles. Census: 27 profiles, 1,349 spans, 1,032 resolved, six non-person, 311 unresolved and 146 PDFs pending; no stale joins. URL registry: 1,056 rows, zero failures. Initial hosted CI found three issues; 422692706 aligns 152 Hosono credits and their generator and compacts n17 to 498,343 bytes under the unchanged 500,000-byte limit. Targeted tests and scoped Ruff/BasedPyright pass; Astra review has no remaining findings. Release tests: 19 passed. Local broad push validation timed out at 900 seconds and is not a passing gate. Final hosted CI is running at b055b23c8. Plan and PR description are current; retain this bead for subsequent upstream landings.
