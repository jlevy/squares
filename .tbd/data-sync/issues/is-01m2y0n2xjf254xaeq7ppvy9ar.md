---
type: is
id: is-01m2y0n2xjf254xaeq7ppvy9ar
title: "PR200-201 review R4: correct verified labels on float-only experiments"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:40:02.864Z
updated_at: 2026-09-20T01:51:15.316Z
closed_at: 2026-09-20T01:51:15.316Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
exp162 and exp164-170/172-178 subject assurance=verified and method=exact-algebraic overstate float64 HiGHS probes that produced no accepted certificate. Match Experiment/v2: numerically-checked, numerical-f64, actual precision/tolerance and scope. Keep successful T028-030 certificates separate and retain exact assurance only where an exact obligation was discharged.
