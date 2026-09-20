---
type: is
id: is-01m2y0n779n5x8r0kf6xa6dfg2
title: "PR200-201 review R7: reconcile n<=100 survey census with the frontier"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:07.272Z
updated_at: 2026-09-20T01:51:15.359Z
closed_at: 2026-09-20T01:51:15.359Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
X038 survey and Session140 report32 proved/68 open; X039 repeats it. Exact frontier already marks n98,n99,n100 proved at10, yielding35 proved/65 open. Correct open interval82..100 to82..97, reconcile surveys/sessions, and derive the census with the existing frontier tooling rather than hand counts.
