---
type: is
id: is-01m2y0qgmwq94dk9ykh5kdhn3v
title: "PR199 review R8: reject unsupported piercing direction angles"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2y07hq7kkss9qh386q3h912
created_at: 2026-09-19T23:41:22.458Z
updated_at: 2026-09-20T01:51:15.387Z
closed_at: 2026-09-20T01:51:15.387Z
close_reason: Repaired at the cumulative tip in PR 202 (https://github.com/jlevy/squares/pull/202). Final code 8dbc1068 passed matching fast 35480879196 and dispatched deferred 35480905141 on clean merge 8ac5a340, identical Git tree, covering all 80 validation steps. Fresh exact and interval replays retain all four n=18 certificates. Original PR 199-201 heads are unchanged and are not independently merge-ready; this closure applies to the corrected tip. The separate scheduling follow-up think-1i1x remains open.
resolution: null
duplicate_of: null
---
integral_piercing.py:528-530 only checks positive angle_limit, though centre_domain assumes nonnegative cosine and sine. L2 B1 sites[(1,1)], direction_steps2, angle_limit2 produces rows[[0]], infeasible and killed_coarse_net; angle_limit1/2 yields[[1]] feasible. The centre pierces every closed unit square in the2x2 container. Reject angle_limit>1 before using first-quadrant geometry (or generalize with absolute projections), test invalid ranges. Defaults and retained certificates unaffected.
