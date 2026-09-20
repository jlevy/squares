---
type: is
id: is-01m2y0n64dsn0fd12wtftnbq58
title: "PR200 review R6: restore structured T027 session provenance"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:06.156Z
updated_at: 2026-09-20T01:51:15.350Z
closed_at: 2026-09-20T01:51:15.350Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
packing/frontier/results.yaml:1572-1573 indents produced_by/session inside the folded composition string. T027 now has no produced_by mapping; optional schema lets gates pass. Dedent produced_by to result level and session beneath it; verify parsed producer and generated consumers.
