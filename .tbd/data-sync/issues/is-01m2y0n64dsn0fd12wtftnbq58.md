---
type: is
id: is-01m2y0n64dsn0fd12wtftnbq58
title: "PR200 review R6: restore structured T027 session provenance"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:06.156Z
updated_at: 2026-09-19T23:40:06.156Z
---
packing/frontier/results.yaml:1572-1573 indents produced_by/session inside the folded composition string. T027 now has no produced_by mapping; optional schema lets gates pass. Dedent produced_by to result level and session beneath it; verify parsed producer and generated consumers.
