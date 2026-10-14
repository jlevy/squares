---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: in_progress
priority: 2
version: 9
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-upstream-1014
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-14T17:13:58.633Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

Current integration: fetched origin/main37e6757ed, merged251commits with19conflicts at b7052bdc3; release pin0ae545d25. News links think-dpvm use explicit preferred-name links and direct navigation. Astra found no actionable merge/news defect; focused profile43/changelog29/publishing47/citation-case125 tests passed, publishing47 reran on committed HEAD. Push prerequisites65/67passed; derived t007 receipt regenerated and release dispositions being refreshed before final rerun/push. Census27profiles1165spans929resolved6nonperson230unresolved146PDFpending, staleempty; URLs1026zero failures. Still local, not yet pushed.
