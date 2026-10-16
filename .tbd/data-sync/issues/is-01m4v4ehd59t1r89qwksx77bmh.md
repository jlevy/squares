---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: in_progress
priority: 2
version: 17
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-upstream-next
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-16T02:33:52.155Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

15 October integration completed and pushed to draft PR #578 at 0d8daf55c. Merges c3a8edaf9 and 96fa1af1f integrate 311 commits through origin/main 6e73ef1c2: 34 initial conflicts and eight from the later reader-page landing were resolved. All 31 active hosted checks passed; gh pr checks --watch exited successfully with no failed or pending jobs. Main validation, all behavioral suites, overview, PDF and frontend checks pass. Numeric records and publication history are preserved, including upstream site v0.7.10 and proposed v0.8.0. All 41 News entries and 39 reviewed profile links survive; Markdown and MathML links convert exactly once. Homepage credits navigate directly to profiles. Census: 27 profiles, 1,349 spans, 1,032 resolved, six non-person, 311 unresolved and 146 PDFs pending. URL registry: 1,056 rows, zero failures. Hosono attribution is aligned across 152 case records and the generator; n17 is 498,343 bytes under its unchanged 500,000-byte ceiling. Astra review has no remaining findings. Latest focused checks: 69 News/changelog, one overview, 24 release impact/component and 19 data-pin release tests passed. Earlier local broad validation timed out and is not claimed green; final hosted checks establish current validation. Plan and PR handoff are updated. Returning this ongoing integration bead to open for future upstream landings; remaining population is think-m7il. No PR merge performed.
