---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: in_progress
priority: 2
version: 10
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-upstream-1014
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-14T17:40:53.315Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

Merged origin/main through 37e6757ed (251 commits, 19 conflicts) and pushed draft PR #578 at adc23c2d9. News uses preferred-name direct profile links; Astra review found no actionable merge/news defects. Focused profile 43, changelog 29, publishing 47, citation/case/importer 125 tests passed. Final local push gate passed all 67 prerequisites; behavioral subset timed out at 900 seconds and 77% with no assertion failures shown, so the full local gate is incomplete. Hosted CI pending at adc23c2d9. Release dispositions and derived audit/URL metadata reconciled. Census: 27 profiles, 1165 spans, 929 resolved, 6 non-person, 230 unresolved; 146 PDFs pending full inspection, no stale joins.
